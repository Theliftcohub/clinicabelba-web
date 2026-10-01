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
  // Desplegables del menú de escritorio: abrir al pasar y cerrar con retardo (como SmartMenus en el WP), sin parpadeos
  // Al abrir un elemento se cierran YA sus hermanos abiertos (si no, con el retardo, el panel del anterior se solapa con el nuevo)
  d.querySelectorAll('.k-nav-menu--main .menu-item-has-children').forEach(function (li) {
    function open() {
      clearTimeout(li._t);
      Array.prototype.forEach.call(li.parentNode.children, function (s) {
        if (s !== li && s.classList.contains('open')) { clearTimeout(s._t); s.classList.remove('open'); s.querySelectorAll('li.open').forEach(function (x) { x.classList.remove('open'); }); }
      });
      li.classList.add('open');
    }
    li.addEventListener('mouseenter', open);
    li.addEventListener('mouseleave', function () { li._t = setTimeout(function () { li.classList.remove('open'); }, 350); });
    li.addEventListener('focusin', open);
    li.addEventListener('focusout', function () { setTimeout(function () { if (!li.contains(d.activeElement)) li.classList.remove('open'); }, 100); });
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
  // Selector de idioma de la cabecera (sustituye al flotante de TranslatePress)
  d.querySelectorAll('.ls').forEach(function (n) {
    var btn = n.querySelector('.ls__cur'), list = n.querySelector('.ls__list');
    function tog(open) { if (open === undefined) open = list.hidden; list.hidden = !open; btn.setAttribute('aria-expanded', open ? 'true' : 'false'); n.classList.toggle('is-open', open); }
    btn.addEventListener('click', function (e) { e.stopPropagation(); tog(); });
    d.addEventListener('click', function (e) { if (!n.contains(e.target)) tog(false); });
    n.addEventListener('keydown', function (e) { if (e.key === 'Escape') { tog(false); btn.focus(); } });
  });
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
  // Acordeones de Elementor (<details>): estado activo para su CSS y, como en el WordPress, uno abierto a la vez
  d.querySelectorAll('.k-accordion').forEach(function (acc) {
    var items = acc.querySelectorAll('details.k-accordion-item');
    function sync() { items.forEach(function (it) { var t = it.querySelector('.k-tab-title'); if (t) { t.classList.toggle('k-active', it.open); t.setAttribute('aria-expanded', it.open ? 'true' : 'false'); } }); }
    items.forEach(function (it) { it.addEventListener('toggle', function () { if (it.open) items.forEach(function (o) { if (o !== it) o.open = false; }); sync(); }); });
    sync();
  });
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
      if (i === 1 && !f._started) { f._started = true; window.dataLayer.push({ event: 'lead_form_start', form_id: f.getAttribute('data-form-id') || '', form_page: location.pathname }); }
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

  // ---- Formularios de Elementor largos → conversación por pasos (decisión Oscar 28/09) ----
  // Mismos campos y textos; solo cambia la presentación: primero la pregunta (doctor, mensaje),
  // después los datos de contacto de dos en dos y al final la aceptación + enviar. Sin JS, el formulario se ve entero.
  var NAV = { es: ['Siguiente', 'Atrás'], ca: ['Següent', 'Enrere'], en: ['Next', 'Back'], fr: ['Suivant', 'Retour'], de: ['Weiter', 'Zurück'], it: ['Avanti', 'Indietro'], nl: ['Volgende', 'Terug'], ru: ['Далее', 'Назад'], uk: ['Далі', 'Назад'] };
  d.querySelectorAll('form.k-form[data-belba-form]').forEach(function (f) {
    var wrap = f.querySelector('.k-form-fields-wrapper'); if (!wrap) return;
    var groups = [].slice.call(wrap.querySelectorAll(':scope > .k-field-group'));
    var submit = groups.filter(function (g) { return g.classList.contains('k-field-type-submit'); })[0];
    var fields = groups.filter(function (g) { return g !== submit && !g.classList.contains('k-field-type-hidden'); });
    if (fields.length < 4 || !submit) return; // formularios cortos (nombre + teléfono) se quedan en una línea
    var isQ = function (g) { return /k-field-type-(select|radio|textarea|checkbox)\b/.test(g.className) && !g.classList.contains('k-field-type-acceptance'); };
    var acc = fields.filter(function (g) { return g.classList.contains('k-field-type-acceptance'); });
    var qs_ = fields.filter(isQ), contact = fields.filter(function (g) { return !isQ(g) && acc.indexOf(g) < 0; });
    var plan = qs_.map(function (g) { return [g]; });
    for (var i = 0; i < contact.length; i += 2) plan.push(contact.slice(i, i + 2));
    if (!plan.length) return;
    plan[plan.length - 1] = plan[plan.length - 1].concat(acc, [submit]);
    var L = NAV[(d.documentElement.lang || 'es').slice(0, 2)] || NAV.es;
    f.classList.add('is-steps');
    var bar = d.createElement('div'); bar.className = 'bf-progress'; bar.setAttribute('aria-hidden', 'true'); bar.appendChild(d.createElement('span'));
    wrap.parentNode.insertBefore(bar, wrap);
    var steps = plan.map(function (gs, n) {
      var s = d.createElement('div'); s.className = 'k-step'; s.setAttribute('data-kstep', '');
      var c = d.createElement('p'); c.className = 'bf-count'; c.textContent = (n + 1) + ' / ' + plan.length; s.appendChild(c);
      gs.forEach(function (g) { s.appendChild(g); });
      var nav = d.createElement('div'); nav.className = 'bf-nav';
      if (n > 0) { var b = d.createElement('button'); b.type = 'button'; b.className = 'bf-back'; b.textContent = L[1]; nav.appendChild(b); }
      if (n < plan.length - 1) { var nx = d.createElement('button'); nx.type = 'button'; nx.className = 'bf-next'; nx.textContent = L[0]; nav.appendChild(nx); }
      if (nav.children.length) s.appendChild(nav);
      wrap.appendChild(s); return s;
    });
    var cur = 0;
    function show(i) {
      steps.forEach(function (s, j) { s.hidden = j !== i; }); cur = i;
      bar.firstChild.style.width = Math.round(100 * (i + 1) / steps.length) + '%';
      if (i > 0) { var el = steps[i].querySelector('input:not([type=hidden]),select,textarea'); if (el) el.focus({ preventScroll: true }); }
    }
    function valid(i) {
      var ok = true;
      steps[i].querySelectorAll('input,select,textarea').forEach(function (el) { if (!el.checkValidity() || (el.required && el.type !== 'checkbox' && !String(el.value).trim())) ok = false; });
      if (!ok) { var bad = steps[i].querySelector(':invalid'); if (bad && bad.reportValidity) bad.reportValidity(); }
      return ok;
    }
    f.addEventListener('click', function (e) {
      if (e.target.closest('.bf-next')) { e.preventDefault(); if (valid(cur)) { show(cur + 1); if (cur === 1) window.dataLayer.push({ event: 'lead_form_start', form_id: f.getAttribute('data-form-id') || '', form_page: location.pathname }); } }
      if (e.target.closest('.bf-back')) { e.preventDefault(); if (cur > 0) show(cur - 1); }
    });
    f.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT' && cur < steps.length - 1) { e.preventDefault(); if (valid(cur)) show(cur + 1); } });
    show(0);
  });

  // ---- Formularios cortos (nombre + teléfono): el lead ya está capturado; después, UNA pregunta opcional ----
  // Pregunta y opciones del formulario general "Belba Gral" (literal en ES; traducciones en scripts/home_i18n.py, las escribe build_assets.py)
  /*FOLLOW-START*/ var FOLLOW = {"es": {"q": "¿Cuándo tienes pensado operarte?", "o": ["Lo antes posible", "En los próximos 1–3 meses", "En 3–6 meses", "Aún estoy evaluando, no tengo fecha definida"], "skip": "Ahora no", "thanks": "¡Gracias por enviar la información! Nos pondremos en contacto contigo muy pronto."}, "ca": {"q": "Quan tens pensat operar-te?", "o": ["Com més aviat millor", "En els propers 1–3 mesos", "D'aquí a 3–6 mesos", "Encara ho estic valorant, no tinc data"], "skip": "Ara no", "thanks": "Gràcies per enviar la informació! Ens posarem en contacte amb tu molt aviat."}, "en": {"q": "When are you planning to have surgery?", "o": ["As soon as possible", "In the next 1–3 months", "In 3–6 months", "Still considering, no date yet"], "skip": "Not now", "thanks": "Thank you for sending your information! We will contact you very soon."}, "fr": {"q": "Quand envisagez-vous de vous faire opérer ?", "o": ["Le plus tôt possible", "Dans les 1 à 3 prochains mois", "Dans 3 à 6 mois", "J'y réfléchis encore, sans date définie"], "skip": "Pas maintenant", "thanks": "Merci d'avoir envoyé vos informations ! Nous vous contacterons très prochainement."}, "de": {"q": "Wann möchten Sie sich operieren lassen?", "o": ["So bald wie möglich", "In den nächsten 1–3 Monaten", "In 3–6 Monaten", "Ich überlege noch, kein festes Datum"], "skip": "Jetzt nicht", "thanks": "Vielen Dank für Ihre Angaben! Wir melden uns sehr bald bei Ihnen."}, "it": {"q": "Quando pensi di operarti?", "o": ["Il prima possibile", "Nei prossimi 1–3 mesi", "Tra 3–6 mesi", "Ci sto ancora pensando, nessuna data"], "skip": "Non ora", "thanks": "Grazie per averci inviato le informazioni! Ti contatteremo molto presto."}, "nl": {"q": "Wanneer wil je je laten opereren?", "o": ["Zo snel mogelijk", "Binnen 1–3 maanden", "Over 3–6 maanden", "Ik overweeg het nog, geen datum"], "skip": "Nu niet", "thanks": "Bedankt voor het versturen van je gegevens! We nemen zeer binnenkort contact met je op."}, "ru": {"q": "Когда вы планируете операцию?", "o": ["Как можно скорее", "В ближайшие 1–3 месяца", "Через 3–6 месяцев", "Пока думаю, даты нет"], "skip": "Не сейчас", "thanks": "Спасибо за отправленную информацию! Мы свяжемся с вами в ближайшее время."}, "uk": {"q": "Коли ви плануєте операцію?", "o": ["Якомога швидше", "У найближчі 1–3 місяці", "Через 3–6 місяців", "Ще думаю, дати немає"], "skip": "Не зараз", "thanks": "Дякуємо за надіслану інформацію! Ми зв'яжемося з вами найближчим часом."}}; /*FOLLOW-END*/
  function followUp(f, data, info) {
    var T = FOLLOW[(d.documentElement.lang || '').slice(0, 2)]; if (!T) return false;
    var box = d.createElement('div'); box.className = 'bf-follow belba-form belba-form--compact'; box.setAttribute('role', 'group');
    var okm = d.createElement('p'); okm.className = 'bf-ok'; okm.textContent = '✓'; box.appendChild(okm);
    var p = d.createElement('p'); p.className = 'bf-title'; p.textContent = T.q; box.appendChild(p);
    var ch = d.createElement('div'); ch.className = 'bf-choices';
    T.o.forEach(function (o) { var b = d.createElement('button'); b.type = 'button'; b.className = 'bf-choice'; b.textContent = o; ch.appendChild(b); });
    box.appendChild(ch);
    var sk = d.createElement('button'); sk.type = 'button'; sk.className = 'bf-back bf-skip'; sk.textContent = T.skip; box.appendChild(sk);
    f.appendChild(box);
    var fin = function () { box.innerHTML = ''; var t = d.createElement('p'); t.className = 'bf-thanks-txt'; t.textContent = T.thanks; box.appendChild(t); };
    sk.addEventListener('click', fin);
    ch.addEventListener('click', function (e) {
      var b = e.target.closest('.bf-choice'); if (!b) return;
      var fd = new FormData();
      data.forEach(function (v, k) { if (k !== 'form_id') fd.append(k, v); });
      fd.set('form_id', (f.getAttribute('data-form-id') || 'el') + '-cualificacion');
      fd.set('q_cuando_tienes_pensado_operarte', b.textContent);
      window.dataLayer.push({ event: 'lead_form_qualify', form_id: info.form_id, form_page: info.form_page, answer: b.textContent, lead_source: info.lead_source, lead_medium: info.lead_medium });
      fin();
      if (!PREVIEW) fetch(f.getAttribute('action') || '/form-handler.php', { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } }).catch(function () {});
    });
    return true;
  }

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
      var ref_ = f.querySelector('input[name="lead_ref"]');
      if (!ref_) { ref_ = d.createElement('input'); ref_.type = 'hidden'; ref_.name = 'lead_ref'; f.appendChild(ref_); }
      ref_.value = (Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10));
      var btn = f.querySelector('[type=submit]'), err = f.querySelector('.bf-error');
      if (btn) { btn.disabled = true; btn.dataset.txt = btn.textContent; btn.textContent = f.getAttribute('data-sending') || '…'; }
      var data = new FormData(f);
      var info = { event: 'lead_form_submit', form_id: f.getAttribute('data-form-id') || '', form_name: f.getAttribute('data-form-name') || '', form_page: location.pathname, form_lang: d.documentElement.lang, lead_source: first.source, lead_medium: first.medium };
      function done() {
        window.dataLayer.push(info);
        var red = f.getAttribute('data-redirect');
        if (red) { setTimeout(function () { location.href = red; }, 300); return; }
        f.querySelectorAll('[data-step], .bf-progress, .k-form-fields-wrapper, .form-aviso').forEach(function (s) { s.hidden = true; s.style.setProperty('display', 'none', 'important'); });
        var th = f.querySelector('.bf-thanks');
        if (th) th.hidden = false;
        else if (!(f.classList.contains('k-form') && !f.classList.contains('is-steps') && followUp(f, data, info))) { var ok = d.createElement('p'); ok.className = 'form-ok'; ok.textContent = '✓'; f.appendChild(ok); }
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
