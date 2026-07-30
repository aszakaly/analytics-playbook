# Stage 1 — Data discovery (detailed checklist)

Goal: understand the raw data's shape, grain, and quality **before** changing
anything, and surface the issues that will need decisions during cleaning.

If a data-profiling skill (e.g. `explore-data`) is available, run it and build
on its output rather than reinventing the profile.

## Table-level

- Row count, column count, file/sheet structure (multiple sheets? combine?).
- **Grain**: one row per *what*? (transaction line, order, customer, event…)
- Candidate primary key — is it actually unique?
- Date-range coverage; last-updated / freshness if relevant.
- Approximate size (matters for git, for embedding in dashboards later).

## Column-level

Classify each column: identifier / dimension / metric / temporal / text /
boolean / structural. For each:

- **Null rate** — flag >5% (warn), >20% (alert).
- **Distinct count & cardinality ratio** — flag low-cardinality surprises
  (an ID with few values) and high-cardinality surprises (a "category" with
  thousands).
- **Top/bottom values** — spot placeholders ("N/A", "TEST", 999999), default
  flooding, encoding inconsistencies (case, whitespace, "US"/"USA").
- Numeric: min/max/mean/median, percentiles, zero & negative counts.
- Dates: min/max, future dates, gaps.

## Quality red flags to call out explicitly

- Missing keys (e.g. null customer/user IDs) — how many, what % of revenue/volume.
- Reversals / cancellations / negative quantities or amounts.
- Non-product / admin / fee codes mixed into a product table.
- Duplicates — exact, and near-duplicates from source overlaps (e.g. two
  exports sharing a month).
- Distribution skew that will distort averages.

## Output

A clean profile (tables grouped by column type) **plus** a short, ranked list of
the specific decisions discovery has surfaced — e.g. "20% of rows have no
customer ID", "cancellations present", "Dec overlaps across two sheets". Those
become the gated choices in Stage 2. End the stage here and let the user react;
don't roll straight into cleaning.
