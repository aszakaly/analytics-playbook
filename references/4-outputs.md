# Stage 4 — Outputs (dashboards / decks / production scripts)

Pick the medium first, then: audience → look-and-feel options → build the chosen
one → verify. Never jump straight to a finished build.

## 0. Pick the output type (ask first)

Confirm what the work should produce (`AskUserQuestion`) — it shapes everything:

- **Slide deck** — a narrative for humans (leadership brief, technical review).
- **Dashboard** — an interactive surface to explore the data.
- **Production-ready modelling script** — a clean module/CLI for handoff.
- **A combination** (e.g. a deck for the readout + a script for the model).

---

## A. Slide decks (presentations)

**Separate decks per audience.** They carry different stories:

- **Executive** — minimal: ~≤5 content slides, opening with an **executive-summary**
  slide (the ask, the answer, the headline number), then trust/why-it-matters,
  then a recommendation. Push detail and the decision rationale into an
  **appendix**.
- **Internal / technical** — full storyline, no slide cap: objective & approach,
  data & quality, key decisions (with evidence), method/benchmark, validation,
  governance/limitations, reproducibility, conclusion, appendix.

Both decks get a **Contents** slide; the **cover and contents don't count** toward
any slide limit.

**Default to BOTH formats:**
- **PPTX** via `pptxgenjs` (Node). Use **Office-safe fonts** (Arial / Cambria /
  Courier New) so the render is faithful everywhere — the brand fonts won't be on
  the viewer's machine. Carry the brand through **palette + layout + motif**
  (cobalt/steel on graphite, mono uppercase eyebrows, drafted offset-frame cards,
  registration-cross + monogram).
- **Self-contained HTML** via Chart.js + the **real brand fonts** (Google Fonts),
  slides at 1280×720 scaled to fit, arrow-key/scroll nav, one slide per print
  page.

**Build notes (learned the hard way):**
- Native PPTX **scatter** renders unreliably in LibreOffice/PowerPoint — render it
  as a **PNG** (matplotlib, brand-styled) and embed the image. Bar/line/column
  charts are fine as native pptx charts (and stay editable).
- In the HTML builder, inject data via a `type="application/json"` block or
  placeholder replacement, and **syntax-check the generated chart `<script>`**
  (`node --check`) — one malformed chart config silently blanks *every* chart.
- Use the `akos-szakaly-brand` skill for tokens, fonts, and slide-type patterns.

## B. Dashboards

### Audience (decides layout and content)

- **Operational** (marketing/CRM/ops): act on individual records. Needs group
  selection, per-group detail + recommended action, a searchable/sortable/
  **exportable** record table, filters (segment, geography, recency/recentness).
- **Executive** (leadership): the story, not the rows. KPIs, concentration
  (where the value lives), population-vs-value imbalance, trend/seasonality, one
  headline insight.

These usually warrant **separate dashboards**. Confirm which are needed.

### Mockups before building

Produce **static look-and-feel mockups in a few distinct directions** and let the
user choose before any real build. Good default trio: a **safe generic** clean
style; the **user's brand** (`akos-szakaly-brand` — cobalt/graphite, sharp
"drafted" cards, mono metrics, indexed mono labels); a **modern** option
(SaaS/BI navy-sidebar + blue accents). Render inline (the visualization widget),
real headline numbers, placeholder rows marked as such. Parallelisable — fan out
one per style×audience if subagents are available and the user is fine with it.

### Build the chosen dashboard

**Default: self-contained interactive HTML** with the real data embedded as JSON,
so it opens in any browser with no server. Confirm if a live app (Streamlit/Dash)
is genuinely wanted. Build pattern (see `templates/dashboard_build_scaffold.py`):

- Prepare data once into a JSON blob (group summaries, trend series, breakdowns,
  full record list for operative use).
- Inject JSON via placeholder replacement (avoid f-strings fighting CSS braces).
- Make interactivity real: filters recompute from embedded records; table sort;
  live search; **CSV export of exactly the filtered set** via Blob.
