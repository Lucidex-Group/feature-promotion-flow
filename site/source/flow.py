"""Feature Promotion Flow on its own: the words, figures and tables for a project that does not use Docket.

Written from Lucidex Group's development standards as they stood on November 24, 2026.
It follows the guide kept with Docket section by section, so the two can be read side by side.
"""
import drawing
from drawing import *
from shared import *

NAMES = {'dev': 'development', 'stage': 'stage', 'main': 'main', 'hot': 'hotfix', 'coord': 'coordination'}

BR_TIP = {
    'feat': 'A feature branch: one piece of work, cut from main and named for its work.',
    'dev': 'development: where features are merged, so that any conflict between them shows. Nothing is run on it, and being here does not mean release.',
    'stage': 'stage: the release. The features on the release list, run and checked together. What is verified here is what ships.',
    'main': 'main: what is released. Only a promoted stage reaches it, and all work starts from it.',
    'hot': 'A hotfix: a fix that cannot wait for the next release, cut from main and named for the fault it fixes.',
    'mrg': 'A merge branch: cut from the receiving branch as it is on GitHub, only to resolve a conflict.',
    'coord': 'A coordination branch: it holds only merges of features that require each other. No work is committed on it, and it is never merged anywhere.',
}
NAME_TIP = {
    'production': 'What is deployed and running. It is not a branch; it is shown here only to say which release is live.',
    'on GitHub': 'development as it is on GitHub. This is the branch; a copy on a machine is only a copy.',
    'your copy': 'A copy of development on a machine, for running and testing only. It is taken from GitHub with no local branch.',
    'a feature that waits': 'A feature that is on development but not on this release list. It goes round again.',
}
PR = ('gh pr create --base {to} --head {kind}/<id>-<name> --title "Merge branch \'{kind}/<id>-<name>\' into {to}"\n'
      'gh pr merge <number> --merge --subject "Merge branch \'{kind}/<id>-<name>\' into {to}" --body "Pull-request: <the pull request\'s URL>"')
MAIN_PR = ('gh pr create --base development --head main --title "Merge branch \'main\' into development"\n'
           'gh pr merge <number> --merge --subject "Merge branch \'main\' into development" --body "Pull-request: <the pull request\'s URL>"')
CUT = 'git fetch origin\ngit worktree add -b {kind}/<id>-<name> ~/Development/worktrees/<Project>/{kind}-<id>-<name> origin/main'
PULL = 'git fetch origin\ngit merge origin/main'
RESET = 'git fetch origin\ngit push --force-with-lease origin origin/main:{to}'


def link_tip(fc, fid, tc, tid, dash):
    """What a link between two lanes is, and the command behind it."""
    if dash:
        if fc == 'main' and tc in ('feat', 'hot'):
            return f'{tid} pulls main, in its own folder. This writes only to that branch.', PULL
        if fc == 'main':
            return f'{tid} is reset to main.', RESET.format(to=tid)
        return f'{tid} takes {fid}', None
    kind = 'hotfix' if 'hot' in (fc, tc) else 'feature'
    if fc == 'main' and tc == 'dev':
        return 'main is merged into development by pull request, after a hotfix, or after a release where development is kept running. This brings the release itself into development.', MAIN_PR
    if fc == 'main' and tc == 'coord':
        return 'The coordination branch is cut from main and named for the coordination.', CUT.format(kind='coordination')
    if tc == 'coord':
        return (f'{fid} is merged into the coordination branch. The work stays on the feature\'s own branch.',
                'git merge --no-ff feature/<member> -m "Merge branch \'feature/<member>\' into coordination/<id>-<name>"')
    if fc == 'main' and tc in ('feat', 'hot'):
        return f'{tid} is cut from main as it is on GitHub, and named for {"the fault it fixes" if tc == "hot" else "its work"}.', CUT.format(kind=kind)
    if fc == 'stage' and tc == 'main':
        return ('stage is promoted to main by pull request, on the maintainer\'s word, by the agent that assembled stage.',
                'gh pr create --base main --head stage --title "Merge branch \'stage\' into main"\n'
                'gh pr merge <number> --merge --subject "Merge branch \'stage\' into main" --body "Pull-request: <the pull request\'s URL>"')
    if tc == 'main':
        return f'{fid} is merged straight into main. It was never verified on stage.', None
    if fc == 'dev' and tc == 'mrg':
        return 'The merge branch is cut from development as it is on GitHub.', 'git fetch origin\ngit switch -c merge/<feature id>-into-development origin/development'
    if tc == 'mrg':
        return (f'{fid} is merged into the merge branch, and the conflict is resolved in that merge.',
                'git merge --no-ff feature/<id>-<name> -m "Merge branch \'feature/<id>-<name>\' into development"')
    if fc == 'mrg':
        return f'The pull request into {tid} is opened from the merge branch.', None
    if fc == 'dev' and tc == 'feat':
        return f'{tid} is cut from development, so it holds every feature already there.', None
    if fc in ('feat', 'hot') and tc in ('feat', 'hot'):
        return f'{tid} is cut from {fid}, so it holds {fid}\'s commits.', None
    if tc in ('dev', 'stage'):
        return f'{fid} is merged into {tid}, by pull request, as a real merge.', PR.format(to=tid, kind=kind)
    return f'{fid} into {tid}', None


def dot_tip(cls, bid, kind):
    if bid in ('on GitHub', 'your copy'):
        return ('A feature that was merged into development before the reset.', None) if kind == 'm' else ('development after the reset: the same as main.', None)
    if kind == 'q':
        if cls == 'stage':
            return ('QA: a fresh agent that has built nothing in the project reads each scenario against the tests that name it, checks by hand what they do not check, and gives a result for each scenario. It does not run the suite.', None)
        if cls == 'mrg':
            return 'The conflict is resolved here, in the merge. The feature is not changed.', None
        if cls == 'coord':
            return 'The members are tested together here. The run says it was made here, and names the commit of each member.', None
        return 'Code review, by an agent that did not write the code.', None
    if kind == 'x':
        return ('The pull request does not merge.', None) if cls == 'dev' else ('A feature fails when stage is verified.', None)
    if kind == 'm':
        if cls == 'main':
            return 'A release: stage promoted to main.', None
        if cls in ('dev', 'stage'):
            return f'A feature merged into {bid}, by pull request.', None
        return f'A merge into {bid}.', None
    return f'A commit on {bid}. Commit as often as needed.', None


READY = 'The work is readied: what is to be built is written down, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault. Until then it is still backlog and has no branch.'
SUITE_SAY = 'The suite\'s run: the project\'s whole suite is run on stage, once, by the agent assembling the release. It is mechanical, and each command and its result is noted. It is run again only if stage changes.'
SUITE_TIP = 'The suite\'s run: the project\'s whole suite, run once on the named commit of stage, taken from GitHub without a local branch. Each command and its result is noted.'
QA_SAY = 'QA: a fresh agent that has built nothing in the project reads each scenario the release names against the tests that name it, checks by hand what they do not check, and gives a result for each. It starts from the suite\'s results and does not run the suite. It reports to the agent that started it, and fixes nothing and pushes nothing.'
ACCEPT_SAY = 'QA\'s report is put in front of the maintainer, whose word to promote is acceptance. On that word, the agent that assembled stage promotes it to main by pull request and tags the release twice: a name of version, pull request and date for people, and the bare version for tools.'
JOIN = 'development is rebuilt, on the word to promote: reset to main, which now holds the release. By then most of what it held is released, so the reset costs little, and a development left running for many releases gathers merges GitHub reads as conflicts Git does not have.'
AGAIN = 'Each feature still in progress that was on development is merged into it again, from its own branch by pull request, without being tested or code reviewed again.'
STAY = 'stage stays as it is: it already holds what main holds.'
NOT_BACK = 'Feature B is not sent back by the release: it is merged again as it was. A feature still being built may pull main now; one already tested is not tested again because of it.'


# One step between main and a feature ---------------------------------------------
def main_fig():
    f = Fig(1100, 212, 'Every feature is cut from main, and pulls main again before it is first tested.')
    M, A = 62, 142
    f.lane('main', M); f.lane('feat', A, [(380, 1076)], 'a feature')
    f.dot('main', 226, M, 'm'); f.tag(226, M, 'release', up=True)
    f.link('main', 324, M, 380, A)
    f.label(368, A + 30, 'a feature is cut from main,\nholding what is released')
    for x in (440, 500):
        f.dot('feat', x, A)
    f.dot('main', 640, M, 'm'); f.tag(640, M, 'a release meanwhile', up=True)
    f.link('main', 660, M, 716, A, dash=True); f.dot('feat', 716, A, 'm')
    f.label(728, A + 30, 'before it is first tested,\nthe feature pulls main', 'start')
    return f


# The road ------------------------------------------------------------------------
def road():
    f = Fig(1100, 430, 'One feature travels from main, through development and stage, back to main; a second feature stays on development.')
    A, B, D, S, M = 64, 128, 216, 288, 360
    f.lane('dev', D, [(X0, 922)]); f.lane('stage', S); f.lane('main', M)
    f.dot('main', 212, M, 'm'); f.tag(212, M, 'last release')
    f.step(READY)
    f.label(196, 30, 'A is readied: what is to be built\nis written down', 'start')
    f.step('A branch is cut from main, as it is on GitHub, and named for its work. A second feature is cut the same way. Neither holds anything of the other.')
    f.link('main', 262, M, 318, A)
    f.lane('feat', A, [(318, 690)], 'feature A')
    f.label(330, A + 24, 'cut from main,\nnamed for its work', 'start')
    for x in (348, 392):
        f.dot('feat', x, A)
    f.link('main', 384, M, 432, B)
    f.lane('feat', B, [(432, 1076)], 'feature B')
    for x in (462, 500):
        f.dot('feat', x, B)
    f.step('Feature A pulls main, then its own tests, those that name its scenarios, pass in its own folder. Then its code is reviewed on its own branch by an agent that did not write it, and each finding is answered, before the feature goes anywhere.')
    f.dot('feat', 470, A, 'q'); f.label(470, A - 20, 'code reviewed')
    f.step('Each feature, tested and code reviewed on its own branch, pulls main and is merged into development by its own pull request, once. Nothing is run on development: it is where the features meet and any conflict between them shows. Being on development does not mean a feature will be released.')
    f.dot('feat', 546, B, 'q')
    f.link('feat', 542, A, 610, D); f.dot('dev', 610, D, 'm')
    f.link('feat', 622, B, 668, D); f.dot('dev', 668, D, 'm')
    f.label(640, D + 28, 'merged; nothing is run')
    f.step('Feature A is on the release list the maintainer named. Once it is on development and meets the bar for stage, and the maintainer has confirmed the list, it is merged into stage from its own branch, so it arrives without feature B. Nothing is built or run anywhere first.')
    f.link('feat', 690, A, 760, S); f.dot('stage', 760, S, 'm')
    f.label(752, A + 5, 'on the release list', 'start')
    f.step(SUITE_SAY)
    f.dot('stage', 794, S, 'q', tip=SUITE_TIP); f.label(794, S + 30, 'the suite')
    f.step(QA_SAY)
    f.dot('stage', 826, S, 'q'); f.label(826, S - 20, 'QA')
    f.step(ACCEPT_SAY)
    f.link('stage', 850, S, 900, M); f.dot('main', 900, M, 'm'); f.tag(900, M, 'release')
    f.step(JOIN)
    f.lane('dev', D, [(968, 1076)], pill=False)
    f.link('main', 920, M, 968, D, dash=True); f.dot('dev', 968, D, 'c')
    f.label(968, D - 20, 'development rebuilt')
    f.step(AGAIN + ' ' + NOT_BACK + ' ' + STAY)
    f.link('feat', 1000, B, 1046, D); f.dot('dev', 1046, D, 'm')
    f.label(1040, B - 20, 'merged again', 'end')
    return f


