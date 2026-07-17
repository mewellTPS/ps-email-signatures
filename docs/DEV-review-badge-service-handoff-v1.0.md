# Google Review Badge Service — Build Handoff
**File:** DEV-review-badge-service-handoff-v1.0.md
**Version:** 1.0
**Date:** 2026-07-17
**Maintained by:** Michael / The Purple Standard
**Target repo:** _new, dedicated_ — proposed `purple-standard/tps-review-badges` (confirm name at kickoff)
**Audience:** a fresh Claude Code session building this service from scratch
**Origin:** spun out of the email-signatures project (WTR DR signature work). This service is **shared, brand-agnostic org infra** — it does NOT live under `email-signatures/` or any single-brand folder.

---

## Goal

A small unattended service that produces an **auto-updating image badge showing a brand's live Google review aggregate** (star rating + total review count), for every TPS brand. Each brand's badge is a PNG served at a stable public URL. Email signatures (and anything else) embed it with a single `<img>` tag; it stays current on its own.

**Why an image, not live HTML:** an email signature is frozen HTML with no script execution at open time. The only thing that can change after send is the *content an `<img> src` returns*. So "live" review data must arrive as an image whose bytes get refreshed over time.

**Why this beats a static "5 gold stars" graphic:** a hardcoded 5-star image becomes a false claim the day the rating dips to 4.8. A data-driven badge never lies because it self-updates — that is the entire reason to build this.

---

## Chosen approach (decided during brainstorming)

**Approach B — pre-rendered, refreshed on a schedule.** A daily job fetches each brand's rating from Google, renders a PNG, and overwrites a fixed file on our own host. Signatures point at that static file.

Alternatives considered and rejected:
- **A. Live endpoint** (`<img>` hits a service that fetches Google + renders on every open) — rejected: the service must stay up on *every* email open forever, adds per-open API/compute, and needs a cache anyway. More moving parts for freshness nobody needs.
- **C. Third-party review-badge SaaS** — rejected: recurring cost, another vendor to trust, branding limits. We already own every piece needed to build B.

**Why B fits:** static file serving never fails mid-send; zero API calls per email open; costs almost nothing; review counts move slowly so daily freshness is more than enough. Every dependency is already in the tool registry (see Stack).

---

## Architecture / data flow

```
  ┌─────────────┐   daily    ┌──────────────────────┐   PNG    ┌──────────────────┐
  │  Scheduler  │──────────▶ │  render job          │────────▶ │ Cloudflare R2    │
  │ (Railway or │            │  1. Google Places    │  upload  │ (public bucket,  │
  │  n8n cron)  │            │     Place Details    │  (over-  │  custom domain)  │
  └─────────────┘            │  2. build badge SVG  │  write)  └────────┬─────────┘
                             │  3. rasterize → PNG  │                   │ stable URL
                             │  4. upload to R2     │                   ▼
                             │  (keep last-good on  │        https://purple-standard.app/
                             │   failure)           │          badges/<brand>-reviews.png
                             └──────────────────────┘                   │
                                                                        ▼
                                             ┌──────────────────────────────────────┐
                                             │ consumer: signature <img src=…>        │
                                             │ wrapped in the brand's g.page review   │
                                             │ link. CodeTwo templates AND the future │
                                             │ signature-generator web app both just  │
                                             │ reference the URL.                     │
                                             └──────────────────────────────────────┘
```

Per-brand loop: the job iterates a config list (below), one badge per brand, one output file per brand.

---

## Stack (all already in the Tool & Connector Registry — reuse, don't add new)

- **Google Places API** (`google-places`, active) — source of `rating` + total review count. Already used by `dev/seo-audit`; reuse that GCP project / key. **Confirm which Places variant seo-audit uses** (Places API "New" returns `rating` + `userRatingCount`; legacy returns `rating` + `user_ratings_total`) and match it.
- **Google Business Profiles API** (`google-business-profiles`, active) — alternative/authoritative source for *owned* locations; consider if Places rating lags or for locations we manage. Places is simpler for v1.
- **Cloudflare R2** (`cloudflare-r2`, active, currently `used_by: 0`) — public object storage for the PNGs. Owner: Michael.
- **purple-standard.app** — Michael-controlled domain on Cloudflare (NOT the Ntiva-owned purple-standard.com). Use an R2 custom domain / bucket binding under it, e.g. `badges.purple-standard.app` or `purple-standard.app/badges/`.
- **Railway** (`railway`, active) OR **n8n** (`n8n`, active, self-hosted) — either runs the daily cron. Railway matches the pattern already used by content-dashboard / sales-dashboard / shot-list.
- Language/render: builder's choice. A Cloudflare Worker + `@resvg/resvg-wasm` (SVG→PNG) is a clean fit and keeps everything on Cloudflare; a small Node job on Railway is equally fine. **Do NOT ship WebP** — Outlook won't render it. PNG only.

Registry action at build time: add a new project row for this service and set `used_by` on `google-places`, `cloudflare-r2`, and the chosen scheduler at `/close`.

---

## Brand config (the brand-agnostic core)

Drive everything from one config so adding a brand is a data edit, not code:

