# Changelog — analytics-playbook

This skill is meant to **learn**. After each project (Stage 6 — Retrospective),
record what changed and why. Keep changes *general* — fix the underlying
principle, not just the one example that exposed it. Prefer explaining the *why*
to adding rigid MUST/NEVER rules.

How to evolve it:
- Update the relevant `SKILL.md` / `references/*` / `templates/*` file.
- Add a dated entry below: what changed, and the observation that prompted it.
- Write durable user preferences to memory (`feedback`/`project`) so they carry
  across projects, and link them from here if useful.

---

## v1.0 — 2026-06-17

Initial version, distilled from the first project built this way: an **RFM
customer segmentation** on the Online Retail II dataset (discovery → cleaning
with cancellation pairing + a 297k-row reconciling audit → quintile RFM into 10
named, strategy-ready segments, K-Means-validated → executive + operative
interactive HTML dashboards → reproducible numbered scripts + README → public
GitHub repo).

Principles captured from how that project actually ran:
- Sequence-gated stages with the result shown before moving on.
- Decisions surfaced via `AskUserQuestion` with a recommendation (snapshot date,
  segment-count method, dashboard audience, visual style, repo visibility).
- Mandatory cleaning audit with exact row reconciliation.
- Reversal/cancellation pairing removes matched originals, not just the
  cancellation line.
- Dashboards: audience-split, mockups in multiple styles before building,
  self-contained interactive HTML as the default build.
- Reproducible numbered scripts + README in a fixed format; large reproducible
  artifacts kept out of git.

## v1.0 — triggering validated — 2026-06-17

Ran trigger tuning on a 20-query eval set (10 should-trigger, 10 tricky
near-misses sharing keywords like "dashboard", "clean", "xlsx", "segment",
"Power BI", "join"). Result: **20/20** — every data-project query triggered
(incl. casual and single-stage phrasings), every near-miss correctly did not.
Description left unchanged — already optimal on this set.

Note: the skill-creator's automated `run_loop` couldn't run here because the
headless `claude -p` CLI returns 401 in this environment; the test was run via
independent subagent judges instead (faithful proxy). Eval set saved at
`~/.claude/skill-workspaces/analytics-playbook/trigger_eval.json` — re-run with
the automated loop if/when CLI auth is available.

## v1.1 — 2026-06-30

Distilled from the second project: a **mortgage maximum-loan model** (held-out
target → cleaning with a reconciling audit → 6-way model benchmark →
HistGradientBoosting, pruned 12→4 features → validation vs the held-out actual →
executive + internal decks (PPTX + HTML) → reproducible scripts + README → public
GitHub repo). Changes:

- **Stage 0 is now "Frame & set up"** — the version-control decision (local repo +
  whether/what/visibility of a remote GitHub repo) is made up front; if the remote
  is deferred, Stage 5 revisits it. Prompted by setting up the repo only at the
  end last time.
- **Stage 3 gained a "feature provenance" check** — test whether a candidate
  predictor is actually a downstream *output* (predictable from other inputs) and
  exclude it if so; plus prune redundant proxies via permutation importance.
  Prompted by interest rate (≈−0.95 with credit score, 91–94% predictable → a
  bank-set price, excluded) and job/education turning out to be income proxies
  (12→4 features, equal accuracy).
- **Stage 4 generalised from "Dashboards" to "Outputs"** — first *ask the medium*
  (deck / dashboard / production script / combination); added full deck
  conventions (two audiences, exec ≤5 + appendix + exec-summary, contents/cover
  free, PPTX **and** HTML) and build gotchas (embed scatter as PNG; syntax-check
  generated chart JS). Reference renamed `4-dashboards.md` → `4-outputs.md`.
- **Show the comparison, then decide** reinforced across stages — empirical
  evidence before a judgment call, and the basis recorded in a durable artifact.

Linked memory: `[[deck-deliverable-preference]]`, and the evidence-first principle
folded into `[[analytics-working-style]]`.

## v1.2 — 2026-06-30

Expanded Stage 4 **section C (production-ready modelling scripts)** in
`references/4-outputs.md`, from building one on the mortgage project (`score.py`):

- Lead with four up-front decisions (interface / I/O / validation / output).
- Concrete patterns: one core + thin wrappers; **feature contract as code**
  (missing column = fatal, bad value = per-row reject, never coerce);
  reject-with-reason + separate rejects file; **traceability** (model_version =
  artifact hash, scored_at, status) with **business policy kept out** of the model
  script; inference-only + pinned-runtime warning; built-in `--selftest`.
- **Observability** (prompted by a direct question this session): per-row errors
  travel with the *data*, not the log; operational + fatal messages go through one
  logger to stderr with an optional `--log-file`; fatals raise a **catchable error
  type** (not a bare `SystemExit`) and the CLI logs at ERROR + exits non-zero.
