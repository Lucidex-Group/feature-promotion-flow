"""The Skills tab: the skills the package delivers, read from plugin/skills/ when the page is built.

Each skill's description, its outline and its whole text come from its SKILL.md, so the page cannot fall behind the files.
What each skill does, in a sentence, is written here; a skill in the package with no sentence here, or a sentence with no
skill, stops the build.
"""
import os
import re
from html import escape as esc

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(HERE, '..', '..', 'plugin', 'skills')
REPO = 'https://github.com/Lucidex-Group/feature-promotion-flow'
FILES = f'{REPO}/blob/main/plugin/skills/'

# What each skill does, in plain words, for a person deciding whether to use it: a line for the table, and a fuller account.
DOES = {
    'feature-promotion-flow': ('The method: branches, merges, who may do what, and the names of the checks', 'The method itself: which branches there are, what is cut from what, how merges are made, who may do what without asking, and what each check is called. The other five skills are its procedures, and each starts by loading it.'),
    'fpf-set-up-project': ('Sets a repository up for the flow, once', 'Gets a repository ready once: creates development and stage from main, allows merge commits only, protects the three branches, sets up the clone, and lists what the project\'s own instruction file has to say.'),
    'fpf-start-feature': ('Starts a piece of work on its own branch and folder', 'Checks that a piece of work is ready to build, then cuts its branch from main, named for the work, in a folder of its own.'),
    'fpf-build-to-development': ('Code reviews a feature and merges it into development', 'Takes a feature from passing tests to development: a code review by an agent that did not write it, each finding classified and dealt with, the merge by pull request, and testing with the other features. It also says when a feature is eligible for stage.'),
    'fpf-release': ('Makes a release, from the chosen set to the tags', 'Makes a release from the features the maintainer chooses: a candidate tested on a machine, the set merged into stage by pull request, QA by a fresh agent, and on the maintainer\'s word the promotion, the tags, and the release brought back into development.'),
    'fpf-hotfix': ('Releases a fix that cannot wait', 'Releases a fix that cannot wait for the next release: cut from main, code reviewed, sent alone through stage and QA, then promoted and brought back into development.'),
}
# The title each skill's section goes by, in plain words; the skill's own name stands under it.
TITLES = {
    'feature-promotion-flow': 'The flow itself',
    'fpf-set-up-project': 'Setting a project up',
    'fpf-start-feature': 'Starting a feature',
    'fpf-build-to-development': 'Building to development',
    'fpf-release': 'Making a release',
    'fpf-hotfix': 'Making a hotfix',
}
PARTS = [
    ('The method', 'The skill an agent loads before any Git command that changes anything.', ['feature-promotion-flow']),
    ('Setting up and starting', 'Once for a project, and once for each piece of work.', ['fpf-set-up-project', 'fpf-start-feature']),
    ('Building and releasing', 'From a feature\'s passing tests to a release, and the fix that cannot wait.', ['fpf-build-to-development', 'fpf-release', 'fpf-hotfix']),
]


def inline(text):
    """A line of the skill's Markdown as HTML: code, bold and links, everything else escaped."""
    out = esc(text.replace('**', ''))
    out = re.sub(r'`([^`]+)`', r'<code>\1</code>', out)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', out)


def read(name):
    text = open(os.path.join(SKILLS, name, 'SKILL.md')).read()
    front, body = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S).groups()
    desc = re.search(r'^description:\s*"?(.*?)"?\s*$', front, re.M).group(1)
    # The outline: each heading, with the steps numbered under it; steps before any heading stand on their own.
    outline, current = [], None
    for line in body.splitlines():
        if line.startswith('## '):
            current = (line[3:], [])
            outline.append(current)
        elif re.match(r'\d+\. \*\*', line):
            step = re.match(r'\d+\. \*\*(.+?)\*\*', line).group(1).rstrip(':,')
            if current:
                current[1].append(step)
            else:
                outline.append((step, None))
    refs = sorted(os.listdir(os.path.join(SKILLS, name, 'reference'))) if os.path.isdir(os.path.join(SKILLS, name, 'reference')) else []
    return {'text': text, 'desc': desc, 'outline': outline, 'refs': refs}


def outline_html(outline):
    items = []
    for title, steps in outline:
        sub = f'<ol>{"".join(f"<li>{inline(s)}</li>" for s in steps)}</ol>' if steps else ''
        items.append(f'<li>{inline(title)}{sub}</li>')
    return f'<ol class="outline">{"".join(items)}</ol>'


