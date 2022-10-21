import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyApEGemuVO2LHKa-30vNuWWFwmYkQimcio",
    authDomain: "greenhouseweb-2b01d.firebaseapp.com",
    databaseURL: "https://greenhouseweb-2b01d-default-rtdb.firebaseio.com",
    projectId: "greenhouseweb-2b01d",
    storageBucket: "greenhouseweb-2b01d.appspot.com",
    messagingSenderId: "737436287095",
    appId: "1:737436287095:web:d9a02b0f4af54668694672",
    measurementId: "G-CVP62RYRG4"
};

const app = initializeApp(firebaseConfig);                     //Starts FireBase API from Database Credentials
const auth = getAuth(app);

const signUpDiv = document.getElementById("signUpDiv");        //Gets signUpDiv reference
const signInDiv = document.getElementById("signInDiv");        //Gets singInDiv reference
const backModal = document.getElementById("back_modal");       //Gets Black Background when modal is being showed
const sideMenu = document.getElementById("offcanvasNavbar");   //Gets sideMenu reference
const inputIP = document.getElementById("ip-input");           //Gets input IP reference
const guiaModal = document.getElementById("modalGuide")        //Gets modalGuide reference
const modalIP = document.getElementById("modalIP")             //Gets modalIP reference
var userValid = false;       

//Sign Up logic
document.getElementById("signup").addEventListener("click", function () {   //Click event triggers this function from Sign Up Button
    const email = document.getElementById("email").value;                   //Stores email data
    const password = document.getElementById("password").value;             //Stores password data
    createUserWithEmailAndPassword(auth, email, password)                   //Creates user from gathered data
        .then((userCredential) => {
            console.log("User Created");
            signUpDiv.classList.add("hid");
            userValid = true;
        })
        .catch((error) => {                                                 //If data isn't OK, it won't creat user, e.g not using @ or not valid password
            const errorCode = error.code;
            alert(errorCode);
        });
})

//Login logic
document.getElementById("signin").addEventListener("click", function () { //Click event triggers this function from Sign In Button 
    const email = document.getElementById("email-login").value;                //Stores email data
    const password = document.getElementById("password-login").value;          //Stores password data
    signInWithEmailAndPassword(auth, email, password)                    //This functions validates data from database. If user exists, it'll sign in
        .then((userCredential) => {
            console.log("User Signed In")
            signInDiv.classList.add("hid");
        })
        .catch((error) => {                                              //If it doesn't exist:
            const errorCode = error.code;
            console.log(errorCode);
        });
})

//Forma Parte Button
document.getElementById("boton-Auth").addEventListener("click", function (){
    signUpDiv.classList.remove("hid");
    backModal.classList.remove("hid");
})

//Forma Parte Button Mobile (Side Menu)
document.getElementById("boton-Auth-mobile").addEventListener("click", function (){
    signUpDiv.classList.remove("hid");
    backModal.classList.remove("hid");
    sideMenu.classList.remove("show");
})

//Close signIn
document.getElementById("boton-cerrar-signin").addEventListener("click", function (){
    signInDiv.classList.add("hid");
    backModal.classList.add("hid");
})

//Close signUp
document.getElementById("boton-cerrar-signup").addEventListener("click", function (){
    signUpDiv.classList.add("hid");
    backModal.classList.add("hid");
})

//Anchor inside signUp Modal
document.getElementById("iniciar-Sesion-Anchor").addEventListener('click',function(){
    signUpDiv.classList.add("hid");
    signInDiv.classList.remove("hid");
})

//Anchor inside signIn modal
document.getElementById("crear-Sesion-Anchor").addEventListener('click',function(){
    signInDiv.classList.add("hid");
    signUpDiv.classList.remove("hid");
})

document.getElementById("ip-aceptar").addEventListener('click', function(){ //Checks if at least "IP" has an IP FORMAT to prevent wrong data
    var IP  = "http://" + inputIP.value;
    if(IP.match(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/)){                 //IP format
        window.open(IP);
        console.log("VALID IP, OPENING WEBSERVER");
    }
    else{
        console.log("INVALID IP...");
        alert("Direccion IP inválida.")
    }
})

document.getElementById("ip-boton-cerrar").addEventListener('click', function(){
    backModal.classList.add("hid");
})

//Open Modal Guia
document.getElementById("openGuide").addEventListener('click', function() {
    backModal.classList.remove("hid");
    guiaModal.classList.remove("hid");
    modalIP.classList.add("hid");
})

//Close Modal Guia
document.getElementById("closeGuide").addEventListener('click', function() {
    backModal.classList.add("hid");
    guiaModal.classList.add("hid");
})

// Code to set the height of the main content in "Guías"

/*let body = document.querySelector("body");  //Selecciono el elemento body
let header = document.querySelector("header"); //Selecciono el elemento header
let contGuia = document.querySelector(".cont_guia"); //Selecciono el div que contiene la informacion de guias
contGuia.style.height = `${body.clientHeight - header.clientHeight}px`; //Resto la altura del body y la del header para determinar la altura del contenedor de guias
*/
setInterval(function(){
    let header = document.querySelector("header")
    let main = document.querySelector(".main-guia")
    let body = document.querySelector("body")
    let cuenta = body.clientHeight - header.clientHeight
    main.style.height = cuenta + "px"
}, 10)
/*let header = document.querySelector("header")
let main = document.querySelector(".main-guia")
let body = document.querySelector("body")
let cuenta = body.clientHeight - header.clientHeight
main.style.height = cuenta + "px"*/





