"""The project's tests: the site builds and is whole, and the skills package is a plugin that stands alone.

    python3 tools/test.py

Prints a line for each check and exits 1 if any fails.
"""
import os, re, subprocess, sys, tempfile, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PLUGIN = os.path.join(ROOT, 'plugin')
SKILLS = ['feature-promotion-flow', 'fpf-set-up-project', 'fpf-start-feature', 'fpf-build-to-development', 'fpf-release', 'fpf-hotfix']
# What a stand-alone package must not lean on: a folder or a commit only its authors have, another product, or wording about one particular person.
PRIVATE = re.compile(r'~/Development/(?!worktrees/|<Project>)|docket|global instructions|commit [0-9a-f]{7}|\b(he|his|him)\b', re.I)
failures = []


def check(name, problem):
    print(('ok    ' if not problem else 'FAIL  ') + name + (': ' + problem if problem else ''))
    if problem:
        failures.append(name)


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def package_files():
    for folder, _, names in os.walk(PLUGIN):
        for name in names:
            if name.endswith(('.md', '.json')):
                yield os.path.join(folder, name)


def the_site_builds():
    done = run(sys.executable, os.path.join('site', 'source', 'build.py'))
    if done.returncode or done.stdout.strip() != 'ok':
        return 'the build did not print ok: ' + (done.stderr or done.stdout).strip()[-300:]
    page = open(os.path.join(ROOT, 'site', 'index.html')).read()
    ids = re.findall(r' id="([\w-]+)"', page)
    twice = sorted({i for i in ids if ids.count(i) > 1})
    nowhere = sorted(set(re.findall(r' href="#([\w-]+)"', page)) - set(ids))
    if twice:
        return 'places named twice: ' + ', '.join(twice)
    if nowhere:
        return 'links that lead nowhere: ' + ', '.join(nowhere)
    files = sorted(set(re.findall(r' (?:src|href)="(images/[^"]+)"', page)))
    missing = [f for f in files if not os.path.isfile(os.path.join(ROOT, 'site', f))]
    return 'images the page names that are not there: ' + ', '.join(missing) if missing else ''


def switching_tabs_leads_where_it_should():
    """The tab rules in site/source/tabs.js, run with Node against the places in the built page."""
    page = open(os.path.join(ROOT, 'site', 'index.html')).read()
    ids = re.findall(r' id="([\w-]+)"', page)
    # A section of the Skills or Docket tab may share its place name with one in another tab only where it shares its title
    # too, because switching tabs goes to the section of the same place name.
    titles = dict(re.findall(r' id="([\w-]+)"><header>(?:<span class="num">\d+</span>)?<h2>(.*?)</h2>', page))
    tabs = {'': {i for i in ids if not re.match(r'[das]-', i)}, 'd-': {i[2:] for i in ids if i.startswith('d-')},
            's-': {i[2:] for i in ids if i.startswith('s-')}, 'a-': {i[2:] for i in ids if i.startswith('a-')}}
    common = {'overview'} | {i for i in ids if re.fullmatch(r'part-\d+', i)}
    shared = sorted({f'{p}{k}' for p in ('s-', 'a-') for q in tabs if q != p and not (p == 'a-' and q == 's-')
                     for k in (tabs[p] & tabs[q]) - common if titles.get(p + k) != titles.get(q + k)})
    if shared:
        return 'the Skills or Docket tab has sections named as in another tab but titled differently, so switching would land on an unrelated one: ' + ', '.join(shared)
    # Each case: the place the reader is at, its part, and where each of the three tabs should then lead.
    cases = [
        ('', 'overview', 'part-1', ['overview', 's-overview', 'd-overview', 'a-overview']),
        ('road', 'road', 'part-3', ['road', 's-overview', 'd-road', 'a-overview']),
        ('d-why', 'why', 'part-2', ['why', 's-overview', 'd-why', 'a-overview']),
        ('part-2', 'part-2', 'part-2', ['part-2', 's-overview', 'd-part-2', 'a-overview']),
        ('d-adds', 'adds', 'part-1', ['part-1', 's-overview', 'd-adds', 'a-overview']),
        ('a-releases', 'releases', 'part-2', ['overview', 's-overview', 'd-overview', 'a-releases']),
        ('a-part-3', 'part-3', 'part-3', ['overview', 's-overview', 'd-overview', 'a-part-3']),
        ('d-docket', 'docket', 'part-1', ['part-1', 's-overview', 'd-docket', 'a-docket']),
        ('a-docket', 'docket', 'part-1', ['overview', 's-overview', 'd-docket', 'a-docket']),
        ('s-install', 'install', 'part-1', ['overview', 's-install', 'd-overview', 'a-overview']),
        ('s-part-3', 'part-3', 'part-3', ['overview', 's-part-3', 'd-overview', 'a-overview']),
    ]
    script = ("const T = require(process.argv[1]); const ids = new Set(JSON.parse(process.argv[2])); const cases = JSON.parse(process.argv[3]);"
              "const out = cases.map(([id, key, part]) => { const p = T.parts(id); return [p.doc, p.key, ['flow', 'skills', 'docket', 'app'].map(t => T.target(t, p.doc, key, part, x => ids.has(x)))]; });"
              "console.log(JSON.stringify(out));")
    import json
    done = run('node', '-e', script, os.path.join(ROOT, 'site', 'source', 'tabs.js'), json.dumps(ids), json.dumps(cases))
    if done.returncode:
        return 'node could not run the tab rules: ' + (done.stderr or done.stdout).strip()[-300:]
    for (id, key, _, want), (doc, got_key, got) in zip(cases, json.loads(done.stdout)):
        if got_key != key:
            return f'the place "{id or "(none)"}" was read as "{got_key}" in the {doc} guide'
        if got != want:
            return f'from "{id or "(none)"}" the tabs lead to {got}, not {want}'
    return ''


