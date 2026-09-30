# Règles de score : ce qui compte comme un record

Cette page explique **comment un score est jugé**, pour que chacun sache à quoi
s'en tenir. Le *comment on mesure* (adresses mémoire, algorithme du listener) reste
fermé (voir [Homologation](homologation.md)) ; ici on décrit les **règles**, pas la
technique.

## Une partie, c'est un lancement du jeu
Ta partie commence au **premier crédit consommé** en arcade, ou au départ sur console, et elle se
termine **quand tu quittes le jeu**. Quitter termine la partie et garde ton score : inutile d'aller
jusqu'au game over ou d'attendre un écran de fin.

## Le 1cc : un crédit, sans continue
Un record **1cc** est un score fait sur **un seul crédit, sans continue**, jeu fini ou non. C'est la
catégorie de référence des records de score, celle où se jouent aussi les jeux sans fin. Dans les
communautés de score, « 1CC » (« one credit clear ») désigne plus précisément le fait de *finir* le
jeu sur un crédit : le site dit donc « Un crédit, sans continue ».

La règle est la même en arcade et sur console, quel que soit le nombre de continues que le jeu
propose.

### En arcade, le crédit fait foi
- **Avant de jouer**, remets autant de pièces que tu veux. Le nombre de pièces par crédit varie
  d'un jeu à l'autre ; la borne compte les crédits.
