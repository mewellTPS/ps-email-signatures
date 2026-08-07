#!/usr/bin/env bash
# Build the v3 "rotating ball" animated GIF for the Purple Standard signature.
#
# Cycles the seven brand marks (tps-badge first, then the six brands) with a
# horizontal-squeeze transition: the outgoing mark compresses toward the vertical
# centre line while the incoming one expands out of it. Read as a sphere/coin
# turning. Uses the treatment-C (native shape) frames Michael selected.
#
# Requires: bash build-icons.sh (produces out/ball-c/).
# Usage:    bash build-ball-gif.sh
#
# Frame 0 is tps-badge deliberately: any client that declines to animate shows
# the first frame, which must therefore be the Purple Standard badge that v1/v2
# ship statically. Verified below.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMES="$HERE/out/ball-c"
OUT="$HERE/out/ball"
GIF="$OUT/tps-badge-cycle.gif"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

SIZE=150          # 2x the 75px display slot (ADR 0008)
HOLD=140          # centiseconds each mark rests, fully upright
STEP=6            # centiseconds per transition frame
HALF=4            # transition frames per half-turn (out, then in)
BG=white          # the signature sits on white; GIF's 1-bit alpha would hard-edge
                  # the antialiased mark edges, so composite on white instead.

# GIF is capped at 256 colours, and ACE's illustration plus Brisa's gradient are
# the two marks that suffer. Values below were picked by sweeping and comparing
# against the source AT THE 75px SHIPPING SIZE, not zoomed in:
#   +dither, 64 colours  -> 164 KiB but visible banding across Brisa's gradient
#   Riemersma, 128       -> 166 KiB and near-indistinguishable from source
# Riemersma compresses better than Floyd-Steinberg here because its error
# diffusion follows a space-filling curve, so it produces less high-frequency
# noise for LZW to encode.
DITHER=Riemersma
COLORS=128
MAXBYTES=262144   # 256 KiB. A signature loads on every message; heavier than
                  # this is not worth the animation.

order=(
  "$FRAMES/ball-0-ps.png"
  "$FRAMES/ball-1-ace.png"
  "$FRAMES/ball-2-purple-current.png"
  "$FRAMES/ball-3-boyette.png"
  "$FRAMES/ball-4-wtr-dr.png"
  "$FRAMES/ball-5-brisa.png"
  "$FRAMES/ball-6-tyrian.png"
)
for f in "${order[@]}"; do [[ -f "$f" ]] || { echo "missing frame: $f (run build-icons.sh)"; exit 1; }; done

# flatten each mark onto white once
flat=()
for i in "${!order[@]}"; do
  o="$WORK/flat-$i.png"
  magick "${order[$i]}" -background "$BG" -alpha remove -alpha off \
    -resize "${SIZE}x${SIZE}!" "$o"
  flat+=("$o")
done

# width of the squeezed mark at step s of HALF, as a cosine so the apparent
# rotation is linear in angle rather than in width (a linear ramp reads as a
# squash, not a turn).
half_width() {  # half_width <step> <total>  -> integer px, min 1
  python3 -c "
import math,sys
s,t,size=int(sys.argv[1]),int(sys.argv[2]),$SIZE
print(max(1,round(size*math.cos(math.pi/2*s/t))))" "$1" "$2"
}

