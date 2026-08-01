# Les records certifiés

Un **classement public** de scores rétro que **personne ne peut truquer** — et que
**n'importe qui peut vérifier**, sans nous faire confiance. Voici tout ce qui se passe,
de la partie jouée jusqu'à la preuve sur Bitcoin.

[Voir le classement en direct →](https://nelfeplay.com/records/megadrive/sonic-the-hedgehog/1cc/){ .md-button .md-button--primary }
[Vérifier soi-même →](https://nelfeplay.com/verify/){ .md-button }

## La chaîne de confiance, d'un coup d'œil

![](assets/chain-of-trust-fr.svg)

Chaque étape est **soit publique et rejouable, soit homologuée et signée**. La sécurité
ne repose **jamais** sur un secret (principe de Kerckhoffs) — seulement sur l'ouvert.

## 1 · Mesuré, pas déclaré
Le score n'est **pas envoyé par le jeu**. Un **composant homologué** (le *listener*) lit
la valeur directement dans la mémoire de l'émulateur, à la source, avec des *checkpoints*
horodatés. Aucun score « déclaré » n'entre dans le système.

## 2 · Signé sur la machine
La borne assemble un **passeport de session** (score, empreintes du core/dump/listener,
checkpoints, ticket) et le **signe** avec une clé matérielle **non exportable**
(ECDSA P-256). Un octet modifié après coup = signature invalide.

## 3 · Vérifié côté serveur
Le serveur **ne rejoue pas le jeu** : il applique des **règles publiques** (le
*CoreVerifier*, open source) — empreintes attendues, monotonie de la trajectoire, fin de
partie, ticket valide — puis rend un verdict **publié**, **retenu** (anomalie statistique,
jamais un refus sec) ou **refusé**. Zéro arbitre humain.

## 4 · Publié dans un index signé
Les scores publiés forment un **index signé** : la liste complète + une **empreinte
SHA-256** signée par l'émetteur. C'est cet index qui reconstruit le classement — et qui
rend une perte de base **sans conséquence** (il est reconstructible et miroitable).

![](assets/shots/records.png)

## 5 · Scellé sur Bitcoin
L'empreinte de l'index est **horodatée sur Bitcoin** via **OpenTimestamps**. Une fois
confirmée, elle prouve que les records **existaient avant un bloc donné** — antériorité
**immuable**. Un score fraîchement scellé s'affiche en **or** ; la preuve `.ots` est
téléchargeable et vérifiable avec le client OpenTimestamps standard.

## 6 · Le Certificat de record
Chaque score a une page **immuable et partageable** : score, empreintes du dump
(MD5 + SHA-256), signature ✓, et le **sceau Bitcoin** (bloc). Pas de rang dessus — le
rang vit sur le classement.

![](assets/shots/certificate.png)

## 7 · Vérifiable sans nous faire confiance
Le **vérifieur public** recalcule l'empreinte, **vérifie la signature** (Web Crypto) et
lit l'état de scellement — **dans votre navigateur**. Il ne prend rien pour argent
comptant. Vous pouvez même l'**héberger vous-même**.

![](assets/shots/verify.png)

[Vérifier maintenant →](https://nelfeplay.com/verify/){ .md-button .md-button--primary }
[Héberger le vérifieur →](heberger-le-verifieur.md){ .md-button }

## La limite, dite honnêtement
Le protocole ouvert **ne prouve pas mathématiquement** que le listener fermé a *lu* la
bonne adresse. Il prouve que le **build homologué était présent, lié au bon processus,
non modifié**, et que les **règles publiques ont été appliquées**. La confiance dans la
*mesure* vient d'un listener **homologué, signé, versionné, audité** — voir
[Transparence](transparence.md) et [Homologation](homologation.md).
