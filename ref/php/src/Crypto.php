<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * Primitives crypto (SPEC v1.0 §5.1). SHA-256 hex ; vérification ECDSA P-256 avec
 * clé publique SPKI et signature ASN.1 DER (ce que openssl attend nativement pour EC),
 * signature transportée en base64url ; key_id = SHA-256(SPKI DER).
 */
final class Crypto
{
    public static function sha256Hex(string $data): string
    {
        return hash('sha256', $data);
    }

    public static function fromB64Url(string $s): string
    {
        $t = strtr($s, '-_', '+/');
        $pad = strlen($t) % 4;
        if ($pad === 2) $t .= '==';
        elseif ($pad === 3) $t .= '=';
        return base64_decode($t, true) ?: '';
    }

    public static function b64url(string $data): string
    {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }

    /**
     * Signe un message avec une clé privée EC P-256 (PEM). openssl_sign produit
     * nativement une signature ASN.1 DER pour EC — exactement ce que verify() attend.
     * @param string $privateKeyPem PEM (BEGIN EC PRIVATE KEY / PRIVATE KEY)
     */
    public static function signB64Url(string $privateKeyPem, string $message): string
    {
        $key = openssl_pkey_get_private($privateKeyPem);
        if ($key === false) return '';
        $signature = '';
        if (!openssl_sign($message, $signature, $key, OPENSSL_ALGO_SHA256)) return '';
        return self::b64url($signature);
    }

    /** @param string $publicKeyPem PEM SPKI (BEGIN PUBLIC KEY) */
    public static function verify(string $publicKeyPem, string $message, string $signatureB64Url): bool
    {
        $key = openssl_pkey_get_public($publicKeyPem);
        if ($key === false) return false;
        $der = self::fromB64Url($signatureB64Url);
        if ($der === '') return false;
        // openssl_verify : EC + SHA-256, signature en ASN.1 DER → 1 si valide.
        return openssl_verify($message, $der, $key, OPENSSL_ALGO_SHA256) === 1;
    }

    /** key_id = SHA-256(SPKI DER), à partir d'un PEM public. */
    public static function keyIdFromPubPem(string $publicKeyPem): string
    {
        $key = openssl_pkey_get_public($publicKeyPem);
        $details = openssl_pkey_get_details($key);
        // $details['key'] est le PEM SPKI ; on reconstruit le DER pour hacher.
        $der = self::pemToDer($details['key']);
        return hash('sha256', $der);
    }

    public static function pemToDer(string $pem): string
    {
        $body = preg_replace('/-----[^-]+-----|\s+/', '', $pem) ?? '';
        return base64_decode($body, true) ?: '';
    }
}
