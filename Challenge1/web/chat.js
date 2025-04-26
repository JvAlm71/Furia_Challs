const form = document.getElementById('form');
const input = document.getElementById('input');
const msgs  = document.getElementById('messages');

function addMsg(text, cls){
  const d = document.createElement('div');
  d.className = 'msg '+cls;
  d.innerText = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

form.addEventListener('submit', async e=>{
  e.preventDefault();
  const txt = input.value.trim();
  if(!txt) return;
  addMsg(txt,'user');
  input.value = '';
  // chama a rota Python
  const res = await fetch('/api/chat', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({ message: txt })
  });
  const data = await res.json();
  addMsg(data.reply,'bot');
});
