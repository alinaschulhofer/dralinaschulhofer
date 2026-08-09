# Dr. Alina Schulhofer — Therapy Website: Project Handoff / Source of Truth

Give this file **plus the website files** to a new Claude chat and say: *"Continue developing this website from its current state."* It is written to be self-contained.

> **Update:** this project now lives in its own git repo — `github.com/alinaschulhofer/dralinaschulhofer` — kept deliberately separate from the `aoe` repo. File layout changed slightly from what §4 below describes: the deploy package (`index.html`, `about.html`, `services.html`, `faq.html`, `styles.css`, `assets/`) sits at the **repo root**, and the master source (`therapy_template.html`, `assets.b64`, `build_site.py`) moved into **`src/`**. `build_site.py` was updated to read/write those locations automatically — run it from the repo root (`python3 src/build_site.py`). The three pending text edits noted in §8 (hero sub-line, "Building a more meaningful life", "Legacy & purpose") are now regenerated into the deploy files. Preview artifact rebuild is still outstanding.

---

## 1. Purpose & strategic positioning

This is a **standalone psychotherapy practice website for Dr. Alina Schulhofer**, deliberately kept **separate** from her organizational brand, **Architecture of Excellence™ (AOE)**.

- **Therapy site (this project)** → domain **dralinaschulhofer.com**. Single-purpose: convert *therapy* clients. Warm, calm, clinical-but-premium. Target audience: **high performers** (executives, entrepreneurs, creatives, founders, professional athletes) who carry private struggles behind outward success.
- **AOE site (separate, already live)** → domain **architectureofexcellence.com**. Coaching / speaking / consulting for individuals, teams, organizations.
- The two are **bridged, not merged**: the therapy site points to AOE only via (a) a charcoal "founder band" on Home + Services and (b) a quiet footer link. **Do NOT build an "other services" page** on the therapy site — it splits focus and leaks warm therapy leads. If anything, AOE is the place to grow the organizational audience.

Key positioning line (hero): therapy site sells the *feeling/outcome*, not credentials. Credentials live in body copy, not the hero.

---

## 2. Site architecture & pages

Four pages: **Home, About, Clinical Services, FAQ.** Nav labels: `Home / About / Clinical Services / FAQ / Contact`.

**HOME** (top → bottom):
1. **Hero** — full-bleed, plain soft gradient bg, centered. Eyebrow `Virtual Therapy · Florida & New York`; H1 `Concierge Psychological Services`; gold italic sub `Depth-oriented therapy for high achievers.`; black **Get in Touch** button (scrolls to `#contact`); animated scroll cue.
2. `divider-full` gold line.
3. **Welcome** — circle arms-crossed photo LEFT + header `Trusted by Pro Athletes, Executives, and Elite Professionals` + `Welcome!` lead + 4 intro paragraphs.
4. `divider-full` gold line.
5. **My Philosophy** — sits in a soft **ivory gradient band** (fades in and out to white). Heading + 4 paragraphs.
6. `divider-full` gold line.
7. **Areas of Focus** — two-column list, small **gold dot** bullets (12 items, see §7).
8. **Animated gold down-chevron** (`.arrow-cue`) → cues scroll to booking.
9. **Contact band** — `Get Started` eyebrow / `Book a Free 15-Minute Consultation` / intro paragraph / **form** (name, email, phone, message — all required) → Formspree → thank-you message.
10. **Charcoal founder band** (full-width `#1B1A18` "chapter break") — AOE cross-link.
11. **Footer** — clickable email · phone · `Architecture of Excellence ↗` · copyright.

**ABOUT**: `.pg-head` (subtle gradient) with `About Me` eyebrow, H1 `Dr. Alina Schulhofer`, sub `Licensed Clinical Psychologist · Florida & New York`, **face-crop circle photo RIGHT**. → gold divider → 5-paragraph bio. (Credentials block was intentionally **removed** as redundant.)

**CLINICAL SERVICES**: `.pg-head` (`Virtual Therapy · FL + NY` / `Services & Investment` / italic sub). 6-paragraph intro → **accordion** with a **gold top border** separating it (5 collapsible items, closed by default): Individual Therapy, Couples & Family Therapy, Concierge Services, Intensive Sessions, Investment. → charcoal founder band.

**FAQ**: `.pg-head` (`Common Questions` / `Frequently Asked Questions`). 9 collapsible Q&As (closed by default), centered block, question text left-aligned & slightly smaller.

