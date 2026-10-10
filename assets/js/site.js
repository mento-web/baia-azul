/* ==========================================================================
   BAÍA AZUL · site.js
   --------------------------------------------------------------------------
   Progressive enhancement only. Every link and button already works without
   this file: booking buttons are plain WhatsApp links, and the tour list is
   complete in the HTML. The script adds:

     1. Mobile menu and the "Passeios" dropdown
     2. Tour filters on the home page
     3. Booking dialog that writes the WhatsApp message for the visitor
     4. Sticky booking bar on tour pages

   No cookies, no storage, no tracking, no network requests.
   ========================================================================== */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };


  /* ------------------------------------------------------------------------
     1. MENU
     ------------------------------------------------------------------------ */
  var nav = $('.nav');
  var burger = $('.nav__burger');

  if (nav && burger) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });
  }

  // Dropdown: hover and focus are handled in CSS. The click handler makes it
  // work on touch screens and inside the mobile menu.
  $$('.nav__item > button').forEach(function (button) {
    var item = button.parentNode;
    button.addEventListener('click', function () {
      var open = item.classList.toggle('is-open');
      button.setAttribute('aria-expanded', String(open));
    });
  });

  document.addEventListener('click', function (event) {
    $$('.nav__item.is-open').forEach(function (item) {
      if (!item.contains(event.target)) {
        item.classList.remove('is-open');
        $('button', item).setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    $$('.nav__item.is-open').forEach(function (item) {
      item.classList.remove('is-open');
      var button = $('button', item);
      button.setAttribute('aria-expanded', 'false');
      button.focus();
    });
  });


  /* ------------------------------------------------------------------------
     2. FILTERS (home page)
     Two questions, answered independently: what kind of trip, and from where.
     After filtering, the visible bands are striped again so the white and
     tinted bands keep alternating.
     ------------------------------------------------------------------------ */
  var typeSelect = $('#filtro-tipo');
  var originSelect = $('#filtro-saida');
  var tours = $$('.tour[data-tipo]');
  var emptyMessage = $('.filter-empty');
  var counter = $('#filtro-status');

  function applyFilters() {
    var type = typeSelect.value;
    var origin = originSelect.value;
    var shown = 0;

    tours.forEach(function (tour) {
      var match = (!type || tour.getAttribute('data-tipo') === type) &&
                  (!origin || tour.getAttribute('data-saida').split(' ').indexOf(origin) !== -1);
      tour.hidden = !match;
      if (match) {
        tour.classList.toggle('band--tint', shown % 2 === 0);
        shown += 1;
      }
    });

    if (emptyMessage) emptyMessage.hidden = shown !== 0;
    if (counter) {
      counter.textContent = shown === 0 ? 'Nenhuma opção encontrada.'
        : shown === 1 ? '1 opção encontrada.' : shown + ' opções encontradas.';
    }
  }

  if (typeSelect && originSelect && tours.length) {
    typeSelect.addEventListener('change', applyFilters);
    originSelect.addEventListener('change', applyFilters);

    var reset = $('#filtro-limpar');
    if (reset) {
      reset.addEventListener('click', function () {
        typeSelect.value = '';
        originSelect.value = '';
        applyFilters();
        typeSelect.focus();
      });
    }

    // A link such as index.html?tipo=transfer opens the list already filtered
    var params = new URLSearchParams(window.location.search);
    if (params.get('tipo')) typeSelect.value = params.get('tipo');
    if (params.get('saida')) originSelect.value = params.get('saida');
    if (typeSelect.value || originSelect.value) applyFilters();
  }


  /* ------------------------------------------------------------------------
     3. BOOKING DIALOG
     Any element with data-reservar opens the dialog. The attribute value is
     the product to preselect. Submitting builds one tidy message and opens
     WhatsApp with it. Nothing is stored or sent anywhere else.
     ------------------------------------------------------------------------ */
  var dialog = $('#reserva');
  var form = $('#reserva-form');

  if (dialog && form && typeof dialog.showModal === 'function') {
    var productField = form.elements.produto;
    var dateField = form.elements.data;

    // Earliest selectable date is today, in the visitor's own time zone
    var now = new Date();
    dateField.min = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0');

    $$('[data-reservar]').forEach(function (trigger) {
      trigger.addEventListener('click', function (event) {
        event.preventDefault();
        var wanted = trigger.getAttribute('data-reservar');
        if (wanted) productField.value = wanted;
        if (nav) nav.classList.remove('is-open');
        if (burger) burger.setAttribute('aria-expanded', 'false');
        dialog.showModal();
      });
    });

    $('.dialog__close', dialog).addEventListener('click', function () { dialog.close(); });

    // A click on the dimmed area around the dialog closes it
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) dialog.close();
    });

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var value = function (name) { return (form.elements[name].value || '').trim(); };
      var lines = ['Olá! Quero fazer uma reserva com a Baía Azul.', ''];

      lines.push('*' + value('produto') + '*');
      if (value('data')) {
        var parts = value('data').split('-');
        lines.push('Data: ' + parts[2] + '/' + parts[1] + '/' + parts[0]);
      }
      var people = 'Adultos: ' + value('adultos');
      if (Number(value('criancas')) > 0) people += ' · Crianças: ' + value('criancas');
      lines.push(people);
      if (value('nome')) lines.push('Nome: ' + value('nome'));
      if (value('hospedagem')) lines.push('Hospedagem: ' + value('hospedagem'));
      if (value('obs')) lines.push('Observações: ' + value('obs'));

      var base = form.getAttribute('data-whatsapp');
      window.open(base + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
      dialog.close();
    });
  }


  /* ------------------------------------------------------------------------
     4. STICKY BOOKING BAR (tour pages)
     Appears once the hero has scrolled out of view.
     ------------------------------------------------------------------------ */
  var bar = $('.bar');
  var hero = $('.hero');

  if (bar && hero && 'IntersectionObserver' in window) {
    document.body.classList.add('has-bar');
    new IntersectionObserver(function (entries) {
      var visible = !entries[0].isIntersecting;
      bar.classList.toggle('is-visible', visible);
      bar.setAttribute('aria-hidden', String(!visible));
    }, { rootMargin: '-80px 0px 0px 0px' }).observe(hero);
  }
})();
