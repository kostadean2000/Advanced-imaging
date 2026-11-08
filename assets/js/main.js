// Mobile navigation toggle
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Consultation form
  // To send submissions to an inbox, set the form's data-endpoint attribute to a
  // form service URL (e.g. Formspree, Netlify Forms, HubSpot). Until then the form
  // opens the visitor's email app with the request pre-filled.
  var form = document.getElementById('consult-form');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = new FormData(form);
    var success = document.getElementById('form-success');
    var endpoint = form.getAttribute('data-endpoint');

    if (endpoint) {
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('Request failed');
          form.reset();
          success.style.display = 'block';
        })
        .catch(function () {
          alert('Sorry, something went wrong. Please call or email us directly.');
        });
      return;
    }

    var services = data.getAll('interest').join(', ') || 'Not specified';
    var lines = [
      'Name: ' + data.get('name'),
      'Title: ' + (data.get('title') || ''),
      'Organization: ' + data.get('organization'),
      'Facility type: ' + data.get('facility'),
      'Email: ' + data.get('email'),
      'Phone: ' + (data.get('phone') || ''),
      'Interested in: ' + services,
      'Timeline: ' + data.get('timeline'),
      '',
      data.get('message') || ''
    ];
    var to = form.getAttribute('data-mailto');
    window.location.href = 'mailto:' + to +
      '?subject=' + encodeURIComponent('Free Consultation Request - ' + data.get('organization')) +
      '&body=' + encodeURIComponent(lines.join('\n'));
    success.style.display = 'block';
  });
})();
