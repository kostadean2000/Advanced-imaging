// Wags to Whiskers site script.
// Uses event delegation on the document so it keeps working when a page
// builder (GoHighLevel, Squarespace, etc.) renders or re-renders the content
// after this script has loaded.
(function () {
  if (window.__wagsInit) return;
  window.__wagsInit = true;

  // Mobile navigation toggle
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest && e.target.closest('.nav-toggle');
    if (!toggle) return;
    var nav = document.getElementById('site-nav');
    if (!nav) return;
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Footer year
  function setYear() {
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setYear);
  else setYear();
  window.addEventListener('load', setYear);

  // Lead forms (free consultation + book appointment)
  // To send submissions to an inbox or CRM, set the form's data-endpoint attribute
  // to a form service or webhook URL (Formspree, a GoHighLevel inbound webhook,
  // HubSpot, etc.). The fields are sent as JSON. Until then the form opens the
  // visitor's email app with the request pre-filled.
  var LABELS = {
    name: 'Owner name', email: 'Email', phone: 'Phone', pet: "Pet's name & breed",
    pet_name: 'Pet name', pet_type: 'Pet type', breed: 'Breed / size', service: 'Service',
    interest: 'Services of interest', preferred: 'Preferred day/time',
    source: 'How did you hear about us', message: 'Notes'
  };
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !(form.id === 'consult-form' || form.classList.contains('js-lead-form'))) return;
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = new FormData(form);
    var success = form.querySelector('#form-success, .form-success');
    var endpoint = form.getAttribute('data-endpoint');
    var subject = form.getAttribute('data-subject') || 'Free Grooming Consultation';
    var payload = {};
    data.forEach(function (v, k) { payload[k] = payload[k] ? payload[k] + ', ' + v : v; });
    payload.form = subject;

    if (endpoint) {
      fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' }
      })
        .then(function (r) {
          if (!r.ok) throw new Error('Request failed');
          form.reset();
          if (success) success.style.display = 'block';
        })
        .catch(function () {
          alert('Sorry, something went wrong. Please call or email us directly.');
        });
      return;
    }

    var lines = [];
    Object.keys(payload).forEach(function (k) {
      if (k !== 'form') lines.push((LABELS[k] || k) + ': ' + payload[k]);
    });
    var who = payload.pet_name || payload.pet || '';
    window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
      '?subject=' + encodeURIComponent(subject + ' - ' + who + ' (' + payload.name + ')') +
      '&body=' + encodeURIComponent(lines.join('\n'));
    if (success) success.style.display = 'block';
  });
})();
