# Empreintes des artefacts, profils, et vérification

Ce document fige **comment** chaque empreinte est calculée, **d'où** viennent les
valeurs d'un profil, et **le piège** qui a produit des profils faux (des valeurs
« placeholder » déposées en production). À lire avant de créer ou de déposer un
profil de scoring.

## 1. Méthode d'empreinte — source de vérité = le wrapper

Toutes les empreintes du passeport sont des **SHA‑256**. Ce qui est haché :

| Champ passeport | Haché sur | Référence code |
|---|---|---|
| `listener.loaded_sha256` | le **fichier DLL du wrapper** (`cores/<core>.dll`) | `Wrapper/wrapper.cpp` `Sha256FileHex(selfPath)` |
| `artifacts.core.loaded_sha256` | le **fichier du vrai core** (`cores_real/<core>.dll`) | `Sha256FileHex(corePath)` |
| `artifacts.mem.loaded_sha256` | le **fichier `.MEM`** | `Sha256FileHex(g_last_mem_path)` |
| `artifacts.content.loaded_sha256` | le **buffer ROM `game->data`** (ROM **extraite** en mémoire = ROM décompressée) | `Sha256BufHex(game->data, game->size)` |

Vérification indépendante possible : `sha256sum <fichier>` pour listener/core/mem ;
`unzip -p <rom.zip> \| sha256sum` pour la ROM. Les valeurs doivent être **identiques**
à celles du passeport — c'est un SHA‑256 brut, sans normalisation.

### Cas MAME (arcade, moteur `mame_standalone`)

MAME **charge les ROMs lui‑même** (le jeu est un `.zip` de *set*, vérifié en interne
contre son propre DAT) : le listener Lua ne voit **pas** de buffer `game->data` à
hacher. L'identité ROM est donc le **SHA‑1 de la ROM programme principale du set**,
lu dans la gamelist `roms/mame` (champ `sha1`), et le profil porte `content_sha1`
(pas de `md5` côté MAME). Les autres empreintes restent des SHA‑256 de fichiers :
`listener` = `init.lua`, `core` = `mame.exe`, `mem` = le `.MEM`.

**Piège de jointure** : la ligne gamelist se relie au jeu par le **nom de set
canonique** (`emu.romname()`, ex. `19xx` ; côté APIExpose `definition.RawRom`),
**jamais** par le nom d'affichage du `.MEM` (`definition.Rom`, ex.
`19xx-the-war-against-destiny`). Une jointure sur le nom d'affichage échoue.

## 2. LE piège : fixture de test ≠ profil de production

- `manifest/profiles/**/<v>.json` est un **FIXTURE DE TEST généré** par
  `ref/csharp/NelfeScoring.Vectors/Program.cs` (ligne ~72). Ses empreintes sont
  des **SHA‑256 de libellés** (`H("genesis_plus_gx_libretro.dll@v1")`,
  `H("Sonic The Hedgehog (USA, Europe).md")`, …). Elles ne correspondent à
  **aucun** fichier réel — c'est voulu, pour tester la logique du vérifieur avec
  les vecteurs. **Lancer `dotnet run` régénère ce fichier : ne jamais l'éditer à la main.**
- **NE JAMAIS déposer ce fixture en production.** C'est exactement ce qui a produit
  les faux `core_mismatch`/`content_mismatch`/`mem_mismatch` : le fixture (valeurs
  bidon) avait été déposé comme profil réel.

- Le **profil réel** se construit avec les **vraies** empreintes mesurées et se
  dépose via `POST https://nelfeplay.com/_ops/scoring/deposit-profile?open=1`
  (entête `X-Nelfeplay-Deploy-Token`). Il est stocké **privé** dans
  `NelfePlay-Site/config/scoring-profiles/` (jamais dans le repo public).

## 3. D'où viennent les valeurs d'un profil réel (registre, pas à la main)

On ne recalcule jamais à la main : chaque valeur vient d'une **source**.

| Empreinte | Source canonique |
|---|---|
| `content` (ROM, **RetroArch**) | identité **No‑Intro**. La gamelist `APIExpose/resources/gamelist/systems` porte `crc/md5/sha1` (pas de sha256). **Voie retenue** : le profil référence le `md5` No‑Intro (déjà dans la gamelist) et le wrapper émet `content_md5` — évite de régénérer les gamelists et de posséder toutes les ROMs. |
| `content` (ROM, **arcade/MAME**) | la gamelist `roms/mame` n'a **pas** de md5 → le profil porte `content_sha1` (le `sha1` du set = ROM programme principale). Jointure par set canonique `RawRom` (voir §1). |
| `core` | pas d'équivalent No‑Intro → **registre central de builds officiels** (SHA‑256 des cores distribués par RetroBat / buildbot libretro), à mettre à jour à chaque release de core. |
| `mem` | donnée NelfePlay → **un SHA‑256 par révision** du `.MEM`. Doit rester cohérent avec `ram_definitions` (base distante). |
| `listener` | **whitelist** des wrappers homologués (`allowed_listener_sha256`), additive à chaque version signée. |

