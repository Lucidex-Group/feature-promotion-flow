---
name: fpf-release
description: "Make a release under Feature Promotion Flow. Use when the user names a release list or asks which features are eligible, when a feature on the list is merged into development, to build stage, to promote to main, or to release: checks the list against the bar for stage, builds stage from it by pull request, runs the whole suite there once, has stage checked by a fresh QA agent, promotes, tags, and brings development up to the release."
---

# Make a release

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded. These are steps 5 to 12 of the testing process in its table, which says what starts each one; the numbers below are the table's. The release list is the maintainer's choice: say what a feature lacks, and never choose.

## The strict standard

- Each feature's own tests and code review were done once, at the feature (the `fpf-build-to-development` skill). The release does not repeat them. It runs the whole suite once on what will ship, and has a fresh agent say what each scenario of the release has behind it.
- What is verified on `stage` is what ships; being merged into `development` proves nothing about the release.
- A `stage` with a known failure is never left standing or offered for promotion. Nothing is changed on `stage` itself.
- Promotion to `main` is on the maintainer's word only.

## The steps

**Before step 5: the release list.** The maintainer names the features the release is to hold, before the work where the maintainer can, and may change the list at any time. Keep it where the project's instruction file says, so that the maintainer and the agents read the same list; where that names no place, keep it as the maintainer gave it and say it back at each check. Ask which part of the version moves.

5. **Check the release list,** each time a feature on it is merged into `development`, and each time the list changes. It reads what is already written down and runs nothing. For each feature on the list:
   - it is merged into `development`;
   - it meets every line of "Eligible for `stage`" in the `fpf-build-to-development` skill;
   - it stands alone: for each other unreleased feature, `git rev-list $(git merge-base --all origin/feature/<a> origin/feature/<b>) --not origin/main` prints nothing, which says the two share no commit that is not already on `main`. A commit printed means one was cut from, or merged with, the other. Looking for merge commits alone does not show this: a feature cut from another holds its commits with no merge. Members of a coordination stay on their own branches and pass.

   Tell the maintainer either that every feature on the list has all of it, or which feature lacks what, and how much churn each feature's code review caused. A feature below the bar goes in only on the maintainer's word, given with what the feature lacked in front of the maintainer; QA reports what it lacked as not verified.
6. **Build `stage` from the list,** once every feature on it meets the bar, or is on it by the maintainer's word with what it lacks in front of the maintainer, and the maintainer has confirmed the list. Say what the maintainer's confirmation covers: the pull requests into `stage`, and every reset and rebuild of `stage` until it can be merged. Promotion is a separate word.
   - If `stage` holds anything `main` does not (`git fetch origin`, then `git rev-list --count origin/main..origin/stage` is not 0), reset it: `git push --force-with-lease origin origin/main:stage`.
   - Merge the features one by one, in the order they first went into `development`, each by its own pull request:
     ```
     gh pr create --base stage --head feature/<first> --title "Merge branch 'feature/<first>' into stage" --body "<what the feature is>"
     gh pr merge <number> --merge --subject "Merge branch 'feature/<first>' into stage" --body "Pull-request: <the pull request's URL>"
     ```
   - Never merge into `stage` on your own machine, never commit on it, and never merge `development` into it. No candidate is built anywhere first, and nothing is run until every feature is in.
   - A conflict is yours to resolve, by the `merge/…` branch in the `feature-promotion-flow` skill, and the merge resolves nothing else. It may be one that was never met on `development`: `stage` is the first place the list's features are together without the rest. A resolution recorded on `development` is replayed only in the clone that made it; from another clone, resolve it again. Features that only work together with a change to one of them are a coordination, and the change is made on the member's own branch.
7. **Run the suite on `stage`,** once every feature on the list is merged, and again only when `stage` has changed since. Take `stage` from GitHub without a local branch (`git fetch origin`, then `git switch --detach origin/stage`), confirm the commit, and run the project's whole suite on it, in whatever way is right for the project, such as on each platform it targets. Note the commit, and each command with its result. This is the one run of the whole suite, and it is mechanical: it does not matter that the agent running it built part of the release. Where the project has a tool that says, for each scenario, whether the tests that name it passed, use it and hand its results to QA.

   **Report the regression count with every run.** It is what shows that everything already released was tested again:
   - the scenarios whose tests ran and passed;
   - the scenarios whose tests were skipped, each named with the test. A skip is "not checked" for its scenario, never a pass. Where a skip came from the order of the commands or the machine, run that test again on the same commit and correct the run;
   - the scenarios no test names. The number is in the report every time; the names are kept with the run, and those new since the last release are called out to the maintainer.

   Say two limits with the numbers every time: a test that names a scenario is not thereby shown to check it, and a test that has been weakened is not seen. The count is made by a script the project keeps, never by an agent counting by hand. Where the project has no such script, or its tests do not name their scenarios, say that the count was not made and why, still name each skipped test, and put the script in the backlog.
