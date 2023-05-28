Telegram.WebApp.ready()
Telegram.WebApp.expand()
Telegram.WebApp.onEvent('qrTextReceived', sendData)
console.log("Hi! ");
function sendData(this, data) {
  console.log(this, data);
  console.log("Hello");
  fetch('/qrCode-response', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qr: data, initData: window.Telegram.WebApp.initData })
  });
};