def section(name):
    s = read(name)
    refs = ''
    if s['refs']:
        links = ', '.join(f'<a href="{FILES}{name}/reference/{r}" target="_blank" rel="noopener"><code>{esc(r)}</code></a>' for r in s['refs'])
        refs = f'<p class="note"><b>Comes with.</b> Reference files it points to when they are needed: {links}.</p>'
    return (name, TITLES[name],
            f'<p class="skillname">The skill <code>{esc(name)}</code></p><p class="say">{esc(DOES[name][1])}</p>'
            f'<h3 class="sk">When it is used</h3><p>{inline(s["desc"])}</p>'
            f'<h3 class="sk">What it covers</h3>{outline_html(s["outline"])}{refs}'
            f'<details class="skilltext"><summary>The whole skill, as an agent reads it</summary>'
            f'<p class="muted"><a href="{FILES}{name}/SKILL.md" target="_blank" rel="noopener"><code>plugin/skills/{name}/SKILL.md</code></a></p>'
            f'<pre>{esc(s["text"])}</pre></details>')


def doc():
    found = sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, 'SKILL.md')))
    placed = sorted(n for _, _, names in PARTS for n in names)
    if found != sorted(DOES) or found != placed or found != sorted(TITLES):
        raise SystemExit(f'the Skills tab and plugin/skills/ disagree: skills {found}, described {sorted(DOES)}, placed {placed}')
    table = ''.join(f'<tr><td><a href="#{n}">{esc(TITLES[n])}</a><br><code>{esc(n)}</code></td><td>{esc(DOES[n][0])}.</td></tr>'
                    for _, _, names in PARTS for n in names)
    first = [
        ('what', 'What the skills are',
         '<p class="say">A skill is a set of written instructions an agent loads when the work calls for it. These six are Feature Promotion Flow written for an agent: the method, and a procedure for each step of it.</p>'
         '<p class="note">They are the flow on its own. A project that keeps its record with Docket adds Docket\'s own skills, which are listed in the <a href="#a-its-skills">Docket</a> tab.</p>'
         f'<div class="tablewrap"><table class="skilltable"><thead><tr><th>Skill</th><th>What it does</th></tr></thead><tbody>{table}</tbody></table></div>'),
        ('install', 'Installing them',
         '<p class="say">They are a plugin for Claude Code. In Claude Code, add this repository as a plugin marketplace, then install the plugin:</p>'
         '<pre class="cmd">/plugin marketplace add Lucidex-Group/feature-promotion-flow\n/plugin install feature-promotion-flow@lucidex-feature-promotion-flow</pre>'
         '<p>Or copy the folders under <code>plugin/skills/</code> in the repository into your own skills folder: <code>~/.claude/skills/</code> for every project, or <code>.claude/skills/</code> in one project.</p>'
         f'<p class="note"><b>The repository.</b> <a href="{REPO}" target="_blank" rel="noopener">github.com/Lucidex-Group/feature-promotion-flow</a>. The skills are licensed CC BY 4.0: use, adapt and share them, with credit to Lucidex Group.</p>'),
        ('project-says', 'What a project says for itself',
         '<p class="say">The skills say what is written down, reviewed, reported and decided. They leave to each project\'s own instruction file where its backlog, code reviews, QA reports and decisions are kept, who the maintainer and the product owner are, and how its tests are run. <a href="#fpf-set-up-project"><code>fpf-set-up-project</code></a> lists them.</p>'
         '<p class="note">The skills name a folder for each branch under <code>~/Development/worktrees/&lt;Project&gt;/</code>. Use another place if you prefer; what matters is one folder to a branch.</p>'),
    ]
    parts = [('The skills', 'What an agent is given, and how to install it.', first)]
    parts += [(t, d, [section(n) for n in names]) for t, d, names in PARTS]
    return {
        'title': 'Skills',
        'lede': 'The six skills delivered with Feature Promotion Flow: what each does, when an agent uses it, and its whole text.',
        'repo': 'Lucidex-Group/feature-promotion-flow, in plugin/',
        'intro': 'An agent working by the flow loads these skills as it works. Each section below is built from the skill\'s own file, so what you read here is what the agent reads.',
        'parts': parts,
    }
