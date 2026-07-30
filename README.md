# NelfeScoringProtocol — scoring rétro certifié (composant OUVERT)

Implémentation **publique et auditable** du protocole de scoring certifié NelfePlay :
format du passeport, vérification, tickets, manifeste, vecteurs de test, ancrage.
La **mesure mémoire** (lecture du score) N'EST PAS ici — c'est le listener
propriétaire homologué (`NelfeMemoryListener`), séparé. Voir le contrat figé
`APIExpose/docs/SPEC_PASSEPORT_SCORING_V1.md` (v1.0) — doc interne, non publiée.

## Frontière de confiance (rappel)
```
NelfeMemoryListener (PROPRIÉTAIRE, homologué)  ──événement normalisé──▶  CE PROTOCOLE (OUVERT)
  mesure .MEM / score / checkpoints                                     ticket · JCS · passeport · signature · vérif
```
La transparence porte sur **comment on décide**, pas sur **comment le listener
extrait le signal**. Le code ici ne prouve pas la mesure ; il prouve que le build
homologué était présent, lié au bon process, non modifié, et que les règles publiques
ont été appliquées.

## Arborescence
```
schemas/        schémas JSON stricts (passport / ticket / profile)
manifest/       manifeste public — profils de scoring signés, versionnés, immuables
  profiles/megadrive/sonic-the-hedgehog/1.json   ← V1 : Sonic 1cc
vectors/        vecteurs de test (entrée → verdict attendu) — LE juge de paix
keys/           clés ECDSA P-256 de TEST (device + issuer) — NE PAS utiliser en prod
ref/
  csharp/       implémentation de RÉFÉRENCE du CoreVerifier (C#) + générateur de vecteurs
  php/  cpp/    (à venir : les ports serveur PHP et listener/protocole C++)
```

## CoreVerifier
Vérifieur **déterministe, SANS état** (SPEC §6.1-6.4) : JCS, empreintes, signatures
device+ticket, profil, listener, modules par rôle, checkpoints (monotonie +
`correlation_rules` par événement), métrique. Il produit `local_check` côté machine et
le socle du verdict côté serveur. Les contrôles **à état** (révocations, ticket
consommé, statistiques → `held`, rangs) sont le **ServerAdmissionVerifier** (§6.5), hors
de ce composant partagé.

**Format figé** : canonicalisation **RFC 8785 (JCS)** ; empreintes **SHA-256** hex ;
signatures **ECDSA P-256**, clé **SPKI DER**, signature **ASN.1 DER**, encodage
**base64url** ; `key_id = SHA-256(SPKI_DER)`. Ancrage : **OpenTimestamps sur Bitcoin**
(hors CoreVerifier).

## Lancer les vecteurs (C#)
```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release
```
Régénère `manifest/…/1.json` + `vectors/*.json` et vérifie **11/11** verdicts. Chaque
`vectors/*.passport.json` est un cas ; `vectors/index.json` liste `{vector, expected}`.

**Contrat inter-langages** : PHP (NelfePlay) et C++ (listener) porteront le **même**
CoreVerifier et devront donner **exactement** le même verdict sur `vectors/*` — c'est
le critère de sortie du Lot 0.

## Vecteurs V1 (Sonic 1cc)
`valid` (→ pass) + refus déterministes : `core_mismatch`, `mem_mismatch`,
`listener_unauthorized`, `save_state`, `continue`, `monotonicity`, `correlation`,
`digest_mismatch`, `ticket_expired`, `signature_invalid`. À venir : vecteurs crypto
d'interop (triplet clé/message/signature figé) et cas statistiques (§6.6b, côté serveur).

## Statut
- **Lot 0 (contrat + vecteurs + CoreVerifier de référence) : EN COURS** — C# vert.
- Suite : ports PHP/C++, ServerAdmissionVerifier, couche attestation du listener,
  endpoint de soumission NelfePlay, ancrage OTS. Découpage dans le plan (Lots 0-5).
