/* Local math, native auto-animate, and fragment-aware video lifecycle. */
(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  renderMathInElement(document.querySelector('.slides'), {
    delimiters: [
      { left: '\\[', right: '\\]', display: true },
      { left: '\\(', right: '\\)', display: false },
    ],
    throwOnError: false,
    strict: 'warn',
  });

  const activeVideos = new Set();
  function visible(video) {
    const current = Reveal.getCurrentSlide();
    if (!current || !current.contains(video)) return false;
    let element = video;
    while (element && element !== current) {
      if (element.classList.contains('fragment') && !element.classList.contains('visible')) return false;
      element = element.parentElement;
    }
    return true;
  }
  function label(video) {
    const button = document.querySelector(`[data-video-toggle="${video.id}"]`);
    if (button) button.textContent = video.paused ? 'Play animation' : 'Pause animation';
  }
  function reset(video) {
    video.pause();
    video.currentTime = 0;
    label(video);
  }
  function syncVideos() {
    document.querySelectorAll('video[data-fragment-video]').forEach(video => {
      if (!visible(video)) {
        reset(video);
        activeVideos.delete(video);
      } else if (!activeVideos.has(video)) {
        activeVideos.add(video);
        reset(video);
        if (!reducedMotion.matches) video.play().catch(() => label(video));
      }
    });
  }
  document.querySelectorAll('video[data-fragment-video]').forEach(video => {
    video.addEventListener('play', () => label(video));
    video.addEventListener('pause', () => label(video));
  });
  document.querySelectorAll('[data-video-toggle]').forEach(button => {
    button.addEventListener('click', () => {
      const video = document.getElementById(button.dataset.videoToggle);
      if (!visible(video)) return;
      if (video.paused) video.play().catch(() => label(video)); else video.pause();
    });
  });
  Reveal.initialize({
    width: 960, height: 700, margin: .05, center: false,
    hash: true, fragmentInURL: true, slideNumber: true,
    transition: reducedMotion.matches ? 'none' : 'slide',
    autoAnimate: !reducedMotion.matches,
    autoAnimateDuration: .65,
    plugins: [RevealHighlight],
  }).then(() => {
    syncVideos();
    // Exposed as a readiness promise for screenshot tools, not a build step.
    window.deckReady = document.fonts.ready;
  });
  ['ready', 'slidechanged', 'fragmentshown', 'fragmenthidden'].forEach(event => Reveal.on(event, syncVideos));
  reducedMotion.addEventListener('change', () => {
    Reveal.configure({ autoAnimate: !reducedMotion.matches, transition: reducedMotion.matches ? 'none' : 'slide' });
    if (reducedMotion.matches) document.querySelectorAll('video').forEach(video => video.pause());
  });
})();
