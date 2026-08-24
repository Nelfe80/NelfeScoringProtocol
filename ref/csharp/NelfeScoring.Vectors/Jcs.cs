using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

namespace NelfeScoring;

/// <summary>
/// Canonicalisation JSON - RFC 8785 (JCS), sous-ensemble suffisant pour le contrat :
/// tous les nombres du passeport sont des ENTIERS (les valeurs sensibles à la
/// précision - score, temps - sont des chaînes). Les flottants sont donc refusés.
///
/// Règles : clés d'objet triées par unités de code UTF-16 (StringComparer.Ordinal),
/// aucun blanc, chaînes échappées à la ECMAScript JSON.stringify (échappements courts
/// \b \t \n \f \r, autres contrôles en \u00xx minuscule), non-ASCII laissé littéral.
/// </summary>
public static class Jcs
{
    public static byte[] CanonicalBytes(JsonNode? node)
        => Encoding.UTF8.GetBytes(Canonical(node));

    public static string Canonical(JsonNode? node)
    {
        // On repasse par le texte + JsonDocument pour un accès de type uniforme,
        // que le nœud vienne d'un parse ou d'une construction programmatique.
        using var doc = JsonDocument.Parse(node?.ToJsonString() ?? "null");
        var sb = new StringBuilder();
        Write(doc.RootElement, sb);
        return sb.ToString();
    }

    public static string Canonical(JsonElement el)
    {
        var sb = new StringBuilder();
        Write(el, sb);
        return sb.ToString();
    }

    private static void Write(JsonElement el, StringBuilder sb)
    {
        switch (el.ValueKind)
        {
            case JsonValueKind.Object:
                sb.Append('{');
                var first = true;
                foreach (var p in el.EnumerateObject().OrderBy(p => p.Name, StringComparer.Ordinal))
                {
                    if (!first) sb.Append(',');
                    first = false;
                    WriteString(p.Name, sb);
                    sb.Append(':');
                    Write(p.Value, sb);
                }
                sb.Append('}');
                break;

            case JsonValueKind.Array:
                sb.Append('[');
                var f2 = true;
                foreach (var item in el.EnumerateArray())
                {
                    if (!f2) sb.Append(',');
                    f2 = false;
                    Write(item, sb);
                }
                sb.Append(']');
                break;

            case JsonValueKind.String:
                WriteString(el.GetString()!, sb);
                break;

            case JsonValueKind.Number:
                if (!el.TryGetInt64(out var l))
                    throw new NotSupportedException(
                        $"Nombre non entier dans le passeport canonique : {el.GetRawText()}");
                sb.Append(l.ToString(CultureInfo.InvariantCulture));
                break;

            case JsonValueKind.True: sb.Append("true"); break;
            case JsonValueKind.False: sb.Append("false"); break;
            case JsonValueKind.Null: sb.Append("null"); break;
            default: throw new NotSupportedException($"ValueKind {el.ValueKind}");
        }
    }

    private static void WriteString(string s, StringBuilder sb)
    {
        sb.Append('"');
        foreach (var ch in s)
        {
            switch (ch)
            {
                case '"': sb.Append("\\\""); break;
                case '\\': sb.Append("\\\\"); break;
                case '\b': sb.Append("\\b"); break;
                case '\f': sb.Append("\\f"); break;
                case '\n': sb.Append("\\n"); break;
                case '\r': sb.Append("\\r"); break;
                case '\t': sb.Append("\\t"); break;
                default:
                    if (ch < 0x20)
                        sb.Append("\\u").Append(((int)ch).ToString("x4", CultureInfo.InvariantCulture));
                    else
                        sb.Append(ch); // non-ASCII laissé littéral (UTF-8 à l'encodage)
                    break;
            }
        }
        sb.Append('"');
    }
}
