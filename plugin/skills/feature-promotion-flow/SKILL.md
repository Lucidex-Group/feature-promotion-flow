---
name: feature-promotion-flow
description: "The branching and release method, Feature Promotion Flow (FPF): which branches exist, what is cut from what, how merges are made, who may push what, and what each step of checking is called. Load before any Git command that changes anything (branch, commit, merge, push, pull request, reset, tag) in a project that uses FPF: one with `development` and `stage` branches, or whose instruction file says so. The other fpf- skills are its procedures."
---

# Feature Promotion Flow

A way of branching and releasing. Its procedures are skills of their own: `fpf-set-up-project`, `fpf-start-feature`, `fpf-build-to-development`, `fpf-release` and `fpf-hotfix`. The reasons for it, and its relation to Git's own workflow, are in [reference/why.md](reference/why.md).

This skill and its procedures are the process alone. A project may add to it in its own instruction file, and a tool the project uses may add a skill of its own. Where either says something different, it governs in that project.

**Where things are kept.** These skills say what is written down, reviewed, reported and decided. Where a project keeps its backlog, its decisions and its code reviews is in that project's instruction file.

A project uses Feature Promotion Flow when it has `development` and `stage` branches, or its instruction file says so. The maintainer can say it is not necessary for a particular project. There, none of this applies.

**Three words for who decides.** *The maintainer* decides what is released: names the release list, answers code review findings, gives the word to promote, and authorises resets, tags and repository settings. *The product owner* decides what is built: orders the backlog, agrees stories and scenarios, and accepts decisions about how the product behaves. *The user* is the person directing the work in the conversation: the one an agent asks, and whose word governs. On a project where one person holds all three, that person is the user, and an agent takes the user's word for each. Where a project names someone else as maintainer or product owner, that decision is theirs.

## The branches

- **`main`** is what is released. Nothing reaches it except a promoted `stage`; a hotfix reaches it the same way.
- **A feature** is `main` as it was when the feature was cut, plus the feature's code. Its folder holds everything needed to build and test it, and testing happens there.
- **`development`** receives features, so that they are merged in one place and any conflict between them shows. No test is run on it. Being on it does not mean a feature will be released.
- **`stage`** receives the release list the maintainer named. What is verified there is what ships.

`development` and `stage` are permanent, created from `main` when the project starts. The branches are not environments, though in a project they may map to them.

Where a piece of work stands is read from the merges, not set by hand: which of `development`, `stage` and `main` hold its branch is a fact of the history. Before reporting that work is or is not released, check it there.

## Starting work

- **Work starts only from `main`,** a hotfix included. Never cut work from, or pull from, `development` or `stage`, and never merge `development` into anything.
- **Cut a branch only when its work is ready:** what is to be built is written down, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault. Until then the work is still backlog and has no branch.
- **Name the branch for its work:** `<kind>/<id>-<a few words>`, such as `feature/w-t3xa8-passkey-sign-in`. `<id>` is the work item's id in lower case where the project gives its work ids; where it does not, the few words alone. For work, the kind is `feature`, `fix` or `hotfix`. One piece of work to a branch. The two other kinds of branch, `coordination/…` and `merge/…`, hold only merges and no work.
- **Every feature is cut fresh.** Never cut a feature from another feature, and never merge one feature into another: a feature that carries another's commits cannot be chosen for a release without it.
- **Features that require each other** are the maintainer's to decide: wait for the first to be released, or tie them in a coordination. A coordination names its members, as many as require each other, and has a branch `coordination/<id>-<name>`, cut from `main`, that holds only merges of the members. The members are merged into it and tested together there. A fix is never written on the coordination branch: it is written on the member's own branch, and the member is merged into the coordination branch again, until they work together. The coordination branch is never merged into anything, and nothing is cut from it. The members go to `development`, `stage` and `main` one by one, each from its own branch and only with or after the members it requires. The steps are in [reference/coordination.md](reference/coordination.md).
- **A feature takes what is released by pulling `main`** (`git fetch origin`, then `git merge origin/main`, in the feature): before it is first tested, as the first thing in its merge into `development`, and whenever, while it is being built, it needs something that was released. A pull starts no test and no code review, and a release made after a feature was tested does not send it back, unless there is an issue: a conflict in the feature's code, or a change to the wording of a scenario it names.

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
- **GitHub may report a conflict that Git does not have,** when the two branches share more than one latest commit. Rebuilding `development` after a release, or merging what was released into it, prevents it (under "After a release or a hotfix"). If the `merge/…` branch has become routine, something has not been merged that should have been: say so.

