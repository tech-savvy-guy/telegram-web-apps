Telegram.WebApp.ready()
Telegram.WebApp.expand()
Telegram.WebApp.onEvent("qrTextReceived", eventHandler=>{
    var qrText = eventHandler.data;
    console.log(qrText);
});
