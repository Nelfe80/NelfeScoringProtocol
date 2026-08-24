# Héberger le vérifieur

Le vérifieur est un **fichier HTML autonome**. **N'importe qui peut l'héberger,
n'importe où** - et comme tout est recalculé dans le navigateur du visiteur, l'héberger
**ne réduit pas la confiance** : le visiteur re-vérifie tout lui-même.

[Le pack sur GitHub →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## Le pack `records-viewer/`
| Fichier | Rôle |
|---|---|
| `verify.html` | Le **vérifieur** : recalcule l'empreinte et **vérifie la signature ECDSA P-256** dans le navigateur, puis lit l'état du sceau Bitcoin. Zéro serveur, zéro build, zéro dépendance. |
| `mirror.sh` | Prend un **instantané durable** (`snapshot/`) - index signé, ancres, et chaque preuve `.ots` - pour que les records restent prouvables **même si nelfeplay.com disparaît**. |

## L'héberger (30 secondes)
`verify.html` est un simple fichier statique :

- **GitHub Pages / Netlify / Cloudflare Pages** - déposez le fichier.
- **En local** - ouvrez `verify.html`, ou `python3 -m http.server`.
- **Hors-ligne / archive** - lancez `./mirror.sh` d'abord, gardez le dossier.

Il lit l'**API publique** de `nelfeplay.com` (CORS activé).

## Deux modes
| Mode | Ce qu'il fait | Intérêt |
|---|---|---|
| **Direct** | interroge l'API en direct | Zéro config, toujours à jour |
| **Instantané** | vérifie contre une copie locale (`mirror.sh`) | **Résistant à la censure** : marche même si le site disparaît |

Le mode instantané rend « immuable » **vraiment** vrai : tant que vous gardez le dossier,
les records restent prouvables - pour toujours, sans nous.

## Construire son propre vérifieur
Vous n'avez même pas besoin de notre fichier - l'API est **publique et signée**.

| Endpoint | Renvoie |
|---|---|
| `GET /api/v1/scores/index` | l'index signé : `records`, `root` (SHA-256 des lignes canoniques), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | les ancres : `generation`, `root_sha256`, `bitcoin_block`, dates |
| `GET /api/v1/scores/anchor-proof?generation=N` | la preuve `.ots` (base64) d'une génération |

Les trois envoient `Access-Control-Allow-Origin: *`. L'algorithme de vérification et la
canonicalisation (JCS, RFC 8785) sont dans `ref/` de ce dépôt.