- Keep numbers honest: only show deltas/trends you can actually compute.

### Visual / chart catalogue (pick by intent)

- **Composition / "where value lives"**: horizontal bars sorted by value; donut
  for top-N share.
- **Imbalance** (share of population vs share of value): paired bars per group.
- **Trend / seasonality**: line or area over time; mark recurring peaks.
- **Distribution**: histogram; flag skew.
- **Per-record detail**: dense table with mono numerals, group color dots, score
  badges.
- KPI cards for headline metrics; one callout box for the single key insight.

## C. Production-ready modelling scripts

When the deliverable is the model itself, not a readout. Settle four decisions up
front (`AskUserQuestion`): **interface** (importable core + CLI / REST API /
module-only / CLI-only), **I/O** (CSV batch / JSON / single vs batch),
**validation behaviour** (reject-with-reason / fail-fast / clamp / none), and
**output contents** (prediction + metadata + flag / + policy / prediction-only).
Then build to these patterns:

- **One core, thin wrappers.** A `score_frame(df)` / `score_record(dict)` core the
  CLI (and any future API) both call — one code path, one place to test.
- **Feature contract as code.** `FEATURES` + `RANGES` constants; validate per row.
  A missing *column* is a fatal contract error (non-zero exit); a bad *value* is a
  per-row reject. **Never silently coerce.**
- **Reject with a reason.** Score the valid rows, attach `status` + `reason`, keep
  the batch going, and write the rejected rows to a separate file.
- **Traceability in every record.** `model_version` (a content hash of the
  artifact) + `scored_at` + validation status, so any prediction is auditable.
  Keep **business policy (approve/decline bands) out of the model script** — emit
  the number; let the consumer apply policy.
- **Flag out-of-distribution inputs (soft).** The contract `RANGES` are usually
  wider than what the model actually trained on, so a row can pass validation yet
  be an extrapolation. Carry a separate `ood_flag` + `ood_reason`, raised when an
  input leaves the per-feature training envelope (e.g. `[p1, p99]`) — a **soft**
  signal that never rejects the row or changes `status`. Build the envelope once
  from the training split into a small **committed reference** (JSON) the scorer
  loads at runtime, so it stays inference-only and needs no raw data in
  production; degrade gracefully (flag left empty) if the reference is absent.
- **Inference-only + pinned runtime.** Load the saved artifact (training stays in
  the numbered scripts); record the training library version and warn on mismatch
  — pickled models break across versions.
- **Observability.** Per-row errors travel with the *data* (reason column + rejects
  file), not the log. Operational + fatal messages go through **one logger to
  stderr** (the platform persists stderr; offer an optional `--log-file`); raise a
  **catchable error type** for fatals (not a bare `SystemExit`) so library callers
  can handle it, and have the CLI log it at ERROR + exit non-zero.
- **Ship a built-in smoke test** (e.g. `--selftest`): assert a known-good record
  scores plausibly and a known-bad one is rejected — a verifiable handoff.
- **Name it plainly** (`score.py`), not as a numbered pipeline stage — `01–05`
  regenerate outputs from raw and run in order; a consumer/inference script sits
  outside that chain (and a module name can't start with a digit).

Document the feature contract (names, types, ranges), the run commands, and keep
the training/eval reproducible + the decision record (`MODEL_DECISION.md`-style)
alongside.

---

## Verify before delivering (every medium)

Confirm the output actually renders and is correct — don't ask the user to be the
tester:

- **Decks (PPTX):** render to images (LibreOffice → PDF → `pdftoppm`) and visually
  inspect every slide for overflow/overlap; also extract text to catch leftovers.
- **Decks (HTML) / dashboards:** serve and screenshot; confirm fonts load, **charts
  actually drew** (sample canvas pixels or check `Chart.getChart`), and
  interactivity works; check displayed numbers match the source aggregates.