def the_plugin_is_valid():
    for target in ('plugin', '.'):
        done = run('claude', 'plugin', 'validate', target)
        if done.returncode:
            return f'claude plugin validate {target} failed: ' + (done.stdout + done.stderr).strip()[-300:]
    return ''


def every_skill_loads():
    found = sorted(os.listdir(os.path.join(PLUGIN, 'skills')))
    if found != sorted(SKILLS):
        return f'the skills are {found}'
    for skill in SKILLS:
        text = open(os.path.join(PLUGIN, 'skills', skill, 'SKILL.md')).read()
        front = re.match(r'---\nname: ([\w-]+)\ndescription: "(.+)"\n---\n', text)
        if not front or front.group(1) != skill:
            return f'{skill}: the front matter does not name it'
        if 'Use ' not in front.group(2) and 'Load ' not in front.group(2):
            return f'{skill}: the description does not say when to use it'
    return ''


def the_package_stands_alone():
    for path in package_files():
        text = open(path).read()
        hit = re.search(r'global instructions|commit [0-9a-f]{7}', text, re.I) if path.endswith('README.md') else PRIVATE.search(text)
        if hit:
            return f'{os.path.relpath(path, ROOT)} refers to "{hit.group(0)}"'
        for link in re.findall(r'\]\(([^)#]+)\)', text):
            if not link.startswith('http') and not os.path.exists(os.path.join(os.path.dirname(path), link)):
                return f'{os.path.relpath(path, ROOT)} points to {link}, which is not in the package'
    return ''


def a_zip_can_be_made():
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'package.zip')
        done = run(sys.executable, os.path.join('tools', 'package.py'), out)
        if done.returncode:
            return done.stderr.strip()[-300:]
        names = zipfile.ZipFile(out).namelist()
        if any(not n.startswith('feature-promotion-flow/') for n in names):
            return 'the zip holds something outside the package'
        need = ['feature-promotion-flow/.claude-plugin/plugin.json'] + [f'feature-promotion-flow/skills/{s}/SKILL.md' for s in SKILLS]
        missing = [n for n in need if n not in names]
        if missing:
            return 'the zip lacks ' + ', '.join(missing)
        zipfile.ZipFile(out).extractall(tmp)
        done = run('claude', 'plugin', 'validate', os.path.join(tmp, 'feature-promotion-flow'))
        return 'the unpacked zip is not a valid plugin' if done.returncode else ''


check('The site builds, with no place named twice, no link that leads nowhere and no image missing', the_site_builds())
check('Switching tabs leads to the same place, the same part, or the overview, as the guide says', switching_tabs_leads_where_it_should())
check('The package is a valid plugin, and the repository a valid marketplace', the_plugin_is_valid())
check('Every skill loads: a name matching its folder and a description that says when to use it', every_skill_loads())
check('The package stands alone: no private reference, and every file it points to is inside it', the_package_stands_alone())
check('A zip can be made that unpacks to the plugin and nothing else', a_zip_can_be_made())
sys.exit(1 if failures else 0)
