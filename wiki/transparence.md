# Transparence : ce qui est ouvert, ce qui ne l'est pas

Notre transparence porte sur **comment NelfePlay décide**, pas sur **comment le
listener extrait le signal**. C'est une distinction volontaire et assumée.

## La frontière de confiance
```
RetroArch
   │
   ▼
NelfeMemoryListener  ── PROPRIÉTAIRE, HOMOLOGUÉ ─────────────────────────
   lit la mémoire, résout les adresses, calcule le score et les compteurs,
   produit des « checkpoints » bruts
   │
   ▼  événement normalisé  { score, compteurs, frame, temps, événement }
   │
Protocole ouvert (ce dépôt)  ── PUBLIC ─────────────────────────────────
   ticket · canonicalisation JCS · passeport · signature · vérification · soumission
```
Le code public sait vérifier la **continuité** et la **cohérence** de ces événements ;
il ne sait **pas** comment ils ont été obtenus.

## Pourquoi le listener est fermé
La logique de lecture mémoire est un savoir-faire coûteux à produire (une définition
par jeu, revalidée à chaque évolution de core). L'ouvrir la donnerait à la
concurrence **et** faciliterait la triche. Nous la gardons donc fermée - comme le
firmware d'un instrument de mesure.

## Ce que la fermeture N'EST PAS
La fermeture **ne fait pas partie de la sécurité** (principe de Kerckhoffs). La
sécurité du système ne repose **que** sur le secret de la **clé de signature de la
machine** - jamais sur le secret des règles. Toutes les règles, tous les contrôles,
tous les codes de refus sont **publics**. Si demain le code du listener fuitait, la
garantie du système ne changerait pas d'un iota : elle vient de l'ouvert.

## La limite, dite honnêtement
Le protocole ouvert **ne prouvera jamais mathématiquement** que le listener a
*réellement* lu la mémoire. Il prouve autre chose, de vérifiable :
- que le **build homologué** (au hash connu) était **présent** ;
- qu'il était **lié au bon processus** (le vrai émulateur, le vrai contenu) ;
- qu'il n'a **pas été modifié** pendant la session ;
- que les événements n'ont **pas été altérés** après leur émission (signature) ;
- que le serveur a appliqué **publiquement les bonnes règles**.

La confiance dans la *mesure* repose donc sur un listener **homologué, signé,
versionné et audité** - pas sur du code secret. Voir [Homologation](homologation.md).

## Ce qui reste 100 % public
Format du passeport · tickets · manifeste · règles des profils · empreintes
autorisées · vérification des signatures · états des soumissions · règles de
classement · **ancrage OpenTimestamps sur Bitcoin** · **codes de refus** · le
**vérifieur public** · les **résultats de la suite d'homologation** du listener.

## Une promesse qu'on peut tenir
> « Les règles et la vérification NelfePlay sont publiques et rejouables. La mesure
> mémoire est réalisée par un listener propriétaire homologué, signé, versionné et
> audité. »

Pas « la triche est mathématiquement impossible » - ce serait faux pour un logiciel
tournant sur le PC du joueur. Mais une garantie **précise et opposable**, c'est mieux
qu'une promesse invérifiable.