# A release -----------------------------------------------------------------------
def release():
    f = Fig(1100, 440, 'Three features are each tested and code reviewed on their own branch, then merged into development, where nothing is run. Two are on the release list: they are merged into stage, the suite is run there once, QA checks it, and it is promoted to main. Afterwards development is rebuilt from main, with B merged into it again; stage stays as it is.')
    A, B, C, D, S, M = 70, 122, 174, 250, 314, 378
    f.band(160, 438, '1  Tested, code reviewed, merged')
    f.band(438, 676, '2  The release list, on stage', alt=True)
    f.band(676, 890, '3  Accepted and promoted')
    f.band(890, 1100, '4  After the release', alt=True)
    f.lane('feat', A, [(X0, 466)], 'feature A')
    f.lane('feat', B, None, 'feature B')
    f.lane('feat', C, [(X0, 536)], 'feature C')
    f.lane('dev', D, [(X0, 912)]); f.lane('stage', S); f.lane('main', M)
    for x, y in ((200, A), (212, B), (224, C)):
        f.dot('feat', x, y)
    f.step('Before the work, the maintainer names the release list: A and C. Each of three features pulls main, passes its own tests in its own folder and is code reviewed on its own branch, with the findings answered. Then each pulls main again and is merged into development by its own pull request, once. Nothing is run on development; it is where any conflict between them shows. Each time a feature on the list lands, the list is checked: is each feature on development, and does it meet the bar for stage.')
    for x, y in ((224, A), (238, B), (298, C)):
        f.dot('feat', x, y, 'q')
    for x, y in ((246, A), (306, B), (366, C)):
        f.link('feat', x, y, x + 46, D); f.dot('dev', x + 46, D, 'm')
    f.step('Every feature on the list meets the bar, and the maintainer confirms the list. A and C are merged into stage from their own branches, in the order they first went into development, one pull request each. No candidate is built first. B is not on the list.')
    f.link('feat', 466, A, 524, S); f.dot('stage', 524, S, 'm')
    f.link('feat', 536, C, 588, S); f.dot('stage', 588, S, 'm')
    f.label(604, B - 10, 'not on this release list', 'start')
    f.step(SUITE_SAY + ' This is the one run of the whole suite.')
    f.dot('stage', 620, S, 'q', tip=SUITE_TIP); f.label(620, S + 30, 'the suite')
    f.step(QA_SAY)
    f.dot('stage', 652, S, 'q'); f.label(652, S - 20, 'QA')
    f.step(ACCEPT_SAY)
    f.link('stage', 740, S, 790, M); f.dot('main', 790, M, 'm'); f.tag(790, M, 'release')
    f.step(JOIN)
    f.lane('dev', D, [(958, 1076)], pill=False)
    f.link('main', 910, M, 958, D, dash=True); f.dot('dev', 958, D, 'c')
    f.label(958, D - 20, 'development rebuilt')
    f.step(AGAIN + ' ' + NOT_BACK + ' ' + STAY)
    f.link('feat', 1000, B, 1046, D); f.dot('dev', 1046, D, 'm')
    f.label(1046, B - 16, 'merged again', 'end')
    return f


# Rework after a code review --------------------------------------------------------
def rework():
    f = Fig(1100, 300, 'A feature is code reviewed on its own branch before its first merge. Each finding is classified and dealt with by its kind. A defect or a risk is fixed on the feature\'s own branch and the fix is code reviewed. The feature is then merged into development once, and on stage it gets the suite\'s run and QA only.')
    A, D, S = 70, 160, 240
    f.lane('feat', A, [(X0, 800)], 'feature A'); f.lane('dev', D); f.lane('stage', S)
    for x in (206, 244):
        f.dot('feat', x, A)
    f.step('The feature is built, pulls main, and its own tests pass in its own folder. Before it is merged anywhere, its code is reviewed on its own branch by an agent that did not write it. The code review reads the feature\'s own code and tests, and reports findings.')
    f.dot('feat', 310, A, 'x', tip='The code review reports findings. The builder checks each one against the source, the file and the line, before accepting it.')
    f.label(310, A - 20, 'code review: findings', strong=True)
    f.step('The builder classifies each finding, and acts on its kind: a defect, a risk, a missing or weak test, untrue wording, design or style, or wrong. The reviewer\'s own label, blocking or not, is not the classification. The table below says what happens to each kind.')
    f.label(310, A + 26, 'each finding classified\nby its kind')
    f.step('A defect, and a risk that is not put to the maintainer, is fixed on the feature\'s own branch. Any agent may take the rework; it is said who wrote the feature and who reworked it.')
    for x in (470, 510):
        f.dot('feat', x, A)
    f.label(490, A + 26, 'fixed on its own branch')
    f.step('The rework is code reviewed again only when it fixed a defect or a risk. That code review reads whether the fix closes the finding, and what the fix itself changed; it is not a second reading of the feature. Rework for a test, for wording or for a backlog item is not code reviewed again.')
    f.dot('feat', 580, A, 'q', tip='The code review of the fix: whether it closes the finding, and what the fix itself changed.')
    f.label(580, A - 20, 'the fix is code reviewed')
    f.step('The code review is reported: the decision, and each finding with its kind and how it ended. The fixed feature is tested again. It pulls main and is merged into development by pull request, once. Nothing is run there.')
    f.link('feat', 716, A, 766, D); f.dot('dev', 766, D, 'm')
    f.label(750, D + 28, 'merged into development once', 'end')
    f.step('When stage is built from the release list, it is merged into stage from its own branch. Nothing is code reviewed on stage: each feature\'s code review was done once, at the feature. stage gets the suite\'s run, once, and QA, by a fresh agent.')
    f.link('feat', 800, A, 860, S); f.dot('stage', 860, S, 'm')
    f.dot('stage', 904, S, 'q', tip=SUITE_TIP); f.dot('stage', 940, S, 'q')
    f.label(922, S + 30, 'the suite, then QA')
    return f


FINDINGS = [
    ('Defect', 'The code does not do what a scenario or a stated requirement says.', 'Fixed on the feature\'s own branch.'),
    ('Risk', 'The tests pass, but a wrong thing can happen: lost data, a race, an unsafe command.', 'Fixed, or put to the maintainer to accept as it is.'),
    ('Missing or weak test', 'A scenario, or part of one, that no test really checks.', 'Fixed where the scenario is otherwise unverified; otherwise noted, for QA to report.'),
    ('Untrue wording', 'A document, a message or a comment that says something untrue.', 'Fixed. It never holds a feature back on its own.'),
    ('Design or style', 'A preference about how the code is shaped, with no defect or risk in it.', 'Put in the backlog. It never holds a feature back.'),
    ('Wrong', 'The finding misreads the code or a convention of the repository.', 'Rejected with the evidence. A tie-breaker confirms it: any agent that neither wrote the code nor raised the finding, given the finding and the evidence. It is then listed for the maintainer with its reason, and the work moves on; it is not asked.'),
]


def findings():
    rows = ''.join(f'<tr><td><b>{esc(k)}</b></td><td>{esc(w)}</td><td>{esc(h)}</td></tr>' for k, w, h in FINDINGS)
    return ('<div class="tablewrap"><table><thead><tr><th>Kind of finding</th><th>What it is</th><th>What happens to it</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            '<p class="note">The builder classifies each finding; the reviewer\'s own label, blocking or not, is not the classification. A finding put to the maintainer keeps the feature out of <code>stage</code> until it is answered, to fix it or to accept it as it is. The reviewer first reads what is already settled, the project\'s decisions and the code reviews of earlier features, so a finding already rejected is not raised again unless something has changed.</p>')


# Features that require each other ---------------------------------------------------
def coordination():
    f = Fig(1100, 410, 'Two features that require each other are each cut from main. A coordination branch holds only merges of them, where they are tested together. Each then goes to development from its own branch.')
    A, K, B, D, M = 70, 142, 214, 294, 362
    f.lane('dev', D); f.lane('main', M)
    f.step('Feature B cannot be built or tested without feature A, which is not released; or the two work together only with a change to one of them that is right only with the other present. The maintainer ties them in a coordination: a name and a list of its members, as many as require each other, kept wherever the project keeps its work.')
    f.label(196, 30, 'the coordination names its members', 'start')
    f.step('Each member is cut from main on its own branch, as any feature is.')
    f.link('main', 254, M, 310, A); f.lane('feat', A, [(310, 930)], 'feature A')
    f.link('main', 290, M, 350, B); f.lane('feat', B, [(350, 1000)], 'feature B')
    f.dot('feat', 350, A); f.dot('feat', 392, B)
    f.step('A coordination branch is cut from main and named for the coordination. It holds only merges of its members; no work is committed on it.')
    f.link('main', 394, M, 450, K); f.lane('coord', K, [(450, 850)])
    f.link('feat', 470, A, 516, K); f.dot('coord', 516, K, 'm')
    f.link('feat', 500, B, 556, K); f.dot('coord', 556, K, 'm')
    f.step('The members are tested together in the coordination branch\'s folder. A run made here says that it was made here, and names the commit of each member it was run with.')
    f.dot('coord', 612, K, 'q'); f.label(612, K - 20, 'tested together')
    f.step('A fix is never written on the coordination branch. It is written on the member\'s own branch, and the member is merged into the coordination branch again, until they work together. The earlier result is then out of date, and the tests are run there again.')
    f.dot('feat', 650, A)
    f.link('feat', 664, A, 710, K); f.dot('coord', 710, K, 'm')
    f.dot('coord', 768, K, 'q'); f.label(768, K - 20, 'tested again')
    f.label(862, K + 4, 'never merged anywhere', 'start', True)
    f.step('The members go to development and to stage one by one, each from its own branch by its own pull request, in the order they require. The coordination branch is never merged into anything, nothing is cut from it, and it is done with when every member is released.')
    f.link('feat', 930, A, 980, D); f.dot('dev', 980, D, 'm')
    f.link('feat', 1000, B, 1046, D); f.dot('dev', 1046, D, 'm')
    f.label(1010, D + 28, 'one by one, in order')
    return f


