const diapositivas = document.querySelectorAll(".diapositiva");
const puntos = document.querySelectorAll(".controles-slider button");
let actual = 0;

function mostrar(indice) {
  actual = indice;
  diapositivas.forEach((diapositiva, posicion) => {
    diapositiva.classList.toggle("activa", posicion === indice);
  });
  puntos.forEach((punto, posicion) => {
    punto.classList.toggle("activo", posicion === indice);
    // Restart animation for the progress bar
    if (posicion === indice) {
      punto.style.animation = 'none';
      punto.offsetHeight; /* trigger reflow */
      punto.style.animation = null; 
    }
  });
}

puntos.forEach((punto, indice) => {
  punto.addEventListener("click", () => mostrar(indice));
});

setInterval(() => mostrar((actual + 1) % diapositivas.length), 7000);
