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

  // Consultation form
  // To send submissions to an inbox or CRM, set the form's data-endpoint attribute
  // to a form service or webhook URL (Formspree, a GoHighLevel inbound webhook,
  // HubSpot, etc.). The fields are sent as JSON. Until then the form opens the
  // visitor's email app with the request pre-filled.
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.id !== 'consult-form') return;
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = new FormData(form);
    var success = document.getElementById('form-success');
    var endpoint = form.getAttribute('data-endpoint');
    var interests = data.getAll('interest').join(', ') || 'Not specified';

    if (endpoint) {
      var payload = {};
      data.forEach(function (v, k) { if (k !== 'interest') payload[k] = v; });
      payload.interest = interests;
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

    var lines = [
      'Owner name: ' + data.get('name'),
      'Email: ' + data.get('email'),
      'Phone: ' + data.get('phone'),
      'Pet name: ' + data.get('pet_name'),
      'Pet type: ' + data.get('pet_type'),
      'Breed / size: ' + (data.get('breed') || ''),
      'Services of interest: ' + interests,
      'Preferred day/time: ' + (data.get('preferred') || ''),
      'How did you hear about us: ' + (data.get('source') || ''),
      '',
      data.get('message') || ''
    ];
    window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
      '?subject=' + encodeURIComponent('Free Grooming Consultation - ' + data.get('pet_name') + ' (' + data.get('name') + ')') +
      '&body=' + encodeURIComponent(lines.join('\n'));
    if (success) success.style.display = 'block';
  });
})();
