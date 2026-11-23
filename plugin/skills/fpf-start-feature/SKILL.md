---
name: fpf-start-feature
description: "Start a feature under Feature Promotion Flow. Use when beginning any piece of work that is ready to be worked on in a project that uses FPF: checks the work is ready, cuts the feature or fix branch from main, named for its work, in a worktree of its own."
---

# Start a feature

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded. A hotfix has its own steps: the `fpf-hotfix` skill.

1. **Check the work is ready.** What is to be built is written down, with a story and scenarios where it is new behaviour; a fix names the scenario it restores, or adds one for the fault. If any of that is missing, the work is still backlog: write it first, or say what is missing, and cut no branch yet. A standing instruction to keep working does not change this.
2. **A story you write yourself is marked, where the story is kept, as written by an agent and not yet seen.** You may build it to `development`. It is not eligible for `stage` until the product owner has seen the story and agreed it. New behaviour nobody has asked for is not built at all without a plan put to the user.
3. **Make sure no other agent holds the same work,** by whatever means the project has, and say what you expect it to take before changing anything.
4. **Cut the branch from `main` as it is on GitHub, in a folder of its own, named for the work:**
   ```
   git fetch origin
   git worktree add -b feature/<id>-<name> ~/Development/worktrees/<Project>/feature-<id>-<name> origin/main
   ```
   Use `fix/` in place of `feature/` where that is what the work is. If the work truly needs another unreleased feature, say so and let the maintainer decide.
5. **Turn on reuse of recorded resolutions** in this clone if it is not on: `git config rerere.enabled true`.
6. **Work in the feature's folder.** It is where the feature is built and tested. Commit there as often as you need to.

When the feature's own tests pass, go on with the `fpf-build-to-development` skill.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