# A hotfix ------------------------------------------------------------------------
def hotfix():
    f = Fig(1100, 372, 'The fault is written down, a hotfix is cut from main, stage is reset, and the hotfix is released alone through stage to main. Development then gets the fix when main is merged into it.')
    H, D, S, M = 80, 160, 232, 304
    f.lane('dev', D)
    f.lane('stage', S, [(X0, 416)])
    f.lane('main', M)
    f.label(700, D - 12, 'the hotfix does not pass through development')
    f.step('The maintainer confirms that this is a hotfix, and not a fix for the next release. The fault is written down: what is wrong in production, and the scenario the fix restores or adds.')
    f.label(190, H - 26, '1  the fault is written down', 'start')
    f.step('The hotfix is cut from main as it is on GitHub, in a folder of its own, and named for the fault.')
    f.link('main', 336, M, 392, H)
    f.lane('hot', H, [(392, 680)], 'hotfix')
    f.label(404, H + 26, '2  the hotfix is cut\nfrom main', 'start')
    f.step('stage is reset to main. A release that was being built there is set aside, and its list is merged into stage again once the hotfix is out.')
    f.lane('stage', S, [(462, 1076)], pill=False)
    f.link('main', 412, M, 462, S, dash=True); f.dot('stage', 462, S, 'c')
    f.label(446, M + 24, '3  stage is reset to main')
    f.step('The fix is made test-first, its own tests are run in the hotfix\'s own folder, and its code is reviewed by an agent that did not write it. It is its own release list of one. It is merged into stage by pull request, on the maintainer\'s word.')
    for x in (444, 496):
        f.dot('hot', x, H)
    f.dot('hot', 600, H, 'q')
    f.label(520, H - 20, '4  fixed, tested, code reviewed', 'start')
    f.link('hot', 680, H, 740, S); f.dot('stage', 740, S, 'm')
    f.step('The whole suite is run on stage, once, and a fresh agent does QA. If either fails, the fix is corrected on the hotfix branch, tested again, and code reviewed again where the correction is to a defect or a risk; stage is reset to main again or the correction merged on top; the suite is run again, and QA checks what changed. Then it is promoted to main and tagged, on the maintainer\'s word. The hotfix never goes straight to main.')
    f.dot('stage', 778, S, 'q', tip=SUITE_TIP); f.dot('stage', 810, S, 'q'); f.label(794, S - 20, '5  the suite, then QA')
    f.link('stage', 850, S, 900, M); f.dot('main', 900, M, 'm'); f.tag(900, M, 'release')
    f.step('development does not hold the fix. It gets it when main is merged into it by pull request: after a hotfix, development is not rebuilt, since the work in progress is where it was. No feature is sent back by it, and the features on development stay where they are.')
    f.link('main', 960, M, 1010, D); f.dot('dev', 1010, D, 'm')
    f.label(1024, D - 14, '6  from main', 'start')
    return f


# A bad release already on main -----------------------------------------------------
def rollback():
    f = Fig(1100, 368, 'A bad release already on main is put back by deploying the previous release again, which changes nothing in Git, and is then corrected by a hotfix that goes through stage like any other.')
    H, S, M, P = 62, 132, 202, 286
    f.lane('stage', S); f.lane('main', M)
    f.lane('mrg', P, None, 'production')
    f.dot('main', 214, M, 'm'); f.tag(214, M, 'v0.6.0', up=True)
    f.link('main', 228, M, 272, P, tip='The release v0.6.0 is deployed to production.'); f.dot('mrg', 272, P, 'm', tip='Production runs v0.6.0.')
    f.dot('main', 330, M, 'm'); f.tag(330, M, 'v0.7.0', up=True)
    f.link('main', 344, M, 388, P, tip='The release v0.7.0 is deployed to production.'); f.dot('mrg', 388, P, 'm', tip='Production runs v0.7.0.')
    f.step('A release turns out to be bad after it is promoted and deployed.')
    f.dot('mrg', 450, P, 'x', tip='The release is found to be bad in production.')
    f.label(450, P + 32, 'v0.7.0 is bad', strong=True)
    f.step('Production is put back first. The previous release is deployed again, from its tag, on the maintainer\'s word. This is a deployment and changes nothing in Git: main is not rewritten, and no tag is moved or deleted.')
    f.link('main', 492, M, 540, P, dash=True, tip='The previous release, v0.6.0, is deployed again from its tag. Nothing changes in Git.'); f.dot('mrg', 540, P, 'c', tip='Production runs v0.6.0 again.')
    f.label(556, P + 32, 'v0.6.0 deployed again', 'start')
    f.step('The bad release is then corrected by the hotfix road. The fault is written down, and the hotfix is cut from main. The fix may do no more than undo the bad change.')
    f.link('main', 604, M, 660, H); f.lane('hot', H, [(660, 800)], 'hotfix')
    f.dot('hot', 700, H); f.dot('hot', 750, H, 'q')
    f.label(648, H + 4, 'the hotfix is cut from main', 'end')
    f.step('The hotfix goes through stage, where the suite is run and QA checks it, and is promoted like any other, and the corrected release is deployed. Nothing is reverted on main directly, and the bad release keeps its tag.')
    f.link('hot', 800, H, 850, S); f.dot('stage', 850, S, 'm')
    f.dot('stage', 900, S, 'q')
    f.link('stage', 924, S, 970, M); f.dot('main', 970, M, 'm'); f.tag(970, M, 'v0.7.1', up=True)
    f.link('main', 986, M, 1034, P, tip='The corrected release, v0.7.1, is deployed to production.'); f.dot('mrg', 1034, P, 'm', tip='Production runs v0.7.1.')
    return f


# The loop ------------------------------------------------------------------------
def loop():
    f = Loop(1100, 820, 550, 412, 'One release drawn as a loop: a feature is cut from main, tested and code reviewed on its own branch, merged into development, merged into stage from the release list, run and checked there, and promoted to main; development is rebuilt from main, and the next turn begins.')
    A, B, D, S, M = 300, 254, 208, 162, 116
    f.ring('feat', B, None, 'a feature that waits'); f.ring('main', M)
    f.ring('dev', D); f.ring('stage', S)
    cx, cy = f.cx, f.cy
    names = [('feat', 'a feature'), ('feat', 'a feature that waits'), ('dev', 'development'), ('stage', 'stage'), ('main', 'main')]
    f.txt.append(f.g(f'<text class="bt" x="{cx}" y="{cy - 46}" text-anchor="middle">from the outside in</text>'))
    for i, (c, n) in enumerate(names):
        f.txt.append(f.g(f'<rect class="namehit" x="{cx - 84}" y="{cy - 36 + 18 * i}" width="168" height="18"/>'
                         f'<text class="ringname c-{c}" x="{cx}" y="{cy - 23 + 18 * i}" text-anchor="middle">{esc(n)}</text>',
                         [n], NAME_TIP.get(n, BR_TIP[c]), None, True))
    f.step('Work is readied, and a feature is cut from main, named for its work.')
    f.rlink('main', .055, M, .105, A)
    f.ring('feat', A, [(.105, .415)], 'a feature')
    for t in (.15, .2):
        f.rdot('feat', t, A)
    f.num(.118, A + 21, 1); f.out(.09, '1  a feature is cut\nfrom main')
    f.step('It pulls main, its own tests pass in its own folder, and its code is reviewed on its own branch, with each finding answered. Then it is merged into development, once. Nothing is run there.')
    f.rdot('feat', .24, A, 'q')
    f.rlink('feat', .272, A, .30, D); f.rdot('dev', .30, D, 'm')
    f.num(.318, D + 21, 2); f.out(.29, '2  tested, code reviewed,\nmerged into development')
    f.step('The maintainer has named the release list. Once every feature on it meets the bar and the list is confirmed, each is merged into stage from its own branch, in the order it first went into development.')
    f.rlink('feat', .415, A, .455, S); f.rdot('stage', .455, S, 'm')
    f.num(.478, S + 21, 3); f.out(.44, '3  on the\nrelease list')
    f.step(SUITE_SAY + ' ' + QA_SAY)
    f.rdot('stage', .503, S, 'q', tip=SUITE_TIP); f.rdot('stage', .53, S, 'q')
    f.num(.552, S + 23, 4); f.out(.515, '4  the suite,\nthen QA')
    f.step(ACCEPT_SAY)
    f.rlink('stage', .60, S, .635, M); f.rdot('main', .635, M, 'm')
    x, y = f.pt(.69, M + 21)
    f.tag(x, y - 27, 'release')
    f.num(.61, M + 21, 5); f.out(.62, '5  accepted, promoted\nand tagged')
    f.step(JOIN)
    f.rlink('main', .755, M, .795, D, dash=True); f.rdot('dev', .795, D, 'c')
    f.num(.813, D + 21, 6); f.out(.785, '6  development\nrebuilt from main')
    f.step(AGAIN + ' A feature that waits goes round again. It is not sent back by the release. stage stays as it is, and the next turn begins.')
    f.num(.937, B + 21, 7); f.out(.91, '7  a feature that waits\ngoes round again')
    return f


# What not to do --------------------------------------------------------------------
def why():
    f, L, R = pair(300, 'cut a feature from development', 'cut it from main', 'A feature cut from development carries every other feature into stage with it. A feature cut from main arrives on stage alone.')
    D, X, S = 92, 162, 232
    L.lane('dev', D); L.lane('feat', X, [(346, 430)], 'feature X'); L.lane('stage', S)
    for x, t in ((226, 'A'), (276, 'B')):
        L.dot('dev', x, D, 'm'); L.label(x, D - 18, t)
    L.link('dev', 296, D, 346, X)
    L.dot('feat', 382, X)
    L.link('feat', 430, X, 480, S); L.dot('stage', 480, S, 'm')
    L.chips(392, S + 34, 'arrives on stage:', [('X', 'feat'), ('A', 'hot'), ('B', 'hot')])
    X2, D2, S2, M2 = 70, 126, 182, 238
    R.lane('feat', X2, [(300, 430)], 'feature X'); R.lane('dev', D2); R.lane('stage', S2); R.lane('main', M2)
    for x, t in ((196, 'A'), (232, 'B')):
        R.dot('dev', x, D2, 'm'); R.label(x, D2 - 18, t)
    R.link('main', 250, M2, 300, X2)
    R.dot('feat', 340, X2)
    R.link('feat', 430, X2, 480, S2); R.dot('stage', 480, S2, 'm')
    R.chips(392, M2 + 34, 'arrives on stage:', [('X', 'feat')])
    return f


def p_chain():
    f, L, R = pair(282, 'cut one feature from another', 'cut each from main', 'A feature cut from another feature carries it into stage. Cut from main, each arrives alone.')
    A, B, S, M = 70, 120, 170, 220
    for H in (L, R):
        H.lane('stage', S)
        H.lane('main', M)
    L.link('main', 200, M, 254, A)
    L.lane('feat', A, [(254, 316)], 'feature A'); L.dot('feat', 284, A)
    L.link('feat', 316, A, 356, B)
    L.lane('feat', B, [(356, 430)], 'feature B'); L.dot('feat', 392, B)
    L.link('feat', 430, B, 476, S); L.dot('stage', 476, S, 'm')
    L.chips(398, 258, 'arrives on stage:', [('B', 'feat'), ('A', 'hot')])
    R.link('main', 200, M, 254, B)
    R.lane('feat', B, [(254, 430)], 'feature B'); R.dot('feat', 384, B)
    R.link('main', 262, M, 316, A)
    R.lane('feat', A, [(316, 390)], 'feature A'); R.dot('feat', 350, A)
    R.link('feat', 430, B, 476, S); R.dot('stage', 476, S, 'm')
    R.chips(398, 258, 'arrives on stage:', [('B', 'feat')])
    return f.svg()


# The tables and cards ---------------------------------------------------------------
def cards(rows, raw=False):
    return ''.join(f'<li><h3>{esc(t)}</h3><p>{d if raw else esc(d)}</p></li>' for t, d in rows)


CHECKS = [
    ('main', 'Plan', 'The files, the changes, their order, the risks and how the result will be verified.', 'The agent that will build', 'when', 'Before building, where a wrong call would be costly after it is merged'),
    ('main', 'Plan review', 'A reading of the plan against the code.', 'A second agent', 'when', 'When a plan needs further input or a second opinion'),
    ('feat', 'Test', 'The feature\'s own tests, those that name its scenarios, run on its committed code in the feature\'s own folder, after it has pulled main.', 'The agent that built it', 'always', 'Before its code review, and whenever its code changes. A pull does not start it'),
    ('feat', 'Code review', 'A reading of the feature\'s own code and tests, on the feature\'s own branch. The builder checks each finding against the source, classifies it, and deals with it by its kind. A rework is code reviewed again only when it fixed a defect or a risk, and that code review reads the fix. Nothing is code reviewed on stage.', 'An agent that did not write it', 'always', 'Before the first merge into development, and for every hotfix'),
    ('stage', 'The suite\'s run', 'The project\'s whole suite, run once on the named commit of stage, with each command and its result noted, and reported with its regression count. It is mechanical: no judgement is used. It is the one run of the whole suite.', 'The agent assembling the release', 'always', 'Once the release list is merged into stage, and again only when stage changes'),
    ('stage', 'QA', 'The independent check of stage. Each scenario the release names is read against the tests that name it, and what the tests do not check is checked by hand. It gives a result for each: verified by a test, partly verified, no test found, checked by hand, or failed, saying what failed and what kind of fault it is. It also confirms the list of what each feature has and lacks. It does not run the suite. Its brief is fixed text, sent as written with its blanks filled in.', 'A fresh agent that has built nothing in the project', 'always', 'After the suite has passed on stage'),
    ('main', 'Acceptance', 'The maintainer\'s word to promote stage to main, given with QA\'s report in front of them.', 'The maintainer', 'always', 'After QA'),
]


