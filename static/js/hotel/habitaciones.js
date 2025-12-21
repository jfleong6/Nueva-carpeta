const tabsList = document.getElementById("tabs-list");
const tabsContainer = document.getElementById("tabs-container");

document.addEventListener("DOMContentLoaded", () => {
    // 🔹 Al hacer clic en una pestaña del navegador
    document.querySelectorAll(".navegador li").forEach(li => {
        li.addEventListener("click", () => activarTab(li.dataset.tab));
    });

    // 🔹 Al hacer clic en una habitación
    document.querySelectorAll(".habitacion-card").forEach(card => {
        card.addEventListener("click", () => {
            const numero = card.dataset.numero;

            if (card.classList.contains("bloqueada")) {
                abrirModalDesbloqueo(numero);
                return;
            }

            if (card.classList.contains("aseo")) {
                abrirModalAseo(numero);
                return;
            }

            if (card.classList.contains("reservada")) {
                abrirModalReservas(numero);
                return;
            }

            // disponible u ocupada → flujo normal
            abrirHabitacion(numero);
        });
    });

});

// 🔹 Activar pestaña
function activarTab(tabId) {
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("activo"));
    document.querySelectorAll(".navegador li").forEach(li => li.classList.remove("activo"));

    const targetTab = document.getElementById(tabId);
    const targetLi = document.querySelector(`.navegador li[data-tab="${tabId}"]`);

    if (targetTab && targetLi) {
        targetTab.classList.add("activo");
        targetLi.classList.add("activo");
    }
}
function abrirHabitacion(numero) {
    const tabId = `tab-${numero}`;
    let tabContent = document.getElementById(tabId);

    if (!tabContent) {
        const li = document.createElement("li");
        li.innerHTML = `
            Hab. ${numero}
            <span class="cerrar-tab" title="Cerrar">×</span>
        `;
        li.dataset.tab = tabId;
        li.addEventListener("click", () => activarTab(tabId));
        tabsList.appendChild(li);

        li.querySelector(".cerrar-tab").addEventListener("click", (e) => {
            e.stopPropagation();
            const tab = document.getElementById(tabId);
            li.remove();
            if (tab) tab.remove();
            activarTab("tab-habitaciones");
        });

        tabContent = document.createElement("iframe");
        tabContent.id = tabId;
        tabContent.classList.add("tab-content");
        tabContent.src = `/habitacion/${numero}`;
        tabContent.style.width = "100%";
        tabContent.style.height = "80vh";
        tabContent.style.border = "none";

        tabsContainer.appendChild(tabContent);
    }

    activarTab(tabId);
}

function abrirModalReservas(numero) {
    modal.innerHTML = `
        <h3>Reservas habitación ${numero}</h3>
        <div id="lista-reservas"></div>
    `;
    cargarReservas(numero);
    mostrarModal();
}
function mostrarModal({ titulo = "", cuerpo = "", footer = "" }) {
    document.getElementById("modal-title").textContent = titulo;
    document.getElementById("modal-body").innerHTML = cuerpo;
    document.getElementById("modal-footer").innerHTML = footer;

    document.getElementById("modal-overlay").classList.remove("hidden");
}
function cerrarModal() {
    document.getElementById("modal-overlay").classList.add("hidden");
    document.getElementById("modal-body").innerHTML = "";
    document.getElementById("modal-footer").innerHTML = "";
}
function abrirModalDesbloqueo(numero) {
    mostrarModal({
        titulo: `Habitación ${numero} bloqueada`,
        cuerpo: `
            <p>Esta habitación se encuentra bloqueada.</p>
            <p>¿Deseas desbloquearla para ponerla nuevamente disponible?</p>
        `,
        footer: `
            <button onclick="cerrarModal()">Cancelar</button>
            <button onclick="desbloquearHabitacion(${numero})">Desbloquear</button>
        `
    });
}

function abrirModalAseo(numero) {
    mostrarModal({
        titulo: `Aseo – Habitación ${numero}`,
        cuerpo: `
            <label for="camarera">Camarera responsable</label>
            <select id="camarera">
                <option value="">Seleccione una opción</option>
                <option value="1">Ana</option>
                <option value="2">Luisa</option>
            </select>
        `,
        footer: `
            <button onclick="cerrarModal()">Cancelar</button>
            <button onclick="finalizarAseo(${numero})">Finalizar aseo</button>
        `
    });
}




