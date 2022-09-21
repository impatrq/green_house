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