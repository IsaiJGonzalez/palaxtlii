document.addEventListener("DOMContentLoaded", function () {
        var exampleModal = document.getElementById("productoModal");

        exampleModal.addEventListener("show.bs.modal", function (event) {
            let button = event.relatedTarget; 
            let categoria = button.getAttribute("data-categoria");
            let estadoP = button.getAttribute("data-estado");
            console.log(estadoP)
            let estado = estadoP === 'True' ? 'Activo' : 'Inactivo'
            let existencias = button.getAttribute("data-existencias");
            let nombre = button.getAttribute("data-nombre");
            let precio = button.getAttribute("data-precio");
            let puntoReorden = button.getAttribute("data-reorden");
            
            // Asignar los valores a los elementos dentro del modal
            document.getElementById("modalNombre").innerText = "Nombre: " + nombre;
            document.getElementById("modalCategoria").innerText = "Categoría: " + categoria;
            document.getElementById("modalPrecio").innerText = "Precio: $" + precio;
            document.getElementById("modalReorden").innerText = "Reorden: " + puntoReorden;
            document.getElementById("modalExistencias").innerText = "Existencias: " + existencias;
            document.getElementById("modalEstado").innerText = "Estado: " + estado;
        });



});