8. **Have `stage` checked by a fresh agent. This is QA.** Start an agent for this release that has built nothing in the project, and give it the brief at the end of this skill, word for word, filling in only what it leaves open. It does not run the suite: it starts from step 7's commands and results. A short-lived agent stays out of any message file the project's agents share: it adds no row and keeps no watch. Post its name, its model and its report yourself, and answer for it. Say which checks were independent.
9. **If the suite or a scenario fails on `stage`, do not leave it standing, and do not wait for a separate word.** Record the failure against its feature, with the step that caught it and its kind. Then work toward a `stage` that can be merged:
   - Usually the feature comes off: reset `stage` to `main` (`git fetch origin`, then `git push --force-with-lease origin origin/main:stage`) and build it again from the features that remain (step 6).
   - Where the fault is small and the feature is fixed quickly, it is fixed on its own branch, tested (step 2), code reviewed where the fix is to a defect or a risk (step 3), merged into `development` again (step 4), and merged into `stage` again by pull request, on top of what is there; see "Resetting `development` and `stage`" in the `feature-promotion-flow` skill.

   Either way `stage` has changed, so the suite is run on it again (step 7). After a fix, QA checks again (step 8), by a fresh agent started again with the brief, only the scenarios of the feature that changed and what its fix touched. After a feature comes off, QA's results for the features that remain stand, and it is not run again unless the suite's new run fails. Tell the maintainer what came out or was fixed, and why. A feature the maintainer did not choose never goes in.
10. **Where QA observed something wrong that fails no scenario, put it to the maintainer** with QA's report. For each such observation the maintainer says: release as it is and put it in the backlog, or treat it as a failure (step 9). Where QA observed nothing of the kind, there is no step 10.
11. **Put QA's report in front of the maintainer and wait for the word to promote.** A scenario reported as partly verified or with no test does not block; it is in front of the maintainer at the decision. That word is acceptance, and it covers step 12.
12. **Promote and tag, and bring `development` level with the release.** The agent that assembled `stage` performs the promotion. Nothing is run:
    ```
    gh pr create --base main --head stage --title "Merge branch 'stage' into main" --body "<what the release contains>"
    gh pr merge <number> --merge --subject "Merge branch 'stage' into main" --body "Pull-request: <the pull request's URL>"
    git fetch origin
    git tag -a v<version>-pr<number>-<date> -m "<what the release contains>" origin/main
    git tag -a v<version> -m "<what the release contains>" origin/main
    git push origin v<version>-pr<number>-<date> v<version>
    ```
    The first tag is the version, the number of the pull request that promoted `stage`, and the date, such as `v0.6.0-pr142-2026-11-21`. The second is the bare version, for tools.

    Then `development`, which the maintainer's word to promote covers. Usually it is rebuilt. Note first which unreleased features are on it (`git log --merges --first-parent --format=%s origin/main..origin/development` lists the merges it holds that `main` does not); reset it; and merge each of those features again from its own branch by pull request, as in step 4 of the `fpf-build-to-development` skill, without testing or reviewing them again. Tell everyone, so that anyone with a copy takes it from GitHub again:
    ```
    git fetch origin
    git push --force-with-lease origin origin/main:development
    ```
    Where the project keeps `development` running across releases, merge `main` into it by pull request instead:
    ```
    gh pr create --base development --head main --title "Merge branch 'main' into development" --body "The release <version>"
    gh pr merge <number> --merge --subject "Merge branch 'main' into development" --body "Pull-request: <the pull request's URL>"
    ```
    A feature already tested is not sent back by the release; one still being built may pull `main`.

**Afterwards, `stage` stays as it is:** it holds what `main` holds. The cases for resetting either branch are under "Resetting `development` and `stage`" in the `feature-promotion-flow` skill.

## The brief for the QA agent

The agent that starts QA may have built part of the release, so it does not write the brief. It sends this, filling in only what is in angle brackets, and adds nothing of its own.

```
You are doing QA of a release on stage, for <project>, in <folder to work in>.
You were started by <name and model of the agent that started you>, which may have built part of this release. You have built nothing in this project. Take nothing about the release from that agent beyond this brief.

The commit to check is origin/stage at <commit>. Take it from GitHub (git fetch origin, then git switch --detach origin/stage) and confirm it is that commit. Never git pull on stage.

The project's whole suite has been run on that commit. These are the commands and their results, with the regression count: <each command with its result; the count; each skipped test and the scenario it guards>. A skipped test has not checked its scenario. Do not run the whole suite again. You may run a single test where reading it is not enough to say what it checks.

The scenarios to check: <all the scenarios the release names; or, after a fix, the scenarios of the feature that changed and what its fix touched, the rest standing from the check of the earlier commit>.

Do this:
1. Read what the release holds, and the scenarios each piece of work names: <where to read them>.
2. For each scenario to check, find the tests that name it and read them against the scenario's words. Give one result: verified by a test; partly verified, naming the part of the scenario the test does not check; no test found; checked by hand; or failed, saying what failed and what kind of fault it is (a defect, a risk, a missing or weak test, untrue wording). A passing suite is not a result for a scenario.
3. Check by hand, on what is built from stage, what the tests do not check, and say what you did and what you saw.
4. List each piece of work that names no scenario, with the reason it gives, or that it gives none.
5. Here is what each feature in the release has and lacks against the bar for stage: <the list>. Confirm each line against what you can read, and say where it is not borne out.
6. Say anything else you observe that the release's builders may have missed, and say which of it fails no scenario.

Fix nothing, commit nothing and push nothing. Do not write in any message file the project's agents share. Report to the agent that started you: the commit checked, the result for each scenario, what you checked by hand, and what you could not do.
```

Drawn from Lucidex Group's development standards, as they stood on November 24, 2026.
