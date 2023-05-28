Telegram.WebApp.ready()
Telegram.WebApp.expand()
Telegram.WebApp.onEvent('qrTextReceived', sendData)

function sendData(this, data) {
  console.log(this, data);
  fetch('/qrCode-response', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qr: data, initData: window.Telegram.WebApp.initData })
  });
};

