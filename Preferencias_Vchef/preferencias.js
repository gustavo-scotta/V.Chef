// ── TAB NAV ──
(function () {
  const nav = document.querySelector('nav.tab-nav');
  const buttons = [...nav.querySelectorAll('.tab')];
  const pill = document.createElement('div');
  pill.className = 'tab-pill';
  buttons.forEach(b => pill.appendChild(b));
  nav.appendChild(pill);

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
})();

// ── TAGS ──
function addTag() {
  const input = document.getElementById('foodInput');
  const value = input.value.trim();
  if (!value) return;

  const container = document.getElementById('tags-container');

  const exists = [...container.querySelectorAll('.tag')].some(
    t => t.dataset.value.toLowerCase() === value.toLowerCase()
  );
  if (exists) {
    input.style.borderColor = '#c0392b';
    setTimeout(() => (input.style.borderColor = ''), 800);
    input.value = '';
    return;
  }

  const tag = document.createElement('span');
  tag.className = 'tag';
  tag.dataset.value = value;
  tag.innerHTML = `${value} <button class="tag-remove" onclick="removeTag(this)">×</button>`;
  container.appendChild(tag);
  input.value = '';
  input.focus();
}

function removeTag(btn) {
  const tag = btn.closest('.tag');
  tag.style.transform = 'scale(0.8)';
  tag.style.opacity = '0';
  tag.style.transition = 'all 0.18s ease';
  setTimeout(() => tag.remove(), 180);
}

// ── ALERGIAS ──
function addAllergy() {
  const input = document.getElementById('allergyInput');
  const value = input.value.trim();
  if (!value) return;

  const grid = document.getElementById('allergy-grid');

  const exists = [...grid.querySelectorAll('.toggle-label')].some(
    l => l.textContent.toLowerCase() === value.toLowerCase()
  );
  if (exists) {
    input.style.borderColor = '#c0392b';
    setTimeout(() => (input.style.borderColor = ''), 800);
    input.value = '';
    return;
  }

  const card = document.createElement('div');
  card.className = 'toggle-card';
  card.style.animation = 'cardIn 0.22s ease both';
  card.innerHTML = `
    <span class="toggle-label">${value}</span>
    <div class="toggle-card-actions">
      <label class="toggle-switch">
        <input type="checkbox">
        <span class="slider"></span>
      </label>
      <button class="allergy-remove" onclick="removeAllergyCard(this)" title="Remover">×</button>
    </div>
  `;
  grid.appendChild(card);
  input.value = '';
  input.focus();
}

function removeAllergyCard(btn) {
  const card = btn.closest('.toggle-card');
  card.style.transition = 'opacity 0.18s, transform 0.18s';
  card.style.opacity = '0';
  card.style.transform = 'scale(0.9)';
  setTimeout(() => card.remove(), 180);
}

function addDiet() {
  const input = document.getElementById('dietInput');
  const value = input.value.trim();
  if (!value) return;

  const grid = document.getElementById('diet-grid');

  const exists = [...grid.querySelectorAll('.toggle-label')].some(
    l => l.textContent.toLowerCase() === value.toLowerCase()
  );
  if (exists) {
    input.style.borderColor = '#c0392b';
    setTimeout(() => (input.style.borderColor = ''), 800);
    input.value = '';
    return;
  }

  const card = document.createElement('div');
  card.className = 'toggle-card';
  card.style.animation = 'cardIn 0.22s ease both';
  card.innerHTML = `
    <span class="toggle-label">${value}</span>
    <div class="toggle-card-actions">
      <label class="toggle-switch">
        <input type="checkbox">
        <span class="slider"></span>
      </label>
      <button class="allergy-remove" onclick="removeAllergyCard(this)" title="Remover">×</button>
    </div>
  `;
  grid.appendChild(card);
  input.value = '';
  input.focus();
}

// ── SAVE ──
function savePrefs() {
  const tags = [...document.querySelectorAll('.tag')].map(t => t.dataset.value);
  const toggles = {};
  document.querySelectorAll('.toggle-card').forEach(card => {
    const label = card.querySelector('.toggle-label').textContent;
    const checked = card.querySelector('input[type=checkbox]').checked;
    toggles[label] = checked;
  });

  
  console.log('Saved:', { dislikedFoods: tags, toggles });


  const toast = document.getElementById('toast');
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2500);
}