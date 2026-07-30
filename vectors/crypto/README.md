# Vecteurs crypto d'interopérabilité

Ces vecteurs isolent les deux primitives qui **doivent** être byte-identiques entre
tous les langages (C#, PHP, C++…), **indépendamment** des vecteurs de passeport.

## `jcs/` — canonicalisation RFC 8785
- `input.json` : une entrée avec clés dans le désordre, objet imbriqué, tableau,
  et une chaîne contenant `\n`, `\t`, `"`.
- `expected.jcs.txt` : sa **forme canonique JCS attendue, octet pour octet** (pas de
  saut de ligne final).

**Test :** canonicalisez `input.json` ; le résultat doit être **exactement** le
contenu de `expected.jcs.txt`. Une divergence d'un octet ici = signatures qui ne
vérifieront pas entre implémentations.

## `signature/` — ECDSA P-256 (SPKI + ASN.1 DER)
- `message.txt` : un message figé (octets exacts, sans saut de ligne).
- `signature.device.b64url` : sa signature ECDSA-P-256/SHA-256 (ASN.1 DER, base64url)
  par la **clé de test device** (`keys/device.pub.pem`, `key_id`
  `44d0aeacdc1943a61ff55e8982577ee3eb780b93f9b762939c349481dc1079cd`).

**Test :** la signature doit **vérifier** avec la clé publique device, sur le message.
Prouve que l'import SPKI + la vérification DER sont interopérables.

## Statut
- **C# : ✅** (les deux vecteurs passent). Voir `ref/csharp` (intégré au runner).
- PHP / C++ : les runners peuvent les vérifier de la même manière.

> ⚠️ Les clés de `keys/` sont des clés de **TEST**. Jamais en production.
