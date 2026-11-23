# Feature Promotion Flow

Feature Promotion Flow (FPF) is a way of branching and releasing with Git. Each feature is built on its own branch, cut from `main`. Features are merged into `development` to be tested together. A release is assembled on `stage` from the features chosen for it, verified there, and promoted to `main`. Being on `development` says nothing about release: the release set is chosen, feature by feature.

This repository holds the guide to the method and a package of skills for an agent working by it.

## The guide

`site/index.html` is the guide: one web page with two tabs. The first is the flow on its own. The second is the flow in a project that keeps its record with Docket, a program from Lucidex Group that is not yet published. Open the file in a browser. Nothing has to be installed; the page loads its fonts from Google Fonts, and falls back to the system's own where it cannot.

The page is built from the files in `site/source/`:

```
python3 site/source/build.py
```

## The skills

`plugin/` is a package of six skills: the method, setting a project up, starting a feature, building to `development`, making a release, and making a hotfix. It is a Claude Code plugin:

```
/plugin marketplace add Lucidex-Group/feature-promotion-flow
/plugin install feature-promotion-flow@lucidex-feature-promotion-flow
```

Or copy the folders under `plugin/skills/` into your own skills folder. [plugin/README.md](plugin/README.md) says more. `python3 tools/package.py` writes the package as a zip.

## Working on this repository

This project is run by the method it describes. `main` is what is released, and `main`, `development` and `stage` change only by pull request. [CLAUDE.md](CLAUDE.md) holds the project's rules for an agent, and they serve a person as well. The tests are:

```
python3 tools/test.py
```

## Licence

Copyright (c) 2026 Lucidex Group. The guide and the skills are under CC BY 4.0, and the code is under the MIT License. See [LICENSE.md](LICENSE.md).
