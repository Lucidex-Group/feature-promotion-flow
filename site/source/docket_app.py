"""The third tab: Docket, the application. What it is, what it does, what it looks like, and how it runs Feature Promotion Flow.

The screenshots are files in site/images/docket/, taken of Docket v0.13.0, the released program, on November 24, 2026,
serving a made-up project, a lending library, written for this guide, with a remote of its own. Each page was reached by
clicking through the app.
"""
from html import escape as esc

SHOTS = 'images/docket/'
# The Docket release this tab describes, and where its files are published.
VERSION = 'v0.13.0'
RELEASE = f'https://github.com/Lucidex-Group/feature-promotion-flow/releases/tag/docket-{VERSION}'
FILES = [
    ('macOS, Apple silicon', f'docket-{VERSION}-darwin-arm64', 'macOS 13.0 or later. Not signed by Apple, not notarised.'),
    ('macOS, Intel', f'docket-{VERSION}-darwin-amd64', 'macOS 13.0 or later. Not signed by Apple, not notarised.'),
    ('Linux, 64-bit ARM', f'docket-{VERSION}-linux-arm64', 'Statically linked: it needs no other libraries.'),
    ('Linux, x86-64', f'docket-{VERSION}-linux-amd64', 'Statically linked: it needs no other libraries.'),
    ('Windows, x86-64', f'docket-{VERSION}-windows-amd64.exe', 'Never run by anyone. Untested.'),
]
LIMITS = [
    'The navigation of the guide inside Docket does not follow the reader in Safari.',
    'A commit-hook folder given relative to the project leaves the record\'s own folder without the hook.',
    'The adoption skill still carries one line of its makers\' own practice, and by default treats a conversion as a trial run on a copy.',
    'No agent has yet been run through a whole adoption with the adoption skill; three of its scenarios are checked as text only.',
    'No program from this release has been started on a Mac older than macOS 27.2, or on Windows. The minimum of macOS 13.0 is what the programs say they need, read from them, not something run.',
    'Docket\'s own pages, and the call an agent makes to report it, still call the one run of the whole suite on stage "testing together", an older name. The guide and the skills call it the suite\'s run. It is the same run.',
    'Docket does not make the regression count. It carries no script for it and does not tie a test\'s result to the scenario the test names, so a project writes its own script, or the run says the count was not made.',
    'Docket refuses a QA run that does not give a result for every scenario the release names. After a fix on stage, the fresh QA agent restates the scenarios it did not check again, each with a note that it stands from the earlier check.',
    'Docket\'s pages fetch their fonts from Google\'s servers, so the program reaches the internet, and looks different without a connection.',
    'Docket reads where a work item stands from this machine\'s own copies of development, stage and main, so it can say a feature is merged nowhere until those copies are brought up to the Git host\'s.',
    'Two lines of advice from docket assess still say stage is reset to main after a production deployment; the method has stage stay as it is after a release.',
]
SHOT_SIZE = (800, 692)


def cards(rows, cls='gives'):
    return f'<ul class="{cls}">' + ''.join(f'<li><h3>{esc(t)}</h3><p>{d}</p></li>' for t, d in rows) + '</ul>'


def shot(name, alt, caption):
    """A screenshot that opens full size when chosen, with its caption under it."""
    src = f'{SHOTS}{name}.jpg'
    return (f'<figure class="shot"><a href="{src}" target="_blank" rel="noopener" aria-label="Open the screenshot full size">'
            f'<img src="{src}" alt="{esc(alt)}" loading="lazy" width="{SHOT_SIZE[0]}" height="{SHOT_SIZE[1]}"></a>'
            f'<figcaption>{caption}</figcaption></figure>')


