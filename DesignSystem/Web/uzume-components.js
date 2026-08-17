/** Behavior for the one current web component with a scripted state. */

export function setUzumeBusy(control, busy, label = 'Working') {
  if (!(control instanceof HTMLButtonElement)) {
    throw new TypeError('setUzumeBusy expects a button element.');
  }

  const wasBusy = control.getAttribute('aria-busy') === 'true';
  if (busy && !wasBusy) {
    control.dataset.uzWasDisabled = String(control.disabled);
    if (control.hasAttribute('aria-label')) control.dataset.uzAriaLabel = control.getAttribute('aria-label');
    control.dataset.uzLabel = control.getAttribute('aria-label') || control.textContent.trim();
  }

  const existing = control.querySelector('.uz-button__spinner');

  if (busy) {
    control.setAttribute('aria-busy', 'true');
    control.disabled = true;

    if (!existing) {
      const spinner = document.createElement('span');
      spinner.className = 'uz-button__spinner';
      spinner.setAttribute('aria-hidden', 'true');
      control.prepend(spinner);
      control.setAttribute('aria-label', `${control.dataset.uzLabel}, ${label}`);
    }
    return;
  }

  control.removeAttribute('aria-busy');
  existing?.remove();

  if ('uzWasDisabled' in control.dataset) {
    if (control.dataset.uzAriaLabel) control.setAttribute('aria-label', control.dataset.uzAriaLabel);
    else control.removeAttribute('aria-label');
    control.disabled = control.dataset.uzWasDisabled === 'true';
    delete control.dataset.uzAriaLabel;
    delete control.dataset.uzLabel;
    delete control.dataset.uzWasDisabled;
  }
}
