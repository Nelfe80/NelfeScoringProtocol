#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# mirror.sh - take a durable, self-verifiable SNAPSHOT of the NelfePlay records.
#
# Downloads the signed index, the anchor metadata, and every OpenTimestamps (.ots)
# proof into ./snapshot/. That snapshot is enough to prove the records EXISTED and
# were sealed on Bitcoin - even if nelfeplay.com disappears. Nothing here trusts us:
# the signature is re-checkable offline, and the .ots proofs verify against Bitcoin
# with the standard OpenTimestamps client (`pip install opentimestamps-client`).
#
#   ./mirror.sh                       # mirror from nelfeplay.com
#   ./mirror.sh https://your.mirror   # mirror from any host serving the same API
#
# Requires: curl, python3 (for pretty JSON; optional).
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
BASE="${1:-https://nelfeplay.com}"
OUT="snapshot"
mkdir -p "$OUT"

echo "→ index signé…"
curl -fsS "$BASE/api/v1/scores/index"   -o "$OUT/index.json"
echo "→ ancres…"
curl -fsS "$BASE/api/v1/scores/anchors" -o "$OUT/anchors.json"

# Une preuve .ots par génération confirmée (téléchargée en base64 → binaire .ots).
echo "→ preuves .ots…"
gens="$(python3 - "$OUT/anchors.json" <<'PY' 2>/dev/null || true
import json,sys
d=json.load(open(sys.argv[1]))
print(' '.join(str(a['generation']) for a in d.get('anchors',[])))
PY
)"
for g in $gens; do
  b64="$(curl -fsS "$BASE/api/v1/scores/anchor-proof?generation=$g" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("ots_b64") or "")')"
  if [ -n "$b64" ]; then
    # base64url → base64 → binaire
    printf '%s' "$b64" | tr '_-' '/+' | base64 -d > "$OUT/records-index-gen$g.ots" 2>/dev/null \
      && echo "   gen $g → records-index-gen$g.ots"
  fi
done

cat > "$OUT/VERIFY.txt" <<'TXT'
Ce dossier est un instantané auto-vérifiable des records NelfePlay.

1) SIGNATURE - ouvrez ../verify.html (il recalcule l'empreinte de index.json et
   vérifie la signature ECDSA P-256 dans votre navigateur, sans serveur).

2) BITCOIN - chaque records-index-genN.ots prouve l'antériorité sur Bitcoin.
   Vérifiez-le sans nous, avec le client OpenTimestamps standard :
       pip install opentimestamps-client
       ots verify records-index-gen1.ots       # (attend le fichier d'origine)
   Le message ancré est le "root" (hex) présent dans index.json.

Tant que vous gardez ce dossier, les records restent prouvables - pour toujours.
TXT

echo "OK - instantané dans ./$OUT/  ($(date -u '+%Y-%m-%d %H:%M UTC'))"
