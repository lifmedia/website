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
})();
