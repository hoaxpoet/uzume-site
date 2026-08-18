import { setUzumeBusy } from './uzume-components.js?v=15';

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
const mobileNavigation = window.matchMedia('(max-width: 900px)');
const themePreference = window.matchMedia('(prefers-color-scheme: light)');
const themeModes = ['system', 'dark', 'light'];
const routeName = {
  overview: 'Inventory',
  foundations: 'Foundations',
  components: 'Components',
  patterns: 'Patterns',
  'native-controls': 'Controls',
  'native-components': 'Components',
  'native-screens': 'Screens',
}[document.body.dataset.route] || 'Design system';

const mobileContext = document.createElement('span');
mobileContext.className = 'ds-mobile-context';
mobileContext.textContent = routeName;
mobileContext.title = routeName;
document.querySelector('.ds-version')?.after(mobileContext);

const catalogueRoot = new URL('./', import.meta.url);
const systemRoutes = [
  ['overview', 'Inventory', 'index.html'],
  ['foundations', 'Foundations', 'foundations/'],
  ['components', 'Web components', 'components/'],
  ['patterns', 'Web patterns', 'patterns/'],
  ['native-controls', 'macOS controls', 'native/controls/'],
  ['native-components', 'macOS components', 'native/components/'],
  ['native-screens', 'Application screens', 'native/screens/'],
];
const mobileLayers = document.createElement('section');
mobileLayers.className = 'ds-mobile-layers';
mobileLayers.innerHTML = `<h2>System layers</h2>${systemRoutes.map(([route, label, href]) => `<a href="${new URL(href, catalogueRoot)}"${document.body.dataset.route === route ? ' aria-current="page"' : ''}>${label}</a>`).join('')}`;
sidebar?.querySelector('nav')?.append(mobileLayers);

const navigationScrim = document.createElement('div');
navigationScrim.className = 'ds-nav-scrim';
navigationScrim.hidden = true;
navigationScrim.setAttribute('aria-hidden', 'true');
sidebar?.after(navigationScrim);

document.querySelectorAll('.ds-table').forEach((table) => {
  const headers = [...table.querySelectorAll('thead th')].map((header) => header.textContent.trim());
  table.querySelectorAll('thead th').forEach((header) => header.setAttribute('scope', 'col'));
  table.querySelectorAll('tbody tr').forEach((row) => {
    [...row.children].forEach((cell, index) => {
      if (cell.tagName === 'TH') cell.setAttribute('scope', 'row');
      if (index === 0 || cell.querySelector('.ds-cell-label')) return;
      const label = document.createElement('span');
      label.className = 'ds-cell-label';
      label.setAttribute('aria-hidden', 'true');
      label.textContent = headers[index] || 'Value';
      cell.prepend(label);
    });
  });
  table.dataset.adapted = 'true';
});

function storedTheme() {
  try {
    const value = localStorage.getItem('uzume-catalogue-theme');
    return themeModes.includes(value) ? value : 'system';
  } catch {
    return 'system';
  }
}

let themeMode = storedTheme();
const themeButton = document.createElement('button');
themeButton.type = 'button';
themeButton.className = 'ds-theme-toggle';
themeButton.innerHTML = '<span>Appearance</span><strong data-theme-label></strong>';
document.querySelector('.ds-toplinks')?.before(themeButton);

function applyTheme(mode, persist = true) {
  themeMode = mode;
  if (mode === 'system') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.dataset.theme = mode;
  if (persist) {
    try { localStorage.setItem('uzume-catalogue-theme', mode); } catch { /* Storage may be unavailable on file URLs. */ }
  }
  const resolved = mode === 'system' ? (themePreference.matches ? 'light' : 'dark') : mode;
  const next = themeModes[(themeModes.indexOf(mode) + 1) % themeModes.length];
  themeButton.querySelector('[data-theme-label]').textContent = mode === 'system' ? `System · ${resolved}` : mode;
  themeButton.setAttribute('aria-label', `Appearance: ${mode}, currently ${resolved}. Change to ${next}.`);
}

applyTheme(themeMode, false);
themeButton.addEventListener('click', () => applyTheme(themeModes[(themeModes.indexOf(themeMode) + 1) % themeModes.length]));
themePreference.addEventListener('change', () => {
  if (themeMode === 'system') applyTheme('system', false);
});

function setSidebarInteractive(interactive) {
  if (!sidebar) return;
  sidebar.toggleAttribute('inert', !interactive);
  sidebar.querySelectorAll('a, button, input').forEach((control) => {
    if (!interactive) {
      if (!control.hasAttribute('data-ds-tabindex')) control.dataset.dsTabindex = control.getAttribute('tabindex') || '';
      control.setAttribute('tabindex', '-1');
      return;
    }
    if (!control.hasAttribute('data-ds-tabindex')) return;
    if (control.dataset.dsTabindex) control.setAttribute('tabindex', control.dataset.dsTabindex);
    else control.removeAttribute('tabindex');
    delete control.dataset.dsTabindex;
  });
}

