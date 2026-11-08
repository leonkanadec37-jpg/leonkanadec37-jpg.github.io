(() => {
  const header = document.querySelector('.storefront-header');
  const trigger = header.querySelector('.storefront-menu-toggle');
  const menu = document.getElementById(trigger.getAttribute('aria-controls'));
  const backdrop = header.querySelector('.storefront-menu-backdrop');
  const materials = menu.querySelector('.storefront-materials');
  const desktop = window.matchMedia('(min-width: 769px)');

  let savedScrollY = 0;

  function setOpen(open, returnFocus = false) {
    if (!open && returnFocus) trigger.focus();
    trigger.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    backdrop.hidden = !open;
    if (open) {
      savedScrollY = window.scrollY || window.pageYOffset || 0;
      document.documentElement.classList.add('drawer-open');
      document.body.classList.add('drawer-open');
      materials.open = desktop.matches;
      menu.querySelector('a').focus({ preventScroll: true });
    } else {
      document.documentElement.classList.remove('drawer-open');
      document.body.classList.remove('drawer-open');
      window.scrollTo(0, savedScrollY);
    }
  }

  trigger.addEventListener('click', () => setOpen(menu.hidden));
  backdrop.addEventListener('click', () => setOpen(false, true));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !menu.hidden) {
      event.preventDefault();
      setOpen(false, true);
    }
  });
  document.addEventListener('focusin', event => {
    if (!menu.hidden && !header.contains(event.target)) setOpen(false);
  });
  desktop.addEventListener('change', () => {
    if (!menu.hidden) setOpen(false, true);
  });
})();
