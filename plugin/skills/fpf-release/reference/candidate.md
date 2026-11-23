# Test the release set before `stage` is built

The concern this answers: a feature is integrated twice. The features tried together on `development` are everything in progress, not the release set, so without this the set itself would first run together on `stage`, where taking a feature out means a reset and the pull requests again. Either of the two ways below runs the set together cheaply first. The candidate on a machine is the usual way; rebuilding `development` is for when people need to see the candidate running.

In both, each feature of the set has already pulled `main` and been pushed, so that the same commits are merged here and into `stage`.

## A candidate on a machine

`main` plus the set, merged in release order in a folder of its own and never pushed. `development` is not disturbed.

```
git fetch origin
git worktree add --detach ~/Development/worktrees/<Project>/candidate origin/main
cd ~/Development/worktrees/<Project>/candidate
for f in origin/feature/<first> origin/feature/<second>; do
  git merge --no-ff "$f" -m "Merge branch '${f#origin/}' into candidate" || break
done
```

Run the project's whole suite there. A feature that breaks the set is left out and the candidate is built again. Remove the folder when `stage` has been verified (`git worktree remove`).

## The candidate on `development`

This is a case of items needing to come out of `development`: everything outside the set. `development` is reset to `main`, on the maintainer's word since it is a push, and the set is merged into it in release order, each feature by its own pull request as for any merge into `development`. The candidate can then be seen running wherever `development` is deployed. While it is there nothing else is merged into `development`, or it no longer matches the set. The features left out are merged into `development` again afterwards, from their own branches.

## Which

Rebuild `development` when the candidate needs to be seen running by people. Use the candidate on a machine when the automated suite is the test; it leaves `development` free for work in progress.

## Check that `stage` is the candidate

Once `stage` is built, compare the contents of the two. The merge commits differ, but when the same features were merged in the same order onto the same `main`, the trees are identical:

```
git fetch origin
git rev-parse origin/stage^{tree}
git rev-parse HEAD^{tree}                  # in the candidate's folder, or:
git rev-parse origin/development^{tree}
```

If the two match, a pass on the candidate is evidence about what `stage` holds, and QA on `stage` is its independent confirmation. If they differ, say so before QA starts and find out why: a feature changed in between, the order differed, or a conflict was resolved differently.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
