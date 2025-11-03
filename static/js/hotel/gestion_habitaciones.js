// === REFERENCIAS ===
const form = document.getElementById("formHabitacion");
const modal = document.getElementById("modal");
const btnAgregar = document.getElementById("btnAgregar");
const btnCerrar = document.getElementById("btnCerrar");
const contenedor = document.querySelector(".habitaciones-grid");

// === FUNCIONES DE INTERFAZ ===

// Mostrar modal
btnAgregar.addEventListener("click", () => {
  modal.style.display = "flex";
});

// Cerrar modal
btnCerrar.addEventListener("click", cerrarModal);
modal.addEventListener("click", (e) => {
  if (e.target === modal) cerrarModal();
});

function cerrarModal() {
  modal.style.display = "none";
  form.reset();
}

// === FUNCIÓN PARA CREAR TARJETA ===
function crearTarjeta(h) {
  const card = document.createElement("article");
  card.classList.add("habitacion-card");
  card.dataset.id = h.numero;

  // Asignar clase según estado
  if (h.estado === 1) card.classList.add("estado-disponible");
  if (h.estado === 2) card.classList.add("estado-ocupada");
  if (h.estado === 3) card.classList.add("estado-aseo");

  // Determinar texto del estado
  const estadoTexto = 
    h.estado === 1 ? "Disponible" : 
    h.estado === 2 ? "Ocupada" : "En Aseo";

  // Construir el contenido HTML
  card.innerHTML = `
    <header class="card-header">
      <h2>Hab. ${h.numero}</h2>
      <span class="badge ${
        h.estado === 1 ? "disponible" : h.estado === 2 ? "ocupada" : "aseo"
      }">${estadoTexto}</span>
    </header>
    <div class="card-body">
      <p><strong>🏷️ Tipo:</strong> ${h.tipo}</p>
      <p><strong>👥 Capacidad:</strong> ${h.capacidad} personas</p>
      <p><strong>🛏️ Camas:</strong> ${h.cama} dobles, ${h.camarote} camarote, ${h.sencilla} sencilla</p>
    </div>
    <footer class="card-footer">
      <span class="precio">$${h.precio_noche} / noche / persona</span>
    </footer>
  `;

  return card;
}

// === FUNCIÓN PARA INSERTAR ORDENADO POR NÚMERO ===
function insertarEnOrden(nuevaCard) {
  const nuevasId = parseInt(nuevaCard.dataset.id);
  const habitaciones = [...contenedor.querySelectorAll(".habitacion-card")];

  let insertado = false;
  for (const card of habitaciones) {
    const idExistente = parseInt(card.dataset.id);
    if (nuevasId < idExistente) {
      contenedor.insertBefore(nuevaCard, card);
      insertado = true;
      break;
    }
  }

  if (!insertado) contenedor.appendChild(nuevaCard);
}

// === GUARDAR HABITACIÓN ===
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Recolectar datos
  const datos = {
    numero: form.numero.value.trim(),
    tipo: form.tipo.value.trim(),
    capacidad: parseInt(form.capacidad.value),
    cama: parseInt(form.doble.value),
    sencilla: parseInt(form.sencilla.value),
    camarote: parseInt(form.camarote.value),
    precio_noche: parseFloat(form.precio_noche.value),
    estado: 1, // Por defecto “Disponible”
  };

  try {
    const respuesta = await fetch("/api/habitaciones/agregar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    const data = await respuesta.json();

    if (!respuesta.ok) throw new Error(data.error || "No se pudo guardar");

    // Mostrar notificación visual
    mostrarAlerta("✅ " + data.mensaje, "success");

    // Cerrar modal
    cerrarModal();

    // Crear y añadir tarjeta visualmente
    const nuevaCard = crearTarjeta(datos);
    insertarEnOrden(nuevaCard);
  } catch (err) {
    mostrarAlerta("❌ Error: " + err.message, "error");
  }
});

// === ALERTAS TEMPORALES ===
function mostrarAlerta(mensaje, tipo = "info") {
  let alerta = document.createElement("div");
  alerta.className = `alerta ${tipo}`;
  alerta.textContent = mensaje;
  document.body.appendChild(alerta);

  setTimeout(() => {
    alerta.style.opacity = "0";
    setTimeout(() => alerta.remove(), 400);
  }, 2500);
}
