/* praxis landing — progressive enhancement, vanilla JS */
(function () {
  'use strict';

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('mobile-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.hasAttribute('hidden');
      if (open) { menu.removeAttribute('hidden'); } else { menu.setAttribute('hidden', ''); }
      toggle.setAttribute('aria-expanded', String(open));
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.setAttribute('hidden', '');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Install tabs (ARIA tablist) ---------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('.tab-panel'));

  function activate(tab) {
    tabs.forEach(function (t) {
      var selected = t === tab;
      t.classList.toggle('active', selected);
      t.setAttribute('aria-selected', String(selected));
      t.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(function (p) {
      var show = p.id === tab.getAttribute('aria-controls');
      p.classList.toggle('active', show);
      if (show) { p.removeAttribute('hidden'); } else { p.setAttribute('hidden', ''); }
    });
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { activate(tab); });
    tab.addEventListener('keydown', function (e) {
      var next;
      if (e.key === 'ArrowRight') { next = tabs[(i + 1) % tabs.length]; }
      else if (e.key === 'ArrowLeft') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
      if (next) { e.preventDefault(); next.focus(); activate(next); }
    });
  });

  /* ---------- Copy-to-clipboard ---------- */
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.parentElement.querySelector('pre');
      if (!code) { return; }
      navigator.clipboard.writeText(code.innerText).then(function () {
        var prev = btn.textContent;
        btn.textContent = '¡Copiado!';
        btn.classList.add('copied');
        setTimeout(function () { btn.textContent = prev; btn.classList.remove('copied'); }, 1800);
      }).catch(function () {
        btn.textContent = 'Error';
        setTimeout(function () { btn.textContent = 'Copiar'; }, 1800);
      });
    });
  });

  /* ---------- Reveal on scroll ---------- */
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'none';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    document.querySelectorAll('.card, .expert, .step, .meta-pill').forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity .5s ease, transform .5s ease';
      io.observe(el);
    });
  }
})();