function closeNavigation({ restoreFocus = false } = {}) {
  if (!sidebar || !menu) return;
  sidebar.dataset.open = 'false';
  menu.setAttribute('aria-expanded', 'false');
  menu.querySelector('.sr-only').textContent = 'Open navigation';
  if (mobileNavigation.matches) {
    setSidebarInteractive(false);
    sidebar.setAttribute('aria-hidden', 'true');
    navigationScrim.hidden = true;
    delete document.body.dataset.navigationOpen;
  }
  if (restoreFocus) menu.focus();
}

function openNavigation() {
  if (!sidebar || !menu) return;
  setSidebarInteractive(true);
  sidebar.removeAttribute('aria-hidden');
  sidebar.dataset.open = 'true';
  menu.setAttribute('aria-expanded', 'true');
  menu.querySelector('.sr-only').textContent = 'Close navigation';
  navigationScrim.hidden = false;
  document.body.dataset.navigationOpen = 'true';
  window.requestAnimationFrame(() => (filter || sidebar.querySelector('a'))?.focus());
}

function syncNavigationMode() {
  if (!sidebar) return;
  if (mobileNavigation.matches) closeNavigation();
  else {
    setSidebarInteractive(true);
    sidebar.removeAttribute('aria-hidden');
    sidebar.dataset.open = 'false';
    navigationScrim.hidden = true;
    delete document.body.dataset.navigationOpen;
    menu?.setAttribute('aria-expanded', 'false');
    if (menu) menu.querySelector('.sr-only').textContent = 'Open navigation';
  }
}

syncNavigationMode();
mobileNavigation.addEventListener('change', syncNavigationMode);

menu?.addEventListener('click', () => {
  if (sidebar.dataset.open === 'true') closeNavigation({ restoreFocus: true });
  else openNavigation();
});

navigationScrim.addEventListener('click', () => closeNavigation({ restoreFocus: true }));

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape' || sidebar?.dataset.open !== 'true') return;
  if (event.target === filter && filter.value) return;
  closeNavigation({ restoreFocus: true });
});

navLinks.forEach((link) => link.addEventListener('click', () => {
  if (mobileNavigation.matches) closeNavigation({ restoreFocus: true });
}));

function applyFilter() {
  if (!filter) return;
  const query = filter.value.trim().toLowerCase();
  const filterable = [...document.querySelectorAll('.ds-sidebar [data-filter]')];
  filterable.forEach((link) => {
    link.hidden = Boolean(query) && !`${link.textContent} ${link.dataset.filter}`.toLowerCase().includes(query);
  });
  const matches = filterable.filter((link) => !link.hidden).length;
  const status = document.querySelector('#ds-filter-status');
  if (status) status.textContent = query ? `${matches} of ${filterable.length} components match “${filter.value.trim()}”.` : `${filterable.length} website components.`;
}

filter?.addEventListener('input', applyFilter);
filter?.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape' || !filter.value) return;
  event.stopPropagation();
  filter.value = '';
  applyFilter();
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

const icons = {
  play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 6 9 6-9 6Z"/></svg>',
  pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6v12M16 6v12"/></svg>',
  mute: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10v4h4l5 4V6L8 10Z"/><path d="m17 9 4 6m0-6-4 6"/></svg>',
  info: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 10v6M12 7h.01"/></svg>',
  success: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/></svg>',
  warning: '<svg viewBox="0 0 32 28" aria-hidden="true"><path d="M16 2 30 26H2Z"/><path d="M16 10v7M16 22h.01"/></svg>',
  danger: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m9 9 6 6m0-6-6 6"/></svg>',
  media: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m8 15 3-3 2 2 3-4 3 5"/></svg>',
};

const bannerCopy = {
  info: ['System audio uses a macOS permission', 'Explain the requirement before sending the listener to System Settings.'],
  success: ['Installation complete', 'Uzume is ready to open.'],
  warning: ['Beta download unavailable', 'A signed and notarized build has not been published yet.'],
  danger: ['Download failed', 'Check the connection and try the download again.'],
};

