#!/usr/bin/env python3
"""
01_clean_data.py  —  cleaning scaffold (analytics-playbook Stage 2)

Fill in the rule blocks for your dataset. The audit-capture + reconciliation
machinery is the part you should NOT remove: every removed row is tagged with a
step and reason, and `clean + removed == raw` is asserted.

Input : <RAW_FILE>
Output: <CLEAN_FILE>, <AUDIT_FILE>
Requires: pandas (+ openpyxl for .xlsx)
"""
import pandas as pd

RAW_FILE   = 'raw_data.xlsx'          # or .csv
CLEAN_FILE = 'data_clean.csv'
AUDIT_FILE = 'cleaning_audit_removed_rows.csv'
ORIG_COLS  = None   # set to the raw column list, or leave None to use all


def main():
    # ---- load (combine sheets/files if needed) ----
    df = pd.read_excel(RAW_FILE)       # or pd.read_csv / pd.concat([...])
    raw_total = len(df)
    cols = ORIG_COLS or list(df.columns)

    removed_frames = []
    audit_log = []

    def capture(rows, step, reason):
        r = rows[cols].copy()
        r.insert(0, 'RemovalStep', step)
        r['RemovalReason'] = reason
        removed_frames.append(r)

    def log(step, note=''):
        audit_log.append((step, len(df), note))

    log('0. Raw loaded')

    # ---- Step 1: exact duplicates ---------------------------------------
    mask = df.duplicated(keep='first')
    capture(df[mask], 1, 'Exact duplicate row')
    df = df[~mask]; log('1. Drop exact duplicates', f'-{int(mask.sum()):,}')

    # ---- Step 2: <reversals / cancellations> ----------------------------
    # Remove reversal lines AND their matching originals where one exists.
    # Confirm the matching keys with the user. (See references/2-cleaning-audit.md)
    # ... capture(...) ; df = df.drop(index=...) ; log(...)

    # ---- Step 3: <missing key dimension> --------------------------------
    # mask = df['key_id'].isna()
    # capture(df[mask], 3, 'Missing key id (cannot be used downstream)')
    # df = df[~mask]; log('3. Drop missing key id', f'-{int(mask.sum()):,}')

    # ---- Step 4..n: <other rules: out-of-scope codes, bad price/qty> ----

    # ---- transformations (log what changed, not just removals) ----------
    # e.g. df['key_id'] = df['key_id'].astype(int)   # cast float->int
    # e.g. df['Country'] = df['Country'].str.strip()  # trim whitespace
    # Record these in a parallel transformation log if material.

    # ---- save + reconcile ----------------------------------------------
    df.to_csv(CLEAN_FILE, index=False)
    audit = pd.concat(removed_frames, ignore_index=True) if removed_frames \
        else pd.DataFrame(columns=['RemovalStep', *cols, 'RemovalReason'])
    audit.sort_values('RemovalStep').to_csv(AUDIT_FILE, index=False)

    print('CLEANING FUNNEL')
    for step, rows, note in audit_log:
        print(f'  {step:<36}{rows:>12,}   {note}')
    assert len(df) + len(audit) == raw_total, 'Row reconciliation MISMATCH!'
    print(f'\nOK: {len(df):,} kept + {len(audit):,} removed = {raw_total:,} raw')
    print(f'Wrote {CLEAN_FILE} and {AUDIT_FILE}')


if __name__ == '__main__':
    main()