DOES = [
    ('It keeps the backlog', 'Use cases and their flows, the stories sliced from them, the work items that deliver each story, and the scenarios each one has to meet. Each item carries its status, its order and who it is assigned to.'),
    ('It keeps the decisions and the evidence', 'Decisions are kept in the words of whoever made them, beside the thing they are about. Estimates, attempts, test runs and code reviews are kept on the work item they belong to.'),
    ('It shows where work stands', 'Where each work item is, on <code>development</code>, <code>stage</code> or <code>main</code>, is read from the merges of the branch named for it. It is not a status someone sets.'),
    ('It serves a person and an agent the same record', 'Web pages for a person, and a connection for an agent (the Model Context Protocol). Both call the same code, and an agent is told the rules of the flow when it connects.'),
    ('It checks the record', '<code>docket check</code> reports slips against the flow. <code>docket assess</code> says what adopting a project would involve, and changes nothing.'),
    ('It reports', 'On delivery, quality, agents, effort and coverage, read out of the record. The reports are partly built.'),
]
WORKS = [
    ('One program, run on your own machine', 'Docket is installed apart from the projects it serves, and puts nothing of its own into them: no packages, no database, no plugin. <code>docket serve</code>, started in any folder of a project, serves that project on its own port, on the local machine only. One server is one project.'),
    ('The record is files, and there is no database', 'The record is files under <code>.docket/</code> and <code>features/</code>, with the project\'s own documents. Everything Docket shows is read from those files and from Git on each request.'),
    ('It writes files and does not commit', 'Docket never stages, commits or pushes, and runs no Git command that changes a repository. It refuses a write based on a file that has changed since it was read. Whoever did the work commits it.'),
    ('It reads Git', 'Who the people are, from the authors of commits. Whether a record file is committed and pushed. And where a work item is, from the titles of the merges on <code>development</code>, <code>stage</code> and <code>main</code>.'),
    ('It is served from the record\'s folder', 'The record has a permanent branch, <code>docket-record</code>, checked out in a folder of its own. Docket reads and writes only that folder, so it always shows one record.'),
    ('The server keeps the time', 'Every call is stamped by the server when it arrives, so the times in the record do not rest on an agent\'s say-so.'),
]
STEPS = [
    ('Before the work', 'The use case, the story and its scenarios are written through Docket, on <code>docket-record</code>. A new scenario is tagged <code>@wip</code>, so a test runner leaves it out until it is built. Work that names no scenario, and gives no reason, is not ready, and Docket names no branch for it.'),
    ('Starting', 'An agent asks for its brief: the work item, its story, its scenarios and the decisions that bear on it, with the branch to cut. It records what it expects the work to take, and opens an attempt. The server stamps the start.'),
    ('Building', 'The feature is built on its own branch, cut from <code>docket-record</code>, so the work item and its scenarios are in the feature\'s folder from its first commit. The feature removes the <code>@wip</code> tag from the scenarios it builds, in the same commits as the code.'),
    ('Testing and code review', 'Test runs are reported against the work item, scenario by scenario or from a JUnit or Cucumber report. A code review is reported with who reviewed it, the commit read, the decision, and each finding with what was done about it.'),
    ('Merging', 'Pull requests are reported against the work item. Where it stands is then read from the merges themselves: on <code>development</code>, on <code>stage</code>, or released.'),
    ('The suite, QA and release', 'The run of the whole suite on <code>stage</code> is reported against the commit it ran on, with each command and its result; Docket\'s own pages still call it testing together. QA of <code>stage</code> is reported as a run of its own, with a result for each scenario the release list names, never mixed with the feature\'s own tests. A release is marked by its two tags on <code>main</code>, and Docket reads the history of releases from them; a release can also be reported to Docket, which checks it against Git.'),
]
GUARDS = [
    ('A commit hook', 'Keeps code off <code>docket-record</code> and the record off features. The one change to the record a feature may make is taking the <code>@wip</code> tag off the scenarios it builds.'),
    ('Status against the merges', 'A work item cannot be set done while a branch of its own holds work that is not released. <code>docket check</code> lists each status the merges contradict.'),
    ('A plan to rebuild', '<code>docket rebuild</code> gives the plan, with the commands, to rebuild <code>development</code> or <code>stage</code> from the released branch, leaving out what must come out. It runs none of them.'),
    ('The skills that go with it', 'Docket installs the skills an agent needs: five of the flow\'s, as the standards write them, and two of its own, under <a href="#its-skills">Its own skills</a>. <code>docket skills install</code> says what it will write before it writes it.'),
]
OWN_SKILLS = [
    ('docket-flow', 'What Docket changes in the flow', 'What Docket adds to Feature Promotion Flow in a project that keeps its record with Docket: the <code>docket-record</code> branch between <code>main</code> and a feature, where the record is written, and what is recorded at each step. An agent loads it together with the flow\'s own skills, before any Git command that changes anything, in a project that has a <code>.docket/</code> folder.'),
    ('adopt-project', 'Adopting a project', 'Brings an existing project under Docket. It keeps a record of the run in the project itself, checks that the project is safe to work in, assesses it, proposes the changes, applies them only after the project\'s owner agrees, and tells the owner what the run met. An agent uses it when asked to adopt a project, or when <code>docket assess</code> reports something missing.'),
]
START = [
    ('Assess the project', '<code>docket assess &lt;folder&gt;</code> reports what adopting the project would involve: what is in place, what is missing, and what waits on a decision. It changes nothing.'),
    ('Adopt it', 'The adoption skill proposes the changes, and applies them only after the project\'s owner agrees: <code>.docket/config.yaml</code>, the <code>docket-record</code> branch and its folder, a section in the instructions for agents, the agent connection and the commit hook. It takes each template, the hook and the schemas from the program, with <code>docket carries</code>.'),
    ('Serve it', '<code>docket serve</code>, from any folder of the project, finds the folder where <code>docket-record</code> is checked out and serves it on the project\'s own port. <code>docket ports</code> lists the projects served on the machine.'),
    ('Connect an agent', 'An agent connects to Docket at <code>/mcp</code> on the same address. For Claude Code: <code>claude mcp add --transport http docket http://127.0.0.1:&lt;port&gt;/mcp</code>.'),
]


