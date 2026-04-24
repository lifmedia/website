(function() {
  'use strict';

  if (!document.getElementById('hpForm')) return;

  var EMAILJS_PUBLIC_KEY = 'Xp2dcCiComLf_F4S2';
  var EMAILJS_SERVICE_ID = 'service_46f4l2j';
  var EMAILJS_TEMPLATE_ID = 'template_w48s8hd';
  var emailjsReady = false;
  function ensureEmailJS() {
    if (!emailjsReady && typeof emailjs !== 'undefined') {
      emailjs.init(EMAILJS_PUBLIC_KEY);
      emailjsReady = true;
    }
  }
  ensureEmailJS();

  var hpSelectedService = null;

  function hpShowToast(message, duration) {
    duration = duration || 4000;
    var toast = document.getElementById('hpToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'hpToast';
      toast.className = 'hp-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(function() { toast.classList.remove('show'); }, duration);
  }

  window.hpSelectService = function(card) {
    document.querySelectorAll('.hp-svc-card').forEach(function(c) { c.classList.remove('selected'); });
    card.classList.add('selected');
    hpSelectedService = card.dataset.service;
    setTimeout(function() { window.hpGoToStep(1); }, 350);
  };

  window.hpToggleChip = function(chip) {
    var parent = chip.parentElement;
    parent.querySelectorAll('.hp-chip').forEach(function(c) { c.classList.remove('selected'); });
    chip.classList.toggle('selected');
  };

  window.hpGoToStep = function(step) {
    var currentEl = document.querySelector('.hp-step.active');
    if (currentEl) currentEl.classList.remove('active');
    setTimeout(function() {
      var nextEl = document.querySelector('.hp-step[data-step="' + step + '"]');
      if (nextEl) nextEl.classList.add('active');
      document.querySelectorAll('.hp-progress-step').forEach(function(p) {
        var pStep = parseInt(p.dataset.step);
        p.classList.remove('active', 'completed');
        if (pStep === step) p.classList.add('active');
        if (pStep < step) p.classList.add('completed');
      });
      var formEl = document.getElementById('hpForm');
      if (formEl) formEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  function hpCollectFormData() {
    var data = { service: hpSelectedService };
    document.querySelectorAll('.hp-step[data-step="1"] input, .hp-step[data-step="1"] textarea').forEach(function(el) {
      var field = el.dataset.field;
      if (field && el.value) data[field] = el.value;
    });
    document.querySelectorAll('.hp-step[data-step="1"] .hp-chips').forEach(function(group) {
      var field = group.dataset.field;
      var selected = Array.from(group.querySelectorAll('.hp-chip.selected')).map(function(c) { return c.textContent.trim(); });
      if (selected.length) data[field] = selected.join(', ');
    });
    return data;
  }

  function hpValidateContact() {
    var valid = true;
    var step = document.querySelector('.hp-step[data-step="1"]');
    var name = step.querySelector('[data-field="name"]');
    var email = step.querySelector('[data-field="email"]');
    step.querySelectorAll('.hp-field').forEach(function(f) { f.classList.remove('error'); });
    if (!name.value.trim()) { name.closest('.hp-field').classList.add('error'); valid = false; }
    if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) { email.closest('.hp-field').classList.add('error'); valid = false; }
    return valid;
  }

  window.hpSubmitForm = function() {
    if (!hpValidateContact()) return;
    var btn = document.getElementById('hpBtnSubmit');
    var originalHTML = btn.innerHTML;
    btn.innerHTML = '<span class="hp-spinner"></span> Sending...';
    btn.disabled = true;
    var data = hpCollectFormData();
    var serviceNames = { commercial: 'Cinematic Commercial', social: 'Social Media Content', documentary: 'Brand Documentary', event: 'Event Coverage' };
    var projectDetails = '';
    if (data.budget) projectDetails += 'Budget: ' + data.budget + '\n';
    if (data.how_found) projectDetails += 'How They Found Us: ' + data.how_found + '\n';
    if (data.additional_notes) projectDetails += 'Notes: ' + data.additional_notes + '\n';
    var templateParams = {
      from_name: data.name || '', from_email: data.email || '',
      company: data.company || 'N/A', phone: data.phone || 'N/A',
      website: 'N/A', service: serviceNames[data.service] || data.service,
      project_details: projectDetails || 'No additional details provided.'
    };
    ensureEmailJS();
    emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams).then(function() {
      if (typeof gtag === 'function') {
        gtag('event', 'conversion', {
          'send_to': 'AW-17933483390/qHYXCJLw-JYcEP76rOdC',
          'value': 1.0,
          'currency': 'CAD',
          'event_callback': function() {
            window.location.href = '/thank-you/';
          }
        });
      }
      setTimeout(function() { window.location.href = '/thank-you/'; }, 1500);
    }).catch(function(error) {
      console.error('EmailJS Error:', error);
      btn.innerHTML = originalHTML;
      btn.disabled = false;
      hpShowToast('Something went wrong. Please try again or email us directly at contact@lifmedia.ca');
    });
  };
})();
