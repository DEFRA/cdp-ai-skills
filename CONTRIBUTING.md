# Contributing

How to add and maintain skills in `cdp-ai-skills`.

## What belongs here

- Skills useful to more than one service/team on CDP.
- Team-local skills for one service should stay in that service repository under `.claude/skills/` or `.agents/skills/`.

## Repository layout

Skills are grouped by owner:

- `skills/cdp/<skill>/` for platform team skills.
- `skills/<team>/<skill>/` for tenant team shared skills.

`<team>` and `<skill>` must be lowercase with hyphens.

## Add a new skill

1. Create `skills/<owner>/<skill>/SKILL.md`.
2. Add `references/` if needed for long guidance.
3. In `SKILL.md` frontmatter:
   - `name` must match `<skill>` exactly.
   - `description` must explain what the skill does and when to use it.
4. Run `python3 scripts/check-skills.py`.
5. Open a pull request.

The owner's plugin picks up every skill folder under `skills/<owner>/`, so `marketplace.json` needs no change.

## New team onboarding

When a team adds its first shared skill:

1. Add a plugin entry named `<team>` in `.claude-plugin/marketplace.json`, with `"skills": ["./skills/<team>/"]`.
2. Add a rule for `/skills/<team>/` to `.github/CODEOWNERS`, following the format in its comments.

## Writing guidelines

- Keep `SKILL.md` short and focused.
- Put large lists and detailed constraints in `references/`.
- Do not include secrets, private tokens, or environment-specific sensitive values.

## Testing locally

Each way below runs the skill from your clone, so edits apply in your next session without a push or `version` bump.

### Claude Code

Install the plugin from your clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/cdp-ai-skills
claude plugin install <plugin>@cdp-ai-skills
```

Run it as `/<owner>:<skill>` (for example `/cdp:prr`). If you added the GitHub marketplace before, remove it first
with `claude plugin marketplace remove cdp-ai-skills`.

### Copilot CLI

Install the plugin from your clone instead of GitHub:

```bash
copilot plugin marketplace add /path/to/cdp-ai-skills
copilot plugin install <plugin>@cdp-ai-skills
```

Run it as `/<owner>:<skill>` (for example `/cdp:prr`). If you added the GitHub marketplace before, remove it first
with `copilot plugin marketplace remove cdp-ai-skills`.

### Cursor and other tools

Replace the `gh skill install` copy with a symlink to your clone:

```bash
rm -rf ~/.agents/skills/<skill>
ln -s "$PWD/skills/<owner>/<skill>" ~/.agents/skills/<skill>
```

Use your tool's skills folder if it isn't `~/.agents/skills`. Run it as `/<skill>`. To go back, delete the link and run
`gh skill install` again.

## Releasing

- Bump the changed plugin `version` in `.claude-plugin/marketplace.json` in the same pull request. That bump is the
  release; there are no repository-wide release tags.

## Questions

Ask in Slack `#cdp-support`.
