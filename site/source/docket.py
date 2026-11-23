"""Feature Promotion Flow in a project on Docket: the words, figures and tables of the guide kept with Docket.

Taken from the guide kept with Docket, as it stood on November 22, 2026. The first part,
on what a project on Docket has to be, is from the design of the guide inside Docket.
"""
import drawing
from drawing import *
from shared import *

NAMES = {'record': 'docket-record', 'dev': 'development', 'stage': 'stage', 'main': 'main', 'hot': 'hotfix', 'coord': 'coordination'}

BR_TIP = {
    'record': 'docket-record: main plus everything recorded since. Work starts here, and no code is committed on it.',
    'feat': 'A feature branch: one work item\'s code, cut from the record and named from its work item.',
    'dev': 'development: where features are tested together. It may be broken, and being here does not mean release.',
    'stage': 'stage: the release. The chosen features, verified together. What is verified here is what ships.',
    'main': 'main: what is released. Only a promoted stage reaches it.',
    'hot': 'A hotfix: a fix that cannot wait for the next release, cut from the record and named from its incident.',
    'mrg': 'A merge branch: cut from the receiving branch as it is on GitHub, only to resolve a conflict.',
    'coord': 'A coordination branch: it holds only merges of features that require each other. No work is committed on it, and it is never merged anywhere.',
}
NAME_TIP = {
    'production': 'What is deployed and running. It is not a branch; it is shown here only to say which release is live.',
    'candidate': 'A candidate: main plus the release set, merged in release order on a machine, where the whole suite is run on the set before stage is built. It is never pushed and never merged anywhere.',
    'on GitHub': 'development as it is on GitHub. This is the branch; a copy on a machine is only a copy.',
    'your copy': 'A copy of development on a machine, for running and testing only. It is taken from GitHub with no local branch.',
    'a feature that waits': 'A feature that was tested but left out of this release. It goes round again.',
}
PR = ('gh pr create --base {to} --head {kind}/<id>-<name> --title "Merge branch \'{kind}/<id>-<name>\' into {to}"\n'
      'gh pr merge <number> --merge --subject "Merge branch \'{kind}/<id>-<name>\' into {to}" --body "Pull-request: <the pull request\'s URL>"')
REC = ('git push origin docket-record\n'
       'gh pr create --base {to} --head docket-record --title "Merge branch \'docket-record\' into {to}"\n'
       'gh pr merge <number> --merge --subject "Merge branch \'docket-record\' into {to}" --body "Pull-request: <the pull request\'s URL>"')
CUT = 'git worktree add -b {kind}/<id>-<name> ~/Development/worktrees/<Project>/{kind}-<id>-<name> docket-record'
RESET = 'git fetch origin\ngit push --force-with-lease origin origin/main:{to}'


def link_tip(fc, fid, tc, tid, dash):
    """What a link between two lanes is, and the command behind it."""
    if dash:
        if fc == 'main' and tc == 'record':
            return 'The record pulls main, in the record\'s own folder.', 'git fetch origin\ngit merge origin/main'
        if fc == 'record':
            return f'{tid} pulls the record. This writes only to that branch.', 'git merge docket-record'
        if fc == 'main':
            return f'{tid} is reset to main.', RESET.format(to=tid)
        return f'{tid} takes {fid}', None
    kind = 'hotfix' if 'hot' in (fc, tc) else 'feature'
    if fc == 'record' and tc == 'stage':
        return 'The record is merged into stage by one more pull request, so the release carries QA\'s result and the acceptance to main.', REC.format(to='stage')
    if fc == 'record' and tc == 'dev':
        return 'The record, having pulled main, is merged into development by pull request. This joins development to what was released. development usually stays as it is.', REC.format(to='development')
    if fc == 'record' and tc == 'coord':
        return 'The coordination branch is cut from the record and named from the coordination\'s work item.', CUT.format(kind='coordination')
    if tc == 'coord':
        return (f'{fid} is merged into the coordination branch. The work stays on the feature\'s own branch.',
                'git merge --no-ff feature/<member> -m "Merge branch \'feature/<member>\' into coordination/<id>-<name>"')
    if fc == 'record':
        return f'{tid} is cut from the record and named from its {"incident" if tc == "hot" else "work item"}.', CUT.format(kind=kind)
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
            return ('QA: the project\'s whole suite, run on stage itself by a fresh agent that has built nothing in the project. It answers for each scenario.',
                    'git fetch origin\ngit switch --detach origin/stage')
        if cls == 'mrg':
            return 'The conflict is resolved here, in the merge. The feature is not changed.', None
        if cls == 'coord':
            return 'The members are tested together here. The result is recorded on the member\'s own work item, naming the commit of each member.', None
        return 'Code review, by an agent that did not write the code.', None
    if kind == 'x':
        return ('The pull request does not merge.', None) if cls == 'dev' else ('A feature fails when stage is verified.', None)
    if kind == 'm':
        if cls == 'main':
            return 'A release: stage promoted to main.', None
        if cls in ('dev', 'stage'):
            return f'A feature merged into {bid}, by pull request.', None
        return f'A merge into {bid}.', None
    if cls == 'record':
        return 'A change to the record, committed whenever the record changes.', 'git add -A\ngit commit'
    return f'A commit on {bid}. Commit as often as needed.', None


# 1. The road -----------------------------------------------------------------
JOIN = 'The record, now holding the release, is merged into development by pull request. This joins development to what was released; the section on resolving a conflict says why that matters.'
READY = 'The work is readied on the record: its work item, and its story and scenarios where it is new behaviour, are written and committed there. The work item names its scenarios or says why it has none. Until then it is still backlog and has no branch.'
QA_SAY = 'QA: the project\'s whole suite is run on stage itself, by a fresh agent that has built nothing in the project. It answers for each scenario and records its own run in the record, so the record says who ran it. It fixes nothing and pushes nothing.'
REC_SAY = 'The maintainer accepts the release, which is the word to promote. QA has already recorded its own run, against the commit it tested. The acceptance is recorded in the maintainer\'s words, and the record is merged into stage by one more pull request, so the release carries both to main. A check confirms that nothing but the record changed on stage since the commit QA tested.'
PROMOTE_SAY = 'On that same word, the agent that assembled stage promotes it to main by pull request and tags the release twice: a name of version, pull request and date for people, and the bare version for tools.'


def road():
    f = Fig(1100, 478, 'One feature travels from the record, through development and stage, to main; a second feature stays on development.')
    R, A, B, D, S, M = 62, 140, 204, 284, 352, 420
    f.lane('record', R); f.lane('dev', D); f.lane('stage', S); f.lane('main', M)
    f.dot('record', 212, R)
    f.dot('main', 212, M, 'm'); f.tag(212, M, 'last release')
    f.step(READY)
    f.dot('record', 250, R)
    f.label(231, R - 34, 'A is readied: work item,\nstory and scenarios')
    f.step('A branch is cut from the record and named from its work item. A second feature is cut the same way. Neither holds anything of the other.')
    f.link('record', 262, R, 318, A)
    f.lane('feat', A, [(318, 690)], 'feature A')
    f.label(300, A + 26, 'cut from the record,\nnamed from its work item')
    for x in (348, 392):
        f.dot('feat', x, A)
    f.dot('record', 372, R)
    f.link('record', 384, R, 432, B)
    f.lane('feat', B, [(432, 622)], 'feature B')
    for x in (462, 500):
        f.dot('feat', x, B)
    f.step('Feature A\'s own tests pass in its own folder. Then its code is reviewed on its own branch by an agent that did not write it, and each finding is answered, before the feature goes anywhere. The test run and the code review are recorded, and the feature pulls the record, so it carries them onward.')
    f.dot('feat', 450, A, 'q'); f.label(424, A + 28, 'code reviewed', 'start')
    f.dot('record', 470, R)
    f.link('record', 482, R, 530, A, dash=True)
    f.dot('feat', 530, A, 'm')
    f.label(540, R + 30, 'pulls the record', 'start')
    f.step('Each feature, code reviewed on its own branch, is merged into development by its own pull request, once, and they are tested together. Being on development does not mean a feature will be released.')
    f.dot('feat', 546, B, 'q')
    f.link('feat', 542, A, 610, D); f.dot('dev', 610, D, 'm')
    f.link('feat', 622, B, 668, D); f.dot('dev', 668, D, 'm')
    f.label(640, D + 28, 'tested together')
    f.step('The maintainer chooses feature A for the release. The chosen set is first built and tested as a candidate on a machine, which a later section shows. Then feature A is merged into stage from its own branch, so it arrives without feature B.')
    f.link('feat', 690, A, 766, S); f.dot('stage', 766, S, 'm')
    f.label(752, A + 5, 'chosen for the release', 'start')
    f.step(QA_SAY)
    f.dot('stage', 808, S, 'q'); f.label(808, S - 20, 'verified')
    f.step(REC_SAY)
    f.dot('record', 838, R)
    f.link('record', 848, R, 888, S); f.dot('stage', 888, S, 'm')
    f.label(832, R - 18, 'QA and acceptance recorded', 'end')
    f.step(PROMOTE_SAY)
    f.link('stage', 904, S, 946, M); f.dot('main', 946, M, 'm'); f.tag(946, M, 'release')
    f.step('The record pulls main. It is again main plus everything recorded since, and the next feature is cut from there. development and stage usually stay as they are: stage already holds what main holds, and the released feature is already on development.')
    f.link('main', 960, M, 1004, R, dash=True); f.dot('record', 1004, R, 'm')
    f.label(1010, R - 18, 'the record pulls main', 'end')
    f.step(JOIN)
    f.link('record', 1018, R, 1060, D); f.dot('dev', 1060, D, 'm')
    f.label(1076, D + 28, 'development is joined', 'end')
    return f


# A release ---------------------------------------------------------------------
def release():
    f = Fig(1100, 492, 'Three features are each code reviewed on their own branch, then tested together. Two are chosen for the release, verified on stage, and promoted to main with the record. Afterwards the record pulls main and the feature left out pulls the record; development and stage usually stay as they are.')
    R, A, B, C, D, S, M = 74, 136, 188, 240, 310, 372, 436
    f.band(160, 438, '1  Code reviewed, tested together')
    f.band(438, 676, '2  The release set, on stage', alt=True)
    f.band(676, 890, '3  Recorded, promoted, tagged')
    f.band(890, 1100, '4  After the release', alt=True)
    f.lane('record', R)
    f.lane('feat', A, [(X0, 466)], 'feature A')
    f.lane('feat', B, None, 'feature B')
    f.lane('feat', C, [(X0, 536)], 'feature C')
    f.lane('dev', D); f.lane('stage', S); f.lane('main', M)
    for x, y in ((200, A), (212, B), (224, C), (200, R), (330, R)):
        f.dot('feat' if y != R else 'record', x, y)
    f.step('Each of three features passes its own tests in its own folder and is code reviewed on its own branch, with the findings answered. Then each is merged into development by its own pull request, once, and they are tested together. development may be broken; that is what it is there to find.')
    for x, y in ((224, A), (238, B), (298, C)):
        f.dot('feat', x, y, 'q')
    for x, y in ((246, A), (306, B), (366, C)):
        f.link('feat', x, y, x + 46, D); f.dot('dev', x + 46, D, 'm')
    f.step('The maintainer chooses A and C for the release. The set is first built as a candidate on a machine and the whole suite is run on it, which a later section shows. Then each is merged into stage from its own branch, in the same order, one pull request each. B is left out.')
    f.link('feat', 466, A, 524, S); f.dot('stage', 524, S, 'm')
    f.link('feat', 536, C, 588, S); f.dot('stage', 588, S, 'm')
    f.label(604, B - 10, 'left out of this release', 'start')
    f.step(QA_SAY + ' A pass on development proves nothing about the release.')
    f.dot('stage', 642, S, 'q'); f.label(642, S + 30, 'verified')
    f.step(REC_SAY)
    f.dot('record', 700, R)
    f.link('record', 712, R, 762, S); f.dot('stage', 762, S, 'm')
    f.label(690, R - 18, 'QA and acceptance recorded', 'start')
    f.step(PROMOTE_SAY)
    f.link('stage', 782, S, 830, M); f.dot('main', 830, M, 'm'); f.tag(830, M, 'release')
    f.step('The record pulls main, so the record branch holds the release.')
    f.link('main', 848, M, 904, R, dash=True); f.dot('record', 904, R, 'm')
    f.label(914, R - 18, 'the record pulls main', 'start')
    f.step(JOIN)
    f.link('record', 920, R, 968, D); f.dot('dev', 968, D, 'm')
    f.label(968, D + 28, 'development is joined')
    f.step('Feature B, still in progress, pulls the record. It is already on development and stays there. development and stage usually stay as they are after a release: stage holds what main holds, and the released features are already on development.')
    f.link('record', 1000, R, 1046, B, dash=True); f.dot('feat', 1046, B, 'm')
    return f



