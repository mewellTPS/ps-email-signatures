#!/usr/bin/env bash
# Build normalized brand icons for the Purple Standard signature v2/v3 brand strip.
#
# Re-runnable from durable sources only: reads multi-brand/*.png (the raw brand
# assets Michael supplied) and ../assets/tps-badge.png. Writes nothing outside
# multi-brand/out/.
#
# Output spec (ADR 0008): 2x source dimensions at explicit 96 DPI, PNG only.
#   strip icons  -> 80x80  (40px display)
#   ball frames  -> 150x150 (75px display, the tps-badge slot)
#
# Four treatments are produced so they can be compared in a browser:
#   a-plain  bare circles; naturally-round marks full-bleed, container marks on white
#   b-ring   every icon = white field + brand-colored ring + inset mark (max consistency)
#   c-native no shape forcing; each mark trimmed and scaled to fit an 80x80 box
#   d-hybrid RECOMMENDED. Naturally-round marks stay full-bleed and bare (biggest,
#            punchiest); only the two marks that need a field (WTR DR's drop, Tyrian's
#            shield) get a white field + thin brand ring. Every cell still reads as a
#            40px circle, but nothing is shrunk by a redundant second ring.
#
# Usage: bash build-icons.sh
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE"
BADGE="$HERE/../assets/tps-badge.png"
OUT="$HERE/out"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

FONT="/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# Internal working resolution; everything downsamples to final size for clean AA.
W=320

# --- brand colors (see PROFILE / prior ADRs) --------------------------------
C_ACE="#335E89"     # Sailfish
C_PC="#411144"
C_BOY="#F93822"
C_WTR="#2E6DA6"     # link-blue, settled 2026-07-22
C_BRISA="#48104F"
C_TYR="#531757"
C_PS="#49104F"
C_PENDING="#C9C9C9" # MOR / ENG, no branding yet

mkdir -p "$OUT/a-plain" "$OUT/b-ring" "$OUT/c-native" "$OUT/d-hybrid" "$OUT/ball" "$OUT/ball-c"

# --- measured crops (derived, not guessed; see session notes) ---------------
# wtrdr-logo.png 200x200: drop occupies x49..147, y2..148; "WTR DR" wordmark
#   begins at y=148 and is illegible at 40px.
WTR_DROP_CROP="98x146+49+2"

# Brisa: superseded 2026-08-06. The original brisa-icon.png was a 1080x1080
# circular badge whose ring read "FINE-TUNED FLORIDA COMFORT" — illegible at
# 40px, so it had to be cropped to its inner disc (650x650+215+215). Michael
# supplied the real bear mark instead: brisa-logo.png, 3366x3745, a gradient
# outline on transparent with the negative space genuinely transparent (mean
# alpha 0.47), so it needs no cropping at all — just trim and scale. The old
# badge is kept in the folder for reference but is no longer built.
BRISA="$SRC/brisa-logo.png"

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

# circle_mask <size> <outfile>
circle_mask() {
  local s=$1 out=$2 r=$(( $1 / 2 ))
  magick -size "${s}x${s}" xc:black -fill white \
    -draw "circle $r,$r $r,0" -alpha off "$out"
}

# fin <infile> <size> <outfile>  -- downsample and stamp 96 DPI
fin() {
  magick "$1" -resize "$2x$2" -units PixelsPerInch -density 96 \
    -define png:include-chunk=none,gAMA,pHYs,tRNS "$3"
}

# full_bleed_circle <src> <outsize> <out>
# For marks that are already edge-to-edge circles: scale up to W, mask, downsample.
full_bleed_circle() {
  local src=$1 size=$2 out=$3
  circle_mask "$W" "$WORK/m.png"
  magick "$src" -resize "${W}x${W}!" "$WORK/s.png"
  magick "$WORK/s.png" "$WORK/m.png" -alpha off -compose CopyOpacity -composite "$WORK/c.png"
  fin "$WORK/c.png" "$size" "$out"
}