## 4. Ce que le vérifieur applique réellement

`CoreVerifier` (SPEC §6.3‑6.4) compare en **égalité stricte** :
- empreintes : `core`, `mem`, `listener`, + `modules_digest` et les rôles
  `listener`/`real_core`/`frontend`.
- **contenu** : le champ comparé suit ce que déclare le profil : `allowed_content_md5`
  (RetroArch) sinon `allowed_content_sha1` (MAME) sinon `allowed_content_sha256`.
- règles `sensitive` : `save_state`, `cheats`, `continues`, **`rewind`, `runahead`,
  `fast_forward`** (ces trois branchés le 2026‑08‑28).
- **réglages** (Phase E, 2026‑08‑30) : `core_options_digest` ∈ `allowed_core_options_digest`,
  en **opt‑in** (contrôlé seulement si le profil épingle la clé). Voir §5.
- progression : monotonie, `game_end`, corrélations, `metric.value` == `result_source`.

À câbler (déclaré mais pas encore appliqué) :
- **BIOS** : conditionnel à `bios.mode` (`none` / `vfs_observed` / `os_observed`).
  `none` (cartouche) = pas de contrôle, normal. Les systèmes à BIOS (PSX, Saturn,
  MegaCD, Neo Geo) demandent une mesure wrapper + un hash autorisé au schéma.
- **frontend** : `process.executable_sha256` est `null` aujourd'hui → check neutralisé.

## 5. Réglages « usine » — le `core_options_digest` (Phase E)

Un score n'est comparable qu'à **réglages égaux** (difficulté, vies, région…). Le profil
épingle donc, en option, l'empreinte des réglages de référence : `allowed_core_options_digest`
(SHA‑256 d'une chaîne canonique triée `clé=valeur;…`). Contrôle **opt‑in** : un profil sans
cette clé ne vérifie pas les réglages (rétro‑compatible).

**Ce qui est digéré = seulement le GAMEPLAY**, pas le cosmétique (audio, filtres vidéo, ratio).
La capture dépend du backend :

| Backend | Source des réglages | Filtre |
|---|---|---|
| RetroArch (wrapper) | `RETRO_ENVIRONMENT_GET_VARIABLE` — le core lit ses options (DIP arcade pour fbneo, région/etc. pour la console) | **allowlist par core** dans le reporter (chaque core a ses clés préfixées : `genesis_plus_gx_*`, `fbneo-*`…) ; ajouter un core = une entrée, partagée par ses jeux |
| MAME standalone (Lua) | `manager.machine.ioport` — les DIP switches | **denylist** dans le plugin Lua (écarte monnayage/service/flip/cabinet/demo/unused) |

Le **digest est calculé côté APIExpose** (le backend émet le brut, le reporter filtre puis hache) :
mécanisme centralisé, et une clé d'un backend non filtré passe inchangée (donc un digest déjà
épinglé ne bouge pas si on ajoute un core à l'allowlist).

**Épinglage d'un jeu** : jouer une fois en réglages usine → lire le digest dans le log APIExpose
(`Scoring Phase E : réglages … → core_options_digest=…`) → le mettre dans `allowed_core_options_digest`
→ redéposer. Un réglage gameplay différent donne alors `profile.core_options_mismatch`.

**Limite** : les jeux configurés par **EEPROM/nvram** (CPS‑2, Neo‑Geo) n'exposent pas leurs
réglages en DIP — le digest y fingerprinte des DIP inertes, pas la vraie difficulté (capture nvram = futur).

## 6. Les deux vérifieurs JUMEAUX — garder synchro

Le vérifieur existe en **deux copies qui doivent donner le même verdict** :
- **Référence** (source de vérité) : `NelfeScoringProtocol/ref/php/src/CoreVerifier.php`
  et `ref/csharp/NelfeScoring.Vectors/CoreVerifier.cs`, validés par `vectors/`.
- **Production** (l'enforcer réel) : `NelfePlay-Site/app/Scoring/CoreVerifier.php`
  (vendoré depuis la référence).

Règle : toute correction se fait **d'abord dans la référence + un vecteur**, se
valide avec `dotnet run` dans `ref/csharp/NelfeScoring.Vectors` (tous les vecteurs
au verdict attendu), **puis** se re‑vendore dans `NelfePlay-Site` et se déploie
(`.deploy/ftps.py upload app/Scoring/CoreVerifier.php /app/Scoring/CoreVerifier.php`,
puis **relire depuis le serveur** — un rapport d'upload ne prouve rien).