- **Naming:** consumer/inference scripts get a plain importable name (`score.py`),
  not a pipeline number — they sit outside the `01–05` reproduce-from-raw chain
  (and a module name can't start with a digit).

## v1.3 — 2026-06-30

Key-decisions table now leads with a **stage** column (`Stage N – Name`), rows
grouped by stage — updated `templates/README_template.md` and the Stage 5
reference (`references/5-repo-readme.md` §README, item 3). Prompted by the
mortgage project's decision log growing long (cleaning + feature + modelling +
output + production-script decisions) and becoming hard to scan without knowing
which stage each call belongs to.

## v1.4 — 2026-06-30

Stage 3 feature-provenance now says: **when you can't verify a feature is an
output, label the input-vs-output call a stated assumption, not a fact** — frame
the evidence as *consistent with* it and mirror that framing across every doc
(README, decision record, slides). Updated `references/3-method-selection.md` and
the `SKILL.md` Stage 3 summary. Prompted by the mortgage project: the rate being
"calculated in parallel with the max loan" is a reasonable read of the data but
isn't fact-checkable, and the docs initially stated it as settled fact.

## v1.5 — 2026-06-30

Distilled from **add-on work on the (closed) mortgage project**: a segment error
breakdown by income/credit band, and an out-of-distribution flag added to
`score.py`. Changes:

- **New "Extending a closed project" entry mode** (`SKILL.md` → Adapting). Add-on
  asks re-discover the existing pipeline first, then enter at Stage 3–4 and treat
  the shipped pipeline as **frozen** (new plainly-named scripts outside the
  numbered chain; don't touch `01–05` or the model). Prompted by two additive
  tasks layered on a delivered project without modifying it.
- **Alignment-assertion guardrail** (same section). When reconstructing data a
  saved artifact didn't store — here, recovering income/credit behind
  `predictions_test.csv` by replaying `03`'s deterministic split — **assert an
  invariant that proves alignment** (reconstructed target bit-identical to the
  saved `actual`) before any positional join. Prompted by needing to segment a
  predictions file that held only actual/predicted/residual.
- **Production scripts should carry a soft OOD / extrapolation flag**
  (`references/4-outputs.md` §C + `SKILL.md` Stage 4). The contract `RANGES` are
  wider than the training support, so a row can pass validation yet be an
  extrapolation; flag it (`ood_flag`/`ood_reason`, per-feature `[p1, p99]`
  envelope) from a small **committed** reference so the scorer stays inference-only.
  Prompted by adding exactly this to `score.py`.

Reinforced: **fixed, interpretable bands beat quantiles** when mirroring an existing
banded readout (income bands + FICO credit tiers here), and an empty band is a
finding worth keeping (the unobserved `<580` tier is what the OOD flag guards).

## v1.6 — 2026-06-30

**New Stage 5 — Cross-examination (Devil's advocate)**, inserted before the
repository stage; **Reproducible repository → Stage 6, Retrospective → Stage 7**
(pipeline diagram, stage headings, Stage 0's forward-reference, and the reference
file `5-repo-readme.md` → `6-repo-readme.md` all updated). Added
`references/5-cross-examination.md` (role-pattern library + side-task catalogue +
deliverable format). Prompted by the user wanting an adversarial review before
publish/closure.

The stage: ask which adversarial **role(s)** to adopt (CRO, CFO, Compliance,
Model Validation, CMO…), formulate role-specific challenges, answer each with a
verdict (resolved / open / mitigate), run cheap high-value **side validation
tasks**, and log it all in `CROSS_EXAMINATION.md`. Distilled live from a CRO
red-team of the mortgage model (over-lending tail, input elasticity, debt
partial-dependence — which *resolved* a flagged worry — and noise-degradation).

## v1.7 — 2026-06-30

Added a **"Resuming across sessions (context hygiene)"** note to `SKILL.md` →
Adapting: stages double as resume checkpoints (durable artifact + logged decision
per stage), so when context gets heavy, stop at a stage boundary, `/compact`
mid-stage or `/clear`/new-session at a boundary, and resume by pointing at the
artifacts. Prompted by a user question about mitigating large-context performance
drops mid-analysis.

## v1.8 — 2026-06-30

Added the **mortgage maximum-loan model** as a second **worked reference** in
`SKILL.md` (the section now holds two, retitled "Worked references"). It covers the
supervised-modelling → decks + production-script + cross-examination path that the
RFM example doesn't — held-out target, feature provenance, 12→4 parsimony, the
6-way benchmark, both deck audiences, `score.py`, and the CRO red-team. Prompted by
the section only citing RFM.

<!-- ## vNEXT — <date>
- <what changed> — prompted by <observation from the latest project>. -->
