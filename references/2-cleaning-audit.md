# Stage 2 — Data cleaning + mandatory audit trail

Two deliverables, always: the **cleaned dataset** and an **audit file** of
everything removed/changed/transformed. The audit is non-negotiable — it is
what makes the cleaning defensible and reversible in reasoning.

## Principles

- **One rule at a time, in a sensible order**, reporting the row impact of each
  step (a running funnel: rows in → rows out → reason).
- **Reconciliation must hold**: `clean rows + removed rows = raw rows`, exactly.
  Assert it in code; if it fails, stop and find out why.
- **Tag the first rule that catches a row** so each removed row appears once
  with an unambiguous reason (follow pipeline order).
- **Surface judgement calls as decisions**, not silent defaults. Common ones:
  - Reversals/cancellations: remove the cancellation line *and*, where it
    matches an original (same key fields), remove that original too — a
    reversed sale was never net activity. Confirm the matching keys.
    Orphan reversals (no original in-window) are still not real activity.
  - Nulls in a key dimension: drop vs impute vs keep-and-flag.
  - Out-of-scope rows (test accounts, internal, geographies): keep or drop —
    ask, and remember the answer.
- **Transformations count too.** If you recast types, normalise text, derive
  columns, or clip outliers, record *what changed* (column, old→new rule), not
  just deletions.

## Audit-capture pattern (pandas)

Capture removed rows with a step + reason as you go, then concatenate:

```python
removed_frames = []
def capture(rows, step, reason):
    r = rows[ORIG_COLS].copy()
    r.insert(0, 'RemovalStep', step)
    r['RemovalReason'] = reason
    removed_frames.append(r)

# example step: exact duplicates
dup_mask = df.duplicated(keep='first')
capture(df[dup_mask], 1, 'Exact duplicate row (source overlap or repeated line)')
df = df[~dup_mask]

# ... more steps, each: capture(df[mask], n, 'why') then df = df[~mask] ...

audit = pd.concat(removed_frames, ignore_index=True)
audit.to_csv('cleaning_audit_removed_rows.csv', index=False)
assert len(df) + len(audit) == raw_total, 'Row reconciliation MISMATCH!'
```

For **transformations** (not removals), log a parallel record: column,
rows affected, rule applied (e.g. "Customer ID cast float→int", "Country
trimmed/upper-cased", "Quantity clipped at p99.9").

## Output

- `*_clean.csv` (or parquet) — the cleaned data, plus any derived columns the
  analysis needs (e.g. a Revenue = qty × price column).
- `cleaning_audit_removed_rows.csv` — every removed row, tagged.
- A printed **audit funnel** so the user sees where rows went and can challenge
  any single rule (filter the audit by reason to inspect).

Runnable skeleton: `templates/clean_script_scaffold.py`.
