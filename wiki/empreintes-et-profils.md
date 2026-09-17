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

### L'arcade en général, pas seulement MAME

Ce qui précède a longtemps été présenté comme une particularité de MAME. C'en est une de
l'**arcade**, et elle vaut aussi quand le jeu tourne sous RetroArch avec un cœur comme
FBNeo.

La raison tient à la nature du référentiel. Les DAT d'arcade décrivent un **set**, pas un
fichier : ils donnent le SHA-1 de la ROM programme, jamais l'empreinte du `.zip` qui la
transporte. Mesuré sur le référentiel arcade complet, la couverture est de **0 % de md5**
pour environ 4 000 entrées, contre 100 % sur une console dont les DAT No-Intro empreintent
le fichier lui-même. Une empreinte **mesurée** du `.zip` ne peut donc jamais résoudre vers
un jeu d'arcade : elle est correcte, et sans emploi.

Conséquence pratique : sur le chemin RetroArch, l'identité du contenu arcade se **lit**
dans la gamelist comme du côté MAME, et le passeport porte les **deux formes** :

| Forme | Origine | Ce qu'elle établit |
|---|---|---|
| `content_sha1` | déclarée, issue des DAT via la gamelist | de quel jeu il s'agit |
| `content_md5`, `content_sha256` | mesurées par le wrapper sur les octets chargés | ce qui a réellement été exécuté |

L'intégrité réelle du romset n'est pas perdue pour autant : elle est garantie par
l'émulateur, qui vérifie le set contre son propre DAT au chargement, et refuse de démarrer
sinon.

Le vérifieur en tire une règle d'**union** plutôt que de cascade : au moins une forme
épinglée par le profil et présentée par le passeport doit correspondre, et aucune ne doit
contredire. Sans cela, le même jeu était certifiable sous MAME et refusé sous FBNeo avec
un « ROM non reconnue » trompeur, alors que la ROM était la bonne.

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

- **NVRAM** (2026‑09‑14) : `nvram_pins`, en **opt‑in**, pour les jeux sans DIP switches dont
  les réglages vivent dans l'EEPROM (CPS‑2…). Plages d'octets calibrées par jeu ; une épingle
  peut être limitée à des cœurs (`cores`) quand le profil sert plusieurs moteurs.
- **BIOS** (2026‑09‑14) : `bios.mode = none` quand le jeu n'utilise pas de BIOS (rien à
  contrôler) ; `bios.mode = files` liste les BIOS exigés (`name`, `allowed_sha256`, `cores`
  optionnel). La borne hache ces fichiers là où le cœur les charge ; un BIOS absent ou
  modifié donne `profile.bios_mismatch`.

Non contrôlé, par décision :
- **frontend** : `process.executable_sha256` est informatif. Le frontend ne touche pas au
  jeu ; seuls le cœur, le contenu, les réglages et le BIOS font la validité d'un score.

## 5. Réglages « usine » — le `core_options_digest` (Phase E)

