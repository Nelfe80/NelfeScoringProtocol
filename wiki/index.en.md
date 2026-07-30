# NelfePlay — Certified Retro Scoring

**Record and rank a retro game's *real* score, verifiable by anyone — without the
server holding the ROM or the emulator.**

This repository is the **open protocol**: the passport format, the verification rules,
the tickets, the profile manifest, the **test vectors** and the **public verifier** —
everything that decides **whether** a score is ranked, and **how**. Reading the score
from memory is done by a separate component (the *listener*).

## The principle, in one sentence
> The **rules and verification** are **public and replayable**. The **memory
> measurement** is performed by a **proprietary listener that is homologated, signed,
> versioned and audited**.

## What is public (in this repo)
Passport schemas · the **verification algorithm** (the *CoreVerifier*, in several
languages) · signed **scoring profiles** · **test vectors** anyone can replay · refusal
codes · ranking rules · **OpenTimestamps-on-Bitcoin** anchoring proof.

## What is not public (and why)
The **memory-reading logic** (how the listener locates the score in the game's RAM)
stays closed — it is know-how, and exposing it would help cheaters and competitors
alike. But it is **never** part of the security guarantee (Kerckhoffs' principle): the
system's security rests only on the secrecy of the **device signing key**.

## Verify without trusting us
1. **Signature** — every passport is signed (ECDSA P-256) over its canonical form
   (JSON JCS, RFC 8785). Reproduce the canonicalization, verify the signature.
2. **Vectors** — run the public verifier over `vectors/*`; you get exactly the same
   verdicts we do.
3. **Anteriority** — every ranked score is anchored via **OpenTimestamps on Bitcoin**;
   anyone can prove it existed before a given block.

## The honest limit
The open protocol will never *mathematically* prove the closed listener actually read
memory. It proves the **homologated build was present, bound to the right process,
unmodified**, and that the **public rules were applied**. Trust in the *measurement*
rests on a homologated, signed, versioned and audited listener — the same trust model
as real-world measurement instruments.

See the French pages for full detail: [Transparence](transparence.md) ·
[Vérifier un score](verifier-un-score.md) · [Homologation](homologation.md).