def checks():
    out = []
    for i, (cls, t, what, who_, kind, when) in enumerate(CHECKS, 1):
        badge = '<span class="need">when needed</span>' if kind == 'when' else '<span class="need all">every time</span>'
        out.append(f'<li class="step c-{cls}"><span class="n">{i}</span><h3>{esc(t)}</h3><p>{esc(what)}</p>'
                   f'<dl><dt>Who</dt><dd>{esc(who_)}</dd><dt>When</dt><dd>{esc(when)}</dd></dl>{badge}</li>')
    return ('<ol class="steps seven">' + ''.join(out) + '</ol>'
            '<p class="note"><b>When something fails.</b> A failure belongs to a feature, wherever it is caught. It is said which step caught it (the feature\'s own tests, the code review, the suite\'s run on <code>stage</code>, QA) and what kind it is, by the six kinds of finding listed under rework after a code review. The feature goes back to its builder and is fixed on its own branch. Knowing the step and the kind is what shows, over time, which step catches what and what reaches <code>stage</code>.</p>')


HOLDS = [
    ('main', 'main', [('code', 'the released code')]),
    ('feat', 'a feature', [('code', 'the released code, as it stood when the feature was cut'), ('rec2', '+ what it has pulled from main since'), ('own', '+ this feature\'s code')]),
    ('dev', 'development', [('code', 'the released code'), ('rec2', '+ main, as it was when development was last rebuilt, and any hotfix since'), ('own', '+ the code of every feature merged there')]),
    ('stage', 'stage', [('code', 'the released code'), ('own', '+ the code of the features on the release list')]),
]


def holds():
    cols = []
    for cls, name, blocks in HOLDS:
        b = ''.join(f'<span class="blk {k}">{esc(t)}</span>' for k, t in reversed(blocks))
        cols.append(f'<div class="col c-{cls}"><div class="stack">{b}</div><code>{esc(name)}</code></div>')
    return '<div class="holds four">' + ''.join(cols) + '</div>'


FOLDERS = [
    ('main', 'The project\'s own folder', '~/Development/<Project>', 'The user works here, on checked-out branches. An agent does not.'),
    ('feat', 'A folder for each feature', '~/Development/worktrees/<Project>/<kind>-<id>-<name>', 'An agent works here, one folder to a branch, and never in a checkout someone else is using. The feature is built and tested here.'),
]


def folders():
    li = ''.join(f'<li class="c-{c}"><h3>{esc(t)}</h3><code>{esc(p)}</code><p>{esc(d)}</p></li>' for c, t, p, d in FOLDERS)
    return f'<div class="repo"><span>one repository</span></div><ul class="folders">{li}</ul>'


WHO = [
    ('Commit on a feature', 'free', 'As often as needed'),
    ('Push a feature, then open and merge its pull request into development', 'free', 'For work the user has said to work, once its code review is answered. A feature already on development is merged again after rework'),
    ('Open a pull request into stage', 'word', 'The maintainer names the release list. The maintainer\'s confirmation of the list covers its pull requests into stage. Including a feature below the bar is the maintainer\'s decision'),
    ('Promote stage to main, and tag the release', 'word', 'The maintainer\'s word to promote is acceptance. The agent that assembled stage performs it'),
    ('Rebuild development after a release, or bring main into it after a hotfix', 'word', 'Covered by the maintainer\'s word to promote'),
    ('Reset development', 'word', 'When that serves the work: usually after a release, when something has to come out of it, or to show a release running before stage is built'),
    ('Reset stage', 'word', 'Usually when a feature has failed on it, before a hotfix, and before a release is built on it if it holds anything main does not. The maintainer\'s confirmation of the release list covers the resets of stage that building it needs'),
    ('Change branch protection or repository settings', 'word', ''),
]


def who():
    say = {'free': 'without asking', 'word': "waits for the maintainer's word"}
    rows = ''.join(
        '<tr><td>%s</td><td><span class="%s">%s</span></td><td>%s</td></tr>' % (esc(a), k, say[k], esc(n))
        for a, k, n in WHO)
    return f'<div class="tablewrap"><table><thead><tr><th>What</th><th>May it be done</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></div>'


ELIGIBLE = [
    ('Its scenarios pass', 'Its work names its scenarios, or says why it has none; naming none, with no reason, does not meet this. Its tests pass in the feature\'s own folder for the feature\'s own code as it stands: a run made before the feature\'s code last changed does not count, and the tests are run again. A pull that brought in what was released does not make a run out of date. For a member of a coordination whose tests cannot pass alone, a passing run from the coordination branch\'s folder stands in its place when it names the commit of each member and no member has changed since.'),
    ('Its code is reviewed', 'By an agent that did not write it, with each finding dealt with as its kind requires. A finding put to the maintainer keeps the feature out until it is answered, to fix it or to accept it as it is.'),
    ('It stands alone', 'It holds no other unreleased feature\'s commits. A member of a coordination is chosen only with, or after, the members it requires.'),
    ('No open defect', 'None is known against it.'),
    ('Its decisions are accepted, and its story agreed', 'Every decision it rests on is accepted by the product owner. Any story an agent wrote for it has been seen and agreed by the product owner: a feature built from a story an agent wrote itself may be built to development, and waits at stage until then.'),
]


def eligible():
    return (f'<ul class="gives five">{cards(ELIGIBLE)}</ul><p class="note">The release list is the maintainer\'s choice. Each time a feature on it is merged into <code>development</code>, and each time the list changes, it is checked against this bar, and the maintainer is told that every feature meets it or which lacks what; the agent never chooses the list. That agent may have built part of the release, so the fresh QA agent confirms what it said. '
            'If the maintainer includes a feature below the bar, that is the maintainer\'s decision, given with what the feature lacked in front of them, and QA reports what it lacked as not verified.</p>')


RESET_USUALLY = [
    ('After a release, for development', 'What it held is by then mostly released. It is reset to main and the features still in progress are merged again. The maintainer\'s word to promote covers it.'),
    ('Something has to come out', 'A feature on development is abandoned, or its merge is in the others\' way; a feature has failed on stage.'),
    ('A clean start is needed', 'Before a hotfix, stage is reset so that the fix travels alone. Before a release is built on it, stage is reset if it holds anything main does not.'),
    ('The branch is to show one thing', 'development is rebuilt from a release list so that people can look at that release wherever development is deployed. No test is run there.'),
    ('The branch can no longer be trusted', 'It has taken a merge it should not have, or so much has gone wrong on it that finding the cause costs more than building it again.'),
]
RESET_SELDOM = [
    ('stage, after a release or a hotfix', 'It already holds what main holds.'),
    ('development, where the project has a reason to keep it running across releases', 'Such as wanting to see what builds up on it. Then main is merged into it by pull request after each release.'),
    ('While features on it are waiting for a release', 'Resetting development means merging each of them again.'),
    ('When a small correction to a feature of the release is quicker and as safe', 'The feature is fixed on its own branch and merged again by pull request, on top of what is there, where rebuilding the whole release would cost more than it protects. Nothing is ever changed on the branch itself.'),
]


def resets():
    return ('<h3 class="sub">When to reset development or stage, and when to leave it running</h3>'
            '<p class="note">Both can be reset to <code>main</code> when that serves the work. This is guidance, not a list to apply by rote: say which case you see and why, and where it is not plain, ask. A reset is a push, so it is on the maintainer\'s word; the maintainer\'s confirmation of the release list covers the resets of <code>stage</code> that building it needs.</p>'
            '<h3 class="sub">A reset is usually right</h3>'
            f'<ul class="gives two">{cards(RESET_USUALLY)}</ul>'
            '<h3 class="sub">It is usually better left running</h3>'
            f'<ul class="gives plain">{cards(RESET_SELDOM)}</ul>'
            '<p class="note">After a reset, the features that should still be there are merged again, each from its own branch by pull request, and everyone is told, so that anyone with a copy takes it from GitHub again.</p>')


TESTING = [
    ('feat', '1. Pull main into the feature', 'The feature\'s code is written, and it is about to be tested for the first time.', 'The agent that built it', 'main as it is on GitHub is merged into the feature, so that it is tested on what is released.'),
    ('feat', '2. Test the feature', 'The feature\'s code is written, or has changed since it was last tested. A pull does not start it.', 'The agent that built it', 'The code is committed, and the feature\'s own tests, those that name its scenarios, are run in its folder.'),
    ('feat', '3. Review the feature\'s code', 'Its tests pass and its code has not been reviewed. Or a rework has fixed a defect or a risk.', 'An agent that did not write the code; the builder answers', 'The feature\'s own code and tests are read, and each finding is answered by its kind. Nothing is run.'),
    ('dev', '4. Merge the feature into development', 'Its tests pass and every finding is answered. Or a feature already there has been reworked.', 'The agent that built it', 'The feature pulls main, is pushed, and is merged by pull request. Nothing is run on development.'),
    ('dev', '5. Check the release list', 'A feature on the list has just been merged into development. Or the maintainer has changed the list.', 'The agent that merged the feature; the maintainer owns the list', 'Each feature on the list is checked: it is on development, and it meets the bar for stage. The maintainer is told that all do, or which lacks what. Nothing is run.'),
    ('stage', '6. Build stage from the list', 'Every feature on the list meets the bar, or is on it by the maintainer\'s word, and the maintainer has confirmed the list.', 'The agent assembling the release', 'stage is reset to main if it holds anything main does not, and each feature is merged by pull request. No candidate is built anywhere first.'),
    ('stage', '7. Run the suite on stage', 'Every feature on the list is merged into stage. Or stage has changed since the suite last ran on it.', 'The agent assembling the release. It is mechanical', 'The project\'s whole suite is run on the named commit of stage, and each command and its result is noted, with the regression count. This is the one run of the whole suite.'),
    ('stage', '8. QA', 'The suite has passed on stage.', 'A fresh agent that has built nothing in the project', 'Each scenario is read against the tests that name it; what the tests do not check is checked by hand; a result is given for every scenario. It does not run the suite.'),
    ('stage', '9. A failure on stage', 'Step 7 or step 8 reports a failure.', 'The agent assembling the release, without waiting; the feature\'s builder fixes', 'The failure is recorded against its feature. Usually the feature comes off and stage is rebuilt; a small fix may be merged on top. Then step 7 again, and step 8 for the feature that was fixed; after a feature comes off, QA\'s results for the rest stand.'),
    ('stage', '10. What QA observed outside the scenarios', 'QA\'s report names something wrong that fails no scenario.', 'The maintainer', 'The maintainer says: release as it is and put it in the backlog, or treat it as a failure (step 9).'),
    ('main', '11. Acceptance', 'QA has reported and every failure is dealt with.', 'The maintainer', 'QA\'s report is put in front of the maintainer, who gives the word to promote. It covers step 12.'),
    ('main', '12. Promote', 'The maintainer\'s word.', 'The agent that assembled stage', 'stage is merged into main by pull request and tagged. development is usually rebuilt: reset to main, with the features still in progress merged again; where it is left running, main is merged into it. Nothing is run.'),
]