```jsonc
// brands.jsonc  (or a table — keep it versioned, no secrets)
[
  {
    "code": "WTRDR",
    "name": "WTR DR",
    "placeId": "TBD — resolve (see below)",
    "reviewUrl": "https://g.page/r/CXbaZrIdtlq-EBM/review",
    "output": "badges/wtrdr-reviews.png",
    "active": true
  }
  // ACE, Boyette, Purple Current, Purple Standard, … one row each
]
```

**Resolving `placeId`:** WTR DR's existing review link is `https://g.page/r/CXbaZrIdtlq-EBM/review` (the `CXbaZrIdtlq-EBM` token is a CID reference). Convert each brand to a canonical **Place ID** at setup (Google's Place ID Finder, or a Places Text Search on business name + city). Store the Place ID in config; don't resolve at runtime.

---

## Badge image spec

- **Format:** PNG. Render at **2× resolution**, set the `<img>` `width`/`height` to the 1× size so it stays crisp on retina and in Outlook.
- **Suggested 1× size:** ~180×48 px (tune to the signature). Fixed dimensions — Outlook needs them on the tag.
- **Content, one compact row:**
  ```
  ★★★★★   4.9   ·   213 Google reviews
  ```
  - Stars filled to the actual `rating` (partial fill on the fractional star, or round to nearest half — confirm which).
  - Numeric rating + total count. Word "Google" present for attribution.
- **Colors (WTR DR palette; parameterize per brand):** stars Google-gold `#FBBC04` or brand navy `#1C2458` (confirm); text navy `#1C2458`. Match the signature's type (Arial).
- **Empty/edge states:** if a brand has 0 reviews or the count is unavailable, render a neutral fallback (e.g. hide the badge / show logo-only) rather than "0.0 ★".

---

## Signature integration (both consumers)

The badge is just a URL. Two consumption paths, both trivial:

1. **CodeTwo dynamic templates (current):** in the signature HTML, replace/append a social-row cell with:
   ```html
   <a href="https://g.page/r/CXbaZrIdtlq-EBM/review" target="_blank">
     <img src="https://purple-standard.app/badges/wtrdr-reviews.png"
          alt="WTR DR — Google reviews" width="180" height="48"
          style="width:180px;height:48px;border:0">
   </a>
   ```
2. **Future signature-generator web app** (see `DEV-email-signatures-handoff-v1.0.md`): expose the badge as a toggleable *block* (that handoff already has a `blocks` concept with a static `review-banner`). The dynamic badge slots in as a block whose `image` is the hosted URL.

---

## Caveats to honor (call these out in the build; they're real)

1. **Gmail proxies & caches images** via googleusercontent. The same URL refreshes periodically, not instantly — a recipient may see "213" when it's actually "215." Harmless at daily cadence. Set sensible `Cache-Control` on R2 (e.g. a few hours) but don't expect per-open freshness.
2. **Google attribution/branding:** show real numbers, say "Google," link to the real review page. Don't fabricate or round misleadingly. Review Google's brand guidelines for displaying ratings.
3. **Fail safe, not broken:** if the Google call fails or returns garbage, **keep the last-good PNG** — never overwrite with an error image. A stale-by-a-day badge beats a broken image in everyone's signature.
4. **Rate/quota:** daily per-brand calls are trivial, but cache and batch anyway; don't call Google per email open (that's the whole point of Approach B).
5. **Uptime:** because it's a static file, the only failure surface is R2 itself. Acceptable. No app server in the hot path.

---

## Open decisions to confirm at kickoff

- Final repo name (`tps-review-badges`?) and scheduler (Railway vs n8n).
- Star color: Google-gold vs brand navy; partial-fill vs half-star rounding.
- R2 URL scheme: `badges.purple-standard.app/<brand>.png` vs `purple-standard.app/badges/<brand>-reviews.png`.
- Full brand list + each brand's Place ID and review URL (WTR DR seeded above).
- Whether to also pull from Google Business Profiles for locations we own.

---

## Acceptance criteria for v1.0.0

- Config-driven: adding a brand is a data edit (Place ID + output path), no code change.
- Daily job fetches live rating + count from Google for each active brand and writes a PNG to R2.
- PNGs are reachable at stable public `purple-standard.app` URLs and render in Gmail, Outlook desktop/web, and Apple Mail.
- Failure path verified: a forced API failure leaves the previous PNG intact.
- WTR DR badge live and embedded in the WTR DR signature (finish the WTR DR signature separately — see that project).
- Registry updated (new project row; `used_by` set on google-places, cloudflare-r2, scheduler).

## Out of scope for v1.0.0

- Real-time / per-open freshness (daily is the design).
- Review *text* / carousels — aggregate rating + count only.
- Non-Google sources (Yelp, Facebook ratings).
- Any per-recipient personalization (would turn the badge into a tracking pixel).

---

## Security / credential notes (pointers only — never commit secrets)

- Reuse the existing Google API key from `dev/seo-audit`'s GCP project; store as an env var / Railway secret, never in the repo.
- R2 credentials: Cloudflare API token scoped to the one bucket; env/secret only.
- Public bucket serves images only; no write path exposed publicly.
