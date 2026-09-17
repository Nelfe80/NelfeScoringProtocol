<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * ServerAdmissionVerifier (§6.5) : ajoute l'état au CoreVerifier et produit le SEUL
 * verdict opposable. `published` | `held` | `refused` | `duplicate`.
 *
 * Règle d'or (§4) : une anomalie DÉTERMINISTE (CoreVerifier ou règle serveur) refuse ;
 * une anomalie UNIQUEMENT statistique met en `held` (jamais un refus - publication auto
 * au délai, gérée ailleurs). Zéro examen humain.
 *
 * Un fichier = un type (voir StateStore.php).
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
        $flags = self::informationFlags($passport, $core['flags'] ?? []);

        // Contrôles à état qui refusent (déterministes).
        if ($state->ticketConsumed($tid)) return self::r('refused', 'session.ticket_reused');
        if ($state->listenerRevoked($passport->listener->loaded_sha256 ?? '')) return self::r('refused', 'profile.listener_revoked');
        if ($state->profileSuspended($passport->game->rom_group ?? '', $passport->game->ruleset ?? '')) return self::r('refused', 'profile.not_open');

        // Anomalie : le score est SIGNALE, pas refuse. Il reste au joueur, ne classe pas, ne
        // s'ancre pas (decision du 2026-09-17). Une macro d'abord : une meme seconde d'entrees
        // rejouee cinq fois a l'identique, ce qu'aucune main ne fait.
        if ((int) ($passport->sensitive->macro_repeats ?? 0) >= self::MacroRepeatsHeld) {
            $state->markConsumed($sid, $tid);
            return self::r('held', 'plausibility.macro_detected', $flags);
        }
        // Anomalie UNIQUEMENT statistique → retenue (pas un refus).
        if ($state->statisticalAnomaly($passport)) {
            $state->markConsumed($sid, $tid);
            return self::r('held', 'plausibility.statistical_hold', $flags);
        }

        $state->markConsumed($sid, $tid);
        return self::r('published', '', $flags);
    }

    /**
     * Ce que le score dit de lui sans etre refuse (decisions du 2026-09-17) :
     *   interrupted     pas de fin de jeu, le score reste celui que les checkpoints prouvent ;
     *   autofire        des appuis d'une regularite mecanique. Une information, pas une anomalie :
     *                   des manettes d'epoque le faisaient, et bien des jeux l'ont d'origine ;
     *   forced_options  la borne s'est alignee sur les reglages du profil au chargement.
     *
     * @param list<string> $core
     * @return list<string>
     */
    private static function informationFlags(\stdClass $passport, array $core): array
    {
        $flags = array_values(array_filter($core, 'is_string'));
        $sensitive = $passport->sensitive ?? null;
        $n = (int) ($sensitive->press_count ?? 0);
        if ($n >= 50) {
            // Variance des durees d'appui, en images carrees, sans avoir garde la serie.
            $sum = (float) ($sensitive->press_frames_sum ?? 0);
            $sq = (float) ($sensitive->press_frames_sq ?? 0);
            $moyenne = $sum / $n;
            $variance = $sq / $n - $moyenne * $moyenne;
            if ($variance < 0.25) $flags[] = 'autofire';
        }
        if ((string) ($passport->artifacts->forced_options ?? '') !== '') $flags[] = 'forced_options';
        return array_values(array_unique($flags));
    }

    /** Repetitions a l'identique d'une meme seconde d'entrees a partir desquelles on signale. */
    public const MacroRepeatsHeld = 5;

    /** @param list<string> $flags */
    private static function r(string $status, string $reason, array $flags = []): array
    {
        return ['status' => $status, 'reason' => $reason, 'flags' => $flags];
    }
}
