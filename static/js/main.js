// ===== MAIN JS =====
document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss toast messages
  document.querySelectorAll('.toast').forEach(function (toast) {
    setTimeout(function () {
      toast.style.animation = 'slideOutRight .3s ease forwards';
      setTimeout(function () { toast.remove(); }, 300);
    }, 4000);
  });
  document.querySelectorAll('.toast-close').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.closest('.toast');
      t.style.animation = 'slideOutRight .3s ease forwards';
      setTimeout(function () { t.remove(); }, 300);
    });
  });
});

function showToast(message, type) {
  type = type || 'success';
  var icons = { success: '✅', error: '❌', warning: '⚠️' };
  var container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  var toast = document.createElement('div');
  toast.className = 'toast ' + type;
  toast.innerHTML = '<span class="toast-icon">' + (icons[type] || '✅') + '</span>' +
    '<span class="toast-msg">' + message + '</span>' +
    '<span class="toast-close">✕</span>';
  container.appendChild(toast);
  toast.querySelector('.toast-close').addEventListener('click', function () {
    toast.remove();
  });
  setTimeout(function () { toast.remove(); }, 5000);
}
