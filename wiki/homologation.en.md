# Listener homologation

The listener (`NelfeMemoryListener`) is the closed component that **measures** the score
in memory. Its credibility comes not from its (secret) code, but from its
**homologation** - like the closed firmware of a measuring instrument (a **technical**
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
The **passport** carries the listener hash **before / loaded / after** - measured
**independently by the open component** (not by the listener itself, to avoid
self-attestation).

## Homologation at publication time

A build sheet is worthless until the platform knows about it. As long as homologation was a
manual step, **every new listener build invalidated the fleet** until someone remembered to
register it: up-to-date cabinets had their scores refused for an unknown build, which is the
exact opposite of the intended effect.

The manifest is therefore **published alongside the binary**, signed, and the platform goes
and reads it:

```json
{
  "built_at": "2026-09-05T21:13:53Z",
  "sha256": "1bd08a9d5d9aaac16692eab6f52278b3f072a143c20436271883d28025034e75",
  "signature": "MEUCIQD5QTn8FMBbiLBZKXLL9P_-1_f6cQAtiLFv9vphxYmqtQIgGdTPvOkMoF5EbwCiSCsBNu_IMJY94d6vGr_Fl60WPRI",
  "subject": "CN=nelfeTech",
  "version": "0.334.0.0"
}
```

The signature is **ECDSA P-256 / SHA-256** over the canonicalised body (RFC 8785), carried as
base64url. The platform verifies it against a **public key pinned in its own code**, never
against a key supplied by the manifest: without that anchor, anyone publishing a file in the
right format would get their own binary homologated.

Three properties of this design are worth stating:

- **The manifest is pulled, not pushed.** The platform polls a public URL. Anyone can read the
  same file and redo the same verification, which makes homologation observable from outside.
- **A build never disappears on its own.** The automation adds, it does not remove.
- **Revocation stays a deliberate act** (see below), and it takes precedence over publication:
  a withdrawn build is not re-homologated just because it is still online.

Since this file is the anchor for the whole fleet, it must be **produced by the signing chain
itself**, never written by hand: a manifest announcing a version that does not match the signed
binary would homologate a hash that does not exist, and every up-to-date cabinet would fall at
once.

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
**public rules** were applied. Trust in the measurement rests on homologation - a
defensible basis, the same as real-world measuring instruments.
