# Verify a score yourself

You don't have to take our word for it. Three independent checks.

## 1. Replay the verifier on the test vectors
The **vectors** (`vectors/*.json`) are **(passport, expected verdict)** pairs. The public
verifier (`ref/`) must return **exactly** those verdicts — the same verdict, byte for
byte, in every implementation (C#, PHP, C++…). That is the protocol's exit criterion.

```
cd ref/csharp/NelfeScoring.Vectors
dotnet run -c Release      # → 11/11 vectors at the expected verdict
```

## 2. Verify a passport's signature
Every passport is **signed** by the machine (ECDSA P-256) over its **canonical form**
(JSON Canonicalization Scheme, **RFC 8785**):

1. remove the `signature` field;
2. canonicalize the rest in JCS (sorted keys, no spaces, minimal escaping);
3. verify the signature (ASN.1 DER, base64url) with the device public key
   (`key_id = SHA-256(SPKI DER)`).

The signature covers **everything**: score, core/content/MEM/listener fingerprints,
checkpoints, ticket. One byte changed afterwards = invalid signature.

## 3. Verify anteriority (blockchain anchoring)
Every ranked score — and each game's **opening** — is grouped into a Merkle tree whose
root is anchored via **OpenTimestamps on Bitcoin**. With a standard OpenTimestamps
client, anyone can verify, **without us**, that the data existed **before a given Bitcoin
block**.

Anchoring proves **anteriority**, not veracity: it guarantees a record wasn't backdated
before the game's opening, and that a later withdrawal is **also** timestamped (history
grows, it is not rewritten).

## What the three establish together
| Check | What it proves |
|---|---|
| Vectors | The **rules** applied are exactly those published. |
| Signature | The passport was **not altered** and comes from **that machine**. |
| Anchoring | The data **existed before** a Bitcoin block — no backdating. |

What they do not prove: that the closed listener *read* the right memory address. That
trust comes from the [listener homologation](homologation.md).
