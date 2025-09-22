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
            productoNombre : cells[0].textContent.trim(),
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
    let mix_ef = 0;
    let mix_tar = 0;

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
        //obtener la operación de la tarjeta
        if (metodoPago === "tarjeta"){
            operacionValue = document.getElementById("operacion").value;
            if (!operacionValue.trim()) {
                alert("Debe ingresar el número de operación de la tarjeta.");
                return;
            }
        }
        //operacion transferencia
        if (metodoPago === "transferencia"){
            operacionValue = document.getElementById("operacion_transferencia").value;
            if (!operacionValue.trim()) {
                alert("Debe ingresar el número de operación de la transferencia.");
                return;
            }
        }
        
        //operación mixta
        if (metodoPago === "mixto"){

            //traer lo que se paga en efectivo y en tarjeta
            const mix_efInput = document.getElementById("mix_ef").value;
            if (!mix_efInput  || parseFloat(mix_efInput) === 0){
                alert("Debe declarar cuánto se pagará en efectivo.");
                return;
            }
            mix_ef = parseFloat(mix_efInput);

            const mix_tarInput = document.getElementById("mix_tar").value;
            if (!mix_tarInput || parseFloat(mix_tarInput) === 0){
                alert("Debe declarar cuánto se pagará en tarjeta/transferencia");
                return;
            }
            mix_tar = parseFloat(mix_tarInput);

            //traer el recibido y el cambio
            const recibidoInput = document.getElementById("recibido_mixto").value;
            if (!recibidoInput || parseFloat(recibidoInput) === 0) {
                alert("Debe declarar cuánto recibió del cliente.");
                return;
            }
            recibido = parseFloat(recibidoInput);

            const cambioInput = document.getElementById("cambio_mixto").value;
            if (!cambioInput || parseFloat(cambioInput) < 0) {
                alert("Verifique cambio negativo");
                return;
            }
            cambio = parseFloat(cambioInput);
            
            //traer el numero de operación
            operacionValue = document.getElementById("operacion_mixto").value;
            if (!operacionValue.trim()) {
                alert("Debe ingresar el número de operación de la transferencia.");
                return;
            }


        }
    }


    agregarCampoOculto(form, "metodo_pago", metodoPago);
    agregarCampoOculto(form, "recibido", recibido);
    agregarCampoOculto(form, "cambio", cambio);
    agregarCampoOculto(form, "numero_operacion", operacionValue);
    agregarCampoOculto(form, "mix_ef", mix_ef);
    agregarCampoOculto(form, "mix_tar", mix_tar);


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
