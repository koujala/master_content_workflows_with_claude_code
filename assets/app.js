(function () {
  var posts = window.POSTS || [];
  var activeTags = {};
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c];
    });
  }
  function uniq(arr) { return arr.filter(function (v, i) { return v && arr.indexOf(v) === i; }).sort(); }

  function fillSelect(el, values) {
    values.forEach(function (v) { var o = document.createElement('option'); o.value = v; o.textContent = v; el.appendChild(o); });
  }
  fillSelect($('cat'), uniq(posts.map(function (p) { return p.category; })));
  fillSelect($('status'), uniq(posts.map(function (p) { return p.status; })));

  var allTags = uniq([].concat.apply([], posts.map(function (p) { return p.tags || []; })));

  function renderTags() {
    $('tags').innerHTML = allTags.map(function (t) {
      return '<button class="chip' + (activeTags[t] ? ' on' : '') + '" data-tag="' + esc(t) + '">#' + esc(t) + '</button>';
    }).join('');
  }

  function matches(p) {
    var q = $('q').value.trim().toLowerCase();
    if ($('cat').value && p.category !== $('cat').value) return false;
    if ($('status').value && p.status !== $('status').value) return false;
    for (var t in activeTags) if (activeTags[t] && (p.tags || []).indexOf(t) < 0) return false;
    if (!q) return true;
    var hay = [p.title, p.subtitle, p.summary, p.category, p.name, (p.tags || []).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(q) >= 0;
  }

  function card(p) {
    var base = 'posts/' + encodeURIComponent(p.name) + '/' + encodeURIComponent(p.name);
    var links = [];
    if (p.files.short) links.push('<a href="' + base + '.md">Short (' + p.shortChars + ')</a>');
    if (p.files.long) links.push('<a href="' + base + '_long.md">Long (' + p.longChars + ')</a>');
    if (p.files.prompt) links.push('<a href="' + base + '_prompt.md">Prompt</a>');
    var tags = (p.tags || []).map(function (t) { return '<button class="chip" data-tag="' + esc(t) + '">#' + esc(t) + '</button>'; }).join('');
    var statusCls = p.status === 'published' ? 'ok' : (p.status === 'draft' ? 'warn' : '');
    return '<article class="card">' +
      (p.files.image ? '<img loading="lazy" alt="" src="' + base + '.png">' : '') +
      '<div class="body">' +
        '<div class="meta"><span class="cat">' + esc(p.category) + '</span><span>' + esc(p.created) + '</span></div>' +
        '<h2>' + esc(p.emoji) + ' ' + esc(p.title) + '</h2>' +
        '<p class="subtitle">' + esc(p.subtitle) + '</p>' +
        '<p class="summary">' + esc(p.summary) + '</p>' +
        '<div class="row"><span class="badge ' + statusCls + '">' + esc(p.status) + '</span>' + tags + '</div>' +
        '<div class="links">' + links.join('') + '</div>' +
      '</div></article>';
  }

  function render() {
    var list = posts.filter(matches);
    var s = $('sort').value;
    list.sort(function (a, b) {
      if (s === 'az') return a.title.localeCompare(b.title);
      var d = String(a.created).localeCompare(String(b.created));
      return s === 'old' ? d : -d;
    });
    $('grid').innerHTML = list.length ? list.map(card).join('') : '<div class="empty">No posts match.</div>';
    $('count').textContent = list.length + ' of ' + posts.length + ' posts';
    renderTags();
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-tag]');
    if (!b) return;
    var t = b.getAttribute('data-tag');
    activeTags[t] = !activeTags[t];
    render();
  });
  ['q', 'cat', 'status', 'sort'].forEach(function (id) { $(id).addEventListener('input', render); });
  render();
})();
