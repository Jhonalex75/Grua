document.addEventListener("DOMContentLoaded", function() {
    console.log("Scripts cargados correctamente.");

    // ==============================
    // Confirmación antes de eliminar registros
    // ==============================
    const deleteButtons = document.querySelectorAll(".btn-delete");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            const url = this.getAttribute("data-url");
            if (confirm("¿Estás seguro de que deseas eliminar este registro? Esta acción no se puede deshacer.")) {
                window.location.href = url;
            }
        });
    });

    // ==============================
    // Notificaciones automáticas (desaparecen después de 5s)
    // ==============================
    setTimeout(() => {
        let alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            alert.classList.add("fade-out");
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);

    // ==============================
    // Vista previa de archivos adjuntos
    // ==============================
    const fileInputs = document.querySelectorAll("input[type='file']");
    fileInputs.forEach(input => {
        input.addEventListener("change", function(event) {
            const previewContainer = document.createElement("div");
            previewContainer.classList.add("file-preview");

            Array.from(event.target.files).forEach(file => {
                const fileReader = new FileReader();
                fileReader.onload = function(e) {
                    let previewElement;
                    if (file.type.startsWith("image/")) {
                        previewElement = document.createElement("img");
                        previewElement.src = e.target.result;
                        previewElement.classList.add("img-thumbnail", "me-2");
                        previewElement.style.maxWidth = "100px";
                    } else {
                        previewElement = document.createElement("p");
                        previewElement.textContent = file.name;
                        previewElement.classList.add("file-name");
                    }
                    previewContainer.appendChild(previewElement);
                };
                fileReader.readAsDataURL(file);
            });

            if (this.parentNode.querySelector(".file-preview")) {
                this.parentNode.querySelector(".file-preview").remove();
            }
            this.parentNode.appendChild(previewContainer);
        });
    });

    // ==============================
    // Validaciones en formularios
    // ==============================
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function(event) {
            let isValid = true;
            const inputs = this.querySelectorAll("input[required], textarea[required], select[required]");
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add("is-invalid");
                } else {
                    input.classList.remove("is-invalid");
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert("Por favor, completa todos los campos requeridos.");
            }
        });
    });

    // ==============================
    // Resaltado de filas en la tabla
    // ==============================
    const tableRows = document.querySelectorAll("table tbody tr");
    tableRows.forEach(row => {
        row.addEventListener("mouseenter", function() {
            this.classList.add("table-hover-row");
        });
        row.addEventListener("mouseleave", function() {
            this.classList.remove("table-hover-row");
        });
    });

    // ==============================
    // Desplazamiento suave a secciones específicas
    // ==============================
    const smoothScrollLinks = document.querySelectorAll("a[href^='#']");
    smoothScrollLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 50,
                    behavior: "smooth"
                });
            }
        });
    });

    // ==============================
    // Mostrar modal de eliminación (para actividades y equipos)
    // ==============================
    window.confirmarEliminacion = function(activityId) {
        const modal = new bootstrap.Modal(document.getElementById("deleteModal"));
        const deleteForm = document.getElementById("deleteForm");
        deleteForm.action = `/activity/delete/${activityId}`;
        modal.show();
    };
});