---

## 3. Design system / aesthetic

**Direction:** black / white / gold — premium, calm, clinical. Same *fonts* as AOE but a **distinct palette** (AOE is warm ivory/gold; this is crisper black/white/gold) so it reads as its own brand.

**Color tokens (CSS `:root`):**
```
--bg:#FCFBF8   near-white background
--bg2:#F1EFEA  soft ivory (bands/gradients)
--bg3:#E6E3DB
--ink:#15151A  near-black (text, buttons)
--ink2:#494842 body text
--ink3:#8A897F muted
--accent:#A9843F  gold (headings-accent, ornaments, dividers)
--accent2:#C9A96F
--line:rgba(21,21,26,.14)  hairlines
```
Darker gold **`#8C6A2E`** is used for **small gold text** (eyebrows, nav active/hover, links) for contrast/accessibility. Charcoal band bg = **`#1B1A18`**, its text `#CFC7B8`, its link `#D8B876`.

**Typography:** `Cormorant Garamond` (serif) for headings, wordmark, pull-quotes, hero title/sub; `Jost` (sans, weights 300/500) for body, eyebrows, buttons, labels. Eyebrows = Jost 500, uppercase, letter-spacing ~2–4px, gold.

**Layout conventions:** `.container` max-width 1080 (padding 0 40px); `.narrow` caps at 760. Sections use generous vertical padding. Section separation = **full-width edge-to-edge gold line** (`.divider-full`, a `100vw` breakout). Philosophy is **bookended** by two such lines.

**Buttons:** black (`--ink`) bg, white text, radius 2px, uppercase Jost 500; hover → gold bg + slight lift + soft shadow.

**Imagery:** studio portrait of Alina in a **black suit, arms crossed, grey background** (`portrait-about.jpg`) used as the Welcome circle; a **tight face crop** of the same shoot (`face.jpg`) for the About circle. `portrait-circle.jpg` is a spare headshot (not currently used). Circles get a soft ring + shadow.

**Motifs:** a small **diamond ornament** (rotated square) is the brand mark. Areas-of-Focus bullets are **small gold dots**.

**Animations (all gated by `body.anim`, all respect `prefers-reduced-motion`):**
- Hero: staggered fade-up entrance of eyebrow→title→sub→button.
- Scroll-reveal fade-ups (`.reveal` + IntersectionObserver) on major blocks.
- Image fade + scale-in (`.reveal-img`) on the two portraits.
- Nav link underline-wipe on hover; button lift on hover.
- Animated gold **down-chevron** (`.arrow-cue`) before the contact band.
- Smooth in-page scroll; page cross-fade in the SPA preview.

**Responsive:** mobile **hamburger** (`.nav-toggle` toggles `.nav.open`), `overflow-x:hidden` on body, hero scales down, multi-columns stack, credentials/areas stack. Main breakpoint `max-width:760px` (plus 700/600 helpers).

---

## 4. Technical architecture & files

There are **two build targets** from **one source**:

**A. MASTER SOURCE — `therapy_template.html`** (a single-file **SPA**):
- 4 "pages" are `<div class="page" id="home|about|services|faq">`; nav uses `data-go` + JS `go()` to switch; shared `<header class="top">`, `<footer>`, one big `<style>`, one `<script>`.
- Fonts & images are **base64 placeholders** injected at build time: `__COR400__ __CORIT__ __JOST3__ __JOST5__` (fonts) and `__PABOUT__ __PCIRCLE__ __FACE__` (images), sourced from **`assets.b64`** (key=base64 lines).
- **Edit all content and design in this file**, then regenerate the two outputs below.

**B. PREVIEW ARTIFACT — `therapy-artifact.html`** (self-contained, published as a claude.ai Artifact):
- Live private preview URL: **https://claude.ai/code/artifact/7505f978-f1e7-4f8d-be17-74391ef21046** (republish the **same file path** to keep this URL).
- Built by: inject `assets.b64` values into `therapy_template.html` placeholders → take the `<style>…</style>` block + everything inside `<body>…</body>` → `.encode('ascii','xmlcharrefreplace')` (so `·`, `—`, `™` render regardless of charset) → write file → publish with the Artifact tool. Favicon 🕊️.
- Note: inside the artifact sandbox, external `fetch`/form POST is **blocked by CSP**, so the form **falls back to mailto** in preview only. On a real domain it POSTs to Formspree normally.

