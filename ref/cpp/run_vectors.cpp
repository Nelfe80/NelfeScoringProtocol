// CoreVerifier - port C++ de RÉFÉRENCE (SPEC v1.0 §6.1-6.4). Côté listener/protocole.
// DOIT donner exactement le même verdict que C# et PHP sur vectors/*.
// Build (Docker) :
//   g++ -std=c++20 -O2 ref/cpp/run_vectors.cpp -lssl -lcrypto -o rv && ./rv
//
// Dates : toutes en ISO-8601 UTC fixe ("....Z") -> comparaison lexicographique =
// chronologique (mêmes verdicts que DateTimeOffset/strtotime). Objets nlohmann::json
// (std::map) triés par octets = tri UTF-16 pour clés ASCII (tout le contrat).

#include <nlohmann/json.hpp>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <algorithm>
#include <climits>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

using json = nlohmann::json;

// ── JCS (RFC 8785) ───────────────────────────────────────────────────────────
static void jcsString(const std::string& s, std::string& out) {
    out += '"';
    for (unsigned char c : s) {
        switch (c) {
            case '"':  out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\b': out += "\\b"; break;
            case '\f': out += "\\f"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (c < 0x20) { char b[8]; std::snprintf(b, sizeof b, "\\u%04x", c); out += b; }
                else out += static_cast<char>(c);
        }
    }
    out += '"';
}
static void jcsWrite(const json& j, std::string& out) {
    if (j.is_null()) { out += "null"; return; }
    if (j.is_boolean()) { out += j.get<bool>() ? "true" : "false"; return; }
    if (j.is_number_integer()) { out += std::to_string(j.get<long long>()); return; }
    if (j.is_number_float()) throw std::runtime_error("float non entier");
    if (j.is_string()) { jcsString(j.get<std::string>(), out); return; }
    if (j.is_array()) {
        out += '['; bool f = true;
        for (const auto& e : j) { if (!f) out += ','; f = false; jcsWrite(e, out); }
        out += ']'; return;
    }
    // objet : nlohmann::json (std::map) est déjà trié par clé (octets)
    out += '{'; bool f = true;
    for (auto it = j.begin(); it != j.end(); ++it) {
        if (!f) out += ','; f = false;
        jcsString(it.key(), out); out += ':'; jcsWrite(it.value(), out);
    }
    out += '}';
}
static std::string jcs(const json& j) { std::string o; jcsWrite(j, o); return o; }

// ── crypto (OpenSSL) ─────────────────────────────────────────────────────────
static std::string sha256hex(const std::string& d) {
    unsigned char md[EVP_MAX_MD_SIZE]; unsigned int len = 0;
    EVP_Digest(d.data(), d.size(), md, &len, EVP_sha256(), nullptr);
    static const char* hx = "0123456789abcdef";
    std::string s; s.reserve(len * 2);
    for (unsigned i = 0; i < len; ++i) { s += hx[md[i] >> 4]; s += hx[md[i] & 15]; }
    return s;
}
static std::vector<unsigned char> b64urlDecode(const std::string& in) {
    static const std::string t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    std::vector<unsigned char> out; int buf = 0, bits = 0;
    for (char ch : in) {
        char c = ch == '-' ? '+' : ch == '_' ? '/' : ch;
        auto p = t.find(c); if (p == std::string::npos) continue;
        buf = (buf << 6) | static_cast<int>(p); bits += 6;
        if (bits >= 8) { bits -= 8; out.push_back((buf >> bits) & 0xFF); }
    }
    return out;
}
static EVP_PKEY* loadPubPem(const std::string& path) {
    FILE* f = std::fopen(path.c_str(), "r"); if (!f) return nullptr;
    EVP_PKEY* k = PEM_read_PUBKEY(f, nullptr, nullptr, nullptr); std::fclose(f); return k;
}
static bool verifySig(EVP_PKEY* key, const std::string& msg, const std::string& sigB64Url) {
    if (!key) return false;
    auto der = b64urlDecode(sigB64Url); if (der.empty()) return false;
    EVP_MD_CTX* ctx = EVP_MD_CTX_new(); bool ok = false;
    if (EVP_DigestVerifyInit(ctx, nullptr, EVP_sha256(), nullptr, key) == 1)
        ok = EVP_DigestVerify(ctx, der.data(), der.size(),
                              reinterpret_cast<const unsigned char*>(msg.data()), msg.size()) == 1;
    EVP_MD_CTX_free(ctx); return ok;
}

