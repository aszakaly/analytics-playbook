# Stage 5 — Cross-examination (Devil's advocate)

A structured adversarial review **before** the work is published (Stage 6). The
goal is to surface what a self-review misses by attacking the findings, model,
and decisions from a stakeholder's point of view — and to convert each weakness
into either a fix, a documented caveat, or a validation task.

## The flow

1. **Ask which role(s) to adopt** (`AskUserQuestion`, multi-select). The role
   determines the angle of attack — pick the ones with real authority over this
   decision. Common personas + what they press on:
   - **Chief Risk Officer** — robustness, failure modes, the dangerous-direction
     error (e.g. over-lending, false approvals), reliance on a single feature,
     what breaks on real/edge data.
   - **CFO** — P&L and capital: what the error band costs, mispricing exposure,
     ROI vs the status quo.
   - **Compliance / Fair-Lending / Legal** — protected-class proxies even when
     demographics are dropped, disparate impact, explainability / adverse-action
     reasons, inherited bias when the target is a past human decision.
   - **Model Validation (SR 11-7 style)** — leakage, overfitting, benchmark
     rigor, stated assumptions, reproducibility, monitoring & drift.
   - **CMO / commercial** — does the segmentation/score actually change an action;
     is the lift real and durable.
   - **COO / Operations** — can the output be operated: latency, data
     availability at decision time, exception handling.
2. **Formulate pointed, role-specific challenges** — short, sharp, falsifiable.
   Not "is the model good?" but "show me the over-lending tail, not symmetric
   error."
3. **Answer each honestly from the evidence**, and mark a **verdict**:
   `resolved` · `open (by-design / scope)` · `mitigate before production`.
   Don't whitewash — a real red-team finds real problems.
4. **Spin up side validation tasks** where a challenge can't be settled from
   what's on hand, and **run the cheap, high-value ones** now (you usually have
   the model + a predictions file already). Catalogue:
   - **Robustness / noise** — inject noise (k × feature-std); watch R²/MAE decay.
   - **Sensitivity / elasticity** — perturb a key input ±10/20%; measure the
     swing in the output (single-point-of-failure / gaming risk).
   - **Partial-dependence** — vary one feature, hold others; check the *learned*
     shape and sign (often **resolves** a "that coefficient looks wrong" worry —
     a marginal correlation can be a confound; the conditional effect is what the
     model uses).
   - **Error asymmetry** — split error into the costly vs benign direction (over-
     vs under-prediction); quantify the costly tail in absolute and % terms.
   - **Subgroup error** — break error down by band/segment to find pockets of
     poor performance (also a fairness lens).
   - **Leakage re-check / uncertainty** — re-confirm no target leak; add an
     out-of-distribution / extrapolation flag for per-decision confidence.
5. **Feed the outcome back** — fixes re-open the relevant earlier stage; residual
   risks become **prominent caveats** in the README and decision record; pre-
   production conditions are listed explicitly.

## Deliverable — `CROSS_EXAMINATION.md`

A challenge log: the persona(s), a table of **# · challenge · response & evidence
· verdict**, the side-validation tasks run (with numbers, reproducible by a
committed `*_checks.py`), and a **disposition** (resolved / mitigate-before-prod /
documentation caveats). State plainly whether anything blocks publication.

## Principles

- **Investigate, don't assume.** A challenge is a hypothesis — test it. Some will
  *strengthen* the work (a "wrong-looking" effect turns out correct once you hold
  confounders fixed); say so.
- **Cheap and high-value first.** Most side tasks reuse the saved model and a
  predictions file — minutes of work for real assurance.
- **Honest verdicts.** "By-design limitation" and "open scope gap" are valid,
  useful outcomes — capture them as caveats rather than hiding them.

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
