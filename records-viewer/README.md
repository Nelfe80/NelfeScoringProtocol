# Records viewer - host your own, trust no one

This folder is a **self-contained, trustless verifier** for NelfePlay certified
records. It is a single HTML file plus a mirror script. Anyone can host it, anywhere.

Full explanation (6 languages): **https://nelfe80.github.io/NelfeScoringProtocol/**

---

## What's inside

| File | What it does |
|---|---|
| `verify.html` | The **verifier**. Recomputes the index fingerprint and **verifies the ECDSA P-256 signature in the browser**, then reads the Bitcoin seal state. No server, no build, no dependency. |
| `mirror.sh` | Takes a **durable snapshot** (`snapshot/`) - signed index, anchors, and every `.ots` proof - so the records stay provable even if nelfeplay.com disappears. |

## Host it (30 seconds)

`verify.html` is just a static file - put it on any host:

- **GitHub Pages / Netlify / Cloudflare Pages** - drop the file in a repo/bucket.
- **Locally** - open `verify.html` in a browser, or `python3 -m http.server`.
- **Offline / archival** - run `./mirror.sh` first, keep the folder.

It reads the **public API** at `https://nelfeplay.com` (CORS-enabled). Because every
check runs **in the visitor's browser**, hosting a copy does **not** reduce trust -
the visitor re-verifies everything from scratch.

## Why this is trustless

The verifier does not take our word for anything:

1. **Fingerprint** - it recomputes the SHA-256 of the raw records (canonical JCS,
   RFC 8785) and compares it to the published one.
2. **Signature** - it verifies the **ECDSA P-256** signature with the issuer's
   public key, using the browser's Web Crypto API. A forgery cannot produce it.
3. **Bitcoin** - the fingerprint is timestamped with **OpenTimestamps**. Once
   confirmed, it proves the records existed before a given Bitcoin block, immutably.
   The `.ots` proof is downloadable and verifiable with the standard client:
   `pip install opentimestamps-client && ots verify …`

## Build your own viewer

You don't even need this file - the API is public and signed. Three endpoints:

| Endpoint | Returns |
|---|---|
| `GET /api/v1/scores/index` | the signed index: `records`, `root` (SHA-256 of canonical lines), `signature` (ECDSA P-256, base64url DER), `issuer_public_key` (SPKI PEM) |
| `GET /api/v1/scores/anchors` | anchor metadata: `generation`, `root_sha256`, `bitcoin_block`, timestamps |
| `GET /api/v1/scores/anchor-proof?generation=N` | the `.ots` proof (base64) for that generation |

All three send `Access-Control-Allow-Origin: *`. The verification algorithm and the
canonicalization are documented in the wiki and implemented (multiple languages) in
this repository's `ref/`.

---

*Part of the [NelfeScoringProtocol](https://github.com/Nelfe80/NelfeScoringProtocol) -
open, auditable certified retro scoring.*
