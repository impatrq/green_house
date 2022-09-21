import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-analytics.js";
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

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

var signUpDiv = document.getElementById("signUpDiv");  //Gets signUpDiv reference
var signInDiv = document.getElementById("signInDiv");  //Gets singInDiv reference
var backModal = document.getElementById("back_modal");  //Gets Black Background when modal is being showed
var sideMenu = document.getElementById("offcanvasNavbar");  //Gets sideMenu reference

//Sign Up logic
document.getElementById("signup").addEventListener("click", function () {   //Click event triggers this function from Sign Up Button
    const email = document.getElementById("email").value;                   //Stores email data
    const password = document.getElementById("password").value;             //Stores password data
    //const span = document.getElementById("error-message");                //Gets span reference to show errors
    createUserWithEmailAndPassword(auth, email, password)                   //Creates user from gathered data
        .then((userCredential) => {
            const user = userCredential.user;
            console.log("User Created");
            const IP = prompt("Ingrese la IP del Display: ");
            console.log(IP);
            window.open(IP, '_blank');
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
    //const span = document.getElementById("error-message");               //Gets span reference to show errors
    signInWithEmailAndPassword(auth, email, password)                    //This functions validates data from database. If user exists, it'll sign in
        .then((userCredential) => {
            console.log("User Signed In")
            const user = userCredential.user;
            const IP = prompt("Ingrese la IP del Display: ");
            console.log(IP);
            window.open(IP, '_blank');
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
