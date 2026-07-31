<?php
declare(strict_types=1);

namespace NelfeScoring;

use PDO;

/**
 * StateStore adossé à une base (PDO). Fonctionne en SQLite (tests) et MariaDB (prod
 * NelfePlay). Toute la connaissance à état du ServerAdmissionVerifier (§6.5) vit ici.
 */
final class PdoStateStore implements StateStore
{
    public function __construct(private PDO $pdo) {}

    public function devicePubPem(string $deviceId, string $keyId): ?string
    {
        $st = $this->pdo->prepare('SELECT public_key_pem FROM scoring_devices WHERE device_id = ? AND key_id = ?');
        $st->execute([$deviceId, $keyId]);
        $pem = $st->fetchColumn();
        return $pem === false ? null : (string) $pem;
    }

    public function issuerPubPem(string $issuerKeyId): ?string
    {
        $st = $this->pdo->prepare('SELECT public_key_pem FROM scoring_issuers WHERE key_id = ? AND revoked_at IS NULL');
        $st->execute([$issuerKeyId]);
        $pem = $st->fetchColumn();
        return $pem === false ? null : (string) $pem;
    }

    public function deviceRevoked(string $deviceId): bool
    {
        $st = $this->pdo->prepare('SELECT revoked_at FROM scoring_devices WHERE device_id = ?');
        $st->execute([$deviceId]);
        $v = $st->fetchColumn();
        return $v !== false && $v !== null;
    }

    public function keyRevoked(string $keyId): bool { return false; } // révocation portée par le device en v1

    public function listenerRevoked(string $sha): bool { return $this->exists('SELECT 1 FROM scoring_revoked_listeners WHERE sha256 = ?', [$sha]); }

    public function profileSuspended(string $rg, string $rs): bool { return $this->exists('SELECT 1 FROM scoring_suspended WHERE rom_group = ? AND ruleset = ?', [$rg, $rs]); }

    public function sessionSeen(string $sid): bool { return $this->exists('SELECT 1 FROM scoring_consumed WHERE session_id = ?', [$sid]); }

    public function ticketConsumed(string $tid): bool { return $this->exists('SELECT 1 FROM scoring_consumed WHERE ticket_id = ?', [$tid]); }

    public function statisticalAnomaly(\stdClass $p): bool { return $this->exists('SELECT 1 FROM scoring_stat_anomaly WHERE session_id = ?', [$p->session_id ?? '']); }

    public function markConsumed(string $sid, string $tid): void
    {
        $st = $this->pdo->prepare('INSERT INTO scoring_consumed (session_id, ticket_id, consumed_at) VALUES (?, ?, ?)');
        $st->execute([$sid, $tid, gmdate('c')]);
    }

    private function exists(string $sql, array $args): bool
    {
        $st = $this->pdo->prepare($sql);
        $st->execute($args);
        return $st->fetchColumn() !== false;
    }
}
