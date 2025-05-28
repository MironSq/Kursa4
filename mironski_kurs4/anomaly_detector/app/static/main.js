async function callEndpoint(path) {
  await fetch(path, {method:'POST'});
}
document.getElementById('train-btn').onclick = () => callEndpoint('/train');
document.getElementById('detect-btn').onclick = () => callEndpoint('/detect');

async function update() {
  const res = await fetch('/data');
  const { anomalies, normal } = await res.json();
  const atb = document.querySelector('#anomalies-table tbody');
  const ntb = document.querySelector('#normal-table tbody');
  atb.innerHTML = ''; ntb.innerHTML = '';
  anomalies.forEach(a => {
    atb.insertAdjacentHTML('beforeend',
      `<tr><td>${a.session_id}</td><td>${a.score.toFixed(3)}</td><td>${a.time}</td></tr>`);
  });
  normal.forEach(n => {
    ntb.insertAdjacentHTML('beforeend',
      `<tr><td>${n.session_id}</td><td>${n.packet_count}</td><td>${n.byte_count}</td><td>${n.time}</td></tr>`);
  });
}
update();
setInterval(update, 5000);
