// ===== DASHBOARD JS =====
document.addEventListener('DOMContentLoaded', function () {
  // Sidebar toggle (desktop)
  var sidebar = document.querySelector('.sidebar');
  var mainContent = document.querySelector('.main-content');
  var sidebarToggle = document.querySelector('.sidebar-toggle');
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('sidebar-collapsed');
      sidebarToggle.classList.toggle('collapsed');
      var icon = sidebarToggle.textContent.trim();
      sidebarToggle.textContent = icon === '◀' ? '▶' : '◀';
    });
  }

  // Mobile hamburger
  var hamburger = document.querySelector('.topbar-hamburger');
  var overlay = document.querySelector('.sidebar-overlay');
  if (hamburger) {
    hamburger.addEventListener('click', function () {
      sidebar.classList.toggle('mobile-open');
      if (overlay) overlay.classList.toggle('visible');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', function () {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('visible');
    });
  }

  // Delete confirmation
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.getAttribute('data-confirm'))) {
        e.preventDefault();
      }
    });
  });

  // Filter toggle
  var filterToggle = document.querySelector('#filterToggle');
  var filterPanel = document.querySelector('#filterPanel');
  if (filterToggle && filterPanel) {
    filterToggle.addEventListener('click', function () {
      var visible = filterPanel.style.display !== 'none';
      filterPanel.style.display = visible ? 'none' : 'block';
      filterToggle.textContent = visible ? '🔽 Show Filters' : '🔼 Hide Filters';
    });
    // Show panel if any filter is active
    var params = new URLSearchParams(window.location.search);
    var filterKeys = ['program', 'branch', 'year', 'gender', 'category', 'blood_group', 'backlog', 'career', 'relocate', 'internship'];
    var hasFilter = filterKeys.some(function (k) { return params.get(k); });
    if (hasFilter && filterPanel) {
      filterPanel.style.display = 'block';
      if (filterToggle) filterToggle.textContent = '🔼 Hide Filters';
    }
  }

  // Auto-dismiss messages
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity .4s';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 400);
    }, 5000);
  });

  // Animate stat values
  document.querySelectorAll('.stat-value[data-target]').forEach(function (el) {
    var target = parseInt(el.getAttribute('data-target'), 10);
    var duration = 1200;
    var step = target / (duration / 16);
    var current = 0;
    var timer = setInterval(function () {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = Math.floor(current).toLocaleString();
    }, 16);
  });

  // Search on Enter
  var searchInput = document.querySelector('#searchInput');
  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        var form = searchInput.closest('form');
        if (form) form.submit();
      }
    });
  }
});