## Who may do what without asking

- **Commit on your feature branch as often as you need to.**
- **For work the user has said to work,** push the feature branch, open its pull request into `development` and merge it.
- **Everything else on a Git host waits for the maintainer's word:** pull requests into `stage` and `main`, resets, tags and settings. The maintainer's confirmation of the release list covers its pull requests into `stage` and each reset and rebuild of `stage` until it can be merged. Promotion waits for its own word.
- Clear a shared branch with `git push --force-with-lease`, never a plain force.

## Two standards

Building to `development` is fast and choosing for `stage` is strict, on purpose: `development` is where features are merged, and `stage` is where the release is proved. The fast standard is in the `fpf-build-to-development` skill; the strict one is in the `fpf-release` skill.

## The testing process

This table is the one statement of what is tested, where, and what starts it. The procedures give the commands for each step and name the step by its number; where anything else disagrees with this table, the table is right. A step is taken when what starts it has happened, and not otherwise: nothing here is run again on code that has not changed.

Before the work, where possible, the maintainer names the release list: the features the release is to hold. It is kept where the project's instruction file says; where that names no place, the agent assembling the release keeps it as the maintainer gave it and says it back at each check.

| Step | Where | What starts it | Who | What is done |
| --- | --- | --- | --- | --- |
| 1. Pull `main` into the feature | The feature's branch | The feature's code is written and it is about to be tested for the first time. | The agent that built it | `main` as it is on GitHub is merged into the feature, so that it is tested on what is released. |
| 2. Test the feature | The feature's branch | The feature's code is written, or has changed since it was last tested. A pull does not start it. | The agent that built it | The code is committed, and the feature's own tests, those that name its scenarios, are run in its folder. |
| 3. Review the feature's code | The feature's branch | Its tests pass and its code has not been reviewed. Or a rework has fixed a defect or a risk. | An agent that did not write the code; the builder answers | The feature's own code and tests are read, and each finding is answered by its kind. Nothing is run. |
| 4. Merge the feature into `development` | `development` | Its tests pass and every finding is answered. Or a feature already there has been reworked. | The agent that built it | The feature pulls `main`, is pushed, and is merged by pull request. Nothing is run on `development`. |
| 5. Check the release list | Read from what is written down; nothing is run | A feature on the list has just been merged into `development`. Or the maintainer has changed the list. | The agent that merged the feature, or the one the maintainer told of the change; the maintainer owns the list | Each feature on the list is checked: it is on `development`, and it meets the bar for `stage`. The maintainer is told that all do, or which lacks what. |
| 6. Build `stage` from the list | `stage` | Every feature on the list meets the bar, or is on it by the maintainer's word with what it lacks in front of the maintainer, and the maintainer has confirmed the list. | The agent assembling the release | `stage` is reset to `main` if it holds anything `main` does not, and each feature is merged by pull request. No candidate is built anywhere first. |
| 7. Run the suite on `stage` | `stage` | Every feature on the list is merged into `stage`. Or `stage` has changed since the suite last ran on it. | The agent assembling the release. It is mechanical: no judgement is used | The project's whole suite is run on the named commit of `stage`, in whatever way is right for the project. Each command and its result is noted, and the run is reported with its regression count. This is the one run of the whole suite. |
| 8. QA | `stage` | The suite has passed on `stage`. | A fresh agent that has built nothing in the project | Each scenario is read against the tests that name it; what the tests do not check is checked by hand; a result is given for every scenario. It does not run the suite. |
| 9. A failure on `stage` | `stage` | Step 7 or step 8 reports a failure. | The agent assembling the release, without waiting; the feature's builder fixes | The failure is recorded against its feature. Usually the feature comes off and `stage` is rebuilt; a small fix may be merged on top. Then step 7 again, and step 8 for the feature that was fixed; after a feature comes off, QA's results for the rest stand. The maintainer is told what came out or was fixed, and why. |
| 10. What QA observed outside the scenarios | `stage` | QA's report names something wrong that fails no scenario. | The maintainer | The maintainer says: release as it is and put it in the backlog, or treat it as a failure (step 9). |
| 11. Acceptance | `stage` | QA has reported and every failure is dealt with. | The maintainer | QA's report is put in front of the maintainer, who gives the word to promote. It covers step 12. |
| 12. Promote | `main` | The maintainer's word. | The agent that assembled `stage` | `stage` is merged into `main` by pull request and tagged; `main` and `development` are brought level: usually `development` is rebuilt, reset to `main` with the features still in progress merged again; where it is left running, `main` is merged into it by pull request. Nothing is run. |

