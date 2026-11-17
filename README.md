# cdp-ai-skills

AI agent skills for teams building services on CDP.

Skills use the open [Agent Skills](https://agentskills.io) format, so they work in any tool that supports it,
including GitHub Copilot, Cursor, Codex, Gemini CLI and Claude Code.

## Skills

| Owner | Skill | What it does |
|---|---|---|
| `cdp` | [`prr`](skills/cdp/prr/SKILL.md) | Self-check for CDP readiness before applying for a platform PRR |

The `prr` skill gives the same kind of code-level checks as the platform PRR (for example noisy-neighbour risk and
statelessness), but it is not a replacement for the platform PRR run in AWS by `cdp-prr-agent`.

Source: this tenant skill started as a copy of `cdp-prr-agent/src/skill/` and is now maintained separately for local
tenant self-check use.

## Install

Each skill is a folder at `skills/<owner>/<skill>`, for example `skills/cdp/prr`.

### Any tool, with GitHub CLI

[`gh skill`](https://cli.github.com/manual/gh_skill) (GitHub CLI 2.90 or later, in public preview) downloads a skill
from this repository into your tool's skills folder on your machine:

```bash
gh skill install DEFRA/cdp-ai-skills skills/cdp/prr --agent cursor --scope user
```

Set `--agent` to your tool, for example `github-copilot`, `cursor`, `codex`, `gemini-cli` or `claude-code`
(`gh skill install --help` lists them all). Leave it out to choose interactively. `--scope user` makes the skill
available in every repository. Start a new session so the tool picks up the skill.

### Claude Code plugin

Claude Code users can install the skills as a plugin from this repository's marketplace instead:

```bash
claude plugin marketplace add DEFRA/cdp-ai-skills
claude plugin install cdp@cdp-ai-skills
```

Plugin skills are prefixed with the plugin name, so `prr` runs as `/cdp:prr`.

### Without GitHub CLI

Clone the repository and link the skill folder, including `references/`, into your tool's skills folder. GitHub
Copilot, Cursor, Codex and Gemini CLI read `~/.agents/skills/`; Claude Code reads `~/.claude/skills/`.

```bash
git clone https://github.com/DEFRA/cdp-ai-skills.git
mkdir -p ~/.agents/skills
ln -s "$PWD/cdp-ai-skills/skills/cdp/prr" ~/.agents/skills/prr
```

## Use

Open your tool in the root of the service repository you want to check, then either ask in plain words ("run a PRR
self-check on this repo") or invoke the skill by name. The command differs by tool, for example `/prr` in Cursor,
`$prr` in Codex and `/cdp:prr` in Claude Code with the plugin.

## Update

- **GitHub CLI installs:** run `gh skill update prr`, or `gh skill update --all` for every skill. It compares your copy
  with `main`, so every change arrives, with or without a version bump.
- **Linked installs:** run `git pull` in your `cdp-ai-skills` clone.
- **Claude Code plugin:** run `claude plugin update cdp@cdp-ai-skills`, or in a session open `/plugin`, go to
  Marketplaces, select `cdp-ai-skills` and choose **Update marketplace**. Choose **Enable auto-update** there to get
  updates automatically. The new version loads in your next session, or after `/reload-plugins`.

## Releases

Versions are bumped manually for now. They only matter to Claude Code plugin installs: Claude Code updates an
installed plugin only when its `version` changes, so a change merged without a bump never reaches those users. GitHub
CLI and linked installs get every change on `main`.

When a plugin changes, update that plugin's `version` in `.claude-plugin/marketplace.json` in the same pull request.
Each plugin is versioned on its own, so there are no repository-wide release tags. Don't create any: `gh skill install`
installs from the latest tag when one exists, so a tag would freeze every new GitHub CLI install at that point.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout

```text
.claude-plugin/marketplace.json         Claude Code plugin marketplace listing (other tools don't need it)
skills/<owner>/<skill>/SKILL.md         frontmatter (name, description) and instructions
skills/<owner>/<skill>/references/      longer reference material
skills/<owner>/<skill>/assets/          optional templates and static files
skills/<owner>/<skill>/scripts/         optional helper scripts
```

The skill folder name must match the `name` in `SKILL.md` frontmatter (lowercase with hyphens).
