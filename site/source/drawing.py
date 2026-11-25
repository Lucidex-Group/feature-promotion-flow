"""Lane diagrams drawn on one grid: the marks, the links between lanes, and the figure that holds them.

Taken from the script that draws the guide kept with Docket,
with the words for each mark moved out, so that each version of the guide supplies its own through use().
"""
import html, json, math

X0 = 172  # where lanes begin


def esc(t):
    return html.escape(t, quote=True)


# The words for the marks. Each version of the guide sets these with use() before it draws.
NAMES, BR_TIP, NAME_TIP, link_tip, dot_tip = {}, {}, {}, None, None


def use(names, br_tip, name_tip, link, dot):
    """Set the branch names and the words shown for each mark, for the figures drawn next."""
    global NAMES, BR_TIP, NAME_TIP, link_tip, dot_tip
    NAMES, BR_TIP, NAME_TIP, link_tip, dot_tip = names, br_tip, name_tip, link, dot


class Fig:
    def __init__(self, w, h, aria):
        self.w, self.h, self.aria = w, h, aria
        self.bg, self.lanes, self.links, self.dots, self.txt = [], [], [], [], []
        self.s, self.steps = 0, []
        self.split, self.at, self.arrive, self.ops = False, {}, {}, []

    def step(self, text):
        self.steps.append(text)
        self.s = len(self.steps)

    def key(self, x, y):
        return (1 if self.split and x >= 556 else 0, y)

    def g(self, m, b=None, tip=None, cmd=None, pick=False, s=None, f=None):
        a = f' data-s="{self.s if s is None else s}"'
        tip = tip[0].upper() + tip[1:] if tip else tip
        if b:
            a += f' data-b="{esc("|".join(b))}" data-f="{esc(f or b[0])}"'
        if tip:
            a += f' data-tip="{esc(tip)}"'
        if cmd:
            a += f' data-cmd="{esc(cmd)}"'
        if pick:
            a += f' class="pick" tabindex="0" role="button" aria-label="Follow {esc(b[0])}"'
        return f'<g{a}>{m}</g>'

    def band(self, x1, x2, title, alt=False):
        self.bg.append(self.g(f'<rect class="band{" alt" if alt else ""}" x="{x1}" y="0" width="{x2 - x1}" height="{self.h}"/>'))
        self.txt.append(self.g(f'<text class="bt" x="{x1 + 14}" y="24">{esc(title)}</text>'))

    def lane(self, cls, y, segs=None, name=None, lx=12, pill=True):
        segs = segs or [(X0, self.w - 24)]
        name = name or NAMES[cls]
        self.at[self.key(segs[0][0], y)] = (cls, name)
        for a, b in segs:
            self.lanes.append(self.g(f'<path class="ln c-{cls}" d="M{a} {y}H{b}"/><path class="hitline" d="M{a} {y}H{b}"/>', [name]))
        if not pill:
            return
        self.txt.append(self.g(
            f'<g class="pill c-{cls}"><rect x="{lx}" y="{y - 13}" width="142" height="26" rx="13"/>'
            f'<text x="{lx + 71}" y="{y + 4}" text-anchor="middle">{esc(name)}</text></g>',
            [name], NAME_TIP.get(name, BR_TIP[cls]), None, True))

    def where(self, k):
        return self.rings[k[1]] if k[0] == 'r' else self.at[k]

    def _link(self, cls, d, fr, to, end, dash, tip, cmd, halo=None):
        self.ops.append(('link', self.s, cls, d, fr, to, end, dash, tip, cmd, halo or d))

    def link(self, cls, x1, y1, x2, y2, dash=False, tip=None, cmd=None):
        xm = (x1 + x2) / 2
        d = f'M{x1} {y1}C{xm} {y1} {xm} {y2} {x2} {y2}'
        self._link(cls, d, self.key(x1, y1), self.key(x2, y2), (x2, y2), dash, tip, cmd)

    def dot(self, cls, x, y, kind='c', tip=None, own=None):
        self.ops.append(('dot', self.s, cls, x, y, kind, tip, own or self.key(x, y)))

    def build(self):
        for op in self.ops:
            if op[0] != 'link':
                continue
            _, s, cls, d, fr, to, end, dash, tip, cmd, halo = op
            fr, to = self.where(fr), self.where(to)
            auto = link_tip(fr[0], fr[1], to[0], to[1], dash)
            if tip is None:
                tip, cmd = auto
            self.arrive[end] = (tip, cmd, [fr[1], to[1]])
            self.links.append(self.g(
                f'<path class="halo" d="{halo}"/><path class="lk c-{cls}{" dash" if dash else ""}" d="{d}"/><path class="hitline" d="{d}"/>',
                [fr[1], to[1]], tip, cmd, s=s))
        for op in self.ops:
            if op[0] != 'dot':
                continue
            _, s, cls, x, y, kind, tip, k = op
            if kind == 'c':
                m = f'<circle class="dc c-{cls}" cx="{x}" cy="{y}" r="5"/>'
            elif kind == 'm':
                m = f'<circle class="dm c-{cls}" cx="{x}" cy="{y}" r="7"/>'
            elif kind == 'q':
                m = (f'<g class="c-{cls}"><circle class="dq" cx="{x}" cy="{y}" r="10"/>'
                     f'<path class="tick" d="M{x - 4.5} {y + .5}l3 3.2 6-7"/></g>')
            else:
                m = (f'<g class="c-hot"><circle class="dq" cx="{x}" cy="{y}" r="10"/>'
                     f'<path class="tick" d="M{x - 4} {y - 4}l8 8M{x + 4} {y - 4}l-8 8"/></g>')
            try:
                lc, bid = self.where(k)
            except KeyError:
                lc, bid = cls, NAMES.get(cls, cls)
            if (x, y) in self.arrive and kind in ('c', 'm'):
                t, c, bs = self.arrive[(x, y)]
            else:
                t, c = dot_tip(lc, bid, kind)
                bs = [bid]
            self.dots.append(self.g(m, bs, tip or t, None if tip else c, s=s, f=bid))
        self.ops = []

    def tag(self, x, y, text, up=False):
        w = 14 + 6.6 * len(text)
        ty = y - 40 if up else y + 16
        self.txt.append(self.g(
            f'<g class="tag"><rect x="{x - w / 2:.1f}" y="{ty:.1f}" width="{w:.1f}" height="22" rx="4"/>'
            f'<text x="{x:.1f}" y="{ty + 15:.1f}" text-anchor="middle">{esc(text)}</text></g>',
            ['main'], 'A release carries two tags on the same commit of main: a descriptive name for people, such as v0.6.0-pr142-2026-11-21, and the bare version, v0.6.0, for tools.',
            'git fetch origin\ngit tag -a v<version>-pr<number>-<date> -m "<what the release contains>" origin/main\ngit tag -a v<version> -m "<what the release contains>" origin/main\ngit push origin v<version>-pr<number>-<date> v<version>'))

    def label(self, x, y, text, anchor='middle', strong=False):
        lines = text.split('\n')
        spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else 15}">{esc(t)}</tspan>' for i, t in enumerate(lines))
        self.txt.append(self.g(f'<text class="lb{" strong" if strong else ""}" x="{x}" y="{y}" text-anchor="{anchor}">{spans}</text>'))

    def chip(self, x, y, text, cls):
        w = 16 + 7 * len(text)
        self.txt.append(self.g(
            f'<g class="chip c-{cls}"><rect x="{x}" y="{y - 11}" width="{w}" height="22" rx="5"/>'
            f'<text x="{x + w / 2}" y="{y + 4}" text-anchor="middle">{esc(text)}</text></g>'))
        return w

    def svg(self):
        self.build()
        body = ''.join(self.bg + self.lanes + self.links + self.dots + self.txt)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.aria)}" '
                f'style="min-width:{int(self.w * .82)}px">{body}</svg>')


