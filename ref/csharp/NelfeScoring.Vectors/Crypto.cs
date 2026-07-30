using System.Security.Cryptography;
using System.Text;

namespace NelfeScoring;

/// <summary>
/// Primitives cryptographiques FIGÉES (SPEC v1.0 §5.1) :
///  - empreintes SHA-256 en hexadécimal minuscule ;
///  - signature device/serveur ECDSA P-256, clé publique en SPKI DER, signature en
///    ASN.1 DER (RFC 3279), le tout encodé base64url sans padding à l'extérieur ;
///  - key_id = SHA-256(SPKI_DER).
/// </summary>
public static class Crypto
{
    public static string Sha256Hex(byte[] data)
        => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();

    public static string Sha256Hex(string utf8) => Sha256Hex(Encoding.UTF8.GetBytes(utf8));

    public static string KeyId(byte[] spkiDer) => Sha256Hex(spkiDer);

    // ── base64url sans padding ────────────────────────────────────────────────
    public static string B64Url(byte[] data)
        => Convert.ToBase64String(data).TrimEnd('=').Replace('+', '-').Replace('/', '_');

    public static byte[] FromB64Url(string s)
    {
        var t = s.Replace('-', '+').Replace('_', '/');
        switch (t.Length % 4) { case 2: t += "=="; break; case 3: t += "="; break; }
        return Convert.FromBase64String(t);
    }

    // ── signature (générateur) / vérification (CoreVerifier) ──────────────────
    public static string SignB64Url(ECDsa privateKey, byte[] message)
        => B64Url(privateKey.SignData(message, HashAlgorithmName.SHA256,
                                      DSASignatureFormat.Rfc3279DerSequence));

    /// <summary>Vérifie une signature base64url (ASN.1 DER) avec une clé SPKI DER.</summary>
    public static bool Verify(byte[] spkiDer, byte[] message, string signatureB64Url)
    {
        try
        {
            using var ec = ECDsa.Create();
            ec.ImportSubjectPublicKeyInfo(spkiDer, out _);
            return ec.VerifyData(message, FromB64Url(signatureB64Url),
                                 HashAlgorithmName.SHA256, DSASignatureFormat.Rfc3279DerSequence);
        }
        catch { return false; }
    }

    /// <summary>Charge une clé privée EC depuis un PEM (pour le générateur de vecteurs).</summary>
    public static ECDsa LoadPrivate(string pemPath)
    {
        var ec = ECDsa.Create();
        ec.ImportFromPem(File.ReadAllText(pemPath));
        return ec;
    }

    /// <summary>Charge une clé et renvoie son SPKI DER (ce que le vérifieur manipule).</summary>
    public static byte[] LoadSpkiDer(string pemPath)
    {
        using var ec = ECDsa.Create();
        ec.ImportFromPem(File.ReadAllText(pemPath));
        return ec.ExportSubjectPublicKeyInfo();
    }
}
