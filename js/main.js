(function() {
  'use strict';

  // Header scroll effect
  var hdr = document.getElementById('lif-hdr');
  if (hdr) {
    function onScroll() {
      hdr.classList.toggle('hdr-scrolled', window.scrollY > 50);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Menu open/close
  var menuBtn = document.getElementById('lifMenuBtn');
  var mobClose = document.getElementById('lifMobClose');
  var mob = document.getElementById('lif-mob');

  if (menuBtn && mob) {
    menuBtn.addEventListener('click', function() {
      mob.classList.add('mob-open');
      document.body.style.overflow = 'hidden';
    });
  }
  if (mobClose && mob) {
    mobClose.addEventListener('click', function() {
      mob.classList.remove('mob-open');
      document.body.style.overflow = '';
    });
  }
  if (mob) {
    document.querySelectorAll('#lif-mob a').forEach(function(a) {
      a.addEventListener('click', function() {
        if (a.getAttribute('href') === '#') return;
        mob.classList.remove('mob-open');
        document.body.style.overflow = '';
      });
    });
  }

  // Scroll reveal animations
  var reveals = document.querySelectorAll('.lif-reveal');
  if (reveals.length) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function(el) { observer.observe(el); });
  }

  // Duplicate marquee track for seamless loop
  var marqueeTrack = document.getElementById('marqueeTrack');
  if (marqueeTrack) {
    marqueeTrack.innerHTML += marqueeTrack.innerHTML;
  }

  // Duplicate carousel track for seamless loop
  var carouselTrack = document.getElementById('carouselTrack');
  if (carouselTrack) {
    carouselTrack.innerHTML += carouselTrack.innerHTML;
  }

  // Floating Action Button — phone call, injected on all pages
  var fab = document.createElement('a');
  fab.href = 'tel:+15066887043';
  fab.className = 'lif-fab';
  fab.id = 'lifFab';
  fab.setAttribute('aria-label', 'Call us');
  fab.setAttribute('onclick', "return gtag_report_conversion('tel:+15066887043');");
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>';
  document.body.appendChild(fab);

  // Show FAB after scrolling past hero (homepage) or immediately (subpages)
  var heroSection = document.querySelector('.lif-hero');
  if (heroSection) {
    var fabObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        fab.classList.toggle('visible', !entry.isIntersecting);
      });
    }, { threshold: 0 });
    fabObserver.observe(heroSection);
  } else {
    // Subpages: always show after a short scroll
    window.addEventListener('scroll', function() {
      fab.classList.toggle('visible', window.scrollY > 200);
    }, { passive: true });
    fab.classList.toggle('visible', window.scrollY > 200);
  }
})();
