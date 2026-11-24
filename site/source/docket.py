"""The second tab: Feature Promotion Flow as a project on Docket runs it, built from Docket's own guide.

Docket carries its guide, and a running Docket gives it at GET /api/guide. A copy taken from the released program is
pinned for each Docket release this site describes, in docket-guide/<version>.json, and this module lays it out as the
public guide's other tabs are laid out. The words, figures and tables are Docket's, under CC BY 4.0. What is the public
site's alone is here: the card that points to the Docket tab, the repository line, and the footer.

Docket's guide is not a fixed format: its shape and its ids can change in any release. So nothing here guesses. A part,
a section or a link this module does not know stops the build and names it, and a new Docket release is taken in by
pinning its copy and bringing the maps below up to it.
"""
import json
import os
import re

from docket_app import VERSION

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, 'docket-guide', f'{VERSION}.json')

# Docket's parts, in order, as the public tab numbers them; its sources become the tab's reference page.
PARTS = ['project', 'why', 'flow', 'releases', 'trouble', 'mistakes', 'who']
SOURCES = 'sources'
# Docket's section ids, and the shorter ids this tab has always used, kept so that links people have saved still lead there.
IDS = {
    'what-using-docket-commits-a-project-to': 'commits',
    'what-docket-keeps': 'keeps',
    'what-docket-adds-to-a-project': 'adds',
    'a-project-with-no-docket-record-branch': 'not-moved',
    'why-it-exists-and-why-the-record-has-its-own-branch': 'why',
    'its-limits-stated-first': 'limits',
    'where-docket-keeps-your-tickets': 'tracker',
    'what-the-parts-add-up-to': 'addup',
    'problems-teams-commonly-report-and-what-this-does-about-them': 'problems',
    'working-with-ai-agents': 'agents',
    'the-road-from-the-record-to-main': 'road',
    'one-feature-step-by-step': 'steps',
    'the-checks-in-order': 'checks',
    'what-makes-a-feature-eligible-for-stage': 'eligible',
    'what-each-branch-holds': 'holds',
    'where-everyone-works': 'folders',
    'a-release': 'release',
    'the-whole-cycle-as-a-loop': 'loop',
    'testing-the-release-set-before-stage-is-built': 'candidate',
    'how-the-history-says-where-work-is-and-how-a-release-is-named': 'history',
    'rework-after-a-code-review': 'rework',
    'when-a-feature-fails-on-stage': 'fails',
    'when-items-need-to-come-out-of-development': 'comeout',
    'a-hotfix': 'hotfix',
    'a-bad-release-already-on-main': 'rollback',
    'resolving-a-conflict': 'conflict',
    'features-that-require-each-other': 'coordination',
    'why-every-branch-is-cut-from-the-record': 'cut',
    'the-other-mistakes-in-pairs': 'mistakes',
    'who-may-do-what-without-asking': 'who',
}
# Links inside Docket's app, and where each leads in this tab.
LINKS = {
    '#/guide/flow/what-each-branch-holds': '#holds',
    '#/guide/sources': '#sources',
    '#/guide/why/why-it-exists-and-why-the-record-has-its-own-branch': '#why',
}


def stop(problem):
    raise SystemExit(f'Docket\'s guide {VERSION} ({os.path.relpath(GUIDE)}): {problem}. Bring docket.py up to it; nothing has been built.')


def links(html):
    """Docket's in-app links as links in this tab; any other in-app link stops the build."""
    unknown = sorted(set(re.findall(r'href="(#/[^"]*)"', html)) - set(LINKS))
    if unknown:
        stop('links this tab does not know: ' + ', '.join(unknown))
    return re.sub(r'href="(#/[^"]*)"', lambda m: f'href="{LINKS[m.group(1)]}"', html)


def inner(section):
    """A section's content without its own <section> and <header>, which this site's builder writes."""
    html = section['html']
    m = re.fullmatch(r'<section id="([^"]+)"[^>]*>\s*<header>.*?</header>(.*)</section>\s*', html, re.S)
    if not m or m.group(1) != section['id']:
        stop(f'section {section["id"]} is not a <section> with its header first')
    return links(m.group(2))


