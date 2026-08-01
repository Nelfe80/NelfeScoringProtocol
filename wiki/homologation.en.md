# Listener homologation

The listener (`NelfeMemoryListener`) is the closed component that **measures** the score
in memory. Its credibility comes not from its (secret) code, but from its
**homologation** — like the closed firmware of a measuring instrument (a **technical**
analogy, not a regulatory claim).

## Vocabulary (precise)
- **NelfePlay-homologated**: each official build is signed and attested by the publisher.
- **Audited**: said only when an independent external audit **actually** took place.
- **Certified**: reserved for a real, formal certification program (accredited body). We
  do not use it until such a program exists.

## Public build sheet
Each listener version publishes:
```json
{
  "listener_build": "4.2.0",
  "sha256": "…",
  "publisher_signature": "…",
  "released_at": "…",
  "supported_protocol": 1,
  "homologation_suite": "listener-tests-2026.1",
  "audit_report": "…",
  "status": "authorized"
}
```
Each **scoring profile** references the authorized builds (`allowed_listener_sha256`).
The **passport** carries the listener hash **before / loaded / after** — measured
**independently by the open component** (not by the listener itself, to avoid
self-attestation).

## Homologation suite (black box, public)
Behavior can be proven **without revealing the algorithm**:
> ROM X + scenario Y → the on-screen score is **12,500** → the official listener must
> produce **12,500**.

The results are public; the memory address and how it is read are not.

## Revocation
A flaw in a build? We **revoke that build for new sessions** (`status: revoked`) without
making old scores unreadable: they stay verifiable with the historical profile and build.

## Toward crediting the closed component
Signed binary · **public SHA-256** per build · **external audit under NDA** with a
**public, code-free report** · public **SBOM** · optional source **escrow** · **public
behavioral tests** · **revocation policy** · **version history** · **vulnerability
disclosure program**.

## The limit, again
None of this *mathematically* proves the listener read the right address. It establishes
that a **homologated, unmodified** build was **bound to the right process** and that the
**public rules** were applied. Trust in the measurement rests on homologation — a
defensible basis, the same as real-world measuring instruments.
