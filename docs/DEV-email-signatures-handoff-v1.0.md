# Email Signature Generator — Build Handoff
**File:** DEV-email-signatures-handoff-v1.0.md
**Version:** 1.0
**Date:** 2026-05-11
**Maintained by:** Michael / The Purple Standard
**Target repo:** purple-standard/tps-email-signatures
**Audience:** Claude Code sessions building this app

## Goal

A static web app, hosted on GitHub Pages at the tps-email-signatures repo,
that lets any TPS employee select their brand, fill in personal fields, toggle
optional content blocks (banners, badges, promos), preview the resulting
signature live, and export it as either copy-to-clipboard HTML or a downloadable
.htm file for Outlook desktop.

Templates are authored once per brand by Michael; end users only fill the form.

## Stack (matches DEV-knowledge-ops conventions)

- React 18 + TypeScript + Vite + Tailwind CSS
- Static build, deployed to GitHub Pages on push to main
- No backend, no auth, no database — all template data lives in the repo
- Public repo (confirmed: nothing sensitive)

## Repo structure

/
├── .claude/
│   └── settings.json          # baseline v1.1 ruleset from foundations doc §5
├── .github/
│   └── workflows/
│       └── deploy.yml         # build + deploy to Pages on push to main
├── public/
├── src/
│   ├── components/            # FormPanel, PreviewPanel, ExportPanel, etc.
│   ├── lib/
│   │   ├── render.ts          # placeholder substitution + block stripping
│   │   ├── export.ts          # clipboard + .htm download logic
│   │   └── manifest.ts        # loads build-generated brand list
│   ├── types.ts               # BrandConfig, Field, Block, etc.
│   ├── App.tsx
│   └── main.tsx
├── templates/
│   ├── boyette/
│   │   ├── template.html      # Outlook-safe table layout with {{placeholders}}
│   │   ├── config.json        # fields + assets + blocks
│   │   └── assets/
│   │       ├── logo.png
│   │       ├── block-review-banner.png
│   │       ├── social-facebook.png
│   │       ├── social-linkedin.png
│   │       └── social-instagram.png
│   └── ace/                   # added in session 6
├── scripts/
│   └── generate-manifest.ts   # walks /templates/, emits manifest.json
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
├── .gitignore
└── README.md

## Template format

### config.json shape

{
  "brand": { "code": "BOY", "name": "Boyette Pump & Well", "active": true },
  "fields": [
    { "key": "firstName", "label": "First name", "required": true },
    { "key": "lastName",  "label": "Last name",  "required": true },
    { "key": "title",     "label": "Title",      "required": true },
    { "key": "phoneOffice", "label": "Office phone", "required": false, "type": "tel" },
    { "key": "phoneMobile", "label": "Mobile phone", "required": false, "type": "tel" },
    { "key": "email",     "label": "Email",      "required": true,  "type": "email" },
    { "key": "address",   "label": "Address",    "required": false, "default": "..." }
  ],
  "assets": {
    "logo": "assets/logo.png",
    "social": [
      { "platform": "facebook",  "icon": "assets/social-facebook.png",  "url": "https://..." },
      { "platform": "linkedin",  "icon": "assets/social-linkedin.png",  "url": "https://..." },
      { "platform": "instagram", "icon": "assets/social-instagram.png", "url": "https://..." }
    ]
  },
  "blocks": [
    {
      "id": "review-banner",
      "label": "Help Spread the Word — review banner",
      "image": "assets/block-review-banner.png",
      "link": "https://...",
      "defaultOn": true
    }
  ]
}

### template.html rules

- Tables only. No flexbox, no grid, no <style> blocks.
- All styles inline on individual elements.
- Web-safe fonts only (Arial, Calibri, Georgia, Verdana).
- Personal field placeholders: {{firstName}}, {{email}}, etc.
- Brand asset placeholders: {{assets.logo}}, {{assets.social.facebook}}.
- Block sections wrapped in {{#block:block-id}} ... {{/block:block-id}}.
  Renderer strips the entire wrapped region if the block is toggled off.
- Asset paths resolve at render time to absolute URLs pointing at the
  hosted location on GitHub Pages (so signatures work in recipient inboxes).

## Render pipeline

1. User selects brand → app fetches /templates/<code>/config.json + template.html
2. Form renders dynamically from config.fields, with block toggles from config.blocks
3. As user types, render.ts substitutes placeholders and strips inactive block regions
4. Live preview shows result inside a sandboxed iframe (iframe srcdoc=...) to prevent CSS leakage from the app into the preview
5. On export: same render output goes to either clipboard (text/html MIME) or download (.htm file)

## Export specifics

- Copy-to-clipboard: navigator.clipboard.write with ClipboardItem containing
  text/html and text/plain blobs. text/plain is a fallback for clients that
  don't accept HTML.
- Download: Blob with type "text/html", filename "<brand>-<firstName>-<lastName>.htm".
  Use .htm (not .html) because Outlook's Signatures folder expects .htm.

## Build manifest

scripts/generate-manifest.ts runs as a Vite plugin / prebuild step. It walks
/templates/, reads each config.json, and emits public/manifest.json containing
the array of { code, name, active } entries. App fetches manifest.json at
startup to populate the brand picker. Hand-maintained index file is avoided.

## Acceptance criteria for v1.0.0

- Boyette template renders correctly in Outlook desktop (Windows) and Outlook web
- ACE template renders correctly in both
- Form correctly enforces required fields before allowing export
- Live preview matches exported output byte-for-byte
- Copy-to-clipboard paste into Outlook produces formatted signature, not raw HTML
- Downloaded .htm file dropped into %AppData%\Microsoft\Signatures\ appears in Outlook
- Site deployed to GitHub Pages at https://purple-standard.github.io/tps-email-signatures/
  (or whatever Pages URL the org assigns)

## Out of scope for v1.0.0

- Editing templates in-browser (templates are author-once, edit-via-PR)
- User accounts, saved signatures, history
- Analytics on usage
- Per-user defaults stored anywhere (form starts blank each visit)