class Loop(Fig):
    """The same marks on rings: time runs clockwise from the top, one turn to a release."""
    def __init__(self, w, h, cx, cy, aria):
        super().__init__(w, h, aria)
        self.cx, self.cy, self.rings = cx, cy, {}

    def pt(self, t, r):
        a = 2 * math.pi * t - math.pi / 2
        return round(self.cx + r * math.cos(a), 1), round(self.cy + r * math.sin(a), 1)

    def ring(self, cls, r, segs=None, name=None):
        name = name or self.rings.get(r, (cls, NAMES.get(cls, cls)))[1]
        self.rings[r] = (cls, name)
        if not segs:
            self.lanes.append(self.g(f'<circle class="ln c-{cls}" cx="{self.cx}" cy="{self.cy}" r="{r}"/><circle class="hitline" cx="{self.cx}" cy="{self.cy}" r="{r}"/>', [name]))
            return
        for a, b in segs:
            (x1, y1), (x2, y2) = self.pt(a, r), self.pt(b, r)
            big = 1 if (b - a) > .5 else 0
            d = f'M{x1} {y1}A{r} {r} 0 {big} 1 {x2} {y2}'
            self.lanes.append(self.g(f'<path class="ln c-{cls}" d="{d}"/><path class="hitline" d="{d}"/>', [name]))

    def rlink(self, cls, t1, r1, t2, r2, dash=False):
        pts = []
        for i in range(33):
            u = i / 32
            e = u * u * (3 - 2 * u)
            pts.append(self.pt(t1 + (t2 - t1) * u, r1 + (r2 - r1) * e))
        d = 'M' + 'L'.join(f'{x} {y}' for x, y in pts)
        halo = 'M' + 'L'.join(f'{x} {y}' for x, y in pts[6:28])
        self._link(cls, d, ('r', r1), ('r', r2), self.pt(t2, r2), dash, None, None, halo)

    def num(self, t, r, n):
        x, y = self.pt(t, r)
        self.txt.append(self.g(f'<g class="nb"><circle cx="{x}" cy="{y}" r="9.5"/><text x="{x}" y="{y + 3.8}" text-anchor="middle">{n}</text></g>'))

    def rdot(self, cls, t, r, kind='c', tip=None):
        x, y = self.pt(t, r)
        self.dot(cls, x, y, kind, tip=tip, own=('r', r))

    def out(self, t, text, r=342):
        (x1, y1), (x2, y2), (x, y) = self.pt(t, r - 10), self.pt(t, r + 2), self.pt(t, r + 12)
        c = math.cos(2 * math.pi * t - math.pi / 2)
        anchor = 'start' if c > .25 else 'end' if c < -.25 else 'middle'
        n = text.count('\n')
        yy = y + 4 - (7 * n if anchor != 'middle' else (15 * n if y < self.cy else -10))
        self.txt.append(self.g(f'<path class="leader" d="M{x1} {y1}L{x2} {y2}"/>'))
        self.label(x, round(yy, 1), text, anchor)



