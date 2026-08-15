// ===== FORM JS =====
document.addEventListener('DOMContentLoaded', function () {
  // Section collapsible toggle
  document.querySelectorAll('.section-header').forEach(function (header) {
    header.addEventListener('click', function () {
      var body = header.nextElementSibling;
      var toggle = header.querySelector('.section-toggle');
      body.classList.toggle('collapsed');
      header.classList.toggle('collapsed');
    });
  });

  // Progress bar
  var allRequired = document.querySelectorAll('[required]');
  function updateProgress() {
    var filled = 0;
    allRequired.forEach(function (el) {
      if (el.type === 'checkbox') { if (el.checked) filled++; }
      else if (el.value.trim() !== '') { filled++; }
    });
    var pct = allRequired.length ? Math.round((filled / allRequired.length) * 100) : 0;
    var bar = document.querySelector('.form-progress-fill');
    if (bar) { bar.style.width = pct + '%'; }
  }
  allRequired.forEach(function (el) {
    el.addEventListener('input', updateProgress);
    el.addEventListener('change', updateProgress);
  });
  updateProgress();

  // Backlog conditional
  var currentBacklog = document.querySelector('[name="current_backlog"]');
  var numBacklogs = document.querySelector('[name="number_of_backlogs"]');
  if (currentBacklog && numBacklogs) {
    function toggleBacklogs() {
      var grp = numBacklogs.closest('.form-group');
      if (currentBacklog.value === 'True' || currentBacklog.value === 'true' || currentBacklog.checked) {
        grp.style.display = '';
        numBacklogs.required = true;
      } else {
        grp.style.display = 'none';
        numBacklogs.required = false;
        numBacklogs.value = '0';
      }
    }
    currentBacklog.addEventListener('change', toggleBacklogs);
    toggleBacklogs();
  }

  // PAN uppercase
  var panField = document.querySelector('[name="pan_number"]');
  if (panField) {
    panField.addEventListener('input', function () {
      this.value = this.value.toUpperCase();
    });
  }

  // Mobile number: digits only
  document.querySelectorAll('[name="mobile"],[name="alternate_mobile"],[name="guardian_mobile"]').forEach(function (el) {
    el.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '').slice(0, 10);
    });
  });

  // Aadhaar: digits only
  var aadhaarField = document.querySelector('[name="aadhaar_number"]');
  if (aadhaarField) {
    aadhaarField.addEventListener('input', function () {
      this.value = this.value.replace(/\D/g, '').slice(0, 12);
    });
  }

  // Client-side validation on submit
  var form = document.querySelector('#studentForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      var valid = true;
      // Clear previous errors
      document.querySelectorAll('.is-invalid').forEach(function (el) { el.classList.remove('is-invalid'); });
      document.querySelectorAll('.client-error').forEach(function (el) { el.remove(); });

      function showError(el, msg) {
        el.classList.add('is-invalid');
        var err = document.createElement('div');
        err.className = 'invalid-feedback client-error';
        err.innerHTML = '⚠ ' + msg;
        el.parentNode.appendChild(err);
        valid = false;
      }

      // Required fields
      form.querySelectorAll('[required]').forEach(function (el) {
        if (el.type === 'checkbox') {
          if (!el.checked) showError(el, 'This field is required.');
        } else if (el.value.trim() === '') {
          showError(el, 'This field is required.');
        }
      });

      // Email
      var email = form.querySelector('[name="email"]');
      if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, 'Enter a valid email address.');
      }

      // Mobile
      var mob = form.querySelector('[name="mobile"]');
      if (mob && mob.value && !/^[6-9]\d{9}$/.test(mob.value)) {
        showError(mob, 'Enter a valid 10-digit Indian mobile number.');
      }

      // Alternate mobile (optional but validated if filled)
      var altMob = form.querySelector('[name="alternate_mobile"]');
      if (altMob && altMob.value && !/^[6-9]\d{9}$/.test(altMob.value)) {
        showError(altMob, 'Enter a valid 10-digit mobile number.');
      }

      // PAN (optional but validated if filled)
      var pan = form.querySelector('[name="pan_number"]');
      if (pan && pan.value && !/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(pan.value.toUpperCase())) {
        showError(pan, 'Enter a valid PAN (e.g., ABCDE1234F).');
      }

      // Aadhaar (optional but validated if filled)
      var aadh = form.querySelector('[name="aadhaar_number"]');
      if (aadh && aadh.value && !/^\d{12}$/.test(aadh.value)) {
        showError(aadh, 'Aadhaar must be exactly 12 digits.');
      }

      // 10th percentage
      var tenth = form.querySelector('[name="tenth_percentage"]');
      if (tenth && tenth.value !== '') {
        var v = parseFloat(tenth.value);
        if (isNaN(v) || v < 0 || v > 100) showError(tenth, 'Percentage must be between 0 and 100.');
      }

      // OGPA
      var ogpa = form.querySelector('[name="ogpa"]');
      if (ogpa && ogpa.value !== '') {
        var g = parseFloat(ogpa.value);
        if (isNaN(g) || g < 0 || g > 10) showError(ogpa, 'OGPA must be between 0.00 and 10.00.');
      }

      // TPC checkbox
      var tpc = form.querySelector('[name="tpc_acceptance"]');
      if (tpc && !tpc.checked) {
        showError(tpc, 'You must accept the TPC rules to submit.');
      }

      if (!valid) {
        e.preventDefault();
        // Expand sections with errors
        document.querySelectorAll('.is-invalid').forEach(function (el) {
          var sec = el.closest('.section-body');
          if (sec && sec.classList.contains('collapsed')) {
            sec.classList.remove('collapsed');
            var h = sec.previousElementSibling;
            if (h) h.classList.remove('collapsed');
          }
        });
        // Scroll to first error
        var first = document.querySelector('.is-invalid');
        if (first) { first.scrollIntoView({ behavior: 'smooth', block: 'center' }); first.focus(); }
      }
    });
  }

  // Reset confirmation
  var resetBtn = document.querySelector('.btn-reset');
  if (resetBtn) {
    resetBtn.addEventListener('click', function (e) {
      if (!confirm('Are you sure you want to reset all fields?')) {
        e.preventDefault();
      }
    });
  }
});
