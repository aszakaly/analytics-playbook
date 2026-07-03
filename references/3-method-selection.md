# Stage 3 — Analysis method selection

The goal is a method that is both **fit for the question** and **defensible**.
Don't silently pick one and compute — present the options, recommend, decide,
then validate.

## The decision pattern

1. **List the candidate methods** for the question, each with a one-line
   trade-off and when it's the right call.
2. **Recommend one** (or a hybrid) and say why, tied to the business goal.
3. **Get the choice** (`AskUserQuestion`).
4. **Settle the parameters that change results** — also as explicit choices,
   not defaults buried in code:
   - reference/snapshot dates,
   - score bins / quantiles,
   - number of clusters / segments,
   - thresholds, windows, weighting.
5. **Validate** with an independent cross-check where possible.

## Feature provenance — input or output? (for predictive models)

Before fixing the feature set, ask of each candidate predictor: **is this an
input the subject brings, or an output the institution produces?** A feature that
is itself a *result* of the process you're modelling (a price, an interest rate,
a risk grade, an internal score) leaks the decision and makes the model circular.

- **Test it.** Treat the suspect feature as a temporary target and predict it from
  the other inputs. If a model recovers it with high R² (or a correlation matrix
  shows it's near-mechanically tied to another feature), it carries little
  independent signal and is most likely a downstream output → **exclude it**.
- **Decide explicitly**, with the evidence, and record the call (a
  `MODEL_DECISION.md`-style note). Keep genuine inputs even when strong.
- **Label it an assumption when you can't verify it.** The test usually shows a
  feature is *consistent with* being an output (predictable from the others), not
  that the institution actually computes it that way. Record the input-vs-output
  call as a **stated assumption, not a fact** — and frame the evidence as
  *consistent with* it. Mirror that framing everywhere it appears (README, decision
  record, slides) so the documents don't contradict each other.
- **Hold the target out.** The ground truth must not appear in any cleaning,
  feature, training, or selection step — use it only as the final evaluation
  reference.

## Prune redundant proxies

After a first fit, run **permutation importance**. Features with ≈0 importance are
often just correlates of stronger ones (e.g. job/education tracking income). When
a **leaner feature set matches accuracy**, prefer it: it's simpler to explain and
govern, and dropping demographic proxies improves fairness defensibility. Show the
comparison (full vs reduced) rather than asserting.

## Recurring example: segmentation

- **Rule-based scoring** (e.g. RFM quintiles → named segments): interpretable,
  every segment maps to an action, count driven by the business framework.
  Best when the output must drive strategy.
- **Unsupervised clustering** (k-means etc. on scaled features): data-driven
  count via elbow/silhouette, but clusters need post-hoc interpretation and may
  not map cleanly to action.
- **Hybrid (recommended default)**: rule-based named segments as the
  deliverable, clustering as a *validation* that the segments reflect real
  structure (e.g. the elbow's k matching how the named segments aggregate).

## Validation cross-checks (pick what fits)

- Clustering: elbow (inertia) + silhouette to justify k, then cross-tab the
  data-driven clusters against the chosen scheme.
- Models: hold-out / cross-validation, baseline comparison, residual checks.
- Always sanity-check distributions and that group sizes are usable.

## Business-readiness test

Whatever the method, each output group/segment/score band should have a
**clear action attached**. If you can't say what someone would *do* with a
segment, the scheme isn't done. Carry an action/strategy per group forward into
the dashboards (operative dashboards need it explicitly).

## Output

- The per-entity result table (scores + assigned group), saved.
- A summary table per group: size, % of population, the key metrics, % of the
  outcome (e.g. revenue), and the attached action.
- A short, honest note on any caveat (a group that's actually two behaviours, a
  label spanning a wide range, etc.).
