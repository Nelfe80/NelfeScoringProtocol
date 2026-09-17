# Règles de score — ce qui compte comme un record

Cette page explique **comment un score est jugé**, pour que chacun sache à quoi
s'en tenir. Le *comment on mesure* (adresses mémoire, algorithme du listener) reste
fermé — voir [Homologation](homologation.md) ; ici on décrit les **règles**, pas la
technique.

## L'unité, c'est le RUN (un crédit), pas la session
Un **run** court **tant que le jeu est joué**. Il commence quand la partie démarre
et il se **fige** à sa fin — une mort, un game over, la fin du jeu, un retour au
titre, un reset, ou la sortie de l'émulateur. Ce qui vient après (une nouvelle
tentative, un continue) appartient à **un autre run**.

Conséquence : **enchaîner les parties ne peut jamais te coûter ton record.** Chaque
run est jugé pour lui-même, et c'est **le meilleur run** qui est retenu au classement.
Faire un gros score puis rater la tentative suivante ne l'efface pas — le gros run a
déjà été figé et soumis.

## Le 1cc = zéro continue
Un record **1cc** (« one-credit-clear ») est un score obtenu **sans utiliser un seul
continue**. Dès qu'un continue est pris, le run n'est plus un 1cc : son score est figé
**à la première mort**, avant le continue.

C'est le sens universel du 1cc (bornes d'arcade, tableaux de shmups). Et c'est **la
même règle pour l'arcade et la console** : peu importe que la borne offre un ou
plusieurs continues par crédit — la barre « zéro continue » ne dépend pas de ce
réglage.

## Le meilleur score, jamais le dernier
On retient toujours **le meilleur run**, jamais le dernier joué. Si un jeu ne fournit
pas assez de repères pour découper les runs, on retient **le meilleur score atteint**
pendant la session — jamais la valeur finale, qui serait fragile.

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
  une anomalie : des manettes d'époque le faisaient, et bien des jeux l'ont d'origine ;
- **réglages appliqués** : la borne s'est alignée sur le profil au lancement.

### Pourquoi une macro est une anomalie et pas le tir automatique
Un tir automatique, c'est **un** bouton répété à période fixe, sans direction : un matériel
d'époque savait le faire. Une macro, c'est une **séquence** de boutons ou de directions
différents, rejouée à l'identique à l'image près : il faut un appareil programmable, et
aucun jeu ne l'a jamais permis. La borne compte l'une et l'autre sans rien coûter à la
partie ; la plateforme tranche au dépôt. Une routine apprise par un joueur ne tombe pas
dans le filet : ses durées varient toujours d'une image ou deux.

## Tous les jeux ne sont pas éligibles au 1cc strict
La finesse du jugement dépend de ce que le jeu **laisse voir** :

| Le jeu fournit… | Classement possible |
|---|---|
| l'état de jeu **et** les fins (mort, continue, fin) | **1cc strict certifié** + meilleur score |
| les fins seules (beaucoup de jeux d'arcade) | 1cc via l'écran de continue |
| seulement le score | **« meilleur score »** uniquement — pas de 1cc strict (on ne peut pas prouver « sans continue ») |
| pas de score lisible | non classé |

La couverture du **1cc strict** s'étend donc au rythme des jeux instrumentés — c'est
un travail de données, jeu par jeu, pas un interrupteur global.

## En résumé
- Le **run** (un crédit) est l'unité ; le **meilleur run** gagne.
- **1cc = zéro continue**, gelé à la première mort — arcade et console, même règle.
- **Réglages de référence** obligatoires ; la borne les applique elle-même avant la partie.
- **Trois sorts** : certifié, signalé (macro : gardé pour toi, jamais classé), refusé.
- Une **partie interrompue** garde son score ; le **tir automatique** est une information.
- **Meilleur** score, jamais le dernier.
- L'éligibilité au 1cc strict dépend des repères que le jeu expose.
