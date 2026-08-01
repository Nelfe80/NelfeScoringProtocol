# Host the verifier

The verifier is a **self-contained HTML file**. **Anyone can host it, anywhere** — and
because everything is recomputed in the visitor's browser, hosting it **does not reduce
trust**: the visitor re-verifies everything.

[The pack on GitHub →](https://github.com/Nelfe80/NelfeScoringProtocol/tree/main/records-viewer){ .md-button .md-button--primary }

## The `records-viewer/` pack
| File | What it does |
|---|---|
| `verify.html` | The **verifier**: recomputes the fingerprint and **verifies the ECDSA P-256 signature** in the browser, then reads the Bitcoin seal state. No server, no build, no dependency. |
| `mirror.sh` | Takes a **durable snapshot** (`snapshot/`) — signed index, anchors, every `.ots` proof — so the records stay provable **even if nelfeplay.com disappears**. |

## Host it (30 seconds)
`verify.html` is just a static file:

- **GitHub Pages / Netlify / Cloudflare Pages** — drop the file.
- **Locally** — open `verify.html`, or `python3 -m http.server`.
- **Offline / archival** — run `./mirror.sh` first, keep the folder.

It reads the **public API** at `nelfeplay.com` (CORS-enabled).

## Two modes
| Mode | What it does | Why |
|---|---|---|
| **Live** | queries the live API | Zero config, always current |
| **Snapshot** | verifies against a local copy (`mirror.sh`) | **Censorship-resistant**: works even if the site disappears |

Snapshot mode makes "immutable" **truly** true: as long as you keep the folder, the
records stay provable — forever, without us.

## Build your own verifier
You don't even need our file — the API is **public and signed**.

| Endpoint | Returns |
|---|---|
| `GET /api/v1/scores/index` | signed index: `records`, `root` (SHA-256 of canonical lines), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | anchors: `generation`, `root_sha256`, `bitcoin_block`, timestamps |
| `GET /api/v1/scores/anchor-proof?generation=N` | the `.ots` proof (base64) for a generation |

All three send `Access-Control-Allow-Origin: *`. The verification algorithm and the
canonicalization (JCS, RFC 8785) live in this repo's `ref/`.