**C. DEPLOY PACKAGE — `therapy-site/`** (real multi-page site, SEO-ready):
- Files: `index.html, about.html, services.html, faq.html, styles.css, assets/{portrait-about.jpg, portrait-circle.jpg, face.jpg}`.
- Built by **`build_site.py`**, which: extracts the `<style>` (drops the 4 base64 `@font-face` rules and instead links **Google Fonts**), splits the 4 page contents, swaps `data:image/jpeg;base64,__PABOUT__/__PCIRCLE__/__FACE__` → `assets/*.jpg`, builds a **real nav with `href`s** + active states, adds **per-page `<title>`/meta description/canonical/OG** + **Schema.org JSON-LD** (`Psychologist`/`MedicalBusiness`) on Home, and a production `<script>` (mobile menu, Formspree handler, reveal animations — no SPA switching).
- This is the folder you actually deploy.

**Fonts (deploy):** Google Fonts — `Cormorant Garamond` (ital 400/500) + `Jost` (300/500) via `<link>`.

**Form backend:** **Formspree** endpoint `https://formspree.io/f/xzdwqnvk` (currently **shared with the AOE newsletter** — recommend creating a dedicated therapy form and swapping the endpoint so inquiries stay separate). Form posts JSON `{name,email,phone,message,_subject}`; on success hides form + shows a thank-you; on failure falls back to `mailto:alina@dralinaschulhofer.com`. Formspree may send a one-time confirm email on first submission from a new domain.

---

## 5. Contact facts & approved copy

