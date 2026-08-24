<?php
declare(strict_types=1);

namespace NelfeScoring;

/**
 * Canonicalisation JSON - RFC 8785 (JCS), sous-ensemble du contrat (nombres ENTIERS
 * uniquement ; les valeurs sensibles sont des chaînes). DOIT produire des octets
 * IDENTIQUES à l'implémentation C# - sinon la signature ne vérifie pas.
 *
 * Décoder le passeport avec json_decode($json) (objets en stdClass, tableaux en
 * array) pour préserver la distinction objet/tableau. Clés d'objet triées par octets
 * (ksort SORT_STRING) - équivalent au tri UTF-16 de C# tant que les clés sont ASCII
 * (elles le sont dans tout le contrat).
 */
final class Jcs
{
    public static function canonical(mixed $node): string
    {
        $out = '';
        self::write($node, $out);
        return $out;
    }

    private static function write(mixed $node, string &$out): void
    {
        if (is_null($node)) { $out .= 'null'; return; }
        if (is_bool($node)) { $out .= $node ? 'true' : 'false'; return; }
        if (is_int($node)) { $out .= (string) $node; return; }
        if (is_float($node)) {
            if (is_finite($node) && floor($node) === $node) { $out .= (string) (int) $node; return; }
            throw new \RuntimeException('Nombre non entier dans le passeport canonique');
        }
        if (is_string($node)) { self::writeString($node, $out); return; }
        if (is_array($node)) { // tableau JSON (liste)
            $out .= '[';
            $first = true;
            foreach ($node as $item) { if (!$first) $out .= ','; $first = false; self::write($item, $out); }
            $out .= ']';
            return;
        }
        if ($node instanceof \stdClass) {
            $props = get_object_vars($node);
            ksort($props, SORT_STRING); // tri par octets = UTF-16 pour clés ASCII
            $out .= '{';
            $first = true;
            foreach ($props as $k => $v) {
                if (!$first) $out .= ',';
                $first = false;
                self::writeString((string) $k, $out);
                $out .= ':';
                self::write($v, $out);
            }
            $out .= '}';
            return;
        }
        throw new \RuntimeException('Type non supporté dans la canonicalisation');
    }

    private static function writeString(string $s, string &$out): void
    {
        $out .= '"';
        $len = strlen($s);
        for ($i = 0; $i < $len; $i++) {
            $c = $s[$i];
            switch ($c) {
                case '"':  $out .= '\\"'; break;
                case '\\': $out .= '\\\\'; break;
                case "\x08": $out .= '\\b'; break;
                case "\x0C": $out .= '\\f'; break;
                case "\n": $out .= '\\n'; break;
                case "\r": $out .= '\\r'; break;
                case "\t": $out .= '\\t'; break;
                default:
                    $o = ord($c);
                    if ($o < 0x20) $out .= sprintf('\\u%04x', $o);
                    else $out .= $c; // ASCII / octets UTF-8 laissés littéraux
            }
        }
        $out .= '"';
    }
}
