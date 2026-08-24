# Transparency: what is open, what is not

Our transparency is about **how NelfePlay decides**, not **how the listener extracts the
signal**. That distinction is deliberate.

## The trust boundary
```
RetroArch
   │  ▼
NelfeMemoryListener  - CLOSED · HOMOLOGATED ----------------
   reads memory, resolves addresses, computes score+counters,
   emits raw checkpoints
   │  ▼  normalized event { score, counters, frame, time, event }
Open protocol (this repo)  - PUBLIC ------------------------
   ticket · JCS canonicalization · passport · signature · verify · submit
```
The public code knows how to verify the **continuity** and **consistency** of these
events; it does **not** know how they were obtained.

## Why the listener is closed
Memory-reading logic is expensive know-how (one definition per game, re-validated on
every core change). Opening it would hand it to competitors **and** help cheaters. We
keep it closed - like the firmware of a measuring instrument.

## What closure is NOT
Closure is **not part of the security** (Kerckhoffs' principle). The system's security
rests **only** on the secrecy of the **device signing key** - never on secret rules. All
rules, all checks, all refusal codes are **public**. If the listener code leaked
tomorrow, the guarantee would not change by an inch: it comes from the open.

## The honest limit
The open protocol **will never mathematically prove** the listener *actually* read
memory. It proves, verifiably: the **homologated build** (known hash) was **present**,
**bound to the right process**, **unmodified** during the session; the events were **not
altered** after emission (signature); and the server applied **the public rules**.

Trust in the *measurement* therefore rests on a listener that is **homologated, signed,
versioned and audited** - see [Homologation](homologation.md).

## What stays 100% public
Passport format · tickets · manifest · profile rules · allowed fingerprints · signature
verification · submission states · ranking rules · **OpenTimestamps-on-Bitcoin
anchoring** · **refusal codes** · the **public verifier** · the listener's
**homologation-suite results**.

## A promise we can keep
> "NelfePlay's rules and verification are public and replayable. The memory measurement
> is done by a proprietary listener that is homologated, signed, versioned and audited."

Not "cheating is mathematically impossible" - that would be false for software running on
the player's PC. But a **precise, accountable** guarantee beats an unverifiable promise.
