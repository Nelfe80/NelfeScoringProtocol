<?php
declare(strict_types=1);

// Exécuteur du flux de soumission SERVEUR adossé à une vraie base (SQLite en test,
// MariaDB en prod). Prouve que l'état (idempotence, ticket, révocations, held) est
// PERSISTÉ et que les scores publiés sont classés.
//   docker run --rm -v <repo>:/app php:8.4-cli php /app/ref/php/run-submission.php

require __DIR__ . '/src/Jcs.php';
require __DIR__ . '/src/Crypto.php';
require __DIR__ . '/src/CoreVerifier.php';
require __DIR__ . '/src/StateStore.php';
require __DIR__ . '/src/ServerAdmissionVerifier.php';
require __DIR__ . '/src/PdoStateStore.php';
require __DIR__ . '/src/SubmissionService.php';

use NelfeScoring\Crypto;
use NelfeScoring\PdoStateStore;
use NelfeScoring\SubmissionService;

$root = dirname(__DIR__, 2);                       // racine du repo
$devicePem = file_get_contents("$root/keys/device.pub.pem");
$issuerPem = file_get_contents("$root/keys/issuer.pub.pem");
$deviceKeyId = Crypto::keyIdFromPubPem($devicePem);
$issuerKeyId = Crypto::keyIdFromPubPem($issuerPem);
$schema = file_get_contents(__DIR__ . '/sql/schema.sql');
$profile = json_decode(file_get_contents("$root/manifest/profiles/megadrive/sonic-the-hedgehog/1.json"));

if (!in_array('sqlite', PDO::getAvailableDrivers(), true)) {
    fwrite(STDERR, "pdo_sqlite absent de cette image PHP\n");
    exit(2);
}

/** Base neuve en mémoire : schéma + device + issuer enregistrés. */
function freshDb(string $schema, string $deviceKeyId, string $devicePem, string $issuerKeyId, string $issuerPem): PDO
{
    $pdo = new PDO('sqlite::memory:');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->exec($schema);
    $pdo->prepare('INSERT INTO scoring_devices (device_id, key_id, public_key_pem) VALUES (?, ?, ?)')
        ->execute(['dev-001', $deviceKeyId, $devicePem]);
    $pdo->prepare('INSERT INTO scoring_issuers (key_id, public_key_pem) VALUES (?, ?)')
        ->execute([$issuerKeyId, $issuerPem]);
    return $pdo;
}

$profileProvider = fn(\stdClass $game): ?\stdClass =>
    ($game->rom_group ?? '') === 'sonic-the-hedgehog' ? $profile : null;

$load = fn(string $name): \stdClass => json_decode(file_get_contents("$root/vectors/$name"));
$valid = $load('valid.passport.json');

$pass = 0; $fail = 0;
function check(string $label, bool $ok, string $got): void
{
    global $pass, $fail;
    if ($ok) { $pass++; printf("  ✅ %-42s → %s\n", $label, $got); }
    else     { $fail++; printf("  ❌ %-42s → %s\n", $label, $got); }
}

echo "== Flux de soumission serveur (DB SQLite) ==\n";

// --- Cas A : première soumission valide PUIS rejeu (idempotence persistée) ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);

$r1 = $svc->submit($valid);
check('A1 valide → published (rang 1)', $r1['status'] === 'published' && ($r1['rank'] ?? 0) === 1, "{$r1['status']} rank=" . ($r1['rank'] ?? '-'));

$scoresCount = (int) $pdo->query('SELECT COUNT(*) FROM scores')->fetchColumn();
check('A2 score persisté (1 ligne dans scores)', $scoresCount === 1, "scores=$scoresCount");

$r2 = $svc->submit($valid);              // même session_id → doublon
check('A3 rejeu même session → duplicate', $r2['status'] === 'duplicate', $r2['status']);

$scoresCount = (int) $pdo->query('SELECT COUNT(*) FROM scores')->fetchColumn();
check('A4 pas de doublon en base', $scoresCount === 1, "scores=$scoresCount");

// --- Cas B : ticket déjà consommé par une AUTRE session → refused ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$pdo->prepare('INSERT INTO scoring_consumed (session_id, ticket_id, consumed_at) VALUES (?, ?, ?)')
    ->execute(['autre-session', $valid->ticket->ticket_id, gmdate('c')]);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);
$rB = $svc->submit($valid);
check('B ticket déjà utilisé → refused ticket_reused', $rB['status'] === 'refused' && $rB['reason'] === 'session.ticket_reused', "{$rB['status']}/{$rB['reason']}");

// --- Cas C : device révoqué → refused ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$pdo->prepare('UPDATE scoring_devices SET revoked_at = ? WHERE device_id = ?')->execute([gmdate('c'), 'dev-001']);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);
$rC = $svc->submit($valid);
check('C device révoqué → refused device_revoked', $rC['status'] === 'refused' && $rC['reason'] === 'session.device_revoked', "{$rC['status']}/{$rC['reason']}");

// --- Cas D : anomalie statistique → held (pas de score classé) ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$pdo->prepare('INSERT INTO scoring_stat_anomaly (session_id) VALUES (?)')->execute([$valid->session_id]);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);
$rD = $svc->submit($valid);
$heldScores = (int) $pdo->query('SELECT COUNT(*) FROM scores')->fetchColumn();
check('D anomalie statistique → held', $rD['status'] === 'held' && $heldScores === 0, "{$rD['status']} scores=$heldScores");

// --- Cas E : échec CoreVerifier remonté en refused ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);
$rE = $svc->submit($load('fail_core_mismatch.passport.json'));
check('E core_mismatch → refused (remonté)', $rE['status'] === 'refused' && $rE['reason'] === 'profile.core_mismatch', "{$rE['status']}/{$rE['reason']}");

// --- Cas F : profil inconnu (jeu non ouvert) → refused ---
$pdo = freshDb($schema, $deviceKeyId, $devicePem, $issuerKeyId, $issuerPem);
$svc = new SubmissionService($pdo, new PdoStateStore($pdo), $profileProvider);
$other = json_decode(json_encode($valid));
$other->game->rom_group = 'super-mario-world';         // pas de profil → not_open
$rF = $svc->submit($other);
check('F jeu sans profil → refused not_open', $rF['status'] === 'refused' && $rF['reason'] === 'profile.not_open', "{$rF['status']}/{$rF['reason']}");

printf("\n%s  %d/%d\n", $fail === 0 ? '✅' : '❌', $pass, $pass + $fail);
exit($fail === 0 ? 0 : 1);
