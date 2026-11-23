---
name: fpf-build-to-development
description: "Finish a feature under Feature Promotion Flow: have its code reviewed and the findings answered, merge it into development by pull request, test it with the others, and rework it. Use when a feature's own tests pass, when a code review comes back, when a pull request into development shows a conflict, when development breaks, or when asked whether a feature is ready for stage."
---

# Build a feature to `development`, and make it ready for `stage`

The method these steps belong to is in the `feature-promotion-flow` skill; load it first if it is not loaded.

## The fast standard

- Work the user has said to work is built, code reviewed and merged into `development` without waiting for a plan to be approved. A standing instruction ("work the backlog") is enough. The exception is work where a wrong call would be costly after it is merged: new behaviour nobody has asked for, a change to a format or a schema that other features depend on, anything that cannot be undone, and anything that contradicts a recorded decision. That waits for a plan the user approves.
- Several agents may work at once, each on its own piece of work, its own branch and its own folder.
- A lower standard means `development` may be broken by features that worked alone. It does not mean placeholders, stubs or unfinished work.
- Say what the work is: built and on `development`. Do not call it verified.

## The code review, before the first merge

A feature is code reviewed on its own branch, and its findings answered, before it goes into `development`, so that it is merged once. A code review is required before a feature is eligible for `stage`.

1. **Run the feature's own tests and scenarios in its own folder.** They pass before anything else here.
2. **Have the code reviewed** by an agent that did not write it. A second model is better than a second session of the same one.
   - It reads the feature's own code and tests.
   - The reviewer first reads what is already settled: the project's decisions and the code reviews of earlier features. A finding already rejected is not raised again unless something has changed.
3. **Verify every finding against the source** before accepting it: the file and the line.
4. **Classify each finding yourself, and act on its kind.** The reviewer's own label, blocking or not, is not the classification.

   | Kind | What it is | What happens to it |
   | --- | --- | --- |
   | Defect | The code does not do what a scenario or a stated requirement says. | Fixed on the feature's own branch. |
   | Risk | The tests pass, but a wrong thing can happen: lost data, a race, an unsafe command. | Fixed, or put to the maintainer to accept as it is. |
   | Missing or weak test | A scenario, or part of one, that no test really checks. | Fixed where the scenario is otherwise unverified; otherwise noted, for QA to report. |
   | Untrue wording | A document, a message or a comment that says something untrue. | Fixed. It never holds a feature back on its own. |
   | Design or style | A preference about how the code is shaped, with no defect or risk in it. | Put in the backlog. It never holds a feature back. |
   | Wrong | The finding misreads the code or a convention of the repository. | Rejected with the evidence. A tie-breaker confirms it: any agent that neither wrote the code nor raised the finding, given the finding and the evidence. It is then listed for the maintainer with its reason, and the work moves on; it is not asked. |

   A finding put to the maintainer keeps the feature out of `stage` until the maintainer answers, to fix it or to accept it as it is.
5. **Report the code review:** the decision, and each finding with its kind and how it ended.
6. **Say how much churn the code review caused,** and discuss it with the user.

## Into `development`

1. **Merge by pull request,** never on your own machine. For work the user has said to work, this needs no asking:
   ```
   git push -u origin feature/<id>-<name>
   gh pr create --base development --head feature/<id>-<name> --title "Merge branch 'feature/<id>-<name>' into development" --body "<what the feature is>"
   gh pr merge <number> --merge --subject "Merge branch 'feature/<id>-<name>' into development" --body "Pull-request: <the pull request's URL>"
   ```
   If the pull request shows a conflict, it is yours to resolve, by the `merge/…` branch in the `feature-promotion-flow` skill: the merge resolves the conflict and nothing else.
2. **Test together:** run what `development` now holds. A break belongs to the feature that caused it and is fixed on that feature's own branch, or the feature is left out. It never holds up other features, and nothing is ever fixed by committing on `development`.

## Rework

Rework after a code review is made on the feature's own branch. Any agent may take it; say who wrote the feature and who reworked it.

A rework is code reviewed again only when it fixed a defect or a risk. That code review reads whether the fix closes the finding, and what the fix itself changed; it is not a second reading of the feature. Rework for a test, for wording, or for a backlog item is not reviewed again. A feature that was already on `development` is merged into it again by pull request; `development` is not reset for it.

## Eligible for `stage`

A feature is eligible only when all of these hold. Say what a feature lacks; never choose the release set.

- Its work names its scenarios, or says why it has none; naming none, with no reason, does not meet this. Its tests pass in the feature's own folder for the code as it stands: a run made before the code last changed does not count, and the tests are run again.
- Its code has been reviewed by an agent that did not write it, and each finding has been dealt with as its kind requires.
- It has pulled `main` since the last release.
- It stands alone: it holds no other unreleased feature's commits.
- No open defect is known against it.
- Every decision it rests on is accepted by the product owner, and any story an agent wrote for it has been seen and agreed by the product owner.

A member of a coordination whose tests cannot pass alone is eligible on a passing run from the coordination branch's folder, naming the commit of each member it was run with, when no member has changed since. It is chosen only with, or after, the members it requires.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