def get_docket():
    """Where to download Docket, how to check the download, and how to run it the first time."""
    rows = ''.join(f'<tr><td>{esc(sysname)}</td><td><a href="{RELEASE.replace('/tag/', '/download/')}/{esc(f)}"><code>{esc(f)}</code></a></td><td>{esc(note)}</td></tr>' for sysname, f, note in FILES)
    mac = f'docket-{VERSION}-darwin-arm64'
    return (f'<p class="say">Docket is one program file, with nothing else to install. Download the file for your system from the release <a href="{RELEASE}" target="_blank" rel="noopener">docket-{VERSION}</a>, check it, make it runnable, and put it where your shell finds it, named <code>docket</code>: the adoption skill and <code>docket assess</code> give commands that begin with <code>docket</code>. Docket also needs Git installed and on your <code>PATH</code>: it reads the repository by running <code>git</code>, and without it cannot read a project.</p>'
            f'<div class="tablewrap"><table class="setup"><thead><tr><th>System</th><th>File</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></div>'
            '<h3 class="sk">Check the download</h3>'
            f'<p>Download <code>docket-{VERSION}-checksums.txt</code> from the same release into the same folder, then:</p>'
            f'<pre class="cmd">shasum -a 256 -c --ignore-missing docket-{VERSION}-checksums.txt</pre>'
            '<p>It should say OK for each file you downloaded. On Linux, <code>sha256sum -c --ignore-missing</code> does the same.</p>'
            '<h3 class="sk">The first run on macOS</h3>'
            '<p>The macOS programs are not signed by Apple and not notarised, and macOS blocks a program from the web that is not. These commands make the file runnable, clear the block, and run it:</p>'
            f'<pre class="cmd">chmod +x {mac}\nxattr -d com.apple.quarantine {mac}\n./{mac} version</pre>'
            f'<p>The last line prints <code>{VERSION}</code>. If your browser did not mark the file, the second prints <code>No such xattr: com.apple.quarantine</code>: that is not an error, there was nothing to clear. For an Intel Mac, use the <code>darwin-amd64</code> file the same way.</p>'
            '<h3 class="sk">On Linux</h3>'
            f'<pre class="cmd">chmod +x docket-{VERSION}-linux-amd64\n./docket-{VERSION}-linux-amd64 version</pre>'
            '<h3 class="sk">Putting it on your path</h3>'
            '<p>Move the file you downloaded there, named <code>docket</code>. For the Apple silicon program:</p>'
            f'<pre class="cmd">sudo mv {mac} /usr/local/bin/docket\ndocket version</pre>'
            '<p>For any other system, put the name of the file you downloaded in place of the first name, such as '
            f'<code>docket-{VERSION}-linux-amd64</code> on Linux on x86-64. <code>/usr/local/bin</code> belongs to the system, hence <code>sudo</code>. A folder on your <code>PATH</code> that you own, such as <code>~/bin</code>, needs none.</p>'
            '<h3 class="sk">Windows</h3>'
            '<p>The Windows program is offered as built, but no one has yet run it. The command Docket gives to install its commit hook is written for a Unix shell.</p>'
            '<h3 class="sk">Licence</h3>'
            '<p>The program is under the MIT License, copyright (c) 2026 Lucidex Group. The skills and the guide it carries are under CC BY 4.0. The names Docket, Feature Promotion Flow and Lucidex Group are not licensed beyond credit. The release carries the licence and the notices of what Docket is built with, and <code>docket licence</code> prints them.</p>'
            '<p class="note"><b>Known limits.</b> Recorded in Docket\'s own backlog, and taken off this list as each is fixed:</p>'
            '<ul class="limits">' + ''.join(f'<li>{esc(x)}</li>' for x in LIMITS) + '</ul>')


