# Changelog — analytics-playbook

This skill is meant to **learn**. After each project (Stage 7 — Retrospective),
record what changed and why. Keep changes *general* — fix the underlying
principle, not just the one example that exposed it. Prefer explaining the *why*
to adding rigid MUST/NEVER rules.

How to evolve it:
- Update the relevant `SKILL.md` / `references/*` / `templates/*` file.
- Add a dated entry below: what changed, and the observation that prompted it.
- Write durable user preferences to memory (`feedback`/`project`) so they carry
  across projects, and link them from here if useful.
- **After every fifth entry, or when `SKILL.md` or a reference file passes ~8k,
  flag that a consolidation is due.** Acting on it is the maintainer's call; a
  deferral is recorded here as deferred. A consolidation that runs gets its own
  entry plus a `CONSOLIDATION_LOG` accounting for every merge and deletion.

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

**Triggering validated** the same day on a 20-query eval set (10 should-trigger,
10 near-misses sharing keywords like "dashboard", "clean", "xlsx", "segment",
"Power BI", "join"): **20/20**, description left unchanged. Run via independent
subagent judges because the headless `claude -p` CLI returned 401 here; eval set
at `~/.claude/skill-workspaces/analytics-playbook/trigger_eval.json`.

## v1.1 — 2026-06-30

Distilled from the second project: a **mortgage maximum-loan model** (held-out
target → cleaning with a reconciling audit → 6-way model benchmark →
HistGradientBoosting, pruned 12→4 features → validation vs the held-out actual →
executive + internal decks (PPTX + HTML) → reproducible scripts + README → public
GitHub repo).

- **Stage 0 became "Frame & set up"** — the version-control decision (local repo +
  whether/what/visibility of a remote) is made up front, revisited later if
  deferred. Prompted by setting up the repo only at the end last time.
- **Stage 3 gained the "feature provenance" check** — test whether a candidate
  predictor is actually a downstream *output* (predictable from other inputs) and
  exclude it if so; prune redundant proxies via permutation importance. Prompted
  by interest rate (≈−0.95 with credit score, 91–94% predictable → a bank-set
  price, excluded) and job/education turning out to be income proxies (12→4
  features, equal accuracy).
- **Stage 4 generalised from "Dashboards" to "Outputs"** — ask the medium first
  (deck / dashboard / production script / combination); added deck conventions
  (two audiences, exec ≤5 + appendix + exec-summary, contents/cover free, PPTX
  **and** HTML) and build gotchas (embed scatter as PNG; syntax-check generated
  chart JS). `4-dashboards.md` → `4-outputs.md`.
- **Show the comparison, then decide** reinforced across stages — empirical
  evidence before a judgment call, the basis recorded in a durable artifact.

Linked memory: `[[deck-deliverable-preference]]`, evidence-first folded into
`[[analytics-working-style]]`.

## v1.2 — 2026-06-30

Expanded Stage 4 **section C (production-ready modelling scripts)**, from building
`score.py` on the mortgage project: four up-front decisions (interface / I/O /
validation / output); one core + thin wrappers; **feature contract as code**
(missing column = fatal, bad value = per-row reject, never coerce);
reject-with-reason + separate rejects file; **traceability** (model_version =
artifact hash, scored_at, status) with **business policy kept out** of the model
script; inference-only + pinned-runtime warning; built-in `--selftest`.

- **Observability** (prompted by a direct question that session): per-row errors
  travel with the *data*, not the log; operational + fatal messages go through one
  logger to stderr with an optional `--log-file`; fatals raise a **catchable error
  type** (not a bare `SystemExit`) and the CLI logs at ERROR + exits non-zero.
- **Naming:** consumer/inference scripts get a plain importable name (`score.py`),
  outside the `01–05` reproduce-from-raw chain (and a module name can't start with
  a digit).

## v1.3 — 2026-06-30

Key-decisions table now leads with a **stage** column (`Stage N – Name`), rows
grouped by stage — `templates/README_template.md` + the repo/README reference.
Prompted by the mortgage project's decision log growing long (cleaning + feature +
modelling + output + production-script decisions) and becoming hard to scan
without knowing which stage each call belonged to.

## v1.4 — 2026-06-30

Stage 3 feature-provenance now says: **when you can't verify a feature is an
output, label the input-vs-output call a stated assumption, not a fact** — frame
the evidence as *consistent with* it and mirror that framing across every doc
(README, decision record, slides). Prompted by the mortgage project: the rate
being "calculated in parallel with the max loan" is a reasonable read of the data
but isn't fact-checkable, and the docs initially stated it as settled fact.

