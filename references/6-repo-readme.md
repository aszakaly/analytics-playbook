# Stage 6 — Reproducible repository + README

The project must end as something anyone can re-run and understand, not a pile
of one-off cells.

## Reproducible code

- **Numbered, standalone scripts** that run top-to-bottom and regenerate every
  output from the raw input: `01_clean_data.py`, `02_<model>.py`,
  `build_dashboards.py`, etc.
- Each script: a module docstring (purpose, inputs, outputs, key decisions),
  config constants at the top (paths, dates, parameters), a `main()`, and a
  printed summary so a run reports its own numbers.
- **A fresh run must reproduce the reported figures** before the work is called
  done, with the audit + reconciliation assertions baked into the cleaning script.

## README (use `templates/README_template.md`)

Always include:

1. **Purpose** — what the analysis is for; lead with the headline finding.
2. **Key steps** — the stages, briefly.
3. **Key decisions** — a table of **stage → decision → choice → why** (snapshot
   date, cancellation handling, method, feature provenance, output medium, etc.),
   where the first column tags the playbook stage the decision was made in
   (`Stage N – Name`) and rows are grouped by stage. This is the most valuable
   section for a future reader; the stage tag keeps a long log scannable.
4. **Pipeline** — a small diagram + the exact run order and requirements.
5. **Methodology** — how the method works and how it was cross-checked.
6. **Files** — a one-line description of every file in the repo.

**Keep the README internally consistent.** When an artifact or output is added or
changed (a new production script, an extra deck, a dropped column), update *every*
affected section — Key steps, Key decisions, Pipeline, Files — not just the one
new section you appended. A reader cross-checks these against each other, so a
step or decision missing from the table reads as an omission.

## Git / GitHub (only if asked)

- Confirm first: **repo name, public vs private, what to exclude.** Publishing
  is outward-facing — get explicit sign-off.
- **Keep large, reproducible artifacts out of git**: gitignore raw data and big
  derived files (they regenerate from the scripts), and document where to get /
  how to regenerate them in the README. Keep small model outputs if handy.
- Watch GitHub's file-size limits (warn >50 MB, hard 100 MB). For a brand-new
  single-commit repo, slimming via amend + force-push is clean.
- Authenticate via the user's own credentials (e.g. `gh auth login` device
  flow); never enter tokens into fields yourself.
- End commit messages with the required Co-Authored-By trailer.
