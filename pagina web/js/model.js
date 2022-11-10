const modeloPequeño = document.getElementById("modelo_celular");
const modeloNormal = document.getElementById("modelo_normal");

if (innerWidth < 768) {
    modeloNormal.classList.add("hid");
    modeloPequeño.classList.remove("hid");
}
console.log(innerWidth);