---
name: feature-promotion-flow
description: "The branching and release method, Feature Promotion Flow (FPF): which branches exist, what is cut from what, how merges are made, who may push what, and what each step of checking is called. Load before any Git command that changes anything (branch, commit, merge, push, pull request, reset, tag) in a project that uses FPF: one with `development` and `stage` branches, or whose instruction file says so. The other fpf- skills are its procedures."
---

# Feature Promotion Flow

A way of branching and releasing. Its procedures are skills of their own: `fpf-set-up-project`, `fpf-start-feature`, `fpf-build-to-development`, `fpf-release` and `fpf-hotfix`. The reasons for it, and its relation to Git's own workflow, are in [reference/why.md](reference/why.md).

This skill and its procedures are the process alone. A project may add to it in its own instruction file, and a tool the project uses may add a skill of its own. Where either says something different, it governs in that project.

**Where things are kept.** These skills say what is written down, reviewed, reported and decided. Where a project keeps its backlog, its decisions and its code reviews is in that project's instruction file.

A project uses Feature Promotion Flow when it has `development` and `stage` branches, or its instruction file says so. The maintainer can say it is not necessary for a particular project. There, none of this applies.

**Three words for who decides.** *The maintainer* decides what is released: chooses the release set, answers code review findings, gives the word to promote, and authorises resets, tags and repository settings. *The product owner* decides what is built: orders the backlog, agrees stories and scenarios, and accepts decisions about how the product behaves. *The user* is the person directing the work in the conversation: the one an agent asks, and whose word governs. On a project where one person holds all three, that person is the user, and an agent takes the user's word for each. Where a project names someone else as maintainer or product owner, that decision is theirs.

## The branches

- **`main`** is what is released. Nothing reaches it except a promoted `stage`; a hotfix reaches it the same way.
- **A feature** is `main` as it was when the feature was cut, plus the feature's code. Its folder holds everything needed to build and test it, and testing happens there.
- **`development`** receives features, to be tried together. It may be broken. Being on it does not mean a feature will be released.
- **`stage`** receives the release set the maintainer chose. What is verified there is what ships.

`development` and `stage` are permanent, created from `main` when the project starts. The branches are not environments, though in a project they may map to them.

Where a piece of work stands is read from the merges, not set by hand: which of `development`, `stage` and `main` hold its branch is a fact of the history. Before reporting that work is or is not released, check it there.

## Starting work

- **Work starts only from `main`,** a hotfix included. Never cut work from, or pull from, `development` or `stage`, and never merge `development` into anything.
- **Cut a branch only when its work is ready:** what is to be built is written down, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault. Until then the work is still backlog and has no branch.
- **Name the branch for its work:** `<kind>/<id>-<a few words>`, such as `feature/w-t3xa8-passkey-sign-in`. `<id>` is the work item's id in lower case where the project gives its work ids; where it does not, the few words alone. For work, the kind is `feature`, `fix` or `hotfix`. One piece of work to a branch. The two other kinds of branch, `coordination/…` and `merge/…`, hold only merges and no work.
- **Every feature is cut fresh.** Never cut a feature from another feature, and never merge one feature into another: a feature that carries another's commits cannot be chosen for a release without it.
- **Features that require each other** are the maintainer's to decide: wait for the first to be released, or tie them in a coordination. A coordination names its members, as many as require each other, and has a branch `coordination/<id>-<name>`, cut from `main`, that holds only merges of the members. The members are merged into it and tested together there. A fix is never written on the coordination branch: it is written on the member's own branch, and the member is merged into the coordination branch again, until they work together. The coordination branch is never merged into anything, and nothing is cut from it. The members go to `development`, `stage` and `main` one by one, each from its own branch and only with or after the members it requires. The steps are in [reference/coordination.md](reference/coordination.md).
- **A feature catches up with a release by pulling `main`** (`git fetch origin`, then `git merge origin/main`, in the feature), after each release and before it is merged into `stage`.

## Merging

- **`development`, `stage` and `main` change only by pull request.** Never commit on any of them, and never merge into any of them on your own machine. The one other write to `development` and `stage` is a reset to `main`. Feature branches are kept.
- **Merges are real merges. Never squash.** The title names the branch merged and the branch merged into (keep both names if you rewrite it), and the body's one line names the pull request:
  ```
  gh pr merge <number> --merge --subject "Merge branch 'feature/<id>-<name>' into development" --body "Pull-request: <the pull request's URL>"
  ```
- **Never use GitHub's "Update branch" or its conflict editor** on such a pull request. They merge `development` or `stage` into the feature.
- **Never rebase a feature that has already been merged somewhere.**
- **A copy of `development` or `stage` on your machine is for running and testing only.** Take it from GitHub without a local branch (`git fetch origin`, then `git switch --detach origin/<branch>`), which works whichever folder holds the local name. Never `git pull` on either: after a reset, a pull brings the old commits back. Reset one on GitHub the same way, with no local branch: `git push --force-with-lease origin origin/main:<branch>`.
- **Whoever meets a merge conflict resolves it,** and the merge is still made by pull request. Cut a branch from the receiving branch as it is on GitHub (`git fetch origin`, then `git switch -c merge/<feature id>-into-<branch> origin/<branch>`), merge the feature into it (`git merge --no-ff <feature> -m "Merge branch '<feature>' into <branch>"`), resolve the conflict there, push that branch and open the pull request from it. The feature itself is not changed. This branch is not work cut from `development` or `stage`: it holds one merge and exists to go back by pull request.
- **A merge resolves its conflict and nothing else.** Any other change features need in order to work together is written on a feature's own branch, never in a merge and never on `development` or `stage`, and the feature is merged again. Where such a change is only right with the other features present, those features require each other, and the answer is a coordination (under "Starting work").
- With `git config rerere.enabled true` in the clone, a conflict resolved once is replayed when the same feature meets it again.
- **GitHub may report a conflict that Git does not have,** when the two branches share more than one latest commit. Merging what was released into `development` after every release and hotfix prevents it (under "After a release or a hotfix"). If the `merge/…` branch has become routine, something has not been merged that should have been: say so.

