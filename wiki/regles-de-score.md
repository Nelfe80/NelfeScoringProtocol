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
- **Réglages de référence** obligatoires ; sinon, hors classement certifié.
- **Meilleur** score, jamais le dernier.
- L'éligibilité au 1cc strict dépend des repères que le jeu expose.
