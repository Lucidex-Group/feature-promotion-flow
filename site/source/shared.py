"""Figures and tables that read the same with or without Docket."""
from drawing import *


# A feature fails on stage ------------------------------------------------------
def fails(noted='The failure is recorded against feature C, with the step that caught it and its kind.'):
    f = Fig(1100, 350, 'Three features are merged into stage and one fails. Stage is not left standing. Usually the feature comes out: stage is reset to main, the other two are merged again, and the suite is run on stage again.')
    A, B, C, S, M = 52, 104, 156, 236, 304
    f.lane('feat', A, [(X0, 650)], 'feature A')
    f.lane('feat', B, [(X0, 720)], 'feature B')
    f.lane('feat', C, [(X0, 388)], 'feature C')
    f.lane('stage', S, [(X0, 560)])
    f.lane('main', M)
    f.step('The release list is merged into stage, one pull request for each feature, and the whole suite is run on stage, once.')
    for i, y in enumerate((A, B, C)):
        x = 248 + 70 * i
        f.link('feat', x, y, x + 50, S); f.dot('stage', x + 50, S, 'm')
    f.step('Feature C fails, in the suite\'s run on stage or in QA. stage is not left standing with a known fault. ' + noted)
    f.dot('stage', 500, S, 'x'); f.label(500, S - 20, 'C fails', strong=True)
    f.step('Usually the feature comes out, as drawn here: stage is reset to main. This does not wait for a separate word. The failed feature is not backed out, and nothing is patched on stage. Where the fault is small and the feature is fixed quickly on its own branch, it may be merged again on top by pull request, and stage is not reset.')
    f.lane('stage', S, [(606, 1076)], pill=False)
    f.link('main', 556, M, 606, S, dash=True); f.dot('stage', 606, S, 'c')
    f.label(590, M + 24, 'stage is reset to main')
    f.step('A and B are merged into stage again from their own branches, each by its own pull request, in the order they first went into development. Nothing is built or run anywhere first.')
    f.link('feat', 650, A, 700, S); f.dot('stage', 700, S, 'm')
    f.link('feat', 720, B, 770, S); f.dot('stage', 770, S, 'm')
    f.label(735, S + 28, 'the rest, merged again')
    f.step('Either way stage has changed, so the whole suite is run on it again. After a feature comes off, QA\'s results for the features that remain stand. After a fix, a fresh agent checks again the scenarios of the feature that changed and what its fix touched. C is fixed on its own branch, tested, code reviewed where the fix is to a defect or a risk, and merged into development again. Once fixed, it may go back on the list.')
    f.dot('stage', 850, S, 'q', tip='The whole suite is run on stage again, because stage has changed.'); f.label(850, S - 20, 'the suite, run again')
    f.label(400, C - 16, 'goes back to be fixed', 'start')
    return f


# Items come out of development ---------------------------------------------------
def comeout():
    f = Fig(1100, 372, 'Development is reset to main when an item needs to come out of it. The features still in progress are then merged into it again from their own branches.')
    A, B, C, D, M = 56, 108, 160, 244, 316
    f.lane('feat', A, [(X0, 660)], 'feature A')
    f.lane('feat', B, [(X0, 730)], 'feature B')
    f.lane('feat', C, [(X0, 440)], 'feature C')
    f.lane('dev', D, [(X0, 566)])
    f.lane('main', M)
    for i, y in enumerate((A, B, C)):
        x = 232 + 60 * i
        f.link('feat', x, y, x + 48, D); f.dot('dev', x + 48, D, 'm')
    f.step('Feature C needs to come out of development. An ordinary release does not cause this: after a release the released features are already on development, so it is usually left as it is.')
    f.dot('feat', 440, C, 'x', tip='Feature C needs to come out of development.')
    f.label(456, C + 4, 'needs to come out', 'start', True)
    f.step('On the maintainer\'s word, development is reset to main. Everyone is told, so that anyone with a copy takes it from GitHub again.')
    f.lane('dev', D, [(612, 1076)], pill=False)
    f.link('main', 562, M, 612, D, dash=True); f.dot('dev', 612, D, 'c')
    f.label(596, M + 26, 'development is reset to main')
    f.step('Every feature it held that is still in progress and does not need to come out is merged into it again, each from its own branch by pull request. Recorded resolutions replay a conflict already resolved on that machine.')
    f.link('feat', 660, A, 710, D); f.dot('dev', 710, D, 'm')
    f.link('feat', 730, B, 780, D); f.dot('dev', 780, D, 'm')
    f.label(745, D + 28, 'the rest, merged again')
    return f


