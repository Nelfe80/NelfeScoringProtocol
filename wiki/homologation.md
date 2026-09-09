# Homologation du listener

Le listener (`NelfeMemoryListener`) est le composant fermé qui **mesure** le score en
mémoire. Sa crédibilité ne vient pas de son code (secret), mais de son **homologation**
- comme le firmware fermé d'un instrument de mesure (analogie **technique**, pas une
revendication réglementaire).

## Vocabulaire (précis)
- **Homologué NelfePlay** : chaque build officiel est signé et attesté par l'éditeur.
- **Audité** : dit uniquement quand un audit externe indépendant a **réellement** eu lieu.
- **Certifié** : réservé à un vrai programme de certification formalisé (organisme
  accrédité). Nous ne l'employons pas tant qu'un tel programme n'existe pas.

## Fiche publique d'un build
Chaque version du listener publie :
```json
{
  "listener_build": "4.2.0",
  "sha256": "…",                     // empreinte publique du binaire
  "publisher_signature": "…",        // signé par l'éditeur
  "released_at": "…",
  "supported_protocol": 1,
  "homologation_suite": "listener-tests-2026.1",
  "audit_report": "…",               // si un audit a eu lieu
  "status": "authorized"             // authorized | revoked
}
```
Chaque **profil de scoring** référence les builds autorisés (`allowed_listener_sha256`).
Le **passeport** porte le hash du listener **avant / chargé / après** - mesuré
**indépendamment par le composant ouvert** (pas par le listener lui-même, pour éviter
l'auto-attestation).

## Homologation à la publication

Une fiche de build ne sert à rien tant que la plateforme ne la connaît pas. Tant que
l'homologation était un geste manuel, **chaque nouvelle version du listener invalidait la
flotte** jusqu'à ce que quelqu'un pense à l'enregistrer : les bornes à jour se voyaient
refuser leurs scores pour cause de build inconnu, ce qui est exactement l'inverse de
l'effet recherché.

Le manifeste est donc **publié avec le binaire**, signé, et la plateforme va le lire :

```json
{
  "built_at": "2026-09-05T21:13:53Z",
  "sha256": "1bd08a9d5d9aaac16692eab6f52278b3f072a143c20436271883d28025034e75",
  "signature": "MEUCIQD5QTn8FMBbiLBZKXLL9P_-1_f6cQAtiLFv9vphxYmqtQIgGdTPvOkMoF5EbwCiSCsBNu_IMJY94d6vGr_Fl60WPRI",
  "subject": "CN=nelfeTech",
  "version": "0.334.0.0"
}
```

La signature est une **ECDSA P-256 / SHA-256** sur le corps canonicalisé (RFC 8785),
transportée en base64url. La plateforme la vérifie contre une **clé publique épinglée dans
son code**, jamais contre une clé fournie par le manifeste : sans cet ancrage, n'importe
qui publiant un fichier au bon format ferait homologuer son propre binaire.

Trois propriétés de ce choix méritent d'être dites :

- **Le manifeste est tiré, pas poussé.** La plateforme relève une URL publique à
  intervalle régulier. Quiconque peut lire le même fichier et refaire la même
  vérification, ce qui rend l'homologation observable de l'extérieur.
- **Un build ne disparaît jamais tout seul.** L'automatisation ajoute, elle ne retire pas.
- **La révocation reste un acte délibéré** (voir plus bas), et elle prime sur la
  publication : un build retiré ne se ré-homologue pas parce qu'il est encore en ligne.

Le fichier étant l'ancre de toute la flotte, il doit être **produit par la chaîne de
signature elle-même**, jamais écrit à la main : un manifeste qui annoncerait une version
sans correspondre au binaire signé homologuerait une empreinte inexistante, et toutes les
bornes à jour tomberaient d'un coup.

## Suite d'homologation (boîte noire, publique)
On peut prouver le comportement **sans révéler l'algorithme** :
> ROM X + scénario Y → le score affiché à l'écran est **12 500**
> → le listener officiel doit produire **12 500**.

Les résultats de ces tests sont publics ; l'adresse mémoire et la manière de la lire
ne le sont pas.

## Révocation
Une faille dans un build ? On **révoque ce build pour les nouvelles parties** (statut
`revoked`) sans rendre les anciens scores incompréhensibles : ils restent vérifiables
avec le profil et le build historiques.

## Pour crédibiliser le composant fermé
Vers une reconnaissance large : binaire **signé**, **SHA-256 public** par build, **audit
externe sous NDA** avec **rapport public sans code**, **SBOM** publique, **séquestre**
éventuel du source, **tests comportementaux publics**, **politique de révocation**,
**historique des versions**, **programme de signalement de vulnérabilités**.

## La limite, encore
Aucun de ces éléments ne prouve *mathématiquement* que le listener a lu la bonne
adresse. Ils établissent qu'un **build homologué, non modifié**, était **lié au bon
processus** et que les **règles publiques** ont été appliquées. La confiance dans la
mesure repose sur l'homologation - et c'est une base défendable, la même que celle des
instruments de mesure du monde réel.
