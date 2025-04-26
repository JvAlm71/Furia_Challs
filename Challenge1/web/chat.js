const form = document.getElementById('form');
const input = document.getElementById('input');
const msgs  = document.getElementById('messages');


function addMsg(text, cls){
  const d = document.createElement('div');
  d.className = 'msg ' + cls;

  if (cls === 'bot') {
    // para bot usamos innerHTML (ele vem confiável do servidor)
    d.innerHTML = text;
  } else {
    // usuário: texto puro + status
    d.innerText = text;
    const s = document.createElement('span');
    s.className = 'status';
    s.innerText = '✓✓';
    d.appendChild(s);
  }

  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}


// Saudação assim que o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  addMsg(
    "Olá! Eu sou o chatbot oficial da FURIA CS2. Pergunte o que quiser sobre o time! Vale ressaltar que se quiser saber sobre noticias do time, digite noticias, ou noticia! Furioso",
    "bot"
  );
});

window.addEventListener('unload', () => {
  // precisa do segundo argumento (body) para o sendBeacon funcionar
  navigator.sendBeacon('/shutdown', '');
});

form.addEventListener('submit', async e => {
  e.preventDefault();
  const txt = input.value.trim();
  if(!txt) return;

  addMsg(txt, 'user');
  input.value = '';

  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ message: txt })
  });
  const data = await res.json();
  addMsg(data.reply, 'bot');
});