def p_pull():
    f, L, R = pair(226, 'run git pull on development or stage', 'take the branch as it is on GitHub', 'After a reset, a pull merges the old commits back into a local copy. Taking the branch as it is on GitHub replaces the copy.')
    G, C = 84, 150
    for H in (L, R):
        H.lane('dev', G, [(X0, 330), (372, 516)], 'on GitHub')
        for x, t in ((214, 'A'), (256, 'B')):
            H.dot('dev', x, G, 'm'); H.label(x, G - 18, t)
            H.dot('dev', x, C, 'm')
        H.dot('dev', 372, G)
        H.label(364, G - 18, 'reset to main', 'start')
    L.lane('dev', C, None, 'your copy')
    L.link('dev', 392, G, 440, C, tip='git pull merges the reset branch into your copy. The old commits stay, so A and B come back.', cmd='git pull'); L.dot('dev', 440, C, 'm')
    L.label(452, C - 26, 'git pull', 'start', True)
    L.chips(398, 200, 'your copy holds:', [('A', 'hot'), ('B', 'hot'), ('main', 'main')])
    R.lane('dev', C, [(X0, 330), (440, 516)], 'your copy')
    R.link('dev', 392, G, 440, C, dash=True, tip='Your copy is taken from GitHub with no local branch, so it is the branch as it is there.', cmd='git fetch origin\ngit switch --detach origin/development'); R.dot('dev', 440, C)
    R.chips(398, 200, 'your copy holds:', [('main', 'main')])
    return f.svg()


def p_update():
    f, L, R = pair(276, 'use "Update branch" or the conflict editor', 'resolve it on a merge branch', 'GitHub\'s Update branch merges development into the feature, which then carries every other feature into stage. A merge branch leaves the feature unchanged.')
    D, X, S = 76, 142, 208
    L.lane('dev', D); L.lane('feat', X, [(X0, 440)], 'feature X'); L.lane('stage', S)
    for x, t in ((214, 'A'), (256, 'B')):
        L.dot('dev', x, D, 'm'); L.label(x, D - 18, t)
    L.dot('feat', 204, X)
    L.link('dev', 290, D, 336, X, tip='Update branch merges development into feature X. The feature now holds A and B.'); L.dot('feat', 336, X, 'm')
    L.label(322, D + 26, 'Update branch', 'start', True)
    L.link('feat', 440, X, 486, S); L.dot('stage', 486, S, 'm')
    L.chips(374, 246, 'arrives on stage:', [('X', 'feat'), ('A', 'hot'), ('B', 'hot')])
    D2, Mg, X2 = 76, 142, 208
    R.lane('dev', D2); R.lane('mrg', Mg, [(296, 424)], 'merge branch'); R.lane('feat', X2, None, 'feature X')
    for x, t in ((214, 'A'), (244, 'B')):
        R.dot('dev', x, D2, 'm'); R.label(x, D2 - 18, t)
    R.dot('feat', 204, X2)
    R.link('dev', 256, D2, 296, Mg)
    R.link('feat', 310, X2, 356, Mg); R.dot('mrg', 356, Mg, 'q')
    R.link('mrg', 424, Mg, 470, D2); R.dot('dev', 470, D2, 'm')
    R.label(344, X2 + 28, 'feature X is not changed', 'middle')
    return f.svg()


def p_squash():
    f, L, R = pair(214, 'squash or rebase a merge', 'make a real merge', 'A squash leaves one new commit with no link to the feature. A real merge keeps the link and names both branches.')
    X, D = 82, 148
    for H in (L, R):
        H.lane('feat', X, [(X0, 366)], 'feature X'); H.lane('dev', D)
        for x in (214, 262, 310):
            H.dot('feat', x, X)
    L.dot('dev', 416, D, tip='A squash: one new commit on development, with no link back to the feature.')
    L.label(416, D + 28, 'one new commit, no link to the feature')
    R.link('feat', 366, X, 416, D); R.dot('dev', 416, D, 'm')
    R.label(344, D + 28, "Merge branch 'feature/x' into development")
    return f.svg()


def p_rebase():
    f, L, R = pair(282, 'rebase a feature already merged somewhere', 'leave its commits as they are', 'Rebasing a merged feature makes new commits of the same work, so development and stage hold it twice under different commits.')
    X, D, S = 90, 154, 218
    for H in (L, R):
        H.lane('dev', D); H.lane('stage', S)
        for x in (204, 240):
            H.dot('feat', x, X)
        H.link('feat', 254, X, 300, D); H.dot('dev', 300, D, 'm')
    L.lane('feat', X, [(X0, 300), (344, 440)], 'feature X')
    for x in (362, 400):
        L.dot('hot', x, X)
    L.label(344, X - 20, 'rebased: new commits', 'start', True)
    L.link('hot', 440, X, 486, S); L.dot('stage', 486, S, 'm')
    L.chips(238, 256, 'the same work, twice:', [('old, on development', 'feat'), ('new, on stage', 'hot')])
    R.lane('feat', X, [(X0, 440)], 'feature X')
    R.link('feat', 440, X, 486, S); R.dot('stage', 486, S, 'm')
    R.chips(304, 256, 'in both:', [('the same commits', 'feat')])
    return f.svg()


def p_hotfix():
    f, L, R = pair(262, 'send a hotfix straight to main', 'release it through stage', 'A hotfix merged straight into main ships without being verified. Through stage it is verified first.')
    H_, S, M = 76, 142, 208
    for H in (L, R):
        H.lane('hot', H_, [(X0, 330)], 'hotfix'); H.lane('stage', S); H.lane('main', M)
        for x in (214, 266):
            H.dot('hot', x, H_)
    L.link('hot', 330, H_, 410, M); L.dot('main', 410, M, 'm'); L.tag(410, M, 'release')
    L.label(420, S - 16, 'never verified', 'start', True)
    R.link('hot', 330, H_, 376, S); R.dot('stage', 376, S, 'm')
    R.dot('stage', 422, S, 'q'); R.label(422, S - 20, 'verified')
    R.link('stage', 444, S, 490, M); R.dot('main', 490, M, 'm'); R.tag(490, M, 'release')
    return f.svg()