def testing():
    rows = ''.join(f'<tr class="c-{c}"><td><b>{esc(s)}</b></td><td>{esc(w)}</td><td>{esc(who_)}</td><td>{esc(d)}</td></tr>' for c, s, w, who_, d in TESTING)
    return ('<p class="note">Before the work, where possible, the maintainer names the release list: the features the release is to hold. It is kept where the project\'s own instructions say; where they name no place, the agent assembling the release keeps it as the maintainer gave it and says it back at each check.</p>'
            '<div class="tablewrap"><table class="testing"><thead><tr><th>Step</th><th>What starts it</th><th>Who</th><th>What is done</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            '<p class="note"><b>Every released scenario is tested again at every release.</b> Not every piece of work is worked on in every release, but the suite run on <code>stage</code> holds the tests of everything already released, so all of it is tested each time. That is a feature of the method, and it is why the whole suite runs on <code>stage</code> and nowhere earlier.</p>'
            '<p class="note"><b>The regression count.</b> Every run of the suite reports how far it reached: the scenarios whose tests ran and passed; the scenarios whose tests were skipped, each named with the test; and the scenarios no test names, whose number is given every time and the new ones called out. A skipped test has not checked its scenario: it is never a pass, and where the skip came from the order of the commands or the machine, the test is run again on the same commit. The count is made by a script the project keeps, never by hand; where there is none, or the tests do not name their scenarios, the run says the count was not made and why, and still names each skipped test. Two limits are said with it every time: a test that names a scenario is not thereby shown to check it, and a test that has been weakened is not seen.</p>'
            '<p class="note"><b>What this leaves out, on purpose.</b> Nothing is run when a feature lands on <code>development</code>. No copy of the release is built and tested before <code>stage</code>. A feature does not pull again because a release happened, and is not tested or code reviewed again because of one. QA does not run the suite. So <code>stage</code> is the first place the release\'s features are together without the rest of <code>development</code>, and a conflict or a failure between them is found there.</p>'
            '<p class="note"><b>Showing a release before it is built.</b> Where people need to see a release running before <code>stage</code> is built, <code>development</code> can be reset to <code>main</code> and rebuilt from the release list, each feature by its own pull request. Nothing in the testing process depends on it.</p>')


def see():
    return ('<ul class="gives two">'
            + cards([('Where', 'From the feature\'s own folder, apart from anything released that is in use: on a port of its own, with data of its own and never the real data.'),
                     ('When', 'Before or after the feature is tested, whenever a person wants to see it. The agent says how to reach it, and builds it again when the code changes.')])
            + '</ul><p class="note">Seeing the work is not testing it. The feature\'s own tests still run when its code is written or changes, and the release is proved on <code>stage</code>.</p>')


def rebuild():
    return ('<p class="note">On the maintainer\'s word to promote, once <code>stage</code> is promoted and tagged. First list the unreleased features <code>development</code> holds, the merges it has that <code>main</code> does not:</p>'
            '<pre class="cmd">git fetch origin\ngit log --merges --first-parent --format=%s origin/main..origin/development</pre>'
            '<p class="note">Reset it to <code>main</code>:</p>'
            '<pre class="cmd">git push --force-with-lease origin origin/main:development</pre>'
            '<p class="note">Merge each of those features again, from its own branch by pull request, as any feature is merged into <code>development</code>, without testing or code reviewing it again. Tell everyone, so that anyone with a copy takes it from GitHub again. Where nothing unreleased was on it, the reset is the whole of it.</p>'
            f'<pre class="cmd">{esc(PR.format(to="development", kind="feature"))}</pre>'
            '<p class="note"><b>Where a project keeps it running.</b> A project with a reason to keep <code>development</code> running across releases, such as wanting to see what builds up on it, merges <code>main</code> into it by pull request after each release instead. After a hotfix, <code>main</code> is merged into it the same way, since the work in progress is where it was.</p>'
            f'<pre class="cmd">{esc(MAIN_PR)}</pre>')


def history():
    return ('<div class="logs"><figure class="log"><figcaption><code>git log --first-parent main</code>, one release to an entry</figcaption><pre>'
            '<b>Merge branch \'stage\' into main</b>            <i>tag v0.6.0-pr142-2026-11-21</i>\n'
            '    Pull-request: https://github.com/&lt;account&gt;/&lt;project&gt;/pull/142\n'
            '<b>Merge branch \'stage\' into main</b>            <i>tag v0.5.1-pr131-2026-11-09, a hotfix</i>\n'
            '    Pull-request: https://github.com/&lt;account&gt;/&lt;project&gt;/pull/131</pre></figure>'
            '<figure class="log"><figcaption><code>git log --first-parent stage</code>, one arrival to an entry</figcaption><pre>'
            '<b>Merge branch \'feature/w-t3xa8-passkey-sign-in\' into stage</b>\n'
            '<b>Merge branch \'fix/w-k7f3q-reset-email\' into stage</b></pre></figure>'
            '<figure class="log"><figcaption>On a feature, a release arriving. This is not the feature arriving anywhere.</figcaption><pre>'
            'Merge remote-tracking branch \'origin/main\' into feature/w-t3xa8-passkey-sign-in</pre></figure></div>'
            '<p class="note"><b>A release\'s name</b> is its tag: <code>v&lt;version&gt;-pr&lt;number&gt;-&lt;date&gt;</code>. The version comes first, then the number of the pull request that promoted <code>stage</code> to <code>main</code>, then the date of the promotion. A second tag on the same commit is the bare version, <code>v&lt;version&gt;</code>, for tools: under semantic versioning a hyphen after a version marks a pre-release, so a tool would rank the descriptive name below the release it names. '
            'Every merge made by pull request carries one line in its body, <code>Pull-request:</code> and the pull request\'s URL, so the merge commit itself leads to GitHub. '
            'The history of releases is read from these tags.</p>'
            '<p class="note"><b>Where a piece of work stands</b> is read from the merges, not set by hand. Which of <code>development</code>, <code>stage</code> and <code>main</code> hold its branch is a fact of the history. Before saying that work is or is not released, check it there.</p>')


RULES = [
    ('Cut work from development or stage, or pull from either.', 'Work starts only from main, a hotfix included. A feature takes what is released by pulling main: before it is first tested, and as it is merged into development.'),
    ('Commit on development or stage, or merge into either on your own machine.', 'Both change only by a pull request on GitHub, merged as a real merge.'),
    ('Cut a branch for work that is not ready.', 'What is to be built is written down first, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault. A standing instruction to keep working does not change this.'),
    ('Change anything in a merge beyond its conflict.', 'A merge resolves its conflict and nothing else. Any other change features need in order to work together is written on a feature\'s own branch, and the feature is merged again. Where the change is only right with the other features present, they are tied in a coordination.'),
    ('Merge a feature into development before its code review.', 'It is code reviewed on its own branch, and the findings answered, first, so that it is merged once.'),
    ('Commit work on a coordination branch, or merge it anywhere.', 'The work is done on the member\'s own branch, and the member is merged into the coordination branch again. The members go onward one by one.'),
    ('Reset development or stage by rote.', 'Both can be reset to main when that serves the work. Say which case you see and why, and where it is not plain, ask. After a release development is usually rebuilt, and stage stays as it is.'),
    ('Leave stage standing with a known fault.', 'Usually the feature comes out and stage is reset. Where the fault is small and quickly fixed on the feature\'s own branch, it may be merged again on top. Either way the suite is run on stage again.'),
    ('Run the suite again on code that has not changed.', 'A step is taken when what starts it has happened. A feature\'s tests run when its code changes; a pull, or a release made since, does not start them. Nothing is run on development. The whole suite runs once, on stage, and again only when stage changes.'),
    ('Count a skipped test as a pass.', 'A skipped test has not checked its scenario. It is named, and where the skip came from the order of the commands or the machine, it is run again on the same commit.'),
    ('Count a scenario as passed because the suite passed.', 'QA reads each scenario against the tests that name it and gives a result for each, and reports one with no test as no test found.'),
]


def rules():
    li = ''.join(f'<li><p class="dont"><b>Don\'t</b> {esc(a)}</p><p class="do"><b>Do</b> {esc(b)}</p></li>' for a, b in RULES)
    return f'<ul class="rules">{li}</ul>'


STEPS = [
    ('main', 'Readied', 'What is to be built is placed under its use case and written down, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault.', ''),
    ('feat', 'Cut and built', 'A branch is cut from main as it is on GitHub and named for its work, one piece of work to a branch, in a folder of its own. Commits as often as needed.', ''),
    ('feat', 'Tested and code reviewed', 'It pulls main, and its own tests, those that name its scenarios, pass in its own folder. Then its code is reviewed on its own branch by an agent that did not write it, and each finding is answered.', ''),
    ('dev', 'Merged into development', 'It pulls main, and a pull request into development is merged without asking. Nothing is run there. Being here does not mean it will be released.', ''),
    ('stage', 'On the release list', 'The maintainer names the release list, before the work where possible. Each time a feature on it lands, the list is checked against the bar for stage.', 'word'),
    ('stage', 'Built on stage', 'Once every feature on the list meets the bar and the list is confirmed, one pull request into stage for each, in the order they first went into development. No candidate is built first.', ''),
    ('stage', 'Run and checked', 'The whole suite is run on stage, once, and reports its regression count. Then QA: a fresh agent that has built nothing in the project reads each scenario against its tests and checks by hand what they miss.', ''),
    ('main', 'Promoted', 'QA\'s report is put in front of the maintainer. On the maintainer\'s word stage is promoted to main and tagged, and development is rebuilt from main.', 'word'),
]


def steps():
    out = []
    for i, (cls, title, text, word) in enumerate(STEPS, 1):
        w = '<span class="word">waits for the maintainer\'s word</span>' if word else ''
        out.append(f'<li class="step c-{cls}"><span class="n">{i}</span><h3>{esc(title)}</h3><p>{esc(text)}</p>{w}</li>')
    return ('<div class="standards"><span class="std a">Building to development: fast, and nothing is run there</span>'
            '<span class="std b">Choosing for stage: strict</span></div><ol class="steps">' + ''.join(out) + '</ol>')


BRANCHES = [
    ('feat', 'feature', 'One piece of work, cut from main. Also fix and hotfix.'),
    ('dev', 'development', 'Where features are merged, and their conflicts show. Nothing is run on it.'),
    ('stage', 'stage', 'The release: the listed features, run and checked together.'),
    ('main', 'main', 'What is released. Only a promoted stage reaches it.'),
]

KEY = (
    '<ul class="key">'
    '<li><svg viewBox="0 0 28 16"><path class="ln c-feat" d="M0 8H28"/><circle class="dc c-feat" cx="14" cy="8" r="5"/></svg>a commit</li>'
    '<li><svg viewBox="0 0 28 16"><path class="ln c-dev" d="M0 8H28"/><circle class="dm c-dev" cx="14" cy="8" r="7"/></svg>a merge</li>'
    '<li><svg viewBox="0 0 28 22"><g class="c-stage"><circle class="dq" cx="14" cy="11" r="10"/><path class="tick" d="M9.5 11.5l3 3.2 6-7"/></g></svg>QA, or a code review</li>'
    '<li><svg viewBox="0 0 36 16"><path class="lk c-feat" d="M0 8H36"/></svg>work moving on, by pull request</li>'
    '<li><svg viewBox="0 0 36 16"><path class="lk c-main dash" d="M0 8H36"/></svg>a pull of main, or a reset</li>'
    '</ul>'
    '<p class="hint">Point at a branch, by its name or anywhere along its line, to follow it; click its name to keep it lit. Point at any link or mark to see what it is and the command behind it.</p>'
)

