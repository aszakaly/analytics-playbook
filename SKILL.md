---
name: analytics-playbook
description: >-
  Akos's standard modus operandi for any end-to-end data-analysis project:
  data discovery → cleaning (with a full audit trail) → analysis method
  selection → dashboard design & build → reproducible code + README → a
  retrospective that improves this playbook. Use this skill whenever the user
  starts an analytical or data project, mentions a dataset/CSV/Excel/warehouse
  table to analyse, asks to explore/profile/clean data, build a model or
  segmentation (e.g. RFM, cohort, churn), create dashboards or data
  visualisations, or wants a repeatable analysis process. Trigger it even when
  the user only names one stage (e.g. "clean this data" or "build a
  dashboard") so the work stays consistent with the rest of the pipeline.
  This is a process/workflow skill, not a single tool — prefer it for the
  shape of the work, then use specific data skills inside each stage.
---

# Analytics Playbook

A staged, gated workflow for taking a raw dataset all the way to decision-ready
dashboards and a reproducible, documented repository. It exists to make every
analytical project follow the same disciplined shape, so the output is
trustworthy, auditable, and repeatable — and so the process itself improves
over time.

## Core operating principles (these hold across every stage)

1. **Sequence is key — never do it all at once.** Run the stages in order.
   Finish a stage, show the result, and get a decision before moving on. The
   user has been explicit about this: surfacing intermediate results and
   pausing at decision points is the point, not an overhead.
2. **Surface decisions, don't bury them.** At each fork that changes the
   outcome (snapshot date, what counts as a duplicate, number of segments,
   dashboard audience, visual style...), present 2–4 options **with a clear
   recommendation** and let the user choose. Use the `AskUserQuestion` tool for
   these. Pick obvious defaults silently; escalate only the choices that matter.
3. **Everything is auditable.** Any row deleted, changed, or transformed must
   be traceable to a reason, and totals must reconcile. See
   `references/2-cleaning-audit.md` — this is non-negotiable.
4. **Reproducible by default.** The end state is numbered, standalone scripts
   plus a README that lets anyone regenerate every output. No "it only exists
   in the notebook I ran once."
5. **Recommend, then act.** Don't present an exhaustive survey of options and
   stop. Give a recommendation and a reason; act once the user confirms.

## The pipeline at a glance

```
0. Setup       → question, decision, audience, data + version control (local/GitHub)
1. Discovery   → profile shape / grain / quality BEFORE touching anything
2. Cleaning    → rule-by-rule, gated, with a full removal/transformation audit
3. Method      → present analysis options + recommendation; check feature provenance
4. Outputs     → pick medium (deck / dashboard / production script) → build for audience
5. Cross-exam  → adversarial review from a chosen role; document Q&A + side tasks
6. Repository  → numbered reproducible scripts + README (revisit GitHub if deferred)
7. Retro       → capture learnings back into THIS skill
```

Each stage has its own reference file with the detailed checklist. Read the
referenced file when you enter that stage — don't try to hold all of it at once.

---

## Stage 0 — Frame & set up the project

Before any tooling, establish in one or two exchanges:

- **The question**: what is being asked, in business terms.
- **The decision it informs**: what someone will *do* differently with the answer.
  Analysis with no attached decision is a warning sign — say so.
- **The audience**: who consumes the output (operators vs leadership shapes
  everything downstream).
- **The data available**: file(s), table(s), connectors. Locate them.
- **Version control**: decide up front whether the work gets its own **local git
  repo** (default yes for anything beyond a throwaway look) and whether to also
  create a **remote GitHub repo** — if so, settle the name and visibility
  (`AskUserQuestion`; public exposes data, so confirm). If the remote is
  deferred, note it and **revisit the decision at Stage 6**.

Keep this light. One short paragraph back to the user confirming the framing
(and the repo decision) is enough before moving to discovery.

## Stage 1 — Data discovery

Profile the raw data and report what's there *before* changing anything. If a
`/explore-data` or equivalent data-profiling skill is available, use it. Cover:
shape, grain (one row per *what*), candidate keys, column types, null rates,
cardinality, distributions, date ranges, and quality red flags.

Output a clean profile and a short list of issues that will need decisions in
cleaning. **Then stop and let the user react.** Full checklist:
`references/1-discovery.md`.

## Stage 2 — Data cleaning (with mandatory audit trail)

Clean rule-by-rule, in a sensible order, **reporting the row impact of each
step**. The deliverables are always:

- the **cleaned dataset**, and
- an **audit file** capturing every removed / changed / transformed row with a
  `reason` (and a step identifier), where `kept + removed = raw` reconciles
  exactly.

Surface any judgement call (how to treat cancellations/reversals, whether to
drop or impute nulls, whether to keep out-of-scope segments) as a decision, not
a silent default. The full cleaning + audit specification, including the
audit-capture code pattern, is in `references/2-cleaning-audit.md`. A ready
scaffold is in `templates/clean_script_scaffold.py`.

## Stage 3 — Analysis method selection

Don't jump to computing. First **present the candidate methods** for the
question (e.g. rule-based scoring vs clustering vs a hybrid for segmentation),
each with trade-offs and a recommendation, and get the user's choice. Then
settle the parameters that change results (reference dates, score bins, k,
thresholds) — again as explicit decisions. **Check feature provenance**: if a
candidate predictor might be an *output* of the process you're modelling (a
price, score, or institution-set field), test whether it's recoverable from the
other inputs and decide input-vs-output before including it — using a downstream
output is leakage. When provenance can't be verified, record the call as a
**stated assumption**, not a fact, and mirror that framing across all docs. Where useful, run a **validation cross-check** (e.g.
elbow/silhouette, or hold-out metrics) so the chosen method is defensible.
Detail and a decision-framing pattern: `references/3-method-selection.md`.