# Rework after a code review -------------------------------------------------------
def rework():
    f = Fig(1100, 350, 'A feature is code reviewed on its own branch before its first merge. Each finding is classified and dealt with by its kind. A defect or a risk is fixed on the feature\'s own branch and the fix is code reviewed. The feature is then merged into development once, and on stage it gets QA only.')
    R, A, D, S = 62, 132, 212, 292
    f.lane('record', R); f.lane('feat', A, [(X0, 800)], 'feature A'); f.lane('dev', D); f.lane('stage', S)
    for x in (206, 244):
        f.dot('feat', x, A)
    f.step('The feature is built and its own tests pass in its own folder. Before it is merged anywhere, its code is reviewed on its own branch by an agent that did not write it. The code review reads the feature\'s own code and tests, and reports findings.')
    f.dot('feat', 310, A, 'x', tip='The code review reports findings. The builder checks each one against the source, the file and the line, before accepting it.')
    f.label(310, A - 20, 'code review: findings', strong=True)
    f.step('The builder classifies each finding, and acts on its kind: a defect, a risk, a missing or weak test, untrue wording, design or style, or wrong. The reviewer\'s own label, blocking or not, is not the classification. The table below says what happens to each kind.')
    f.label(310, A + 26, 'each finding classified\nby its kind')
    f.step('A defect, and a risk that is not put to the maintainer, is fixed on the feature\'s own branch. Where the feature\'s attempt has already ended, the work item goes back to active and gets a new attempt for the rework, with an estimate, naming the findings. Any agent may take it, by assignment.')
    f.dot('record', 420, R, tip='Where the feature\'s attempt has already ended, the work item goes back to active, with a new attempt for the rework. The record says who wrote the feature and who reworked it.')
    f.label(420, R - 18, 'the rework is recorded')
    for x in (470, 510):
        f.dot('feat', x, A)
    f.label(490, A + 26, 'fixed on its own branch')
    f.step('The rework is code reviewed again only when it fixed a defect or a risk. That code review reads whether the fix closes the finding, and what the fix itself changed; it is not a second reading of the feature. Rework for a test, for wording or for a backlog item is not code reviewed again.')
    f.dot('feat', 580, A, 'q', tip='The code review of the fix: whether it closes the finding, and what the fix itself changed.')
    f.label(580, A - 20, 'the fix is code reviewed')
    f.step('The code review is recorded beside the work item: the decision, and each finding with its kind and how it ended. The feature pulls the record and is merged into development by pull request, once, and tested with the others.')
    f.dot('record', 640, R, tip='The code review is recorded beside the work item: the decision, and each finding with its kind and how it ended.')
    f.link('record', 652, R, 700, A, dash=True); f.dot('feat', 700, A, 'm')
    f.link('feat', 716, A, 766, D); f.dot('dev', 766, D, 'm')
    f.label(750, D + 28, 'merged into development once', 'end')
    f.step('When it is chosen, it is merged into stage from its own branch. Nothing is code reviewed on stage: each feature\'s code review was done once, at the feature, and stage gets QA only, by a fresh agent.')
    f.link('feat', 800, A, 860, S); f.dot('stage', 860, S, 'm')
    f.dot('stage', 920, S, 'q')
    f.label(920, S + 30, 'QA only')
    return f


FINDINGS = [
    ('Defect', 'The code does not do what a scenario or a stated requirement says.', 'Fixed on the feature\'s own branch.'),
    ('Risk', 'The tests pass, but a wrong thing can happen: lost data, a race, an unsafe command.', 'Fixed, or put to the maintainer to accept as it is.'),
    ('Missing or weak test', 'A scenario, or part of one, that no test really checks.', 'Fixed where the scenario is otherwise unverified; otherwise recorded, for QA to report.'),
    ('Untrue wording', 'A document, a message or a comment that says something untrue.', 'Fixed. It never holds a feature back on its own.'),
    ('Design or style', 'A preference about how the code is shaped, with no defect or risk in it.', 'Recorded as a backlog item. It never holds a feature back.'),
    ('Wrong', 'The finding misreads the code or a convention of the repository.', 'Rejected with the evidence. A tie-breaker confirms it: any agent that neither wrote the code nor raised the finding, given the finding and the evidence. It is then listed for the maintainer with its reason, and the work moves on; it is not asked.'),
]


def findings():
    rows = ''.join(f'<tr><td><b>{esc(k)}</b></td><td>{esc(w)}</td><td>{esc(h)}</td></tr>' for k, w, h in FINDINGS)
    return ('<div class="tablewrap"><table><thead><tr><th>Kind of finding</th><th>What it is</th><th>What happens to it</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>'
            '<p class="note">The builder classifies each finding; the reviewer\'s own label, blocking or not, is not the classification. A finding put to the maintainer keeps the feature out of <code>stage</code> until it is answered, and the answer, to fix it or to accept it as it is, is recorded. The reviewer first reads what is already settled, the project\'s decisions and the code review records of earlier features, so a finding already rejected is not raised again unless something has changed.</p>')



# Features that require each other ----------------------------------------------------
def coordination():
    f = Fig(1100, 424, 'Two features that require each other are each cut from the record. A coordination branch holds only merges of them, where they are tested together. Each then goes to development from its own branch.')
    R, A, K, B, D = 62, 132, 204, 276, 356
    f.lane('record', R); f.lane('dev', D)
    f.dot('record', 204, R)
    f.step('Feature B cannot be built or tested without feature A, which is not released; or the two work together only with a change to one of them that is right only with the other present. The maintainer ties them in a coordination: a work item that names its members, as many as require each other, and holds their shared history.')
    f.dot('record', 244, R, tip='The coordination\'s work item. It names its members and holds the history; it holds no work of its own.')
    f.label(244, R - 18, 'the coordination is recorded')
    f.step('Each member is cut from the record on its own branch, as any feature is.')
    f.link('record', 262, R, 310, A); f.lane('feat', A, [(310, 930)], 'feature A')
    f.link('record', 282, R, 350, B); f.lane('feat', B, [(350, 1000)], 'feature B')
    f.dot('feat', 350, A); f.dot('feat', 392, B)
    f.step('A coordination branch is cut from the record and named from the coordination\'s work item. It holds only merges of its members; no work is committed on it.')
    f.dot('record', 380, R)
    f.link('record', 394, R, 450, K); f.lane('coord', K, [(450, 850)])
    f.link('feat', 470, A, 516, K); f.dot('coord', 516, K, 'm')
    f.link('feat', 500, B, 556, K); f.dot('coord', 556, K, 'm')
    f.step('The members are tested together in the coordination branch\'s folder. A result made here is recorded on the member\'s own work item, and names the commit of each member it was run with.')
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


# A hotfix ----------------------------------------------------------------------
def hotfix():
    f = Fig(1100, 424, 'An incident is recorded, a hotfix is cut from the record, stage is reset, and the hotfix is released alone through stage to main. Development then gets the fix from the record.')
    R, H, D, S, M = 70, 148, 228, 296, 364
    f.lane('record', R); f.lane('dev', D)
    f.lane('stage', S, [(X0, 416)])
    f.lane('main', M)
    f.label(560, D - 12, 'the hotfix does not pass through development')
    f.step('The record pulls main, so it is up to what is released.')
    f.link('main', 196, M, 262, R, dash=True); f.dot('record', 262, R, 'm')
    f.label(274, R - 18, '1  the record pulls main', 'end')
    f.step('The incident is recorded on the record, as a work item of the incident kind, and committed. The decision to make a hotfix is itself recorded.')
    f.dot('record', 330, R)
    f.label(300, R - 18, '2  the incident is recorded', 'start')
    f.step('The hotfix is cut from the record and named from the incident. It is a branch from what is released that already holds its own record.')
    f.link('record', 342, R, 392, H)
    f.lane('hot', H, [(392, 680)], 'hotfix')
    f.label(404, H + 26, '3  the hotfix is cut\nfrom the record', 'start')
    f.step('stage is reset to main. A release that was being assembled there is set aside, and is merged into stage again once the hotfix is out.')
    f.lane('stage', S, [(462, 1076)], pill=False)
    f.link('main', 412, M, 462, S, dash=True); f.dot('stage', 462, S, 'c')
    f.label(446, M + 24, '4  stage is reset to main')
    f.step('The fix is made and tested, the record is pulled, and the fix\'s code is reviewed by an agent that did not write it. Then it is merged into stage by pull request.')
    for x in (444, 496):
        f.dot('hot', x, H)
    f.link('record', 530, R, 578, H, dash=True); f.dot('hot', 578, H, 'm')
    f.dot('hot', 630, H, 'q')
    f.label(594, H - 20, '5  fixed, tested, code reviewed', 'start')
    f.link('hot', 680, H, 740, S); f.dot('stage', 740, S, 'm')
    f.step('stage is verified by a fresh agent; the set is the one fix, so there is no candidate to build first. If it fails, the fix is corrected on the hotfix branch and code reviewed there, stage is reset to main again, and the fix is merged and checked again. Then the record is brought into stage, and it is promoted to main and tagged, on the maintainer\'s word. The hotfix never goes straight to main.')
    f.dot('stage', 792, S, 'q'); f.label(780, S + 30, '6  verified')
    f.dot('record', 800, R)
    f.link('record', 812, R, 852, S); f.dot('stage', 852, S, 'm')
    f.link('stage', 870, S, 914, M); f.dot('main', 914, M, 'm'); f.tag(914, M, 'release')
    f.step('As after any release, the record pulls main, and every feature in progress pulls the record. stage already holds what main holds.')
    f.link('main', 930, M, 980, R, dash=True); f.dot('record', 980, R, 'm')
    f.label(974, R - 18, '7  the record pulls main', 'end')
    f.step('development does not hold the fix. It gets it from the record, which now holds it, by pull request. This is the same step as after any release. development need not be reset for a hotfix, and the features on it stay where they are.')
    f.link('record', 996, R, 1046, D); f.dot('dev', 1046, D, 'm')
    f.label(1076, D + 28, '8  from the record', 'end')
    return f


# A bad release already on main ---------------------------------------------------
def rollback():
    f = Fig(1100, 438, 'A bad release already on main is put back by deploying the previous release again, which changes nothing in Git, and is then corrected by a hotfix that goes through stage like any other.')
    R, H, S, M, P = 62, 132, 202, 272, 356
    f.lane('record', R); f.lane('stage', S); f.lane('main', M)
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
    f.step('The bad release is then corrected by the hotfix road. The incident is recorded, and the hotfix is cut from the record. The fix may do no more than undo the bad change.')
    f.dot('record', 600, R, tip='The incident is recorded, as a work item of the incident kind. It says what was wrong with the release.')
    f.link('record', 612, R, 660, H); f.lane('hot', H, [(660, 800)], 'hotfix')
    f.dot('hot', 700, H); f.dot('hot', 750, H, 'q')
    f.label(600, R - 18, 'the incident is recorded')
    f.step('The hotfix goes through stage, is verified and is promoted like any other, and the corrected release is deployed. Nothing is reverted on main directly, and the bad release keeps its tag and its record.')
    f.link('hot', 800, H, 850, S); f.dot('stage', 850, S, 'm')
    f.dot('stage', 900, S, 'q')
    f.link('stage', 924, S, 970, M); f.dot('main', 970, M, 'm'); f.tag(970, M, 'v0.7.1', up=True)
    f.link('main', 986, M, 1034, P, tip='The corrected release, v0.7.1, is deployed to production.'); f.dot('mrg', 1034, P, 'm', tip='Production runs v0.7.1.')
    return f


