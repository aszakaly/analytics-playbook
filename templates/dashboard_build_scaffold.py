#!/usr/bin/env python3
"""
build_dashboards.py  —  interactive-HTML dashboard scaffold (Stage 4)

Generates self-contained HTML dashboards with the real data embedded as JSON,
so they open in any browser with no server. Inject data via placeholder
replacement (NOT f-strings) so CSS braces don't clash.

Input : the modelled output (e.g. <model>_output.csv) + any aggregates
Output: dashboard_<audience>.html
Requires: pandas
"""
import json
import pandas as pd

# ---- 1. prepare the data blob once ---------------------------------------
def build_data():
    df = pd.read_csv('model_output.csv')
    # group summaries, trend series, breakdowns, and (for operative) the full
    # record list. Keep it JSON-serialisable; round floats sensibly.
    data = {
        'meta': {},          # totals, dates, headline numbers
        'groups': [],        # per-segment/group summary + attached action
        'trend': [],         # [{period, value}, ...] if you have time series
        'records': [],       # full per-entity list for the operative table
    }
    return data

# ---- 2. shared style (use the chosen mockup's CSS verbatim) --------------
CSS = """ /* paste the approved mockup CSS here (scoped) */ """

# ---- 3. HTML templates with __PLACEHOLDERS__ -----------------------------
EXEC_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>__CSS__</style></head><body>
<!-- exec markup: KPIs, concentration, imbalance, trend, insight -->
<script>
const DATA = __DATA__;
// render KPIs/charts from DATA; wire the country/period filters to recompute.
</script></body></html>"""

OPS_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>__CSS__</style></head><body>
<!-- ops markup: group list, detail+action, filters, record table -->
<script>
const DATA = __DATA__;
// segment select -> detail + table; live search; column sort;
// Export button -> Blob CSV of the currently filtered records.
</script></body></html>"""

def render(tmpl, data_json):
    return tmpl.replace('__CSS__', CSS).replace('__DATA__', data_json)

def main():
    data_json = json.dumps(build_data())
    with open('dashboard_executive.html', 'w') as f: f.write(render(EXEC_HTML, data_json))
    with open('dashboard_operative.html', 'w') as f: f.write(render(OPS_HTML, data_json))
    print('Wrote dashboard_executive.html and dashboard_operative.html')

if __name__ == '__main__':
    main()