- **Au départ**, le premier crédit consommé lance ta partie.
- **Pendant la partie**, des crédits ajoutés ne changent rien tant qu'ils ne sont pas consommés.
  **Tout crédit consommé ensuite est un continue**, sauf l'arrivée d'un autre joueur (voir
  [Les parties à plusieurs](#les-parties-a-plusieurs)).
- **Un continue ne fait pas refuser ta partie.** Ton score certifié s'arrête au dernier score
  affiché avant le continue. Tu peux continuer à jouer, la suite ne compte plus.
- **Rejouer sans quitter le jeu** consomme un crédit après le départ : pour la borne, c'est un
  continue, même quand le jeu remet le score à zéro. Pour une nouvelle partie classée, **quitte le
  jeu et relance-le**.

### Les vies ne coupent jamais un 1cc
Perdre une vie, en gagner une, tomber à zéro : rien de tout cela n'arrête une partie 1cc. Seul un
crédit consommé la coupe. Les vies servent au classement « une vie » (1LC), là où un jeu l'ouvre.

### Sur console, chaque jeu a son continue
Une console n'a pas de pièce : chaque jeu gère ses continues à sa façon (un compteur de
continues, un écran « Continue ? », un score remis à zéro). Le profil du jeu dit comment la borne
reconnaît le sien. Un jeu dont le continue ne se reconnaît pas n'ouvre pas de classement 1cc.

### Le doute profite au joueur
Une partie n'est coupée que sur une **preuve** : un signal vérifié à l'écran pour ce jeu, avant son
ouverture au scoring. Sans preuve, rien ne coupe.

## Ce que la borne te dit pendant la partie
Un bandeau orange s'affiche à chaque crédit consommé après le départ, et quand un joueur te rejoint :

| Moment | Bandeau |
|---|---|
| premier continue | « Crédit consommé : ton score certifié reste 29 960 » ; « la partie qui vient n'est pas certifiable : quitte et relance le jeu pour une partie certifiée » |
| continues suivants | « Partie non certifiable » ; « pour une partie certifiée, quitte et relance le jeu » |
| un joueur te rejoint | « Un joueur te rejoint : ton score solo certifié reste 30 000 » ; « la suite se joue à plusieurs, hors classement solo » |
| partie à plusieurs dès le départ | « Partie à plusieurs : hors classement solo » ; « l'arrivée d'un joueur ne compte pas comme un continue » |
| la borne perd la lecture des crédits | « Crédits illisibles : partie non certifiable » |

Le score du bandeau est celui que tu as vu à l'écran juste avant : c'est lui qui part au classement.

## Les parties à plusieurs
- **Le 1cc est solo.** Seul au départ, tu joues pour le 1cc, même si ta partie est ouverte aux
  autres en netplay.
- **Un joueur qui te rejoint en joueur** fait basculer la partie à plusieurs, pour toi comme pour
  lui. Un spectateur ne change rien. **L'arrivée d'un joueur n'est pas un continue** : ton score
  fait seul avant son arrivée reste un 1cc, certifié s'il bat ton record. La suite n'est pas encore
  classée.
- **Chaque borne le dit à son joueur** : l'hôte à l'arrivée de l'autre joueur, l'invité dès que sa
  partie démarre. La borne qui rejoint une partie ne soumet aucun score solo.
- **Le replay suit** : celui de ta partie solo s'arrête à l'arrivée du joueur, et un replay de la
  partie à plusieurs commence aussitôt.
- **À terme, un classement 1CC MULTI** : chaque joueur y fait sa partie sur un crédit, et chaque
  borne certifie le score de son joueur. Il demande un jeu qui affiche le score de chaque joueur, et
  le seul crédit permis en plus du départ y sera celui de l'arrivée d'un joueur.

## Le meilleur score, jamais le dernier
Sur une partie, on retient **le meilleur score atteint** (avant un éventuel continue), jamais la
valeur affichée au moment où tu quittes. Au classement, c'est **ta meilleure partie** qui compte :
enchaîner les parties ne peut jamais te coûter ton record, une partie ratée n'efface pas la
précédente.

## Les réglages doivent être identiques
Deux scores ne sont comparables **qu'à réglages égaux**. Le nombre de vies, la
difficulté, les seuils de vie bonus changent tout : un 1cc à 5 vies en facile n'est
pas le même exploit qu'un 1cc à 3 vies en difficile.

Un score certifié n'est donc valable **qu'aux réglages de référence** (par défaut
« usine ») du jeu. Les réglages font partie de l'**identité** du record, au même titre
que la ROM, l'émulateur et le listener homologué. Un score joué avec des réglages
modifiés reste ton score, mais il n'entre pas au classement certifié de référence.

**Ce qui compte comme réglage** : ce qui change la partie, et rien d'autre. Vies,
difficulté, bonus, vitesse du processeur, ROM patchée, cheats, reprise de partie. Un
réglage d'affichage ou de manette n'entre **jamais** en ligne de compte : résolution,
format d'image, filtres, zone morte, sensibilité, tir automatique du frontend. Ils
dépendent de l'écran et des manettes de chacun, pas du jeu.

### La borne applique les réglages avant la partie
Depuis APIExpose 1.8.12 (1.8.13 pour le rembobinage), tu n'as plus à connaître les réglages de référence : le profil
du jeu les publie en clair, et la borne les **applique au chargement** pour un jeu ouvert
au scoring (option « Force certified settings », allumée par défaut). Rien n'est réécrit
dans tes fichiers : le listener répond la valeur certifiée quand le cœur lit ses options,
et tout revient à la normale sur un jeu qui n'est pas ouvert.

La borne neutralise aussi, pour ce jeu seulement, ce que RetroBat active par défaut et qui
ferait refuser le score : le **rembobinage** (Rewind vaut « auto », c'est-à-dire allumé pour
presque tous les cœurs), le **run-ahead** et la **sauvegarde d'état automatique**. Elle écrit
les réglages RetroBat du jeu dès sa sélection dans le menu ; rien ne change pour les autres
jeux ni pour tes réglages globaux. Forçage éteint, elle te le dit avant la partie.

Au chargement, la borne demande aussi à la plateforme un **verdict avant la partie**, avec
exactement le code du verdict final : « partie certifiable », ou la raison pour laquelle
elle ne l'est pas (émulateur non reconnu, ROM, BIOS). Tu le sais avant de jouer, pas après.
Ce qui ne se voit qu'en jouant (cheats, rembobinage, entrées) reste vérifié à la fin.

## Ce qui refuse, ce qui signale, ce qui informe
Un score n'a que trois sorts, décidés au dépôt, par des règles publiques :

| Sort | Ce qui le déclenche | Conséquence |
|---|---|---|
| **Certifié** | passeport valide, rien à signaler | classé, certificat, scellé sur Bitcoin |
| **Signalé** | une **macro** : une même seconde d'entrées rejouée à l'identique, image par image, cinq fois ou plus | gardé sur ton compte, visible de toi seul, jamais classé ni scellé |
| **Refusé** | triche logicielle (cheats, rembobinage, avance rapide, sauvegarde d'état), **entrées impossibles** (deux directions opposées tenues ensemble), émulateur, ROM, réglages ou listener non conformes, passeport invalide | rien de publié |

Un score signalé ou refusé n'existe nulle part ailleurs que sur ton compte, avec le motif
en clair. Le classement ne contient que du certifié.

Certaines choses se disent sans rien retirer au record, par un repère ⓘ à côté du score :
- **partie interrompue** : pas de fin de jeu (coupure, plantage, fermeture). Le score
  reste celui que les points de passage prouvent ; une interruption ne coûte jamais un record ;
- **tir automatique** : des appuis d'une régularité mécanique. C'est une information, pas
  une anomalie : des manettes d'époque le faisaient, et bien des jeux l'ont d'origine. Le
  profil de chaque jeu dit comment la lire : d'origine sur ce jeu (rien à signaler), absent du
  jeu d'origine (le repère le précise), ou sans objet pour ce jeu (rien à signaler) ;
- **réglages appliqués** : la borne s'est alignée sur le profil au lancement.

### Pourquoi une macro est une anomalie et pas le tir automatique
Un tir automatique, c'est **un** bouton répété à période fixe, sans direction : un matériel
d'époque savait le faire. Une macro, c'est une **séquence** de boutons ou de directions
différents, rejouée à l'identique à l'image près : il faut un appareil programmable, et
aucun jeu ne l'a jamais permis. La borne compte l'une et l'autre sans rien coûter à la
partie ; la plateforme tranche au dépôt. Une routine apprise par un joueur ne tombe pas
dans le filet : ses durées varient toujours d'une image ou deux.

## Tous les jeux ne sont pas éligibles au 1cc
Un jeu n'ouvre un classement 1cc que si la borne sait y reconnaître un continue :

| Le jeu fournit… | Classement possible |
|---|---|
| en arcade, son compteur de crédits | **1cc** (un crédit, sans continue) |
| sur console, aucun continue, ou un continue reconnaissable | **1cc** |
| un score, avec un continue qu'on ne sait pas reconnaître | pas de 1cc : on ne peut pas prouver « sans continue » |
| pas de score lisible | non classé |

La couverture s'étend donc au rythme des jeux vérifiés : c'est un travail de données, jeu par jeu.

## Un classement par mode de jeu
Certains jeux se jouent de plusieurs façons qui ne se comparent pas : Tetris sur Game Boy a un
type A (score sans fin) et un type B (25 lignes à faire). Chaque mode a **son classement**, donc son
profil, avec son propre `ruleset`.

- La définition mémoire du jeu lit le mode choisi (action `GAME_MODE`). Le profil dit **quelle
  valeur** il couvre ; le passeport signe **le mode joué** dans `game.mode`. La plateforme refuse
  une partie dont le mode n'est pas celui du classement, et une partie sans mode mesuré.
- La **difficulté de départ** (niveau, hauteur, difficulté choisie au menu, action
  `GAME_DIFFICULTY`) est signée dans `game.difficulty`, une valeur par adresse mémoire.
  Par défaut elle est **libre et affichée** : elle ne sépare pas les classements, elle s'affiche à
  côté du score. Un profil peut la **restreindre** à une liste de valeurs ; ce qui en sort est refusé.
- La valeur qui compte est celle **en vigueur au début du run retenu**. Le profil déclare la valeur
  de démarrage de chaque champ : un joueur qui ne touche à rien au menu n'émet aucun signal, et
  c'est elle qui vaut.

## En résumé
- Une **partie**, c'est un lancement du jeu : quitter la termine et garde ton score.
- **1cc = un crédit, sans continue**, jeu fini ou non ; arcade et console, même règle.
- En arcade, **tout crédit consommé après le départ est un continue** : le 1cc s'arrête au dernier
  score affiché avant lui, et la partie n'est pas refusée.
- Pour une nouvelle partie classée, **quitte le jeu et relance-le**.
- Les **vies** ne coupent jamais un 1cc.
- Le 1cc est **solo** ; un joueur qui te rejoint n'est pas un continue, et ton score fait seul
  avant son arrivée reste certifié.
- **Réglages de référence** obligatoires ; la borne les applique elle-même avant la partie.
- **Trois sorts** : certifié, signalé (macro : gardé pour toi, jamais classé), refusé.
- Une **partie interrompue** garde son score ; le **tir automatique** est une information.
- **Meilleur** score, jamais le dernier.
- Le 1cc demande un jeu dont la borne sait reconnaître le continue.
- Un jeu à **modes** a un classement par mode ; la **difficulté** de départ s'affiche à côté du score.
