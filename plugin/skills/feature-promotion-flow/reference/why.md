# Why Feature Promotion Flow is shaped as it is

## What it separates

Most branching methods tie two decisions together: testing a feature with the others, and releasing it. Where features are cut from a shared `development` branch and merged back into it, whatever is on that branch is in the next release unless someone backs it out. Feature Promotion Flow separates the two. A feature is merged into `development`, where its conflicts with the others show, and that says nothing about release. The release is built separately, on `stage`, from the features the maintainer lists for it, each merged from its own branch, and it is tested and checked there.

## Why features are cut from `main` and nowhere else

Git can merge a branch into any other branch it shares an ancestor with. A feature cut from `main` holds its own commits and what is released, so it can be merged into `development` and later into `stage` for release, and neither merge brings another feature's code along. A feature cut from `development` would carry every other feature on `development` into `stage` with it. That is the whole of what lets a release be chosen feature by feature.

## How the history says where work is

A commit does not record the branch it was made on, but a merge commit's title names the branch merged and the branch merged into, and every merge in this method is a real merge. So the history shows each arrival of a feature on `development` and on `stage`, and a promotion of `stage` carries those merges onto `main`. Only the branch merged says whose work arrived: a feature that pulls `main` makes a commit titled "Merge remote-tracking branch 'origin/main' into feature/…", which is a release arriving in the feature, not the feature arriving anywhere.

## Two standards

`development` is where features are merged, and nothing is run on it; `stage` is where the release is proved. Building to `development` is held to a fast standard and choosing for `stage` to a strict one, on purpose.

## Why the whole suite runs once, on `stage`

What is tested, where, and what starts each step is stated once, as a table of twelve steps, in the `feature-promotion-flow` skill under "The testing process". What follows is why it is as it is.

A step is taken when what starts it has happened, and not otherwise. A feature's own tests run when its code changes, and its code is reviewed once. Running the whole suite each time a feature lands on `development`, again on a copy of the release built on a machine, and again on `stage`, runs it several times on code that has not changed between runs. So nothing is run on `development`; no copy of the release is built and tested before `stage`; the whole suite runs once, on `stage`, and again only when `stage` changes; and QA reads each scenario against its tests and checks by hand, and does not run the suite.

*Every released scenario is tested again at every release.* Not every piece of work is worked on in every release, but the suite run on `stage` holds the tests of everything already released, so all of it is tested each time: the run on `stage` is the regression test of everything released. It is reported with a count of how far it reaches, and a skipped test has not checked its scenario. A test that names a scenario is not thereby shown to check it, and a weakened test still passes; the count says how far the suite reached, not how well each test checks.

*What it costs.* `stage` is the first place the release's features are together without the rest of `development`. A conflict or a failure between them is found there, by pull request and in the open, and not before. A resolution Git recorded when the features met on `development` is replayed on `stage` only in the clone that recorded it.

*Showing a release before it is built.* Where people need to see a release running before `stage` is built, `development` can be reset to `main` and rebuilt from the release list, each feature by its own pull request. That is one of the cases under "Resetting `development` and `stage`" in the skill. Nothing in the testing process depends on it.

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
| The testing branch `next` is long-lived. Rewinding and rebuilding it after a release is optional. Only `seen` is throw-away. | `development` and `stage` are permanent. `development` is usually reset to `main` after a release, with the features still in progress merged again, and whenever items need to come out of it; `stage` when a feature fails on it, before a hotfix, and before a release is built on it if it holds anything `main` does not. | When either is reset, every surviving feature is merged again, so the same conflict can come up again: this is what reuse of recorded resolutions is for. |
| Topics graduate to `master` one at a time as each proves stable. `master` is the next release, not production. | A release list is built on `stage` and promoted as a whole. `main` is production. | `stage` is what is verified, because it is the only place the release exists together without the rest of `development`. Nothing is run on `development`; it shows only that the features merge. |
| "Merge to downstream only at well-defined points": do not merge the released line into a topic by habit, only for a good reason. | The released line reaches a feature at well-defined points: before it is first tested and as part of its merge into `development`, when the feature pulls `main`. | The same idea, with the point fixed. |

A feature never takes anything from `development` or `stage`, and a feature that has already been merged into either is never rebased. This agrees with Git's documentation, which says never to base work on a throw-away integration branch and not to rebase a topic that has already been merged elsewhere.

## What it does not cover

The method says nothing about database migrations, or about fixing an older version while a newer one is out. It does not say how a release is deployed, and its rollback assumes the previous release can be deployed again. It does not say where a project keeps its backlog, its decisions or its code reviews: that is the project's to state.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
