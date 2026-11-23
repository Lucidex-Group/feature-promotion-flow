---
name: fpf-hotfix
description: "Make a hotfix under Feature Promotion Flow. Use when a fix must reach production without waiting for the next release: cuts the hotfix from main, resets stage, and releases the fix alone through stage by pull request."
---

# Make a hotfix

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded. A hotfix takes the same road as a release, alone. It never goes straight to `main`.

1. **Confirm with the maintainer that this is a hotfix** and not a fix for the next release. If it is to correct a bad release already on `main`, production is put back first by deploying the previous release's tag again, on the maintainer's word; that changes nothing in Git, and the hotfix then corrects the release, where the fix may do no more than undo the bad change.
2. **Write down the fault:** what is wrong in production, and the scenario the fix restores or adds.
3. **Cut the hotfix from `main` as it is on GitHub, in a folder of its own:**
   ```
   git fetch origin
   git worktree add -b hotfix/<id>-<name> ~/Development/worktrees/<Project>/hotfix-<id>-<name> origin/main
   ```
4. **Reset `stage` to `main`,** on the maintainer's word, since it is a push:
   ```
   git fetch origin
   git push --force-with-lease origin origin/main:stage
   ```
   If a release was being assembled on `stage`, tell the user it is set aside by this and that its set is merged into `stage` again after the hotfix.
5. **Make the fix, test-first:** write the failing test, then the change. Run the project's tests in the hotfix's folder. Commit on the hotfix branch as often as needed.
6. **Have the fix's code reviewed** by an agent that did not write it, before it goes anywhere near `stage`, as in "The code review, before the first merge" in the `fpf-build-to-development` skill. Afterwards, say how much churn the code review caused and discuss it with the user. A hotfix is held to the same bar for `stage` as any feature.
7. **Open the pull request into `stage`,** on the maintainer's word, and merge it as a real merge with both branch names in the title:
   ```
   git push -u origin hotfix/<id>-<name>
   gh pr create --base stage --head hotfix/<id>-<name> --title "Merge branch 'hotfix/<id>-<name>' into stage" --body "<the fix>"
   gh pr merge <number> --merge --subject "Merge branch 'hotfix/<id>-<name>' into stage" --body "Pull-request: <the pull request's URL>"
   ```
   A conflict is yours to resolve, by the `merge/…` branch in the `feature-promotion-flow` skill, and still by pull request.
8. **Have `stage` checked by a fresh QA agent,** started for this hotfix, that has built nothing in the project, with the brief at the end of the `fpf-release` skill; the set is the one fix. There is no candidate to build first. If it fails, the fix is corrected on the hotfix branch and code reviewed there; `stage` is reset to `main` again, or the correction merged on top, as "Resetting `development` and `stage`" in the `feature-promotion-flow` skill guides; and it is checked again.
9. **Promote and tag,** on the maintainer's word, as in step 10 of the `fpf-release` skill.
10. **Afterwards, do steps 11 and 12 of the `fpf-release` skill:** `main` goes into `development` by pull request, and every feature still in progress pulls `main`. That pull request is how `development` gets the fix; the features on it stay where they are, and a conflict with one of them shows in that pull request and is yours to resolve.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