# The loop ----------------------------------------------------------------------
def loop():
    f = Loop(1100, 820, 550, 412, 'One release drawn as a loop: a feature is cut from the record, code reviewed on its own branch, tested on development, chosen for stage, verified, and promoted to main with the record; the record pulls main and goes into development, features in progress pull the record, and the next turn begins. Development and stage usually stay as they are after a release.')
    Rr, A, B, D, S, M = 322, 280, 240, 198, 156, 114
    f.ring('record', Rr); f.ring('feat', B, None, 'a feature that waits'); f.ring('main', M)
    f.ring('dev', D); f.ring('stage', S)
    f.rdot('record', .02, Rr)
    cx, cy = f.cx, f.cy
    names = [('record', 'docket-record'), ('feat', 'a feature'), ('feat', 'a feature that waits'), ('dev', 'development'), ('stage', 'stage'), ('main', 'main')]
    f.txt.append(f.g(f'<text class="bt" x="{cx}" y="{cy - 54}" text-anchor="middle">from the outside in</text>'))
    for i, (c, n) in enumerate(names):
        f.txt.append(f.g(f'<rect class="namehit" x="{cx - 84}" y="{cy - 44 + 18 * i}" width="168" height="18"/>'
                         f'<text class="ringname c-{c}" x="{cx}" y="{cy - 31 + 18 * i}" text-anchor="middle">{esc(n)}</text>',
                         [n], NAME_TIP.get(n, BR_TIP[c]), None, True))
    f.step('Work is readied on the record, and a feature is cut from it, named from its work item.')
    f.rdot('record', .06, Rr)
    f.rlink('record', .08, Rr, .105, A)
    f.ring('feat', A, [(.105, .415)], 'a feature')
    for t in (.15, .2):
        f.rdot('feat', t, A)
    f.num(.118, A + 21, 1); f.out(.09, '1  a feature is cut\nfrom the record')
    f.step('Its own tests pass in its own folder, and its code is reviewed on its own branch, with each finding answered. Then it is merged into development, once, and tested together with the others.')
    f.rdot('feat', .24, A, 'q')
    f.rlink('feat', .272, A, .30, D); f.rdot('dev', .30, D, 'm')
    f.num(.318, D + 21, 2); f.out(.29, '2  code reviewed, then\ntested together')
    f.step('The maintainer chooses the release set. It is first built and tested as a candidate on a machine. Then each feature is merged into stage from its own branch, in the same order.')
    f.rlink('feat', .415, A, .455, S); f.rdot('stage', .455, S, 'm')
    f.num(.478, S + 21, 3); f.out(.44, '3  chosen for\nthe release')
    f.step(QA_SAY)
    f.rdot('stage', .515, S, 'q')
    f.num(.535, S + 23, 4); f.out(.515, '4  verified')
    f.step(REC_SAY)
    f.rdot('record', .555, Rr)
    f.rlink('record', .572, Rr, .612, S); f.rdot('stage', .612, S, 'm')
    f.num(.633, S + 21, 5); f.out(.585, '5  QA and acceptance\nrecorded, and brought in')
    f.step(PROMOTE_SAY)
    f.rlink('stage', .662, S, .692, M); f.rdot('main', .692, M, 'm')
    x, y = f.pt(.74, M + 21)
    f.tag(x, y - 27, 'release')
    f.num(.668, M + 21, 6); f.out(.68, '6  promoted\nand tagged')
    f.step('The record pulls main, so it is again main plus everything recorded since.')
    f.rlink('main', .765, M, .81, Rr, dash=True); f.rdot('record', .81, Rr, 'm')
    f.num(.826, Rr - 21, 7); f.out(.80, '7  the record\npulls main')
    f.step(JOIN)
    f.rlink('record', .835, Rr, .868, D); f.rdot('dev', .868, D, 'm')
    f.num(.886, D + 21, 8); f.out(.855, '8  the record goes\ninto development')
    f.step('Features still in progress pull the record. A feature that waits is already on development and goes round again. development and stage usually stay as they are after a release, and the next turn begins.')
    f.rlink('record', .915, Rr, .94, B, dash=True); f.rdot('feat', .94, B, 'm')
    f.num(.957, B + 21, 9); f.out(.93, '9  features in progress\npull the record')
    return f



def why():
    f, L, R = pair(300, 'cut a feature from development', 'cut it from the record', 'A feature cut from development carries every other feature into stage with it. A feature cut from the record arrives on stage alone.')
    D, X, S = 92, 162, 232
    L.lane('dev', D); L.lane('feat', X, [(346, 430)], 'feature X'); L.lane('stage', S)
    for x, t in ((226, 'A'), (276, 'B')):
        L.dot('dev', x, D, 'm'); L.label(x, D - 18, t)
    L.link('dev', 296, D, 346, X)
    L.dot('feat', 382, X)
    L.link('feat', 430, X, 480, S); L.dot('stage', 480, S, 'm')
    L.chips(392, S + 34, 'arrives on stage:', [('X', 'feat'), ('A', 'hot'), ('B', 'hot')])
    R2, X2, D2, S2 = 70, 130, 190, 250
    R.lane('record', R2); R.lane('feat', X2, [(300, 430)], 'feature X'); R.lane('dev', D2); R.lane('stage', S2)
    for x, t in ((226, 'A'), (276, 'B')):
        R.dot('dev', x, D2, 'm'); R.label(x, D2 + 26, t)
    R.dot('record', 214, R2)
    R.link('record', 250, R2, 300, X2)
    R.dot('feat', 340, X2)
    R.link('feat', 430, X2, 480, S2); R.dot('stage', 480, S2, 'm')
    R.chips(392, S2 + 34, 'arrives on stage:', [('X', 'feat')])
    return f


def p_chain():
    f, L, R = pair(276, 'cut one feature from another', 'cut each from the record', 'A feature cut from another feature carries it into stage. Cut from the record, each arrives alone.')
    Rc, A, B, S = 70, 120, 170, 220
    for H in (L, R):
        H.lane('record', Rc)
        H.lane('stage', S)
        H.dot('record', 200, Rc)
    L.link('record', 214, Rc, 254, A)
    L.lane('feat', A, [(254, 316)], 'feature A'); L.dot('feat', 284, A)
    L.link('feat', 316, A, 356, B)
    L.lane('feat', B, [(356, 430)], 'feature B'); L.dot('feat', 392, B)
    L.link('feat', 430, B, 476, S); L.dot('stage', 476, S, 'm')
    L.chips(398, 252, 'arrives on stage:', [('B', 'feat'), ('A', 'hot')])
    R.dot('record', 262, Rc)
    R.link('record', 214, Rc, 274, B)
    R.lane('feat', B, [(274, 430)], 'feature B'); R.dot('feat', 384, B)
    R.link('record', 276, Rc, 316, A)
    R.lane('feat', A, [(316, 390)], 'feature A'); R.dot('feat', 350, A)
    R.link('feat', 430, B, 476, S); R.dot('stage', 476, S, 'm')
    R.chips(398, 252, 'arrives on stage:', [('B', 'feat')])
    return f.svg()



CHECKS = [
    ('record', 'Plan', 'The files, the changes, their order, the risks and how the result will be verified.', 'The agent that will build', 'when', 'For work of sufficient complexity or risk'),
    ('record', 'Plan review', 'A reading of the plan against the code.', 'A second agent', 'when', 'When a plan needs a second opinion'),
    ('feat', 'Test', 'The feature\'s own tests and scenarios, run in the feature\'s own folder.', 'The agent that built it', 'always', 'Before its code review, and whenever it changes'),
    ('feat', 'Code review', 'A reading of the feature\'s own code and tests, on the feature\'s own branch. The builder checks each finding against the source, classifies it, and deals with it by its kind. A rework is code reviewed again only when it fixed a defect or a risk, and that code review reads the fix. Nothing is code reviewed on stage.', 'An agent that did not write it', 'always', 'Before the first merge into development, and for every hotfix'),
    ('dev', 'Testing together', 'The features on development, run together.', 'Whoever merged it', 'always', 'After each merge into development'),
    ('stage', 'QA', 'The independent check of stage. The whole suite, run on stage itself. It answers for each scenario: verified, partly verified, no test found, checked by hand, or failed, saying what failed and what kind of fault it is. It records its own run in the record, so the record says who ran it. It also confirms the list of what each feature has and lacks against the record. Its brief is fixed text, sent as written with its blanks filled in.', 'A fresh agent that has built nothing in the project', 'always', 'After the release set is on stage'),
    ('main', 'Acceptance', 'The word to promote stage to main. It is recorded, and travels to main with the release.', 'The maintainer', 'always', 'After QA'),
]


def checks():
    out = []
    for i, (cls, t, what, who, kind, when) in enumerate(CHECKS, 1):
        badge = '<span class="need">when needed</span>' if kind == 'when' else '<span class="need all">every time</span>'
        out.append(f'<li class="step c-{cls}"><span class="n">{i}</span><h3>{esc(t)}</h3><p>{esc(what)}</p>'
                   f'<dl><dt>Who</dt><dd>{esc(who)}</dd><dt>When</dt><dd>{esc(when)}</dd></dl>{badge}</li>')
    return '<ol class="steps seven">' + ''.join(out) + '</ol>'


HOLDS = [
    ('main', 'main', [('code', 'the released code'), ('rec', 'the record, as it stood at the release')]),
    ('record', 'docket-record', [('code', 'the released code'), ('rec', 'the record, as it stood at the release'), ('rec2', '+ everything recorded since')]),
    ('feat', 'a feature', [('code', 'the released code'), ('rec', 'the record, as it stood when the feature was cut'), ('rec2', '+ the record it has pulled since'), ('own', '+ this feature\'s code')]),
    ('dev', 'development', [('code', 'the released code'), ('rec', 'the record the features brought'), ('rec2', '+ the record, merged in after each release and hotfix'), ('own', '+ the code of every feature being tested')]),
    ('stage', 'stage', [('code', 'the released code'), ('rec', 'the record the features brought'), ('own', '+ the code of the release set'), ('rec2', '+ the record, merged in before promotion')]),
]


def holds():
    cols = []
    for cls, name, blocks in HOLDS:
        b = ''.join(f'<span class="blk {k}">{esc(t)}</span>' for k, t in reversed(blocks))
        cols.append(f'<div class="col c-{cls}"><div class="stack">{b}</div><code>{esc(name)}</code></div>')
    return '<div class="holds">' + ''.join(cols) + '</div>'


FOLDERS = [
    ('main', 'The project\'s own folder', '~/Development/<Project>', 'The user works here, on checked-out branches. An agent does not.'),
    ('record', 'The record\'s folder', '~/Development/worktrees/<Project>/docket-record', 'Docket is served from here. The record is written here, through Docket, and committed and pushed here whenever it changes.'),
    ('feat', 'A folder for each feature', '~/Development/worktrees/<Project>/feature-<id>-<name>', 'An agent works here, one folder to a branch, and never in a checkout someone else is using.'),
]


def folders():
    cards = ''.join(f'<li class="c-{c}"><h3>{esc(t)}</h3><code>{esc(p)}</code><p>{esc(d)}</p></li>' for c, t, p, d in FOLDERS)
    return f'<div class="repo"><span>one repository</span></div><ul class="folders">{cards}</ul>'


