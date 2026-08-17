const menu = document.querySelector('.menu-button');
const nav = document.querySelector('.chapter-nav');

const setCurrentChapter = () => {
  const hash = window.location.hash || '#top';
  nav.querySelectorAll('a').forEach((link) => {
    if (link.getAttribute('href') === hash) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
};

menu.addEventListener('click', () => {
  const expanded = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-expanded', String(!expanded));
  nav.classList.toggle('open', !expanded);
  if (!expanded) nav.querySelector('a').focus();
});

nav.addEventListener('click', (event) => {
  if (event.target.matches('a')) {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
    setCurrentChapter();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && nav.classList.contains('open')) {
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.focus();
  }
});

window.addEventListener('hashchange', setCurrentChapter);
setCurrentChapter();

const demo = document.querySelector('#motion-demo');
demo.addEventListener('click', () => {
  demo.classList.remove('play');
  requestAnimationFrame(() => requestAnimationFrame(() => demo.classList.add('play')));
});