GIVES = [
    ('A release is named, not inherited', 'Being on development does not put a feature in a release. The maintainer, the person who decides what is released, names the release list feature by feature.'),
    ('Nothing is run on development', 'It is where features are merged and their conflicts show. The release\'s features are run together once, on stage.'),
    ('Many features at once', 'Every feature is built to stand alone, so several people or agents can build at the same time, each in a folder of its own (a Git worktree).'),
    ('What is verified is what ships', 'stage holds the release list and nothing else, run and checked as a whole. Nothing is changed on stage itself.'),
    ('A failed feature comes out cleanly', 'Usually stage is rebuilt without it. Nothing is backed out, and nothing is patched in place.'),
    ('Every released scenario is tested again at every release', 'Not every piece of work is worked on in every release, but the whole suite runs on stage, so everything already released is tested each time, and the run says how far it reached.'),
    ('Each check is made once', 'A feature\'s own tests and its code review are done at the feature, and are not repeated because a release happened. The release runs the whole suite once, on what ships, and a fresh agent checks each scenario.'),
    ('A hotfix takes a release\'s road, alone', 'Cut from main, run and checked on stage, promoted. It does not pass through development first, and it never goes straight to main.'),
    ('The history says where work has been', 'Every merge is a real merge whose title names both branches, so Git can say which branches hold a feature.'),
    ('Plain Git', 'Every step is ordinary Git, with pull requests on GitHub, and can be done by hand.'),
]


def purpose():
    return f"""<section class="purpose" id="why">
<div class="cols">
<div><h2>Why it exists</h2>
<p>Most branching methods tie two decisions together: testing a feature with the others, and releasing it. Where features are cut from a shared <code>development</code> branch and merged back into it, whatever is on that branch is in the next release unless someone backs it out. One unfinished feature holds up everything behind it.</p>
<p>Feature Promotion Flow separates the two. A feature is merged into <code>development</code>, where its conflicts with the others show, and that says nothing about release. The release is built separately, on <code>stage</code>, from the features the maintainer lists for it, each merged from its own branch, and is tested and checked there.</p>
<p>It is close to the method the Git project uses to build Git itself, <a href="https://git-scm.com/docs/gitworkflows">gitworkflow</a>: topic branches that graduate through integration branches, and tagged releases. In the projects it was written for, it replaced gitflow.</p>
</div>
<div><h2>Why features are cut from main</h2>
<p>Git can merge a branch into any other branch it shares an ancestor with. What a branch was cut from decides what comes with it.</p>
<p>A feature cut from <code>main</code> holds its own commits and what is released. So it can be merged into <code>development</code> and later into <code>stage</code> for release, and neither merge brings another feature's code along. A feature cut from <code>development</code> would carry every other feature on <code>development</code> into <code>stage</code> with it.</p>
<p>That is the whole of what lets a release be chosen feature by feature. So work starts only from <code>main</code>, a hotfix included, and a feature takes what is released by pulling <code>main</code>.</p>
</div></div>
{fig(main_fig(), 'A feature holds its own commits and what is released, and nothing of any other feature. Nobody cuts work from <code>development</code> or <code>stage</code>, and nobody pulls from them.')}
<h2>What it gives you</h2>
<ul class="gives">{cards(GIVES)}</ul>
</section>"""


LIMITS = [
    ('The evidence so far', 'The method is new. As it is written here it has been run on one project, through few releases, and that project kept its record with Docket. Nothing here has yet been shown with several people on several machines, and every benefit below should be read with that in mind.'),
    ('What it costs', 'A release of n features is 2n + 2 pull requests: each feature into development and into stage, stage into main, and main into development. It is also n code reviews, one run of the whole suite, and one QA run. A feature that fails on stage usually costs a reset, a pull request for each feature that remains, and the suite run again. Because nothing runs the release\'s features together before stage, a conflict or a failure between them is found there. A hotfix is three pull requests, a code review, a run of the suite and a QA run, and sets aside any release being built.'),
    ('What it does not cover', 'The method says nothing about database migrations, or about fixing an older version while a newer one is out: there is one released line. It does not say how a release is deployed, and its rollback (see the section on a bad release) assumes the previous release can be deployed again. It does not say where a project keeps its backlog, its decisions or its code reviews.'),
    ('Against trunk-based development', 'Trunk-based development with feature flags separates testing from releasing another way: everything merges to one branch daily, and a flag decides what is released. It integrates sooner and needs no assembly. It asks that unfinished work be safe to ship switched off, and the flags, not the history, say what a release contains. This method makes the other trade. Integration comes later and costs more pull requests. In return a release is a set of whole features, each with its own tests and code review, and what is left out is not in the build at all.'),
]
UNPROVEN = [
    ('Fewer regressions', 'This is what the design should produce. Too few releases have been through stage to show it.'),
    ('What the regression count cannot show', 'A test that names a scenario is not thereby shown to check it, and a test that has been weakened still passes. The count says how far the suite reached, not how well each test checks.'),
    ('The testing process as it now stands', 'The twelve steps were settled on November 23, 2026, after one project ran its whole suite four to six times for each release on code that had not changed. One project has since taken one small feature through them.'),
    ('Reliable release dates', 'They depend on features staying independent. Where features require each other, a coordination handles it, at the cost of some freedom to choose.'),
]


def limits():
    return (f'<ul class="gives two">{cards(LIMITS)}</ul>'
            '<h3 class="sub">Designed in, and not yet proven by use</h3>'
            f'<ul class="gives two">{cards(UNPROVEN)}</ul>')


ADDUP = [
    ('Reliable release dates', 'The maintainer may change the release list at any time, so the date does not wait on one unfinished feature: it comes off the list. stage is rebuilt and not patched, so a late failure removes one feature, not the release. The date is the promise; the contents are whatever is ready by then.'),
    ('Fewer regressions', 'Scenarios are written before the branch exists, so behaviour is pinned down first. The whole suite runs on the exact combination that ships, so every released scenario is tested again at every release. And after a hotfix main is merged into development, so the next release cannot quietly lose the fix.'),
    ('Checking by someone who did not build', 'A feature\'s code is reviewed by an agent that did not write it, and stage is checked by a fresh agent that has built nothing in the project. The agent that starts QA does not write its brief.'),
    ('A history that answers questions', 'Every merge is a real merge that names both branches and its pull request. Which of development, stage and main hold a piece of work is read from the history, not set by hand.'),
]
STATIONS = [
    ('feat', 'The feature\'s own folder', 'Its own tests, those that name its scenarios, after it has pulled main', 'A passing run, for the commit it was run on'),
    ('feat', 'Code review', 'The code and its tests, on the feature\'s own branch, by an agent that did not write them', 'A report: the decision, and each finding with its kind and how it ended'),
    ('dev', 'development', 'Nothing is run. The features are merged', 'A conflict between features shows, and is resolved by a merge branch'),
    ('stage', 'The suite\'s run', 'The whole suite, once, on the named commit of stage', 'The commit, and each command with its result'),
    ('stage', 'QA', 'Each scenario the release names, read against its tests and checked by hand where they fall short, by a fresh agent. It does not run the suite', 'QA\'s report: the commit checked, the result for each scenario, and what was checked by hand'),
    ('main', 'Promotion', 'The maintainer\'s acceptance', 'The promotion of stage to main, and the release\'s two tags'),
]


