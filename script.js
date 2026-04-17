/* =============================================================
   СРО ССС · Apple-style scroll behavior
   ============================================================= */

(() => {
  'use strict';

  /* ---------- Scroll reveal (IntersectionObserver) ---------- */
  const revealSelector = '.reveal, .reveal-up';
  const revealEls = document.querySelectorAll(revealSelector);

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -10% 0px', threshold: 0.08 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-in'));
  }

  /* ---------- Animated number counters ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const easeOut = (t) => 1 - Math.pow(1 - t, 3);

  const animate = (el) => {
    const target = parseFloat(el.dataset.count || '0');
    const duration = 1600;
    const start = performance.now();
    const initial = 0;

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const value = initial + (target - initial) * easeOut(progress);
      el.textContent = Math.round(value).toLocaleString('ru-RU');
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString('ru-RU');
    };
    requestAnimationFrame(tick);
  };

  if ('IntersectionObserver' in window) {
    const countIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target);
            countIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => countIO.observe(el));
  }

  /* ---------- Parallax: hero image + banner ---------- */
  const heroImage = document.querySelector('.hero__image');
  const banner = document.querySelector('.banner--skyline');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let ticking = false;
  const onScroll = () => {
    if (prefersReduced) return;
    const y = window.scrollY;

    if (heroImage) {
      const scale = 1.08 + Math.min(y / 3000, 0.06);
      const translate = Math.min(y * 0.25, 180);
      heroImage.style.transform = `translateY(${translate}px) scale(${scale})`;
    }

    if (banner) {
      const rect = banner.getBoundingClientRect();
      const vh = window.innerHeight;
      if (rect.top < vh && rect.bottom > 0) {
        const progress = (vh - rect.top) / (vh + rect.height);
        const shift = (progress - 0.5) * 80;
        banner.style.setProperty('--parallax', `${shift}px`);
        banner.style.backgroundPositionY = `calc(50% + ${shift}px)`;
      }
    }

    ticking = false;
  };

  window.addEventListener(
    'scroll',
    () => {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    },
    { passive: true }
  );
  onScroll();

  /* ---------- Auto-hide nav on scroll down, show on up ---------- */
  const nav = document.getElementById('nav');
  let lastY = window.scrollY;
  let navTicking = false;

  const updateNav = () => {
    const y = window.scrollY;
    if (nav) {
      if (y > 120 && y > lastY) nav.classList.add('is-hidden');
      else nav.classList.remove('is-hidden');
    }
    lastY = y;
    navTicking = false;
  };

  window.addEventListener(
    'scroll',
    () => {
      if (!navTicking) {
        window.requestAnimationFrame(updateNav);
        navTicking = true;
      }
    },
    { passive: true }
  );
})();
