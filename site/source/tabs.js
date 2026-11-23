// Which guide a place belongs to, and where each tab leads from it. Kept apart from shell.js, with nothing that needs a page,
// so that tools/test.py can check it with Node.
// A place in the flow on its own has a plain name. The same place in the guide with Docket has "d-" in front, and a place in
// the third tab, Docket itself, has "a-" in front.
var FPF_TABS = (function () {
  var PREFIX = { flow: '', docket: 'd-', app: 'a-' };
  function name(doc, key) { return PREFIX[doc] + key; }
  function parts(id) {
    id = id || 'overview';
    if (/^d-/.test(id)) return { doc: 'docket', key: id.slice(2) };
    if (/^a-/.test(id)) return { doc: 'app', key: id.slice(2) };
    return { doc: 'flow', key: id };
  }
  // Where the tab for guide `tab` leads, from place `key` in part `part` of guide `doc`; `has(id)` says whether a place exists.
  // Each tab leads to the same place in its own guide. Where that guide has no such section, the first two tabs lead to the
  // same part, since their parts match; the third tab's parts are its own, so to or from it the tab leads to the overview.
  function target(tab, doc, key, part, has) {
    var same = tab === doc || (tab !== 'app' && doc !== 'app');
    var section = key !== 'overview' && !/^part-\d+$/.test(key);
    return has(name(tab, key)) && (same || section) ? name(tab, key) : name(tab, same ? part : 'overview');
  }
  return { name: name, parts: parts, target: target };
})();
if (typeof module !== 'undefined') module.exports = FPF_TABS;