WHO = [
    ('Commit on the record branch', 'free', 'Whenever the record has changed'),
    ('Commit on a feature', 'free', 'As often as needed'),
    ('Push a feature, then open and merge its pull request into development', 'free', 'For work the user has said to work, once its code review is answered. A feature already on development is merged again after rework'),
    ('Open a pull request into stage', 'word', 'The maintainer chooses the release set. The word to build a release candidate covers its pull requests into stage. Including a feature below the bar is the maintainer\'s decision, and is recorded'),
    ('Promote stage to main, and tag the release', 'word', 'The maintainer\'s word to promote is acceptance. The agent that assembled stage performs it'),
    ('Push the record branch', 'free', 'Whenever it has been committed on, so every session and machine reads the same record'),
    ('Bring the record into stage, before promotion', 'word', 'Covered by the maintainer\'s word to promote'),
    ('Bring the record into development, after a release or a hotfix', 'word', 'Covered by the maintainer\'s word to promote'),
    ('Reset development', 'word', 'When that serves the work: usually when something has to come out of it, or to show a release candidate running. After an ordinary release it usually stays as it is'),
    ('Reset stage', 'word', 'Usually when a feature has failed on it, before a hotfix, and before a release set is assembled if it holds anything main does not. The word to build a release candidate covers the resets of stage that the candidate needs'),
    ('Change branch protection or repository settings', 'word', ''),
]


ELIGIBLE = [
    ('Its scenarios pass', 'Its work item names its scenarios, or says why it has none, and every scenario it names has a passing result recorded from the feature\'s own folder, for the code as it stands. A result made before the code last changed does not count; a pull of the record afterwards does not make it stale. A work item that names none must say why; silence does not meet this. For a member of a coordination, a passing result from the coordination branch\'s folder stands in its place when it is recorded on the member\'s work item, names the commit of each member, and no member has changed since.'),
    ('Its code is reviewed', 'By an agent that did not write it, with each finding dealt with as its kind requires. A finding put to the maintainer keeps the feature out until it is answered, and the answer, to fix it or to accept it as it is, is recorded.'),
    ('It has pulled the record', 'It has pulled the record since the last release, and after its own test run and code review were recorded, so it carries them.'),
    ('It stands alone', 'It holds no other unreleased feature\'s commits. A member of a coordination is chosen only with, or after, the members it requires.'),
    ('No open defect', 'None is recorded against it.'),
    ('Its decisions are accepted, and its story agreed', 'Every decision it rests on is accepted by the product owner, not still proposed. Any story an agent wrote for it has been seen and agreed by the product owner: a feature built from a story an agent wrote itself may be built to development, and waits at stage until then.'),
]


def eligible():
    cards = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in ELIGIBLE)
    return (f'<ul class="gives six">{cards}</ul><p class="note">The release set is the maintainer\'s choice. The agent assembling the release says which features are eligible and why, from the record, and lists what each lacks. That agent may have built part of the set, so the fresh QA agent confirms its list against the record. '
            'If the maintainer includes one below the bar, that is recorded as the maintainer\'s decision, with what the feature lacked, and QA reports those scenarios as not verified.</p>')


RESET_USUALLY = [
    ('Something has to come out', 'A feature on development is abandoned or broken and holding the others up; a feature has failed on stage.'),
    ('A clean start is needed', 'Before a hotfix, stage is reset so that the fix travels alone. Before a release set is assembled, stage is reset if it holds anything main does not.'),
    ('The branch is to show one thing', 'development is rebuilt from a release set so that people can see that candidate running.'),
    ('The branch can no longer be trusted', 'It has taken a merge it should not have, or so much has gone wrong on it that finding the cause costs more than building it again.'),
]
RESET_SELDOM = [
    ('After an ordinary release or hotfix', 'stage already holds what main holds, and the released features are already on development; the record going into development joins it to the release.'),
    ('While features on it are still being tried together', 'Resetting development means merging each of them again.'),
    ('When a small correction to a feature of the set is quicker and as safe', 'The feature is fixed on its own branch and merged again by pull request, on top of what is there, where rebuilding the whole set would cost more than it protects. Nothing is ever changed on the branch itself.'),
]


def resets():
    def cards(rows):
        return ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in rows)
    return ('<h3 class="sub">When to reset development or stage, and when to leave it running</h3>'
            '<p class="note">Both can be reset to <code>main</code> when that serves the work. This is guidance, not a list to apply by rote: say which case you see and why, and where it is not plain, ask. A reset is a push, so it is on the maintainer\'s word; the word to build a release candidate covers the resets of <code>stage</code> that the candidate needs. The record branch is never reset.</p>'
            '<h3 class="sub">A reset is usually right</h3>'
            f'<ul class="gives two">{cards(RESET_USUALLY)}</ul>'
            '<h3 class="sub">It is usually better left running</h3>'
            f'<ul class="gives plain">{cards(RESET_SELDOM)}</ul>'
            '<p class="note">After a reset, the features that should still be there are merged again, each from its own branch by pull request, and everyone is told, so that anyone with a copy takes it from GitHub again.</p>')




def who():
    say = {'free': 'without asking', 'word': "waits for the maintainer's word"}
    rows = ''.join(
        '<tr><td>%s</td><td><span class="%s">%s</span></td><td>%s</td></tr>' % (esc(a), k, say[k], esc(n))
        for a, k, n in WHO)
    return f'<div class="tablewrap"><table><thead><tr><th>What</th><th>May it be done</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></div>'


def history():
    return ('<div class="logs"><figure class="log"><figcaption><code>git log --first-parent main</code>, one release to an entry</figcaption><pre>'
            '<b>Merge branch \'stage\' into main</b>            <i>tag v0.6.0-pr142-2026-11-21</i>\n'
            '    Pull-request: https://github.com/&lt;account&gt;/&lt;project&gt;/pull/142\n'
            '<b>Merge branch \'stage\' into main</b>            <i>tag v0.5.1-pr131-2026-11-09, a hotfix</i>\n'
            '    Pull-request: https://github.com/&lt;account&gt;/&lt;project&gt;/pull/131</pre></figure>'
            '<figure class="log"><figcaption><code>git log --first-parent stage</code>, one arrival to an entry</figcaption><pre>'
            '<b>Merge branch \'docket-record\' into stage</b>            <i>the record, with QA\'s result and the acceptance</i>\n'
            '<b>Merge branch \'feature/w-t3xa8-passkey-sign-in\' into stage</b>\n'
            '<b>Merge branch \'fix/w-k7f3q-reset-email\' into stage</b></pre></figure>'
            '<figure class="log"><figcaption>On a feature, the record arriving. This is not the feature arriving anywhere.</figcaption><pre>'
            'Merge branch \'docket-record\' into feature/w-t3xa8-passkey-sign-in</pre></figure></div>'
            '<p class="note"><b>A release\'s name</b> is its tag: <code>v&lt;version&gt;-pr&lt;number&gt;-&lt;date&gt;</code>. The version comes first, then the number of the pull request that promoted <code>stage</code> to <code>main</code>, then the date of the promotion. A second tag on the same commit is the bare version, <code>v&lt;version&gt;</code>, for tools: under semantic versioning a hyphen after a version marks a pre-release, so a tool would rank the descriptive name below the release it names. '
            'Every merge made by pull request carries one line in its body, <code>Pull-request:</code> and the pull request\'s URL, so the merge commit itself leads to GitHub. '
            'Nothing is entered for the history of releases: it is read from the tags, the work items, QA\'s run and the acceptance.</p>'
            '<p class="note"><b>Where a work item stands</b> is read from the merges, not set by hand. Which of <code>development</code>, <code>stage</code> and <code>main</code> hold its branch is a fact of the history, and a status that says otherwise is wrong.</p>')


RULES = [
    ('Commit code on the record branch, or change the record on a feature.', 'The record is changed on the record branch, through Docket, and a feature pulls it.'),
    ('Commit on development or stage, or merge into either on your own machine.', 'Both change only by a pull request on GitHub, merged as a real merge.'),
    ('Cut a branch for work that is not ready.', 'Its work item, and its story and scenarios where it is new behaviour, are committed on the record first. A work item with no scenario and no reason for having none is not ready. A fix names the scenario it restores, or adds one for the fault. A standing instruction to keep working does not change this.'),
    ('Change anything in a merge beyond its conflict.', 'A merge resolves its conflict and nothing else. Any other change features need in order to work together is written on a feature\'s own branch, and the feature is merged again. Where the change is only right with the other features present, they are tied in a coordination.'),
    ('Merge a feature into development before its code review.', 'It is code reviewed on its own branch, and the findings answered, first, so that it is merged once.'),
    ('Commit work on a coordination branch, or merge it anywhere.', 'The work is done on the member\'s own branch, and the member is merged into the coordination branch again. The members go onward one by one.'),
    ('Reset development or stage by rote.', 'Both can be reset to main when that serves the work. Say which case you see and why, and where it is not plain, ask. After an ordinary release both usually stay as they are: the released features are already on development.'),
    ('Leave stage standing with a known fault.', 'Usually the feature comes out and stage is reset. Where the fault is small and quickly fixed on the feature\'s own branch, it may be merged again on top. Either way stage is checked again.'),
    ('Count a scenario as passed because the suite passed.', 'QA answers for each scenario, and reports one with no test as no test found.'),
]


def rules():
    li = ''.join(f'<li><p class="dont"><b>Don\'t</b> {esc(a)}</p><p class="do"><b>Do</b> {esc(b)}</p></li>' for a, b in RULES)
    return f'<ul class="rules">{li}</ul>'



STEPS = [
    ('record', 'Readied', 'Its work item, and its story and scenarios where it is new behaviour, are committed on the record. The work item names its scenarios or says why it has none.', ''),
    ('feat', 'Cut and built', 'A branch is cut from the record and named from its work item, one work item to a branch. Commits as often as needed. The feature pulls the record whenever it needs something recorded since.', ''),
    ('feat', 'Code reviewed', 'Its own tests pass in its own folder first. Then its code is reviewed on its own branch by an agent that did not write it, and each finding is answered, before its first merge into development, so that it is merged once.', ''),
    ('dev', 'Tested together', 'A pull request into development, merged without asking, and the features there are run together. A break is fixed on the feature\'s own branch. Being here does not mean it will be released.', ''),
    ('stage', 'Chosen', 'The maintainer chooses the release set from the features that are eligible.', 'word'),
    ('stage', 'Assembled', 'The set is built as a candidate on a machine, main plus the set in release order, and the whole suite is run on it. Then one pull request into stage for each feature, in the same order, and stage is checked against the candidate.', ''),
    ('stage', 'Verified', 'QA: the whole suite is run on stage by a fresh agent that has built nothing in the project, with an answer for each scenario.', ''),
    ('main', 'Promoted', 'The record, with QA\'s result and the acceptance, is merged into stage, and a check confirms nothing else changed. Then stage is promoted to main and tagged.', 'word'),
]


def steps():
    out = []
    for i, (cls, title, text, word) in enumerate(STEPS, 1):
        w = '<span class="word">waits for the maintainer\'s word</span>' if word else ''
        out.append(f'<li class="step c-{cls}"><span class="n">{i}</span><h3>{esc(title)}</h3><p>{esc(text)}</p>{w}</li>')
    return ('<div class="standards"><span class="std a">Building to development: fast, and development may be broken</span>'
            '<span class="std b">Choosing for stage: strict</span></div><ol class="steps">' + ''.join(out) + '</ol>')



BRANCHES = [
    ('record', 'docket-record', 'main plus everything recorded since. Work starts here. No code is committed on it.'),
    ('feat', 'feature', 'One work item\'s code, cut from the record. Also fix and hotfix.'),
    ('dev', 'development', 'Where features are tested together. It may be broken.'),
    ('stage', 'stage', 'The release: the chosen features, verified together.'),
    ('main', 'main', 'What is released. Only a promoted stage reaches it.'),
]