## Stage 4 — Outputs (dashboards / decks / production scripts)

First **ask what output the work should produce** (`AskUserQuestion`), since it
shapes everything downstream:

- **Slide deck** — a narrative for humans (leadership brief, review). Usually
  *separate decks per audience*: executive (minimal, ~≤5 content slides + an
  executive-summary slide + an appendix for key decisions) and internal/technical
  (full storyline, no cap). Both get a Contents slide; cover + contents don't
  count toward limits. Default to producing **both PPTX** (pptxgenjs,
  Office-safe fonts) **and self-contained HTML** (Chart.js, real brand fonts).
- **Dashboard** — an interactive surface to explore the data. Operational (act
  on individual records) vs executive (KPIs + concentration); often *separate*
  dashboards. Default to **self-contained interactive HTML** with data embedded.
- **Production-ready modelling script** — a clean, parameterised, documented
  module/CLI (saved model + an inference entry point) for handoff into a system.
  Carry a soft **out-of-distribution / extrapolation flag** with each prediction
  (inputs outside the training envelope), from a small committed reference so the
  scorer stays inference-only.
- or a **combination** of these.

Then, whatever the medium: **audience first → show look-and-feel options in a
few style directions before building** (a safe generic, the user's brand via
`akos-szakaly-brand`, a modern option) → build the chosen one → **QA visually
before claiming done** (render PPTX→images and inspect; for HTML, serve +
screenshot + confirm charts actually drew).

Audience patterns, the chart catalogue, the interactive-HTML build pattern, and
the deck/presentation conventions are in `references/4-outputs.md`. Scaffold:
`templates/dashboard_build_scaffold.py`.

## Stage 5 — Cross-examination (Devil's advocate)

Before publishing, **red-team the work**. Ask which adversarial **role(s)** to
adopt (`AskUserQuestion` — CFO, Chief Risk Officer, Compliance / Fair-Lending,
Model Validation, CMO…), then formulate pointed, role-specific challenges to the
findings, model, and decisions. For each: give the honest current answer from the
evidence, mark a **verdict** (resolved / open / mitigate), and where it can't be
settled from what's on hand, define a **side validation task** (robustness,
sensitivity, subgroup error, over-/under-shoot, leakage re-check…) and run the
cheap, high-value ones. Feed the outcome back — caveats into the README, or
re-open an earlier decision. Deliverable: a **`CROSS_EXAMINATION.md`** log
(role · challenge · response · verdict · side task). Challenge-pattern library
and the run pattern: `references/5-cross-examination.md`.

## Stage 6 — Reproducible repository