def addup():
    rows = ''.join(f'<tr class="c-{c}"><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(w)}</td></tr>' for c, a, b, w in STATIONS)
    return (f'<ul class="gives two">{cards(ADDUP)}</ul>'
            '<h3 class="sub">Fixed places to test</h3>'
            '<p class="note">The road has stations. Each has its check and what comes of it, so nobody has to invent where testing happens. Nothing is checked twice on code that has not changed.</p>'
            '<div class="tablewrap"><table><thead><tr><th>Station</th><th>What is checked</th><th>What comes of it</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


PROBLEMS = [
    ('One unfinished feature is blocking the release.', 'A release is built from the features on its list. The unfinished one stays on development.'),
    ('We need a code freeze before every release.', 'development never freezes. The release is built on stage, apart from ongoing work.'),
    ('Merge hell on long-lived branches.', 'Features are built to be independent, and conflicts surface on development early. A conflict resolved once can be replayed by Git\'s recorded resolutions (rerere), on the machine that resolved it.'),
    ('The hotfix never made it back, and the bug returned.', 'A hotfix takes the same road, and main is merged into development straight after, which is how development gets the fix.'),
    ('It worked in testing but not in the release.', 'The whole suite is run on stage, which holds exactly what ships, and what is verified there is what is promoted: nothing is changed on stage itself.'),
    ('We run the same tests again and again.', 'A step is taken only when what starts it has happened. A feature\'s own tests run when its code changes. Nothing is run on development. The whole suite runs once, on stage, and again only if stage changes.'),
    ('We reverted it and now the history is a mess.', 'Before promotion nothing is reverted: stage is rebuilt without the feature. A bad release already on main is put back by deploying the previous release again, then corrected by a hotfix. main is never reverted.'),
    ('Nobody knows what is actually in this release.', 'The release list is named feature by feature, and the history names every branch merged and the pull request that merged it.'),
    ('QA is a rubber stamp, or the author tested their own work.', 'QA is done by a fresh agent that has built nothing in the project. It reads each scenario against the tests that name it, checks by hand what they miss, and gives a result scenario by scenario. Its brief is fixed text: the agent that starts QA sends it as written, filling in only what it leaves open.'),
]


def problems():
    rows = ''.join(f'<tr><td class="q">&ldquo;{esc(a)}&rdquo;</td><td>{esc(b)}</td></tr>' for a, b in PROBLEMS)
    return ('<div class="tablewrap"><table class="two"><thead><tr><th>The complaint</th><th>What this method does</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


DORA = 'https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf'
HARV = 'https://fion.ac/jellyfish.pdf'
AI = [
    ('AI writes faster than we can review.',
     f'A Harvard working paper by Fiona Chen and James Stratton, <a href="{HARV}">Artificial Intelligence in the Firm: Bottlenecks in Software Production</a>, finds that after firms adopted coding agents there were more commits and more pull requests, the time from a pull request to its merge grew, and the rise in resolved issues was not statistically significant.',
     'Every feature arrives at code review with its scenarios written and its own tests passing, so code review is not the first check. The strictest checking, QA, is spent only on what is chosen to ship.',
     'The method does not remove the cost of code review. That is why the rework each code review causes is said, and discussed with the user.'),
    ('We are faster, but less stable.',
     f'Google\'s <a href="{DORA}">2025 DORA report</a> found that adopting AI now improves software delivery throughput and still increases delivery instability.',
     'The method holds work to two standards: fast into development, strict at stage. Instability is meant to be met at that gate, before a release, with each feature small and independent.', ''),
    ('Running agents in parallel just moves the conflicts to merge time.',
     'Practitioners report that separate folders stop agents overwriting each other but do not prevent conflicts, that two agents told to work the backlog pick the same task, and that the person ends up as the coordination layer.',
     'One piece of work to a branch, each in a folder of its own, and before starting an agent makes sure no other agent holds the same work. development is where conflicts are meant to surface, and a conflict resolved once is replayed by Git\'s recorded resolutions.',
     'The flow does not say how work is assigned. That is the project\'s to arrange, by whatever means it has.'),
    ('Who wrote this, and can we prove it?',
     'There are new tools for attributing lines to an AI, and no accepted standard yet for naming one in a commit.',
     'Every commit ends with lines naming the contributor and the agent, and every merge made by pull request names its pull request. The person directing the work is its author, whatever share the agent typed.', ''),
    ('We are drowning in low-quality AI contributions.',
     'Open-source maintainers are adopting policies on AI-assisted contributions. The measures in use include disclosure of AI use, evidence that a change was built and tested, and, on some projects, accepting an AI-assisted change only for an issue already accepted.',
     'All three are this method\'s defaults: work starts from what is written down and ready, attribution is on every commit, and a feature\'s tests pass before it is merged anywhere. Small changes are its aim, and nothing enforces them.', ''),
]


def ai():
    out = []
    for q, said, does, still in AI:
        extra = f'<dt>What stays true</dt><dd>{esc(still)}</dd>' if still else ''
        out.append(f'<li><h3>&ldquo;{esc(q)}&rdquo;</h3><dl><dt>What is reported</dt><dd>{said}</dd><dt>What this method does</dt><dd>{esc(does)}</dd>{extra}</dl></li>')
    return ('<ul class="talks">' + ''.join(out) + '</ul>'
            '<p class="note">What other teams report is taken from published reports and practitioner writing gathered on November 21, 2026. The Harvard paper has been revised and its figures have changed between versions, so none is quoted here. Every source is listed under <a href="#sources">Sources</a>.</p>')


def conflict_notes():
    return ('<p class="note"><b>A merge resolves its conflict and nothing else.</b> Any other change features need in order to work together is written on a feature\'s own branch, never in a merge and never on <code>development</code> or <code>stage</code>, and the feature is merged again. Where such a change is only right with the other features present, those features require each other, and the answer is a coordination.</p>'
            '<p class="note"><b>A conflict GitHub reports and Git does not have.</b> A feature cut from <code>main</code> after a release holds every released feature. <code>development</code> holds the same features by another route, their own pull requests. Until the two are joined they share each released feature separately, and GitHub reports a conflict on a pull request that Git on a machine merges cleanly. The cure is to bring the two level after every release and hotfix: <code>development</code> is rebuilt from <code>main</code> after a release, and <code>main</code> goes into it by pull request after a hotfix or where it is left running. If the merge branch has become routine, something has not been merged that should have been, and that is what to say.</p>')


# What a project on the flow has to be -------------------------------------------------
SETUP = [
    ('<code>development</code> and <code>stage</code>, created from <code>main</code> when the project starts',
     'Both are permanent. <code>development</code> receives features to be merged, and <code>stage</code> receives the release list.',
     'git fetch origin\ngit push origin origin/main:refs/heads/development origin/main:refs/heads/stage'),
    ('Protection of <code>main</code> on GitHub',
     'Force pushes are blocked and deletion is blocked. It changes only by a pull request, from <code>stage</code>.', ''),
    ('Protection of <code>development</code> and <code>stage</code>',
     'They change only by a pull request, and deletion is blocked. A force push is allowed only to whoever resets one of them to <code>main</code>.', ''),
    ('The repository\'s merge settings',
     'Merge commits only, with squash merging and rebase merging turned off, so a pull request cannot be merged any other way. A branch is not required to be up to date before merging, since that would need <code>development</code> or <code>stage</code> merged into the feature.', ''),
    ('Reuse of recorded resolutions, once per clone',
     'A conflict resolved once is replayed when the same feature meets it again, on <code>stage</code> or after a reset, in the clone that recorded it.',
     'git config rerere.enabled true'),
    ('A folder for each branch an agent works on',
     'Each feature has a folder of its own, a Git worktree, so no two people or agents share a checkout.',
     'git config worktree.useRelativePaths true'),
]
KEPT = [
    ('Before a branch exists', 'What is to be built, with a story and scenarios where it is new behaviour. A fix names the scenario it restores, or adds one for the fault.'),
    ('At the feature', 'The test run and the commit it was run on. The code review: the decision, and each finding with its kind and how it ended, and how much rework it caused.'),
    ('The release list', 'The features the release is to hold, as the maintainer named them, kept where the maintainer and the agents read the same list.'),
    ('At stage', 'The suite\'s run: the commit, each command with its result, and the regression count. QA\'s report: the result for each scenario, what was checked by hand, and what could not be done.'),
    ('At promotion', 'The maintainer\'s word to promote, and the release\'s two tags on main.'),
]


def first():
    rows = ''.join(f'<tr><td>{a}</td><td>{b}{"<pre>" + esc(c) + "</pre>" if c else ""}</td></tr>' for a, b, c in SETUP)
    return [
        ('commits', 'What using the flow commits a project to',
         '<p class="say">Using Feature Promotion Flow commits a project to three permanent branches and one rule about where work starts: every feature is cut from <code>main</code>, and from nowhere else.</p>'
         '<p class="note"><code>main</code> is what is released. <code>development</code> receives features, so that they are merged in one place and any conflict between them shows; nothing is run on it. <code>stage</code> receives the release list the maintainer named. All three change only by pull request, merged as real merges and never squashed.</p>'
         '<p class="note">The branches are not environments, though in a project they may map to them. Every step is plain Git, with pull requests on GitHub, and can be done by hand.</p>'),
        ('setup', 'What is set up once',
         '<p class="say">A project is set up for the flow once, when it starts. Nothing here needs a tool beyond Git and GitHub.</p>'
         '<div class="tablewrap"><table class="setup"><thead><tr><th>What is set up</th><th>What it is for</th></tr></thead>'
         f'<tbody>{rows}</tbody></table></div>'),
        ('kept', 'Where the work is written down',
         '<p class="say">The flow says what is written down, reviewed, reported and decided. It does not say where. Where a project keeps its backlog, its decisions and its code reviews is in that project\'s own instructions.</p>'
         f'<ul class="gives two">{cards(KEPT)}</ul>'
         '<p class="note">Docket is one place to keep all of it: as files in the repository, on a branch of their own that every feature is cut from. The other tab, Feature Promotion Flow with Docket, describes the flow in a project that does.</p>'),
        ('opt-out', 'A project that does not use it',
         '<p class="say">Feature Promotion Flow is the preference, and the maintainer can say it is not necessary for a particular project, such as a repository of documents.</p>'
         '<p class="note">There, none of this applies. The project has no <code>development</code> or <code>stage</code> branch, and its commits go to <code>main</code>.</p>'),
    ]


SOURCES = [
    ('The method', [
        ('The development standards this guide is drawn from', '', 'The rules and the steps, as they stood on November 24, 2026. They are Lucidex Group\'s own and are not published; every rule and figure here is drawn from them.', 'source'),
        ("gitworkflows, in Git's manual", 'https://git-scm.com/docs/gitworkflows', "The Git project's own method, and the parent of this one: topic branches that graduate through integration branches, throw-away integration, tagged releases.", 'named in the standards; read at its source'),
        ('gitworkflow, explained for other teams', 'https://github.com/rocketraman/gitworkflow', 'The same method set out for teams outside the Git project.', 'named in the standards; not opened in this check'),
        ('Branch Per Feature, Adam Dymitruk, 2012', 'https://dymitruk.com/blog/2012/02/05/branch-per-feature/', 'The closest published method: every feature starts from the same commit, and a release is assembled from the features that are ready.', 'named in the standards; not opened in this check'),
        ('Branch Per Feature in practice', 'https://bitbashing.io/2015/02/10/bpf-in-practice.html', 'An account of using it on one project for most of a year: a release is built by merging in the features that are ready.', 'named in the standards; read at its source'),
        ('FeiFlow, Maksym Moyseyev, 2024', 'https://dev.to/feiflow/feiflow-an-opinioned-git-branching-and-release-management-strategy-33l3', 'Similar in one respect: an integration branch that is never merged anywhere and is rebuilt to clear it.', 'named in the standards; read at its source'),
    ]),
    ('What other teams report', [
        ('DORA 2025: State of AI-assisted Software Development', DORA, 'AI adoption now improves software delivery throughput and still increases delivery instability. Used in "We are faster, but less stable."', 'checked at its source'),
        ('Artificial Intelligence in the Firm: Bottlenecks in Software Production, Fiona Chen and James Stratton, Harvard working paper', HARV, 'After firms adopted coding agents: more commits and pull requests, a longer time from pull request to merge, and a rise in resolved issues that is not statistically significant. Used in "AI writes faster than we can review."', 'read at its source, in the version of November 19, 2026; the first third of the paper, which holds the findings'),
        ('5 Lessons from Running AI Coding Agents in Parallel, Batty', 'https://dev.to/battyterm/5-lessons-from-running-ai-coding-agents-in-parallel-53on', 'Two agents told to work the backlog took the same feature, separate folders leave the conflicts for merge time, and the work needs someone supervising. The source for "Running agents in parallel just moves the conflicts to merge time."', 'read at its source'),
        ('Git Worktrees Changed How I Run Parallel AI Agents, Batty', 'https://dev.to/battyterm/git-worktrees-changed-how-i-run-parallel-ai-agents-39pm', 'Separate folders stop agents overwriting each other, conflicts still come at merge time, and a person assigns the tasks and orders the merges. Used in the same conversation.', 'read at its source'),
        ('Identity-Attributed Git Commits via Tier-Structured Trailers, Blake Morrison, an Internet-Draft', 'https://datatracker.ietf.org/doc/draft-morrison-identity-attributed-commits/', 'One person\'s proposal, not adopted by any working group, for commit trailers that name the person and the AI tool. Evidence that naming an AI in a commit has proposals and no accepted standard. Used in "Who wrote this, and can we prove it?"', 'read at its source'),
        ('Git AI', 'https://github.com/git-ai-project/git-ai', 'A tool that records in Git notes which lines an agent wrote. The "new tools for attributing lines to an AI" in the same conversation.', 'read at its source'),
        ('AI Policy, Disclosure, and Human in the Loop: How Are Contribution Guidelines Adapting to GenAI?, Andre Hora and Romain Robbes, 2026', 'https://arxiv.org/abs/2605.16706', 'Of 1,000 popular repositories, 118 had a policy on AI. About half of those policies require disclosure, and most require a person in the loop. The source for "Open-source maintainers are adopting policies."', 'read at its source'),
        ("Stop Closing the Door. Fix the House., Angie Jones, O'Reilly Radar, 2026", 'https://www.oreilly.com/radar/stop-closing-the-door-fix-the-house/', "One maintainer's advice: say how AI may be used on the project, and ask contributors to disclose it and to build and test before opening a pull request. It reports one project accepting AI-assisted changes only for accepted issues, and argues against closing the door that way.", 'read at its source'),
    ]),
]


def sources():
    out = []
    for group, items in SOURCES:
        rows = ''.join(
            f'<tr><td>{f"<a href={chr(34)}{esc(u)}{chr(34)}>{esc(t)}</a>" if u else esc(t)}</td><td>{esc(d)}</td><td><span class="st">{esc(st)}</span></td></tr>'
            for t, u, d, st in items)
        out.append(f'<h3 class="sub">{esc(group)}</h3><div class="tablewrap"><table class="src"><thead><tr><th>Source</th><th>What it is used for</th><th>How far it was checked</th></tr></thead><tbody>{rows}</tbody></table></div>')
    return ''.join(out)


PARTS = [
    ('What a project on the flow has to be', 'For a person deciding whether to run a project this way, and anyone working in one that does.'),
    ('Why', 'For anyone deciding whether to work this way.'),
    ('The flow', 'How work moves from main to a release.'),
    ('Releases', 'Building one on stage, testing it, naming it.'),
    ('When things do not go to plan', 'Rework, failures, hotfixes, a bad release, conflicts and features that require each other.'),
    ('What not to do', 'The mistakes that cost a release later.'),
    ('Who decides what', 'What may be done without asking, and what waits for the maintainer.'),
]

SAID = 'It is said which step caught it, and what kind of fault it is.'


def doc():
    """The guide to the flow on its own, as parts and sections for the page to lay out."""
    drawing.use(NAMES, BR_TIP, NAME_TIP, link_tip, dot_tip)
    br = ''.join(f'<li class="c-{c}"><code>{esc(n)}</code><span>{esc(t)}</span></li>' for c, n, t in BRANCHES)
    S = [
        (2, 'limits', 'Its limits, stated first',
         'What has and has not been shown, what the method costs, what it leaves out, and how it compares with the most common alternative.',
         limits()),
        (2, 'addup', 'What the parts add up to',
         'Each of these comes from two or more pieces of the method working together, which is why no single rule delivers it.',
         addup()),
        (2, 'problems', 'Problems teams commonly report, and what this does about them',
         'Complaints teams commonly voice, with what this method does about each.',
         problems()),
        (2, 'agents', 'Working with AI agents',
         'Five conversations teams are having about building software with AI, and where this method answers them.',
         ai()),
        (3, 'road', 'The road from main, and back to it',
         'Work starts from <code>main</code> and ends on <code>main</code>. A feature is tested and code reviewed on its own branch, merged into <code>development</code> where nothing is run, and merged into <code>stage</code> only when it is on the release list.',
         fig(road(), 'Time runs left to right. Feature A is released. Feature B is on <code>development</code> and waits for a later release. No feature is ever cut from <code>development</code> or <code>stage</code>, and nothing pulls from them.')),
        (3, 'steps', 'One feature, step by step',
         'The same road as the section before, as eight cards for one feature, ending at promotion. Two standards apply. Building to <code>development</code> is fast. Choosing for <code>stage</code> is strict, and two of its steps wait for the maintainer.',
         steps()),
        (3, 'see', 'Seeing a feature before it is tested',
         'A person working with an agent will want to see what has been built before it goes anywhere. That is what a developer does while working on a feature, and it is an option, not a step of the testing process.',
         see()),
        (3, 'checks', 'The checks, in order',
         'Each word means one thing. A review is always a plan review or a code review.',
         checks()),
        (3, 'eligible', 'What makes a feature eligible for stage',
         'Being on <code>development</code> is not enough. These five conditions are the bar for <code>stage</code>. A feature below it is on the release list only by the maintainer\'s decision.',
         eligible()),
        (3, 'holds', 'What each branch holds',
         'A feature\'s folder always holds everything needed to build and test it: what is released, and its own code. Nothing of any other feature is in it.',
         holds()),
        (3, 'folders', 'Where everyone works',
         'One repository, checked out in several folders, so no two people or agents share a checkout.',
         folders()),
        (4, 'release', 'A release',
         'The same road, for three features. A release is built on <code>stage</code> from the features on its list, the whole suite is run there once, QA checks it, and it is promoted to <code>main</code> as a whole.',
         fig(release(), 'After the release <code>development</code> is rebuilt: reset to <code>main</code>, and feature B, still in progress, merged into it again without being tested or code reviewed again. No feature is sent back by the release. <code>stage</code> stays as it is: it already holds what <code>main</code> holds.')),
        (4, 'rebuild', 'Rebuilding development after a release',
         'After a release, <code>development</code> is usually reset to <code>main</code> and the features still in progress are merged into it again. By then most of what it held is released, so the reset costs little, and it keeps <code>development</code> from gathering merges that GitHub reads as conflicts.',
         rebuild()),
        (4, 'loop', 'The whole cycle, as a loop',
         'The same release, drawn as rings. Time runs clockwise from the top, and one turn is one release. Where the linear picture ends, this one begins again.',
         '<div class="loopwrap">' + fig(loop(), 'The rings are the branches, with <code>main</code> at the centre. A feature that is released ends when it reaches <code>stage</code>. A feature that waits goes all the way round, and an ordinary release breaks no ring.') + '</div>'),
        (4, 'testing', 'The testing process',
         'What is tested, where, and what starts it, as twelve steps. A step is taken when what starts it has happened, and not otherwise: nothing is run again on code that has not changed.',
         testing()),
        (4, 'history', 'How the history says where work is, and how a release is named',
         'A commit does not record its branch, but a merge\'s title names the branch merged and the branch merged into, and its body names the pull request that made it. Read by first parent, each permanent branch is one line per arrival.',
         history()),
        (5, 'rework', 'Rework after a code review',
         'A feature is code reviewed on its own branch, and its findings answered, before it is first merged into <code>development</code>, so that it is merged once. The builder classifies each finding and deals with it by its kind, and anything to fix is fixed where the feature was built.',
         fig(rework(), 'A feature that was already on <code>development</code> when it was reworked is merged into it again by pull request; <code>development</code> is not reset for it. How much rework each code review caused is said, and discussed with the user.') + findings()),
        (5, 'fails', 'When a feature fails on stage',
         'If <code>stage</code> fails, it is not left standing. A failed feature is not backed out. Usually it comes out, and <code>stage</code> is rebuilt without it; where the fault is small and quickly fixed on the feature\'s own branch, the feature may be merged again on top. Either way the suite is run on <code>stage</code> again.',
         fig(fails(noted=SAID), 'Shown: the usual case. <code>stage</code> is reset to <code>main</code>, the rest of the release list is merged into it again, and the suite is run again; QA\'s results for the features that remain stand. The fix is made on the feature\'s own branch, tested, and code reviewed where it is to a defect or a risk. A feature the maintainer did not list never goes in.') + resets()),
        (5, 'comeout', 'When items need to come out of development',
         'This is one reason to reset <code>development</code>; the cases are listed in the section before. After a release it is usually rebuilt, as the section on a release shows. Rebuilding it from a release list, to show that release running before <code>stage</code> is built, is a case of the same thing: everything outside the list comes out, and is merged in again afterwards.',
         fig(comeout(), 'When <code>development</code> is reset, every surviving feature is merged again, so the same conflict can come up again. Git\'s recorded resolutions replay it.')),
        (5, 'hotfix', 'A hotfix',
         'A hotfix is a fix that cannot wait for the next release. It takes a release\'s road from <code>stage</code> onward, alone. It does not pass through <code>development</code>, and it never goes straight to <code>main</code>.',
         fig(hotfix(), 'The fault is written down before the branch exists. Afterwards <code>development</code> gets the fix when <code>main</code> is merged into it by pull request. If the fix conflicts with a feature there, the conflict shows in that pull request.')),
        (5, 'rollback', 'A bad release already on main',
         'Rolling back is two things, in this order: put production back, then correct the release. <code>main</code> is never reverted or rewritten.',
         fig(rollback(), 'Putting production back is a deployment and changes nothing in Git. The reset of <code>stage</code> and the steps after a release are as in the hotfix above and are left out of this drawing.')),
        (5, 'conflict', 'Resolving a conflict',
         'Whoever opened the pull request resolves the conflict. Nothing is pushed to <code>development</code> or <code>stage</code> to get round one.',
         fig(conflict(), 'The same means serves <code>stage</code>. The merge is made on a machine, so Git\'s reuse of recorded resolutions (rerere, turned on once per clone) applies: the same conflict, resolved once, is replayed when it comes up again on that machine. The recordings are kept per clone, and Git has no means of sharing them, so a conflict resolved on <code>development</code> is replayed on <code>stage</code> only from the same clone; from another, it is resolved again. <code>stage</code> is the first place the release\'s features are together without the rest, so a conflict between them may first show there. A merge branch is for a real conflict, and it is the one branch ever cut from <code>development</code> or <code>stage</code>.') + conflict_notes()),
        (5, 'coordination', 'Features that require each other',
         'Sometimes one feature cannot be built or tested without another that is not yet released, or features work together only with a change that is right only with the others present. One answer is to wait for the first to be released. The other is a coordination, which lets them be worked on together while each stays on its own branch. Which is the maintainer\'s to decide.',
         fig(coordination(), 'A member\'s passing result was earned with the other members present, so it goes into <code>development</code> or <code>stage</code> only with, or after, the members it requires.') + mergeonly()),
        (6, 'cut', 'Why every branch is cut from main',
         'Git can merge a branch into any branch it shares an ancestor with. What the branch was cut from decides what comes with it. This is the rule the rest of the method rests on, and the first thing not to do.',
         fig(why(), 'Features A and B are already on <code>development</code>. Cut from there, feature X carries both into <code>stage</code>. Cut from <code>main</code>, which holds only what is released, it arrives alone and can be chosen for a release by itself. The other ways to end up carrying work that was not chosen are in the next section.')),
        (6, 'mistakes', 'The other mistakes, in pairs',
         'Cutting from <code>development</code>, above, is the plainest case. Each of these does the same kind of damage by another route: it looks harmless when it is done and costs a release later. Wrong on the left, right on the right.',
         fig(p_chain(), 'A feature cut from another, or with another merged into it, cannot be chosen for a release without it. Features that truly require each other are tied in a coordination instead.')
         + fig(p_pull(), 'A local copy of <code>development</code> or <code>stage</code> is for running and testing only. After a reset, a pull merges the old commits back in.')
         + fig(p_update(), 'Both of GitHub\'s buttons merge <code>development</code> into the feature. The feature then carries every other feature wherever it goes.')
         + fig(p_squash(), 'Every merge is a real merge, and its title names both branches. That is how the history says where work has been.')
         + fig(p_rebase(), 'A feature that has been merged anywhere is never rebased.')
         + fig(p_hotfix(), 'What is verified on <code>stage</code> is what ships. A hotfix is no exception.')
         + fig(p_backout(), 'Nothing is patched on <code>stage</code>. Usually it is reset, and the rest of the release list is merged again.')
         + rules()),
        (7, 'who', 'Who may do what without asking',
         'Work on a feature is free. Anything that changes what is released waits for the maintainer.',
         who()),
    ]
    return {
        'name': 'Feature Promotion Flow',
        'title': 'Feature Promotion Flow',
        'lede': 'How work moves from a feature to a release under Feature Promotion Flow: the branches, the checks, a release, and what to do when things do not go to plan. This is the flow on its own. The other tab adds what changes in a project that keeps its record with Docket.',
        'intro': 'Feature Promotion Flow is a way of branching and releasing. Every feature lives on its own branch, cut from <code>main</code>. Features are merged into <code>development</code>, where their conflicts show. A release is built on <code>stage</code> from the features the maintainer lists for it, tested and checked there, and promoted to <code>main</code>. Being on <code>development</code> says nothing about release: the release list is named, feature by feature.',
        'parts': PARTS,
        'first': [{'id': i, 'title': t, 'html': f'<section id="{i}"><header><h2>{t}</h2></header>{b}</section>'} for i, t, b in first()],
        'repo': ('https://github.com/Lucidex-Group/feature-promotion-flow', 'github.com/Lucidex-Group/feature-promotion-flow', 'This guide, its source, and the skills for the flow.'),
        'why': {'id': 'why', 'title': 'Why it exists, and why features are cut from main', 'html': purpose()},
        'legend': f'<div class="top legend"><h3 class="sub">The branches, and how to read the figures</h3><ul class="branches">{br}</ul>{KEY}{who3()}</div>',
        'sections': S,
        'sources': sources(),
        'sources_desc': 'Where the method comes from, and where each claim about other teams comes from, with how far each was checked.',
        'footer': 'Drawn from Lucidex Group\'s development standards, November 24, 2026. Branch names are the standard ones.',
    }
