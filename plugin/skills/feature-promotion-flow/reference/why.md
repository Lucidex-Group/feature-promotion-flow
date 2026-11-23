# Why Feature Promotion Flow is shaped as it is

## What it separates

Most branching methods tie two decisions together: testing a feature with the others, and releasing it. Where features are cut from a shared `development` branch and merged back into it, whatever is on that branch is in the next release unless someone backs it out. Feature Promotion Flow separates the two. A feature is merged into `development` to be tested with the others, and that says nothing about release. The release is assembled separately, on `stage`, from the features chosen for it, each merged from its own branch.

## Why features are cut from `main` and nowhere else

Git can merge a branch into any other branch it shares an ancestor with. A feature cut from `main` holds its own commits and what is released, so it can be merged into `development` for testing and later into `stage` for release, and neither merge brings another feature's code along. A feature cut from `development` would carry every other feature on `development` into `stage` with it. That is the whole of what lets a release be chosen feature by feature.

## How the history says where work is

A commit does not record the branch it was made on, but a merge commit's title names the branch merged and the branch merged into, and every merge in this method is a real merge. So the history shows each arrival of a feature on `development` and on `stage`, and a promotion of `stage` carries those merges onto `main`. Only the branch merged says whose work arrived: a feature that pulls `main` makes a commit titled "Merge remote-tracking branch 'origin/main' into feature/…", which is a release arriving in the feature, not the feature arriving anywhere.

## Two standards

`development` can be broken so that things are working before they reach `stage`. Building to `development` is held to a fast standard and choosing for `stage` to a strict one, on purpose.

## What it is related to

No published method has this exact shape or this name. Three come close:

| Name | Who | How it compares |
| --- | --- | --- |
| gitworkflow | The Git project's own method, in Git's manual: <https://git-scm.com/docs/gitworkflows>. Explained for other teams at <https://github.com/rocketraman/gitworkflow>. | The parent. Topic branches, integration branches a topic "graduates" through, throw-away integration, tagged releases. |
| Branch Per Feature | Adam Dymitruk, 2012: <https://dymitruk.com/blog/2012/02/05/branch-per-feature/>. In practice: <https://bitbashing.io/2015/02/10/bpf-in-practice.html>. | The closest. Every feature starts from the same commit, the released branch changes only at a release, the QA branch is rebuilt from scratch, and a release is assembled from the features that are ready. |
| FeiFlow | <https://dev.to/feiflow/feiflow-an-opinioned-git-branching-and-release-management-strategy-33l3> | Similar in one respect: an integration branch that is never merged anywhere and is recreated to clear it. |

Gitflow is the method it most often replaces. In gitflow, features are cut from `development` and merged back into it, so a feature on `development` is in the next release unless someone backs it out.

## Where it differs from Git's documentation

Only the differences that matter in practice.

| Git's documentation | Feature Promotion Flow | Why it matters |
| --- | --- | --- |
| A topic is forked from the oldest integration branch it will ever be merged into. Git keeps a maintenance branch, so fixes fork from there. | Everything forks from `main`. There is one released line. | Simpler. A project that must keep fixing an older release while a newer one is out would need a maintenance branch, which this method does not have. |
| The testing branch `next` is long-lived. Rewinding and rebuilding it after a release is optional. Only `seen` is throw-away. | `development` and `stage` are permanent. `development` is reset to `main` when items need to come out of it, which includes rebuilding it from a release set as a candidate; `stage` when a feature fails on it and before a hotfix. | When either is reset, every surviving feature is merged again, so the same conflict can come up again: this is what reuse of recorded resolutions is for. |
| Topics graduate to `master` one at a time as each proves stable. `master` is the next release, not production. | A release set is assembled on `stage` and promoted as a whole. `main` is production. | `stage` is what is verified, because it is the only place the release set exists together without the rest of `development`. A pass on `development` shows the features get along; it does not prove the release. |
| "Merge to downstream only at well-defined points": do not merge the released line into a topic by habit, only for a good reason. | The released line reaches a feature at one well-defined point: after each release, when the feature pulls `main`. | The same idea, with the point fixed. |

A feature never takes anything from `development` or `stage`, and a feature that has already been merged into either is never rebased. This agrees with Git's documentation, which says never to base work on a throw-away integration branch and not to rebase a topic that has already been merged elsewhere.

## What it does not cover

The method says nothing about database migrations, or about fixing an older version while a newer one is out. It does not say how a release is deployed, and its rollback assumes the previous release can be deployed again. It does not say where a project keeps its backlog, its decisions or its code reviews: that is the project's to state.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
