# Vérifier un score soi-même

Vous n'avez pas à nous croire sur parole. Trois vérifications, indépendantes.

## 1. Rejouer le vérifieur sur les vecteurs de test
Les **vecteurs** (`vectors/*.json`) sont des couples **(passeport, verdict attendu)**.
Le vérifieur public (`ref/`) doit donner **exactement** ces verdicts. Chaque
implémentation (C#, PHP, C++…) doit produire le **même verdict, octet pour octet** -
c'est le critère de sortie du protocole.

Exemple (implémentation de référence C#) :
```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release
# → 11/11 vecteurs au verdict attendu
```
Si votre propre implémentation du vérifieur diverge d'un seul verdict, c'est un bug -
et il est public.

## 2. Vérifier la signature d'un passeport
Chaque passeport est **signé** par la machine (ECDSA P-256) sur sa **forme canonique**
(JSON Canonicalization Scheme, **RFC 8785**). Pour vérifier :
1. retirez le champ `signature` du passeport ;
2. canonicalisez le reste en JCS (clés triées, pas d'espaces, échappement minimal) ;
3. vérifiez la signature (ASN.1 DER, base64url) avec la clé publique du device
   (`key_id = SHA-256(SPKI DER)`).

La signature couvre **tout** : le score, les empreintes du core/contenu/MEM/listener,
les checkpoints, le ticket. Un octet modifié après coup = signature invalide.

## 3. Vérifier l'antériorité (ancrage blockchain)
Chaque score classé - et l'**ouverture** de chaque jeu - est regroupé dans un arbre de
Merkle dont la racine est ancrée via **OpenTimestamps sur Bitcoin**. Avec un client
OpenTimestamps standard, n'importe qui peut vérifier, **sans nous**, que la donnée
existait **avant l'inclusion dans un bloc Bitcoin donné**.

- `Soumis le … UTC` = heure applicative (déclarative) ;
- `Ancré - OpenTimestamps sur Bitcoin (bloc #NNN)` = **preuve d'antériorité**.

L'ancrage prouve l'**antériorité**, pas la véracité : il garantit qu'un record n'a pas
été antidaté avant l'ouverture du jeu, et qu'un retrait ultérieur est **lui aussi**
horodaté (l'histoire s'augmente, elle ne se réécrit pas).

## Ce que ces trois vérifications établissent ensemble
| Vérification | Ce qu'elle prouve |
|---|---|
| Vecteurs | Les **règles** appliquées sont exactement celles publiées. |
| Signature | Le passeport n'a **pas été altéré** et vient de **cette machine**. |
| Ancrage | La donnée **existait avant** un bloc Bitcoin - pas d'antidatage. |

Ce qu'elles ne prouvent pas : que le listener fermé a *lu* la bonne adresse mémoire.
Cette confiance-là vient de l'[homologation du listener](homologation.md).
