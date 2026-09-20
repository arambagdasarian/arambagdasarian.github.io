(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const dialog = document.querySelector('#research-video-dialog');
  const player = dialog?.querySelector('video');
  const refreshPreviews = [];
  let returnToPreview;
  if (dialog && typeof dialog.showModal === 'function') {
    const restorePage = () => {
      if (dialog.open) return;
      player.pause();
      document.documentElement.classList.remove('video-dialog-open');
      const restoreFocus = returnToPreview;
      returnToPreview = undefined;
      restoreFocus?.();
      refreshPreviews.forEach((refresh) => refresh());
    };
    const closePlayer = () => {
      player.pause();
      dialog.close();
      restorePage();
    };
    dialog.addEventListener('close', restorePage);
    dialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closePlayer();
    });
    dialog.querySelector('form').addEventListener('submit', (event) => {
      event.preventDefault();
      closePlayer();
    });
    dialog.addEventListener('click', (event) => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) {
        closePlayer();
      }
    });
  }
  document.querySelectorAll('.research-visual').forEach((preview) => {
    const video = preview.querySelector('video');
    let hovered = false;
    let focused = false;
    let visible = true;
    let dismissed = false;
    const update = () => {
      const active = (hovered || focused) && visible && !dismissed && !dialog?.open && !document.hidden && !reducedMotion.matches;
      if (active) {
        video.play().catch(() => {});
      } else {
        video.pause();
        preview.classList.remove('is-playing');
      }
    };
    video.addEventListener('playing', () => {
      if (!video.paused) preview.classList.add('is-playing');
    });
    video.addEventListener('pause', () => preview.classList.remove('is-playing'));
    const activate = (restart = false) => {
      dismissed = false;
      preview.classList.remove('is-dismissed');
      if (restart && video.hasAttribute('data-restart-on-hover') && !reducedMotion.matches) {
        video.currentTime = 0;
      }
      update();
    };
    const dismiss = () => {
      dismissed = true;
      preview.classList.add('is-dismissed');
      update();
    };
    refreshPreviews.push(update);
    if (preview.hasAttribute('data-video-dialog') && dialog && typeof dialog.showModal === 'function') {
      preview.setAttribute('aria-haspopup', 'dialog');
      preview.setAttribute('aria-controls', dialog.id);
      preview.addEventListener('click', (event) => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        dismiss();
        dialog.querySelector('#research-video-title').textContent = preview.getAttribute('aria-label');
        const caption = dialog.querySelector('#research-video-caption');
        caption.textContent = preview.dataset.videoCaption || '';
        caption.hidden = !caption.textContent;
        if (caption.textContent) dialog.setAttribute('aria-describedby', caption.id);
        else dialog.removeAttribute('aria-describedby');
        player.setAttribute('aria-label', preview.getAttribute('aria-label'));
        player.poster = video.poster;
        player.src = video.querySelector('source').src;
        returnToPreview = () => {
          preview.focus({ preventScroll: true });
          dismiss();
        };
        dialog.showModal();
        document.documentElement.classList.add('video-dialog-open');
        refreshPreviews.forEach((refresh) => refresh());
        player.play().catch(() => {});
      });
    }
    preview.addEventListener('mouseenter', () => { hovered = true; activate(true); });
    preview.addEventListener('mouseleave', () => { hovered = false; update(); });
    preview.addEventListener('focus', () => { focused = true; activate(!hovered); });
    preview.addEventListener('blur', () => { focused = false; update(); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && (hovered || focused)) {
        dismiss();
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
