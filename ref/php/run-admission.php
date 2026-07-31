<?php
declare(strict_types=1);

// Exécuteur du ServerAdmissionVerifier (§6.5) : vérifie que la couche À ÉTAT produit
// le bon verdict (published / held / refused / duplicate) sur des états configurés.
//   docker run --rm -v <repo>:/app php:8.4-cli php /app/ref/php/run-admission.php

require __DIR__ . '/src/Jcs.php';
require __DIR__ . '/src/Crypto.php';
require __DIR__ . '/src/CoreVerifier.php';
require __DIR__ . '/src/StateStore.php';
require __DIR__ . '/src/ServerAdmissionVerifier.php';

use NelfeScoring\StateStore;
use NelfeScoring\ServerAdmissionVerifier;
use NelfeScoring\Crypto;

final class MemoryStateStore implements StateStore
{
    public array $seenSessions = [];
    public array $consumedTickets = [];
    public array $revokedDevices = [];
    public array $revokedKeys = [];
    public array $revokedListeners = [];
    public array $suspendedProfiles = [];
    public bool $statAnomaly = false;

    private string $deviceKeyId;
    private string $issuerKeyId;

    public function __construct(private string $devicePem, private string $issuerPem)
    {
        $this->deviceKeyId = Crypto::keyIdFromPubPem($devicePem);
        $this->issuerKeyId = Crypto::keyIdFromPubPem($issuerPem);
    }

    public function devicePubPem(string $deviceId, string $keyId): ?string
    { return ($deviceId === 'dev-001' && $keyId === $this->deviceKeyId) ? $this->devicePem : null; }
    public function issuerPubPem(string $issuerKeyId): ?string
    { return $issuerKeyId === $this->issuerKeyId ? $this->issuerPem : null; }

    public function deviceRevoked(string $deviceId): bool { return in_array($deviceId, $this->revokedDevices, true); }
    public function keyRevoked(string $keyId): bool { return in_array($keyId, $this->revokedKeys, true); }
    public function listenerRevoked(string $sha): bool { return in_array($sha, $this->revokedListeners, true); }
    public function profileSuspended(string $rg, string $rs): bool { return in_array("$rg|$rs", $this->suspendedProfiles, true); }
    public function sessionSeen(string $sid): bool { return in_array($sid, $this->seenSessions, true); }
    public function ticketConsumed(string $tid): bool { return in_array($tid, $this->consumedTickets, true); }
    public function statisticalAnomaly(\stdClass $p): bool { return $this->statAnomaly; }
    public function markConsumed(string $sid, string $tid): void { $this->seenSessions[] = $sid; $this->consumedTickets[] = $tid; }
}

$root = dirname(__DIR__, 2);
$profile = json_decode((string) file_get_contents($root . '/manifest/profiles/megadrive/sonic-the-hedgehog/1.json'));
$devPem = (string) file_get_contents($root . '/keys/device.pub.pem');
$issPem = (string) file_get_contents($root . '/keys/issuer.pub.pem');
$valid = json_decode((string) file_get_contents($root . '/vectors/valid.passport.json'));
$coreFail = json_decode((string) file_get_contents($root . '/vectors/fail_core_mismatch.passport.json'));
$listenerSha = $valid->listener->loaded_sha256;

/** @var array<array{0:string,1:string,2:string,3:callable,4:object}> $cases */
$cases = [
    // nom, status attendu, reason attendue, config(state), passport
    ['valid_published', 'published', '', fn(MemoryStateStore $s) => null, $valid],
    ['duplicate', 'duplicate', 'session.duplicate', fn(MemoryStateStore $s) => $s->seenSessions[] = $valid->session_id, $valid],
    ['ticket_reused', 'refused', 'session.ticket_reused', fn(MemoryStateStore $s) => $s->consumedTickets[] = $valid->ticket->ticket_id, $valid],
    ['device_revoked', 'refused', 'session.device_revoked', fn(MemoryStateStore $s) => $s->revokedDevices[] = 'dev-001', $valid],
    ['listener_revoked', 'refused', 'profile.listener_revoked', fn(MemoryStateStore $s) => $s->revokedListeners[] = $listenerSha, $valid],
    ['profile_suspended', 'refused', 'profile.not_open', fn(MemoryStateStore $s) => $s->suspendedProfiles[] = 'sonic-the-hedgehog|1cc', $valid],
    ['statistical_held', 'held', 'plausibility.statistical_hold', fn(MemoryStateStore $s) => $s->statAnomaly = true, $valid],
    ['core_failure_surfaced', 'refused', 'profile.core_mismatch', fn(MemoryStateStore $s) => null, $coreFail],
];

$fail = 0;
echo "── ServerAdmissionVerifier (§6.5) — cas à état ──\n";
foreach ($cases as [$name, $expStatus, $expReason, $cfg, $passport]) {
    $state = new MemoryStateStore($devPem, $issPem);
    $cfg($state);
    $r = ServerAdmissionVerifier::admit($passport, $profile, $state);
    $ok = ($r['status'] === $expStatus && $r['reason'] === $expReason);
    if (!$ok) $fail++;
    printf("  %s %-24s attendu=%-10s %-28s obtenu=%s %s\n",
        $ok ? 'OK ' : 'XX ', $name, $expStatus, $expReason, $r['status'], $r['reason']);
}
$n = count($cases);
echo $fail === 0 ? "\n✅ {$n}/{$n} — verdicts serveur (published/held/refused/duplicate) conformes.\n"
                 : "\n❌ {$fail} divergence(s) sur {$n}.\n";
exit($fail === 0 ? 0 : 1);
