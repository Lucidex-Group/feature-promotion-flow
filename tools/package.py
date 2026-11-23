"""Write the skills package as a zip, for attaching to a release.

    python3 tools/package.py [the zip to write]

The zip holds the plugin folder and nothing else from the repository. Unpacked, it is a folder named
feature-promotion-flow that Claude Code can load as a plugin, and whose skills folders can be copied by hand.
Without an argument it writes dist/feature-promotion-flow-<version>.zip, with the version from the plugin's manifest.
"""
import json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, '..', 'plugin'))


def files():
    for folder, _, names in sorted(os.walk(PLUGIN)):
        for name in sorted(names):
            if name != '.DS_Store' and '__pycache__' not in folder:
                yield os.path.join(folder, name)


def main():
    version = json.load(open(os.path.join(PLUGIN, '.claude-plugin', 'plugin.json')))['version']
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'dist', f'feature-promotion-flow-{version}.zip')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in files():
            z.write(path, os.path.join('feature-promotion-flow', os.path.relpath(path, PLUGIN)))
    print(os.path.normpath(out))


main()