// ── accès json ───────────────────────────────────────────────────────────────
static const json* at(const json& n, std::vector<std::string> path) {
    const json* c = &n;
    for (auto& p : path) { if (!c->is_object()) return nullptr; auto it = c->find(p); if (it == c->end()) return nullptr; c = &*it; }
    return c;
}
static std::string S(const json& n, std::vector<std::string> path) { auto* v = at(n, path); return (v && v->is_string()) ? v->get<std::string>() : std::string(); }
static long long I(const json& n, std::vector<std::string> path) { auto* v = at(n, path); return (v && v->is_number_integer()) ? v->get<long long>() : LLONG_MIN; }
static bool B(const json& n, std::vector<std::string> path) { auto* v = at(n, path); return v && v->is_boolean() && v->get<bool>(); }
static long long counter(const json* cp, const std::string& k) {
    if (!cp) return 0; auto* c = at(*cp, {"counters", k}); return (c && c->is_number_integer()) ? c->get<long long>() : 0;
}
static bool inArr(const json& profile, const std::string& val, const std::string& key) {
    auto* a = at(profile, {key}); if (!a || !a->is_array()) return false;
    for (const auto& e : *a) if (e.is_string() && e.get<std::string>() == val) return true;
    return false;
}

struct Result { bool ok; std::string reason; };
static Result F(const std::string& c) { return {false, c}; }

// ── CoreVerifier ─────────────────────────────────────────────────────────────
static Result verify(const json& p, const json& profile, EVP_PKEY* devKey, EVP_PKEY* issKey) {
    // §6.1 forme
    if (I(p, {"protocol"}) != 1) return F("format.protocol");
    if (S(p, {"session_id"}).empty()) return F("format.schema");
    if (S(p, {"device", "device_id"}).empty()) return F("format.schema");

    // §6.1-4 ticket
    auto* ticket = at(p, {"ticket"}); if (!ticket || !ticket->is_object()) return F("session.ticket_missing");
    std::string tsig = S(*ticket, {"signature"}); if (tsig.empty()) return F("session.ticket_missing");
    { json tb = *ticket; tb.erase("signature");
      if (!verifySig(issKey, jcs(tb), tsig)) return F("session.ticket_invalid"); }
    if (S(*ticket, {"device_id"}) != S(p, {"device", "device_id"})) return F("session.ticket_invalid");
    std::string ended = S(p, {"timing", "ended_at"}), expires = S(*ticket, {"expires_at"});
    if (ended.empty() || expires.empty()) return F("format.schema");
    if (ended > expires) return F("session.ticket_expired");
    if (I(profile, {"manifest_epoch"}) > I(*ticket, {"manifest_epoch"})) return F("session.ticket_invalid");

    // §6.2 signature device
    std::string psig = S(p, {"signature"}); if (psig.empty()) return F("format.schema");
    { json body = p; body.erase("signature");
      if (!verifySig(devKey, jcs(body), psig)) return F("session.signature_invalid"); }

    // §6.3 profil
    if (S(p, {"game", "rom_group"}) != S(profile, {"rom_group"})
        || S(p, {"game", "ruleset"}) != S(profile, {"ruleset"})
        || S(p, {"game", "system_id"}) != S(profile, {"system_id"}))
        return F("profile.mismatch");

    std::string coreL = S(p, {"artifacts", "core", "loaded_sha256"});
    std::string contentL = S(p, {"artifacts", "content", "loaded_sha256"});
    std::string memL = S(p, {"artifacts", "mem", "loaded_sha256"});
    std::string listL = S(p, {"listener", "loaded_sha256"});
    if (!inArr(profile, coreL, "allowed_core_sha256")) return F("profile.core_mismatch");
    if (!inArr(profile, contentL, "allowed_content_sha256")) return F("profile.content_mismatch");
    if (memL != S(profile, {"mem_sha256"})) return F("profile.mem_mismatch");
    if (!inArr(profile, listL, "allowed_listener_sha256")) return F("profile.listener_unauthorized");

    auto* modules = at(p, {"software", "modules"}); if (!modules || !modules->is_array()) return F("format.schema");
    auto roleHash = [&](const std::string& role) -> std::string {
        for (const auto& m : *modules) if (m.contains("role") && m["role"] == role && m.contains("sha256")) return m["sha256"].get<std::string>();
        return "";
    };
    if (S(p, {"software", "modules_digest"}) != sha256hex(jcs(*modules))) return F("attestation.modules_digest");
    if (roleHash("listener") != listL) return F("runtime.module_unauthorized");
    if (roleHash("real_core") != coreL) return F("runtime.module_unauthorized");
    if (roleHash("frontend") != S(p, {"process", "executable_sha256"})) return F("runtime.module_unauthorized");

    std::string opened = S(profile, {"opened_at"});
    if (!opened.empty() && !ended.empty() && ended < opened) return F("profile.not_open");

    // §6.4 cohérence & checkpoints
    std::string started = S(p, {"timing", "started_at"});
    if (started.empty() || ended.empty() || ended <= started) return F("timing.incoherent");

    if (B(p, {"sensitive", "save_state_loaded"}) && S(profile, {"rules", "save_state"}) == "forbidden") return F("runtime.save_state_detected");
    if (B(p, {"sensitive", "cheats"}) && S(profile, {"rules", "cheats"}) == "forbidden") return F("runtime.cheat_detected");
    if (I(p, {"sensitive", "continues"}) > 0 && S(profile, {"rules", "continues"}) == "forbidden") return F("runtime.continue_forbidden");

    auto* cps = at(p, {"progression", "checkpoints"}); if (!cps || !cps->is_array() || cps->empty()) return F("format.schema");
    if (S(p, {"progression", "checkpoints_digest"}) != sha256hex(jcs(*cps))) return F("progression.digest_mismatch");

    std::string monot = S(profile, {"trajectory_policy", "monotonicity"}); if (monot.empty()) monot = "non_decreasing";
    // règles de corrélation
    struct Rule { std::vector<std::string> req, any; };
    std::map<std::string, Rule> corr;
    if (auto* cr = at(profile, {"correlation_rules"}); cr && cr->is_array())
        for (const auto& r : *cr) if (r.contains("event")) {
            Rule ru;
            if (r.contains("requires")) for (const auto& t : r["requires"]) ru.req.push_back(t.get<std::string>());
            if (r.contains("requires_any")) for (const auto& t : r["requires_any"]) ru.any.push_back(t.get<std::string>());
            corr[r["event"].get<std::string>()] = ru;
        }

    long long prevMetric = 0; const json* prev = nullptr; bool sawEnd = false;
    for (const auto& cp : *cps) {
        long long metric = std::stoll(S(cp, {"metric"}).empty() ? "0" : S(cp, {"metric"}));
        if (monot == "non_decreasing" && metric < prevMetric) return F("progression.monotonicity");
        if (monot == "non_increasing" && prev && metric > prevMetric) return F("progression.monotonicity");
        std::string ev = S(cp, {"event"});
        if (ev == "game_end") sawEnd = true;
        auto rit = corr.find(ev);
        if (!ev.empty() && rit != corr.end()) {
            auto tok = [&](const std::string& t) -> bool {
                if (t == "score_delta") return metric != prevMetric;
                if (t == "rings_delta") return counter(&cp, "rings") != counter(prev, "rings");
                if (t == "level_delta") return counter(&cp, "level") != counter(prev, "level");
                if (t == "lives_delta") return counter(&cp, "lives") != counter(prev, "lives");
                if (t == "time_checkpoint") return !prev || I(cp, {"t_ms"}) > I(*prev, {"t_ms"});
                return false;
            };
            bool ok = true;
            for (auto& t : rit->second.req) if (!tok(t)) ok = false;
            if (!rit->second.any.empty()) { bool a = false; for (auto& t : rit->second.any) if (tok(t)) a = true; if (!a) ok = false; }
            if (!ok) return F("progression.invalid_correlation");
        }
        prev = &cp; prevMetric = metric;
    }
    if (!sawEnd) return F("session.no_game_end");

    std::string rs = S(profile, {"metric", "result_source"}); if (rs.empty()) rs = "final";
    std::string declared = S(p, {"metric", "value"});
    std::string expected;
    if (rs == "final") expected = S((*cps)[cps->size() - 1], {"metric"});
    else if (rs == "best" || rs == "max" || rs == "min") {
        long long best = (rs == "min") ? LLONG_MAX : LLONG_MIN;
        for (const auto& c : *cps) { long long v = std::stoll(S(c, {"metric"})); best = (rs == "min") ? std::min(best, v) : std::max(best, v); }
        expected = std::to_string(best);
    } else expected = declared;
    if (declared != expected) return F("format.out_of_bounds");

    return {true, ""};
}

