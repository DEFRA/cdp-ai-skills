# Contributing

How to add and maintain skills in `cdp-ai-skills`.

## What belongs here

- Skills useful to more than one service/team on CDP.
- Not here: a skill only one service needs. Keep it in that service's repository (`.claude/skills/` or
  `.agents/skills/`).

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

Install as in the [README](README.md#install), but from your clone, so edits apply in your next session without a
push or `version` bump:

- **Claude Code or Copilot CLI plugin:** use the path to your clone in place of `DEFRA/cdp-ai-skills`, e.g.
  `claude plugin marketplace add ~/dev/cdp-ai-skills`. Remove the GitHub marketplace first if you added it.
- **Other tools:** symlink the skill folder from your clone, as in
  [Without GitHub CLI](README.md#without-github-cli), in place of the `gh skill install` copy.

## Releasing

- Bump the changed plugin `version` in `.claude-plugin/marketplace.json` in the same pull request. That bump is the
  release; there are no repository-wide release tags.

## Questions

Ask in Slack `#cdp-support`.
