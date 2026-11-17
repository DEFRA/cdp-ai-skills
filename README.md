# cdp-ai-skills

AI agent skills for teams building services on CDP.

This repository uses the [Agent Skills](https://agentskills.io) format, so skills can be used in Claude Code, Cursor,
Codex, Gemini CLI and other compatible tools.

## Skills

| Plugin | Skill | What it does |
|---|---|---|
| `cdp` | [`prr`](skills/cdp/prr/SKILL.md) | Self-check for CDP readiness before applying for a platform PRR |

The `prr` skill gives the same kind of code-level checks as the platform PRR (for example noisy-neighbour risk and
statelessness), but it is not a replacement for the platform PRR run in AWS by `cdp-prr-agent`.

Source: this tenant skill started as a copy of `cdp-prr-agent/src/skill/` and is now maintained separately for local
tenant self-check use.

## Use

### Claude Code

```bash
claude plugin marketplace add DEFRA/cdp-ai-skills
claude plugin install cdp@cdp-ai-skills
```

Then run `/cdp:prr` in your service repository.

Update later with:

```bash
claude plugin marketplace update cdp-ai-skills
```

### Cursor

Clone the repo and symlink the skill:

```bash
git clone https://github.com/DEFRA/cdp-ai-skills.git
ln -s "$PWD/cdp-ai-skills/skills/cdp/prr" ~/.cursor/skills/prr
```

Then run `/prr` in Cursor Agent chat.

Update later by running this in your `cdp-ai-skills` clone:

```bash
git pull
```

### Other agents

Copy or symlink the skill folder (with `references/`) into your agent's skills directory:

| Agent | Personal | Per repo |
|---|---|---|
| Claude Code | `~/.claude/skills/<skill>/` | `<repo>/.claude/skills/<skill>/` |
| Codex, Gemini CLI and others | `~/.agents/skills/<skill>/` | `<repo>/.agents/skills/<skill>/` |

Use `skills/<owner>/<skill>`, for example `skills/cdp/prr`.

## Install and auth notes

If this repository is internal, users need GitHub access to DEFRA repositories (via `gh auth login` or SSH) to clone
it and to install from Claude Code marketplace.

## Releases

Versions are bumped manually for now. Claude Code only updates an installed plugin when its `version` changes, so a
change merged without a bump never reaches users.

When a plugin changes:
1. Update that plugin's `version` in `.claude-plugin/marketplace.json` in the same pull request.
2. After merging, tag a release as `vX.Y.Z`.

Users receive updates by running `claude plugin marketplace update cdp-ai-skills` (Claude Code) or `git pull`
(Cursor/manual installs). Claude Code auto-update is off by default for third-party marketplaces unless users or admins
turn it on.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

```text
.claude-plugin/marketplace.json         Claude Code marketplace listing
skills/<owner>/<skill>/SKILL.md         frontmatter (name, description) and instructions
skills/<owner>/<skill>/references/      longer reference material
skills/<owner>/<skill>/assets/          optional templates and static files
skills/<owner>/<skill>/scripts/         optional helper scripts
```

The skill folder name must match the `name` in `SKILL.md` frontmatter (lowercase with hyphens).
