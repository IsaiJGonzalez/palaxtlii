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
            cantidad: parseInt(cells[1].innerText,10),
            precio_unitario: parseFloat(cells[2].innerText),
            subtotal: parseFloat(cells[3].innerText),
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
    const metodoPagoInput = document.querySelector('input[name="metodo_pago"]:checked');
    let metodoPago;

    if (!metodoPagoInput) {
        alert("Seleccione método de pago");
        return;
    } else {
        metodoPago = metodoPagoInput.value;
    }

    let recibido = 0;
    let cambio = 0;
    let operacionValue = "";

    if (metodoPago === "efectivo") {
        const recibidoInput = document.getElementById("recibido").value;
        if (!recibidoInput || parseFloat(recibidoInput) === 0) {
            alert("Debe declarar cuánto recibió del cliente.");
            return;
        }
        recibido = parseFloat(recibidoInput);

        const cambioInput = document.getElementById("cambio").value;
        if (!cambioInput || parseFloat(cambioInput) < 0) {
            alert("Verifique cambio negativo");
            return;
        }
        cambio = parseFloat(cambioInput);

    } else {
        operacionValue = document.getElementById("operacion").value;
        if (!operacionValue.trim()) {
            alert("Debe ingresar el número de operación.");
            return;
        }
    }


    agregarCampoOculto(form, "metodo_pago", metodoPago);
    agregarCampoOculto(form, "recibido", recibido);
    agregarCampoOculto(form, "cambio", cambio);
    agregarCampoOculto(form, "numero_operacion", operacionValue);


    // ✅ Envía el formulario
    form.requestSubmit();
}

function agregarCampoOculto(form, name, value) {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = name;
    input.value = value;
    form.appendChild(input);
}

document.getElementById('venta_form').addEventListener('submit', function (e) {

    console.log('OVERLAYYYY')

    e.preventDefault(); // Solo si quieres evitar que se envíe inmediatamente

    const overlay = document.getElementById('overlay-loading');
    overlay.classList.remove('d-none');

    document.getElementById('registrarCompra').disabled = true;

    // Si después quieres enviar el form:
    this.submit(); // solo si hiciste preventDefault antes
});
