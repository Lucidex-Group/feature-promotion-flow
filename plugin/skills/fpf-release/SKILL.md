---
name: fpf-release
description: "Make a release under Feature Promotion Flow. Use when the user defines a release target or asks which features are eligible, to build a release candidate, to assemble stage, to promote to main, or to release: says what is eligible, tests the chosen set as a candidate, merges it into stage by pull request, has stage checked by a fresh QA agent, promotes, tags, and brings development and open features up to the release."
---

# Make a release

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded. Do nothing here without the maintainer's word. The release set is the maintainer's choice.

## The strict standard

- Each feature's own tests and code review were done once, at the feature (the `fpf-build-to-development` skill). The release does not repeat them. It checks that the chosen set works together, that `stage` holds what was tested, and, by a fresh agent, what each scenario of the set has behind it.
- What is verified on `stage` is what ships; a pass on `development` proves nothing about the release.
- A candidate with a known defect is never left standing or offered for promotion. Nothing is changed on `stage` itself.
- Promotion to `main` is on the maintainer's word only.

## The steps

1. **Say which features are eligible, then confirm the release set.** For each feature on `development`, check the list "Eligible for `stage`" in the `fpf-build-to-development` skill, and that it stands alone: for each other unreleased feature, `git rev-list $(git merge-base --all origin/feature/<a> origin/feature/<b>) --not origin/main` prints nothing, which says the two share no commit that is not already on `main`. A commit printed means one was cut from, or merged with, the other. Looking for merge commits alone does not show this: a feature cut from another holds its commits with no merge. Members of a coordination stay on their own branches and pass. List the features with what each lacks, say how much churn each feature's code review caused, and ask which eligible ones are in the release, in a dialog of choices. Ask which part of the version moves. A feature below the bar goes in only on the maintainer's word, given with what the feature lacked in front of the maintainer; QA reports what it lacked as not verified.
2. **Say what the maintainer's confirmation covers:** the pushes of the features, the pull requests into `stage`, and every reset and rebuild of `stage` until it can be merged. Promotion is a separate word.
3. **Have each feature of the set pull `main` and push,** in its own folder: `git fetch origin`, `git merge origin/main`, then `git push origin feature/<id>-<name>`.
4. **Build a candidate on a machine and run the set together there.** `main` plus the set, merged in release order in a folder of its own and never pushed:
   ```
   git fetch origin
   git worktree add --detach ~/Development/worktrees/<Project>/candidate origin/main
   cd ~/Development/worktrees/<Project>/candidate
   for f in origin/feature/<first> origin/feature/<second>; do
     git merge --no-ff "$f" -m "Merge branch '${f#origin/}' into candidate" || break
   done
   ```
   Run the project's whole suite there on the assembled set, not after each merge, in whatever way is right for the project, such as on each platform it targets; and again whenever the set changes. A conflict between two features is resolved in the merge, as any conflict is, and the merge resolves nothing else, so that the same resolutions are replayed when the set is merged into `stage`. Features that only work together with a change to one of them are a coordination, and the change is made on the member's own branch. A feature that breaks the set is left out, or fixed on its own branch, code reviewed there and merged into `development` again, and the candidate is built again, as many times as it takes. Tell the user what came out and why. Where people need to see the candidate running, it can be built on `development` instead: see [reference/candidate.md](reference/candidate.md).
5. **Merge the set into `stage` one by one, in the same order, each by its own pull request:**
   ```
   gh pr create --base stage --head feature/<first> --title "Merge branch 'feature/<first>' into stage" --body "<what the feature is>"
   gh pr merge <number> --merge --subject "Merge branch 'feature/<first>' into stage" --body "Pull-request: <the pull request's URL>"
   ```
   Never merge into `stage` on your own machine, never commit on it, and never merge `development` into it. A conflict is yours to resolve, by the `merge/…` branch in the `feature-promotion-flow` skill.
6. **Check that `stage` is the candidate.** The merge commits differ, but the contents are identical when the same features were merged in the same order onto the same `main`:
   ```
   git fetch origin
   git rev-parse origin/stage^{tree}
   git rev-parse HEAD^{tree}        # in the candidate's folder
   ```
   If they differ, say so before QA starts and find out why.
