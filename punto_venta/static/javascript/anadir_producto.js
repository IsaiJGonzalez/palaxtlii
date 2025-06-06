document.addEventListener("DOMContentLoaded", function() {
    const cantidadInput = document.getElementById('cantidad');
    const precioInput = document.getElementById('precio-unitario');
    const totalInput = document.getElementById('total-tab');

    function actualizarTotal() {
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const precio = parseFloat(precioInput.value) || 0;
        totalInput.value = (cantidad * precio).toFixed(2); // Calcula y muestra el total con 2 decimales
    }

    // Ejecutar actualización cada vez que cambien los valores
    cantidadInput.addEventListener('input', actualizarTotal);
    precioInput.addEventListener('input', actualizarTotal);
});



document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('btnAnadir').addEventListener('click', function(event) {
        event.preventDefault();

        const formData = new FormData(document.getElementById('venta_form'));

        // Productos
        const productoId = formData.get('producto_id'); // ID del producto
        const selectElement = document.getElementById('producto-select');
        const productoNombre = selectElement.options[selectElement.selectedIndex].text; // Nombre del producto

        // Cantidad
        const cantidad = formData.get('cantidad') || 1; // Asegura un valor por defecto

        // Precio unitario y total
        const precio_unitario = parseFloat(formData.get('precio-unitario')) || 0;
        const total_tab = parseFloat(formData.get('total-tab')) || 0;

        // Tabla de productos
        const table = document.getElementById('resumenTabla');
        const newRow = table.insertRow();
        newRow.innerHTML = `
            <td data-id='${productoId}' >${productoNombre}</td>
            <td>${cantidad}</td>
            <td>${precio_unitario.toFixed(2)}</td>
            <td>${total_tab.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-outline-warning btn-circle btn-editar editarBtn">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger btn-circle btn-elim eliminarBtn">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;


        //AÑADIENDO ACCIONES A LOS BOTONES DE EDITAR Y ELIMINAR
        newRow.querySelector('.editarBtn').addEventListener('click',function(){
            editarFila(newRow);
        })

        newRow.querySelector(".btn-elim").addEventListener("click", function() {
            eliminarFila(newRow);
        });


        //LIMPIANDO EL FORM
        $('#producto-select').val(null).trigger('change');
        document.getElementById('cantidad').value='';
        document.getElementById('precio-unitario').value='';
        document.getElementById('total-tab').value='';
        document.getElementById('producto-select').value='';


        actualizarTotalTabla();

        //actualizando el total

    });

});

//FUNCION DE EDITAR FILA
function editarFila(row){

    //obteniendo la id del total para restar directamente el subtotal del producto
    const total =  document.getElementById('total');

    const productoCell = row.cells[0];
    const cantidadCell = row.cells[1];
    const precio_unitarioCell = row.cells[2];
    const subtotalCell = row.cells[3];

    const productoId = productoCell.getAttribute('data-id');
    const producto = productoCell.textContent;

    const cantidad = parseInt(cantidadCell.textContent);

    const prec_uni= parseInt(precio_unitarioCell.textContent);

    const subtotal = parseInt(subtotalCell.textContent);

    console.log(productoId, producto, cantidad, prec_uni, subtotal);

    //tengo que restarle los cosos ajsajs


    $('#producto-select').val(productoId).trigger('change');
    document.getElementById('cantidad').value = cantidad;
    document.getElementById('precio-unitario').value = prec_uni;
    document.getElementById('total-tab').value = subtotal;

    //restando subtotal del producto del total
    const newTotal = parseInt(total.textContent) - subtotal;
    total.textContent = newTotal;


    eliminarFilaParaEditar(row);

}

//eliminar fila para su edicion
function eliminarFilaParaEditar(row){
    row.remove();
}


//eliminar fila 
function eliminarFila(row){
    
    const subtotalCell = row.cells[3];
    const subtotal = parseInt(subtotalCell.textContent);
    
    const total =  document.getElementById('total');
    const currentTotal = parseInt(total.textContent) || 0;

    const newTotal = currentTotal - subtotal;
    total.textContent = newTotal;
    
    row.remove();
}



//CAMBIO DE ACUERDO A LO RECIBIDO
document.addEventListener("DOMContentLoaded", function() {
    const totalElement = document.getElementById('total'); // Captura el elemento donde está el total
    const metodoEfectivo = document.getElementById('metodo_efectivo');
    const recibidoInput = document.getElementById('recibido');
    const cambioOutput = document.getElementById('cambio');

    function calcularCambio() {
        const total = parseFloat(totalElement.textContent) || 0; // Convierte el total a número
        const recibido = parseFloat(recibidoInput.value) || 0; // Convierte lo recibido a número
        
        if (metodoEfectivo.checked) { // Verifica si el método "Efectivo" está seleccionado
            const cambio = recibido - total;
            cambioOutput.value = cambio.toFixed(2); // Muestra el cambio con dos decimales
        } else {
            cambioOutput.value = '0.00'; // Si otro método está seleccionado, el cambio es 0
            recibidoInput.value = '0.00';
        }
    }

    // Actualiza el cambio cada vez que cambien el método de pago o el monto recibido
    metodoEfectivo.addEventListener('change', calcularCambio);
    recibidoInput.addEventListener('input', calcularCambio);
});

function actualizarTotalTabla() {
    let total = 0;
    const filas = document.querySelectorAll('#resumenTabla tr'); // Todas las filas de la tabla

    filas.forEach(fila => {
        const subtotalElemento = fila.querySelector('td:nth-child(4)'); // La columna del subtotal
        if (subtotalElemento) {
            const subtotal = parseFloat(subtotalElemento.textContent.replace('$', '')) || 0;
            total += subtotal;
        }
    });

    document.getElementById('total').textContent = total.toFixed(2); // Actualiza el total
}