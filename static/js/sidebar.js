
if (window.lucide) { lucide.createIcons(); }

// ── Date badge
document.getElementById('today-date').textContent =
  new Date().toLocaleDateString('id-ID', { weekday:'long', day:'numeric', month:'long', year:'numeric' });

// ── Sidebar toggle (default open)
const btn     = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');
const mainEl  = document.getElementById('mainContent');
let isOpen = true;
sidebar.classList.add('open');
mainEl.classList.add('shifted');
btn.classList.add('open');

btn.addEventListener('click', () => {
  isOpen = !isOpen;
  sidebar.classList.toggle('open', isOpen);
  mainEl.classList.toggle('shifted', isOpen);
  btn.classList.toggle('open', isOpen);
});

// ── Nav active state
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
  });
});
