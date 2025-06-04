document.getElementById('pagado').addEventListener('click', function() {
    const folio = this.getAttribute('data-folio'); // Obtiene el folio asignado
    const pagoSeleccionado = document.querySelector('input[name="pago"]:checked'); // Verifica si hay pago seleccionado

    if (!pagoSeleccionado) {
        alert('Por favor, selecciona una forma de pago antes de continuar.');
        return;
    }

    enviarFolio(folio, 'Pedido actualizado correctamente.');
});

// Nueva lógica para el botón "entregado_directo"
document.getElementById('entregado_directo').addEventListener('click', function() {
    const folio = this.getAttribute('data-folio_ed'); // Obtiene el folio asignado
    
    if (confirm('¿Desea marcar como entregado?')) { // Confirma la acción antes de ejecutar
        enviarFolio(folio, 'Pedido marcado como entregado.');
    }
});

// Función reutilizable para enviar el folio al backend
function enviarFolio(folio, mensajeExito) {
    fetch('/pedidos/act_pedido_estado/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ folio })
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