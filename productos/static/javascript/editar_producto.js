function editarProducto(id, categoria, estado, existencias, nombre, precio, puntoReorden,sucursal) {

    btnEditar = document.getElementById('editarBtn');
    btnCancelar = document.getElementById('cancelarBtn');
    btnSub = document.getElementById('submit');

    btnSub.classList.add('d-none');
    btnEditar.classList.remove('d-none');
    btnCancelar.classList.remove('d-none');
     // Asignar los valores a los inputs del formulario
    $("#idP").val(id);
    $("#nombre").val(nombre);
    $("#existencias").val(existencias);
    $("#precio").val(precio);
    $("#categoria").val(categoria).trigger("change");
    $("#punto_reorden").val(puntoReorden);
    $("#estado").prop("checked", estado === 'True' || estado === 'true' || estado === '1'); // Checkbox manejado correctamente
    $("#sucursal").val(sucursal)
};

function cancelarEdicion(event){
    event.preventDefault();
    console.log('Apretado');
    window.location.reload();
}

document.addEventListener('DOMContentLoaded', function() {
    const guardarEdicion = document.getElementById('editarBtn');
    guardarEdicion.addEventListener('click', function(e) {
        e.preventDefault(); // evita comportamiento por defecto si es un submit

        const form = document.getElementById('form_productos');
        const formData = new FormData(form);

        fetch('/productos/editar_producto/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': obtenerCSRFToken() // no pongas Content-Type aquí
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta:", data);
            alert(data.mensaje || "Producto editado");
            location.reload(); 
        })
        .catch(error => console.error("Error:", error));
    });
});

function obtenerCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