KEY = (
    '<ul class="key">'
    '<li><svg viewBox="0 0 28 16"><path class="ln c-feat" d="M0 8H28"/><circle class="dc c-feat" cx="14" cy="8" r="5"/></svg>a commit</li>'
    '<li><svg viewBox="0 0 28 16"><path class="ln c-dev" d="M0 8H28"/><circle class="dm c-dev" cx="14" cy="8" r="7"/></svg>a merge</li>'
    '<li><svg viewBox="0 0 28 22"><g class="c-stage"><circle class="dq" cx="14" cy="11" r="10"/><path class="tick" d="M9.5 11.5l3 3.2 6-7"/></g></svg>QA, or a code review</li>'
    '<li><svg viewBox="0 0 36 16"><path class="lk c-feat" d="M0 8H36"/></svg>work moving on, by pull request</li>'
    '<li><svg viewBox="0 0 36 16"><path class="lk c-main dash" d="M0 8H36"/></svg>a pull of the record or of main, or a reset</li>'
    '</ul>'
    '<p class="hint">Point at a branch, by its name or anywhere along its line, to follow it; click its name to keep it lit. Point at any link or mark to see what it is and the command behind it.</p>'
)



GIVES = [
    ('A release is chosen, not inherited', 'Being on development does not put a feature in a release. The maintainer, the person who decides what is released, chooses the set feature by feature.'),
    ('Development may be broken', 'It is where features are tried together. A break is fixed on the feature\'s own branch, and it does not hold up the release of the others.'),
    ('Many features at once', 'Every feature is built to stand alone, so several people or agents can build at the same time, each in a folder of its own (a Git worktree).'),
    ('What is verified is what ships', 'stage holds the release set, verified as a whole. The one merge made after QA brings the record, with QA\'s result and the acceptance, and a check confirms that nothing but the record changed since the commit QA tested.'),
    ('A failed feature comes out cleanly', 'Usually stage is rebuilt without it. Nothing is backed out, and nothing is patched in place.'),
    ('A release carries its own proof', 'QA\'s result and the maintainer\'s acceptance are recorded and travel to main with the release they belong to.'),
    ('A hotfix takes a release\'s road, alone', 'Recorded, cut from the record, verified on stage, promoted. It does not pass through development first, and it never goes straight to main.'),
    ('The history says where work has been', 'Every merge is a real merge whose title names both branches, so Git can say which branches hold a feature.'),
    ('Plain Git', 'Every step is ordinary Git, with pull requests on GitHub, and can be done by hand. Docket writes the record; the code can be worked on without it.'),
]


def record_fig():
    f = Fig(1100, 272, 'The record branch is one step between main and a feature: it pulls main after a release, the record is written on it, and every feature is cut from it and pulls from it.')
    M, R, A = 62, 132, 202
    f.lane('main', M); f.lane('record', R); f.lane('feat', A, [(560, 1076)], 'a feature')
    f.dot('main', 226, M, 'm'); f.tag(226, M, 'release', up=True)
    f.link('main', 244, M, 300, R, dash=True); f.dot('record', 300, R, 'm')
    f.label(236, M + 34, 'the record pulls main', 'end')
    for x in (372, 430, 488):
        f.dot('record', x, R)
    f.label(430, R - 18, 'the work is planned and recorded here')
    f.link('record', 504, R, 560, A)
    f.label(548, A + 30, 'a feature is cut from the record,\nholding its own work item', 'middle')
    for x in (610, 660):
        f.dot('feat', x, A)
    f.dot('record', 716, R)
    f.label(716, R - 18, 'its test run is recorded')
    f.link('record', 732, R, 788, A, dash=True); f.dot('feat', 788, A, 'm')
    f.label(800, A + 30, 'the feature pulls it, and carries\nthe record onward with its code', 'start')
    return f


def purpose():
    cards = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in GIVES)
    return f"""<section class="purpose" id="why">
<div class="cols">
<div><h2>Why it exists</h2>
<p>Most branching methods tie two decisions together: testing a feature with the others, and releasing it. Where features are cut from a shared <code>development</code> branch and merged back into it, whatever is on that branch is in the next release unless someone backs it out. One unfinished feature holds up everything behind it.</p>
<p>Feature Promotion Flow separates the two. A feature is merged into <code>development</code> to be tested with the others, and that says nothing about release. The release is assembled separately, on <code>stage</code>, from the features chosen for it, each merged from its own branch.</p>
<p>It is close to the method the Git project uses to build Git itself, <a href="https://git-scm.com/docs/gitworkflows">gitworkflow</a>: topic branches that graduate through integration branches, and tagged releases. In the projects it was written for, it replaced gitflow.</p>
</div>
<div><h2>Why the record has its own branch</h2>
<p>Docket is the program that keeps the record and shows it to people and to agents. A project on Docket keeps its record as files in the repository: use cases, stories, scenarios, work items and decisions, with the attempts and test runs made on them. The method needs that record in two places at once: where the work is planned, and inside every feature built from it.</p>
<p>Written on a feature, a work item would not reach <code>main</code>, or any other feature, until that feature was released. Kept in a branch that never meets the code, it would stop being part of the codebase, and a work item could no longer be tied to a build and carried along with it.</p>
<p>So the record has one permanent branch, <code>docket-record</code>: <code>main</code> plus everything recorded since. It holds the released code, and no code is committed on it, so it never holds unreleased code. Every feature is cut from it, so a feature holds its own work item and scenarios from its first commit. Because it holds no unreleased code, cutting from it brings no other feature along, which is what lets a release be chosen feature by feature.</p>
</div></div>
{fig(record_fig(), 'The whole record reaches <code>main</code> with each release, including work items that are not built yet. That is the aim: the backlog is the ledger of past, present and future work, and each item carries its status.')}
<h2>What it gives you</h2>
<ul class="gives">{cards}</ul>
</section>"""


ADDUP = [
    ('One record, open to everyone who works on it', 'The record is files in the repository, so a person and an agent read and write the same work items, scenarios and decisions from the same checkout. Anyone with the repository needs no separate login, connector or export to see what the work is, and every feature branch carries the record it was built from.'),
    ('Reliable release dates', 'A release is chosen from what is ready, so the date does not wait on one unfinished feature. stage is rebuilt and not patched, so a late failure removes one feature, not the release. The date is the promise; the contents are whatever is ready by then.'),
    ('Fewer regressions', 'Scenarios are written before the branch exists, so behaviour is pinned down first. The whole suite runs on the exact combination that ships. And after a hotfix the record carries the fix into development, so the next release cannot quietly lose it.'),
    ('Release documents read out of the record', 'A release is a known list of work items, each with its story, scenarios, test results and decisions. Release notes, a change log, a notice to users and an audit trail are the same data read out in different forms.'),
    ('Coordination without status meetings', 'The backlog is the ledger. What is in progress, what could ship, what is blocked and on what are questions the record answers. Work items name what they wait for, and a coordination (see features that require each other) ties features that require each other.'),
    ('Accountability across people and agents', 'Every commit names the person, the agent and the model. Decisions are kept in the words of whoever made them. Checking is done by someone who did not build. An agent\'s work is as open to inspection as a person\'s.'),
    ('Continuity', 'A new person or a fresh agent reads the record and knows why things are as they are. Nothing depends on who remembers.'),
]
STATIONS = [
    ('feat', 'The feature\'s own folder', 'Its own tests and scenarios', 'A test run on its work item'),
    ('feat', 'Code review', 'The code and its tests, on the feature\'s own branch, by an agent that did not write them', 'The code review beside the work item: each finding, its kind and how it ended'),
    ('dev', 'development', 'The features, run together', 'A break recorded against the feature'),
    ('mrg', 'The candidate', 'The release set, together, with the whole suite, before stage is built', 'Its contents compared with stage, tree against tree'),
    ('stage', 'stage', 'The whole suite, with an answer for every scenario in the set, by a fresh agent', 'QA\'s result, scenario by scenario, recorded by the QA agent itself'),
    ('main', 'Promotion', 'The maintainer\'s acceptance', 'A decision, in the maintainer\'s words, carried to main'),
]


