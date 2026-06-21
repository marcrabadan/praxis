/* praxis landing — progressive enhancement, vanilla JS */
(function () {
  'use strict';

  /* ---------- Theme toggle ---------- */
  var root = document.documentElement;
  var themeBtn = document.querySelector('.theme-toggle');
  var themeMeta = document.getElementById('theme-color-meta');

  function syncThemeButton(theme) {
    if (!themeBtn) { return; }
    var goingTo = theme === 'light' ? 'dark' : 'light';
    themeBtn.setAttribute('aria-label', 'Switch to ' + goingTo + ' theme');
    themeBtn.setAttribute('aria-pressed', String(theme === 'light'));
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeMeta) { themeMeta.setAttribute('content', theme === 'light' ? '#ffffff' : '#0a0f1a'); }
    syncThemeButton(theme);
  }

  syncThemeButton(root.getAttribute('data-theme') || 'dark');

  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      applyTheme(next);
      try { localStorage.setItem('praxis-theme', next); } catch (e) { /* storage may be blocked */ }
    });
  }

  /* Follow the OS preference unless the visitor has made an explicit choice. */
  var mql = window.matchMedia('(prefers-color-scheme: light)');
  var onSchemeChange = function (e) {
    var hasChoice;
    try { hasChoice = !!localStorage.getItem('praxis-theme'); } catch (err) { hasChoice = false; }
    if (!hasChoice) { applyTheme(e.matches ? 'light' : 'dark'); }
  };
  if (mql.addEventListener) { mql.addEventListener('change', onSchemeChange); }
  else if (mql.addListener) { mql.addListener(onSchemeChange); }

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
  var statusRegion = document.getElementById('status-region');
  function announce(msg) { if (statusRegion) { statusRegion.textContent = msg; } }

  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var code = btn.parentElement.querySelector('pre');
      if (!code) { return; }
      navigator.clipboard.writeText(code.innerText).then(function () {
        var prev = btn.textContent;
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        announce('Copied to clipboard');
        setTimeout(function () { btn.textContent = prev; btn.classList.remove('copied'); }, 1800);
      }).catch(function () {
        btn.textContent = 'Error';
        announce('Copy failed');
        setTimeout(function () { btn.textContent = 'Copy'; }, 1800);
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

    document.querySelectorAll('.card, .expert, .step, .meta-pill, .example-card').forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity .5s ease, transform .5s ease';
      io.observe(el);
    });
  }

  /* ---------- Active-section nav (scrollspy) ---------- */
  if ('IntersectionObserver' in window) {
    /* Map each section id to every nav link that targets it (desktop + mobile). */
    var linkMap = {};
    document.querySelectorAll('.nav-links a[href^="#"], .mobile-menu a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      if (!id) { return; }
      (linkMap[id] = linkMap[id] || []).push(a);
    });

    var sections = Object.keys(linkMap)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    var current = null;
    function setCurrent(id) {
      if (id === current) { return; }
      current = id;
      Object.keys(linkMap).forEach(function (key) {
        var on = key === id;
        linkMap[key].forEach(function (a) {
          if (on) { a.setAttribute('aria-current', 'true'); }
          else { a.removeAttribute('aria-current'); }
        });
      });
    }

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { setCurrent(entry.target.id); }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- Back to top ---------- */
  var toTop = document.querySelector('.to-top');
  if (toTop) {
    var ticking = false;
    function updateToTop() {
      ticking = false;
      var show = window.scrollY > window.innerHeight * 0.6;
      toTop.classList.toggle('visible', show);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(updateToTop); ticking = true; }
    }, { passive: true });
    updateToTop();

    toTop.addEventListener('click', function () {
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      /* Return keyboard focus to the top of the document for a sensible tab order. */
      var brand = document.querySelector('.brand');
      if (brand) { brand.setAttribute('tabindex', '-1'); brand.focus({ preventScroll: true }); }
    });
  }
})();