7. **Have `stage` checked by a fresh agent. This is QA.** Start an agent for this release set that has built nothing in the project, and give it the brief at the end of this skill, word for word, filling in only what it leaves open. A short-lived agent stays out of any message file the project's agents share: it adds no row and keeps no watch. Post its name, its model and its report yourself, and answer for it. Say which checks were independent.
8. **If `stage` fails, do not leave it standing.** Usually the feature comes out: reset `stage` to `main` (`git fetch origin`, then `git push --force-with-lease origin origin/main:stage`) and go back to step 4 with the rest of the set. Where the fault is small and the feature is fixed quickly on its own branch, it may be merged again on top by pull request; see "Resetting `development` and `stage`" in the `feature-promotion-flow` skill. Either way `stage` is checked again, since it has changed, and none of this waits for a separate word. Tell the user what came out or was fixed, and why. A feature the maintainer did not choose never goes in.
9. **Put QA's report in front of the maintainer and wait for the word to promote.** A scenario reported as partly verified or with no test does not block; it is in front of the maintainer at the decision. That word is acceptance.
10. **Promote and tag.** The agent that assembled `stage` performs the promotion:
    ```
    gh pr create --base main --head stage --title "Merge branch 'stage' into main" --body "<what the release contains>"
    gh pr merge <number> --merge --subject "Merge branch 'stage' into main" --body "Pull-request: <the pull request's URL>"
    git fetch origin
    git tag -a v<version>-pr<number>-<date> -m "<what the release contains>" origin/main
    git tag -a v<version> -m "<what the release contains>" origin/main
    git push origin v<version>-pr<number>-<date> v<version>
    ```
    The first tag is the version, the number of the pull request that promoted `stage`, and the date, such as `v0.6.0-pr142-2026-11-21`. The second is the bare version, for tools.
11. **Bring the release into `development`,** by pull request; the maintainer's word to promote covers it:
    ```
    gh pr create --base development --head main --title "Merge branch 'main' into development" --body "The release <version>"
    gh pr merge <number> --merge --subject "Merge branch 'main' into development" --body "Pull-request: <the pull request's URL>"
    ```
12. **Bring every feature still in progress up to it,** in each feature's folder: `git fetch origin`, then `git merge origin/main`. Remove the candidate's folder (`git worktree remove`).
13. **`development` and `stage` usually stay as they are after a release.** `stage` holds what `main` holds, and the released features are already on `development`. Whether either should be reset is under "Resetting `development` and `stage`" in the `feature-promotion-flow` skill.

## The brief for the QA agent

The agent that starts QA may have built part of the set, so it does not write the brief. It sends this, filling in only what is in angle brackets, and adds nothing of its own.

```
You are doing QA of a release set on stage, for <project>, in <folder to work in>.
You were started by <name and model of the agent that started you>, which may have built part of this set. You have built nothing in this project. Take nothing about the set from that agent beyond this brief.

The commit to test is origin/stage at <commit>. Take it from GitHub (git fetch origin, then git switch --detach origin/stage) and confirm it is that commit. Never git pull on stage.

Do this:
1. Read what the set releases, and the scenarios each piece of work names: <where to read them>.
2. Run the project's whole suite on stage, in whatever way is right for the project, such as on each platform it targets. Note each command and its result.
3. For each scenario the set names, give one result: verified by a test; partly verified, naming the part of the scenario the test does not check; no test found; checked by hand; or failed, saying what failed and what kind of fault it is (a defect, a risk, a missing or weak test, untrue wording). A passing suite is not a result for a scenario.
4. Where the suite cannot exercise a scenario, check it by hand on stage, and say what you did and what you saw.
5. List each piece of work that names no scenario, with the reason it gives, or that it gives none.
6. Here is what each feature in the set has and lacks against the bar for stage: <the list>. Confirm each line against what you can read, and say where it is not borne out.
7. Say anything else you observe that the set's builders may have missed.

Fix nothing, commit nothing and push nothing. Do not write in any message file the project's agents share. Report to the agent that started you: the commit tested, each command with its result, the result for each scenario, and what you could not do.
```

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
