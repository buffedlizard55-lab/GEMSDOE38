'use strict';
const button = document.getElementById('copy-note');
if (button) button.addEventListener('click', async () => {
  const text = document.getElementById('submission-note').textContent;
  const status = document.getElementById('copy-status');
  try { await navigator.clipboard.writeText(text); status.textContent = 'Note copied.'; }
  catch { status.textContent = 'Clipboard unavailable. Select and copy the note above.'; }
});
