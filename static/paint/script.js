const canvas = document.querySelector("#canvas"),
toolbar = document.getElementById("tool-bar"),
ctx = canvas.getContext('2d');

window.addEventListener("load", () => {
    const stroke = document.querySelector("#slider"),
    color = document.querySelector("#color"),
    canvasOffsetY = canvas.offsetTop;

    canvas.height  = 0.9 * (window.innerHeight - toolbar.clientHeight);
    canvas.width = toolbar.clientWidth;
    
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    let painting = false;

    function startPosition(e){
        painting = true;
        draw(e);
    }

    function finishedPosition(){
        painting = false;
        ctx.beginPath();
    }

    function draw(e){
        if (!painting) return;
        ctx.lineWidth = stroke.value;
        ctx.lineCap = "round";
        ctx.strokeStyle = color.value
        ctx.lineTo(e.clientX - 20, e.clientY - canvasOffsetY)
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX - 20, e.clientY - canvasOffsetY)
    }

    canvas.addEventListener("mousedown", startPosition);
    canvas.addEventListener("mouseup", finishedPosition);
    canvas.addEventListener("mousemove", draw);


});

const eraseBtn = document.querySelector(".erase-button")
eraseBtn.addEventListener("click", clear)

function clear() {
    var canvas = document.querySelector("#canvas"),
    ctx = canvas.getContext('2d');
    ctx.fillStyle = "white";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

const saveBtn = document.querySelector(".save-button")
saveBtn.addEventListener("click", save)

function save() {
    var canvas = document.querySelector("#canvas");
    // const a = document.createElement("a");

    // document.body.appendChild(a);
    // a.href = canvas.toDataURL();
    // a.download = "image.png";
    // a.click();
    // document.body.removeChild(a);

    fetch('/paint-response', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
          imageData: canvas.toDataURL(),
          initData: window.Telegram.WebApp.initData
        })
    });
}

Telegram.WebApp.ready()