let counter = 1;

document.addEventListener("DOMContentLoaded", ()=> {

    setInterval(() => {
        
        let imgs = document.querySelectorAll(".carrousel img");
        
        imgs.forEach((img, index) => {

            if(index == counter) {
                img.classList.remove("hid");
            }
            else {
                img.classList.add("hid");
            }
        });
        counter++;
        if(counter > imgs.length - 1) {
            counter = 0;
        }

    }, 3000);
});

setInterval(function(){
    let header = document.querySelector("header")
    let body = document.querySelector("body")
    let mainGaleria = document.querySelector(".galeria_main")
    let resultado = body.clientHeight - header.clientHeight
    mainGaleria.style.height = resultado + "px"
}, 10)
/*
let header = document.querySelector("header")
let body = document.querySelector("body")
let mainGaleria = document.querySelector(".galeria_main")
let resultado = body.clientHeight - header.clientHeight
mainGaleria.style.height = resultado + "px"
console.log(resultado)*/