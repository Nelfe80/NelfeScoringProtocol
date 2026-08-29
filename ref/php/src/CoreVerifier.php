<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * CoreVerifier - port PHP de RÉFÉRENCE (SPEC v1.0 §6.1-6.4). Déterministe, SANS état.
 * DOIT donner exactement le même verdict que le CoreVerifier C# sur vectors/*.
 * Entrées : passeport et profil (stdClass via json_decode), clés publiques PEM.
 */
final class CoreVerifier
{
    /** @return array{ok:bool, reason:string} */
    public static function verify(\stdClass $passport, \stdClass $profile,
                                  string $devicePubPem, string $issuerPubPem): array
    {
        // ── §6.1 forme ─────────────────────────────────────────────────────────
        if (self::iv($passport, 'protocol') !== 1) return self::f('format.protocol');
        if (self::s($passport, 'session_id') === null) return self::f('format.schema');
        if (self::s($passport, 'device', 'device_id') === null) return self::f('format.schema');

        // ── §6.1-4 ticket ──────────────────────────────────────────────────────
        $ticket = $passport->ticket ?? null;
        if (!($ticket instanceof \stdClass)) return self::f('session.ticket_missing');
        $tsig = self::s($ticket, 'signature');
        if ($tsig === null) return self::f('session.ticket_missing');
        $tbody = json_decode(json_encode($ticket));
        unset($tbody->signature);
        if (!Crypto::verify($issuerPubPem, Jcs::canonical($tbody), $tsig)) return self::f('session.ticket_invalid');
        if (self::s($ticket, 'device_id') !== self::s($passport, 'device', 'device_id')) return self::f('session.ticket_invalid');
        $ended = self::ts(self::s($passport, 'timing', 'ended_at'));
        $expires = self::ts(self::s($ticket, 'expires_at'));
        if ($ended === null || $expires === null) return self::f('format.schema');
        if ($ended > $expires) return self::f('session.ticket_expired');
        if (self::iv($profile, 'manifest_epoch') > self::iv($ticket, 'manifest_epoch')) return self::f('session.ticket_invalid');

        // ── §6.2 signature device ──────────────────────────────────────────────
        $psig = self::s($passport, 'signature');
        if ($psig === null) return self::f('format.schema');
        $body = json_decode(json_encode($passport));
        unset($body->signature);
        if (!Crypto::verify($devicePubPem, Jcs::canonical($body), $psig)) return self::f('session.signature_invalid');

        // ── §6.3 profil & attestation ──────────────────────────────────────────
        if (self::s($passport, 'game', 'rom_group') !== self::s($profile, 'rom_group')
            || self::s($passport, 'game', 'ruleset') !== self::s($profile, 'ruleset')
            || self::s($passport, 'game', 'system_id') !== self::s($profile, 'system_id'))
            return self::f('profile.mismatch');

        $coreLoaded = self::s($passport, 'artifacts', 'core', 'loaded_sha256');
        $contentLoaded = self::s($passport, 'artifacts', 'content', 'loaded_sha256');
        $memLoaded = self::s($passport, 'artifacts', 'mem', 'loaded_sha256');
        $listenerLoaded = self::s($passport, 'listener', 'loaded_sha256');

        if (!self::inArr($profile, $coreLoaded, 'allowed_core_sha256')) return self::f('profile.core_mismatch');
        // Voie A : si le profil épingle la ROM par md5 (No-Intro/gamelist), on compare le md5
        // (le wrapper homologué DOIT l'émettre) ; sinon on retombe sur le sha256 (legacy).
        $allowedContentMd5 = $profile->allowed_content_md5 ?? null;
        $allowedContentSha1 = $profile->allowed_content_sha1 ?? null;
        if (is_array($allowedContentMd5) && count($allowedContentMd5) > 0) {
            if (!self::inArr($profile, self::s($passport, 'artifacts', 'content', 'md5'), 'allowed_content_md5')) return self::f('profile.content_mismatch');
        } elseif (is_array($allowedContentSha1) && count($allowedContentSha1) > 0) {
            // MAME : le Lua ne mesure pas la ROM (MAME la charge en interne + la verifie
            // contre son DAT). Identite = sha1 du set dans la gamelist MAME.
            if (!self::inArr($profile, self::s($passport, 'artifacts', 'content', 'sha1'), 'allowed_content_sha1')) return self::f('profile.content_mismatch');
        } elseif (!self::inArr($profile, $contentLoaded, 'allowed_content_sha256')) {
            return self::f('profile.content_mismatch');
        }
        if ($memLoaded !== self::s($profile, 'mem_sha256')) return self::f('profile.mem_mismatch');
        if (!self::inArr($profile, $listenerLoaded, 'allowed_listener_sha256')) return self::f('profile.listener_unauthorized');

        // Phase E : epinglage des reglages (DIP/vies/difficulte). Additif : on ne controle
        // QUE si le profil epingle allowed_core_options_digest (sinon on saute, retro-compatible).
        $allowedCoreOpts = $profile->allowed_core_options_digest ?? null;
        if (is_array($allowedCoreOpts) && count($allowedCoreOpts) > 0) {
            if (!self::inArr($profile, self::s($passport, 'artifacts', 'core_options_digest'), 'allowed_core_options_digest'))
                return self::f('profile.core_options_mismatch');
        }

        $modules = $passport->software->modules ?? null;
        if (!is_array($modules)) return self::f('format.schema');
        $roleHash = function (string $role) use ($modules): ?string {
            foreach ($modules as $m) if (($m->role ?? null) === $role) return $m->sha256 ?? null;
            return null;
        };
        if (self::s($passport, 'software', 'modules_digest') !== Crypto::sha256Hex(Jcs::canonical($modules)))
            return self::f('attestation.modules_digest');
        if ($roleHash('listener') !== $listenerLoaded) return self::f('runtime.module_unauthorized');
        if ($roleHash('real_core') !== $coreLoaded) return self::f('runtime.module_unauthorized');
        if ($roleHash('frontend') !== self::s($passport, 'process', 'executable_sha256')) return self::f('runtime.module_unauthorized');

        $opened = self::ts(self::s($profile, 'opened_at'));
        if ($opened !== null && $ended !== null && $ended < $opened) return self::f('profile.not_open');

        // ── §6.4 cohérence & checkpoints ───────────────────────────────────────
        $started = self::ts(self::s($passport, 'timing', 'started_at'));
        if ($started === null || $ended === null || $ended <= $started) return self::f('timing.incoherent');

        $rules = $profile->rules ?? null;
        if (self::bv($passport, 'sensitive', 'save_state_loaded') && self::s($rules, 'save_state') === 'forbidden') return self::f('runtime.save_state_detected');
        if (self::bv($passport, 'sensitive', 'cheats') && self::s($rules, 'cheats') === 'forbidden') return self::f('runtime.cheat_detected');
        if (self::iv($passport, 'sensitive', 'continues') > 0 && self::s($rules, 'continues') === 'forbidden') return self::f('runtime.continue_forbidden');
        if (self::bv($passport, 'sensitive', 'rewind') && self::s($rules, 'rewind') === 'forbidden') return self::f('runtime.rewind_detected');
        if (self::bv($passport, 'sensitive', 'runahead') && self::s($rules, 'runahead') === 'forbidden') return self::f('runtime.runahead_detected');
        if (self::bv($passport, 'sensitive', 'fast_forward') && self::s($rules, 'fast_forward') === 'forbidden') return self::f('runtime.fast_forward_detected');

        $checkpoints = $passport->progression->checkpoints ?? null;
        if (!is_array($checkpoints) || count($checkpoints) === 0) return self::f('format.schema');
        if (self::s($passport, 'progression', 'checkpoints_digest') !== Crypto::sha256Hex(Jcs::canonical($checkpoints)))
            return self::f('progression.digest_mismatch');

        $monot = self::s($profile, 'trajectory_policy', 'monotonicity') ?? 'non_decreasing';
        $corr = self::correlationRules($profile);
        $prevMetric = 0; $prev = null; $sawGameEnd = false;
        foreach ($checkpoints as $cp) {
            $metric = (int) (self::s($cp, 'metric') ?? '0');
            if ($monot === 'non_decreasing' && $metric < $prevMetric) return self::f('progression.monotonicity');
            if ($monot === 'non_increasing' && $prev !== null && $metric > $prevMetric) return self::f('progression.monotonicity');
            $ev = self::s($cp, 'event');
            if ($ev === 'game_end') $sawGameEnd = true;
            if ($ev !== null && isset($corr[$ev]) && !self::correlationOk($corr[$ev], $prev, $cp, $prevMetric, $metric))
                return self::f('progression.invalid_correlation');
            $prev = $cp; $prevMetric = $metric;
        }
        if (!$sawGameEnd) return self::f('session.no_game_end');

        $resultSource = self::s($profile, 'metric', 'result_source') ?? 'final';
        $declared = self::s($passport, 'metric', 'value');
        $metrics = array_map(fn($c) => (int) (self::s($c, 'metric') ?? '0'), $checkpoints);
        $expected = match ($resultSource) {
            'final' => self::s($checkpoints[count($checkpoints) - 1], 'metric'),
            'best', 'max' => (string) max($metrics),
            'min' => (string) min($metrics),
            default => $declared,
        };
        if ($declared !== $expected) return self::f('format.out_of_bounds');

        return ['ok' => true, 'reason' => ''];
    }

