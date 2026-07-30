# NelfePlay — Scoring rétro certifié

**Enregistrer et classer le *vrai* score d'un jeu rétro, de façon vérifiable par
n'importe qui — sans que le serveur possède la ROM ni l'émulateur.**

Ce dépôt contient le **protocole ouvert** : le format du passeport, les règles de
vérification, les tickets, le manifeste des profils, les **vecteurs de test** et le
**vérifieur public**. C'est tout ce qui décide **si** un score est classé, et
**comment**. La lecture du score en mémoire, elle, est faite par un composant séparé
(le *listener*) — voir [Transparence](transparence.md).

## Le principe en une phrase
> Les **règles et la vérification** sont **publiques et rejouables**. La **mesure
> mémoire** est réalisée par un **listener propriétaire homologué, signé, versionné
> et audité**.

## Ce qui est public (dans ce dépôt)
- le **format du passeport** de session (`schemas/`) ;
- l'**algorithme de vérification** (`ref/` — le *CoreVerifier*, en plusieurs langages) ;
- les **profils de scoring** signés du manifeste (`manifest/`) ;
- les **vecteurs de test** entrée→verdict (`vectors/`) que **tout le monde peut rejouer** ;
- les **codes de refus**, les **règles de classement**, la preuve d'**ancrage blockchain**.

## Ce qui n'est pas public (et pourquoi)
La logique de **lecture mémoire** (comment le listener trouve le score dans la RAM du
jeu) reste fermée — c'est un savoir-faire, et l'exposer aiderait la triche autant que
la concurrence. Mais elle n'entre **jamais** dans la garantie de sécurité : voir
[Transparence](transparence.md) et [Homologation du listener](homologation.md).

## Trois façons de vérifier, sans nous faire confiance
1. **La signature** : chaque passeport est signé (ECDSA P-256) sur sa forme canonique
   (JSON JCS, RFC 8785). Reproduisez la canonicalisation, vérifiez la signature.
2. **Les vecteurs** : lancez le vérifieur public sur `vectors/*` — vous obtenez
   exactement les mêmes verdicts que nous. Voir [Vérifier un score](verifier-un-score.md).
3. **L'antériorité** : chaque score classé est ancré via **OpenTimestamps sur
   Bitcoin** — n'importe qui peut prouver qu'il existait avant un bloc donné.

## Les règles du classement
- **Aucun score public non vérifié.** Après l'ouverture d'un jeu, un score est
  **publié** (certifié), **refusé**, ou **retenu** (anomalie statistique, non public,
  publié automatiquement au délai — jamais refusé sur la seule statistique).
- **Ligne de départ prouvée** : l'ouverture d'un jeu est datée et **ancrée** ; seuls
  les scores postérieurs comptent. Personne n'a d'avance.
- **Zéro arbitre humain** pour accepter/refuser un score. (Un humain valide en amont
  qu'un jeu lit bien son score — pas les scores eux-mêmes.)

## Voir aussi
- [Transparence : ce qui est ouvert, ce qui ne l'est pas](transparence.md)
- [Vérifier un score soi-même](verifier-un-score.md)
- [Homologation du listener](homologation.md)
