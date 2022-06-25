import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.8.4/firebase-auth.js";


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

document.getElementById("signup").addEventListener("click", function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            console.log("created")
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorCode + errorMessage)

        });
})