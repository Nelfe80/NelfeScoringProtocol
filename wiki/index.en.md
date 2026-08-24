# NelfePlay - Certified Retro Scoring

**Record and rank a retro game's *real* score, verifiable by anyone - without the
server holding the ROM or the emulator.**

[The certified records →](records.md){ .md-button .md-button--primary }
[Verify a score →](https://nelfeplay.com/verify/){ .md-button }

![](assets/chain-of-trust-en.svg)

## The principle, in one sentence
> The **rules and verification** are **public and replayable**. The **memory
> measurement** is performed by a **proprietary listener that is homologated, signed,
> versioned and audited**.

## What is public (this repo)
The **passport format** (`schemas/`) · the **verification algorithm** (`ref/`, the
*CoreVerifier*, in several languages) · the **signed profiles** (`manifest/`) · the
replayable **test vectors** (`vectors/`) · the **refusal codes**, **ranking rules**, and
the **Bitcoin anchoring** proof.

## Verify without trusting us
1. **Signature** - every passport is signed (ECDSA P-256) over its canonical form
   (JCS, RFC 8785).
2. **Vectors** - run the public verifier over `vectors/*`: the same verdicts we get.
3. **Anteriority** - every score is anchored via **OpenTimestamps on Bitcoin**.

## Go further
- [The certified records - the whole process](records.md)
- [Transparency: what is open, what is not](transparence.md)
- [Verify a score yourself](verifier-un-score.md)
- [Host the verifier](heberger-le-verifieur.md)
- [Listener homologation](homologation.md)