**Every released scenario is tested again at every release.** Not every piece of work is worked on in every release, but the suite run on `stage` holds the tests of everything already released, so all of it is tested each time. That is a feature of the method, and it is why the whole suite runs on `stage` and nowhere earlier. The regression count reported with the run says how far it reaches: the scenarios whose tests ran and passed, those whose tests were skipped, and those no test names.

Steps 1 to 4 are in the `fpf-build-to-development` skill; steps 5 to 12 are in the `fpf-release` skill; a hotfix takes them alone, in the `fpf-hotfix` skill.

What this leaves out, on purpose: nothing is run when a feature lands on `development`; no copy of the release is built and tested before `stage`; a feature does not pull again because a release happened; and QA does not run the suite. So `stage` is the first place the release's features are together without the rest of `development`, and a conflict or a failure between them is found there.

## The words

Each word means one thing. "Review" on its own is not used: say plan review or code review.

| Word | What it is | When | Who does it |
| --- | --- | --- | --- |
| Plan | The files, the changes, their order, the risks and how the result will be verified. | Before building, where a wrong call would be costly after it is merged. | The agent that will build. Nothing is built until the user approves. |
| Plan review | A reading of the plan against the code. | When a plan needs further input or a second opinion. | A second agent, or a person, that did not write the plan. |
| Test | The feature's own tests, those that name its scenarios, run in the feature's own folder. | Before its code review, and whenever its code changes. | The agent that built it. |
| Code review | A reading of the feature's own code and tests. | On the feature's branch, before it is first merged into `development`, and for a hotfix. Elsewhere, when the work needs a second opinion. | An agent that did not write the code. |
| The suite's run | The project's whole suite, run on `stage`, reported with its regression count. | Once the release list is merged into `stage`, and again only when `stage` changes. | The agent assembling the release. |
| QA | The independent check of `stage`: each scenario the release names read against the tests that name it, and checked by hand where they fall short, with a result for each. | After the suite has passed on `stage`, before promotion. | A fresh agent that has built nothing in the project. |
| Acceptance | The maintainer's word to promote `stage` to `main`. | After QA. | The maintainer. |

## When something fails

A failure belongs to a feature, wherever it is caught. Say which step caught it (the feature's own tests, the code review, the suite's run on `stage`, QA) and what kind it is, by the six kinds of finding in the `fpf-build-to-development` skill. The feature goes back to its builder and is fixed on its own branch. Knowing the step and the kind is what shows, over time, which step catches what and what reaches `stage`.

