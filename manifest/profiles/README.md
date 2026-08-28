# ⚠️ Ces profils sont des FIXTURES DE TEST — ne pas déposer en production

Les fichiers `**/<version>.json` de ce dossier sont **générés** par
`ref/csharp/NelfeScoring.Vectors/Program.cs` (via `dotnet run`). Leurs empreintes
(`allowed_core_sha256`, `allowed_content_sha256`, `mem_sha256`,
`allowed_listener_sha256`) sont des **SHA‑256 de libellés** (ex.
`H("genesis_plus_gx_libretro.dll@v1")`), **pas** des hachages de fichiers réels.
Ils servent uniquement aux **vecteurs de test** du vérifieur.

- **Ne les éditez pas à la main** : `dotnet run` les écrase.
- **Ne les déposez JAMAIS en production.** Déposer un fixture = un profil qui ne
  correspond à aucune machine réelle → `core_mismatch` / `content_mismatch` /
  `mem_mismatch` pour tout le monde. (C'est exactement le bug survenu une fois.)

## Les vrais profils de production

Ils se construisent avec les **vraies empreintes mesurées** (voir
`wiki/empreintes-et-profils.md`), se stockent en privé dans
`NelfePlay-Site/config/scoring-profiles/`, et se déposent via
`POST /_ops/scoring/deposit-profile` (entête `X-Nelfeplay-Deploy-Token`).
