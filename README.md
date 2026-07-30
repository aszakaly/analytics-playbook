# Analytics Playbook

A [Claude Code](https://claude.com/claude-code) skill that encodes a staged,
gated workflow for executing a data-analysis project end to end: frame the
question → profile the raw data → clean it with a full audit trail → choose and
defend a method → build the outputs (decks / dashboards / production scripts) →
red-team them from a stakeholder role → leave a reproducible repository → retro
that improves the playbook itself.

It exists so that any analytical project follows the same disciplined shape, so
the output is trustworthy, auditable, and repeatable.

- **In scope:** executing the analysis and the artifacts it leaves behind.
- **Out of scope:** raw data collection, model/output governance, and the later
  technical management or deployment of the output.

## What's in here

```
SKILL.md         the skill definition Claude reads — principles, the 8 stages, worked examples
CHANGELOG.md     versioned history of what changed in the playbook and why
references/      the detailed checklist for each stage (1 discovery … 6 repo/README)
templates/       reusable scaffolds — cleaning script, dashboard build script, README
```

See [SKILL.md](SKILL.md) for the pipeline diagram, the full stage-by-stage
walkthrough, and two worked examples (an RFM customer segmentation and a
supervised mortgage max-loan model) that bracket the playbook's range.

## Installing

Copy or clone this folder into wherever your Claude Code client loads local
skills from — e.g. `~/.claude/skills/analytics-playbook` — keeping the directory
structure intact. `SKILL.md`'s frontmatter (`name` + `description`) is what
Claude uses to decide when to trigger the skill.

## Contributing

This playbook is meant to **learn** — Stage 7 (Retrospective) is a standing
invitation to propose edits after every project, and every fifth entry raises a
consolidation reminder the maintainer can act on or defer. See
[CHANGELOG.md](CHANGELOG.md) for how changes are recorded.

## License

MIT — see [LICENSE](LICENSE).