class Half:
    """One side of a wrong-and-right pair: the same drawing calls, moved across."""
    def __init__(self, f, o):
        self.f, self.o = f, o

    def lane(self, cls, y, segs=None, name=None):
        segs = segs or [(X0, 516)]
        self.f.lane(cls, y, [(a + self.o, b + self.o) for a, b in segs], name, lx=self.o + 12)

    def link(self, cls, x1, y1, x2, y2, dash=False, tip=None, cmd=None):
        self.f.link(cls, x1 + self.o, y1, x2 + self.o, y2, dash, tip, cmd)

    def dot(self, cls, x, y, kind='c', tip=None):
        self.f.dot(cls, x + self.o, y, kind, tip)

    def label(self, x, y, text, anchor='middle', strong=False):
        self.f.label(x + self.o, y, text, anchor, strong)

    def tag(self, x, y, text):
        self.f.tag(x + self.o, y, text)

    def chips(self, x, y, label, items):
        self.f.label(x + self.o - 8, y + 4, label, 'end')
        cx = x + self.o
        for t, c in items:
            cx += self.f.chip(cx, y, t, c) + 6


def pair(h, dont, do, aria):
    f = Fig(1100, h, aria)
    f.split = True
    f.bg.append(f'<rect class="band bad" x="0" y="0" width="550" height="{h}"/>')
    f.bg.append(f'<path class="split" d="M550 0V{h}"/>')
    f.txt.append(f'<text class="bt bad" x="16" y="26">Don\'t · {esc(dont)}</text>')
    f.txt.append(f'<text class="bt good" x="578" y="26">Do · {esc(do)}</text>')
    return f, Half(f, 0), Half(f, 562)


def fig(f, caption):
    svg = f if isinstance(f, str) else f.svg()
    steps = [] if isinstance(f, str) else f.steps
    if not steps:
        return f'<figure><div class="scroll">{svg}</div><figcaption>{caption}</figcaption></figure>'
    bar = ('<div class="stepper"><div class="btns"><button type="button" class="back" hidden>Back</button>'
           '<button type="button" class="next primary">Step through</button>'
           '<button type="button" class="all" hidden>Show all</button><span class="cnt"></span></div>'
           '<p class="say" aria-live="polite"></p></div>')
    return (f'<figure data-steps="{esc(json.dumps(steps))}"><div class="scroll">{svg}</div>{bar}'
            f'<figcaption>{caption}</figcaption></figure>')


def section(n, title, lede, body):
    return (f'<section id="s{n}"><header><span class="num">{n}</span><h2>{esc(title)}</h2></header>'
            f'<p class="lede">{lede}</p>{body}</section>')

