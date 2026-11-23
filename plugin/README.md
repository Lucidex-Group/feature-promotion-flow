# Feature Promotion Flow: the skills

Six skills for an agent working in a project that uses Feature Promotion Flow, a way of branching and releasing with Git. They are the flow on its own: a project that keeps its record with a tool such as Docket adds that tool's own skill.

| Skill | When it is used |
| --- | --- |
| `feature-promotion-flow` | Before any Git command that changes anything. The method: the branches, what is cut from what, how merges are made, who may do what, and what each check is called. |
| `fpf-set-up-project` | Once, when a project starts or adopts the flow. |
| `fpf-start-feature` | Beginning a piece of work that is ready. |
| `fpf-build-to-development` | A feature's tests pass, a code review comes back, or `development` breaks. |
| `fpf-release` | Choosing a release set, building a candidate, assembling `stage`, promoting. |
| `fpf-hotfix` | A fix that cannot wait for the next release. |

## Installing

In Claude Code:

```
/plugin marketplace add Lucidex-Group/feature-promotion-flow
/plugin install feature-promotion-flow@lucidex-feature-promotion-flow
```

Or copy the folders under `skills/` into your own skills folder (`~/.claude/skills/`, or `.claude/skills/` in a project). Each release of the repository also carries this folder as a zip.

## What a project has to say for itself

The skills say what is written down, reviewed, reported and decided. They leave to each project's own instruction file where its backlog, code reviews, QA reports and decisions are kept, who the maintainer and product owner are, and how its tests are run. `fpf-set-up-project` lists them.

The skills name folders under `~/Development/worktrees/<Project>/` for the worktrees. Use another place if you prefer; what matters is one folder to a branch.

## Where they come from

The skills are drawn from Lucidex Group's development standards, and each says in its last line when. The guide to the method, with every figure, is the site in the same repository.

## Licence

Copyright (c) 2026 Lucidex Group. The skills are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0): use, adapt and share them, with credit to Lucidex Group. The full text is at <https://creativecommons.org/licenses/by/4.0/legalcode>.