Un score n'est comparable qu'à **réglages égaux** (difficulté, vies, région…). Le profil
épingle donc, en option, l'empreinte des réglages de référence : `allowed_core_options_digest`
(SHA‑256 d'une chaîne canonique triée `clé=valeur;…`). Contrôle **opt‑in** : un profil sans
cette clé ne vérifie pas les réglages (rétro‑compatible).

**Ce qui est digéré = seulement ce qui change la PARTIE.**

> **Règle : un réglage d'affichage ou de manette ne compte jamais.** Résolution, format
> d'image, filtres, rotation, flip, cabinet, zone morte, sensibilité analogique, résolution
> gauche+droite (SOCD), tir automatique, souris, pistolet : le frontend les écrit selon l'écran
> et les manettes de chaque borne. Les compter refuserait une borne d'usine. Entrent dans
> l'empreinte : vitesse (overclock, 60 Hz), matériel émulé et région, ROM patchée, cheats,
> reprise de partie, DIP switches de jeu (vies, difficulté, bonus).

La capture dépend du backend :

| Backend | Source des réglages | Filtre |
|---|---|---|
| RetroArch (wrapper) | `RETRO_ENVIRONMENT_GET_VARIABLE` : les options que le cœur lit | **liste par cœur** dans le reporter (`genesis_plus_gx_*`, `fbneo-*`, `mame_*`). Un cœur **sans liste ne verse rien** (depuis APIExpose 1.8.12 ; avant, il versait toutes ses options, affichage compris). Les DIP FBNeo (`fbneo-dipswitch-<jeu>-<nom>`) passent le même filtre de noms que MAME autonome |
| MAME autonome (Lua) | `manager.machine.ioport` : les DIP switches | **noms écartés** : monnayage, free play, service, test mode, demo sounds, unused, flip, cabinet, screen, monitor, controls, joystick, trackball (plugin Lua, complété côté APIExpose) |

Le **digest est calculé côté APIExpose** (le backend émet le brut, le reporter filtre puis hache),
dans un mécanisme centralisé. Changer le filtre change les empreintes des jeux déjà épinglés :
les nouvelles s'ajoutent aux profils avant la version qui les produit.

**Les valeurs en clair : `core_options_expected`** (2026‑09‑17). Une empreinte ne se remonte
pas : sans les valeurs, une borne ne pouvait ni nommer au joueur le réglage fautif ni le
corriger. Le profil publie donc, par moteur (`cores` optionnel), la liste `clé = valeur` des
réglages certifiés. L'empreinte reste le contrôle ; les valeurs servent à deux choses :

- **le forçage** : la borne dépose les valeurs dans `wrapper\certified.txt` avant le lancement,
  et le listener répond la valeur certifiée quand le cœur lit ses options (`GET_VARIABLE`).
  Aucun fichier de configuration n'est réécrit. Ce qui a réellement changé part dans le
  passeport (`artifacts.forced_options`) et se voit sur le record ;
- **le frontend** (1.8.13) : rembobinage, run‑ahead et sauvegarde d'état automatique ne sont pas
  des options de cœur ; la borne les met à zéro par les réglages RetroBat du jeu
  (`<système>["<rom>"].rewind|runahead|autosave` dans es_settings.cfg) dès la sélection, pour
  que le lanceur les lise. RetroBat allume le rewind en « auto » : sans cela, chaque nouveau
  joueur était refusé pour rembobinage ;
- **le verdict avant la partie** : à son attestation, la borne envoie à `scores/preflight` ce
  qu'elle a mesuré (cœur, contenu, MEM, listener, empreinte des réglages, BIOS) ; la plateforme
  répond « certifiable » ou la raison, par `CoreVerifier::profileArtifacts`, le code même du
  verdict final, après les mêmes élargissements. Sans NVRAM présentée, les épingles NVRAM
  attendent la fin de partie. La borne y ajoute ce que la plateforme ne voit pas : ce que
  RetroArch a réellement chargé (retroarch.cfg), pour prévenir d'un rembobinage actif.

Une session **sans aucun appui** (`press_count = 0`, listener 0.336) n'est jamais soumise : c'est
la démo d'attract, ou un jeu lancé et laissé là.

**Épinglage d'un jeu** : déposer les valeurs dans `core_options_expected` et l'empreinte qu'elles
produisent dans `allowed_core_options_digest`. Depuis le forçage, toutes les bornes convergent
vers les mêmes valeurs : une seule empreinte par jeu et par moteur, au lieu d'une par borne.

**Limite** : les jeux configurés par **EEPROM/nvram** (CPS‑2, Neo‑Geo) n'exposent pas leurs
réglages en DIP — le digest y fingerprinte des DIP inertes, pas la vraie difficulté (capture nvram = futur).

## 5 bis. Les entrées : ce que le passeport dit du jeu de la main (2026‑09‑17)

Le listener observe les entrées du port 1 sans rien coûter à la partie (bits et compteurs de
taille fixe, repliés une fois par image, émis en fin de session) :

| Champ (`sensitive`) | Ce qu'il compte | Ce qu'en fait la plateforme |
|---|---|---|
| `impossible_inputs` | images où deux directions opposées étaient tenues ensemble | **refus** `runtime.impossible_inputs` au‑delà de 3 images (un rebond de contact) |
| `macro_repeats` | le plus grand nombre de fois qu'une même seconde d'entrées (64 images, avec de la matière : 6 changements et deux directions ou deux boutons d'action) a été rejouée à l'identique sans chevauchement | **signalé** `plausibility.macro_detected` à partir de 5 : gardé pour le joueur, jamais classé ni ancré |
| `press_count`, `press_frames_sum`, `press_frames_sq` | nombre, somme et somme des carrés des durées d'appui | **information** `autofire` si la variance est nulle sur 50 appuis ou plus |

Un tir automatique sur un seul bouton, direction tenue, n'entre pas dans la fenêtre d'une
macro ; une routine humaine varie d'une image ou deux et ne se répète pas cinq fois à
l'identique. Une macro à qui l'on ajoute du bruit n'est pas détectée : c'est assumé.

**Partie interrompue** : `session.no_game_end` n'est plus un refus. Le score soumis est déjà le
meilleur segment croissant ; le verdict porte le drapeau `interrupted`, rien n'est perdu.

**Trois sorts au dépôt** : `published` (classé, certificat, ancré), `held` (signalé : gardé,
visible du seul joueur, jamais dans `scores` ni dans l'arbre ancré ; un signalement levé
rejoint une génération suivante), `refused`. Les drapeaux d'information (`interrupted`,
`autofire`, `forced_options`) voyagent avec le score et s'affichent par un repère ⓘ.

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