# white_disc_mark <mark> <ring-color> <ring-width-px-at-W> <mark-frac> <outsize> <out>
# White field, optional brand ring, mark centered and scaled to <mark-frac> of the disc.
white_disc_mark() {
  local mark=$1 ring=$2 rw=$3 frac=$4 size=$5 out=$6
  local r=$(( W / 2 ))
  local inner=$(python3 -c "print(int($W*$frac))")
  # disc: white fill, brand stroke inset by half the stroke width
  local inset=$(python3 -c "print(int($rw/2))")
  magick -size "${W}x${W}" xc:none \
    -fill white -stroke "$ring" -strokewidth "$rw" \
    -draw "circle $r,$r $r,$inset" "$WORK/disc.png"
  magick "$mark" -resize "${inner}x${inner}" "$WORK/mk.png"
  magick "$WORK/disc.png" "$WORK/mk.png" -gravity center -compose over -composite "$WORK/c.png"
  # re-mask so the stroke's outer AA doesn't bleed a square edge
  circle_mask "$W" "$WORK/m.png"
  magick "$WORK/c.png" \( "$WORK/m.png" -alpha off \) -compose CopyOpacity -composite "$WORK/c2.png"
  fin "$WORK/c2.png" "$size" "$out"
}

# color_disc_text <disc-color> <text> <text-color> <outsize> <out>
color_disc_text() {
  local disc=$1 txt=$2 tc=$3 size=$4 out=$5
  local r=$(( W / 2 ))
  magick -size "${W}x${W}" xc:none -fill "$disc" -draw "circle $r,$r $r,0" \
    -font "$FONT" -pointsize 92 -fill "$tc" -gravity center \
    -annotate +0+0 "$txt" "$WORK/c.png"
  fin "$WORK/c.png" "$size" "$out"
}

# circle_crop <src> <out>  -- mask a source to a circle inscribed in its own canvas.
# Needed before insetting a square crop of a round mark, or the crop's corners
# (and any ring text they clip) show inside the container.
circle_crop() {
  local src=$1 out=$2
  local s; s=$(magick identify -format '%w' "$src")
  circle_mask "$s" "$WORK/cc-m.png"
  magick "$src" \( "$WORK/cc-m.png" -alpha off \) -compose CopyOpacity -composite "$out"
}

# fit_box <src> <outsize> <out>  -- trim, scale to fit, center on transparent square
fit_box() {
  local src=$1 size=$2 out=$3
  magick "$src" -trim +repage -resize "${W}x${W}" \
    -background none -gravity center -extent "${W}x${W}" "$WORK/c.png"
  fin "$WORK/c.png" "$size" "$out"
}

# ---------------------------------------------------------------------------
# prepared marks
# ---------------------------------------------------------------------------
magick "$BRISA" -trim +repage "$WORK/brisa-bear.png"
magick "$SRC/wtrdr-logo.png" -crop "$WTR_DROP_CROP" +repage -trim +repage "$WORK/wtr-drop.png"
magick "$SRC/tyrian-logo.png" -trim +repage "$WORK/tyr-shield.png"
# Boyette is natively a blue ring with a transparent interior; give it a white field.
circle_mask "$W" "$WORK/m.png"
magick "$SRC/boyette-icon.png" -resize "${W}x${W}!" -background white -alpha remove -alpha off "$WORK/boy-flat.png"
magick "$WORK/boy-flat.png" "$WORK/m.png" -compose CopyOpacity -composite "$WORK/boy-disc.png"
# tps-badge: purple ring mark on transparent; flatten to white for the ball frames.
magick "$BADGE" -resize "${W}x${W}!" -background white -alpha remove -alpha off "$WORK/ps-flat.png"
magick "$WORK/ps-flat.png" "$WORK/m.png" -compose CopyOpacity -composite "$WORK/ps-disc.png"

# ---------------------------------------------------------------------------
# TREATMENT A — plain discs
# ---------------------------------------------------------------------------
full_bleed_circle "$SRC/ace-logo.png"   80 "$OUT/a-plain/brand-ace.png"
full_bleed_circle "$SRC/pc-icon.png"    80 "$OUT/a-plain/brand-purple-current.png"
full_bleed_circle "$WORK/boy-disc.png"  80 "$OUT/a-plain/brand-boyette.png"
white_disc_mark "$WORK/brisa-bear.png" "$C_BRISA" 0  0.68 80 "$OUT/a-plain/brand-brisa.png"
white_disc_mark "$WORK/wtr-drop.png"  "$C_WTR" 0  0.60 80 "$OUT/a-plain/brand-wtr-dr.png"
white_disc_mark "$WORK/tyr-shield.png" "$C_TYR" 0 0.66 80 "$OUT/a-plain/brand-tyrian.png"
color_disc_text "$C_PENDING" "MOR" white 80 "$OUT/a-plain/brand-mor.png"
color_disc_text "$C_PENDING" "ENG" white 80 "$OUT/a-plain/brand-eng.png"

