(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.research-visual').forEach((preview) => {
    const video = preview.querySelector('video');
    let hovered = false;
    let focused = false;
    let visible = true;
    let dismissed = false;
    const update = () => {
      const active = (hovered || focused) && visible && !dismissed && !document.hidden && !reducedMotion.matches;
      if (active) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    };
    const activate = () => {
      dismissed = false;
      preview.classList.remove('is-dismissed');
      update();
    };
    preview.addEventListener('mouseenter', () => { hovered = true; activate(); });
    preview.addEventListener('mouseleave', () => { hovered = false; update(); });
    preview.addEventListener('focus', () => { focused = true; activate(); });
    preview.addEventListener('blur', () => { focused = false; update(); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && (hovered || focused)) {
        dismissed = true;
        preview.classList.add('is-dismissed');
        update();
      }
    });
    reducedMotion.addEventListener('change', update);
    document.addEventListener('visibilitychange', update);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        update();
      }).observe(preview);
    }
  });
})();
