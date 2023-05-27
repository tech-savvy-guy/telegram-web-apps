Telegram.WebApp.ready()
Telegram.WebApp.expand()

Telegram.WebApp.onEvent('qrTextReceived', function(data) {
    console.log(this, data);
  });
  
