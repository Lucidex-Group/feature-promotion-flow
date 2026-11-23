"""Build the Feature Promotion Flow site: one page, two guides, a tab for each.

    python3 build.py                 writes ../index.html, a whole page
    python3 build.py --body <file>   also writes the page without its document tags, for a host that supplies its own

The first tab is the flow on its own (flow.py). The second is the flow in a project on Docket (docket.py).
Both are laid out the same way: the contents on the left, and a page for each part. The home page is the overview
with the first part below it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import docket, flow  # noqa: E402
from drawing import esc  # noqa: E402

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">')
# The Lucidex Group mark: an orange triangle, a second triangle and a dot, the last two in the colour of the text around them.
MARK = ('<svg class="mark" viewBox="0 0 56 40" aria-hidden="true"><path d="M0 2 L0 36 L34 36 Z" fill="#F25C1F"/>'
        '<path d="M30 16 L52 16 L52 38 Z" fill="currentColor"/><circle cx="50.3" cy="4.3" r="4.3" fill="currentColor"/></svg>')


def read(name):
    return open(os.path.join(HERE, name)).read()


def place(html, prefix):
    """Name every place in one guide's pages with that guide's prefix, and make every link inside it lead there."""
    html = re.sub(r' data-go="[^"]*"', '', html)
    html = re.sub(r' id="([\w-]+)"', lambda m: f' id="{prefix}{m.group(1)}"', html)
    return re.sub(r' href="#([\w-]+)"', lambda m: f' href="#{prefix}{m.group(1)}" data-go="{prefix}{m.group(1)}"', html)


def guide(key, prefix, d):
    """One guide: its contents tree for the left, and its pages."""
    numbered = sorted(d['sections'], key=lambda s: s[0])
    numbered = [(n, p, slug, title, lede, body) for n, (p, slug, title, lede, body) in enumerate(numbered, 1)]
    views = [(f'part-{i}', t, f'Part {i}') for i, (t, _) in enumerate(d['parts'], 1)] + [('sources', 'Sources', 'Reference')]
    whole = next(s for s in numbered if s[2] == 'loop')

    def link(view, cls=''):
        v, title, label = view
        return f'<a{cls} href="#{v}">{"<span>" + label + "</span>" if label else ""}{esc(title)}</a>'

    def prevnext(i):
        back = f'<a href="#{views[i - 1][0]}"><span>Previous</span>{esc(views[i - 1][1])}</a>' if i else ''
        on = f'<a class="nx" href="#{views[i + 1][0]}"><span>Next</span>{esc(views[i + 1][1])}</a>' if i + 1 < len(views) else ''
        return f'<nav class="prevnext" aria-label="Previous and next part">{back}{on}</nav>'

    tree = ['<a class="ov" href="#overview">Overview</a>']
    cards = ''.join(f'<li><a href="#{v}"><span>{label}</span><b>{esc(title)}</b></a></li>' for v, title, label in views)
    # The home page: the overview, with the whole cycle drawn as a loop, and the first part below it.
    home = (f'<div class="home" id="overview"><header class="page-head"><h1>{esc(d["title"])}</h1>'
            f'<p class="muted">{esc(d["lede"])}</p>'
            + (f'<p class="repoline"><span>Repository</span><a href="{d["repo"][0]}" target="_blank" rel="noopener">{esc(d["repo"][1])}</a>{esc(d["repo"][2])}</p>'
               if d["repo"][0] else f'<p class="repoline"><span>Repository</span>{esc(d["repo"][2])}</p>') +
            f'</header><p class="intro">{d["intro"]}</p>'
            f'<section><header><h2>{esc(whole[3])}</h2></header><p class="lede">One release, drawn as rings. Time runs clockwise from the top, and one turn is one release.</p>{whole[5]}</section>'
            f'<ol class="partcards">{cards}</ol></div>')
    pages = []
    for i, (title, desc) in enumerate(d['parts'], 1):
        head = f'<header class="part"{" id=" + chr(34) + "part-1" + chr(34) if i == 1 else ""}><span>Part {i}</span><h2>{esc(title)}</h2><p>{esc(desc)}</p></header>'
        lead, items = '', []
        if i == 1:
            lead = ''.join(s['html'] for s in d['first'])
            items = [(s['id'], s['title']) for s in d['first']]
        elif i == 2:
            lead = d['why']['html']
            items = [(d['why']['id'], d['why']['title'])]
        elif i == 3:
            lead = d['legend']
        mine = [s for s in numbered if s[1] == i]
        body = ''.join(f'<section id="{slug}"><header><span class="num">{n}</span><h2>{esc(t)}</h2></header><p class="lede">{lede}</p>{b}</section>'
                       for n, _, slug, t, lede, b in mine)
        items += [(slug, t) for _, _, slug, t, _, _ in mine]
        if i == 1:
            pages.append(f'<div class="view" data-view="part-1">{home}{head}{lead}{body}{prevnext(0)}</div>')
        else:
            pages.append(f'<div class="view" id="part-{i}" data-view="part-{i}" hidden>{head}{lead}{body}{prevnext(i - 1)}</div>')
        subs = ''.join(f'<li><a href="#{s}">{esc(t)}</a></li>' for s, t in items)
        tree.append(f'<details data-part="part-{i}"{" open" if i == 1 else ""}><summary>{link(views[i - 1])}</summary><ol>{subs}</ol></details>')
    pages.append('<div class="view" id="sources" data-view="sources" hidden><section><header class="part"><span>Reference</span><h2>Sources</h2>'
                 f'<p>{esc(d["sources_desc"])}</p></header>{d["sources"]}</section>{prevnext(len(views) - 1)}<footer>{esc(d["footer"])}</footer></div>')
    tree.append(f'<div class="leaf" data-part="sources">{link(views[-1])}</div>')
    hidden = '' if key == 'flow' else ' hidden'
    return (place(f'<div class="gtree" data-doc="{key}"{hidden}>{"".join(tree)}</div>', prefix),
            place(f'<div class="gdoc" data-doc="{key}"{hidden}>{"".join(pages)}</div>', prefix))


def body():
    guides = [('flow', '', flow.doc()), ('docket', 'd-', docket.doc())]
    built = [guide(k, p, d) for k, p, d in guides]
    tabs = ''.join(f'<a href="#{p}overview" data-go="{p}overview" data-doc="{k}"{" class=" + chr(34) + "on" + chr(34) if k == "flow" else ""}>{esc(d["title"])}</a>'
                   for k, p, d in guides)
    return (f'<header class="masthead"><p class="brand">{MARK}<b>Lucidex</b><span>Group</span></p>'
            '<p class="name">Feature Promotion Flow</p>'
            '<p class="tagline">A way of branching and releasing with Git, in which features are tested together and a release is chosen feature by feature.</p></header>'
            f'<div class="bar"><nav class="tabs" aria-label="Which guide">{tabs}</nav></div>'
            '<div class="shell"><nav class="rail" id="rail" aria-label="Contents"><button type="button" class="fold" aria-expanded="false" aria-controls="trees">Contents</button>'
            '<div id="trees">' + ''.join(t for t, _ in built) + '</div><div class="copyright">' + MARK + '© 2026 Lucidex Group</div></nav>'
            '<div class="content"><main>' + ''.join(g for _, g in built) + '</main></div></div>')


def main():
    css = read('figures.css') + read('shell.css')
    js = read('figures.js') + read('shell.js')
    top = f'<title>Feature Promotion Flow</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<style>{css}</style>\n'
    page = body()
    open(os.path.join(HERE, '..', 'index.html'), 'w').write(
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        f'{top}</head><body>\n{page}\n<script>{js}</script></body></html>\n')
    if '--body' in sys.argv:
        open(sys.argv[sys.argv.index('--body') + 1], 'w').write(f'{top}{page}\n<script>{js}</script>\n')
    print('ok')


main()
