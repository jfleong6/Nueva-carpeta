// ===========================
// REGISTRO HOTEL — NAVEGACIÓN
// ===========================

document.addEventListener("DOMContentLoaded", () => {
  let pasoActual = 1;
  const totalPasos = 4;

  const btnSiguiente = document.getElementById("btn-siguiente");
  const btnAtras = document.getElementById("btn-atras");
  const btnGuardar = document.getElementById("btn-guardar");

  const secciones = document.querySelectorAll(".seccion");
  const pasos = document.querySelectorAll(".progress-line .step");

  mostrarPaso(pasoActual);

  // Botón siguiente
  btnSiguiente.addEventListener("click", () => {
    // TODO: validarPaso(pasoActual)
    if (pasoActual < totalPasos) pasoActual++;
    mostrarPaso(pasoActual);
  });

  // Botón atrás
  btnAtras.addEventListener("click", () => {
    if (pasoActual > 1) pasoActual--;
    mostrarPaso(pasoActual);
  });

  // Guardar
  btnGuardar.addEventListener("click", () => {
    alert("✅ Registro guardado correctamente (simulado)");
    pasoActual = 1;
    mostrarPaso(pasoActual);
  });

  // Mostrar sección activa y actualizar progreso
  function mostrarPaso(paso) {
    secciones.forEach((sec, i) => {
      sec.classList.toggle("oculto", i !== paso - 1);
    });

    pasos.forEach((p, i) => {
      p.classList.toggle("active", i === paso - 1);
    });

    btnAtras.style.display = paso === 1 ? "none" : "inline-block";
    btnSiguiente.style.display = paso === totalPasos ? "none" : "inline-block";
    btnGuardar.classList.toggle("oculto", paso !== totalPasos);
  }
});

// ===========================
// SECCIÓN 3 — LÓGICA RESERVA
// ===========================
document.addEventListener("DOMContentLoaded", () => {
  const fechaLlegada = document.getElementById("fecha-llegada");
  const fechaSalida = document.getElementById("fecha-salida");
  const numHuespedes = document.getElementById("num-huespedes");
  const paqueteSelect = document.getElementById("paquete-select");
  const descuentoInput = document.getElementById("descuento");
  const valorPaqueteEl = document.getElementById("valor-paquete");
  const btnAgregar = document.getElementById("btn-agregar-paquete");
  const tablaBody = document.querySelector("#tabla-paquetes tbody");
  const subtotalEl = document.getElementById("subtotal-paquetes");

  let paquetesAgregados = [];

  const hoy = new Date();
  fechaLlegada.value = hoy.toISOString().split("T")[0];

  function calcularValor() {
    const opt = paqueteSelect.selectedOptions[0];
    if (!opt) return 0;
    const precio = parseFloat(opt.dataset.precio) || 0;
    const porPersona = parseInt(opt.dataset.porPersona) || 0;
    const n = Math.max(1, parseInt(numHuespedes.value) || 1);
    const desc = Math.max(0, Math.min(100, parseFloat(descuentoInput.value) || 0));
    const base = porPersona ? precio * n : precio;
    const total = base * (1 - desc / 100);
    valorPaqueteEl.textContent = "$" + total.toLocaleString();
    return total;
  }

  function renderTabla() {
    tablaBody.innerHTML = "";
    let subtotal = 0;
    paquetesAgregados.forEach((p, i) => {
      subtotal += p.total;
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${p.nombre}</td>
        <td>$${p.precio.toLocaleString()}</td>
        <td>${p.porPersona ? "Sí" : "No"}</td>
        <td>${p.personas}</td>
        <td>${p.descuento}%</td>
        <td>$${p.total.toLocaleString()}</td>
        <td><button data-i="${i}" class="btn btn-secondary btn-sm">✖</button></td>
      `;
      tablaBody.appendChild(tr);
    });
    subtotalEl.textContent = "$" + subtotal.toLocaleString();
  }

  paqueteSelect.addEventListener("change", calcularValor);
  numHuespedes.addEventListener("input", calcularValor);
  descuentoInput.addEventListener("input", calcularValor);

  btnAgregar.addEventListener("click", () => {
    const opt = paqueteSelect.selectedOptions[0];
    if (!opt || !opt.value) return alert("Seleccione un paquete.");
    const precio = parseFloat(opt.dataset.precio);
    const porPersona = parseInt(opt.dataset.porPersona);
    const personas = parseInt(numHuespedes.value);
    const descuento = parseFloat(descuentoInput.value);
    const base = porPersona ? precio * personas : precio;
    const total = base * (1 - descuento / 100);
    paquetesAgregados.push({
      id: opt.value,
      nombre: opt.textContent.trim(),
      precio, porPersona, personas, descuento, total
    });
    renderTabla();
  });

  tablaBody.addEventListener("click", e => {
    if (e.target.matches("button[data-i]")) {
      const i = e.target.dataset.i;
      paquetesAgregados.splice(i, 1);
      renderTabla();
    }
  });

  calcularValor();
});
