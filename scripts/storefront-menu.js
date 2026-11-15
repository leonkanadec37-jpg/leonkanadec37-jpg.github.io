(() => {
  function initStorefrontMenu() {
    const trigger = document.getElementById('burger') || document.querySelector('.storefront-menu-toggle');
    if (!trigger) return;
    const header = trigger.closest('.storefront-header') || trigger.closest('header') || document.body;
    const menuId = trigger.getAttribute('aria-controls') || 'storefront-menu';
    const menu = document.getElementById(menuId) || document.getElementById('storefront-menu');
    if (!menu) return;
    const backdrop = header.querySelector('.storefront-menu-backdrop') || document.querySelector('.storefront-menu-backdrop');
    const desktop = window.matchMedia('(min-width: 769px)');

    let savedScrollY = 0;

    function updateBadges() {
      try {
        const raw = localStorage.getItem('livi_cart_v3') || '[]';
        const items = JSON.parse(raw);
        const count = items.reduce((sum, item) => sum + (Number(item.qty) || 1), 0);
        const badges = document.querySelectorAll('.cart-badge');
        badges.forEach(b => {
          if (count > 0) {
            b.textContent = String(count);
            b.style.display = 'inline-flex';
          } else {
            b.style.display = 'none';
          }
        });
      } catch (e) {}
    }

    function setOpen(open, returnFocus = false, isKeyboard = false) {
      if (!open && returnFocus) {
        try { trigger.focus(); } catch(e) {}
      }
      trigger.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
      if (backdrop) backdrop.hidden = !open;
      if (open) {
        savedScrollY = window.scrollY || window.pageYOffset || 0;
        document.documentElement.classList.add('drawer-open');
        document.body.classList.add('drawer-open');
        updateBadges();
        const materials = menu.querySelector('.storefront-materials');
        if (materials) materials.open = desktop.matches;
        if (isKeyboard) {
          try {
            const firstLink = menu.querySelector('.smm-close-btn') || menu.querySelector('a');
            firstLink?.focus({ preventScroll: true });
          } catch(e) {}
        }
      } else {
        document.documentElement.classList.remove('drawer-open');
        document.body.classList.remove('drawer-open');
        window.scrollTo(0, savedScrollY);
      }
    }

    trigger.addEventListener('click', event => {
      const isKeyboard = event.detail === 0;
      setOpen(menu.hidden, isKeyboard, isKeyboard);
    });

    // Close button inside mobile menu
    const closeBtns = menu.querySelectorAll('.smm-close-btn, [data-menu-close]');
    closeBtns.forEach(btn => {
      btn.addEventListener('click', () => setOpen(false, true, true));
    });

    if (backdrop) {
      backdrop.addEventListener('click', () => setOpen(false, false, false));
    }

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !menu.hidden) {
        event.preventDefault();
        setOpen(false, true, true);
      }
    });

    document.addEventListener('focusin', event => {
      if (!menu.hidden && !header.contains(event.target) && !menu.contains(event.target)) {
        setOpen(false, false, false);
      }
    });

    desktop.addEventListener('change', () => {
      if (!menu.hidden) setOpen(false, false, false);
    });

    updateBadges();
    window.addEventListener('storage', updateBadges);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStorefrontMenu);
  } else {
    initStorefrontMenu();
  }
})();
