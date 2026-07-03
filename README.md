# Analytics Playbook

A [Claude Code](https://claude.com/claude-code) skill that encodes a staged,
gated workflow for taking a raw dataset all the way to decision-ready
dashboards and a reproducible, documented repository — data discovery →
cleaning (with a full audit trail) → analysis method selection → dashboard
design & build → cross-examination → reproducible code + README → a
retrospective that improves the playbook itself.

It exists to make every analytical project follow the same disciplined shape,
so the output is trustworthy, auditable, and repeatable.

## What's in here

```
SKILL.md              the skill definition Claude reads (frontmatter + stage-by-stage instructions)
CHANGELOG.md           versioned history of what changed in the playbook and why
references/            detailed checklist for each pipeline stage (discovery, cleaning, method selection, outputs, cross-examination, repo/README)
templates/             reusable scaffolds — a cleaning script, a dashboard build script, a README template
```

## Installing

Copy (or clone) this folder into wherever your Claude Code client loads local
skills from — e.g. `~/.claude/skills/analytics-playbook` — keeping the
directory structure intact. `SKILL.md`'s frontmatter (`name` + `description`)
is what Claude uses to decide when to trigger the skill.

## The pipeline at a glance

```
0. Setup       → question, decision, audience, data + version control (local/GitHub)
1. Discovery   → profile shape / grain / quality BEFORE touching anything
2. Cleaning    → rule-by-rule, gated, with a full removal/transformation audit
3. Method      → present analysis options + recommendation; check feature provenance
4. Outputs     → pick medium (deck / dashboard / production script) → build for audience
5. Cross-exam  → adversarial review from a chosen role; document Q&A + side tasks
6. Repository  → numbered reproducible scripts + README (revisit GitHub if deferred)
7. Retro       → capture learnings back into THIS skill
```

Each stage has its own reference file with the detailed checklist — see
`SKILL.md` for the full walkthrough and two worked examples (an RFM customer
segmentation, and a supervised mortgage max-loan model) that bracket the
playbook's range.

## Contributing

This playbook is meant to **learn** — Stage 7 (Retrospective) is a standing
invitation to propose edits after every project. See `CHANGELOG.md` for how
changes are recorded.

## License

MIT — see [LICENSE](LICENSE).