function renderDemo(demo, state) {
  const preview = demo.querySelector('[data-preview]');
  if (!preview) return;

  if (demo.dataset.demo === 'button') {
    preview.innerHTML = '<button type="button" class="uz-button uz-button--primary">Download beta</button><p class="uz-disabled-reason" data-reason hidden>A signed beta has not been attached.</p>';
    const control = preview.querySelector('button');
    const reason = preview.querySelector('[data-reason]');
    if (state === 'loading') setUzumeBusy(control, true, 'Preparing download');
    if (state === 'disabled') {
      control.disabled = true;
      control.textContent = 'Download unavailable';
      control.setAttribute('aria-describedby', 'button-demo-reason');
      reason.id = 'button-demo-reason';
      reason.hidden = false;
    }
  }

  if (demo.dataset.demo === 'icon-button') {
    const disabled = state === 'disabled';
    const action = disabled ? 'mute' : state;
    const names = { play: 'Play preview', pause: 'Pause preview', mute: 'Mute preview' };
    preview.innerHTML = `<button type="button" class="uz-icon-button" aria-label="${disabled ? 'Mute unavailable' : names[action]}" ${disabled ? 'disabled aria-describedby="icon-demo-reason"' : ''}>${icons[action]}</button><p class="uz-disabled-reason" id="icon-demo-reason" data-reason ${disabled ? '' : 'hidden'}>Playback controls are unavailable until media loads.</p>`;
  }

  if (demo.dataset.demo === 'link') {
    const markup = {
      default: '<a class="uz-link" href="#media-frame">See performance media guidance</a>',
      quiet: '<a class="uz-link uz-link--quiet" href="../native/controls/#native-census">Review the app census</a>',
      unavailable: '<span class="uz-link uz-link--unavailable">Contributor portal unavailable</span>',
    };
    preview.innerHTML = markup[state];
  }

  if (demo.dataset.demo === 'banner') {
    const [title, body] = bannerCopy[state];
    preview.innerHTML = `<section class="uz-banner" data-tone="${state}"><div class="uz-banner__icon">${icons[state]}</div><div class="uz-banner__content"><strong class="uz-banner__title">${title}</strong><p class="uz-banner__body">${body}</p></div></section>`;
  }

  if (demo.dataset.demo === 'definition-list') {
    preview.dataset.demoWidth = state;
  }

  if (demo.dataset.demo === 'media-frame') {
    const content = state === 'available'
      ? '<img src="../../../brand/icon/Uzume-1024.png" alt="First Opening identity artwork" width="1024" height="1024" loading="lazy">'
      : '<div class="uz-media-frame__fallback" role="img" aria-label="Performance preview unavailable"><div><strong>Performance preview unavailable</strong><span>The title and attribution remain available while media is missing.</span></div></div>';
    const title = state === 'available' ? 'First Opening identity artwork' : 'Prepared-performance evidence';
    const meta = state === 'available' ? 'Brand asset — not performance footage' : 'Capture pending';
    preview.innerHTML = `<figure class="uz-media-frame"><div class="uz-media-frame__content">${content}</div><figcaption class="uz-media-frame__caption"><strong>${title}</strong><span class="uz-media-frame__meta">${meta}</span></figcaption></figure>`;
  }

  if (demo.dataset.demo === 'preset-card') {
    const media = state === 'available'
      ? '<img src="../../../brand/icon/Uzume-1024.png" alt="First Opening identity artwork; performance capture pending" width="1024" height="1024" loading="lazy">'
      : `<div>${icons.media}<strong>Preview unavailable</strong><span>The preset remains identifiable without its media.</span></div>`;
    preview.innerHTML = `<figure class="uz-preset-card"><div class="uz-preset-card__media">${media}</div><figcaption class="uz-preset-card__caption"><span class="uz-preset-card__identity"><strong class="uz-preset-card__title">First Opening</strong><span class="uz-preset-card__author">Uzume</span></span><span class="uz-preset-card__status">Certified · 0 flashes/s<br>${state === 'available' ? 'Identity artwork' : 'Capture pending'}</span></figcaption></figure>`;
  }
}

document.querySelectorAll('[data-demo]').forEach((demo) => {
  const active = demo.querySelector('[data-state][aria-pressed="true"]');
  if (active) renderDemo(demo, active.dataset.state);
});

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const fallback = document.createElement('textarea');
  fallback.value = text;
  fallback.setAttribute('readonly', '');
  fallback.className = 'sr-only';
  document.body.append(fallback);
  fallback.select();
  const copied = document.execCommand('copy');
  fallback.remove();
  if (!copied) throw new Error('Copy command was unavailable.');
}

document.addEventListener('click', async (event) => {
  const stateControl = event.target.closest('[data-demo] [data-state]');
  if (stateControl) {
    const demo = stateControl.closest('[data-demo]');
    demo.querySelectorAll('[data-state]').forEach((control) => control.setAttribute('aria-pressed', String(control === stateControl)));
    renderDemo(demo, stateControl.dataset.state);
    return;
  }

  const copyButton = event.target.closest('[data-copy]');
  if (!copyButton) return;
  const source = document.getElementById(copyButton.dataset.copy);
  if (!source) return;
  const status = document.getElementById('ds-copy-status');
  const componentName = copyButton.closest('.ds-component-doc')?.querySelector('h2')?.textContent || 'Component';
  try {
    await copyText(source.textContent);
    copyButton.dataset.copied = 'true';
    copyButton.textContent = 'Copied';
    if (status) status.textContent = `${componentName} markup copied.`;
    window.setTimeout(() => {
      copyButton.removeAttribute('data-copied');
      copyButton.textContent = 'Copy markup';
    }, 1800);
  } catch {
    copyButton.textContent = 'Copy failed';
    if (status) status.textContent = `${componentName} markup could not be copied. Select the code and copy it manually.`;
  }
});