def addup():
    cards = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in ADDUP)
    rows = ''.join(f'<tr class="c-{c}"><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(w)}</td></tr>' for c, a, b, w in STATIONS)
    return (f'<ul class="gives">{cards}</ul>'
            '<h3 class="sub">Fixed places to test, and to record the result</h3>'
            '<p class="note">The road has stations. Each has its check and a place where the result is kept, so nobody has to invent where testing happens or where its evidence goes.</p>'
            '<div class="tablewrap"><table><thead><tr><th>Station</th><th>What is checked</th><th>Where the result lives</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


PROBLEMS = [
    ('One unfinished feature is blocking the release.', 'A release is assembled from chosen features. The unfinished one stays on development.'),
    ('We need a code freeze before every release.', 'development never freezes. The release is built on stage, apart from ongoing work.'),
    ('Merge hell on long-lived branches.', 'Features are built to be independent, and conflicts surface on development early. A conflict resolved once can be replayed by Git\'s recorded resolutions (rerere), on the machine that resolved it.'),
    ('The hotfix never made it back, and the bug returned.', 'A hotfix takes the same road, and development gets the fix from the record straight after.'),
    ('It worked in testing but not in the release.', 'The code QA verifies on stage is the code promoted: only the record is merged after QA, and that is checked. Before that, the set is tested together as a candidate, and stage is checked against it, tree against tree.'),
    ('We reverted it and now the history is a mess.', 'Before promotion nothing is reverted: stage is rebuilt without the feature. A bad release already on main is put back by deploying the previous release again, then corrected by a hotfix. main is never reverted.'),
    ('Nobody knows what is actually in this release.', 'The release is a list of work items in the record, and the history names every branch merged and the pull request that merged it.'),
    ('Release notes are a scramble.', 'They can be read out of the release\'s work items. Docket does not produce them yet.'),
    ('The tracker and the code disagree.', 'The tracker is in the repository and moves with the code.'),
    ('Half the team, and all of the agents, cannot see the tickets.', 'The record is files in the repository. Anyone with the code has the work items, the scenarios and the decisions.'),
    ('Why was this decision made?', 'Decisions are recorded with the work, in the words of whoever made them.'),
    ('QA is a rubber stamp, or the author tested their own work.', 'QA is done by a fresh agent that has built nothing in the project, and answers scenario by scenario. Its brief is fixed text: the agent that starts QA sends it as written, filling in only the project, the folder, the starting agent\'s name and model, and the commit to test.'),
    ('Auditors want proof of testing and approval.', 'Each release carries its QA result and its acceptance to main.'),
]


def problems():
    rows = ''.join(f'<tr><td class="q">&ldquo;{esc(a)}&rdquo;</td><td>{esc(b)}</td></tr>' for a, b in PROBLEMS)
    return ('<div class="tablewrap"><table class="two"><thead><tr><th>The complaint</th><th>What this method does</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


DORA = 'https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf'
PLAYBOOK = 'https://claude.com/resources/articles/the-ai-native-sdlc-playbook'
HARV = 'https://fion.ac/jellyfish.pdf'
AI = [
    ('AI writes faster than we can review.',
     'A Harvard working paper by Fiona Chen and James Stratton, <a href="https://fion.ac/jellyfish.pdf">Artificial Intelligence in the Firm: Bottlenecks in Software Production</a>, finds that after firms adopted coding agents there were more commits and more pull requests, the time from a pull request to its merge grew, and the rise in resolved issues was not statistically significant.',
     'Every feature arrives at code review with its scenarios and a recorded test run, so code review is not the first check. The strictest checking, QA, is spent only on what is chosen to ship.',
     'The method does not remove the cost of code review. That is why the rework each code review causes is watched and discussed with the maintainer.'),
    ('We are faster, but less stable.',
     f'Google\'s <a href="{DORA}">2025 DORA report</a> found that adopting AI now improves software delivery throughput and still increases delivery instability.',
     'The method holds work to two standards: fast into development, strict at stage. Instability is meant to be met at that gate, before a release, with each feature small and independent.', ''),
    ('Running agents in parallel just moves the conflicts to merge time.',
     'Practitioners report that separate folders stop agents overwriting each other but do not prevent conflicts, that two agents told to work the backlog pick the same task, and that the person ends up as the coordination layer.',
     'Work is taken by assignment in the record, by name, one work item to a branch, so two agents do not take the same item, and the record is pushed whenever it changes so that every machine sees the claim. development is where conflicts are meant to surface. The record is the shared context the folders lack.', ''),
    ('The agent forgot what we decided.',
     'Writers describe specifications going stale while the real state lives in someone\'s head, and recommend decision logs and handoff documents.',
     'The record is kept as the work happens, decisions are recorded in the turn they are made, and an agent\'s session starts by reading it. It also travels with the code, which a handoff document does not.', ''),
    ('Who wrote this, and can we prove it?',
     'There are new tools for attributing lines to an AI, and no accepted standard yet for naming one in a commit.',
     'Every commit names the contributor, the agent, the model and the session. The person directing the work is its author, whatever share the agent typed.', ''),
    ('The specifications and tickets live somewhere the agent cannot see.',
     f'Anthropic\'s <a href="{PLAYBOOK}">AI-native SDLC playbook</a> recommends keeping the chain of artifacts in the product\'s repository, beside the code derived from it, as plain files that a person and an agent can both read and act on, with each stage committing something the next stage reads. It allows tickets and approvals to stay in an outside system, provided one source of truth is named.',
     'The record is that chain, in the repository: use cases, stories, scenarios, work items, decisions, attempts and test runs. It reaches every feature through the record branch, so whoever picks up the work, person or agent, already holds everything it rests on.',
     'The method goes further than the playbook in two places. The tickets themselves are in the repository, not linked from outside it. And decisions are kept as records of their own, in the words of whoever made them, where the playbook leaves them to merges and review approvals.'),
    ('We are drowning in low-quality AI contributions.',
     'Open-source maintainers are adopting policies on AI-assisted contributions. The measures in use include disclosure of AI use, evidence that a change was built and tested, and, on some projects, accepting an AI-assisted change only for an issue already accepted.',
     "All three are this method's defaults: work starts from a work item, attribution is on every commit, and test runs are recorded. Small changes are its aim, and nothing enforces them.", ''),
]


def ai():
    out = []
    for q, said, does, still in AI:
        label = 'Where this goes further' if still.startswith('The method goes further') else 'What stays true'
        extra = f'<dt>{label}</dt><dd>{esc(still)}</dd>' if still else ''
        out.append(f'<li><h3>&ldquo;{esc(q)}&rdquo;</h3><dl><dt>What is reported</dt><dd>{said}</dd><dt>What this method does</dt><dd>{esc(does)}</dd>{extra}</dl></li>')
    return ('<ul class="talks">' + ''.join(out) + '</ul>'
            '<p class="note">What other teams report is taken from published reports and practitioner writing gathered on November 21, 2026. Each source was opened and read by November 22, 2026, except where the list of sources says otherwise. The Harvard paper has been revised and its figures have changed between versions, so none is quoted here. Every source is listed under <a href="#sources">Sources</a>.</p>')


UNPROVEN = [
    ('Release documents read out of the record', 'The data is in the record. Docket does not yet produce release notes from it.'),
    ('Fewer regressions', 'This is what the design should produce. Two releases have been through stage, which is too few to show it.'),
    ('Reliable release dates', 'They depend on features staying independent. Where features require each other, a coordination handles it, at the cost of some freedom to choose.'),
]


LIMITS = [
    ('The evidence so far', 'The method is new. It has been run on one project, through two releases. Nothing here has yet been shown with several people on several machines, and every benefit below should be read with that in mind.'),
    ('What it costs', 'A release of n features is 2n + 3 pull requests: each feature into development and into stage, the record into stage, stage into main, and the record into development. It is also n code reviews, a candidate built and tested on a machine, and one full QA run. A feature that fails on stage usually costs a reset, the candidate built again, a pull request for each feature that remains, and QA again. A hotfix is four pull requests, a code review and a QA run, and sets aside any release being assembled.'),
    ('What it does not cover', 'The method says nothing about database migrations, or about fixing an older version while a newer one is out: there is one released line. It does not say how a release is deployed, and its rollback (see the section on a bad release) assumes the previous release can be deployed again.'),
    ('Against trunk-based development', 'Trunk-based development with feature flags separates testing from releasing another way: everything merges to one branch daily, and a flag decides what is released. It integrates sooner and needs no assembly. It asks that unfinished work be safe to ship switched off, and the flags, not the history, say what a release contains. This method makes the other trade. Integration comes later and costs more pull requests. In return a release is a set of whole features, each with its own record, tests and code review, and what is left out is not in the build at all.'),
]


def limits():
    cards = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in LIMITS)
    more = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in UNPROVEN)
    return (f'<ul class="gives two">{cards}</ul>'
            '<h3 class="sub">Designed in, and not yet proven by use</h3>'
            f'<ul class="gives plain">{more}</ul>')


