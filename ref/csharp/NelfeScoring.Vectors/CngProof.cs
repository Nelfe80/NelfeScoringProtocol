using System.Security.Cryptography;
using System.Text.Json.Nodes;
using NelfeScoring;

/// <summary>
/// Preuve du chemin de signature device en PRODUCTION : une clé ECDSA P-256
/// PERSISTÉE via Windows CNG/NCrypt (non exportable) signe le corps du passeport,
/// et le CoreVerifier de référence l'accepte. C'est le seul verrou technique neuf
/// de l'étape 2 (APIExpose signe avec la clé de l'appareil). `dotnet run -- cng`.
/// </summary>
static class CngProof
{
    public static int Run()
    {
        string root = FindRoot();
        var profile = JsonNode.Parse(File.ReadAllText(
            Path.Combine(root, "manifest", "profiles", "megadrive", "sonic-the-hedgehog", "1.json")))!;
        byte[] issuerSpki = Crypto.LoadSpkiDer(Path.Combine(root, "keys", "issuer.pub.pem"));
        var passport = JsonNode.Parse(File.ReadAllText(
            Path.Combine(root, "vectors", "valid.passport.json")))!.AsObject();

        Console.WriteLine("== Signature device via CNG/NCrypt (pattern APIExpose prod) ==");

        const string keyName = "Nelfe.Scoring.Device.ProofTest";
        if (CngKey.Exists(keyName)) using (var k = CngKey.Open(keyName)) k.Delete();

        var creation = new CngKeyCreationParameters
        {
            ExportPolicy = CngExportPolicies.None,          // privée NON exportable (idéal)
            KeyUsage = CngKeyUsages.Signing,
            Provider = CngProvider.MicrosoftSoftwareKeyStorageProvider,
        };
        using (CngKey.Create(CngAlgorithm.ECDsaP256, keyName, creation)) { /* persistée */ }

        try
        {
            // Réouverture PAR NOM → prouve la persistance NCrypt (l'appareil retrouve sa clé).
            using var reopened = CngKey.Open(keyName);
            using var ecdsa = new ECDsaCng(reopened);

            byte[] spki = ecdsa.ExportSubjectPublicKeyInfo();     // publique seulement
            string keyId = Crypto.KeyId(spki);                    // key_id = SHA-256(SPKI DER)

            // Reconstruire le corps signé par CETTE clé device.
            passport.Remove("signature");
            passport["device"]!["key_id"] = keyId;
            var body = passport.DeepClone().AsObject();
            body.Remove("signature");
            passport["signature"] = Crypto.SignB64Url(ecdsa, Jcs.CanonicalBytes(body));

            // Ce que fera le serveur : vérifier via le CoreVerifier avec la clé publique.
            var verdict = CoreVerifier.Verify(passport, profile, spki, issuerSpki);
            bool direct = Crypto.Verify(spki, Jcs.CanonicalBytes(body),
                                        passport["signature"]!.GetValue<string>());

            Console.WriteLine($"  clé PERSISTÉE puis rouverte : {keyName} ({reopened.Provider?.Provider})");
            Console.WriteLine($"  key_id (SHA-256 du SPKI)    : {keyId}");
            Console.WriteLine($"  signature ECDSA vérifiée    : {direct}");
            Console.WriteLine($"  CoreVerifier                : {(verdict.Ok ? "pass" : verdict.ReasonCode)}");

            bool ok = verdict.Ok && direct;
            Console.WriteLine(ok
                ? "\n✅ Un passeport signé par une clé CNG/NCrypt non exportable est accepté."
                : "\n❌ ÉCHEC");
            return ok ? 0 : 1;
        }
        finally
        {
            if (CngKey.Exists(keyName)) using (var k = CngKey.Open(keyName)) k.Delete();
        }
    }

    private static string FindRoot()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir is not null)
        {
            if (File.Exists(Path.Combine(dir.FullName, "keys", "issuer.pub.pem"))) return dir.FullName;
            dir = dir.Parent;
        }
        throw new DirectoryNotFoundException("Racine du repo introuvable (keys/issuer.pub.pem).");
    }
}