// ── main ─────────────────────────────────────────────────────────────────────
static json load(const std::string& path) { std::ifstream f(path); std::stringstream ss; ss << f.rdbuf(); return json::parse(ss.str()); }
static std::string readAll(const std::string& path) { std::ifstream f(path); std::stringstream ss; ss << f.rdbuf(); return ss.str(); }

int main(int argc, char** argv) {
    std::string root = argc > 1 ? argv[1] : ".";
    json profile = load(root + "/manifest/profiles/megadrive/sonic-the-hedgehog/1.json");
    EVP_PKEY* dev = loadPubPem(root + "/keys/device.pub.pem");
    EVP_PKEY* iss = loadPubPem(root + "/keys/issuer.pub.pem");
    json index = load(root + "/vectors/index.json");

    int fail = 0;
    std::cout << "── CoreVerifier (port C++) sur les vecteurs Sonic 1cc ──\n";
    for (const auto& e : index) {
        std::string name = e["vector"].get<std::string>();
        std::string expected = e["expected"].get<std::string>();
        json p = load(root + "/vectors/" + name);
        Result r = verify(p, profile, dev, iss);
        std::string got = r.ok ? "pass" : r.reason;
        bool ok = (got == expected);
        if (!ok) ++fail;
        std::printf("  %s %-38s attendu=%-32s obtenu=%s\n", ok ? "OK " : "XX ", name.c_str(), expected.c_str(), got.c_str());
    }
    if (fail == 0)
        std::printf("\n✅ %zu/%zu - verdicts C++ IDENTIQUES au C#/PHP (JCS byte-identique prouve par la signature).\n",
                    index.size(), index.size());
    else
        std::printf("\n❌ %d divergence(s) sur %zu.\n", fail, index.size());
    EVP_PKEY_free(dev); EVP_PKEY_free(iss);
    return fail == 0 ? 0 : 1;
}
