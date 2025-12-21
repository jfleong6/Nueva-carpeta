/* ==================================
   1. GESTIÓN DEL MODAL NUEVO / EDITAR
   ================================== */
const modal = document.getElementById("modal");
const form = document.getElementById("formHabitacion");
const btnAgregar = document.getElementById("btnAgregar"); // Ahora está en el Header
const btnCerrar = document.getElementById("btnCerrar");

// ====== MAPEO DE ESTADOS ======
// Este objeto centraliza toda la información visual y textual de cada estado.
const MAPEO_ESTADOS = {
    '0': {
        clase: 'mant',
        texto: 'Bloqueada',
        color: '#95a5a6',
        acciones: (id) => `
            <button class="btn-icon" onclick="desbloquear('${id}')" title="Desbloquear">🔓</button>
        `
    },
    '1': {
        clase: 'disponible',
        texto: 'Disponible',
        color: '#2ecc71',
        acciones: (id) => `
            <button class="btn-icon btn-danger-text" onclick="abrirModalBloqueo('${id}')" title="Bloquear">🚫</button>
        `
    },
    '2': {
        clase: 'ocupada',
        texto: 'Ocupada',
        color: '#e74c3c',
        acciones: (id) => `
            <button class="btn-icon btn-danger-text" onclick="abrirModalBloqueo('${id}')" title="Bloquear">🚫</button>
        `
    },
    '3': {
        clase: 'aseo',
        texto: 'Limpieza',
        color: '#f1c40f',
        acciones: (id) => `
            <button class="btn-icon btn-limpiar" onclick="marcarLimpia('${id}')" title="Marcar Limpia">🧹</button>
            <button class="btn-icon btn-danger-text" onclick="abrirModalBloqueo('${id}')" title="Bloquear">🚫</button>
        `
    },
    // Si agregas '4' = Reservada, solo añades la clave aquí:
    // '4': { clase: 'reservada', texto: 'Reservada', color: '#3498db', acciones: (id) => '...' }
};
// =============================

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
        console.log("Vamos bien")

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
        if (estado === 'todos' || fila.dataset.estado === estado) {
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

async function confirmarBloqueo() {
    const motivo = document.getElementById('motivoBloqueo').value;

    // Validar que haya motivo
    if (!motivo) return alert("Por favor selecciona un motivo");

    const datos = {
        numero: habSeleccionada, // Ej: "101"
        motivo: motivo,
        usuario_id: 1 // TODO: Cambiar por el ID del usuario logueado en sesión
    };

    try {
        const respuesta = await fetch('/api/bloquear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const data = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(data.error || "Error al bloquear");
        }

        alert(`✅ ${data.mensaje}`);
        cerrarModalBloqueo();
        actualizarFilaEstado(habSeleccionada, "0")


    } catch (err) {
        alert(`❌ Error: ${err.message}`);
    }
}

// En gestion_habitaciones.js

async function desbloquear(numeroHabitacion, habitacion) {
    if (!confirm(`¿Seguro que quieres habilitar la habitación ${habitacion}?`)) return;

    try {
        const respuesta = await fetch('/api/desbloquear', { // <-- Nueva ruta
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ numero: numeroHabitacion }) // Solo enviamos el número
        });

        const data = await respuesta.json();

        if (respuesta.ok) {
            alert('✅ Habitación ' + habitacion + ' desbloqueada.');
            // ACTUALIZACIÓN LOCAL SIN RECARGAR
            actualizarFilaEstado(numeroHabitacion, '1'); // Estado '1' es Disponible
        } else {
            // Manejar errores como "No había bloqueo activo"
            alert("❌ Error: " + data.error);
        }

    } catch (err) {
        alert("❌ Error de conexión: " + err.message);
    }
}

