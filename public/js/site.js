/* Clínica Belba · interacciones mínimas de la web estática (sin jQuery ni WordPress) */
(function () {
  var d = document;
  // Menú móvil
  d.querySelectorAll('.k-menu-toggle').forEach(function (t) {
    t.setAttribute('role', 'button'); t.setAttribute('tabindex', '0');
    function tog() { var on = t.classList.toggle('k-active'); t.setAttribute('aria-expanded', on ? 'true' : 'false'); }
    t.addEventListener('click', tog);
    t.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tog(); } });
  });
  // Submenús en el menú desplegable (móvil)
  d.querySelectorAll('.k-nav-menu--dropdown .menu-item-has-children > a').forEach(function (a) {
    var arrow = a.querySelector('.sub-arrow');
    (arrow || a).addEventListener('click', function (e) {
      var li = a.parentNode;
      if (arrow || a.getAttribute('href') === '#') { e.preventDefault(); li.classList.toggle('open'); }
    });
  });
  d.querySelectorAll('a.k-item-anchor[href="#"]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });
  // Selector de idioma
  d.querySelectorAll('.trp-language-switcher').forEach(function (n) {
    var cur = n.querySelector('.trp-language-item__current'), list = n.querySelector('.trp-switcher-dropdown-list');
    if (!cur || !list) return;
    function tog() { var open = list.hasAttribute('hidden'); if (open) list.removeAttribute('hidden'); else list.setAttribute('hidden', ''); cur.setAttribute('aria-expanded', open ? 'true' : 'false'); n.classList.toggle('is-open', open); }
    cur.addEventListener('click', tog);
    cur.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tog(); } });
  });
  // Pestañas (nested tabs)
  d.querySelectorAll('.e-n-tabs').forEach(function (w) {
    var titles = w.querySelectorAll(':scope > .e-n-tabs-heading > .e-n-tab-title');
    var panels = w.querySelectorAll(':scope > .e-n-tabs-content > .e-con');
    function show(i) {
      titles.forEach(function (t, j) { t.setAttribute('aria-selected', i === j ? 'true' : 'false'); t.tabIndex = i === j ? 0 : -1; });
      panels.forEach(function (p, j) { p.classList.toggle('e-active', i === j); });
    }
    titles.forEach(function (t, i) { t.addEventListener('click', function () { show(i); }); });
    if (titles.length) show(0);
  });
  // Carruseles: desplazamiento con flechas y autoplay suave
  d.querySelectorAll('.swiper').forEach(function (sw) {
    var wrap = sw.querySelector('.swiper-wrapper'); if (!wrap) return;
    var root = sw.closest('.k-widget') || sw.parentNode;
    var spv = parseInt(sw.getAttribute('data-spv') || '1', 10);
    function step(dir) { wrap.scrollBy({ left: dir * wrap.clientWidth / (spv || 1), behavior: 'smooth' }); }
    var prev = root.querySelector('.k-swiper-button-prev, .swiper-button-prev'), next = root.querySelector('.k-swiper-button-next, .swiper-button-next');
    if (prev) prev.addEventListener('click', function () { step(-1); });
    if (next) next.addEventListener('click', function () { step(1); });
    var auto = setInterval(function () {
      if (wrap.scrollLeft + wrap.clientWidth >= wrap.scrollWidth - 4) wrap.scrollTo({ left: 0, behavior: 'smooth' }); else step(1);
    }, 6000);
    sw.addEventListener('mouseenter', function () { clearInterval(auto); });
    sw.addEventListener('touchstart', function () { clearInterval(auto); }, { passive: true });
  });
  // Índice de contenidos plegable
  d.querySelectorAll('.k-toc__header').forEach(function (h) {
    h.addEventListener('click', function () { var w = h.closest('.k-widget-table-of-contents'); if (w) w.classList.toggle('k-toc--collapsed'); });
  });
  // Formularios: en la preview no se envían
  if (d.body.getAttribute('data-entorno') === 'preview') {
    d.querySelectorAll('form[data-belba-form]').forEach(function (f) {
      var p = d.createElement('p'); p.className = 'form-aviso'; p.textContent = 'Vista previa: este formulario no envía datos.';
      f.insertBefore(p, f.firstChild);
      f.addEventListener('submit', function (e) { e.preventDefault(); });
    });
  }
  // Mensaje tras envío correcto (?enviado=1)
  if (/[?&]enviado=1/.test(location.search)) {
    d.querySelectorAll('form[data-belba-form]').forEach(function (f) {
      var p = d.createElement('p'); p.className = 'form-ok'; p.textContent = '✓'; f.appendChild(p);
    });
  }
})();
