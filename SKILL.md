---
name: analytics-playbook
description: >-
  A staged, gated workflow for executing a data-analysis project end to end:
  frame the question → profile the raw data → clean it with a full audit trail
  → choose and defend a method → build the outputs → red-team them → leave a
  reproducible repository → retro that improves the playbook itself. Use it
  whenever an analytical or data project starts, a dataset (CSV, Excel,
  warehouse table) is named for analysis, or the ask is to explore, profile or
  clean data, build a model or segmentation (RFM, cohort, churn), or produce
  dashboards, decks or data visualisations. Trigger it even when only one stage
  is named ("clean this data", "build a dashboard") so the work stays
  consistent with the rest of the pipeline. In scope: the execution of the
  analysis and the artifacts it leaves behind. Out of scope: raw data
  collection, model and output governance, and the later technical management
  or deployment of the output.
---

# Analytics Playbook

A staged, gated workflow that takes a dataset from raw to decision-ready and
leaves behind a reproducible, documented repository. It exists so that any
analytical project follows the same disciplined shape — trustworthy, auditable,
repeatable — and so the process itself improves after each run.

- **In scope:** executing an analytics project, Stage 0 → Stage 7 below.
- **Out of scope:** raw data collection, model/output governance, and the later
  technical management or deployment of what is built here.

## Core operating principles (these hold across every stage)

1. **Sequence is gated, not drip-fed.** State the whole job up front —
   question, the decision it supports and who makes it, audience for the
   outputs, dataset and what is known about its provenance and timing, likely
   method branch, definition of done, and what is explicitly out of scope.
   Then run the stages in order. Gating is about *approval*, not about
   withholding context: finish a stage, show the result, get a decision before
   moving on. The goal is never discovered one stage at a time.
2. **Surface decisions, don't bury them.** At each fork that changes the
   outcome (snapshot date, what counts as a duplicate, number of segments,
   dashboard audience, visual style…), present 2–4 options **with a clear
   recommendation** via `AskUserQuestion`. Pick obvious defaults silently;
   escalate only the choices that matter.
3. **Everything is auditable.** Any row deleted, changed, or transformed is
   traceable to a reason, and totals reconcile exactly — non-negotiable, see
   `references/2-cleaning-audit.md`.
4. **Reproducible by default.** The end state is numbered, standalone scripts
   plus a README that lets anyone regenerate every output. No "it only exists
   in the notebook I ran once."
5. **Recommend, then act.** Don't present an exhaustive survey of options and
   stop. Give a recommendation and a reason; act once the user confirms.
6. **Deliverables are sized to the decision.** Match the length of any written
   artifact — README, cleaning audit, decision memo, cross-examination log,
   retro entry — to what the task needs: cover the substance, do not pad with
   filler sections, redundant summaries, or boilerplate. Prefer a table or a
   numbered decision list over prose restatement. If a section repeats
   something stated elsewhere in the repo, link it instead of restating it.

## The pipeline at a glance

```
0. Setup       → project spec (question · decision · audience · data · done · out-of-scope) + version control
1. Discovery   → profile shape / grain / quality BEFORE touching anything
2. Cleaning    → rule-by-rule, gated, with a full removal/transformation audit
3. Method      → present options + recommendation; check feature provenance
4. Outputs     → pick medium (deck / dashboard / production script) → build for audience
5. Cross-exam  → adversarial review from a named stakeholder role → written Q&A
6. Repository  → numbered reproducible scripts + README (revisit GitHub if deferred)
7. Retro       → capture learnings back into THIS skill
```

Each stage has its own reference file with the detailed checklist. Read the
referenced file when you enter that stage — don't try to hold all of it at once.

---

## Stage 0 — Frame & set up the project

Write the **project spec** as a block in the working notes or README. This is
mandatory and must exist before Stage 1 begins:

| Line | Content |
|---|---|
| Question | what is being asked, in business terms |
| Decision & owner | what someone will *do* differently, and who decides. No attached decision is a warning sign — say so |
| Audience | who consumes the outputs (operators vs leadership shapes everything downstream) |
| Data | the file(s) / table(s) / connectors, located — plus what is known about provenance and timing |
| Likely method branch | the expected Stage 3 direction, stated as an expectation |
| Definition of done | the artifacts that end the job |
| Out of scope | what this project will deliberately not do |

