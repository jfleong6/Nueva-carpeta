function cargarVista(nombreVista, boton) {
    const visor = document.getElementById("visor");
    visor.src = nombreVista; // Carga la vista Flask correspondiente

    // Marca el botón activo visualmente
    document.querySelectorAll(".menu-opciones button").forEach(btn => {
        btn.classList.remove("activo");
    });
    boton.classList.add("activo");
}

