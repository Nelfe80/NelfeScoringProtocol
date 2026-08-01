# Alojar el verificador

El verificador es un **archivo HTML autónomo**. **Cualquiera puede alojarlo, donde
sea** — y como todo se recalcula en el navegador del visitante, alojarlo **no reduce la
confianza**: el visitante lo re-verifica todo.

[El pack en GitHub →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## El pack `records-viewer/`
| Archivo | Rol |
|---|---|
| `verify.html` | El **verificador**: recalcula la huella y **verifica la firma ECDSA P-256** en el navegador, luego lee el estado del sello Bitcoin. Sin servidor, sin build, sin dependencias. |
| `mirror.sh` | Toma una **instantánea duradera** (`snapshot/`) — índice firmado, anclas y cada prueba `.ots` — para que los récords sigan siendo demostrables **aunque nelfeplay.com desaparezca**. |

## Alojarlo (30 segundos)
`verify.html` es solo un archivo estático:

- **GitHub Pages / Netlify / Cloudflare Pages** — sube el archivo.
- **En local** — abre `verify.html`, o `python3 -m http.server`.
- **Sin conexión / archivo** — ejecuta `./mirror.sh` primero, guarda la carpeta.

Lee la **API pública** de `nelfeplay.com` (CORS activado).

## Dos modos
| Modo | Qué hace | Por qué |
|---|---|---|
| **En vivo** | consulta la API en vivo | Cero configuración, siempre al día |
| **Instantánea** | verifica contra una copia local (`mirror.sh`) | **Resistente a la censura**: funciona aunque el sitio desaparezca |

El modo instantánea hace que «inmutable» sea **de verdad** cierto: mientras guardes la
carpeta, los récords siguen siendo demostrables — para siempre, sin nosotros.

## Crea tu propio verificador
Ni siquiera necesitas nuestro archivo — la API es **pública y firmada**.

| Endpoint | Devuelve |
|---|---|
| `GET /api/v1/scores/index` | índice firmado: `records`, `root` (SHA-256 de líneas canónicas), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | anclas: `generation`, `root_sha256`, `bitcoin_block`, fechas |
| `GET /api/v1/scores/anchor-proof?generation=N` | la prueba `.ots` (base64) de una generación |

Los tres envían `Access-Control-Allow-Origin: *`. El algoritmo de verificación y la
canonicalización (JCS, RFC 8785) están en `ref/` de este repositorio.
