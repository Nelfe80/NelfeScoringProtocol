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

## Lancer les vecteurs
**C# (référence, régénère aussi profil + vecteurs) :**
```
cd ref/csharp/NelfeScoring.Vectors && dotnet run -c Release      # → 11/11
```
**PHP (NelfePlay) — rejoue les mêmes vecteurs :**
```
docker run --rm -v "$PWD:/app" php:8.4-cli php /app/ref/php/run-vectors.php   # → 11/11
```
**C++ (listener) — build + run :**
```
docker run --rm -v "$PWD:/app" -w /app gcc:14 sh -c \
  'apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq libssl-dev nlohmann-json3-dev >/dev/null 2>&1 \
   && g++ -std=c++20 -O2 ref/cpp/run_vectors.cpp -lssl -lcrypto -o /tmp/rv && /tmp/rv /app'   # → 11/11
```
Chaque `vectors/*.passport.json` est un cas ; `vectors/index.json` liste
`{vector, expected}`.

**Contrat inter-langages (critère de sortie du Lot 0)** : chaque port doit donner
**exactement** le même verdict sur `vectors/*`. Le vecteur `valid` qui passe est la
preuve d'un **JCS byte-identique** (sinon la signature ECDSA ne vérifie pas).
- **C# (APIExpose) : ✅ 11/11**
- **PHP (NelfePlay) : ✅ 11/11** (via `php:8.4-cli`)
- **C++ (listener) : ✅ 11/11** (via `gcc` + `libssl` + `nlohmann-json`)

## Vecteurs V1 (Sonic 1cc)
`valid` (→ pass) + refus déterministes : `core_mismatch`, `mem_mismatch`,
`listener_unauthorized`, `save_state`, `continue`, `monotonicity`, `correlation`,
`digest_mismatch`, `ticket_expired`, `signature_invalid`. À venir : vecteurs crypto
d'interop (triplet clé/message/signature figé) et cas statistiques (§6.6b, côté serveur).

## Statut
- **Lot 0 COMPLET** : CoreVerifier **C# ✅ + PHP ✅ + C++ ✅** (11/11 chacun, verdicts
  **identiques octet pour octet**), + vecteurs **crypto d'interop** (JCS + signature).
- **ServerAdmissionVerifier (§6.5) ✅** — référence PHP (`ref/php/src/ServerAdmission.php`),
  la couche À ÉTAT au-dessus du CoreVerifier : idempotence, révocations
  (device/clé/listener/profil), ticket consommé, **statistique → `held`** (jamais un
  refus), verdict `published`/`held`/`refused`/`duplicate`. **8/8** cas :
  ```
  docker run --rm -v "$PWD:/app" php:8.4-cli php /app/ref/php/run-admission.php   # → 8/8
  ```
  L'état passe par une interface `StateStore` (en prod : NelfePlay / account_devices +
  tables scoring ; en test : magasin mémoire).
- **Flux de soumission adossé à une base ✅** — `StateStore` implémenté sur **PDO**
  (`ref/php/src/PdoStateStore.php`, SQLite en test / MariaDB en prod, schéma
  `ref/php/sql/schema.sql`) + `SubmissionService` (vérifie → **persiste** l'audit et le
  score publié → calcule le **rang**). L'idempotence (session), l'usage unique du ticket,
  les révocations et le `held` sont **persistés en base**. **9/9** cas :
  ```
  docker run --rm -v "$PWD:/app" php:8.4-cli php /app/ref/php/run-submission.php   # → 9/9
  ```
  Reste à brancher : l'adaptateur `StateStore` sur les vraies tables NelfePlay + l'endpoint
  HTTP `POST /api/v1/scores/submissions` (le service ci-dessus EST sa logique).
- Suite : adaptateur `StateStore` + endpoint HTTP côté NelfePlay ; couche attestation du
  listener (SHA-256/handshake, additive) ; ancrage OTS. Plan (Lots 0-5).
