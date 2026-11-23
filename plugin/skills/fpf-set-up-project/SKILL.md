---
name: fpf-set-up-project
description: "Set a project up for Feature Promotion Flow. Use once, when a project starts or when it adopts FPF: creates the development and stage branches from main, sets the repository to merge commits only, sets branch protection, sets up the clone, and says what the project's instruction file has to state."
---

# Set a project up

The method this belongs to is in the `feature-promotion-flow` skill; load it first if it is not loaded. Everything here is done once for a repository, except the last step, which is done once for each clone. The branches, the settings and the protection are changes on the Git host, so they are made on the maintainer's word.

Branch names are the standard ones. `<Project>` is the project's name.

1. **Confirm with the maintainer that the project is to use Feature Promotion Flow,** and that `main` holds what is released. If `main` holds work that is not released, say so first: both new branches start from it.
2. **Create `development` and `stage` from `main`, as it is on the Git host:**
   ```
   git fetch origin
   git push origin origin/main:refs/heads/development origin/main:refs/heads/stage
   ```
   Both are permanent. No local branch is made for either.
3. **Allow merge commits only.** Turn squash merging and rebase merging off, so that a pull request cannot be merged any other way. Do not require a branch to be up to date before merging: that would need `development` or `stage` merged into the feature. On GitHub:
   ```
   gh api -X PATCH repos/<account>/<project> -F allow_merge_commit=true -F allow_squash_merge=false -F allow_rebase_merge=false
   ```
4. **Set branch protection,** as a ruleset or as branch protection:

   | Branch | Protection |
   | --- | --- |
   | `main` | Force pushes blocked. Deletion blocked. Changes only from a pull request, from `stage`. |
   | `development`, `stage` | Changes only from a pull request. Deletion blocked. Force pushes allowed only to whoever resets them. |

   Where the host does not offer protection for the repository (GitHub does not, for a private repository on a free plan), say so plainly and write it in the project's instruction file: nothing then stops a direct push, and the rules hold only because whoever works there follows them.
5. **Write what the project has to say for itself** in its instruction file. The skills leave these to the project:
   - That the project uses Feature Promotion Flow, and who the maintainer and the product owner are where they are not the user.
   - Where the work is kept: the backlog, with the scenarios of each piece of work; the code reviews; QA's reports; and the decisions.
   - Whether the project gives its work ids, which decides how a branch is named.
   - What the project's whole suite is, and how it is run.
6. **Set up the clone.** Once for each clone, on each machine:
   ```
   git config rerere.enabled true
   git config worktree.useRelativePaths true
   ```
   The first makes Git replay a conflict already resolved. The second lets another machine that shares the files use the same worktrees. Each feature an agent works on then has a folder of its own under `~/Development/worktrees/<Project>/`.
7. **Check it.** `git fetch origin`, then confirm that `origin/development` and `origin/stage` are at the same commit as `origin/main`, and read the merge settings back from the host.

A project that already has work in progress on other branches is a different matter: each such branch has to be looked at for what it was cut from, since a branch cut from anything but `main` carries other work with it. Put that to the maintainer before changing anything.

Start the first piece of work with the `fpf-start-feature` skill.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
