// ── Helpers ───────────────────────────────────────────────
const $ = id => document.getElementById(id);

// ── Who's Home ────────────────────────────────────────────
async function loadMembers() {
  const res = await fetch('/api/members');
  const members = await res.json();
  renderMembers(members);
}

function renderMembers(members) {
  const grid = $('members-grid');
  grid.innerHTML = '';

  members.forEach(member => {
    const card = document.createElement('div');
    card.className = `member-card ${member.home ? 'home' : ''}`;
    card.dataset.id = member.id;
    card.innerHTML = `
      <div class="member-avatar">${avatarEmoji(member.name)}</div>
      <div class="member-name">${member.name}</div>
      <div class="member-status">${member.home ? '✅ Home' : '⬜ Away'}</div>
    `;
    card.addEventListener('click', () => toggleMember(member));
    grid.appendChild(card);
  });
}

function avatarEmoji(name) {
  const emojis = { Mom: '👩', Dad: '👨', Gagan: '🧒', Shashank: '👦' };
  return emojis[name] || '🙂';
}

async function toggleMember(member) {
  member.home = !member.home;

  // Update UI immediately (optimistic update)
  const card = document.querySelector(`[data-id="${member.id}"]`);
  card.classList.toggle('home', member.home);
  card.querySelector('.member-status').textContent =
    member.home ? '✅ Home' : '⬜ Away';

  // Tell the server
  await fetch(`/api/members/${member.id}/toggle`, { method: 'POST' });
}

// ── Grocery List ──────────────────────────────────────────
let groceryItems = [];

async function loadGrocery() {
  const res = await fetch('/api/grocery');
  groceryItems = await res.json();
  renderGrocery();
}

function renderGrocery() {
  const list = $('grocery-list');
  const empty = $('grocery-empty');
  list.innerHTML = '';

  if (groceryItems.length === 0) {
    empty.style.display = 'block';
    return;
  }

  empty.style.display = 'none';
  groceryItems.forEach(item => {
    const li = document.createElement('li');
    li.dataset.id = item.id;
    li.innerHTML = `
      <span>${item.item}</span>
      <button class="delete-btn" onclick="deleteItem(${item.id})">✕</button>
    `;
    list.appendChild(li);
  });
}

async function addItem() {
  const input = $('grocery-input');
  const itemText = input.value.trim();
  if (!itemText) return;

  // Optimistic update
  const tempId = Date.now();
  groceryItems.push({ id: tempId, item: itemText });
  renderGrocery();
  input.value = '';
  input.focus();

  // Tell the server
  await fetch('/api/grocery', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item: itemText })
  });
}

async function deleteItem(itemId) {
  // Optimistic update
  groceryItems = groceryItems.filter(i => i.id !== itemId);
  renderGrocery();

  // Tell the server
  await fetch(`/api/grocery/${itemId}`, { method: 'DELETE' });
}

// ── Event Listeners ───────────────────────────────────────
$('grocery-add-btn').addEventListener('click', addItem);

$('grocery-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') addItem();
});

// ── Init ──────────────────────────────────────────────────
loadMembers();
loadGrocery();