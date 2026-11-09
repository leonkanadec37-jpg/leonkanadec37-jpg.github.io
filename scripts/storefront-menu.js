(() => {
  const header = document.querySelector('.storefront-header');
  const trigger = header.querySelector('.storefront-menu-toggle');
  const menu = document.getElementById(trigger.getAttribute('aria-controls'));
  const backdrop = header.querySelector('.storefront-menu-backdrop');
  const materials = menu.querySelector('.storefront-materials');
  const desktop = window.matchMedia('(min-width: 769px)');

  let savedScrollY = 0;

  function setOpen(open, returnFocus = false, isKeyboard = false) {
    if (!open && returnFocus && isKeyboard) {
      try { trigger.focus(); } catch(e) {}
    }
    trigger.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
    backdrop.hidden = !open;
    if (open) {
      savedScrollY = window.scrollY || window.pageYOffset || 0;
      document.documentElement.classList.add('drawer-open');
      document.body.classList.add('drawer-open');
      materials.open = desktop.matches;
      if (isKeyboard) {
        try { menu.querySelector('a')?.focus({ preventScroll: true }); } catch(e) {}
      }
    } else {
      document.documentElement.classList.remove('drawer-open');
      document.body.classList.remove('drawer-open');
      window.scrollTo(0, savedScrollY);
    }
  }

  trigger.addEventListener('click', event => {
    // Keyboard activation (Enter/Space) has event.detail === 0. Tap / mouse click has event.detail >= 1.
    const isKeyboard = event.detail === 0;
    setOpen(menu.hidden, isKeyboard, isKeyboard);
  });
  backdrop.addEventListener('click', () => setOpen(false, false, false));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !menu.hidden) {
      event.preventDefault();
      setOpen(false, true, true);
    }
  });
  document.addEventListener('focusin', event => {
    if (!menu.hidden && !header.contains(event.target)) setOpen(false, false, false);
  });
  desktop.addEventListener('change', () => {
    if (!menu.hidden) setOpen(false, false, false);
  });
})();