## After a release or a hotfix

After a release, `development` is usually rebuilt: reset to `main`, and every feature still in progress that was on it merged again, each from its own branch by pull request. By then most of what it holds is released, so a reset costs little, and a `development` left running for many releases gathers merges that GitHub reads as conflicts Git does not have. Where nothing unreleased was on it, the reset alone is the whole of it.

Where `development` is left running, and after a hotfix, `main` is merged into it by pull request instead. That pull request brings the release itself into `development`, which until then holds the released features only by their own separate merges; without it GitHub reports conflicts that are not there.

Either way, a feature still being built may pull `main` then; a feature already tested is not sent back by the release.

- A release is marked on `main` with two annotated tags on the same commit: `v<version>-pr<number>-<date>`, such as `v0.6.0-pr142-2026-11-21`, and the bare version, `v0.6.0`, for tools. The history of releases is read from these tags.
- A bad release already on `main` is rolled back in two steps: production is put back by deploying the previous release's tag again, which changes nothing in Git; then it is corrected by a hotfix. `main` is never reverted or rewritten directly.
- On GitHub, `main` cannot be force-pushed or deleted; `development` and `stage` cannot be deleted, are force-pushed only to reset them, and accept changes only from a pull request.

## Resetting `development` and `stage`

Both can be reset to `main` when that serves the work. This is guidance, not a list to apply by rote: say which case you see and why, and where it is not plain, ask. A reset is a push, so it is on the maintainer's word; the maintainer's confirmation of the release list covers the resets of `stage` that building it needs.

Cases where a reset is usually right:

- **Something has to come out.** A feature on `development` is abandoned, or its merge is in the others' way; a feature has failed on `stage`.
- **After a release, for `development`.** What it held is by then mostly released; it is reset to `main` and the features still in progress are merged again. The maintainer's word to promote covers it.
- **A clean start is needed.** Before a hotfix, `stage` is reset so that the fix travels alone. Before a release is built on it, `stage` is reset if it holds anything `main` does not.
- **The branch is to show one thing.** `development` is rebuilt from a release list so that people can look at that release wherever `development` is deployed. No test is run there.
- **The branch can no longer be trusted.** It has taken a merge it should not have, or so much has gone wrong on it that finding the cause costs more than building it again.

Cases where it is usually better left running:

- **`stage`, after a release or a hotfix.** It already holds what `main` holds.
- **`development`, where the project has a reason to keep it running across releases,** such as wanting to see what builds up on it. Then `main` is merged into it after each release.
- **While features on it are waiting for a release.** Resetting `development` means merging each of them again.
- **When a small correction to a feature of the release is quicker and as safe.** The feature is fixed on its own branch and merged again by pull request, on top of what is there, where rebuilding the whole release would cost more than it protects. Nothing is ever changed on the branch itself.

After a reset, the features that should still be there are merged again, each from its own branch by pull request, and everyone is told, so that anyone with a copy takes it from GitHub again.

## Reading the history

A commit does not carry its branch's name, but a merge commit's title does, for both sides. Only the branch merged says whose work arrived. "Merge branch 'feature/w-t3xa8-x' into development" is that feature arriving on `development`. "Merge remote-tracking branch 'origin/main' into feature/w-t3xa8-x" is a release arriving in the feature, and says nothing about where the feature is. `git log --first-parent main` reads what was released.

## Folders

- Each feature an agent works on has a folder of its own: `~/Development/worktrees/<Project>/<kind>-<id>-<name>` (`git worktree`, with `git config worktree.useRelativePaths true`). Never share a checkout with another agent or the user.
- The project's own folder is the user's. An agent does not work in it.

The Git features the method uses, with what each does, are in [reference/git-features.md](reference/git-features.md). A project is set up for the method once, with the `fpf-set-up-project` skill.

Every step is plain Git.

Drawn from Lucidex Group's development standards, as they stood on November 24, 2026.
