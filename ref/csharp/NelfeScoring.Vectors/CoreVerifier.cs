using System.Globalization;
using System.Text.Json.Nodes;

namespace NelfeScoring;

/// <summary>
/// CoreVerifier - implémentation de RÉFÉRENCE, déterministe et SANS ÉTAT
/// (SPEC v1.0 §6.1-6.4). Il produit `local_check` côté machine et le socle du verdict
/// côté serveur. Il ne fait AUCUN contrôle à état (révocations, ticket consommé,
/// statistiques) : ceux-là sont du ServerAdmissionVerifier (§6.5).
///
/// Entrées : le passeport, le profil signé, et les clés publiques (SPKI DER) fournies
/// - le CoreVerifier ne connaît pas d'annuaire. Sortie : Ok + reason_code (§8ter).
/// </summary>
public sealed record VerifyResult(bool Ok, string ReasonCode)
{
    public static readonly VerifyResult Pass = new(true, "");
    public static VerifyResult Fail(string code) => new(false, code);
}

public static class CoreVerifier
{
    public static VerifyResult Verify(JsonNode passport, JsonNode profile,
                                      byte[] deviceSpkiDer, byte[] issuerSpkiDer)
    {
        // ── §6.1 forme ────────────────────────────────────────────────────────
        if (I(passport, "protocol") != 1) return F("format.protocol");
        if (Str(passport, "session_id") is null) return F("format.schema");
        if (Str(passport, "device", "device_id") is null) return F("format.schema");

        // ── §6.1-4 ticket (signature serveur + temporel, sans état) ───────────
        var ticket = passport["ticket"] as JsonObject;
        if (ticket is null) return F("session.ticket_missing");
        {
            var sig = Str(ticket, "signature");
            if (sig is null) return F("session.ticket_missing");
            var body = ticket.DeepClone().AsObject();
            body.Remove("signature");
            if (!Crypto.Verify(issuerSpkiDer, Jcs.CanonicalBytes(body), sig))
                return F("session.ticket_invalid");
            if (Str(ticket, "device_id") != Str(passport, "device", "device_id"))
                return F("session.ticket_invalid");
            // ended_at ≤ expires_at (borne temporelle, auto-contenue)
            var ended = Date(passport, "timing", "ended_at");
            var expires = DateStr(Str(ticket, "expires_at"));
            if (ended is null || expires is null) return F("format.schema");
            if (ended > expires) return F("session.ticket_expired");
            // profile.manifest_epoch ≤ ticket.manifest_epoch
            if (I(profile, "manifest_epoch") > I(ticket, "manifest_epoch"))
                return F("session.ticket_invalid");
        }

        // ── §6.2 signature device sur JCS(passeport sans « signature ») ───────
        {
            var psig = Str(passport, "signature");
            if (psig is null) return F("format.schema");
            var body = passport.DeepClone().AsObject();
            body.Remove("signature");
            if (!Crypto.Verify(deviceSpkiDer, Jcs.CanonicalBytes(body), psig))
                return F("session.signature_invalid");
        }

        // ── §6.3 profil & attestation ─────────────────────────────────────────
        if (Str(passport, "game", "rom_group") != Str(profile, "rom_group")
            || Str(passport, "game", "ruleset") != Str(profile, "ruleset")
            || Str(passport, "game", "system_id") != Str(profile, "system_id"))
            return F("profile.mismatch");

        var coreLoaded = Str(passport, "artifacts", "core", "loaded_sha256");
        var contentLoaded = Str(passport, "artifacts", "content", "loaded_sha256");
        var memLoaded = Str(passport, "artifacts", "mem", "loaded_sha256");
        var listenerLoaded = Str(passport, "listener", "loaded_sha256");

        if (!InArr(profile, coreLoaded, "allowed_core_sha256")) return F("profile.core_mismatch");
        if (!InArr(profile, contentLoaded, "allowed_content_sha256")) return F("profile.content_mismatch");
        if (memLoaded != Str(profile, "mem_sha256")) return F("profile.mem_mismatch");
        if (!InArr(profile, listenerLoaded, "allowed_listener_sha256")) return F("profile.listener_unauthorized");

        // modules par rôle + digest (§6.3-10, §5.5)
        var modules = passport["software"]?["modules"] as JsonArray;
        if (modules is null) return F("format.schema");
        string? RoleHash(string role) => modules
            .FirstOrDefault(m => Str(m, "role") == role) is JsonNode m ? Str(m, "sha256") : null;
        var modulesDigest = Str(passport, "software", "modules_digest");
        if (modulesDigest != Crypto.Sha256Hex(Jcs.Canonical(modules)))
            return F("attestation.modules_digest");
        // égalités d'indépendance (§5.5)
        if (RoleHash("listener") != listenerLoaded) return F("runtime.module_unauthorized");
        if (RoleHash("real_core") != coreLoaded) return F("runtime.module_unauthorized");
        if (RoleHash("frontend") != Str(passport, "process", "executable_sha256"))
            return F("runtime.module_unauthorized");

        // le jeu était ouvert à la fin (borne statique du profil)
        var opened = DateStr(Str(profile, "opened_at"));
        var ended2 = Date(passport, "timing", "ended_at");
        if (opened is not null && ended2 is not null && ended2 < opened) return F("profile.not_open");

        // ── §6.4 cohérence & checkpoints ──────────────────────────────────────
        var started = Date(passport, "timing", "started_at");
        if (started is null || ended2 is null || ended2 <= started) return F("timing.incoherent");

        var rules = profile["rules"] as JsonObject;
        if (Bool(passport, "sensitive", "save_state_loaded") && Str(rules, "save_state") == "forbidden")
            return F("runtime.save_state_detected");
        if (Bool(passport, "sensitive", "cheats") && Str(rules, "cheats") == "forbidden")
            return F("runtime.cheat_detected");
        if (I(passport, "sensitive", "continues") > 0 && Str(rules, "continues") == "forbidden")
            return F("runtime.continue_forbidden");

        var checkpoints = passport["progression"]?["checkpoints"] as JsonArray;
        if (checkpoints is null || checkpoints.Count == 0) return F("format.schema");
        if (Str(passport, "progression", "checkpoints_digest") != Crypto.Sha256Hex(Jcs.Canonical(checkpoints)))
            return F("progression.digest_mismatch");

        var monot = Str(profile, "trajectory_policy", "monotonicity") ?? "non_decreasing";
        var corr = CorrelationRules(profile);
        long prevMetric = 0; JsonNode? prev = null; bool sawGameEnd = false;
        foreach (var cp in checkpoints)
        {
            if (cp is null) return F("format.schema");
            long metric = ParseLong(Str(cp, "metric"));
            if (monot == "non_decreasing" && metric < prevMetric) return F("progression.monotonicity");
            if (monot == "non_increasing" && metric > prevMetric && prev is not null) return F("progression.monotonicity");

            var ev = Str(cp, "event");
            if (ev == "game_end") sawGameEnd = true;
            if (ev is not null && corr.TryGetValue(ev, out var rule)
                && !CorrelationOk(rule, prev, cp, prevMetric, metric))
                return F("progression.invalid_correlation");

            prev = cp; prevMetric = metric;
        }
        if (!sawGameEnd) return F("session.no_game_end");

        // metric.value cohérente avec result_source
        var resultSource = Str(profile, "metric", "result_source") ?? "final";
        var declared = Str(passport, "metric", "value");
        var expected = resultSource switch
        {
            "final" => Str(checkpoints[^1], "metric"),
            "best" or "max" => checkpoints.Max(c => ParseLong(Str(c, "metric"))).ToString(),
            "min" => checkpoints.Min(c => ParseLong(Str(c, "metric"))).ToString(),
            _ => declared
        };
        if (declared != expected) return F("format.out_of_bounds");

        return VerifyResult.Pass;
    }

