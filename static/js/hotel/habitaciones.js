document.addEventListener("DOMContentLoaded", () => {
    const tabsList = document.getElementById("tabs-list");
    const tabsContainer = document.getElementById("tabs-container");

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

    // 🔹 Al hacer clic en una pestaña del navegador
    document.querySelectorAll(".navegador li").forEach(li => {
        li.addEventListener("click", () => activarTab(li.dataset.tab));
    });

    // 🔹 Al hacer clic en una habitación
    document.querySelectorAll(".habitacion-card").forEach(card => {
        card.addEventListener("click", () => {
            const numero = card.dataset.numero;
            const tabId = `tab-${numero}`;
            let tabContent = document.getElementById(tabId);

            // Si no existe, se crea
            if (!tabContent) {
                const li = document.createElement("li");
                li.innerHTML = `
                    Hab. ${numero}
                    <span class="cerrar-tab" title="Cerrar">×</span>
                `;
                li.dataset.tab = tabId;
                li.addEventListener("click", () => activarTab(tabId));
                tabsList.appendChild(li);

                // 🔹 Cerrar pestaña
                li.querySelector(".cerrar-tab").addEventListener("click", (e) => {
                    e.stopPropagation(); // evita activar la pestaña al cerrar
                    const tab = document.getElementById(tabId);
                    li.remove();
                    if (tab) tab.remove();

                    // volver a "Habitaciones"
                    const habitacionesTab = document.getElementById("tab-habitaciones");
                    const habitacionesLi = document.querySelector('[data-tab="tab-habitaciones"]');
                    if (habitacionesTab && habitacionesLi) activarTab("tab-habitaciones");
                });

                // 🔹 Crear iframe
                tabContent = document.createElement("iframe");
                tabContent.id = tabId;
                tabContent.classList.add("tab-content");
                tabContent.src = `/habitacion/${numero}`; // <– aquí se carga el HTML completo
                tabContent.loading = "lazy";
                tabContent.style.width = "100%";
                tabContent.style.height = "80vh";
                tabContent.style.border = "none";

                tabsContainer.appendChild(tabContent);
            }

            activarTab(tabId);
        });
    });
});
