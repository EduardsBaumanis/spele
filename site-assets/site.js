(() => {
  'use strict';
  const docs = JSON.parse(document.getElementById('document-data').textContent);
  const byId = new Map(docs.map(doc => [doc.id, doc]));
  const links = [...document.querySelectorAll('[data-document]')];
  const search = document.getElementById('document-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const stage = document.getElementById('page-stage');
  const picture = document.getElementById('document-page');
  const select = document.getElementById('page-select');
  const previous = document.getElementById('previous-page');
  const next = document.getElementById('next-page');
  const original = document.getElementById('original-link');
  const download = document.getElementById('download-document');
  const error = document.getElementById('page-error');
  const status = document.getElementById('reader-status');
  const zoomOutput = document.getElementById('zoom-value');
  let active = byId.get('guide');
  let page = 0;
  let zoom = 1;
  let filter = 'all';
  let loading = 0;

  const normalized = text => text.toLocaleLowerCase('lv').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  function filterDocuments() {
    const term = normalized(search.value.trim());
    let count = 0;
    for (const link of links) {
      const doc = byId.get(link.dataset.document);
      link.hidden = (filter !== 'all' && doc.type !== filter) || !normalized(`${doc.title} ${doc.description} ${doc.keywords || ''} ${doc.id}`).includes(term);
      if (!link.hidden) count++;
    }
    document.getElementById('no-documents').hidden = count !== 0;
  }
  function updateZoom(resetPosition = false) {
    const style = getComputedStyle(stage);
    const available = stage.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    picture.style.width = `${Math.max(1, available * zoom)}px`;
    zoomOutput.textContent = `${Math.round(zoom * 100)}%`;
    document.getElementById('zoom-out').disabled = zoom <= .5;
    document.getElementById('zoom-in').disabled = zoom >= 4;
    if (resetPosition) { stage.scrollTop = 0; stage.scrollLeft = 0; }
  }
  function changeZoom(delta) {
    const old = zoom;
    const focusX = (stage.scrollLeft + stage.clientWidth / 2) / old;
    const focusY = (stage.scrollTop + Math.min(stage.clientHeight / 2, picture.clientHeight / 2)) / old;
    zoom = Math.max(.5, Math.min(4, zoom + delta));
    updateZoom();
    stage.scrollLeft = Math.max(0, focusX * zoom - stage.clientWidth / 2);
    stage.scrollTop = Math.max(0, focusY * zoom - stage.clientHeight / 2);
  }
  function renderPage() {
    const token = ++loading;
    error.hidden = true;
    picture.hidden = false;
    stage.setAttribute('aria-busy', 'true');
    picture.alt = `${active.title} — ${page + 1}. lapa no ${active.pages.length}. Visi izmēri cm.`;
    picture.onload = () => { if (token === loading) stage.setAttribute('aria-busy', 'false'); };
    picture.onerror = () => {
      if (token !== loading) return;
      stage.setAttribute('aria-busy', 'false');
      picture.hidden = true;
      error.hidden = false;
    };
    picture.src = active.pages[page];
    if (picture.complete && picture.naturalWidth) stage.setAttribute('aria-busy', 'false');
    select.value = String(page);
    previous.disabled = page === 0;
    next.disabled = page === active.pages.length - 1;
    select.disabled = active.pages.length === 1;
    document.getElementById('page-total').textContent = `/ ${active.pages.length}`;
    status.textContent = `${active.type} · ${page + 1}. lapa no ${active.pages.length} · izmēri cm`;
    updateZoom(true);
  }
  function setDocument(id, scroll = false) {
    const doc = byId.get(id);
    if (!doc) return;
    active = doc; page = 0; zoom = 1;
    document.getElementById('active-title').textContent = doc.title;
    document.getElementById('active-type').textContent = doc.type;
    document.getElementById('active-description').textContent = doc.description;
    original.href = doc.file;
    download.href = doc.file;
    download.download = doc.file.split('/').pop();
    original.setAttribute('aria-label', `Atvērt “${doc.title}” oriģinālu jaunā cilnē`);
    download.setAttribute('aria-label', `Lejupielādēt “${doc.title}”`);
    for (const link of links) {
      if (link.dataset.document === id) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    }
    select.replaceChildren(...doc.pages.map((_, index) => {
      const option = document.createElement('option'); option.value = String(index); option.textContent = `${index + 1}. lapa`; return option;
    }));
    renderPage();
    if (scroll) document.getElementById('dokumenti').scrollIntoView({behavior: 'auto', block: 'start'});
  }
  function pageBy(offset) {
    const target = page + offset;
    if (target >= 0 && target < active.pages.length) { page = target; renderPage(); }
  }
  for (const link of links) link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    history.replaceState(null, '', `#doc-${link.dataset.document}`);
    setDocument(link.dataset.document);
  });
  function fromHash(scroll = false) {
    if (location.hash.startsWith('#doc-')) setDocument(decodeURIComponent(location.hash.slice(5)), scroll);
  }
  addEventListener('hashchange', () => fromHash(true));
  search.addEventListener('input', filterDocuments);
  for (const button of filters) button.addEventListener('click', () => {
    filter = button.dataset.filter;
    for (const item of filters) item.setAttribute('aria-pressed', String(item === button));
    filterDocuments();
  });
  select.addEventListener('change', () => { page = Number(select.value); renderPage(); });
  previous.addEventListener('click', () => pageBy(-1));
  next.addEventListener('click', () => pageBy(1));
  document.getElementById('zoom-in').addEventListener('click', () => changeZoom(.25));
  document.getElementById('zoom-out').addEventListener('click', () => changeZoom(-.25));
  document.getElementById('zoom-fit').addEventListener('click', () => { zoom = 1; updateZoom(true); });
  stage.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.key === '+' || event.key === '=') { event.preventDefault(); changeZoom(.25); }
    else if (event.key === '-') { event.preventDefault(); changeZoom(-.25); }
    else if (event.key === '0') { event.preventDefault(); zoom = 1; updateZoom(true); }
    else if (event.key === 'PageDown' && event.shiftKey) { event.preventDefault(); pageBy(1); }
    else if (event.key === 'PageUp' && event.shiftKey) { event.preventDefault(); pageBy(-1); }
  });
  new ResizeObserver(() => updateZoom()).observe(stage);
  const sections = [...document.querySelectorAll('.guide-text details')];
  const expand = document.getElementById('expand-guide');
  function updateExpand() {
    const all = sections.every(section => section.open);
    expand.setAttribute('aria-expanded', String(all));
    expand.textContent = all ? 'Sakļaut visas sadaļas' : 'Izvērst visas sadaļas';
  }
  expand.addEventListener('click', () => { const open = !sections.every(section => section.open); for (const section of sections) section.open = open; updateExpand(); });
  for (const section of sections) section.addEventListener('toggle', updateExpand);
  let printOpen = [];
  addEventListener('beforeprint', () => { printOpen = sections.map(section => section.open); sections.forEach(section => section.open = true); });
  addEventListener('afterprint', () => { sections.forEach((section, index) => section.open = printOpen[index]); updateExpand(); });
  setDocument('guide'); fromHash(true);
})();
