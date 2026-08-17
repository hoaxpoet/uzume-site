const legacyRoutes = {
  taxonomy: './foundations/#taxonomy',
  color: './foundations/#color',
  typography: './foundations/#typography',
  spacing: './foundations/#spacing',
  accessibility: './foundations/#accessibility',
  'component-overview': './components/#component-overview',
  button: './components/#button',
  'icon-button': './components/#icon-button',
  link: './components/#link',
  banner: './components/#banner',
  'definition-list': './components/#definition-list',
  'media-frame': './components/#media-frame',
  'preset-card': './components/#preset-card',
  'site-header': './patterns/#site-header',
  'download-decision': './patterns/#download-decision',
  'trust-explanation': './patterns/#trust-explanation',
  'preset-gallery': './patterns/#preset-gallery',
  'contributor-invitation': './patterns/#contributor-invitation',
  'native-census': './native/controls/#native-census',
  'native-controls': './native/controls/#native-controls',
  'native-migration': './native/components/#native-migration',
  swiftui: './native/components/#swiftui',
  'native-screens': './native/screens/#native-screens',
};

if (document.body.dataset.route === 'overview') {
  const legacyTarget = legacyRoutes[location.hash.slice(1)];
  if (legacyTarget) location.replace(legacyTarget);
}

const menu = document.querySelector('.ds-menu');
const sidebar = document.querySelector('.ds-sidebar');
const filter = document.querySelector('#ds-filter');
const navLinks = [...document.querySelectorAll('.ds-sidebar a[href^="#"]')];

menu?.addEventListener('click', () => {
  const open = sidebar.dataset.open !== 'true';
  sidebar.dataset.open = String(open);
  menu.setAttribute('aria-expanded', String(open));
  if (open) filter?.focus();
});

sidebar?.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape' || sidebar.dataset.open !== 'true') return;
  sidebar.dataset.open = 'false';
  menu?.setAttribute('aria-expanded', 'false');
  menu?.focus();
});

navLinks.forEach((link) => link.addEventListener('click', () => {
  sidebar.dataset.open = 'false';
  menu?.setAttribute('aria-expanded', 'false');
}));

filter?.addEventListener('input', () => {
  const query = filter.value.trim().toLowerCase();
  document.querySelectorAll('.ds-sidebar [data-filter]').forEach((link) => {
    link.hidden = Boolean(query) && !`${link.textContent} ${link.dataset.filter}`.toLowerCase().includes(query);
  });
});

const observed = navLinks
  .map((link) => ({ link, target: document.querySelector(link.getAttribute('href')) }))
  .filter((item) => item.target);

const observer = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  navLinks.forEach((link) => link.removeAttribute('aria-current'));
  observed.find((item) => item.target === visible.target)?.link.setAttribute('aria-current', 'location');
}, { rootMargin: '-20% 0px -70% 0px', threshold: [0, 0.25, 0.75] });

observed.forEach((item) => observer.observe(item.target));