- Email: **alina@dralinaschulhofer.com** · Phone: **+1 786-671-4945**
- Licensed **Florida + New York**; **virtual only**; accepting new clients on a **limited basis**; offers a **free 15-minute consultation**; **private-pay** (Superbill available); relational-psychoanalytic, depth/long-term.
- Hero: H1 `Concierge Psychological Services`; sub `Depth-oriented therapy for high achievers.`
- **Areas of Focus (12, in order):** Relationship problems · Identity beyond achievement · Connecting accomplishments with deeper values · Life & career transitions · Perfectionism & self-criticism · Low self-esteem · Building a more meaningful life · Legacy & purpose · Burnout · Emotional dysregulation · Anxiety and depression · Neurodiverse couples.
- **Home founder band:** *"Dr. Schulhofer is also the founder of Architecture of Excellence™, offering 1:1 coaching, speaking engagements, & consulting for high-performing individuals, teams & organizations. Explore →"*
- **Services founder band:** *"Looking for executive coaching or organizational consulting rather than clinical therapy? Dr. Schulhofer is also the founder of Architecture of Excellence™ — a framework for leaders, teams & organizations. Explore →"* (→ https://architectureofexcellence.com)
- **About bio** describes AOE as a **six-pillar** proprietary system and "my **1:1 coaching and consulting** services." **Clinical Focus** = Trauma · Personality · Relationships (dissociation was removed).
- All longer body/service/FAQ copy is Alina's **own verbatim text** — never paraphrase it.

---

## 6. Decisions approved / things rejected

**Approved:**
- Two separate sites on two domains; therapy stays single-purpose.
- Black/white/gold palette (distinct from AOE's ivory/gold); keep header **light** (never a dark nav bar).
- Arms-crossed studio photo as the primary image; tight face-crop circle on About.
- Section dividers = **full-width gold line, no diamond**; Philosophy bookended by lines.
- Founder note = **charcoal full-width band** with one uniform gold-grey text color; on Home it sits **below** the contact CTA.
- Areas of Focus sits **under** Philosophy; the "What I Help With" label was removed; bullets are **gold dots** (not diamonds).
- Contact = **form (Formspree) + email/phone**; phone & message fields **required**.
- Header/`.pg-head` gets a subtle gradient on all inner pages.
- Quiet **"Architecture of Excellence ↗"** link in the footer sitewide.
- Full six animation touches added (with reduced-motion support).

**Rejected / do NOT:**
- **No client testimonials** (therapist ethics).
- **No dark/charcoal header nav.**
- **No credentials block** on About (removed as redundant).
- **No separate "other services" page** on the therapy site.
- Do **not** regionalize (no "Middle East"/Gulf framing on the therapy site).
- Hero sub-line: the idiom *"It's lonely at the top —"* was **removed** by the client (kept only `Depth-oriented therapy for high achievers.`). Do not reintroduce without asking.
- **Never invent/paraphrase clinical content** — a prior batch of AI-written content was rejected; use only client-provided exact wording.

---

## 7. Deployment plan (not yet executed)

Both domains are registered/managed at **Squarespace**. AOE currently lives on **GitHub Pages** (repo `alinaschulhofer/aoe`, branch `gh-pages`) and — importantly — its `CNAME` file currently says **`www.dralinaschulhofer.com`**, i.e. **AOE is presently served on the therapy domain.** Launch is therefore a **SWAP**, done deliberately at a low-traffic time:

1. **Change AOE repo `CNAME`** from `www.dralinaschulhofer.com` → `www.architectureofexcellence.com`.
2. In Squarespace DNS for **architectureofexcellence.com**, point to GitHub Pages: A records → `185.199.108.153 / .109.153 / .110.153 / .111.153`; `www` CNAME → `alinaschulhofer.github.io`.
3. **Host the therapy `therapy-site/`** — **recommended: Netlify** (free, drag-and-drop, auto-HTTPS, and **built-in Forms** could replace Formspree). Alternative: a second GitHub Pages repo (then keep Formspree).
4. Add `www.dralinaschulhofer.com` as the therapy host's custom domain; in Squarespace DNS repoint `dralinaschulhofer.com` from GitHub → the therapy host.
5. Verify HTTPS on both; **test the form** (send a real submission; complete Formspree/host confirmation).

**Safety rule:** building files = **zero risk to AOE**. Do **not** touch AOE's `CNAME`/DNS/`gh-pages` until the deliberate cutover.

---

## 8. Current state & remaining tasks

**State:** Design/content essentially complete in `therapy_template.html`. Preview artifact and `therapy-site/` were built and match — **except** the last three text edits below, which are in `therapy_template.html` but the outputs were **not yet regenerated**:
1. Hero sub-line now `Depth-oriented therapy for high achievers.`
2. Areas of Focus: `Building a more meaningful life` (was "…and purposeful life").
3. Areas of Focus: `Legacy & purpose` (was "Legacy").

**➡ First action in the new chat:** regenerate **both** outputs so they include these edits (rebuild the artifact via the inject→extract→ascii-encode→publish flow to the same URL, and run `build_site.py` to refresh `therapy-site/`). Then verify.

**Open decisions / optional (discussed, not built):**
- Dedicated Formspree form for the therapy site (vs. shared `xzdwqnvk`).
- Trust signals: license numbers, Psychology Today "Verified" badge, memberships.
- Compliance for a US clinical site: **crisis line note (988)**, **Privacy Policy**, **Good Faith Estimate** notice.
- Optional Insights/blog section (curated clinical essays with `rel=canonical` back to AOE to avoid duplicate content).
- Real favicon file (currently just the 🕊️ emoji on the artifact).
- Analytics (AOE uses GA `G-H4ZR2JQYWN`; therapy site has none).

---

## 9. Rules for safely editing later (preserve the design)

1. **Edit the MASTER `therapy_template.html`**, then rebuild both outputs (preview artifact + `therapy-site/`). Keeping them in sync prevents drift.
2. **Keep the tokens** — don't add new colors or fonts; reuse the CSS variables and existing classes: `.divider-full, .founder / .founder-line / .founder-link, .helpwith / .help-list, .cform, .arrow-cue, .reveal / .reveal-img, .pg-head, .trust3, .philosophy-band, .svc-acc, .nav-toggle`.
3. **Dividers:** `.divider-full` is a `100vw` breakout — it works in wide/centered contexts but **breaks inside `.container.narrow`** (renders off-center). Inside the narrow Services column, use the **gold top-border on the accordion** pattern instead.
4. **Any new motion** must include a `prefers-reduced-motion` off-switch, matching the existing `@media(prefers-reduced-motion:reduce)` block.
5. **Copy:** use the client's exact wording; never paraphrase clinical/service/FAQ text.
6. **Encoding:** when regenerating the artifact, keep the `ascii/xmlcharrefreplace` step so `·`, `—`, `™`, `→` render correctly.
7. **Never touch the AOE deployment** (repo `aoe`, `gh-pages`, its `CNAME`/DNS) except during an intentional, coordinated launch cutover.
8. To view changes without spending heavily: prefer the deploy files opened locally over repeatedly re-publishing the 2.6 MB artifact.

---

*Files that travel with this handoff: `therapy-site/` (deploy package: index/about/services/faq + styles.css + assets/), plus the build sources `therapy_template.html`, `assets.b64`, and `build_site.py`.*
