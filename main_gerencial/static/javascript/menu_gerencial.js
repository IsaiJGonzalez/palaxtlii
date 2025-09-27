document.addEventListener('DOMContentLoaded', () => {

    // Definir primero las variables
    let btn_prvh = document.getElementById('btn_prvh');
    let btn_prmc = document.getElementById('btn_prmc');
    let div_vh = document.getElementById('vhp');
    let div_mc = document.getElementById('mcp');


    // Luego agregar los listeners
    btn_prvh.addEventListener('click', () => cambiarProductos('vista_hermosa'));
    btn_prmc.addEventListener('click', () => cambiarProductos('moctezuma'));

    function cambiarProductos(sucursal) {
        // Eliminar clases anteriores
        btn_prvh.classList.remove('btn-success', 'btn-secondary');
        btn_prmc.classList.remove('btn-success', 'btn-secondary');
        div_vh.classList.remove('d-none');
        div_mc.classList.remove('d-none');


        // Agregar las nuevas clases según la sucursal
        if (sucursal === 'vista_hermosa') {
            btn_prvh.classList.add('btn-success');
            btn_prmc.classList.add('btn-secondary');
            div_mc.classList.add('d-none');
        } else if (sucursal === 'moctezuma') {
            btn_prmc.classList.add('btn-success');
            btn_prvh.classList.add('btn-secondary');
            div_vh.classList.add('d-none')
        }
    }

    // Si quieres iniciar con una opción activa
    cambiarProductos('vista_hermosa');
});



document.addEventListener("DOMContentLoaded", function () {
        var exampleModal = document.getElementById("pedidoModal");

        exampleModal.addEventListener("show.bs.modal", function (event) {
            var button = event.relatedTarget;  // Botón que activó el modal
            //var anticipo = button.getAttribute("data-anticipo");
            const anticipo = button.getAttribute('data-anticipo');
            var at_no_emp = button.getAttribute("data-at-no_emp");
            var at_nom_emp = button.getAttribute("data-at-nom-emp");
            var cel = button.getAttribute("data-cel");
            var direccion = button.getAttribute("data-direccion");
            var especificaciones = button.getAttribute("data-especificaciones");
            var estado = button.getAttribute("data-estado");
            var fecha_entrega = button.getAttribute("data-fecha-entrega");
            var folio = button.getAttribute("data-folio");
            var forma_entrega = button.getAttribute("data-forma-entrega");
            var gran_total = button.getAttribute("data-gran-total");
            var hora_entrega = button.getAttribute("data-hora-entrega");
            var metodo_pago = button.getAttribute("data-metodo-pago");
            var mix_ef = button.getAttribute("data-mix-ef");
            var mix_tar = button.getAttribute("data-mix-tar");
            var nombre_cliente = button.getAttribute("data-nombre-cliente");
            var num_operacion = button.getAttribute("data-num_operacion");
            var recibe = button.getAttribute("data-recibe");
            var referencias = button.getAttribute("data-referencias");
            var sucursal = button.getAttribute("data-sucursal");
            var telefono = button.getAttribute("data-telefono");
            var total = button.getAttribute("data-total");

            const div_pagos = document.getElementById('forma_de_pago');

            // Asignar los valores a los elementos dentro del modal

            document.getElementById("folio_r").innerText = "Folio: " + folio;
            document.getElementById("no_emp").innerText = at_no_emp;
            document.getElementById("nom_emp").innerText = at_nom_emp;

            document.getElementById("fecha_entrega").innerText = fecha_entrega.split(" a las")[0];
            document.getElementById("hora_entrega").innerText = hora_entrega;
            if (forma_entrega == "envio") {
                document.getElementById('lugar').innerText = direccion + " " + 'Recibe: ' + recibe + ', Cel: ' + cel
            } else if (forma_entrega == 'tienda') {
                document.getElementById('lugar').innerText = 'Sucursal ' + (parseInt(sucursal) === 1 ? "Vista Hermosa" : (parseInt(sucursal) === 2 ? "Moctezuma" : "Desconocido"));
            }

            document.getElementById('cliente').innerText = 'Cliente: ' + nombre_cliente;
            document.getElementById('telefono').innerText = 'Teléfono: ' + telefono;

            document.getElementById('total').innerText = 'Total: ' + '$' + total;
            document.getElementById("anticipo").innerText = 'Anticipó: ' + '$' + anticipo;
            document.getElementById('restante').innerText = 'Pago Restante: ' + '$' + gran_total;
            document.getElementById('especificaciones').innerText = especificaciones;
            
            document.getElementById('pagado').setAttribute('data-folio',folio)
            

            if (gran_total != 0) {
                div_pagos.classList.remove('d-none');
            }


        });
});



//PAGADO
document.getElementById('pagado').addEventListener('click', function() {
    const folio = this.getAttribute('data-folio'); // Obtiene el folio asignado
    const pagoInput = document.querySelector('input[name="pago"]:checked'); // Verifica si hay pago seleccionado

    if (!pagoInput) {
        alert('Por favor, selecciona una forma de pago antes de continuar.');
        return;
    }

    const pagoSeleccionado = pagoInput.value;

    enviarFolio(folio,pagoSeleccionado,'Pedido actualizado correctamente.');
});


document.querySelectorAll('.entregado_directo').forEach(boton => {
    boton.addEventListener('click', function() {
        const folio = this.getAttribute('data-folio_ed');
        if (confirm('¿Desea marcar como entregado?')) {
            enviarFolio(folio,null,'Pedido marcado como entregado.');
        }
    });
});


// Función reutilizable para enviar el folio al backend
function enviarFolio(folio,pagoSeleccionado,mensajeExito) {
    fetch('/pedidos/act_pedido_estado/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ folio,pagoSeleccionado })
    })
    .then(response => response.text())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        alert(mensajeExito);
        location.reload(); // Recarga la página para reflejar los cambios
    })
    .catch(error => console.error('Error:', error));
}

// Función para obtener el token CSRF de Django
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


//olverlau
document.getElementById('registrarAbonoBtn').addEventListener('click', function () {
    document.getElementById('overlay').style.display = 'flex';
    // Aquí puedes continuar con tu lógica de envío o validación
});
