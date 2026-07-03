# <Project Title>

<One-sentence description of the project and the dataset.>

---

## Purpose

<What the analysis is for. Lead with the headline finding — the single most
important, decision-relevant number.>

---

## Key steps

1. **Data discovery** — <what the raw data looked like, key issues found>.
2. **Data cleaning** — `01_clean_data.py` → cleaned data + full removal audit.
3. **<Analysis> modelling** — `02_<model>.py` → per-entity output (+ validation).
4. **Dashboards** — `build_dashboards.py` → interactive HTML (audiences).

---

## Key decisions

First column is the playbook stage the decision was made in (`Stage N – Name`);
group rows by stage so a long log stays scannable.

| Stage | Decision | Choice made | Why |
|---|---|---|---|
| <e.g. Stage 2 – Cleaning> | <e.g. reversal/cancellation handling> | <choice> | <reason> |
| <e.g. Stage 2 – Cleaning> | <e.g. missing-key handling> | <choice> | <reason> |
| <e.g. Stage 3 – Method> | <e.g. reference/snapshot date> | <choice> | <reason> |
| <e.g. Stage 3 – Method> | <e.g. method / segment count> | <choice> | <reason> |
| <e.g. Stage 4 – Outputs> | <e.g. output medium & style> | <choice> | <reason> |

---

## Pipeline

```
<raw input>
   │  01_clean_data.py
   ▼
<clean data>  ──►  <audit file>
   │  02_<model>.py
   ▼
<model output>
   │  build_dashboards.py
   ▼
dashboard_<audience>.html ...
```

Run order:

```bash
python3 01_clean_data.py      # → clean data + audit
python3 02_<model>.py         # → model output (+ validation)
python3 build_dashboards.py   # → dashboards
```

Requirements: <pandas, numpy, ...>. <How to obtain the raw data if not committed.>

---

## Methodology

<How the chosen method works, the parameters used, and how it was validated.>

---

## Files

| File | One-line description |
|---|---|
| `<raw>` | <source data — note if not committed and where to get it>. |
| `01_clean_data.py` | <cleans raw into tidy data + writes the removal audit>. |
| `02_<model>.py` | <computes the model/segments + validation>. |
| `build_dashboards.py` | <generates the interactive dashboards>. |
| `<model>_output.csv` | <per-entity result>. |
| `dashboard_*.html` | <the dashboards>. |
| `README.md` | This file. |
