# The Git features the method uses

| Feature | Command | Where it is used |
| --- | --- | --- |
| Reuse of recorded resolutions (rerere) | `git config rerere.enabled true`, once per clone | Every merge into `development` and `stage`, and every merge made again after a reset: a conflict resolved once is not resolved by hand again. |
| Real merges | `git merge --no-ff`, and merge commits only on the Git host | Every merge of a feature, and the promotion of `stage`. The merge's title is how the history says where work has been. |
| Annotated tags | `git tag -a` | The release, on `main`: two tags on the same commit. |
| Safe overwriting | `git push --force-with-lease` | Resetting `development` or `stage` on the remote. Never a plain force. |
| Try a merge without doing it | `git merge-tree --write-tree <branch> <branch>` | A quick check that a release list merges, without building anything. Nothing in the steps depends on it. |
| First-parent history | `git log --first-parent main` | Reading `main` as one line per release. |
| A worktree per branch | `git worktree add`, with `git config worktree.useRelativePaths true` | A folder for each feature, so no two agents share a checkout. Relative paths need Git 2.48 or later. |
| Commit trailers | A line such as `Pull-request: <URL>` at the end of a message | The one line in the body of every merge made by pull request, so that the merge commit leads to its pull request. |

## Cautions

- **Recorded resolutions are kept per clone.** Every worktree of one clone shares them; another clone, on the same machine or another, does not have them. Git has no means of sharing them.
- **A worktree needs its own setup step in a fresh clone.** An agent starting there has to be told.

Drawn from Lucidex Group's development standards, as they stood on November 22, 2026.
