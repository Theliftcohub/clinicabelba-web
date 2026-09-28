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
  // ---- Atribución: primera visita (se guarda 90 días) y visita actual ----
  var ATTR_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ad_id', 'adgroup_id', 'campaign_id'];
  function qs() { var o = {}; location.search.replace(/^\?/, '').split('&').forEach(function (p) { if (!p) return; var kv = p.split('='); try { o[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || '').replace(/\+/g, ' ')); } catch (e) {} }); return o; }
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  var q = qs(), now = Date.now();
  var ref = document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : '';
  function sourceOf() {
    if (q.gclid) return ['google', 'cpc'];
    if (q.fbclid) return ['facebook', q.utm_medium || 'paid_social'];
    if (q.utm_source) return [q.utm_source, q.utm_medium || ''];
    if (!ref) return ['(direct)', '(none)'];
    var h = ''; try { h = new URL(ref).hostname; } catch (e) {}
    if (/google\.|bing\.|yahoo\.|duckduckgo\.|ecosia\.|yandex\./.test(h)) return [h.replace(/^www\./, ''), 'organic'];
    if (/chatgpt\.com|openai\.com|perplexity\.ai|claude\.ai|gemini\.google|copilot\.microsoft/.test(h)) return [h.replace(/^www\./, ''), 'ai'];
    if (/facebook\.|instagram\.|t\.co|twitter\.|linkedin\.|tiktok\./.test(h)) return [h.replace(/^www\./, ''), 'social'];
    return [h.replace(/^www\./, ''), 'referral'];
  }
  var first = store('belba_first');
  if (!first || now - (first.ts || 0) > 90 * 864e5) {
    var so = sourceOf();
    first = { source: so[0], medium: so[1], landing: location.pathname, referrer: ref, ts: now };
    store('belba_first', first);
  }
  var last = store('belba_last') || {};
  if (ATTR_KEYS.some(function (k) { return q[k]; }) || ref) { last = { q: {}, ref: ref, landing: location.pathname }; ATTR_KEYS.forEach(function (k) { if (q[k]) last.q[k] = q[k]; }); store('belba_last', last); }
  function gaClientId() { var m = document.cookie.match(/(?:^|; )_ga=GA\d\.\d\.(\d+\.\d+)/); return m ? m[1] : ''; }
  function fillAttr(f) {
    var set = function (n, v) { var el = f.querySelector('input[name="' + n + '"]'); if (el && v) el.value = v; };
    ATTR_KEYS.forEach(function (k) { set(k, q[k] || (last.q && last.q[k]) || ''); });
    set('first_source', first.source); set('first_medium', first.medium); set('first_landing', first.landing);
    set('first_referrer', first.referrer); set('first_ts', new Date(first.ts).toISOString());
    set('referrer', last.ref || ref); set('landing', last.landing || location.pathname); set('ga_client_id', gaClientId());
  }
  window.dataLayer = window.dataLayer || [];

  // ---- Formularios por pasos (sustitutos de Typeform) ----
  d.querySelectorAll('form.belba-form').forEach(function (f) {
    var steps = f.querySelectorAll('[data-step]'), cur = 0, bar = f.querySelector('.bf-progress span');
    function show(i) {
      steps.forEach(function (s, j) { s.hidden = j !== i; });
      cur = i; if (bar) bar.style.width = Math.round(100 * (i + 1) / steps.length) + '%';
      var first = steps[i].querySelector('input:not([type=hidden]),button'); if (first && i > 0) first.focus({ preventScroll: true });
    }
    function valid(i) {
      var ok = true;
      steps[i].querySelectorAll('input[required]').forEach(function (inp) {
        if (inp.type === 'radio') { if (!f.querySelector('input[name="' + inp.name + '"]:checked')) ok = false; }
        else if (!inp.value.trim() || !inp.checkValidity()) ok = false;
      });
      steps[i].classList.toggle('bf-invalid', !ok);
      return ok;
    }
    f.addEventListener('click', function (e) {
      if (e.target.closest('.bf-next')) { e.preventDefault(); if (valid(cur) && cur < steps.length - 1) show(cur + 1); }
      if (e.target.closest('.bf-back')) { e.preventDefault(); if (cur > 0) show(cur - 1); }
    });
    f.addEventListener('change', function (e) {
      if (e.target.type === 'radio' && cur < steps.length - 1 && steps[cur].querySelectorAll('input:not([type=radio])').length === 0) setTimeout(function () { show(cur + 1); }, 180);
    });
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT' && cur < steps.length - 1) { e.preventDefault(); if (valid(cur)) show(cur + 1); }
    });
    show(0);
  });

  // ---- Envío de TODOS los formularios (nativos y los antiguos de Elementor) ----
  var PREVIEW = d.body.getAttribute('data-entorno') === 'preview';
  d.querySelectorAll('form[data-belba-form]').forEach(function (f) {
    fillAttr(f);
    if (PREVIEW) { var p = d.createElement('p'); p.className = 'form-aviso'; p.textContent = 'Vista previa: el envío es simulado (no llega a ningún sitio), pero dispara el evento de medición.'; f.insertBefore(p, f.firstChild); }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.classList.contains('belba-form')) { var st = f.querySelectorAll('[data-step]'); for (var i = 0; i < st.length; i++) if (!st[i].hidden) { var reqs = st[i].querySelectorAll('input[required]'), ok = true; reqs.forEach(function (r) { if (r.type === 'radio' ? !f.querySelector('input[name="' + r.name + '"]:checked') : !r.value.trim() || !r.checkValidity()) ok = false; }); if (!ok) { st[i].classList.add('bf-invalid'); return; } } }
      else if (!f.checkValidity()) { f.reportValidity(); return; }
      fillAttr(f);
      var btn = f.querySelector('[type=submit]'), err = f.querySelector('.bf-error');
      if (btn) { btn.disabled = true; btn.dataset.txt = btn.textContent; btn.textContent = f.getAttribute('data-sending') || '…'; }
      var data = new FormData(f);
      var info = { event: 'lead_form_submit', form_id: f.getAttribute('data-form-id') || '', form_name: f.getAttribute('data-form-name') || '', form_page: location.pathname, form_lang: d.documentElement.lang, lead_source: first.source, lead_medium: first.medium };
      function done() {
        window.dataLayer.push(info);
        var red = f.getAttribute('data-redirect');
        if (red) { setTimeout(function () { location.href = red; }, 300); return; }
        f.querySelectorAll('[data-step], .bf-progress, .k-form-fields-wrapper').forEach(function (s) { s.hidden = true; });
        var th = f.querySelector('.bf-thanks'); if (th) th.hidden = false; else { var ok = d.createElement('p'); ok.className = 'form-ok'; ok.textContent = '✓'; f.appendChild(ok); }
      }
      function fail() {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.txt; }
        if (!err) { err = d.createElement('p'); err.className = 'bf-error'; err.setAttribute('role', 'alert'); f.appendChild(err); }
        err.textContent = f.getAttribute('data-error') || 'No se ha podido enviar. Inténtalo de nuevo o escríbenos por WhatsApp.'; err.hidden = false;
      }
      if (PREVIEW) { done(); return; }
      fetch(f.getAttribute('action') || '/form-handler.php', { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (j) { if (j && j.ok) done(); else fail(); })
        .catch(fail);
    });
  });
})();