SOURCES = [
    ('The method', [
        ('The development standards this guide is drawn from', '', 'The rules and the steps, as they stood on November 22, 2026. They are Lucidex Group\'s own and are not published; every rule and figure here is drawn from them.', 'source'),
        ("gitworkflows, in Git's manual", 'https://git-scm.com/docs/gitworkflows', "The Git project's own method, and the parent of this one: topic branches that graduate through integration branches, throw-away integration, tagged releases.", 'named in the standards; read at its source'),
        ('gitworkflow, explained for other teams', 'https://github.com/rocketraman/gitworkflow', 'The same method set out for teams outside the Git project.', 'named in the standards; not opened in this check'),
        ('Branch Per Feature, Adam Dymitruk, 2012', 'https://dymitruk.com/blog/2012/02/05/branch-per-feature/', 'The closest published method: every feature starts from the same commit, and a release is assembled from the features that are ready.', 'named in the standards; not opened in this check'),
        ('Branch Per Feature in practice', 'https://bitbashing.io/2015/02/10/bpf-in-practice.html', 'An account of using it on one project for most of a year: a release is built by merging in the features that are ready.', 'named in the standards; read at its source'),
        ('FeiFlow, Maksym Moyseyev, 2024', 'https://dev.to/feiflow/feiflow-an-opinioned-git-branching-and-release-management-strategy-33l3', 'Similar in one respect: an integration branch that is never merged anywhere and is rebuilt to clear it.', 'named in the standards; read at its source'),
    ]),
    ('What other teams report', [
        ('DORA 2025: State of AI-assisted Software Development', 'https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf', 'AI adoption now improves software delivery throughput and still increases delivery instability. Used in "We are faster, but less stable."', 'checked at its source'),
        ('Announcing the 2025 DORA Report, Google Cloud', 'https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report', "Google's own summary of the same report.", 'checked at its source'),
        ('The AI-native SDLC playbook, Anthropic, August 2026', 'https://claude.com/resources/articles/the-ai-native-sdlc-playbook', 'Keep the chain of artifacts in the product\'s repository, beside the code, as files a person and an agent both read. Used in "The specifications and tickets live somewhere the agent cannot see."', 'read at its source'),
        ('Artificial Intelligence in the Firm: Bottlenecks in Software Production, Fiona Chen and James Stratton, Harvard working paper', 'https://fion.ac/jellyfish.pdf', 'After firms adopted coding agents: more commits and pull requests, a longer time from pull request to merge, and a rise in resolved issues that is not statistically significant. Used in "AI writes faster than we can review."', 'read at its source, in the version of November 19, 2026; the first third of the paper, which holds the findings'),
        ("TechRadar's report of that paper", 'https://techradar.com/pro/ai-agents-are-great-at-writing-new-code-but-then-the-human-bottleneck-slows-everything-down', "A report of an earlier version of the paper, with that version's figures.", 'read; superseded by the paper itself'),
        ("Born City's report of that paper", 'https://borncity.com/news/harvard-studie-zu-ki-agenten-pull-requests-brauchen-49-prozent-laenger/', 'A second report of the earlier version, in German.', 'read; superseded by the paper itself'),
    ]),
    ('Practitioner writing and studies behind the other conversations', [
        ('AI Is Breaking Code Review, Cláudia Carvalho, Codacy, 2026', 'https://blog.codacy.com/ai-breaking-code-review-how-engineering-teams-survive-pr-bottleneck', 'A vendor\'s article gathering other organisations\' findings that pull requests wait longer for review. Supports "AI writes faster than we can review." None of its figures is quoted.', 'read at its source'),
        ('AI Coding Agents and the Code Review Bottleneck, Dromeas', 'https://dromeas.ai/blog/ai-coding-agents-code-review-bottleneck', "A vendor's restatement of the Harvard paper's earlier figures. It adds no evidence of its own, and nothing here rests on it.", 'read at its source; adds nothing'),
        ('Early-Stage Prediction of Review Effort in AI-Generated Pull Requests, Dao Sy Duy Minh and others, MSR 2026', 'https://arxiv.org/abs/2601.00753', 'A study of 33,707 pull requests written by agents: many are abandoned during review, which costs maintainers time. Supports "AI writes faster than we can review."', 'read at its source'),
        ('5 Lessons from Running AI Coding Agents in Parallel, Batty', 'https://dev.to/battyterm/5-lessons-from-running-ai-coding-agents-in-parallel-53on', 'Two agents told to work the backlog took the same feature, separate folders leave the conflicts for merge time, and the work needs someone supervising. The source for "Running agents in parallel just moves the conflicts to merge time."', 'read at its source'),
        ('Git Worktrees Changed How I Run Parallel AI Agents, Batty', 'https://dev.to/battyterm/git-worktrees-changed-how-i-run-parallel-ai-agents-39pm', 'Separate folders stop agents overwriting each other, conflicts still come at merge time, and a person assigns the tasks and orders the merges. Used in the same conversation.', 'read at its source'),
        ('AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates, George Xu, Arjun Subramanian and Nithilan Karthik, 2026', 'https://arxiv.org/abs/2607.04697', 'A study that replayed the merges of pull requests agents had open at the same time, and found conflicts in a substantial share of them. Used in the same conversation. Its figures are not quoted.', 'read at its source'),
        ('Why AI coding agents forget: memory, handoffs, and latent context, Faris Haddad, AWS Builder Center, 2026', 'https://builder.aws.com/content/3LVv7v1qJ7fyd8buaDIKJYZbw9K/why-ai-coding-agents-forget-memory-handoffs-and-latent-context', 'Recommends a written handoff record holding decisions, constraints and open questions. Supports "The agent forgot what we decided."', 'read at its source'),
        ("Your AI Agent Already Forgot Half of What You Told It, Andrew Stellman, O'Reilly Radar, 2026", 'https://www.oreilly.com/radar/your-ai-agent-already-forgot-half-of-what-you-told-it/', 'Decisions made in a session are lost when the tool shortens its context. Recommends keeping them in files and writing handoff documents. Used in the same conversation.', 'read at its source'),
        ('The Session-End Spec Update That Keeps AI Agents on Track Across Days, Molisha Shah, Augment Code, 2026', 'https://www.augmentcode.com/guides/session-end-spec-update-ai-agents', "Specifications go stale within hours while the real state is in the developer's memory. Recommends recording each decision, with its reason, in a file under version control. The source for the sentence on specifications going stale.", 'read at its source'),
        ('Identity-Attributed Git Commits via Tier-Structured Trailers, Blake Morrison, an Internet-Draft', 'https://datatracker.ietf.org/doc/draft-morrison-identity-attributed-commits/', 'One person\'s proposal, not adopted by any working group, for commit trailers that name the person and the AI tool. Evidence that naming an AI in a commit has proposals and no accepted standard. Used in "Who wrote this, and can we prove it?"', 'read at its source'),
        ('Bridging the Gap on AI-Assisted Scientific Software Development Through Transparency and Traceability, Chaitanya Bhave and others, Idaho National Laboratory, 2026', 'https://arxiv.org/abs/2605.17675', 'Proposes recording AI involvement on every commit, and holds the person directing the work to be its author. Used in the same conversation.', 'read at its source'),
        ('Git AI', 'https://github.com/git-ai-project/git-ai', 'A tool that records in Git notes which lines an agent wrote. The "new tools for attributing lines to an AI" in the same conversation.', 'read at its source'),
        ('AI Policy, Disclosure, and Human in the Loop: How Are Contribution Guidelines Adapting to GenAI?, Andre Hora and Romain Robbes, 2026', 'https://arxiv.org/abs/2605.16706', 'Of 1,000 popular repositories, 118 had a policy on AI. About half of those policies require disclosure, and most require a person in the loop. The source for "Open-source maintainers are adopting policies."', 'read at its source'),
        ("Godot maintainers struggle with 'draining and demoralizing' AI slop submissions, Tim Anderson, The Register, 2026", 'https://www.theregister.com/2026/02/18/godot_maintainers_struggle_with_draining/', 'Godot\'s maintainers on what AI-written pull requests cost them, with a list of projects that have written policies. Supports "We are drowning in low-quality AI contributions."', 'read at its source'),
        ('GitHub ponders kill switch for pull requests to stop AI slop, Thomas Claburn, The Register, 2026', 'https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai', 'GitHub weighing whether to let maintainers restrict pull requests or turn them off. Used in the same conversation.', 'read at its source'),
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




TRACKER_GIVES = [
    ('Anyone with the code has the tracker', 'A person or an agent who clones the repository has every ticket, with no second login and no integration.'),
    ('A feature\'s branch carries its own ticket', 'The scenarios it has to meet and the results of testing it sit beside the code that was built against them.'),
    ('A release carries its tickets as they stood', 'Check out last year\'s release and you can read what was asked for and what was accepted.'),
    ('A change to a ticket is a commit', 'Who changed it, when, and what it said before are in the history, like any other file.'),
    ('The acceptance criteria are the files the tests run', 'The ticket and the tests cannot say different things.'),
]
TRACKER_BRANCH = [
    ('A place to write tickets to', 'A ticket can be added or changed at any time, whatever state the code is in.'),
    ('A place as recent as production', 'After every release, <code>docket-record</code> takes in what was released, so it never lags behind what is live.'),
    ('A place everyone can reach without conflicts', 'People and agents all read and write tickets there, and no one\'s ticket change collides with someone else\'s code.'),
]
TRACKER_HAND = [
    ('To look at a ticket', 'Pull <code>docket-record</code> and read the file.'),
    ('To change a ticket', 'Edit the file on <code>docket-record</code>, commit, and push.'),
    ('To start work', 'Cut your branch from <code>docket-record</code> and not from <code>main</code>, so the work begins with its own ticket.'),
    ('Before your work moves on', 'Pull <code>docket-record</code> into your branch, so the ticket and its results go with it.'),
]


def tracker():
    def cards(rows):
        return ''.join(f'<li><h3>{esc(t)}</h3><p>{d}</p></li>' for t, d in rows)
    return ('<p class="say">One thing is different. The tickets are files in your repository, not rows in a database on someone else\'s server. They travel with the code, so they are available to both the AI and the humans.</p>'
            '<p class="note">On the rest of this page a ticket is called a work item, and the tickets with everything kept beside them are called the record.</p>'
            '<h3 class="sub">What that gives you</h3>'
            f'<ul class="gives">{cards([(t, esc(d)) for t, d in TRACKER_GIVES])}</ul>'
            '<h3 class="sub">Where the tickets are kept</h3>'
            '<p class="say">The tickets are kept on a branch of their own, <code>docket-record</code>. It gives you three things.</p>'
            f'<ul class="gives plain">{cards(TRACKER_BRANCH)}</ul>'
            '<p class="say">Docket runs on your machine and shows you the files on <code>docket-record</code> as pages, and you change a ticket through it. Committing that change is still yours to do.</p>'
            '<h3 class="sub">If you work by hand</h3>'
            '<p class="say">You can use all of this without Docket, because <code>docket-record</code> is the tracker.</p>'
            f'<ul class="gives two">{cards(TRACKER_HAND)}</ul>')




# What a project on Docket has to be: the first part, as designed for the guide inside Docket.
PART1 = [
    ('commits', 'What using Docket commits a project to',
     '<p class="say">Using Docket commits a project to two things: it is structured as this part describes, and its work moves through Feature Promotion Flow, which the rest of this guide describes.</p>\n<p class="note">The two go together. Docket keeps the project\'s record as files in the project\'s own repository, on a branch of its own, and it reads where each work item stands from the merges in the history. So it shows where work stands only for work that moved as the flow says.</p>\n<p class="note">Every step is plain Git. A project on Docket can be worked on without Docket, and nothing here makes that impossible.</p>'),
    ('keeps', 'What Docket keeps',
     '<p class="say">Docket keeps what is to be built and what was done about it: use cases, stories, scenarios, work items and decisions, and the record of the work done on them, which is the estimates, the attempts and the test runs.</p>\n<ul class="gives two"><li><h3>The backlog is the ledger</h3><p>Past, present and future work. Each item carries its status and its notes, and bringing the ledger forward to <code>main</code> with every release is the goal. A record kept apart from the code is not this design.</p></li><li><h3>Docket writes files and does not commit</h3><p>A person or an agent commits what it wrote.</p></li><li><h3>The record is these folders</h3><p><code>.docket/</code> holds the use cases, stories, work items, decisions and the record of the work. <code>features/</code> holds the scenarios. <code>docs/</code> and the Markdown files at the top of the project are record too.</p></li><li><h3>It lives on one branch</h3><p><code>docket-record</code>, permanent and never reset, with no code committed on it. Why, and what each branch holds, is in <a href="#why" data-go="why">Part 2</a> and <a href="#s10" data-go="s10">Part 3</a>.</p></li></ul>'),
    ('adds', 'What Docket adds to a project',
     '<p class="lede">Adopting a project adds the record and a few things beside it. <code>docket assess</code>, given the project\'s folder, reports what adopting it would involve and changes nothing; nothing is applied until the project\'s owner agrees.</p>\n<div class="tablewrap"><table><thead><tr><th>What is added</th><th>What it is for</th></tr></thead><tbody>\n<tr><td><code>.docket/config.yaml</code></td><td>Names the project and gives it its own port. One running Docket is one project.</td></tr>\n<tr><td>The <code>docket-record</code> branch, and a folder where it is checked out</td><td>Where the record is written, and the folder Docket is served from.</td></tr>\n<tr><td>A marked section in the project\'s instructions for agents</td><td>Tells an agent to work through Docket. Its first line marks it, so that it can be found.</td></tr>\n<tr><td><code>.mcp.json</code></td><td>The connection to Docket for agents.</td></tr>\n<tr><td>A commit hook</td><td>Keeps code off <code>docket-record</code> and the record off features.</td></tr>\n</tbody></table></div>'),
    ('not-moved', 'A project that has not been moved yet',
     '<p class="say">A project with no <code>docket-record</code> branch has not been moved to this form. Work there still starts from <code>main</code>, and the rules about the record\'s branch do not apply to it yet.</p>'),
]


# What Docket is, and how it works: written for this site, as Docket stood on November 22, 2026.
DOES = [
    ('It keeps the backlog', 'Use cases and their flows, the stories sliced from them, the work items that deliver each story, and the scenarios each one has to meet. Each item carries its status, its order and who it is assigned to.'),
    ('It keeps the decisions and the evidence', 'Decisions are kept in the words of whoever made them, beside the thing they are about. Estimates, attempts, test runs and code reviews are kept on the work item they belong to.'),
    ('It shows where work stands', 'Where each work item is, on development, stage or main, is read from the merges of the branch named for it. It is not a status someone sets.'),
    ('It serves a person and an agent the same record', 'Web pages for a person, and a connection for an agent (the Model Context Protocol). Both call the same code, and an agent is told the rules of the flow when it connects.'),
    ('It checks the record', 'docket check reports slips against the flow. docket assess says what adopting a project would involve, and changes nothing.'),
    ('It reports', 'On delivery, quality, agents, effort and coverage, read out of the record. The reports are partly built.'),
]
WORKS = [
    ('One program, run on your own machine', 'Docket is installed apart from the projects it serves, and puts nothing of its own into them: no packages, no database, no plugin. docket serve, started in any folder of a project, serves that project on its own port, on the local machine only. One server is one project.'),
    ('The record is files, and there is no database', 'The record is files under .docket/ and features/, with the project\'s own documents. Everything Docket shows is read from those files and from Git on each request.'),
    ('It writes files and does not commit', 'Docket never stages, commits or pushes, and runs no Git command that changes a repository. It refuses a write based on a file that has changed since it was read. Whoever did the work commits it.'),
    ('It reads Git', 'Who the people are, from the authors of commits. Whether a record file is committed and pushed. And where a work item is, from the titles of the merges on development, stage and main.'),
    ('It is served from the record\'s folder', 'The record has a permanent branch, docket-record, checked out in a folder of its own. Docket reads and writes only that folder, so it always shows one record.'),
    ('The server keeps the time', 'Every call is stamped by the server when it arrives, so the times in the record do not rest on an agent\'s say-so.'),
]


def about():
    def cards(rows):
        return ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in rows)
    return ('<p class="say">Docket is a program that keeps a record of everything a software project creates, in the project\'s own repository, for people and agents to work through: use cases, stories, scenarios, work items, decisions, and the evidence of what was done and tested.</p>'
            '<p class="note">It is a ticket tracker whose tickets are files in the repository. It was built to run Feature Promotion Flow, and the rest of this guide describes the flow as a project on Docket runs it.</p>'
            '<h3 class="sub">What it does</h3>'
            f'<ul class="gives">{cards(DOES)}</ul>'
            '<h3 class="sub">How it works</h3>'
            f'<ul class="gives two">{cards(WORKS)}</ul>'
            '<h3 class="sub">Its pages</h3>'
            '<p class="note">The pages follow the life of the work. <b>Define:</b> Principles and Decisions. <b>Do:</b> Work, the backlog as one table of use cases, stories and work items, with what needs attention. <b>Deliver:</b> Environments, History and Reports. <b>Project:</b> Artifacts, Participants, Record health, and this guide.</p>'
            '<h3 class="sub">What it is not</h3>'
            '<p class="note">Docket is not a hosted service. It has no sign-in and no database shared between users, and it does not deploy anything. It is in active development and is not yet in production. A project on Docket can be worked on without it, because every step is plain Git and the record is plain files.</p>'
            '<p class="note"><b>The repository.</b> Docket is not yet published. Its repository will be linked here when it is.</p>')


PARTS = [
    ('Docket, and what a project on it has to be', 'For a person deciding whether to put a project on Docket, and anyone working in one that is on it.'),
    ('Why', 'For anyone deciding whether to work this way.'),
    ('The flow', 'How work moves from the record to a release.'),
    ('Releases', 'Assembling one, testing it, naming it.'),
    ('When things do not go to plan', 'Rework, failures, hotfixes, a bad release, conflicts and features that require each other.'),
    ('What not to do', 'The mistakes that cost a release later.'),
    ('Who decides what', 'What may be done without asking, and what waits for the maintainer.'),
]


def doc():
    """The guide for a project on Docket, as parts and sections for the page to lay out."""
    drawing.use(NAMES, BR_TIP, NAME_TIP, link_tip, dot_tip)
    br = ''.join(f'<li class="c-{c}"><code>{esc(n)}</code><span>{esc(t)}</span></li>' for c, n, t in BRANCHES)
    S = [
        (2, 'limits', 'Its limits, stated first',
         'What has and has not been shown, what the method costs, what it leaves out, and how it compares with the most common alternative.',
         limits()),
        (2, 'tracker', 'Where Docket keeps your tickets',
         'Docket is a ticket tracker. It has a backlog, statuses, an order, and people assigned to work. You write a ticket before the work starts, update it as the work moves, and look at it to see where things stand. If you have used a tracker before, you know how to use this one.',
         tracker()),
        (2, 'addup', 'What the parts add up to',
         'Each of these comes from two or more pieces of the method working together, which is why no single rule delivers it.',
         addup()),
        (2, 'problems', 'Problems teams commonly report, and what this does about them',
         'Complaints teams commonly voice, with what this method does about each.',
         problems()),
        (2, 'agents', 'Working with AI agents',
         'Seven conversations teams are having about building software with AI, and where this method answers them.',
         ai()),
        (3, 'road', 'The road from the record to main',
         'Work starts in the record and ends on <code>main</code>. A feature is code reviewed on its own branch, merged into <code>development</code> to be tested with the others, and merged into <code>stage</code> only when it is chosen for a release.',
         fig(road(), 'Time runs left to right. Feature A is released. Feature B is tested on <code>development</code> and waits for a later release. No feature is ever cut from <code>development</code> or <code>stage</code>, and nothing pulls from them.')),
        (3, 'steps', 'One feature, step by step',
         'The same road as the section before, as eight cards for one feature, ending at promotion. Two standards apply. Building to <code>development</code> is fast. Choosing for <code>stage</code> is strict, and two of its steps wait for the maintainer.',
         steps()),
        (3, 'checks', 'The checks, in order',
         'Each word means one thing. A review is always a plan review or a code review.',
         checks() + '<p class="note"><b>When something fails.</b> A failure is recorded, wherever it is caught, against the feature it belongs to: the step that caught it (the feature\'s own tests, the code review, testing together, the candidate, QA on <code>stage</code>) and its kind, by the six kinds of finding listed under rework after a code review. The feature goes back to its builder and is fixed on its own branch. The point of recording the step and the kind is to see, over time, which step catches what and what reaches <code>stage</code>.</p>'),
        (3, 'eligible', 'What makes a feature eligible for stage',
         'Being on <code>development</code> is not enough. These six conditions are the bar for <code>stage</code>. A feature below it is chosen only by the maintainer\'s recorded decision.',
         eligible()),
        (3, 'holds', 'What each branch holds',
         'The record travels with the code. A feature\'s folder always holds everything needed to build and test it: the code, its work item and its scenarios.',
         holds()),
        (3, 'folders', 'Where everyone works',
         'One repository, checked out in several folders, so no two people or agents share a checkout and Docket always reads one record.',
         folders()),
        (4, 'release', 'A release',
         'The same road, for a set of three features. A release is assembled on <code>stage</code> from the features chosen for it, verified there, and promoted to <code>main</code> as a whole, carrying its own QA result and acceptance.',
         fig(release(), 'After the release the record pulls <code>main</code>, goes into <code>development</code> by pull request, and each feature still in progress pulls the record. <code>development</code> and <code>stage</code> usually stay as they are: <code>stage</code> already holds what <code>main</code> holds, and the released features are already on <code>development</code>. The pull request from the record is what joins <code>development</code> to the release.')),
        (4, 'loop', 'The whole cycle, as a loop',
         'The same release, drawn as rings. Time runs clockwise from the top, and one turn is one release. Where the linear picture ends, this one begins again.',
         '<div class="loopwrap">' + fig(loop(), 'The rings are the branches, with <code>main</code> at the centre. A feature that is released ends when it reaches <code>stage</code>. A feature that waits goes all the way round, and an ordinary release breaks no ring.') + '</div>'),
        (4, 'candidate', 'Testing the release set before stage is built',
         'The features tried together on <code>development</code> are everything in progress, not the release set. So the chosen set is first built as a candidate on a machine: <code>main</code> plus the set, merged in release order and never pushed, with the whole suite run on the assembled set. The same features are then merged into <code>stage</code> in the same order, and <code>stage</code> is checked against the candidate.',
         fig(candidate(), 'A break is found before <code>stage</code> exists, where leaving a feature out costs nothing on GitHub. Where people need to see the candidate running, it can be built on <code>development</code> instead. That is a case of items coming out of it: <code>development</code> is reset to <code>main</code> on the maintainer\'s word and the set is merged into it, so the candidate can be seen running wherever <code>development</code> is deployed. The features left out are merged into it again afterwards.')),
        (5, 'rework', 'Rework after a code review',
         'A feature is code reviewed on its own branch, and its findings answered, before it is first merged into <code>development</code>, so that it is merged once. The builder classifies each finding and deals with it by its kind, and anything to fix is fixed where the feature was built.',
         fig(rework(), 'A feature that was already on <code>development</code> when it was reworked is merged into it again by pull request; <code>development</code> is not reset for it. How much rework each code review caused is said, and discussed with the user.') + findings()),
        (5, 'fails', 'When a feature fails on stage',
         'If <code>stage</code> fails, it is not left standing. A failed feature is not backed out. Usually it comes out, and <code>stage</code> is rebuilt without it; where the fault is small and quickly fixed on the feature\'s own branch, the feature may be merged again on top. Either way <code>stage</code> is checked again.',
         fig(fails(), 'Shown: the usual case. <code>stage</code> is reset to <code>main</code>, the candidate is built again from the rest of the release set, the rest is merged into <code>stage</code> again, and it is checked again. The fix is made on the feature\'s own branch and code reviewed there. A feature the maintainer did not choose never goes in.') + resets()),
        (5, 'comeout', 'When items need to come out of development',
         'This is the usual reason to reset <code>development</code>; the cases are listed in the section before. After an ordinary release it usually stays as it is. Rebuilding it from a release set, to test that set as a candidate, is a case of the same thing: everything outside the set comes out, and is merged in again afterwards.',
         fig(comeout(), 'When <code>development</code> is reset, every surviving feature is merged again, so the same conflict can come up again. Git\'s recorded resolutions replay it.')),
        (5, 'hotfix', 'A hotfix',
         'A hotfix is a fix that cannot wait for the next release. It takes a release\'s road from <code>stage</code> onward, alone. It does not pass through <code>development</code>, and it never goes straight to <code>main</code>.',
         fig(hotfix(), 'The incident is recorded before the branch exists, so the hotfix holds its own record from its first commit. Afterwards <code>development</code> gets the fix from the record by pull request. If the fix conflicts with a feature there, the conflict shows in that pull request.')),
        (5, 'rollback', 'A bad release already on main',
         'Rolling back is two things, in this order: put production back, then correct the release. <code>main</code> is never reverted or rewritten.',
         fig(rollback(), 'Putting production back is a deployment and changes nothing in Git. The stage reset, the record going into <code>stage</code> and the steps after a release are as in the hotfix above and are left out of this drawing.')),
        (5, 'conflict', 'Resolving a conflict',
         'Whoever opened the pull request resolves the conflict. Nothing is pushed to <code>development</code> or <code>stage</code> to get round one.',
         fig(conflict(), 'The same means serves <code>stage</code>. The merge is made on a machine, so Git\'s reuse of recorded resolutions (rerere, turned on once per clone) applies: the same conflict, resolved once, is replayed when it comes up again on that machine. The recordings are kept per clone, and Git has no means of sharing them. A merge branch is for a real conflict, and it is the one branch ever cut from <code>development</code> or <code>stage</code>.') + '<p class="note"><b>A merge resolves its conflict and nothing else.</b> Any other change features need in order to work together is written on a feature\'s own branch, never in a merge and never on <code>development</code> or <code>stage</code>, and the feature is merged again. Where such a change is only right with the other features present, those features require each other, and the answer is a coordination.</p><p class="note"><b>A conflict GitHub reports and Git does not have.</b> A branch cut from the record holds every released feature, because the record has pulled <code>main</code>. <code>development</code> holds the same features by another route, its own pull requests. Until the two are joined they share each released feature separately, and GitHub reports a conflict on a pull request that Git on a machine merges cleanly. The cure is the join made after every release and hotfix: the record goes into <code>development</code> by pull request. If the merge branch has become routine, something is unjoined, and that is what to say.</p>'),
        (5, 'coordination', 'Features that require each other',
         'Sometimes one feature cannot be built or tested without another that is not yet released, or features work together only with a change that is right only with the others present. One answer is to wait for the first to be released. The other is a coordination, which lets them be worked on together while each stays on its own branch. Which is the maintainer\'s to decide.',
         fig(coordination(), 'A member\'s passing result was earned with the other members present, so it goes into <code>development</code> or <code>stage</code> only with, or after, the members it requires.') + mergeonly()),
        (6, 'cut', 'Why every branch is cut from the record',
         'Git can merge a branch into any branch it shares an ancestor with. What the branch was cut from decides what comes with it. This is the rule the rest of the method rests on, and the first thing not to do.',
         fig(why(), 'Features A and B are already on <code>development</code>. Cut from there, feature X carries both into <code>stage</code>. Cut from the record, which holds no unreleased code, it arrives alone and can be chosen for a release by itself. The other ways to end up carrying work that was not chosen are in the next section.')),
        (6, 'mistakes', 'The other mistakes, in pairs',
         'Cutting from <code>development</code>, above, is the plainest case. Each of these does the same kind of damage by another route: it looks harmless when it is done and costs a release later. Wrong on the left, right on the right.',
         fig(p_chain(), 'A feature cut from another, or with another merged into it, cannot be chosen for a release without it. Features that truly require each other are tied in a coordination instead.')
         + fig(p_pull(), 'A local copy of <code>development</code> or <code>stage</code> is for running and testing only. After a reset, a pull merges the old commits back in.')
         + fig(p_update(), 'Both of GitHub\'s buttons merge <code>development</code> into the feature. The feature then carries every other feature wherever it goes.')
         + fig(p_squash(), 'Every merge is a real merge, and its title names both branches. That is how the history says where work has been.')
         + fig(p_rebase(), 'A feature that has been merged anywhere is never rebased.')
         + fig(p_hotfix(), 'What is verified on <code>stage</code> is what ships. A hotfix is no exception.')
         + fig(p_backout(), 'Nothing is patched on <code>stage</code>. Usually it is reset, and the rest of the set is merged again.')
         + rules()),
        (7, 'who', 'Who may do what without asking',
         'Work on the record and on a feature is free. Anything that changes what is released waits for the maintainer.',
         who()),
        (4, 'history', 'How the history says where work is, and how a release is named',
         'A commit does not record its branch, but a merge\'s title names the branch merged and the branch merged into, and its body names the pull request that made it. Read by first parent, each permanent branch is one line per arrival.',
         history()),
    ]
    return {
        'name': 'With Docket',
        'title': 'Feature Promotion Flow with Docket',
        'lede': 'What using Docket commits a project to: how the project is structured, and how its work moves through Feature Promotion Flow. It states the method as the development standards Docket is built to state it.',
        'intro': 'A project\'s record is its use cases, stories, scenarios, work items and decisions, kept as files in the repository on a branch of their own. Every feature lives on its own branch, cut from that record. Features are merged into <code>development</code> to be tested together. A release is assembled on <code>stage</code> from the features chosen for it, verified, and promoted to <code>main</code>. The record travels with the code the whole way, so a build carries its own work items.',
        'parts': PARTS,
        'first': [{'id': i, 'title': t, 'html': f'<section id="{i}"><header><h2>{t}</h2></header>{b.replace('#s10', '#holds')}</section>'}
                  for i, t, b in [('docket', 'What Docket is, and how it works', about())] + PART1],
        'repo': ('', '', 'Docket is not yet published. Its repository will be linked here when it is.'),
        'why': {'id': 'why', 'title': 'Why it exists, and why the record has its own branch', 'html': purpose()},
        'legend': f'<div class="top legend"><h3 class="sub">The branches, and how to read the figures</h3><ul class="branches">{br}</ul>{KEY}{who3()}</div>',
        'sections': S,
        'sources': sources(),
        'sources_desc': 'Where the method comes from, and where each claim about other teams comes from, with how far each was checked.',
        'footer': 'Drawn from Lucidex Group\'s development standards, November 22, 2026. Branch names are the standard ones; a project\'s features are named from their work items.',
    }
