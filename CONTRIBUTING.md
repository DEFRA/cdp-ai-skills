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
4. Add `./skills/<owner>/<skill>` to the matching plugin entry in `.claude-plugin/marketplace.json`.
5. Run `python3 scripts/check-skills.py`.
6. Open a pull request.

## New team onboarding

When a team adds its first shared skill:

1. Add a plugin entry named `<team>` in `.claude-plugin/marketplace.json`.
2. Add that team's skill paths to the plugin `skills` list.
3. Add a rule for `/skills/<team>/` to `.github/CODEOWNERS`, following the format in its comments.

## Writing guidelines

- Keep `SKILL.md` short and focused.
- Put large lists and detailed constraints in `references/`.
- Do not include secrets, private tokens, or environment-specific sensitive values.

## Testing locally

Replace your installed copy with a symlink to your clone, so edits apply from the next session without a release:

```bash
rm -rf ~/.claude/skills/<skill> ~/.copilot/skills/<skill>
ln -s "$PWD/skills/<owner>/<skill>" ~/.claude/skills/<skill>
ln -s "$PWD/skills/<owner>/<skill>" ~/.copilot/skills/<skill>
```

Run it as `/<skill>`. The `rm` removes only the `gh skill install` copies. The Claude Code plugin, if installed, lives
in `~/.claude/plugins/` and still runs the released version as `/<owner>:<skill>`. To go back, delete the links and
run `gh skill install` again.

### Claude Code plugin

```bash
claude plugin marketplace add /path/to/cdp-ai-skills
claude plugin install <plugin>@cdp-ai-skills
```

Run the skill by slash command (for example `/cdp:prr`). It refreshes only on a `version` bump.

### Cursor

Symlink your skill into Cursor's skill folder and run it from Agent chat.

## Releasing

- Bump the changed plugin `version` in `.claude-plugin/marketplace.json` in the same pull request. That bump is the
  release; there are no repository-wide release tags.

## Questions

Ask in Slack `#cdp-support`.