# Build the frame list: hold, then turn, for each mark, wrapping back to frame 0.
args=()
n=${#flat[@]}
for i in "${!flat[@]}"; do
  cur="${flat[$i]}"
  nxt="${flat[$(( (i + 1) % n ))]}"

  args+=( -delay "$HOLD" "$cur" )

  # outgoing half-turn: full width -> edge on
  for ((s = 1; s <= HALF; s++)); do
    w=$(half_width "$s" "$HALF")
    fr="$WORK/t-$i-out-$s.png"
    magick "$cur" -resize "${w}x${SIZE}!" \
      -background "$BG" -gravity center -extent "${SIZE}x${SIZE}" "$fr"
    args+=( -delay "$STEP" "$fr" )
  done

  # incoming half-turn: edge on -> full width (reverse the same curve)
  for ((s = HALF - 1; s >= 0; s--)); do
    w=$(half_width "$s" "$HALF")
    fr="$WORK/t-$i-in-$s.png"
    magick "$nxt" -resize "${w}x${SIZE}!" \
      -background "$BG" -gravity center -extent "${SIZE}x${SIZE}" "$fr"
    args+=( -delay "$STEP" "$fr" )
  done
done

mkdir -p "$OUT"
magick -loop 0 "${args[@]}" \
  -dither "$DITHER" -colors "$COLORS" -layers Optimize "$GIF"

# ---------------------------------------------------------------------------
# verify: it must animate, be the right size, loop forever, and open on the badge
# ---------------------------------------------------------------------------
echo
echo "=== $GIF ==="
count=$(magick identify -format '%n\n' "$GIF" | head -1)
read -r cw ch <<<"$(magick identify -format '%W %H' "$GIF[0]")"
bytes=$(wc -c < "$GIF" | tr -d ' ')
loop=$(magick identify -verbose "$GIF[0]" | awk -F': *' '/Iterations/{print $2; exit}')
cycle=$(python3 -c "print(round(7*($HOLD + 2*$HALF*$STEP)/100, 1))")
echo "  frames:     $count"
echo "  canvas:     ${cw}x${ch} (display 75x75 = 2x)"
echo "  file:       $(( bytes / 1024 )) KiB (ceiling $(( MAXBYTES / 1024 )) KiB)"
echo "  iterations: ${loop:-unset} (0 = loop forever)"
echo "  cycle:      ${cycle}s for all 7 marks"

# Frame 0 must be the tps-badge: that is what any client which declines to
# animate will display, and it has to match what v1/v2 ship statically.
#
# -coalesce is required — -layers Optimize crops later frames to their changed
# region, so reading a raw frame gives a partial tile, not the composed image.
#
# The test is discriminative, not exact. Frame 0 is quantised to $COLORS colours
# while the source PNG is full colour, so an exact pixel match is unachievable
# and an AE==0 assertion just fails on dither noise. What actually matters is
# that frame 0 is the BADGE rather than one of the six brand marks, so: score
# frame 0 against all seven marks and assert the badge wins.
magick "$GIF" -coalesce "$WORK/co-%03d.png"
best=-1; bestscore=""
for i in "${!flat[@]}"; do
  # `compare` exits non-zero whenever the images differ, which is always here;
  # without `|| true` set -e aborts the script mid-loop.
  d=$( { magick compare -metric RMSE "$WORK/co-000.png" "${flat[$i]}" null: 2>&1 || true; } | sed 's/.*(\(.*\))/\1/')
  echo "    frame0 vs $(basename "${order[$i]}"): RMSE $d"
  if [[ -z "$bestscore" ]] || python3 -c "import sys; sys.exit(0 if float('$d') < float('$bestscore') else 1)"; then
    bestscore="$d"; best="$i"
  fi
done

fail=0
[[ "$count" -gt 1 ]]                     || { echo "  FAIL: not animated"; fail=1; }
[[ "$cw" == "$SIZE" && "$ch" == "$SIZE" ]] || { echo "  FAIL: canvas is ${cw}x${ch}"; fail=1; }
[[ "$bytes" -lt "$MAXBYTES" ]]           || { echo "  FAIL: $(( bytes / 1024 )) KiB exceeds ceiling"; fail=1; }
[[ "${loop:-x}" == "0" ]]                || { echo "  FAIL: does not loop forever"; fail=1; }
if [[ "$best" == "0" ]]; then
  echo "  frame 0:    closest match is tps-badge (RMSE $bestscore) — correct static fallback"
else
  echo "  FAIL: frame 0 resembles $(basename "${order[$best]}") more than tps-badge"; fail=1
fi
echo
[[ $fail -eq 0 ]] && echo "GIF OK." || { echo "GIF FAILED CHECKS"; exit 1; }
