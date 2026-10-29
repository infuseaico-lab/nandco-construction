// Nandco Construction: free estimate ad landing page (free-estimate.html).

// Reveal once when an element enters the viewport. Never replays, never leaves content hidden.
(() => {
  const targets = document.querySelectorAll('[data-reveal], .run__row, .gallery__grid');
  document.querySelectorAll('.moment, .shot').forEach((el) => el.style.setProperty('--n', [...el.parentNode.children].indexOf(el)));
  if (!('IntersectionObserver' in window)) { targets.forEach((el) => el.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
  targets.forEach((el) => io.observe(el));
  window.addEventListener('load', () => setTimeout(() => {
    targets.forEach((el) => { const r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) el.classList.add('is-in'); });
  }, 2500));
})();

// Project quiz: one step at a time; a tap moves on, Next serves the keyboard.
// The answers are summed up at the end and carried into the booking form.
(() => {
  const pick = document.getElementById('pick');
  if (!pick) return;
  const SCOPE = { upgrade: 'an upgrade', rebuild: 'fire or damage rebuild', space: 'more space' };
  const LAYOUT = { kb: 'Kitchen or bath', home: 'Whole home', adu: 'ADU or addition', new: 'New or custom home' };
  const SIZE = { s: 'start as soon as possible', m: 'start in 1 to 3 months', l: 'just exploring' };
  const NAMES = ['layout', 'scope', 'size'];
  const $ = (id) => document.getElementById(id);
  const wiz = pick.closest('.wiz');
  const steps = [...wiz.querySelectorAll('.wiz__step')];
  const back = $('wiz-back'), next = $('wiz-next');
  let at = 0, pointer = false;

  const show = (i, dir = 1) => {
    at = i;
    wiz.classList.toggle('is-back', dir < 0);
    wiz.classList.toggle('is-done', i >= 3);
    wiz.classList.toggle('is-form', i === 4);
    steps.forEach((el, n) => el.classList.toggle('is-on', n === i));
    $('wiz-count').textContent = i < 3 ? `Step ${i + 1} of 4` : i === 3 ? 'Your project' : 'Step 4 of 4: your details';
    $('wiz-fill').style.width = `${((i + 1) / 5) * 100}%`;
    back.hidden = i === 0;
    next.disabled = i < 3 && !pick.elements[NAMES[i]].value;
  };
  const summary = () => {
    const v = Object.fromEntries(new FormData(pick));
    if (!(v.layout && v.scope && v.size)) return '';
    return `${LAYOUT[v.layout]}, ${SCOPE[v.scope]}, ${SIZE[v.size]}`;
  };
  const update = () => {
    const what = summary();
    const mine = $('book-mine');
    mine.hidden = !what;
    mine.firstChild.textContent = `Your project: ${what}. `;
    $('f-estimate').value = what;
    if (pick.elements.layout.value) $('f-type').value = pick.elements.scope.value === 'rebuild' ? 'rebuild' : pick.elements.layout.value;
    const v = Object.fromEntries(new FormData(pick));
    const SIZEFULL = { s: 'As soon as possible', m: 'In 1 to 3 months', l: 'Just exploring' };
    const FULL = { upgrade: 'An upgrade', rebuild: 'Fire or damage rebuild', space: 'More space' };
    $('sum-layout').textContent = v.layout ? LAYOUT[v.layout] : 'Not chosen';
    $('sum-scope').textContent = v.scope ? FULL[v.scope] : 'Not chosen';
    $('sum-size').textContent = v.size ? SIZEFULL[v.size] : 'Not chosen';
    if (v.layout) $('wiz-pic').src = $('wiz-pic2').src = pick.querySelector(`input[name=layout][value="${v.layout}"] + img`).getAttribute('src');
    $('recap-what').textContent = what || 'Not chosen yet';
    $('q-kitchen').value = what;
    $('q-project').value = v.layout ? LAYOUT[v.layout] : '';
  };

  pick.addEventListener('pointerdown', () => { pointer = true; });
  pick.addEventListener('keydown', () => { pointer = false; });
  pick.addEventListener('change', () => {
    update();
    next.disabled = false;
    if (pointer && at < 3) setTimeout(() => show(at + 1), 320);
  });
  next.addEventListener('click', () => {
    show(at + 1);
    const first = steps[at].querySelector('input, a');
    if (first) first.focus({ preventScroll: true });
  });
  back.addEventListener('click', () => show(at - 1, -1));
  $('wiz-again').addEventListener('click', () => { pick.reset(); update(); show(0, -1); });
  $('out-book').addEventListener('click', () => { show(4); setTimeout(() => $('q-name').focus({ preventScroll: true }), 350); });
  $('wiz-edit').addEventListener('click', () => show(0, -1));
  update();
  show(0);
})();

// Drag row: back and forward buttons, and the bar that shows how far the row has scrolled.
(() => {
  const row = document.getElementById('run-row');
  if (!row) return;
  const fill = document.getElementById('run-fill');
  const [back, fwd] = document.querySelectorAll('[data-run]');
  const step = () => (row.querySelector('.moment')?.getBoundingClientRect().width || 300) + 32;
  const sync = () => {
    const max = row.scrollWidth - row.clientWidth;
    const seen = row.clientWidth / row.scrollWidth;
    const at = max > 0 ? row.scrollLeft / max : 1;
    fill.style.width = `${(seen + (1 - seen) * at) * 100}%`;
    back.disabled = row.scrollLeft <= 2;
    fwd.disabled = row.scrollLeft >= max - 2;
  };
  [back, fwd].forEach((b) => b.addEventListener('click', () => row.scrollBy({ left: Number(b.dataset.run) * step(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' })));
  row.addEventListener('scroll', sync, { passive: true });
  addEventListener('resize', sync);
  sync();
})();

// Request forms (the quiz's and the booking card's): check the required fields, then post to the
// endpoint if one is set, otherwise open an email to the office with everything filled in.
const LABELS = { name: 'Name', phone: 'Phone', email: 'Email', zip: 'ZIP', project: 'Project', budget: 'Budget', start: 'Start', summary: 'Answers' };
document.querySelectorAll('#book-form, #quiz-form').forEach((form) => {
  const status = form.querySelector('.form__status');
  const send = form.querySelector('[type=submit]');
  if (form.elements.start) {
    const today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
    form.elements.start.min = today.toISOString().slice(0, 10);
  }
  const checks = [
    [form.elements.name, (v) => v.trim().length > 1],
    [form.elements.phone, (v) => v.replace(/\D/g, '').length >= 10],
    [form.elements.email, (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())],
    [form.elements.zip, (v) => /^\d{5}$/.test(v.trim())],
  ];
  const mark = (input, ok) => {
    input.setAttribute('aria-invalid', String(!ok));
    document.getElementById(input.getAttribute('aria-describedby')).hidden = ok;
  };
  checks.forEach(([input, ok]) => {
    input.addEventListener('blur', () => { if (input.value) mark(input, ok(input.value)); });
    input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') mark(input, ok(input.value)); });
  });
  const say = (text, kind) => { status.textContent = text; status.className = 'form__status field--wide' + (kind ? ` is-${kind}` : ''); };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const bad = checks.filter(([input, ok]) => { const good = ok(input.value); mark(input, good); return !good; });
    if (bad.length) { bad[0][0].focus(); say('Please check the highlighted field.', 'err'); return; }
    const data = Object.fromEntries(new FormData(form));
    const endpoint = form.dataset.endpoint;
    if (endpoint) {
      send.setAttribute('aria-busy', 'true'); send.disabled = true; say('Sending…');
      try {
        const r = await fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) });
        if (!r.ok) throw new Error(r.status);
        form.reset();
        say(`Thank you, ${data.name.split(' ')[0]}. We'll call you at ${data.phone} within one business day.`, 'ok');
      } catch {
        say('That did not go through. Please call (213) 444-6596.', 'err');
      } finally { send.removeAttribute('aria-busy'); send.disabled = false; }
      return;
    }
    const project = form.elements.project;
    if (project && project.tagName === 'SELECT') data.project = project.value ? project.selectedOptions[0].textContent : '';
    const body = ['Free estimate request', ...Object.entries(LABELS).filter(([k]) => data[k]).map(([k, label]) => `${label}: ${data[k]}`)].join('\n');
    location.href = `mailto:hello@nandcoconstruction.com?subject=${encodeURIComponent(`Free estimate request: ${data.name}, ${data.zip}`)}&body=${encodeURIComponent(body)}`;
    say('Your email app should open with the details ready to send. If it does not, call (213) 444-6596.', 'ok');
  });
});

// Phone dock: shown once the hero is out of sight, hidden while the booking card is on screen.
(() => {
  const dock = document.querySelector('[data-dock]');
  const hero = document.querySelector('.hero');
  const book = document.getElementById('book');
  if (!dock || !hero || !book || !('IntersectionObserver' in window)) return;
  dock.hidden = false;
  let pastHero = false, onBook = false;
  const set = () => dock.classList.toggle('is-on', pastHero && !onBook);
  new IntersectionObserver(([e]) => { pastHero = !e.isIntersecting; set(); }, { threshold: 0.15 }).observe(hero);
  new IntersectionObserver(([e]) => { onBook = e.isIntersecting; set(); }, { threshold: 0.2 }).observe(book);
})();