    // ── corrélations ───────────────────────────────────────────────────────────
    /** @return array<string, array{requires:string[], requires_any:string[]}> */
    private static function correlationRules(\stdClass $profile): array
    {
        $d = [];
        foreach (($profile->correlation_rules ?? []) as $r) {
            $ev = $r->event ?? null;
            if ($ev !== null) $d[$ev] = ['requires' => $r->requires ?? [], 'requires_any' => $r->requires_any ?? []];
        }
        return $d;
    }

    private static function correlationOk(array $rule, ?\stdClass $prev, \stdClass $cur, int $prevMetric, int $metric): bool
    {
        $token = function (string $t) use ($prev, $cur, $prevMetric, $metric): bool {
            return match ($t) {
                'score_delta' => $metric !== $prevMetric,
                'rings_delta' => self::counter($cur, 'rings') !== self::counter($prev, 'rings'),
                'level_delta' => self::counter($cur, 'level') !== self::counter($prev, 'level'),
                'lives_delta' => self::counter($cur, 'lives') !== self::counter($prev, 'lives'),
                'time_checkpoint' => $prev === null || self::iv($cur, 't_ms') > self::iv($prev, 't_ms'),
                default => false,
            };
        };
        $req = $rule['requires']; $any = $rule['requires_any'];
        if (count($req) > 0) foreach ($req as $t) if (!$token($t)) return false;
        if (count($any) > 0) { $ok = false; foreach ($any as $t) if ($token($t)) { $ok = true; break; } if (!$ok) return false; }
        return true;
    }

    // ── helpers ─────────────────────────────────────────────────────────────────
    private static function f(string $code): array { return ['ok' => false, 'reason' => $code]; }

    private static function nav(mixed $n, array $path): mixed
    {
        foreach ($path as $p) { if (is_object($n) && property_exists($n, $p)) $n = $n->{$p}; else return null; }
        return $n;
    }
    private static function s(mixed $n, string ...$path): ?string
    { $v = self::nav($n, $path); return is_string($v) ? $v : null; }
    private static function iv(mixed $n, string ...$path): int
    { $v = self::nav($n, $path); return is_int($v) ? $v : PHP_INT_MIN; }
    private static function bv(mixed $n, string ...$path): bool
    { return self::nav($n, $path) === true; }
    private static function counter(?\stdClass $cp, string $key): int
    { $v = ($cp?->counters ?? null)?->{$key} ?? null; return is_int($v) ? $v : 0; }
    private static function inArr(mixed $n, ?string $val, string $key): bool
    { if ($val === null) return false; $a = $n->{$key} ?? null; return is_array($a) && in_array($val, $a, true); }
    private static function ts(?string $iso): ?int
    { if ($iso === null) return null; $t = strtotime($iso); return $t === false ? null : $t; }
}