The last two lines are the project's **scope guardrail**; later stages cite them
rather than carrying scope rules of their own.

Also settle **version control** here: a local git repo (default yes for anything
beyond a throwaway look), and whether to add a remote GitHub repo — name and
visibility via `AskUserQuestion`, since public exposes the data. If the remote is
deferred, note it and revisit at Stage 6.

## Stage 1 — Data discovery

Profile the raw data and report what's there *before* changing anything (use
`explore-data` or an equivalent profiling skill if available). Output a clean
profile plus a short, ranked list of the issues that will need a cleaning
decision — **then stop and let the user react.** Checklist:
`references/1-discovery.md`.

## Stage 2 — Data cleaning (with mandatory audit trail)

Clean rule-by-rule, in a sensible order, **reporting the row impact of each
step**. Two deliverables, always: the **cleaned dataset**, and an **audit file**
holding every removed / changed / transformed row with a step id and a `reason`,
where `kept + removed = raw` reconciles exactly.

Surface every judgement call as a decision, not a silent default — cancellations
and reversals, drop vs impute vs flag for nulls, whether out-of-scope rows go
(cite the Stage 0 out-of-scope line). Specification + audit-capture pattern:
`references/2-cleaning-audit.md`; scaffold: `templates/clean_script_scaffold.py`.

## Stage 3 — Analysis method selection

Don't jump to computing. **Present the candidate methods** with trade-offs and a
recommendation, get the choice, then settle the parameters that change results
(reference dates, score bins, k, thresholds) as explicit decisions, and
cross-check the result so the choice is defensible.

Two things carry real risk and are specified in
`references/3-method-selection.md`: **feature provenance** — a predictor that is
itself an *output* of the process being modelled is leakage, and when provenance
can't be established the call is a **stated assumption**, not a fact — and
**holding the target out** of every cleaning, feature, and selection step.

## Stage 4 — Outputs (decks / dashboards / production scripts)

First **ask what the work should produce** (`AskUserQuestion`) — it shapes
everything downstream:

- **Slide deck** — a narrative for humans; usually separate executive and
  internal/technical decks, as both PPTX and self-contained HTML.
- **Dashboard** — an interactive surface; operational (act on records) vs
  executive (KPIs + concentration), usually separate. Default: self-contained
  interactive HTML with the data embedded.
- **Production-ready modelling script** — a parameterised module/CLI with a saved
  model and an inference entry point, for handoff into a system.
- or a **combination**.

Then, whatever the medium: **audience first → show look-and-feel options in a few
style directions before building** (a safe generic, the user's own brand skill if
they have one, a modern option) → build the chosen one → **render it and
inspect before delivering**. Audience patterns, deck conventions, chart
catalogue, the interactive-HTML pattern, and the production-script contract:
`references/4-outputs.md`; scaffold: `templates/dashboard_build_scaffold.py`.

## Stage 5 — Cross-examination (Devil's advocate)

> Stage 5 is not a correctness re-check. The model verifies its own work
> already; generic "double-check", "re-verify", or "delegate verification to a
> subagent" instructions are deliberately absent from this playbook and should
> not be added back. Stage 5 is an adversarial review from a named stakeholder
> role (CRO, CFO, Compliance, Model Validation, CMO) whose output is a written
> Q&A artifact for a human reader: challenges to assumptions, framing, and
> fitness for the decision. If a challenge can be settled by re-running the
> code, it belongs in Stage 2 or 3, not here.

Ask which role(s) to adopt (`AskUserQuestion`), put pointed role-specific
challenges to the findings, model, and decisions, answer each from the evidence
with a **verdict** (resolved / open / mitigate), and where a challenge can't be
settled from what's on hand define a **side validation task** and run the cheap
high-value ones. Feed the outcome back: caveats into the README, or re-open an
earlier decision. Deliverable: a **`CROSS_EXAMINATION.md`** log (role ·
challenge · response · verdict · side task). Role library, side-task catalogue,
and run pattern: `references/5-cross-examination.md`.

## Stage 6 — Reproducible repository

