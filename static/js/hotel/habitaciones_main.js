/* ==================================
   1. GESTIÓN DEL MODAL NUEVO / EDITAR
   ================================== */
const modal = document.getElementById("modal");
const form = document.getElementById("formHabitacion");
const btnAgregar = document.getElementById("btnAgregar"); // Ahora está en el Header
const btnCerrar = document.getElementById("btnCerrar");

// Abrir modal
btnAgregar.addEventListener("click", () => {
    form.reset();
    modal.style.display = "flex";
});

// Cerrar modal
function cerrarModal() {
    modal.style.display = "none";
}
btnCerrar.addEventListener("click", cerrarModal);

// ENVIAR FORMULARIO (AGREGAR)
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const datos = {
        numero: form.numero.value.trim(),
        tipo: form.tipo.value.trim(),
        capacidad: parseInt(form.capacidad.value),
        cama: parseInt(form.doble.value),
        sencilla: parseInt(form.sencilla.value),
        camarote: parseInt(form.camarote.value),
        precio_noche: parseFloat(form.precio_noche.value),
        estado: 1
    };

    try {
        const respuesta = await fetch("/api/habitaciones/agregar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos),
        });

        const data = await respuesta.json();
        if (!respuesta.ok) throw new Error(data.error || "Error al guardar");

        alert("✅ " + data.mensaje);
        cerrarModal();
        
        // Agregar visualmente a la tabla (sin recargar)
        insertarFilaTabla(datos); 

    } catch (err) {
        alert("❌ Error: " + err.message);
    }
});

/* ==================================
   2. FUNCIONES DE TABLA (FILTROS)
   ================================== */

function filtrarTabla() {
    const texto = document.getElementById('buscador').value.toLowerCase();
    const filas = document.querySelectorAll('.fila-habitacion');

    filas.forEach(fila => {
        const numero = fila.querySelector('.col-numero').textContent.toLowerCase();
        fila.style.display = numero.includes(texto) ? '' : 'none';
    });
}

function filtrarEstado(estado) {
    document.querySelectorAll('.filter-pill').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    const filas = document.querySelectorAll('.fila-habitacion');
    filas.forEach(fila => {
        if(estado === 'todos' || fila.dataset.estado === estado) {
            fila.style.display = '';
        } else {
            fila.style.display = 'none';
        }
    });
}

/* ==================================
   3. ACCIONES: BLOQUEO Y LIMPIEZA
   ================================== */

let habSeleccionada = null;

function abrirModalBloqueo(numero) {
    habSeleccionada = numero;
    document.getElementById('modalBloqueo').style.display = 'flex';
}

function cerrarModalBloqueo() {
    document.getElementById('modalBloqueo').style.display = 'none';
}

function confirmarBloqueo() {
    const motivo = document.getElementById('motivoBloqueo').value;
    // Aquí iría el fetch real para actualizar estado a '0'
    alert(`Habitación ${habSeleccionada} bloqueada por: ${motivo}`);
    cerrarModalBloqueo();
    location.reload(); // Recargar para ver cambio de estado (temporal)
}

function marcarLimpia(numero) {
    if(confirm(`¿La habitación ${numero} ya está limpia y lista?`)) {
        // Fetch para actualizar estado a '1'
        alert(`Habitación ${numero} habilitada 🟢`);
        location.reload();
    }
}

/* ==================================
   4. RENDERIZADO DINÁMICO (NUEVO)
   ================================== */
function insertarFilaTabla(h) {
    const tbody = document.getElementById('tablaBody');
    const tr = document.createElement('tr');
    tr.className = 'fila-habitacion';
    tr.dataset.estado = h.estado;
    tr.dataset.id = h.numero;

    tr.innerHTML = `
        <td class="col-numero"><strong>${h.numero}</strong></td>
        <td>
            <div class="dato-tipo">${h.tipo}</div>
            <span class="dato-capacidad">👤 ${h.capacidad} pers.</span>
        </td>
        <td class="col-camas">
           <span>🛏️ Total: ${h.cama + h.sencilla + h.camarote}</span>
        </td>
        <td class="col-precio">$ ${h.precio_noche}</td>
        <td><span class="badge disponible">Disponible</span></td>
        <td class="text-right">
            <button class="btn-icon btn-danger-text" onclick="abrirModalBloqueo('${h.numero}')">🚫</button>
            <button class="btn-icon">✏️</button>
        </td>
    `;
    // Insertar al inicio
    tbody.insertBefore(tr, tbody.firstChild);
}