// Step through a figure: marks drawn at a later step are faint, the current step is lit.
document.querySelectorAll('figure[data-steps]').forEach(function (fig) {
  var texts = JSON.parse(fig.dataset.steps);
  var els = Array.prototype.slice.call(fig.querySelectorAll('svg [data-s]'));
  var back = fig.querySelector('.back'), next = fig.querySelector('.next'), all = fig.querySelector('.all');
  var say = fig.querySelector('.say'), cnt = fig.querySelector('.cnt');
  var k = 0;
  function show() {
    fig.classList.toggle('stepping', k > 0);
    els.forEach(function (e) {
      var s = +e.dataset.s;
      e.classList.toggle('future', k > 0 && s > k);
      e.classList.toggle('now', k > 0 && s === k);
    });
    say.textContent = k ? texts[k - 1] : '';
    cnt.textContent = k ? 'Step ' + k + ' of ' + texts.length : '';
    back.hidden = all.hidden = k === 0;
    back.disabled = k <= 1;
    next.textContent = k === 0 ? 'Step through' : k === texts.length ? 'Start again' : 'Next';
  }
  next.addEventListener('click', function () { k = k >= texts.length ? 1 : k + 1; show(); });
  back.addEventListener('click', function () { k = Math.max(1, k - 1); show(); });
  all.addEventListener('click', function () { k = 0; show(); });
  fig.querySelector('.stepper').addEventListener('keydown', function (e) {
    if (!k) return;
    if (e.key === 'ArrowRight') { k = Math.min(texts.length, k + 1); show(); }
    if (e.key === 'ArrowLeft') { k = Math.max(1, k - 1); show(); }
  });
});

// Follow a branch: point at its name (or tap to pin) and everything else in the figure dims.
(function () {
  var pinned = null;
  function ids(e) { return (e.dataset.b || '').split('|'); }
  function follow(fig, id) {
    fig.classList.add('following');
    fig.querySelectorAll('svg [data-b]').forEach(function (e) { e.classList.toggle('on', ids(e).indexOf(id) > -1); });
  }
  function clear(fig) {
    fig.classList.remove('following');
    fig.querySelectorAll('svg .on').forEach(function (e) { e.classList.remove('on'); });
  }
  function figOf(e) { return e.closest('figure'); }
  // A branch is followed from its name, its line, or any mark that sits on it; a link follows the branch it leaves.
  document.addEventListener('pointerover', function (ev) {
    var p = ev.target.closest && ev.target.closest('svg [data-b]');
    if (p && !pinned) follow(figOf(p), p.dataset.f);
  });
  document.addEventListener('pointerout', function (ev) {
    var p = ev.target.closest && ev.target.closest('svg [data-b]');
    if (p && !pinned && !p.contains(ev.relatedTarget)) clear(figOf(p));
  });
  function toggle(p) {
    var fig = figOf(p), id = ids(p)[0];
    if (pinned && pinned.fig === fig && pinned.id === id) { pinned = null; clear(fig); return; }
    if (pinned) clear(pinned.fig);
    pinned = { fig: fig, id: id };
    follow(fig, id);
  }
  document.addEventListener('click', function (ev) {
    var p = ev.target.closest && ev.target.closest('.pick');
    if (p) { toggle(p); return; }
    if (pinned && !(ev.target.closest && ev.target.closest('.stepper'))) { clear(pinned.fig); pinned = null; }
  });
  document.addEventListener('keydown', function (ev) {
    var p = ev.target.closest && ev.target.closest('.pick');
    if (p && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); toggle(p); }
    if (ev.key === 'Escape' && pinned) { clear(pinned.fig); pinned = null; }
  });
  document.addEventListener('focusin', function (ev) {
    var p = ev.target.closest && ev.target.closest('.pick');
    if (p && !pinned) follow(figOf(p), ids(p)[0]);
  });
  document.addEventListener('focusout', function (ev) {
    var p = ev.target.closest && ev.target.closest('.pick');
    if (p && !pinned) clear(figOf(p));
  });
})();

// What a mark is: one tooltip for the page, with the command where there is one.
(function () {
  var tip = document.createElement('div');
  tip.id = 'tip'; tip.setAttribute('role', 'tooltip'); tip.hidden = true;
  var what = document.createElement('p'), cmd = document.createElement('pre');
  tip.appendChild(what); tip.appendChild(cmd);
  document.body.appendChild(tip);
  var cur = null;
  // Keep clear of the drawing: sit just beyond the whole mark, on the side nearer the figure's edge.
  function place(x, y) {
    var w = tip.offsetWidth, h = tip.offsetHeight, gap = 14;
    var svg = cur && cur.closest('svg');
    var box = svg ? svg.getBoundingClientRect() : { top: 0, height: window.innerHeight };
    var r = cur ? cur.getBoundingClientRect() : { top: y, bottom: y, height: 0 };
    var above = r.top + r.height / 2 < box.top + box.height / 2;
    var t = above ? r.top - h - gap : r.bottom + gap;
    if (t < 8) t = r.bottom + gap;
    if (t + h > window.innerHeight - 8) t = r.top - h - gap;
    if (t < 8) t = 8;
    var l = Math.min(Math.max(8, x - w / 2), window.innerWidth - w - 8);
    tip.style.left = l + 'px'; tip.style.top = t + 'px';
  }
  function show(e, x, y) {
    cur = e;
    what.textContent = e.dataset.tip;
    cmd.textContent = e.dataset.cmd || ''; cmd.hidden = !e.dataset.cmd;
    tip.hidden = false; place(x, y);
  }
  function hide() { cur = null; tip.hidden = true; }
  document.addEventListener('pointerover', function (ev) {
    var e = ev.target.closest && ev.target.closest('[data-tip]');
    if (e) show(e, ev.clientX, ev.clientY); else if (cur) hide();
  });
  document.addEventListener('pointermove', function (ev) { if (cur) place(ev.clientX, ev.clientY); });
  document.addEventListener('pointerleave', hide);
  document.addEventListener('scroll', hide, true);
  document.addEventListener('focusin', function (ev) {
    var e = ev.target.closest && ev.target.closest('[data-tip]');
    if (e) { var r = e.getBoundingClientRect(); show(e, r.left + r.width / 2, r.bottom); }
  });
  document.addEventListener('focusout', hide);
})();