Leave numbered, standalone scripts (`01_clean_data.py`, `02_<model>.py`,
`build_dashboards.py`, …) that regenerate every output from the raw input, plus a
**README** in the format specified in `references/6-repo-readme.md` (template:
`templates/README_template.md`) — the key-decisions table is its most valuable
section. A fresh run must reproduce the reported numbers.

**If the remote GitHub repo was deferred at Stage 0, settle it now** — name,
visibility, what to exclude; keep large reproducible artifacts out of git
(gitignore + document how to regenerate).

## Stage 7 — Retrospective (this is how the playbook learns)

After delivery, briefly reflect and **propose concrete improvements to this
skill**: decision points that were missing or asked unnecessarily, defaults that
turned out wrong, reusable patterns worth bundling, durable user preferences.

Offer the edits, and on approval: update the relevant file(s) here, add a dated
`CHANGELOG.md` entry, and write durable preferences to memory as
`feedback`/`project` notes. Keep changes general — fix the principle, not just
the one example. Don't rewrite the skill silently.

**Keeping the playbook small.** Every additive edit pays rent: name the file the
text belongs in, and apply principle 6 to it — if it is already said elsewhere,
link instead. That is what keeps consolidation rare.

After every fifth changelog entry, or when `SKILL.md` or a reference file passes
~8k, **say that a consolidation is due** and let the user decide. Deferral is a
valid answer and is recorded in the next entry as deferred, so the debt stays
visible. A consolidation that does run gets its own branch and PR, keeps every
worked example, hard number and stated reason a rule exists (only restatement and
duplication go), and logs every merge and deletion with before/after byte counts
in a `CONSOLIDATION_LOG`.

---

## Worked references

Two projects bracket the playbook's range — the canonical examples of the depth
each stage should reach.

**RFM customer segmentation** (Online Retail II) — the *unsupervised segmentation
→ dashboards* path: discovery → cleaning with cancellation pairing and a
**297k-row reconciling audit** → quintile RFM into 10 named, strategy-ready
segments, K-Means-validated → executive + operative interactive HTML dashboards →
numbered scripts + README → public GitHub repo.

**Mortgage maximum-loan model** (49,990 applicants) — the *supervised modelling →
decks + production + red-team* path: **held-out target** (the actual max loan kept
out of all modelling, used only for final evaluation); **feature provenance** —
interest rate excluded as an *assumed* bank output (a stated, non-verifiable
assumption), down payment kept — then **parsimony**, 12→4 features once
income/credit proxies were pruned; a 6-way benchmark → HistGradientBoosting,
R² 0.990 / MAE $21,966 against the held-out actual with error-by-band; executive +
internal decks *and* a production `score.py`; a Chief-Risk-Officer red-team
(worked through in `references/5-cross-examination.md`); `MODEL_DECISION.md` +
numbered scripts + README → public GitHub repo.

## Adapting the playbook

Not every project needs every stage at full depth — a quick exploration may stop
at Stage 1; a refresh on clean data may skip to Stage 3. Scale the rigor to the
Stage 0 definition of done, but keep the **order**, the **decision gates**, and
the **audit + reproducibility** guarantees. When you skip or compress a stage,
say so, so the user can object.

**Extending a closed project (add-on work).** Re-discover the existing pipeline
first (its README, decision record, scripts), then enter at Stage 3–4 and treat
the shipped pipeline as **frozen** — add plainly-named scripts outside the
numbered chain rather than editing `01–05` or the model. Hold the same audit bar:
if you must reconstruct data a saved artifact didn't store (e.g. recovering the
features behind a predictions file by replaying the exact deterministic split),
**assert an invariant that proves alignment** — such as a reconstructed target
bit-identical to the saved one — before any positional join, so the join is
audited rather than assumed.

**Resuming across sessions.** Each stage ends with a durable on-disk artifact plus
a logged decision, so the files, not the conversation, are the source of truth.
When context gets heavy, finish the stage, write its outputs, then reset
(`/compact` mid-stage, `/clear` or a new session at a boundary) and resume by
pointing at the artifacts: *"Resume <project> at Stage N: read README.md +
MODEL_DECISION.md + the scripts, then continue."*
