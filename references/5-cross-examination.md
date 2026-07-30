# Stage 5 — Cross-examination (Devil's advocate)

> Stage 5 is not a correctness re-check. The model verifies its own work
> already; generic "double-check", "re-verify", or "delegate verification to a
> subagent" instructions are deliberately absent from this playbook and should
> not be added back. Stage 5 is an adversarial review from a named stakeholder
> role (CRO, CFO, Compliance, Model Validation, CMO) whose output is a written
> Q&A artifact for a human reader: challenges to assumptions, framing, and
> fitness for the decision. If a challenge can be settled by re-running the
> code, it belongs in Stage 2 or 3, not here.

It runs **before** the work is published (Stage 6), and every weakness it finds
becomes a fix, a documented caveat, or a validation task.

## The flow

1. **Ask which role(s) to adopt** (`AskUserQuestion`, multi-select) — pick the
   ones with real authority over this decision. What each presses on:
   - **Chief Risk Officer** — failure modes, the dangerous-direction error
     (over-lending, false approvals), reliance on a single feature, edge data.
   - **CFO** — what the error band costs, mispricing exposure, ROI vs status quo.
   - **Compliance / Fair-Lending / Legal** — protected-class proxies even when
     demographics are dropped, disparate impact, explainability / adverse-action
     reasons, inherited bias when the target is a past human decision.
   - **Model Validation (SR 11-7 style)** — leakage, overfitting, benchmark rigor,
     stated assumptions, reproducibility, monitoring & drift.
   - **CMO / commercial** — does the score actually change an action; is the lift
     real and durable.
   - **COO / Operations** — latency, data availability at decision time,
     exception handling.
2. **Formulate pointed, role-specific challenges** — short, sharp, falsifiable.
   Not "is the model good?" but "show me the over-lending tail, not symmetric
   error." A challenge is a hypothesis, so investigate rather than assume: some
   will *strengthen* the work, and saying so is part of an honest review.
3. **Answer each from the evidence** with a **verdict**: `resolved` · `open
   (by-design / scope)` · `mitigate before production`. Don't whitewash — a real
   red-team finds real problems, and "by-design limitation" or "open scope gap"
   are valid outcomes to capture as caveats.
4. **Spin up side validation tasks** where a challenge can't be settled from what
   is on hand, and run the cheap, high-value ones now — most reuse the saved
   model and a predictions file, so they are minutes of work for real assurance.
   Catalogue:
   - **Robustness / noise** — inject noise (k × feature-std); watch R²/MAE decay.
   - **Sensitivity / elasticity** — perturb a key input ±10/20%; measure the
     swing in the output (single-point-of-failure / gaming risk).
   - **Partial-dependence** — vary one feature, hold others; check the *learned*
     shape and sign (often **resolves** a "that coefficient looks wrong" worry —
     a marginal correlation can be a confound; the conditional effect is what
     the model uses).
   - **Error asymmetry** — split error into the costly vs benign direction (over-
     vs under-prediction); quantify the costly tail in absolute and % terms.
   - **Subgroup error** — break error down by band/segment to find pockets of
     poor performance (also a fairness lens).
   - **Uncertainty** — an out-of-distribution / extrapolation flag for
     per-decision confidence.
5. **Feed the outcome back** — fixes re-open the relevant earlier stage; residual
   risks become **prominent caveats** in the README and decision record;
   pre-production conditions are listed explicitly.

## Deliverable — `CROSS_EXAMINATION.md`

The persona(s); a table of **# · challenge · response & evidence · verdict**; the
side tasks run, with numbers, reproducible by a committed `*_checks.py`; and a
**disposition** (resolved / mitigate-before-prod / documentation caveats) that
states plainly whether anything blocks publication.

## Worked example (mortgage max-loan model)

Persona: **Chief Risk Officer**. Six challenges; four side tasks run from
`model_final.joblib` + `predictions_test.csv`:
- over-lending tail — 49% sized above the bank limit, p95 +$68k, 3.4% >10% over →
  *mitigate* (conservative offset / review band);
- sensitivity — income elasticity ~1.4, credit ~2.5–2.9 → *mitigate* (input
  controls + uncertainty/OOD flag);
- debt partial-dependence — correct negative direction → **resolved** (the +0.275
  marginal correlation was an income confound);
- noise-degradation — +10% noise nearly doubles MAE → *mitigate* (real backtest).

See the project's `CROSS_EXAMINATION.md` + `cross_examination_checks.py`.
