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

//Funcionalidad Sign Up
document.getElementById("signup").addEventListener("click", function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const span = document.getElementById("error-message");
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            console.log("User Created")
            open("../index.html", "_self");                      
        })
        .catch((error) => {
            const errorCode = error.code;
            console.log (errorCode)
            span.style.visibility = 'visible';
            span.textContent = errorCode;
        });
})


//Funcionalidad Login
document.getElementById("login").addEventListener("click", function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const span = document.getElementById("error-message");
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            console.log("User Signed In")
            const user = userCredential.user;
            open("../index.html", "_self");                      
        })
        .catch((error) => {
            const errorCode = error.code;
            console.log (errorCode)
            span.style.visibility = 'visible';
            span.textContent = errorCode;
        });
})