# ---------------------------------------------------------------------------
# TREATMENT B — unified ring discs (every icon gets a brand ring on white)
# ---------------------------------------------------------------------------
RW=14
white_disc_mark "$SRC/ace-logo.png"      "$C_ACE"   $RW 0.66 80 "$OUT/b-ring/brand-ace.png"
white_disc_mark "$SRC/pc-icon.png"       "$C_PC"    $RW 0.66 80 "$OUT/b-ring/brand-purple-current.png"
white_disc_mark "$SRC/boyette-icon.png"  "$C_BOY"   $RW 0.70 80 "$OUT/b-ring/brand-boyette.png"
white_disc_mark "$WORK/brisa-bear.png"   "$C_BRISA" $RW 0.62 80 "$OUT/b-ring/brand-brisa.png"
white_disc_mark "$WORK/wtr-drop.png"     "$C_WTR"   $RW 0.56 80 "$OUT/b-ring/brand-wtr-dr.png"
white_disc_mark "$WORK/tyr-shield.png"   "$C_TYR"   $RW 0.60 80 "$OUT/b-ring/brand-tyrian.png"
white_disc_mark "$WORK/m.png"            "$C_PENDING" $RW 0.01 80 "$WORK/pending-blank.png"
# These two write their final PNG directly rather than through fin(), so they need
# the same include-chunk allowlist. Without it ImageMagick stamps a tIME chunk (a
# wall-clock timestamp), which makes the build non-reproducible: identical pixels,
# different bytes on every run, so git reports drift that isn't there.
magick "$WORK/pending-blank.png" -font "$FONT" -pointsize 23 -fill "#8A8A8A" \
  -gravity center -annotate +0+0 "MOR" -units PixelsPerInch -density 96 \
  -define png:include-chunk=none,gAMA,pHYs,tRNS "$OUT/b-ring/brand-mor.png"
magick "$WORK/pending-blank.png" -font "$FONT" -pointsize 23 -fill "#8A8A8A" \
  -gravity center -annotate +0+0 "ENG" -units PixelsPerInch -density 96 \
  -define png:include-chunk=none,gAMA,pHYs,tRNS "$OUT/b-ring/brand-eng.png"

# ---------------------------------------------------------------------------
# TREATMENT C — native shapes, normalized size only
# ---------------------------------------------------------------------------
fit_box "$SRC/ace-logo.png"    80 "$OUT/c-native/brand-ace.png"
fit_box "$SRC/pc-icon.png"     80 "$OUT/c-native/brand-purple-current.png"
fit_box "$SRC/boyette-icon.png" 80 "$OUT/c-native/brand-boyette.png"
fit_box "$WORK/brisa-bear.png" 80 "$OUT/c-native/brand-brisa.png"
fit_box "$SRC/wtrdr-logo.png"  80 "$OUT/c-native/brand-wtr-dr.png"
fit_box "$SRC/tyrian-logo.png" 80 "$OUT/c-native/brand-tyrian.png"
color_disc_text "$C_PENDING" "MOR" white 80 "$OUT/c-native/brand-mor.png"
color_disc_text "$C_PENDING" "ENG" white 80 "$OUT/c-native/brand-eng.png"

# ---------------------------------------------------------------------------
# TREATMENT D — hybrid (RECOMMENDED)
#
# Full-bleed and bare where the mark is already a circle, so it uses the whole
# 40px. White field + thin brand ring only for the two marks that have no field
# of their own — otherwise they read as loose glyphs floating next to solid
# discs. MOR/ENG sit lighter than in A so they read as pending, not as content.
# ---------------------------------------------------------------------------
RW_D=10
full_bleed_circle "$SRC/ace-logo.png"     80 "$OUT/d-hybrid/brand-ace.png"
full_bleed_circle "$SRC/pc-icon.png"      80 "$OUT/d-hybrid/brand-purple-current.png"
full_bleed_circle "$WORK/boy-disc.png"    80 "$OUT/d-hybrid/brand-boyette.png"
white_disc_mark "$WORK/brisa-bear.png" "$C_BRISA" $RW_D 0.62 80 "$OUT/d-hybrid/brand-brisa.png"
white_disc_mark "$WORK/wtr-drop.png"   "$C_WTR" $RW_D 0.72 80 "$OUT/d-hybrid/brand-wtr-dr.png"
white_disc_mark "$WORK/tyr-shield.png" "$C_TYR" $RW_D 0.66 80 "$OUT/d-hybrid/brand-tyrian.png"
color_disc_text "#DCDCDC" "MOR" "#8A8A8A" 80 "$OUT/d-hybrid/brand-mor.png"
color_disc_text "#DCDCDC" "ENG" "#8A8A8A" 80 "$OUT/d-hybrid/brand-eng.png"

