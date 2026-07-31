<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * État serveur nécessaire au ServerAdmissionVerifier (§6.5). Le CoreVerifier est
 * SANS état ; toute la connaissance à état (annuaire des clés, révocations, tickets
 * consommés, sessions vues, statistiques) passe par cette interface — implémentée en
 * prod par NelfePlay (account_devices, tables scoring), en test par un magasin mémoire.
 *
 * Un fichier = un type (l'autoloader PSR-4 des consommateurs, ex. NelfePlay, en dépend).
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
