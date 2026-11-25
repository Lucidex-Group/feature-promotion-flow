---
name: fpf-start-feature
description: "Start a feature under Feature Promotion Flow. Use when beginning any piece of work that is ready to be worked on in a project that uses FPF: checks the work is ready, cuts the feature or fix branch from main, named for its work, in a worktree of its own."
---

# Start a feature

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded. A hotfix has its own steps: the `fpf-hotfix` skill.

1. **Place the work before writing it down.** Before a work item or a story is created, read the use cases and stories the project already has, and place the new work under the one it belongs to; where none fits, say which is missing. The order is: the use case, then the story and its scenarios, then the work item. A quick note may be captured at once, but it sits under a story or says which use case is missing.
2. **Check the work is ready.** What is to be built is written down, with a story and scenarios where it is new behaviour; a fix names the scenario it restores, or adds one for the fault. If any of that is missing, the work is still backlog: write it first, or say what is missing, and cut no branch yet. A standing instruction to keep working does not change this.
3. **A story you write yourself is marked, where the story is kept, as written by an agent and not yet seen.** You may build it to `development`. It is not eligible for `stage` until the product owner has seen the story and agreed it. When a story and its scenarios are put to the product owner, they are a question of their own, asking that one thing, never folded into another question. New behaviour nobody has asked for is not built at all without a plan put to the user.
4. **Make sure no other agent holds the same work,** by whatever means the project has, and say what you expect it to take before changing anything.
5. **Cut the branch from `main` as it is on GitHub, in a folder of its own, named for the work:**
   ```
   git fetch origin
   git worktree add -b feature/<id>-<name> ~/Development/worktrees/<Project>/feature-<id>-<name> origin/main
   ```

   Use `fix/` in place of `feature/` where that is what the work is. If the work truly needs another unreleased feature, say so and let the maintainer decide.
6. **Turn on reuse of recorded resolutions** in this clone if it is not on: `git config rerere.enabled true`.
7. **Work in the feature's folder.** It is where the feature is built and tested. Commit there as often as you need to.
8. **Where a person wants to see the work, run the feature's build for them** from the feature's folder, before or after it is tested. Run it apart from anything released that is in use, with data of its own and never the real data, say how to reach it, and build it again when the code changes. It is what a developer does while working on a feature, and it is not a step of the testing process.

When the feature's code is written, go on with the `fpf-build-to-development` skill: the feature pulls `main` before it is first tested.

Drawn from Lucidex Group's development standards, as they stood on November 24, 2026.