async function marcarLimpia(id_hab, numero) {
    // Nota: La función en el HTML debe enviar el número: onclick="marcarLimpia('{{ h.numero }}')"
    const usuario = 1;
    if (!confirm(`¿La habitación ${numero} ya está limpia y lista para ser habilitada (🟢 Disponible)?`)) {
        return;
    }

    const datos = {
        id_hab: id_hab,
        usuario: usuario,
        numero: numero,
        // No enviamos el usuario_id desde aquí, lo maneja el Backend/Sesión
    };

    try {
        const respuesta = await fetch('/api/marcar_limpia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const data = await respuesta.json();

        if (!respuesta.ok) {
            // Captura el error devuelto por el Backend
            throw new Error(data.error || "Error al marcar como limpia.");
        }

        alert(`✅ ${data.mensaje}`);

        // **ACTUALIZACIÓN VISUAL:**
        // Usamos la función existente para actualizar el estado visualmente a '1' (Disponible)
        actualizarFilaEstado(numero, '1');

    } catch (err) {
        console.error("Error al finalizar limpieza:", err);
        alert(`❌ Error al finalizar la limpieza: ${err.message}`);
    }
}


function crearNewFilaTabla(h) {
    const tr = document.createElement('tr');
    tr.className = 'fila-habitacion';
    tr.dataset.estado = h.estado;
    tr.dataset.id = h.numero;

    // Generamos el HTML de las camas dinámicamente
    let htmlCamas = '<div class="camas-wrapper">';
    if (h.cama > 0) htmlCamas += `<div class="item-cama"><img src="/static/iconos/cama.png"> <span>×${h.cama}</span></div>`;
    if (h.sencilla > 0) htmlCamas += `<div class="item-cama"><img src="/static/iconos/sencilla.png"> <span>×${h.sencilla}</span></div>`;
    if (h.camarote > 0) htmlCamas += `<div class="item-cama"><img src="/static/iconos/camarote.png"> <span>×${h.camarote}</span></div>`;
    htmlCamas += '</div>';

    tr.innerHTML = `
        <td class="col-numero"><strong>${h.numero}</strong></td>
        <td>
            <div class="dato-tipo">${h.tipo}</div>
            <span class="dato-capacidad">👤 ${h.capacidad} pers.</span>
        </td>
        <td class="col-camas">
           ${htmlCamas}
        </td>
        <td class="col-precio">$ ${h.precio_noche}</td>
        <td><span class="badge disponible">Disponible</span></td>
        <td class="text-right actions-cell">
            <button class="btn-icon btn-danger-text" onclick="abrirModalBloqueo('${h.id}')">🚫</button>
            <button class="btn-icon">✏️</button>
            <button class="btn-icon">👁️</button>
        </td>
    `;

    return tr
}
function insertarFilaTabla(datos) {
    // 1. Crear el elemento de la fila
    const nuevaFila = crearNewFilaTabla(datos); // Asumiendo que esta función existe y crea el <tr>

    const tablaBody = document.getElementById('tablaBody');
    const filasExistentes = tablaBody.querySelectorAll('tr.fila-habitacion');

    const nuevoNumero = datos.numero; // Número de la nueva habitación (ej: "607")
    let insertado = false;

    // 2. Iterar sobre las filas existentes para encontrar el punto de inserción
    for (const fila of filasExistentes) {
        const numeroExistente = fila.querySelector('.col-numero strong').textContent;

        // Comparamos alfabéticamente el nuevo número con los existentes
        if (nuevoNumero < numeroExistente) {
            // Encontró una fila con un número mayor: insertamos antes de ella
            tablaBody.insertBefore(nuevaFila, fila);
            insertado = true;
            break;
        }
    }

    // 3. Si no se insertó (es el número más grande), se añade al final
    if (!insertado) {
        tablaBody.appendChild(nuevaFila);
    }

    // 4. Aplicar el efecto de resaltado (ver paso 2)
    aplicarResaltado(nuevaFila);
}
function aplicarResaltado(fila) {
    // 1. Aplicar la clase que tiene el color de fondo amarillo
    fila.classList.add('highlight-new');

    // 2. Remover la clase después de un tiempo (1500 milisegundos = 1.5 segundos)
    setTimeout(() => {
        // La clase se remueve, y la propiedad transition de CSS hace que el color vuelva al normal lentamente.
        fila.classList.remove('highlight-new');
    }, 1500);
}
function actualizarFilaEstado(numeroHab, nuevoEstado) {
    // 1. Obtener la configuración del estado del objeto de mapeo
    const config = MAPEO_ESTADOS[nuevoEstado];
    if (!config) return; // Si el estado no existe, salimos

    // 2. Localizar la fila y actualizar el data-estado
    const fila = document.querySelector(`.fila-habitacion[data-id="${numeroHab}"]`);
    if (!fila) return;

    fila.dataset.estado = nuevoEstado;

    // 3. Actualizar el Badge de Estado visible
    const badgeCell = fila.querySelector('td:nth-child(5)');

    // Usamos la información del objeto de mapeo directamente
    const badgeHtml = `<span class="badge ${config.clase}">${config.texto}</span>`;

    badgeCell.innerHTML = badgeHtml;

    // 4. Rerenderizar los Botones de Acción (Remplazar Bloquear por Desbloquear, etc.)
    const actionsCell = fila.querySelector('.actions-cell');

    // Obtenemos el HTML de las acciones específicas del estado
    let newActionsHtml = config.acciones(numeroHab);

    // Añadimos las acciones base (Editar y Ver Detalle) que van SIEMPRE al final
    // newActionsHtml += `
    //     <button class="btn-icon" onclick="editarHabitacion('${numeroHab}')" title="Editar">✏️</button>
    //     <button class="btn-icon" onclick="verDetalle('${numeroHab}')" title="Ver Detalle">👁️</button>
    // `;

    // Insertar el nuevo HTML de Acciones
    actionsCell.innerHTML = newActionsHtml;
}

// En gestion_habitaciones.js

async function verDetalle(numero) {
    try {
        const respuesta = await fetch(`/api/habitaciones/detalle/${numero}`);
        const data = await respuesta.json();


        if (!respuesta.ok) {
            throw new Error(data.error || 'Error al cargar detalles');
        }

        // Aquí debes tener una función para construir el HTML del modal
        mostrarModalDetalles(data);
        console.log(data);

    } catch (error) {
        console.error('Fallo en verDetalle:', error);
        alert('❌ Error al cargar los detalles: ' + error.message);
    }
}

function mostrarModalDetalles(data) {
    // 1. Referencias al DOM (usando el ID del overlay principal)
    const modalOverlay = document.getElementById('modal-detalle-overlay');
    const detalleNumero = document.getElementById('detalle-numero');
    const detalleEstadoBadge = document.getElementById('detalle-estado-badge');
    const infoBasica = document.getElementById('detalle-info-basica');
    const historialBody = document.getElementById('detalle-historial-body');

    const hab = data.habitacion;
    const historial = data.historial_aseo;

    // Obtener la configuración de estado usando el MAPEO_ESTADOS global
    const configEstado = MAPEO_ESTADOS[hab.estado] || { clase: 'mant', texto: 'Desconocido', icono: '?' };

    // =======================================================
    // 2. Renderizar Encabezado (Título y Estado)
    // =======================================================

    detalleNumero.textContent = hab.numero;

    // Inyectar el Badge (Icono y Texto) en el encabezado
    detalleEstadoBadge.innerHTML =
        `<span class="badge ${configEstado.clase}">${configEstado.texto}</span>`;

    // =======================================================
    // 3. Renderizar Columna Izquierda: Información Clave
    // =======================================================

    // Se utiliza parseFloat() para limpiar los precios si vienen como string
    const precioFormateado = parseFloat(hab.precio_noche).toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    });

    // Formatear la fecha del último aseo
    let fechaAseoStr = 'Nunca';
    if (hab.fecha_ultimo_aseo) {
        const fechaAseo = new Date(hab.fecha_ultimo_aseo);
        fechaAseoStr = `${fechaAseo.toLocaleDateString()} ${fechaAseo.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    infoBasica.innerHTML = `
        <p><strong>Tipo:</strong> ${hab.tipo}</p>
        <p><strong>Capacidad:</strong> ${hab.capacidad} personas</p>
        <p><strong>Precio/Noche:</strong> ${precioFormateado}</p>
        <hr style="border: 0; border-top: 1px solid #f0f0f0; margin: 15px 0;">
        <p><strong>Camas Dobles:</strong> ${hab.cama}</p>
        <p><strong>Camas Sencillas:</strong> ${hab.sencilla}</p>
        <p><strong>Camarotes:</strong> ${hab.camarote}</p>
        <hr style="border: 0; border-top: 1px solid #f0f0f0; margin: 15px 0;">

    `;

    // =======================================================
    // 4. Renderizar Columna Derecha: Historial Simplificado
    // =======================================================

    historialBody.innerHTML = ''; // Limpiar historial previo

    if (historial && historial.length > 0) {
        historial.forEach(registro => {
            const fila = document.createElement('tr');

            const fechaInicio = new Date(registro.fecha_inicio).toLocaleString('es-CO', {
                timeZone: 'UTC',
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });



            // Estado Final
            const estadoFinal = registro.fecha_fin ? '✅ Terminado' : '🧹 ACTIVO';
            const claseEstado = registro.fecha_fin ? '' : 'historial-activo';
            const usuarioStr = registro.nombre || 'Sistema';

            // ¡Solo 3 columnas según el requisito!
            fila.innerHTML = `
                <td>${fechaInicio}</td>
                <td>${usuarioStr}</td>
            `;
            historialBody.appendChild(fila);
        });
    } else {
        // Colspan debe ser 3 para la nueva tabla
        historialBody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: #777;">No hay registros de aseo recientes.</td></tr>';
    }

    // 5. Mostrar el Modal
    // Usamos 'flex' para que el centrado CSS (modal-overlay) funcione
    modalOverlay.style.display = 'flex';
}


function cerrarModalDetalle() {
    // CAMBIO: Apuntar al OVERLAY
    const modalOverlay = document.getElementById('modal-detalle-overlay');
    modalOverlay.style.display = 'none';
}