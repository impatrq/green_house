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

// //Sign Up logic
// document.getElementById("signup").addEventListener("signUp", function () {  //Click event triggers this function from Sign Up Button
//     const email = document.getElementById("email").value;                   //Stores email data
//     const password = document.getElementById("password").value;             //Stores password data
//     const span = document.getElementById("error-message");                  //Gets span reference to show errors
//     createUserWithEmailAndPassword(auth, email, password)                   //Creates user from gathered data
//         .then((userCredential) => {
//             const user = userCredential.user;
//             console.log("User Created")
//             open("../index.html", "_self");                      
//         })
//         .catch((error) => {                                                 //If data isn't OK, it won't creat user, e.g not using @ or not valid password
//             const errorCode = error.code;
//             console.log (errorCode)
//             span.style.visibility = 'visible';
//             span.textContent = errorCode;
//         });
// })

// //Login logic
// document.getElementById("login").addEventListener("signIn", function () { //Click event triggers this function from Sign In Button 
//     const email = document.getElementById("email").value;                //Stores email data
//     const password = document.getElementById("password").value;          //Stores password data
//     const span = document.getElementById("error-message");               //Gets span reference to show errors
//     signInWithEmailAndPassword(auth, email, password)                    //This functions validates data from database. If user exists, it'll sign in
//         .then((userCredential) => {
//             console.log("User Signed In")
//             const user = userCredential.user;
//             open("../index.html", "_self");                      
//         })
//         .catch((error) => {                                              //If it doesn't exist:
//             const errorCode = error.code;
//             console.log (errorCode)
//             span.style.visibility = 'visible';
//             span.textContent = errorCode;
//         });
// })

//Forma Parte Button
document.getElementById("botonAuth").addEventListener("click", function (){
    console.log("Forma Parte was clicked");
    //Show Sign Up or Sign In Modal
    //modal.style.visibility = 'visible';
})

// const signUpDiv = document.getElementById("signUp_div");  //Gets signUpDiv reference
// const signInDiv = document.getElementById("singIn_div");  //Gets singInDiv reference

//document.getElementById("cerrar").addEventListener("click", function (){
    //Close signUp and signIn
//})