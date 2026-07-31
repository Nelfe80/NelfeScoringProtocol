<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * État serveur nécessaire au ServerAdmissionVerifier (§6.5). Le CoreVerifier est
 * SANS état ; toute la connaissance à état (annuaire des clés, révocations, tickets
 * consommés, sessions vues, statistiques) passe par cette interface — implémentée en
 * prod par NelfePlay (account_devices, tables scoring), en test par un magasin mémoire.
 */
interface StateStore
{
    /** Clé publique PEM enregistrée pour (device_id, key_id), ou null si inconnue. */
    public function devicePubPem(string $deviceId, string $keyId): ?string;
    public function issuerPubPem(string $issuerKeyId): ?string;

    public function deviceRevoked(string $deviceId): bool;
    public function keyRevoked(string $keyId): bool;
    public function listenerRevoked(string $listenerSha256): bool;
    public function profileSuspended(string $romGroup, string $ruleset): bool;

    public function sessionSeen(string $sessionId): bool;
    public function ticketConsumed(string $ticketId): bool;

    /** Anomalie UNIQUEMENT statistique (§6.6b) → retenue (jamais un refus). */
    public function statisticalAnomaly(\stdClass $passport): bool;

    /** Consomme la session + le ticket (idempotence + usage unique). */
    public function markConsumed(string $sessionId, string $ticketId): void;
}

/**
 * ServerAdmissionVerifier (§6.5) : ajoute l'état au CoreVerifier et produit le SEUL
 * verdict opposable. `published` | `held` | `refused` | `duplicate`.
 *
 * Règle d'or (§4) : une anomalie DÉTERMINISTE (CoreVerifier ou règle serveur) refuse ;
 * une anomalie UNIQUEMENT statistique met en `held` (jamais un refus — publication auto
 * au délai, gérée ailleurs). Zéro examen humain.
 */
final class ServerAdmissionVerifier
{
    /** @return array{status:string, reason:string} */
    public static function admit(\stdClass $passport, \stdClass $profile, StateStore $state): array
    {
        $sid = $passport->session_id ?? '';
        $ticket = $passport->ticket ?? null;
        $tid = $ticket->ticket_id ?? '';
        $did = $passport->device->device_id ?? '';
        $kid = $passport->device->key_id ?? '';

        // Idempotence d'abord : un rejeu exact renvoie duplicate, sans rien refaire.
        if ($state->sessionSeen($sid)) return self::r('duplicate', 'session.duplicate');

        // Résolution de la clé device via l'ANNUAIRE (le CoreVerifier ne le connaît pas).
        $devPem = $state->devicePubPem($did, $kid);
        if ($devPem === null) return self::r('refused', 'session.device_unknown');
        if ($state->deviceRevoked($did) || $state->keyRevoked($kid)) return self::r('refused', 'session.device_revoked');

        $issPem = $state->issuerPubPem($ticket->issuer_key_id ?? '');
        if ($issPem === null) return self::r('refused', 'session.ticket_invalid');

        // Socle déterministe, sans état.
        $core = CoreVerifier::verify($passport, $profile, $devPem, $issPem);
        if (!$core['ok']) return self::r('refused', $core['reason']);

        // Contrôles à état qui refusent (déterministes).
        if ($state->ticketConsumed($tid)) return self::r('refused', 'session.ticket_reused');
        if ($state->listenerRevoked($passport->listener->loaded_sha256 ?? '')) return self::r('refused', 'profile.listener_revoked');
        if ($state->profileSuspended($passport->game->rom_group ?? '', $passport->game->ruleset ?? '')) return self::r('refused', 'profile.not_open');

        // Anomalie UNIQUEMENT statistique → retenue (pas un refus).
        if ($state->statisticalAnomaly($passport)) {
            $state->markConsumed($sid, $tid);
            return self::r('held', 'plausibility.statistical_hold');
        }

        $state->markConsumed($sid, $tid);
        return self::r('published', '');
    }

    private static function r(string $status, string $reason): array
    {
        return ['status' => $status, 'reason' => $reason];
    }
}