## Who may do what without asking

- **Commit on your feature branch as often as you need to.**
- **For work the user has said to work,** push the feature branch, open its pull request into `development` and merge it.
- **Everything else on a Git host waits for the maintainer's word:** pull requests into `stage` and `main`, resets, tags and settings. The maintainer's word to build a release candidate covers its pull requests into `stage` and each reset and rebuild of `stage` until it can be merged. Promotion waits for its own word.
- Clear a shared branch with `git push --force-with-lease`, never a plain force.

## Two standards

Building to `development` is fast and choosing for `stage` is strict, on purpose: `development` can be broken so that things are working before they reach `stage`. The fast standard is in the `fpf-build-to-development` skill; the strict one is in the `fpf-release` skill.

## The words

Each word means one thing. "Review" on its own is not used: say plan review or code review.

| Word | What it is | When | Who does it |
| --- | --- | --- | --- |
| Plan | The files, the changes, their order, the risks and how the result will be verified. | Before building, where a wrong call would be costly after it is merged. | The agent that will build. Nothing is built until the user approves. |
| Plan review | A reading of the plan against the code. | When a plan needs further input or a second opinion. | A second agent, or a person, that did not write the plan. |
| Test | The feature's own tests and scenarios, run in the feature's own folder. | Before its code review, and whenever it changes. | The agent that built it. |
| Code review | A reading of the feature's own code and tests. | On the feature's branch, before it is first merged into `development`, and for a hotfix. Elsewhere, when the work needs a second opinion. | An agent that did not write the code. |
| Testing together | The features on `development` run together. | After a feature is merged into `development`. | Whoever merged it. |
| QA | The independent check of `stage`: the suite run there, and a result for each scenario the release set names. | After the release set is merged into `stage`, before promotion. | A fresh agent that has built nothing in the project. |
| Acceptance | The maintainer's word to promote `stage` to `main`. | After QA. | The maintainer. |

## When something fails

A failure belongs to a feature, wherever it is caught. Say which step caught it (the feature's own tests, the code review, testing together, the candidate, QA on `stage`) and what kind it is, by the six kinds of finding in the `fpf-build-to-development` skill. The feature goes back to its builder and is fixed on its own branch. Knowing the step and the kind is what shows, over time, which step catches what and what reaches `stage`.

## After a release or a hotfix

`main` is merged into `development` by pull request, and every feature still in progress pulls `main`. That pull request brings the release itself into `development`, which until then holds the released features only by their own separate merges; without it GitHub reports conflicts that are not there.

- A release is marked on `main` with two annotated tags on the same commit: `v<version>-pr<number>-<date>`, such as `v0.6.0-pr142-2026-11-21`, and the bare version, `v0.6.0`, for tools. The history of releases is read from these tags.
- A bad release already on `main` is rolled back in two steps: production is put back by deploying the previous release's tag again, which changes nothing in Git; then it is corrected by a hotfix. `main` is never reverted or rewritten directly.
- On GitHub, `main` cannot be force-pushed or deleted; `development` and `stage` cannot be deleted, are force-pushed only to reset them, and accept changes only from a pull request.

## Resetting `development` and `stage`

Both can be reset to `main` when that serves the work. This is guidance, not a list to apply by rote: say which case you see and why, and where it is not plain, ask. A reset is a push, so it is on the maintainer's word; the word to build a release candidate covers the resets of `stage` that the candidate needs.

Cases where a reset is usually right:

- **Something has to come out.** A feature on `development` is abandoned or broken and holding the others up; a feature has failed on `stage`.
- **A clean start is needed.** Before a hotfix, `stage` is reset so that the fix travels alone. Before a release set is assembled, `stage` is reset if it holds anything `main` does not.
- **The branch is to show one thing.** `development` is rebuilt from a release set so that people can see that candidate running.
- **The branch can no longer be trusted.** It has taken a merge it should not have, or so much has gone wrong on it that finding the cause costs more than building it again.

Cases where it is usually better left running:

- **After an ordinary release or hotfix.** `stage` already holds what `main` holds, and the released features are already on `development`.
- **While features on it are still being tried together.** Resetting `development` means merging each of them again.
- **When a small correction to a feature of the set is quicker and as safe.** The feature is fixed on its own branch and merged again by pull request, on top of what is there, where rebuilding the whole set would cost more than it protects. Nothing is ever changed on the branch itself.

After a reset, the features that should still be there are merged again, each from its own branch by pull request, and everyone is told, so that anyone with a copy takes it from GitHub again.

## Reading the history

A commit does not carry its branch's name, but a merge commit's title does, for both sides. Only the branch merged says whose work arrived. "Merge branch 'feature/w-t3xa8-x' into development" is that feature arriving on `development`. "Merge remote-tracking branch 'origin/main' into feature/w-t3xa8-x" is a release arriving in the feature, and says nothing about where the feature is. `git log --first-parent main` reads what was released.

## Folders

- Each feature an agent works on has a folder of its own: `~/Development/worktrees/<Project>/<kind>-<id>-<name>` (`git worktree`, with `git config worktree.useRelativePaths true`). Never share a checkout with another agent or the user.
- The project's own folder is the user's. An agent does not work in it.

The Git features the method uses, with what each does, are in [reference/git-features.md](reference/git-features.md). A project is set up for the method once, with the `fpf-set-up-project` skill.

Every step is plain Git.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
