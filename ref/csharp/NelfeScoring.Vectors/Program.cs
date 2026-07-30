using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Nodes;
using NelfeScoring;

// ─────────────────────────────────────────────────────────────────────────────
// Lot 0 — générateur + exécuteur de vecteurs de test (SPEC v1.0).
// 1) construit le profil Sonic 1cc + un passeport VALIDE signé (device + ticket),
// 2) en dérive des mutations à verdict connu,
// 3) exécute le CoreVerifier de référence et compare au verdict attendu.
// Sortie non nulle si un seul verdict diverge.
// ─────────────────────────────────────────────────────────────────────────────

string root = FindRoot();
string keys = Path.Combine(root, "keys");
string vectorsDir = Path.Combine(root, "vectors");
string profileDir = Path.Combine(root, "manifest", "profiles", "megadrive", "sonic-the-hedgehog");
Directory.CreateDirectory(vectorsDir);
Directory.CreateDirectory(profileDir);

using var deviceKey = Crypto.LoadPrivate(Path.Combine(keys, "device.key.pem"));
using var issuerKey = Crypto.LoadPrivate(Path.Combine(keys, "issuer.key.pem"));
byte[] deviceSpki = Crypto.LoadSpkiDer(Path.Combine(keys, "device.pub.pem"));
byte[] issuerSpki = Crypto.LoadSpkiDer(Path.Combine(keys, "issuer.pub.pem"));
string deviceKeyId = Crypto.KeyId(deviceSpki);
string issuerKeyId = Crypto.KeyId(issuerSpki);

// Empreintes de test : cohérentes entre profil et passeport (les vrais binaires ne
// sont pas ici — on hache des libellés stables, ça reste des SHA-256 valides).
string H(string label) => Crypto.Sha256Hex(label);
string coreH = H("genesis_plus_gx_libretro.dll@v1");
string contentH = H("Sonic The Hedgehog (USA, Europe).md");
string memH = H("sonic_megadrive.mem@v1");
string listenerH = H("NelfeMemoryListener@4.2.0");
string frontendH = H("retroarch.exe@1.19");
string apiexposeH = H("apiexpose@1.3.6");
string hookH = H("APIExpose-start-wait.bat@v1");
string emuLauncherH = H("emulatorlauncher.exe@v1");

// ── PROFIL Sonic 1cc ──────────────────────────────────────────────────────────
var profile = new JsonObject
{
    ["system_id"] = "megadrive",
    ["rom_group"] = "sonic-the-hedgehog",
    ["engine"] = "libretro",
    ["ruleset"] = "1cc",
    ["version"] = 1,
    ["manifest_epoch"] = 12,
    ["published_at"] = "2026-07-01T00:00:00Z",
    ["opened_at"] = "2026-07-01T00:00:00Z",
    ["metric"] = new JsonObject { ["type"] = "score", ["unit"] = "points", ["ranking_direction"] = "higher_better", ["result_source"] = "final" },
    ["trajectory_policy"] = new JsonObject { ["monotonicity"] = "non_decreasing" },
    ["allowed_content_sha256"] = new JsonArray { contentH },
    ["allowed_core_sha256"] = new JsonArray { coreH },
    ["allowed_listener_sha256"] = new JsonArray { listenerH },
    ["mem_sha256"] = memH,
    ["bios"] = new JsonObject { ["mode"] = "none" },
    ["rules"] = new JsonObject
    {
        ["save_state"] = "forbidden", ["cheats"] = "forbidden", ["rewind"] = "forbidden",
        ["runahead"] = "forbidden", ["continues"] = "forbidden", ["players"] = 1
    },
    ["correlation_rules"] = new JsonArray
    {
        new JsonObject { ["event"] = "ring_collected", ["requires_any"] = new JsonArray { "score_delta", "rings_delta" } },
        new JsonObject { ["event"] = "level_complete", ["requires"] = new JsonArray { "level_delta", "time_checkpoint" } }
    }
};
File.WriteAllText(Path.Combine(profileDir, "1.json"), Pretty(profile));

// ── PASSEPORT valide (non signé) ──────────────────────────────────────────────
JsonArray Checkpoints() => new()
{
    Cp(5000, 300, "100", "ring_collected", 3, 1, 1),
    Cp(42000, 2520, "28400", "level_complete", 3, 2, 0),
    Cp(90000, 5400, "50000", "ring_collected", 2, 2, 5),
    Cp(115000, 6900, "14523400", "game_end", 0, 3, 0)
};

