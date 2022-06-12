const captcha = document.querySelector(".captcha"),
reloadBtn = document.querySelector(".reload-btn"),
inputField = document.querySelector(".input-area input"),
checkBtn = document.querySelector(".check-btn"),
statusTxt = document.querySelector(".status-text"),
maxtries = document.querySelector(".error");

var attempts = 0;

Telegram.WebApp.ready()

let allCharacters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                     'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                     'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
function getCaptcha(){
  for (let i = 0; i < 6; i++) {
    let randomCharacter = allCharacters[Math.floor(Math.random() * allCharacters.length)];
    captcha.innerText += ` ${randomCharacter}`;
  }
}
getCaptcha();
reloadBtn.addEventListener("click", ()=>{
  removeContent();
  getCaptcha();
});

checkBtn.addEventListener("click", e =>{
  e.preventDefault();
  statusTxt.style.display = "block";
  let inputVal = inputField.value.split('').join(' ');
  if(inputVal == captcha.innerText){
    statusTxt.style.color = "#4db2ec";
    statusTxt.innerText = "Nice! You don't appear to be a robot.";
    checkBtn.style.display = "none";
    fetch('/captcha-response', {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        isbot: false, attempts: attempts + 1,
        initData: window.Telegram.WebApp.initData
      })
  });
    attempts = 0;

  }else{
    if (attempts < 2) { 
      statusTxt.style.color = "#ff0000";
      statusTxt.innerText = "Error! Remaining attempts: " + (2 - attempts);
      fetch('/captcha-response', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
          isbot: true, attempts: attempts + 1,
          initData: window.Telegram.WebApp.initData
        })
      });
      inputField.value = "";
      captcha.innerText = "";
      attempts = attempts + 1;
      getCaptcha();
    }

    else {
        maxtries.style.display = "block";
        statusTxt.style.display = "none";
        maxtries.innerText = "Maximum attempts reached!";
        document.querySelector(".input-area").style.display = "none";
        document.querySelector(".captcha-area").style.display = "none";
        fetch('/captcha-response', {
          method: 'POST',
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
          body: JSON.stringify({
            isbot: true, attempts: attempts + 1,
            initData: window.Telegram.WebApp.initData
          })
        });
    }
  }
});

function removeContent(){
 inputField.value = "";
 captcha.innerText = "";
 statusTxt.style.display = "none";
}