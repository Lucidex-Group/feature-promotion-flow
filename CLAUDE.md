# Feature Promotion Flow: project instructions

This project holds the guide to Feature Promotion Flow, which is one web page built by a script, and a package of skills for the flow. There is no application to run or deploy.

## How the project is run

- **The project uses Feature Promotion Flow, on its own, without Docket.** Load the `feature-promotion-flow` skill before any Git command that changes anything, and the `fpf-` skill for the step in hand. The skills are in `plugin/skills/`.
- `main`, `development` and `stage` change only by pull request, merged as real merges. The repository allows merge commits only.
- **GitHub enforces it with two rulesets.** `main`: no deletion, no force push, changes only by pull request, merged as a merge commit; no one may bypass it. `development` and `stage`: no deletion, changes only by pull request, merged as a merge commit; the repository's admins may bypass it, so that they can reset either to `main`.
- The project gives its work no ids, so a branch is named `<kind>/<a few words>`, and its folder is `~/Development/worktrees/feature-promotion-flow/<kind>-<a few words>`.
- **The project's whole suite** is `python3 tools/test.py`. It builds the site and checks that the page has no place named twice, no link that leads nowhere and no image missing, and runs the rules for switching tabs (`site/source/tabs.js`) with Node against the built page (the build itself fails if the Skills tab and `plugin/skills/` disagree); it checks that the tab built from Docket's guide stops the build, naming what it found, on a section, an in-app link or a part it does not know; and it checks the skills package: that it is a valid plugin, that every skill loads, that nothing in it leans on anything only its authors have, and that the zip can be made.
- **Where the work is kept.** What is to be built is written as an issue on GitHub, with its scenarios where it is new behaviour. A code review is reported on the feature's pull request into `development`. QA's report and the maintainer's acceptance are written on the pull request that promotes `stage` to `main`.
- Lucidex Group is the maintainer and the product owner.

## What is where

- `site/index.html` is the guide. It is built; do not edit it by hand. Build it with `python3 site/source/build.py`.
- The tabs, in order. `site/source/flow.py` is the flow on its own. `site/source/skills.py` is the Skills tab: the six skills of `plugin/skills/`, each with when it is used, what it does, its outline and its whole text, read from the skill files when the page is built; what each does and its title in plain words are written in `skills.py`, and the build stops if those and the package's skills disagree. `site/source/docket.py` is the flow in a project on Docket: it is built from the guide Docket carries, as the released program gives it at `GET /api/guide`, pinned for each Docket release in `site/source/docket-guide/<version>.json`. It maps Docket's parts, section ids and in-app links to this site's, keeps this site's own ids so saved links still lead there, adds what is this site's alone (the card pointing to the Docket tab, the repository line, the footer), and stops the build, naming what it found, on any part, section or link it does not know. To take in a new Docket release: pin its copy, set `VERSION` in `docket_app.py`, and bring the maps in `docket.py` up to it. `site/source/docket_app.py` is Docket itself, the application, with screenshots in `site/images/docket/`, Docket's own skills in summary, and "Get Docket": where to download each program, how to check it and how to run it the first time. `drawing.py` draws the first tab's figures, and `shared.py` holds figures and tables the first tab uses; the second tab's figures come drawn in Docket's guide. `figures.css` and `figures.js` are the guide's own styles and script; `shell.css` and `shell.js` are the header, the four tabs and the contents on the left; `tabs.js` holds how places are named in each tab and where each tab leads, apart, so that the suite can run it.
- The two guides to the flow follow each other section by section, and a section has the same name in both, so a reader can switch tabs and stay in the same place. The Skills and Docket tabs have sections of their own; switching to or from either goes to the same place where there is one, and otherwise to the overview.
- The screenshots in the Docket tab are of the released Docket program named in `docket_app.py` (`VERSION`), serving a made-up project written for the guide, with a remote of its own so that its work reads as pushed; never a real project's record. Each page is reached by clicking through the app, as a person would, not by typing an address. Retake them when Docket's pages change.
- Docket's programs are published as a release of this repository tagged `docket-<Docket's version>`, carrying the files of Docket's own release as release files, never committed. The guide's own releases keep their tags `v<version>`, so the two cannot be confused. What Docket's release holds, and what "Get Docket" says about it, is agreed with the agent that builds Docket.
- `plugin/` is the skills package, a Claude Code plugin, and `.claude-plugin/marketplace.json` makes the repository its marketplace. `tools/package.py` writes the package as a zip. The plugin's version, in `plugin/.claude-plugin/plugin.json`, moves with each release that changes the package.
- `.github/workflows/pages.yml` publishes `site/` to GitHub Pages, at https://lucidex-group.github.io/feature-promotion-flow/, each time `main` changes. It first checks that the committed `site/index.html` is the page the sources build, and publishes nothing if it is not.

## The rules are not changed here

The method is Lucidex Group's, and its rules are decided there. The skills and the guide state them. A change here may make them clearer, correct a mistake in how one is stated, or improve a figure. It does not change what a rule says. Where a skill, the guide and the method seem to disagree, say so in an issue.

## Writing

- Write for a reader who has not used the method: say what each thing is before using its name.
- Never refer to anything by a code or an identifier alone. Say what it is.
- Never present a made-up release, measurement or result as a real one. The tags, pull request numbers and branch names in the examples are illustrations of a format, and the same ones are used throughout: `v0.6.0-pr142-2026-11-21`, `feature/w-t3xa8-passkey-sign-in`.
- Nothing in the skills package may lean on anything a reader does not have: a private folder, a tool the package does not name, or one person's own instructions.
