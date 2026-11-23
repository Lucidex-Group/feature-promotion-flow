# Features that require each other: a coordination

Sometimes one feature cannot be built or tested without another that is not yet released. One answer is to wait: the second is cut once the first is released. The other is a coordination, which lets them be worked on together while each stays on its own branch. Which is the maintainer's to decide.

A coordination has two parts.

- *A name and a list of members:* the features that require each other, each with its own branch, and for each member the members it requires. It is kept wherever the project keeps its work, with why the members are tied and the test runs made with them together. It holds no work of its own.
- *A coordination branch.* It is cut from `main`, with a folder of its own, and it holds nothing but merges of its members:

```
git fetch origin
git worktree add -b coordination/<id>-<name> ~/Development/worktrees/<Project>/coordination-<id>-<name> origin/main
cd ~/Development/worktrees/<Project>/coordination-<id>-<name>
git merge --no-ff feature/<first> -m "Merge branch 'feature/<first>' into coordination/<id>-<name>"
git merge --no-ff feature/<second> -m "Merge branch 'feature/<second>' into coordination/<id>-<name>"
```

This is what Git's own manual calls a throw-away integration branch: "To test the interaction of several topics, merge them into a throw-away branch. You must never base any work on such a branch!" (<https://git-scm.com/docs/gitworkflows>). The Git project keeps one of its own, named `seen`.

The rules for it:

- **No work is committed on the coordination branch, and no fix is written there.** The work is done on the member's own branch, and the member is merged into the coordination branch again (`git merge --no-ff feature/<member>`), until the members work together; or the branch is rebuilt from `main`.
- **It is also the answer when a merge would need more than its conflict resolved.** A merge resolves its conflict and nothing else. Where two features only work together with a change to one of them (a test that counts what both add to, a name both chose, text one changes and another checks), that change belongs to no merge: the features are members of a coordination, and the change is made on the member's own branch.
- **It is never merged into `development`, `stage` or `main`,** and no feature is cut from it. The members reach `development` and `stage` one by one, each from its own branch, each by its own pull request.
- **A member's tests may pass only there.** A member that calls another member's code cannot pass in its own folder until the other is released. Its test run is made in the coordination branch's folder, and says that it was made there and names the commit of each member it was run with. That result stands in place of one from the member's own folder. If any member changes afterwards, the result is out of date and the tests are run there again.
- **A member goes into `development` or `stage` only with, or after, the members it requires,** in the order they require. Its passing result was earned with them present and holds only with them present.
- **The members may be released together, or held until they are ready.** That is the maintainer's choice of release set, as for any feature.
- **One agent may hold every member and the coordination branch.** Where several agents hold the members, one of them holds the coordination branch's folder, and the coordination says which.
- **It is temporary.** When every member has been released, the coordination is closed and the branch has done its work.
- **Conflicts between members are met here first.** With reuse of recorded resolutions on, a conflict resolved on the coordination branch is replayed when the members meet again on `development` and `stage`.

Three kinds of branch hold merges and no work of their own, and differ in where they end: the coordination branch, which is never merged anywhere; the candidate built to test a release set, which is never merged anywhere either; and the `merge/<feature id>-into-<branch>` branch made to resolve a conflict, which exists to be merged into `development` or `stage` by pull request.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
