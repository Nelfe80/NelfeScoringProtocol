<?php
declare(strict_types=1);

namespace NelfeScoring;

use PDO;

/**
 * Flux de soumission serveur : charge le profil, appelle le ServerAdmissionVerifier,
 * PERSISTE le résultat (audit + score publié) et calcule le rang. En prod NelfePlay,
 * c'est ce que l'endpoint POST /api/v1/scores/submissions exécute.
 */
final class SubmissionService
{
    /** @param callable(\stdClass):?\stdClass $profileProvider game → profil signé, ou null */
    public function __construct(
        private PDO $pdo,
        private StateStore $state,
        private $profileProvider,
    ) {}

    /** @return array{status:string, reason:string, rank?:int} */
    public function submit(\stdClass $passport): array
    {
        $profile = ($this->profileProvider)($passport->game ?? new \stdClass());
        if (!($profile instanceof \stdClass)) return ['status' => 'refused', 'reason' => 'profile.not_open'];

        $r = ServerAdmissionVerifier::admit($passport, $profile, $this->state);

        // Un doublon est déjà enregistré : réponse idempotente, aucune écriture.
        if ($r['status'] === 'duplicate') return $r;

        // Audit de la soumission (session_id UNIQUE). Défensif contre un rejeu d'un refus.
        try {
            $st = $this->pdo->prepare(
                'INSERT INTO score_submissions (session_id, device_id, rom_group, ruleset, metric_value, verdict, reason_code, received_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            );
            $st->execute([
                $passport->session_id, $passport->device->device_id,
                $passport->game->rom_group, $passport->game->ruleset,
                (string) $passport->metric->value, $r['status'], $r['reason'], gmdate('c'),
            ]);
        } catch (\PDOException $e) {
            return ['status' => 'duplicate', 'reason' => 'session.duplicate']; // déjà audité
        }

        if ($r['status'] === 'published') {
            $subId = (int) $this->pdo->lastInsertId();
            $mv = (int) $passport->metric->value;
            $ins = $this->pdo->prepare(
                'INSERT INTO scores (submission_id, rom_group, ruleset, player_ref, metric_value, accepted_at)
                 VALUES (?, ?, ?, ?, ?, ?)'
            );
            $ins->execute([$subId, $passport->game->rom_group, $passport->game->ruleset,
                           $passport->identity->player_ref ?? null, $mv, gmdate('c')]);
            $r['rank'] = $this->rank((string) $passport->game->rom_group, (string) $passport->game->ruleset, $mv, $profile);
        }
        return $r;
    }

    private function rank(string $rg, string $rs, int $mv, \stdClass $profile): int
    {
        $dir = $profile->metric->ranking_direction ?? 'higher_better';
        $op = $dir === 'higher_better' ? '>' : '<';
        $st = $this->pdo->prepare("SELECT COUNT(*) FROM scores WHERE rom_group = ? AND ruleset = ? AND metric_value $op ?");
        $st->execute([$rg, $rs, $mv]);
        return 1 + (int) $st->fetchColumn();
    }
}
