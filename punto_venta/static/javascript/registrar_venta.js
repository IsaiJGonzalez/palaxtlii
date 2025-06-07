document.getElementById("registrarCompra").addEventListener("click", function (event) {
    event.preventDefault();
    
    const total = parseFloat(document.getElementById("total").textContent) || 0;

    if (total <= 0) {
        alert("No hay registros para venta.");
        return;
    } else {
        registrarCompra();
    }
});

function registrarCompra() {
    const resumenData = [];
    const tbody = document.querySelector("#resumenTabla tbody");
    const rows = tbody.getElementsByTagName("tr");

    // Recorre solo las filas del <tbody>
    for (let row of rows) {
        const cells = row.getElementsByTagName("td");
        const rowData = {
            productoId: cells[0].getAttribute("data-id"),
            cantidad: cells[1].innerText,
            precio_unitario: cells[2].innerText,
            subtotal: cells[3].innerText,
        };
        resumenData.push(rowData);
    }

    const form = document.getElementById("venta_form");

    // 🧽 Elimina campos ocultos agregados previamente, excepto el csrfmiddlewaretoken
    const camposPrevios = form.querySelectorAll('input[type="hidden"]');
    camposPrevios.forEach(campo => {
        if (campo.name !== "csrfmiddlewaretoken") {
            campo.remove();
        }
    });


    // 📦 Agrega resumen_data en un input oculto
    agregarCampoOculto(form, "resumen_data", JSON.stringify(resumenData));

    // 🧾 Método de pago y valores asociados
    const metodoPago = document.querySelector('input[name="metodo_pago"]:checked').value;
    const recibidoValue = metodoPago === "efectivo" ? document.getElementById("recibido").value : "";
    const cambioValue = metodoPago === "efectivo" ? document.getElementById("cambio").value : "";
    const operacionValue = metodoPago !== "efectivo" ? document.getElementById("operacion").value : "";

    agregarCampoOculto(form, "metodo_pago", metodoPago);
    agregarCampoOculto(form, "recibido", recibidoValue);
    agregarCampoOculto(form, "cambio", cambioValue);
    agregarCampoOculto(form, "numero_operacion", operacionValue);

    // ✅ Envía el formulario
    form.submit();
}

function agregarCampoOculto(form, name, value) {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = name;
    input.value = value;
    form.appendChild(input);
}