JsonObject BuildUnsigned()
{
    var modules = new JsonArray
    {
        new JsonObject { ["role"] = "frontend", ["sha256"] = frontendH },
        new JsonObject { ["role"] = "listener", ["sha256"] = listenerH },
        new JsonObject { ["role"] = "real_core", ["sha256"] = coreH },
        new JsonObject { ["role"] = "apiexpose", ["sha256"] = apiexposeH },
        new JsonObject { ["role"] = "emulatorlauncher", ["sha256"] = emuLauncherH },
        new JsonObject { ["role"] = "gamescript_hook", ["sha256"] = hookH }
    };
    var checkpoints = Checkpoints();

    var ticket = new JsonObject
    {
        ["ticket_id"] = "t_9f2a3b", ["device_id"] = "dev-001", ["scope"] = "scoring_session",
        ["manifest_epoch"] = 12,
        ["issued_at"] = "2026-07-30T18:00:00Z", ["expires_at"] = "2026-07-30T20:00:00Z",
        ["nonce"] = "n_abc123", ["issuer_key_id"] = issuerKeyId
    };

    return new JsonObject
    {
        ["protocol"] = 1,
        ["session_id"] = "b3f1c2a4-5d6e-4f80-9a1b-2c3d4e5f6071",
        ["ticket"] = ticket,
        ["game"] = new JsonObject
        {
            ["system_id"] = "megadrive", ["rom_group"] = "sonic-the-hedgehog",
            ["engine"] = "libretro", ["ruleset"] = "1cc", ["profile_version"] = 1,
            ["manifest_commit"] = "a1b2c3d4e5f6", ["profile_document_sha256"] = Crypto.Sha256Hex(Jcs.Canonical(profile))
        },
        ["device"] = new JsonObject { ["device_id"] = "dev-001", ["key_id"] = deviceKeyId, ["key_type"] = "ecdsa_p256" },
        ["identity"] = new JsonObject { ["player_ref"] = null, ["session_player_id"] = null },
        ["listener"] = new JsonObject { ["build"] = "4.2.0", ["start_sha256"] = listenerH, ["loaded_sha256"] = listenerH, ["end_sha256"] = listenerH, ["certification"] = "listener-tests-2026.1" },
        ["software"] = new JsonObject { ["modules"] = modules, ["modules_digest"] = Crypto.Sha256Hex(Jcs.Canonical(modules)) },
        ["artifacts"] = new JsonObject
        {
            ["core"] = HashTriple(coreH), ["content"] = HashTriple(contentH), ["mem"] = HashTriple(memH),
            ["core_options_digest"] = H("core-options@default"), ["bios"] = new JsonObject { ["mode"] = "none" }
        },
        ["process"] = new JsonObject
        {
            ["pid"] = 12345, ["executable_sha256"] = frontendH, ["parent_pid"] = 6789,
            ["created_at"] = "2026-07-30T18:40:11Z",
            ["open_files"] = new JsonArray
            {
                new JsonObject { ["role"] = "content", ["identity"] = "vol1:file:1001" },
                new JsonObject { ["role"] = "mem", ["identity"] = "vol1:file:1002" },
                new JsonObject { ["role"] = "core", ["identity"] = "vol1:file:1003" }
            }
        },
        ["timing"] = new JsonObject { ["started_at"] = "2026-07-30T18:40:12Z", ["ended_at"] = "2026-07-30T18:42:07Z", ["monotonic_ms"] = 115000, ["frame_count"] = 6900 },
        ["sensitive"] = new JsonObject { ["cheats"] = false, ["save_state_loaded"] = false, ["resets"] = 0, ["rewind"] = false, ["runahead"] = false, ["fast_forward"] = false, ["netplay"] = false, ["continues"] = 0 },
        ["metric"] = new JsonObject { ["type"] = "score", ["unit"] = "points", ["value"] = "14523400", ["ranking_direction"] = "higher_better", ["result_source"] = "final" },
        ["progression"] = new JsonObject { ["checkpoints"] = checkpoints, ["checkpoints_digest"] = Crypto.Sha256Hex(Jcs.Canonical(checkpoints)) },
        ["local_check"] = "pass"
    };
}

// Signe le ticket (issuer) puis le passeport (device). Renvoie le passeport signé.
JsonObject Sign(JsonObject unsigned)
{
    var ticket = unsigned["ticket"]!.AsObject();
    ticket.Remove("signature");
    ticket["signature"] = Crypto.SignB64Url(issuerKey, Jcs.CanonicalBytes(ticket));

    var body = unsigned.DeepClone().AsObject();
    body.Remove("signature");
    unsigned["signature"] = Crypto.SignB64Url(deviceKey, Jcs.CanonicalBytes(body));
    return unsigned;
}

// Recalcule le digest des checkpoints après mutation.
void RefreshCheckpointsDigest(JsonObject p)
{
    var cps = p["progression"]!["checkpoints"]!.AsArray();
    p["progression"]!["checkpoints_digest"] = Crypto.Sha256Hex(Jcs.Canonical(cps));
}

