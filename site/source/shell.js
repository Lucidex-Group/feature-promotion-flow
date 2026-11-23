// The four tabs and the contents: one guide is shown at a time, one part of it to a page.
// How places are named in each guide, and where each tab leads, is in tabs.js.
(function () {
  var all = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };
  var docs = all('.gdoc'), trees = all('.gtree'), tabs = all('.tabs a');
  var rail = document.getElementById('rail'), fold = rail.querySelector('.fold');
  // On a narrow screen the contents fold away under a button; on a wide one they are always shown.
  function unfold(open) { rail.classList.toggle('open', open); fold.setAttribute('aria-expanded', String(open)); }
  fold.addEventListener('click', function () { unfold(!rail.classList.contains('open')); });

  var name = FPF_TABS.name, parts = FPF_TABS.parts;
  function has(id) { return !!document.getElementById(id); }

  function show(id, scroll) {
    var el = id && document.getElementById(id);
    if (!el || !el.closest('.view')) { id = name(parts(id).doc, 'overview'); el = document.getElementById(id); }
    var view = el.closest('.view'), doc = view.closest('.gdoc').getAttribute('data-doc');
    var key = parts(id).key, part = view.getAttribute('data-view');
    docs.forEach(function (d) { d.hidden = d.getAttribute('data-doc') !== doc; });
    all('.view', view.closest('.gdoc')).forEach(function (v) { v.hidden = v !== view; });
    trees.forEach(function (t) {
      var mine = t.getAttribute('data-doc') === doc;
      t.hidden = !mine;
      if (!mine) return;
      all('[data-part]', t).forEach(function (d) {
        var cur = d.getAttribute('data-part') === part;
        d.classList.toggle('cur', cur);
        if (d.tagName === 'DETAILS') d.open = cur;
      });
      t.querySelector('a.ov').classList.toggle('cur', key === 'overview');
      all('ol a', t).forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-go') === id); });
    });
    // Where each tab leads from here: see tabs.js.
    tabs.forEach(function (t) {
      var d = t.getAttribute('data-doc'), on = d === doc;
      var to = FPF_TABS.target(d, doc, key, part, has);
      t.classList.toggle('on', on);
      t.setAttribute('aria-current', on ? 'page' : 'false');
      t.setAttribute('href', '#' + to);
      t.setAttribute('data-go', to);
    });
    if (scroll !== false) { if (el === view || key === 'overview') window.scrollTo(0, 0); else el.scrollIntoView(); }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-go]');
    if (!a) return;
    e.preventDefault();
    var id = a.getAttribute('data-go');
    try { history.replaceState(null, '', '#' + id); } catch (x) { location.hash = id; }
    if (a.closest('.gtree')) unfold(false);
    show(id);
  });
  window.addEventListener('hashchange', function () { show(location.hash.slice(1)); });
  show(location.hash.slice(1), !!location.hash);
})();