# ---------------------------------------------------------------------------
# BALL FRAMES — 150x150 plain discs for the v3 rotating-ball GIF
# ---------------------------------------------------------------------------
full_bleed_circle "$WORK/ps-disc.png"     150 "$OUT/ball/ball-0-ps.png"
full_bleed_circle "$SRC/ace-logo.png"     150 "$OUT/ball/ball-1-ace.png"
full_bleed_circle "$SRC/pc-icon.png"      150 "$OUT/ball/ball-2-purple-current.png"
full_bleed_circle "$WORK/boy-disc.png"    150 "$OUT/ball/ball-3-boyette.png"
white_disc_mark "$WORK/wtr-drop.png"  "$C_WTR" 10 0.72 150 "$OUT/ball/ball-4-wtr-dr.png"
white_disc_mark "$WORK/brisa-bear.png" "$C_BRISA" 10 0.68 150 "$OUT/ball/ball-5-brisa.png"
white_disc_mark "$WORK/tyr-shield.png" "$C_TYR" 10 0.66 150 "$OUT/ball/ball-6-tyrian.png"

# ---------------------------------------------------------------------------
# BALL-C FRAMES — 150x150, treatment C (native shapes), for the v3 GIF.
# This is the set the v3 animation uses: Michael selected treatment C, so the
# ball cycles the same marks the strip shows, plus tps-badge as frame 0 (it is
# also the static first frame any client that won't animate will display).
# ---------------------------------------------------------------------------
fit_box "$BADGE"               150 "$OUT/ball-c/ball-0-ps.png"
fit_box "$SRC/ace-logo.png"    150 "$OUT/ball-c/ball-1-ace.png"
fit_box "$SRC/pc-icon.png"     150 "$OUT/ball-c/ball-2-purple-current.png"
fit_box "$SRC/boyette-icon.png" 150 "$OUT/ball-c/ball-3-boyette.png"
fit_box "$SRC/wtrdr-logo.png"  150 "$OUT/ball-c/ball-4-wtr-dr.png"
fit_box "$WORK/brisa-bear.png" 150 "$OUT/ball-c/ball-5-brisa.png"
fit_box "$SRC/tyrian-logo.png" 150 "$OUT/ball-c/ball-6-tyrian.png"

# ---------------------------------------------------------------------------
# verify: size, then pHYs (96 DPI) by parsing the chunk
#
# `magick identify %x` is NOT a usable DPI oracle here: PNG stores only
# pixels-per-metre, so a correct 96 DPI file reports back as
# "37.79 PixelsPerCentimeter". verify-phys.py reads the pHYs bytes instead.
# ---------------------------------------------------------------------------
echo
echo "=== size check ==="
fail=0
while IFS= read -r f; do
  read -r w h <<<"$(magick identify -format '%w %h' "$f")"
  case "$f" in
    */ball/*|*/ball-c/*) want=150 ;;
    *)                   want=80  ;;
  esac
  if [[ "$w" == "$want" && "$h" == "$want" ]]; then
    printf '  OK       %sx%s  %s\n' "$w" "$h" "${f#$OUT/}"
  else
    printf '  BAD-SIZE %sx%s (want %sx%s)  %s\n' "$w" "$h" "$want" "$want" "${f#$OUT/}"
    fail=1
  fi
done < <(find "$OUT" -name '*.png' | sort)
[[ $fail -eq 0 ]] || { echo "SIZE FAILURES ABOVE"; exit 1; }

echo
echo "=== pHYs / 96 DPI check (ADR 0008) ==="
python3 "$HERE/verify-phys.py" "$OUT"