// ── VECTEURS ──────────────────────────────────────────────────────────────────
var vectors = new List<(string name, string expected, JsonObject p)>();
void Add(string name, string expected, Action<JsonObject> mutate, bool refreshDigest = true, bool sign = true, Action<JsonObject>? postSign = null)
{
    var p = BuildUnsigned();
    mutate(p);
    if (refreshDigest) RefreshCheckpointsDigest(p);
    if (sign) Sign(p);
    postSign?.Invoke(p);
    vectors.Add((name, expected, p));
}

Add("valid", "", _ => { });
Add("fail_core_mismatch", "profile.core_mismatch", p => p["artifacts"]!["core"]!["loaded_sha256"] = H("wrong_core"));
Add("fail_mem_mismatch", "profile.mem_mismatch", p => p["artifacts"]!["mem"]!["loaded_sha256"] = H("wrong_mem"));
Add("fail_listener_unauthorized", "profile.listener_unauthorized", p => p["listener"]!["loaded_sha256"] = H("rogue_listener"));
Add("fail_save_state", "runtime.save_state_detected", p => p["sensitive"]!["save_state_loaded"] = true);
Add("fail_continue", "runtime.continue_forbidden", p => p["sensitive"]!["continues"] = 1);
Add("fail_monotonicity", "progression.monotonicity", p => p["progression"]!["checkpoints"]![2]!["metric"] = "20000"); // 28400 -> 20000
Add("fail_correlation", "progression.invalid_correlation", p => p["progression"]!["checkpoints"]![1]!["counters"]!["level"] = 1); // level_complete sans level_delta
Add("fail_digest_mismatch", "progression.digest_mismatch", p => p["progression"]!["checkpoints"]![0]!["metric"] = "999", refreshDigest: false);
Add("fail_ticket_expired", "session.ticket_expired", p => p["ticket"]!["expires_at"] = "2026-07-30T18:41:00Z"); // avant ended_at 18:42:07
Add("fail_signature_invalid", "session.signature_invalid", _ => { }, postSign: p =>
{
    var s = p["signature"]!.GetValue<string>().ToCharArray();
    s[0] = s[0] == 'A' ? 'B' : 'A';
    p["signature"] = new string(s);
});

// ── EXÉCUTION ─────────────────────────────────────────────────────────────────
int failures = 0;
var index = new JsonArray();
Console.WriteLine("── CoreVerifier (référence C#) sur les vecteurs Sonic 1cc ──");
foreach (var (name, expected, p) in vectors)
{
    File.WriteAllText(Path.Combine(vectorsDir, name + ".passport.json"), Pretty(p));
    var r = CoreVerifier.Verify(p, profile, deviceSpki, issuerSpki);
    var got = r.Ok ? "" : r.ReasonCode;
    bool ok = got == expected;
    if (!ok) failures++;
    index.Add(new JsonObject { ["vector"] = name + ".passport.json", ["expected"] = expected == "" ? "pass" : expected });
    Console.WriteLine($"  {(ok ? "OK  " : "XX  ")}{name,-30} attendu={(expected == "" ? "pass" : expected),-32} obtenu={(got == "" ? "pass" : got)}");
}
File.WriteAllText(Path.Combine(vectorsDir, "index.json"), Pretty(index));

Console.WriteLine($"\ndevice key_id = {deviceKeyId}\nissuer key_id = {issuerKeyId}");
Console.WriteLine(failures == 0
    ? $"\n✅ {vectors.Count}/{vectors.Count} vecteurs au verdict attendu. Vecteurs écrits dans /vectors."
    : $"\n❌ {failures} divergence(s) sur {vectors.Count}.");
return failures == 0 ? 0 : 1;

// ── utilitaires ───────────────────────────────────────────────────────────────
static JsonObject HashTriple(string h) => new() { ["start_sha256"] = h, ["loaded_sha256"] = h, ["end_sha256"] = h };
static JsonObject Cp(int tms, int frame, string metric, string ev, int lives, int level, int rings) => new()
{
    ["t_ms"] = tms, ["frame"] = frame, ["metric"] = metric, ["event"] = ev,
    ["counters"] = new JsonObject { ["lives"] = lives, ["level"] = level, ["rings"] = rings }
};
static string Pretty(JsonNode n) => n.ToJsonString(new JsonSerializerOptions(JsonSerializerOptions.Default) { WriteIndented = true });
static string FindRoot()
{
    var d = new DirectoryInfo(AppContext.BaseDirectory);
    while (d is not null && !Directory.Exists(Path.Combine(d.FullName, "keys"))) d = d.Parent;
    return d?.FullName ?? throw new DirectoryNotFoundException("racine NelfeScoringProtocol (dossier 'keys') introuvable");
}