Leave behind numbered, standalone scripts (`01_clean_data.py`,
`02_<model>.py`, `build_dashboards.py`, ...) that regenerate every output from
the raw input, and a **README** in the established format (purpose, key steps,
key decisions table, pipeline diagram, methodology, one-line description of
every file). Verify the scripts actually run and reproduce the numbers before
calling it done. Conventions and the README template:
`references/6-repo-readme.md` and `templates/README_template.md`. **If the remote
GitHub repo was deferred at Stage 0, revisit it now** — offer to create it and
confirm name/visibility/what-to-exclude; keep large reproducible artifacts out of
git (gitignore + document how to regenerate).

## Stage 7 — Retrospective (this is how the playbook learns)

This stage is what makes the modus operandi *adjustable*. After delivery,
briefly reflect and **propose concrete improvements to this skill**:

- What decision points were missing, or asked unnecessarily?
- Did a default turn out wrong? Should a recommendation change?
- Was a new reusable pattern or script discovered worth bundling?
- Did the user state a durable preference?

Offer the edits, and on approval: update the relevant file(s) here, add a dated
entry to `CHANGELOG.md`, and write durable user preferences to memory as
`feedback`/`project` notes so they persist across projects. Keep changes
general — fix the principle, not just the one example (see the writing notes in
`CHANGELOG.md`). Don't rewrite the skill silently; show what you're changing
and why.

---

## Worked references

Two projects bracket the playbook's range — use them as the canonical examples of
the depth and shape each stage should reach.

**RFM customer segmentation** (Online Retail II) — the *unsupervised segmentation
→ dashboards* path: discovery → cleaning (cancellation pairing + 297k-row audit)
→ quintile RFM into 10 named, strategy-ready segments (K-Means-validated) →
executive + operative interactive HTML dashboards → reproducible scripts + README
→ public GitHub repo.

**Mortgage maximum-loan model** (49,990 applicants) — the *supervised modelling →
decks + production + red-team* path, exercising the stages RFM didn't:
- **Held-out target** discipline (the actual max loan kept out of all modelling,
  used only for final evaluation) and **feature provenance** — interest rate
  excluded as an *assumed* bank output (a stated, non-verifiable assumption),
  down payment kept — then **parsimony**, 12→4 features once income/credit proxies
  were pruned.
- Model picked by a 6-way benchmark → **HistGradientBoosting** (raw target),
  validated against the held-out actual (R² 0.990, MAE $21,966) with error-by-band.
- **Outputs:** executive + internal decks (PPTX + HTML) *and* a production
  `score.py` (feature-contract validation, reject-with-reason, traceability, soft
  OOD flag, `--selftest`).
- **Stage 5 cross-examination:** a Chief-Risk-Officer red-team with side validation
  tasks — over-lending tail, input sensitivity, a debt partial-dependence that
  *resolved* a flagged worry, and noise-degradation → `CROSS_EXAMINATION.md`.
- Decision record (`MODEL_DECISION.md`) + reproducible numbered scripts + README →
  public GitHub repo.

## Adapting the playbook

Not every project needs every stage at full depth — a quick exploration may
stop at Stage 1; a modelling refresh on already-clean data may skip to Stage 3.
Scale the rigor to the request, but keep the **order**, the **decision gates**,
and the **audit + reproducibility** guarantees. When you skip or compress a
stage, say so, so the user can object.

**Extending a closed project (add-on work).** When the ask is to *add* an analysis
to an already-delivered project, re-discover the existing pipeline first (read its
README / decision record / scripts), then enter at Stage 3–4. Treat the shipped
pipeline as **frozen** — don't modify the numbered scripts or the model; add
plainly-named scripts outside the numbered chain (as a consumer/inference script
already does). Hold the same audit + reproducibility bar: if you must reconstruct
data a saved artifact didn't store (e.g. recover features behind a predictions
file by replaying the exact deterministic split), **assert an invariant that proves
alignment** — such as a reconstructed target bit-identical to the saved one —
before any positional join, so the join is audited, not assumed.

**Resuming across sessions (context hygiene).** The stages double as resume
checkpoints — each ends with a durable on-disk artifact + a logged decision, so
the files (not the conversation) are the source of truth. If context gets heavy,
prefer to stop **at a stage boundary** once that stage's outputs are written, then
reset: `/compact` to continue in-session when mid-stage, or `/clear` / a new
session at a boundary. To pick back up, point at the artifacts — e.g. *"Resume
<project> at Stage N: read README.md + MODEL_DECISION.md + the scripts, confirm
state, then continue."* Before resetting, make sure the last stage's decisions are
actually committed/written — that is what makes the pickup lossless.