    // ── corrélations ──────────────────────────────────────────────────────────
    private sealed record Rule(string Event, string[] Requires, string[] RequiresAny);

    private static Dictionary<string, Rule> CorrelationRules(JsonNode profile)
    {
        var d = new Dictionary<string, Rule>();
        if (profile["correlation_rules"] is JsonArray arr)
            foreach (var r in arr)
                if (Str(r, "event") is string ev)
                    d[ev] = new Rule(ev, StrArr(r, "requires"), StrArr(r, "requires_any"));
        return d;
    }

    private static bool CorrelationOk(Rule rule, JsonNode? prev, JsonNode cur, long prevMetric, long metric)
    {
        bool Token(string t) => t switch
        {
            "score_delta" => metric != prevMetric,
            "rings_delta" => Counter(cur, "rings") != Counter(prev, "rings"),
            "level_delta" => Counter(cur, "level") != Counter(prev, "level"),
            "lives_delta" => Counter(cur, "lives") != Counter(prev, "lives"),
            "time_checkpoint" => prev is null || Long(cur, "t_ms") > Long(prev, "t_ms"),
            _ => false
        };
        if (rule.Requires.Length > 0 && !rule.Requires.All(Token)) return false;
        if (rule.RequiresAny.Length > 0 && !rule.RequiresAny.Any(Token)) return false;
        return true;
    }

    // ── helpers d'accès JsonNode ───────────────────────────────────────────────
    private static VerifyResult F(string code) => VerifyResult.Fail(code);

    private static JsonNode? Nav(JsonNode? n, string[] path)
    {
        foreach (var p in path) { if (n is null) return null; n = n[p]; }
        return n;
    }
    private static string? Str(JsonNode? n, params string[] path)
        => Nav(n, path) is JsonNode v && v.GetValueKind() == System.Text.Json.JsonValueKind.String ? v.GetValue<string>() : null;
    private static long I(JsonNode? n, params string[] path)
    {
        var v = Nav(n, path);
        return v is not null && v.GetValueKind() == System.Text.Json.JsonValueKind.Number
            && long.TryParse(v.ToJsonString(), NumberStyles.Integer, CultureInfo.InvariantCulture, out var l)
            ? l : long.MinValue;
    }
    private static long Long(JsonNode? n, string key) => I(n, key);
    private static bool Bool(JsonNode? n, params string[] path)
        => Nav(n, path) is JsonNode v && v.GetValueKind() == System.Text.Json.JsonValueKind.True;
    private static long Counter(JsonNode? cp, string key)
    {
        var v = cp?["counters"]?[key];
        return v is not null && v.GetValueKind() == System.Text.Json.JsonValueKind.Number
            && long.TryParse(v.ToJsonString(), NumberStyles.Integer, CultureInfo.InvariantCulture, out var l)
            ? l : 0;
    }
    private static bool InArr(JsonNode? n, string? val, string key)
        => val is not null && n?[key] is JsonArray a && a.Any(x => x?.GetValue<string>() == val);
    private static string[] StrArr(JsonNode? n, string key)
        => n?[key] is JsonArray a ? a.Select(x => x!.GetValue<string>()).ToArray() : Array.Empty<string>();
    private static long ParseLong(string? s) => long.TryParse(s, NumberStyles.None, CultureInfo.InvariantCulture, out var l) ? l : long.MinValue;
    private static DateTimeOffset? Date(JsonNode? n, params string[] path) => DateStr(Str(n, path));
    private static DateTimeOffset? DateStr(string? s)
        => s is not null && DateTimeOffset.TryParse(s, CultureInfo.InvariantCulture, DateTimeStyles.RoundtripKind, out var d) ? d : null;
}
