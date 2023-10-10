Telegram.WebApp.ready()
Telegram.WebApp.expand()

function handleQRTextReceived(event) {
  var qrText = event.data;

  fetch('/qrCodeResponse', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qr: qrText, initData: window.Telegram.WebApp.initData })
  });

  Telegram.WebApp.offEvent('qrTextReceived', handleQRTextReceived);

  setTimeout(Telegram.WebApp.closeScanQrPopup(), 1000);
}

Telegram.WebApp.onEvent('qrTextReceived', handleQRTextReceived);