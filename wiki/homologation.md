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