## v1.5 — 2026-06-30

Distilled from **add-on work on the (closed) mortgage project** — a segment error
breakdown by income/credit band, and an OOD flag added to `score.py`:

- **New "Extending a closed project" entry mode** (`SKILL.md` → Adapting). Add-on
  asks re-discover the existing pipeline first, then enter at Stage 3–4 and treat
  the shipped pipeline as **frozen** (new plainly-named scripts outside the
  numbered chain; don't touch `01–05` or the model).
- **Alignment-assertion guardrail** (same section). When reconstructing data a
  saved artifact didn't store — here, recovering income/credit behind
  `predictions_test.csv` by replaying `03`'s deterministic split — **assert an
  invariant that proves alignment** (reconstructed target bit-identical to the
  saved `actual`) before any positional join. Prompted by needing to segment a
  predictions file that held only actual/predicted/residual.
- **Production scripts carry a soft OOD / extrapolation flag.** The contract
  `RANGES` are wider than the training support, so a row can pass validation yet be
  an extrapolation; flag it (`ood_flag`/`ood_reason`, per-feature `[p1, p99]`) from
  a small **committed** reference so the scorer stays inference-only.

Reinforced: **fixed, interpretable bands beat quantiles** when mirroring an
existing banded readout (income bands + FICO tiers here), and an empty band is a
finding worth keeping (the unobserved `<580` tier is what the OOD flag guards).

## v1.6 — 2026-06-30

**New Stage 5 — Cross-examination (Devil's advocate)**, inserted before the
repository stage; **Reproducible repository → Stage 6, Retrospective → Stage 7**
(diagram, headings, Stage 0's forward-reference, and `5-repo-readme.md` →
`6-repo-readme.md` all updated). Added `references/5-cross-examination.md` (role
library + side-task catalogue + deliverable format). Prompted by the user wanting
an adversarial review before publish/closure.

The stage: ask which adversarial **role(s)** to adopt (CRO, CFO, Compliance, Model
Validation, CMO…), formulate role-specific challenges, answer each with a verdict
(resolved / open / mitigate), run cheap high-value **side validation tasks**, and
log it all in `CROSS_EXAMINATION.md`. Distilled live from a CRO red-team of the
mortgage model (over-lending tail, input elasticity, debt partial-dependence —
which *resolved* a flagged worry — and noise-degradation).

## v1.7 — 2026-06-30

Added **"Resuming across sessions (context hygiene)"** to `SKILL.md` → Adapting:
stages double as resume checkpoints (durable artifact + logged decision per
stage), so when context gets heavy, stop at a stage boundary, `/compact` mid-stage
or `/clear`/new-session at a boundary, and resume by pointing at the artifacts.
Prompted by a user question about mitigating large-context performance drops
mid-analysis.

## v1.8 — 2026-06-30

Added the **mortgage maximum-loan model** as a second **worked reference** in
`SKILL.md` (section retitled "Worked references"). It covers the supervised-
modelling → decks + production-script + cross-examination path the RFM example
doesn't. Prompted by the section only citing RFM.

## v1.9 — 2026-07-30 — consolidation pass

Ten additive entries in, the playbook had accumulated the predictable failure
mode of an additive-only skill: `SKILL.md` restated most of what the reference
files already specified. This entry is a **reducing** pass — see
`CONSOLIDATION_LOG` below for every merge and deletion. Eight content changes
landed alongside it (changes 7 and 8 came out of review, which also settled the
final shape of change 5):

1. **Principle 1 rewritten: "Sequence is gated, not drip-fed."** The whole job is
   stated up front (question, decision + owner, audience, data + provenance/timing,
   likely method branch, definition of done, out of scope); gating is about
   *approval*, not withholding context. Prompted by the old wording being readable
   as "reveal the goal one stage at a time", which starves the early stages of the
   context they need to make good calls.
2. **Stage 0 now requires a written project-spec block** before Stage 1, as a
   table. Its *definition of done* and *out of scope* lines are the project's
   **scope guardrail** that later stages cite instead of carrying scope rules of
   their own (Stage 2's out-of-scope rows and "Adapting"'s depth-scaling now do
   exactly that).
3. **Stage 5 is explicitly not a correctness re-check.** Framing added at the head
   of both `SKILL.md` Stage 5 and `references/5-cross-examination.md`: the model
   already verifies its own work, so generic "double-check / re-verify / delegate
   verification to a subagent" instructions stay out of this playbook. Stage 5 is
   an adversarial review from a named stakeholder role producing a written Q&A
   artifact; anything settleable by re-running code belongs in Stage 2 or 3.
4. **New principle 6: "Deliverables are sized to the decision."** Cover the
   substance, don't pad; prefer a table or numbered decision list to prose; link
   rather than restate. This is the principle the consolidation itself applies.
5. **New Stage 7 size discipline.** Every additive edit pays rent (name the file
   it belongs in; apply principle 6 and link rather than restate). After every
   fifth changelog entry, or when `SKILL.md` or a reference file passes ~8k,
   Stage 7 **says a consolidation is due** and the user decides — deferral is a
   valid answer, recorded in the next entry as deferred, so the debt stays visible
   without becoming an obligation. A consolidation that runs gets its own branch
   and PR, keeps every worked example, hard number and stated reason a rule
   exists, and logs every merge and deletion with byte counts. Prompted by this
   pass — nothing previously made shrinking a scheduled event — and settled in
   review: the first draft forced a consolidation *instead of* an additive edit,
   which would make a retro withhold a genuine improvement to do housekeeping, and
   deleting is riskier than adding, so it wants a deliberate session rather than a
   due date. The rent rule is the load-bearing half; the reminder only makes drift
   visible.
6. **Description and objective generalised** for sharing beyond one user, with
   explicit skill-level scope (executing an analytics project) and out-of-scope
   (raw data collection, model/output governance, later technical management or
   deployment of the output).
7. **Stage 4's personal-brand reference became a brand slot** — "the user's own
   brand skill if they have one", with `akos-szakaly-brand` named once as an
   example of what fills it. Detail under *Deleted* below.
8. **Stage 1's lists declared a floor, not a ceiling** (`1-discovery.md`), with a
   generative rule — *what would make this column wrong, given its role in the
   grain?* — and a required output line stating **which checks were added beyond
   the lists, and why** ("none" is valid), where an added check must point at a
   decision Stage 2 will face. Prompted by the observation that an enumerated
   checklist reads to a model as a specification to satisfy, so the list had
   silently become a ceiling, and no list can anticipate an unseen dataset. This
   change is an **addition, not a consolidation** (+507 bytes): the fix is a
   generative rule plus an artifact requirement rather than more rows, because
   more rows would go stale and repeat the bloat this pass removed. The artifact
   requirement is doing the work — an exhortation to think past the list gets
   under-weighted, whereas a required line in the profile forces the question
   every time and puts the answer where a reader can judge it.

### CONSOLIDATION_LOG — v1.9

Byte counts, before → after:

| File | Before | After | Δ |
|---|---|---|---|
| `SKILL.md` | 14,617 | 14,328 | −289 |
| `README.md` | 2,525 | 2,046 | −479 |
| `references/1-discovery.md` | 2,139 | 2,646 | **+507** (addition, see change 8) |
| `references/2-cleaning-audit.md` | 2,787 | 2,771 | −16 |
| `references/3-method-selection.md` | 4,282 | 4,232 | −50 |
| `references/4-outputs.md` | 8,418 | 7,735 | −683 |
| `references/5-cross-examination.md` | 4,831 | 4,777 | −54 |
| `references/6-repo-readme.md` | 2,746 | 2,630 | −116 |
| **total** | **42,345** | **41,165** | **−1,180 (−2.8%)** |

`SKILL.md` absorbed ~3.1k of new text (principles 1 and 6, the Stage 0 spec
table, the Stage 5 framing block, the Stage 7 size discipline, the rewritten
description) and still came in under its baseline, so roughly 3.4k of duplication
came out of it.

`1-discovery.md` is the one file above its baseline, and it is an **addition, not
a failed consolidation** — content change 8. Consolidation alone took the in-scope
total to 40,103 (−5.3%); the two additions that came out of review — change 8
(+507) and change 5's final form (+471) — bring it to 41,165 (−2.8%).

**Merged**

- `SKILL.md` Stage 3 → the feature-provenance walkthrough (how to test
  recoverability, the assumption framing, mirroring it across docs) was a
  near-copy of `3-method-selection.md` §Feature provenance. `SKILL.md` now names
  the two load-bearing risks (provenance, held-out target) and points there.
- `SKILL.md` Stage 4 → the per-medium detail (deck slide caps, PPTX/HTML formats,
  operational-vs-executive dashboard content, the OOD-flag spec) duplicated
  `4-outputs.md` §§A–C. Reduced to one line per medium, which is all the gate
  needs.
- `SKILL.md` Stage 5 → the flow restated `5-cross-examination.md` steps 1–5;
  reduced to the gate sequence plus the deliverable.
- `SKILL.md` Stage 6 → the enumeration of the README's six sections duplicated
  `6-repo-readme.md` §README; replaced with a pointer plus the one fact worth
  hoisting (the key-decisions table is the most valuable section).
- `SKILL.md` Worked references → the mortgage entry's bulleted expansion of the
  CRO red-team duplicated the worked example in `5-cross-examination.md`; the two
  entries are now one paragraph each, keeping the numbers that live nowhere else
  (297k-row audit, 10 named segments, held-out target, 12→4 features, R² 0.990 /
  MAE $21,966) and cross-referencing the red-team detail.
- `README.md` → the pipeline diagram was a verbatim copy of the one in `SKILL.md`;
  removed in favour of a link (an application of new principle 6).
- `1-discovery.md` → §Output and §What to carry forward both said "surface the
  decisions cleaning will need, then stop"; merged into one §Output.
- `5-cross-examination.md` → §Principles ("investigate, don't assume", "cheap and
  high-value first", "honest verdicts") each restated a flow step; folded into
  steps 2–4 and the section deleted. Persona descriptions tightened.
- `3-method-selection.md` → "sanity-check that group sizes are usable" merged into
  the business-readiness test as "needs a clear action attached and a usable size".
- `4-outputs.md` → §0 "Pick the output type" duplicated the Stage 4 gate in
  `SKILL.md`; deleted, with the reference now opening by pointing at the gate. The
  six-bullet chart catalogue became one prose line per intent (no items lost).

**Deleted**

- The **leakage re-check** side task in Stage 5 (`SKILL.md` and
  `5-cross-examination.md` §4) — a leakage question is settled by re-running the
  code, so under content change 3 it belongs in Stage 3, where provenance and
  target hold-out already live. The uncertainty/OOD half of that bullet is kept.
- `6-repo-readme.md` "Re-scan all six sections after any late addition" — a
  generic self-recheck. The substantive half (update *every* affected section, not
  just the appended one, because readers cross-check them) is kept.
- `6-repo-readme.md` "State this verification" — generic; the concrete requirement
  ("a fresh run must reproduce the reported figures") is kept.
- Principle 1's appeal to authority ("the user has been explicit about this…") —
  superseded by the rewritten principle.
- `CHANGELOG.md` → the separate "v1.0 — triggering validated" entry was folded
  into v1.0 as a paragraph (all facts kept: 20/20, the eval-set path, the 401 CLI
  workaround). Historical entries tightened in prose only — every change and every
  "prompted by" reason is preserved.
- **Personal-brand specifics in Stage 4** — the hardcoded palette and motif
  (cobalt/steel on graphite, mono uppercase eyebrows, drafted offset-frame cards,
  registration-cross + monogram, indexed mono labels) in `4-outputs.md`, and the
  unconditional `akos-szakaly-brand` invocation in `SKILL.md` Stage 4. Replaced by
  a **brand slot**: "the user's own brand skill if they have one", with the skill
  named once as an example of what fills it. Two reasons — content change 5
  generalises the skill, but Stage 4 still resolved to one person's identity (a
  reader without that skill hits a failed Skill call; a reader who follows the
  palette literally ships someone else's brand), and a brand skill is the source
  of truth for its own tokens, so restating them here was the same duplication
  this pass removed everywhere else.

**Deliberately kept**

- Every worked example and hard number: the 297k-row reconciliation, the debt
  partial-dependence confound (+0.275 marginal correlation was an income
  confound), the bit-identical split assertion, the interest-rate 91–94%
  recoverability, 12→4 features, R² 0.990 / MAE $21,966, the over-lending tail
  figures. These carry information a general sentence cannot.
- Artifact-specific checks, which are audit requirements rather than re-checks:
  the `kept + removed = raw` assertion, the alignment invariant, the fresh-run
  reproduction requirement, `--selftest`, and the render QA in `4-outputs.md`
  (rendering a deck to images and screenshotting a dashboard inspects an artifact
  the model cannot otherwise see — it is not a re-check of its own reasoning).
**Fixed in passing**

- `6-repo-readme.md` was still titled "Stage 5 — Reproducible repository", stale
  since the v1.6 renumber; now "Stage 6".
- The `CHANGELOG.md` header said retrospectives are Stage 6; corrected to Stage 7.

<!-- ## vNEXT — <date>
- <what changed> — prompted by <observation from the latest project>. -->
