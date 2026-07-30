<?php
declare(strict_types=1);

// Exécuteur PHP : rejoue vectors/* avec le CoreVerifier PHP et compare aux verdicts
// attendus (vectors/index.json). Doit être IDENTIQUE au CoreVerifier C#.
//   docker run --rm -v <NelfeScoringProtocol>:/app php:8.4-cli php /app/ref/php/run-vectors.php

require __DIR__ . '/src/Jcs.php';
require __DIR__ . '/src/Crypto.php';
require __DIR__ . '/src/CoreVerifier.php';

use NelfeScoring\CoreVerifier;

$root = dirname(__DIR__, 2); // ref/php -> NelfeScoringProtocol
$vectorsDir = $root . '/vectors';

$profile = json_decode((string) file_get_contents($root . '/manifest/profiles/megadrive/sonic-the-hedgehog/1.json'));
$devicePem = (string) file_get_contents($root . '/keys/device.pub.pem');
$issuerPem = (string) file_get_contents($root . '/keys/issuer.pub.pem');
$index = json_decode((string) file_get_contents($vectorsDir . '/index.json'));

$fail = 0;
echo "── CoreVerifier (port PHP) sur les vecteurs Sonic 1cc ──\n";
foreach ($index as $entry) {
    $passport = json_decode((string) file_get_contents($vectorsDir . '/' . $entry->vector));
    $r = CoreVerifier::verify($passport, $profile, $devicePem, $issuerPem);
    $got = $r['ok'] ? 'pass' : $r['reason'];
    $expected = $entry->expected; // "pass" ou reason_code
    $ok = ($got === $expected);
    if (!$ok) $fail++;
    printf("  %s %-30s attendu=%-32s obtenu=%s\n", $ok ? 'OK ' : 'XX ', $entry->vector, $expected, $got);
}
$n = count($index);
echo $fail === 0
    ? "\n✅ {$n}/{$n} — verdicts PHP IDENTIQUES au C# (le vecteur 'valid' qui passe prouve un JCS byte-identique).\n"
    : "\n❌ {$fail} divergence(s) sur {$n}.\n";
exit($fail === 0 ? 0 : 1);