def whole(section, our):
    """A section kept whole, as the opening sections of a part are, with this tab's id."""
    html = section['html']
    if not html.startswith(f'<section id="{section["id"]}"'):
        stop(f'section {section["id"]} does not open with its own id')
    return links(html.replace(f'id="{section["id"]}"', f'id="{our}"', 1))


def doc():
    d = json.load(open(GUIDE))
    for key in ('title', 'text', 'flow', 'parts', 'foot'):
        if key not in d:
            stop(f'no "{key}"')
    names = [p.get('name') for p in d['parts']]
    if names != PARTS + [SOURCES]:
        stop(f'parts {names}, where this tab expects {PARTS + [SOURCES]}')
    seen = [s['id'] for p in d['parts'] for s in p['sections']]
    if sorted(seen) != sorted(IDS):
        stop('sections this tab does not know: ' + ', '.join(sorted(set(seen) - set(IDS)))
             + '; sections it expects and does not find: ' + ', '.join(sorted(set(IDS) - set(seen))))
    parts = {p['name']: p for p in d['parts']}

    first = [{'id': 'docket', 'title': 'What Docket is',
              'html': '<section id="docket"><header><h2>What Docket is</h2></header><p class="say">What Docket is, what it does, what its pages look like, how it runs the flow, and where to get it are in the <a href="#a-overview">Docket</a> tab. This tab is the flow as a project on Docket runs it, in the words of the guide Docket carries.</p></section>'}]
    first += [{'id': IDS[s['id']], 'title': s['title'], 'html': whole(s, IDS[s['id']])} for s in parts['project']['sections']]
    why = [s for s in parts['why']['sections'] if s['number'] == 0]
    if len(why) != 1:
        stop('Part 2 does not open with exactly one unnumbered section')
    legend = parts['flow'].get('lead') or {}
    if not legend.get('html', '').startswith('<div class="legend">'):
        stop('Part 3 does not open with its legend')
    # This site spaces the block that opens a part with the class "top".
    legend = legend['html'].replace('<div class="legend">', '<div class="top legend">', 1)

    sections = []
    for n, name in enumerate(PARTS, 1):
        for s in parts[name]['sections']:
            if s['number'] == 0:
                continue
            body = inner(s)
            m = re.match(r'\s*<p class="lede">(.*?)</p>(.*)', body, re.S)
            if not m:
                stop(f'section {s["id"]} does not open with its lede')
            sections.append((n, IDS[s['id']], s['title'], m.group(1), m.group(2)))
    unnumbered = [s['id'] for name in PARTS[2:] for s in parts[name]['sections'] if s['number'] == 0]
    if unnumbered:
        stop('unnumbered sections after Part 2, which this tab has no place for: ' + ', '.join(unnumbered))
    sources = parts[SOURCES].get('lead') or {}
    if 'html' not in sources:
        stop('the sources have no table')

    return {
        'name': 'With Docket',
        'title': 'Feature Promotion Flow with Docket',
        'lede': d['text'],
        'intro': re.sub(r'`([^`]+)`', r'<code>\1</code>', d['flow']['text']),
        'parts': [(parts[name]['title'], parts[name]['for']) for name in PARTS],
        'first': first,
        'repo': ('', '', f'From the guide Docket {VERSION} carries. Docket\'s source is not public; its programs are published as a release of this repository: see Get Docket in the Docket tab.'),
        'why': {'id': 'why', 'title': why[0]['title'], 'html': whole(why[0], 'why')},
        'legend': links(legend),
        'sections': sections,
        'sources': links(sources['html']),
        'sources_desc': parts[SOURCES]['for'],
        'footer': f'{d["foot"]} Laid out here from the guide Docket {VERSION} carries; the standards are Lucidex Group\'s own.',
    }