def p_backout():
    f, L, R = pair(232, 'back a failed feature out of stage', 'reset stage and merge the rest again', 'Reverting a failed feature leaves stage holding it and its undoing. A reset leaves only the features that are going out.')
    S, M = 86, 152
    for H in (L, R):
        H.lane('main', M)
        for x, t in ((214, 'A'), (252, 'B'), (290, 'C')):
            H.dot('stage', x, S, 'm'); H.label(x, S - 18, t)
        H.dot('stage', 334, S, 'x')
    L.lane('stage', S)
    L.dot('hot', 392, S, tip='A commit on stage that undoes C. stage now holds C and its undoing.'); L.label(392, S - 18, 'C undone', strong=True)
    L.chips(300, 204, 'stage holds:', [('A', 'feat'), ('B', 'feat'), ('C', 'hot'), ('C undone', 'hot')])
    R.lane('stage', S, [(X0, 356), (404, 516)])
    R.link('main', 358, M, 404, S, dash=True); R.dot('stage', 404, S)
    for x, t in ((440, 'A'), (478, 'B')):
        R.dot('stage', x, S, 'm'); R.label(x, S - 18, t)
    R.chips(300, 204, 'stage holds:', [('A', 'feat'), ('B', 'feat')])
    return f.svg()


def conflict():
    f = Fig(1100, 318, 'A pull request that does not merge is resolved on a merge branch cut from the receiving branch. The feature is merged into it, the conflict is resolved there, and the pull request is opened from that branch.')
    X, Mg, D = 70, 158, 246
    f.lane('feat', X, None, 'feature X')
    f.lane('dev', D)
    for x in (212, 256):
        f.dot('feat', x, X)
    f.dot('dev', 240, D, 'm')
    f.label(1070, X - 20, 'the feature itself is not changed', 'end')
    f.step('The feature\'s pull request into development does not merge. Whoever opened it resolves the conflict.')
    f.link('feat', 290, X, 372, D, tip='The pull request from feature X into development does not merge.'); f.dot('dev', 372, D, 'x')
    f.label(372, D + 32, '1  the pull request does not merge')
    f.step('A merge branch is cut from development as it is on GitHub.')
    f.link('dev', 430, D, 486, Mg)
    f.lane('mrg', Mg, [(486, 790)], 'merge branch')
    f.label(500, Mg + 28, '2  cut from development,\nas it is on GitHub', 'start')
    f.step('The feature is merged into the merge branch, and the conflict is resolved in that merge. The merge resolves the conflict and nothing else. The feature itself is not changed.')
    f.link('feat', 560, X, 624, Mg); f.dot('mrg', 624, Mg, 'q')
    f.label(640, X + 36, '3  the feature is merged in, and\nthe conflict is resolved here', 'start')
    f.step('The pull request is opened from the merge branch and merged. With recorded resolutions turned on, Git replays the resolution if the same conflict comes up on stage or after a reset, in the clone that recorded it.')
    f.link('mrg', 790, Mg, 852, D); f.dot('dev', 852, D, 'm')
    f.label(866, Mg + 28, '4  the pull request is\nopened from this branch', 'start')
    return f


MERGEONLY = [
    ('coord', 'Coordination branch', 'coordination/<id>-<name>', 'Features that require each other are built and tested together.', 'Never merged anywhere'),
    ('mrg', 'Merge branch', 'merge/<feature id>-into-<branch>', 'A conflict is resolved without changing the feature.', 'Merged into development or stage by pull request'),
]


def mergeonly():
    rows = ''.join(f'<tr class="c-{c}"><td><b>{esc(n)}</b><br><code>{esc(b)}</code></td><td>{esc(w)}</td><td>{esc(e)}</td></tr>' for c, n, b, w, e in MERGEONLY)
    return ('<div class="tablewrap"><table><thead><tr><th>A branch that holds merges and no work of its own</th><th>What it is for</th><th>Where it ends</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


WHO3 = [
    ('The maintainer', 'Decides what is released: names the release list, answers code review findings, gives the word to promote, and authorises resets, tags and repository settings.'),
    ('The product owner', 'Decides what is built: orders the backlog, agrees stories and scenarios, and accepts decisions about how the product behaves.'),
    ('The user', 'The person directing the work in the conversation: the one an agent asks, whose word governs, and under whose name commits are made.'),
]


def who3():
    cards = ''.join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in WHO3)
    return ('<h3 class="sub">Three words for who decides</h3>'
            f'<ul class="gives plain">{cards}</ul>'
            '<p class="note">On a project where one person holds all three, that person is the user, and an agent takes the user\'s word for each. Where a project names someone else as maintainer or product owner, that decision is theirs.</p>')