def doc():
    pages_intro = (f'<p class="note shotnote"><b>About the screenshots.</b> They are of Docket {VERSION}, the released program, serving a small made-up project, a lending library, written for this guide. '
                   'No real project\'s record is shown. Choose a screenshot to open it full size.</p>')
    parts = [
        ('What Docket is', 'For a person deciding whether to put a project on Docket.', [
            ('docket', 'What Docket is',
             '<p class="say">Docket is a program that keeps a record of everything a software project creates, in the project\'s own repository, for people and agents to work through: use cases, stories, scenarios, work items, decisions, and the evidence of what was done and tested.</p>'
             '<p class="note">It is a ticket tracker whose tickets are files in the repository. It was built to run Feature Promotion Flow, and the second tab of this guide describes the flow as a project on Docket runs it.</p>'
             + pages_intro + shot('work', 'Docket\'s Work page for the made-up lending library: use cases, stories, decisions and work items in one table, with status and estimates.',
                    '<b>The Work page.</b> The backlog as one table: each use case, the stories sliced from it, the decisions beside them and the work items that deliver them, in the order of work, with status, estimate and actual effort. A proposed decision that waits on a person is marked as needing attention.')),
            ('does', 'What it does', cards(DOES)),
            ('works', 'How it works', cards(WORKS, 'gives two')),
            ('not', 'What it is not',
             '<p class="say">Docket is not a hosted service. It has no sign-in and no database shared between users, and it does not deploy anything.</p>'
             '<p class="note">Docket is in active development. Its commands, and what an agent\'s calls return, can change between releases without notice. A project on Docket can be worked on without it, because every step is plain Git and the record is plain files.</p>'
             f'<p class="note"><b>Getting it.</b> Docket\'s source is not public. The program itself is published, for macOS, Linux and Windows: see <a href="#get">Get Docket</a>.</p>'),
        ]),
        ('Its pages', 'What a person sees, page by page.', [
            ('layout', 'How the pages are arranged',
             '<p class="say">The pages follow the life of the work. <b>Define:</b> Principles and Decisions. <b>Do:</b> Work, the backlog as one table, with what needs attention. <b>Deliver:</b> Environments, History and Reports. <b>Project:</b> Artifacts, Participants, Record health and the Guide. <b>You:</b> Settings.</p>'
             '<p class="note">Everything in the backlog opens where it is, in the Work table: choose a row and it unfolds beneath itself, with what can be done to it.</p>'),
            ('work-item', 'A work item',
             '<p class="say">A work item, opened in the Work table, shows where it stands, how it got there and what it was tested against.</p>'
             + shot('work-item', 'A work item opened in Docket\'s Work table, Borrowing at the desk: its effort and budget, its status done, released and accepted, a button to object and reopen it, and its line of stamped times.',
                    '<b>A work item, done, released and accepted.</b> Its effort against its estimate and budget, with hours a person can add. Its status, and beside it "Released", read from the merges. Under it, Docket says why it counts as accepted: \u201cAn agent reported it done, and that work and its record are committed and pushed.\u201d A person can still object and reopen it. Below, the line of its times, each stamped by Docket\'s server.')
             + shot('work-item-tests', 'Further down the same work item: the story it delivers, each scenario with its text and a passing test result, and what it was tested against.',
                    '<b>Further down: its scenarios and tests.</b> The story it delivers, and each scenario with its words and its latest result, who ran it and when. When the work item was set to done, what it was tested against was frozen, so it does not change when a scenario does later.')),
            ('use-case', 'A use case and its stories',
             '<p class="say">A use case, opened in the Work table the same way, holds the goal, its flows, and the stories sliced from each flow.</p>'
             + shot('use-case', 'A use case opened in Docket\'s Work table, Borrow a book: its actors and state, its text with the main flow, and its flows with their stories and where each stands.',
                    '<b>A use case.</b> Its primary and supporting actors, its state, who wrote it, its text, and below, each flow with the stories sliced from it and where each stands: "Borrow a book on the shelf" is delivered and proven; "Reserve a book that is out" is in progress.')),
            ('decisions', 'Decisions',
             '<p class="say">The Decisions page lists the project\'s design decisions, each with whether it is in force, proposed, decided against or replaced. It reads them from the project\'s own numbered decision files, and an agent is given those that bear on its work when it asks for its brief.</p>'
             + shot('decisions', 'Docket\'s Decisions page for the made-up lending library: two decisions in force and one decided against, each with its number and state.',
                    '<b>The decisions.</b> Each numbered decision file, with its title and its state as the project wrote it: keeping one catalogue for every branch library and identifying members by card number are in force; charging late fines was decided against. Choose a row to read the decision. Smaller decisions about a story are kept beside it in the Work table.')),
            ('environments', 'Where work is',
             '<p class="say">The Environments page shows what each branch carries, read from the merges each time.</p>'
             + shot('environments', 'Docket\'s Environments page: Development carries Reservations and Borrowing at the desk; Stage carries Borrowing at the desk; Released below.',
                    '<b>Environments.</b> The branch is the environment, and a merge into it is the promotion. Reservations is on <code>development</code> only; Borrowing at the desk has reached <code>stage</code> and been released. Nothing was recorded to say so: it is read from the merge titles.')),
            ('releases', 'The releases',
             '<p class="say">The History page lists the releases, newest first, as an agent reported each one after the promotion.</p>'
             + shot('history', 'Docket\'s History page: release v0.1.0 with its date, commit, the pull request that promoted it, its two tags on the release\'s commit, its work item, QA, what was verified, and who accepted it.',
                    '<b>A release.</b> The pull request that promoted it, its two tags, the work items it brought and the pull request of each, the commit QA tested, what was verified, and who accepted it. Docket checked against Git that the commit, the tags and the merges are where the agent said; the rest is as the agent stated it, and the page says which is which.')),
            ('guide', 'The guide inside Docket',
             '<p class="say">Docket carries its own guide to what a project on it has to be, and to Feature Promotion Flow, for a person on the Guide page and for an agent when it connects.</p>'
             + shot('guide', 'The Guide page inside Docket: one guide in eight parts, each a page of its own, with its contents in the navigation on the left.',
                    '<b>The guide.</b> One guide in eight parts, from what a project on Docket has to be to who decides what, each a page of its own, with its contents in the navigation on the left. The same text is given to a person here, to an agent through its connection, and at a terminal: <code>docket guide</code> lists its parts, and <code>docket guide &lt;part&gt;</code> gives one.')),
        ]),
        ('How Docket runs the flow', 'What Docket records and checks at each step of Feature Promotion Flow.', [
            ('record-branch', 'The record has its own branch',
             '<p class="say">The record is kept on <code>docket-record</code>: <code>main</code> plus everything recorded since. Work is cut only from it, so a work item, its scenarios and the evidence of its attempts and tests travel in the same history as the code that delivers it, and a build carries its own work items.</p>'
             '<p class="note">Why the record has a branch of its own, and what each branch holds, are in the second tab: <a href="#d-why">Why it exists</a> and <a href="#d-holds">What each branch holds</a>.</p>'),
            ('each-step', 'What is recorded at each step', cards(STEPS)),
            ('guards', 'What keeps the flow straight', cards(GUARDS, 'gives two')),
            ('its-skills', 'Its own skills',
             '<p class="say">Docket installs five of the flow\'s skills as the standards write them, each with a note that a project on Docket reads it together with <code>docket-flow</code>, which governs where they differ, and two of its own. Setting a project up is done by its own adoption skill, in place of the flow\'s. The flow\'s skills are in the <a href="#s-overview">Skills</a> tab; Docket\'s own two are these.</p>'
             + '<ul class="gives two">' + ''.join(f'<li><h3>{esc(t)}</h3><p class="skillname">The skill <code>{esc(n)}</code></p><p>{d}</p></li>' for n, t, d in OWN_SKILLS) + '</ul>'
             + '<p class="note">The text of these two skills is not shown here. It comes with the program: <code>docket skills</code> lists the skills it carries, and <code>docket skills install</code> writes them into a project. It says each file it will write and asks first, and leaves a skill that differs alone unless told to replace it.</p>'),
        ]),
        ('Getting started', 'Getting Docket, and putting a project on it.', [
            ('get', 'Get Docket', get_docket()),
            ('start', 'From a project to a project on Docket', cards(START, 'gives two')
             + '<p class="note">What adopting adds to a project, and what using Docket commits it to, are in the second tab: <a href="#d-adds">What Docket adds to a project</a>.</p>'),
        ]),
    ]
    return {
        'title': 'Docket',
        'lede': 'The program that keeps a project\'s record in its own repository, and runs Feature Promotion Flow: what it does, what it looks like, and how it runs the flow.',
        'intro': 'Docket keeps everything a software project creates as files in the project\'s own repository, and shows that record as pages to a person and through a connection to an agent. It reads where each piece of work stands from the merges in Git, so what it shows is the history, not what someone remembered to set.',
        'repo': f'Docket\'s source is not public. Its programs are published as the release docket-{VERSION} of Lucidex-Group/feature-promotion-flow.',
        'parts': parts,
    }
