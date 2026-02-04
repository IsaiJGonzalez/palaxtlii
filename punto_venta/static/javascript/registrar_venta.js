/* registrar_venta.js - VERSIÓN FINAL BLINDADA */

document.addEventListener("DOMContentLoaded", function () {

    // --- ELEMENTOS PARA BLOQUEO EN TIEMPO REAL ---
    const btnCobrar = document.querySelector('button[data-bs-target="#ticketModal"]');
    const totalSpan = document.getElementById('total');
    const recibidoIn = document.getElementById('recibido');
    const operacionIn = document.getElementById('operacion');
    const mixEf = document.getElementById('mix_ef');
    const mixRec = document.getElementById('recibido_mixto');
    const opMix = document.getElementById('operacion_mixto');

    function validarYBloquear() {
        if (!btnCobrar) return;
        
        const total = parseFloat(totalSpan.textContent.replace(/[^\d.-]/g, '')) || 0;
        const metodoInput = document.querySelector('input[name="metodo_pago"]:checked');
        
        // REGLA ORO: Si no hay productos, bloquear siempre
        const numProds = document.querySelectorAll("#resumenTabla tbody tr").length;
        if (numProds === 0) {
            btnCobrar.disabled = true;
            btnCobrar.classList.add('opacity-50');
            return;
        }

        // Si el total es 0 (por cupón), habilitar siempre (es cortesía)
        if (total <= 0) {
            btnCobrar.disabled = false;
            btnCobrar.classList.remove('opacity-50');
            return;
        }

        // Si no hay método seleccionado y el total > 0, bloquear
        if (!metodoInput) {
            btnCobrar.disabled = true;
            btnCobrar.classList.add('opacity-50');
            return;
        }

        const metodo = metodoInput.value;
        let esValido = false;

        if (metodo === 'efectivo') {
            const recibido = parseFloat(recibidoIn.value) || 0;
            esValido = recibido >= total && recibidoIn.value.trim() !== "";
        } 
        else if (metodo === 'tarjeta' || metodo === 'transferencia') {
            esValido = operacionIn.value.trim() !== "";
        } 
        else if (metodo === 'mixto') {
            const mEf = parseFloat(mixEf.value) || 0;
            const mRec = parseFloat(mixRec.value) || 0;
            const mOp = opMix.value.trim();
            esValido = mEf > 0 && mOp !== "" && mRec >= mEf;
        }

        btnCobrar.disabled = !esValido;
        if (esValido) {
            btnCobrar.classList.remove('opacity-50');
        } else {
            btnCobrar.classList.add('opacity-50');
        }
    }

    // 1. SELECCIÓN DE PAGO (Visual y lógica)
    const opcionesPago = document.querySelectorAll('.payment-option');
    opcionesPago.forEach(op => {
        op.addEventListener('click', function () {
            opcionesPago.forEach(o => o.classList.remove('bg-light', 'border-primary', 'text-primary', 'selected'));
            this.classList.add('selected', 'bg-light', 'border-primary', 'text-primary');

            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
                radio.dispatchEvent(new Event('change'));
            }
        });
    });

    // 2. MOSTRAR/OCULTAR CAMPOS
    const radios = document.getElementsByName('metodo_pago');
    radios.forEach(r => {
        r.addEventListener('change', function () {
            const idsToHide = ['efectivo-fields', 'operacion-fields', 'mixto-fields', 'msg-select-payment'];
            idsToHide.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.add('d-none');
            });

            if (this.value === 'efectivo') {
                document.getElementById('efectivo-fields').classList.remove('d-none');
                setTimeout(() => recibidoIn.focus(), 100);
                calcCambio();
            }
            else if (this.value === 'tarjeta' || this.value === 'transferencia') {
                document.getElementById('operacion-fields').classList.remove('d-none');
                setTimeout(() => operacionIn.focus(), 100);
            }
            else if (this.value === 'mixto') {
                document.getElementById('mixto-fields').classList.remove('d-none');
                setTimeout(() => mixEf.focus(), 100);
                calcMixto();
            }
            validarYBloquear();
        });
    });

    // 3. LISTENERS DE INPUT
    [recibidoIn, operacionIn, mixEf, mixRec, opMix].forEach(input => {
        if (input) input.addEventListener('input', () => {
            if (input.id === 'recibido') calcCambio();
            if (input.id === 'mix_ef' || input.id === 'recibido_mixto') calcMixto();
            validarYBloquear();
        });
    });

    function calcCambio() {
        const total = parseFloat(totalSpan.textContent.replace(/[^\d.-]/g, '')) || 0;
        const recibido = parseFloat(recibidoIn.value) || 0;
        const visual = document.getElementById('cambio_visual');
        if (recibido >= total) {
            visual.value = "$" + (recibido - total).toFixed(2);
            visual.classList.replace('text-danger', 'text-success');
            document.getElementById('cambio').value = (recibido - total).toFixed(2);
        } else {
            visual.value = "Faltan $" + (total - recibido).toFixed(2);
            visual.classList.replace('text-success', 'text-danger');
            document.getElementById('cambio').value = 0;
        }
    }

    function calcMixto() {
        const total = parseFloat(totalSpan.textContent.replace(/[^\d.-]/g, '')) || 0;
        const montoEfectivo = parseFloat(mixEf.value) || 0;
        const restante = Math.max(0, total - montoEfectivo);
        document.getElementById('mix_tar').value = restante.toFixed(2);

        const entregado = parseFloat(mixRec.value) || 0;
        const txt = document.getElementById('cambio_mixto_txt');
        if (entregado >= montoEfectivo) {
            txt.textContent = "$" + (entregado - montoEfectivo).toFixed(2);
            txt.className = "fw-bold text-success";
            document.getElementById('cambio_mixto').value = (entregado - montoEfectivo).toFixed(2);
        } else {
            txt.textContent = "Falta efectivo";
            txt.className = "fw-bold text-danger";
            document.getElementById('cambio_mixto').value = 0;
        }
    }

    const observer = new MutationObserver(validarYBloquear);
    if (totalSpan) observer.observe(totalSpan, { childList: true, characterData: true, subtree: true });

    document.getElementById("btnImprimirTicket").addEventListener("click", () => ejecutarVenta(1));
    document.getElementById("btnSinTicket").addEventListener("click", () => ejecutarVenta(0));

    validarYBloquear();
});

// FUNCIÓN DE ENVÍO FINAL
function ejecutarVenta(opcionTicket) {
    const form = document.getElementById("venta_form");
    const metodoInput = document.querySelector('input[name="metodo_pago"]:checked');
    const totalVenta = parseFloat(document.getElementById("total").textContent.replace(/[^\d.-]/g, '')) || 0;

    // --- ARREGLO PARA TOTAL $0 (Cortesía) ---
    // Si el total es 0, forzamos que el método sea efectivo para evitar el error None: 0
    let metodoFinal = "";
    if (totalVenta <= 0) {
        metodoFinal = "efectivo";
    } else {
        metodoFinal = metodoInput.value;
    }

    // Sincronizar datos mixtos
    if (metodoFinal === 'mixto') {
        document.getElementById('recibido').value = document.getElementById('recibido_mixto').value;
        document.getElementById('operacion').value = document.getElementById('operacion_mixto').value;
        document.getElementById('cambio').value = document.getElementById('cambio_mixto').value;
    }

    // Asegurar que el método de pago viaje al servidor
    let inputMetodo = form.querySelector('input[name="metodo_pago_final"]');
    if (!inputMetodo) {
        inputMetodo = document.createElement("input");
        inputMetodo.type = "hidden";
        inputMetodo.name = "metodo_pago";
        form.appendChild(inputMetodo);
    }
    inputMetodo.value = metodoFinal;

    // Campos ocultos de ticket y resumen
    let inputTicket = form.querySelector('input[name="ticket"]') || document.createElement("input");
    inputTicket.type = "hidden"; inputTicket.name = "ticket"; inputTicket.value = opcionTicket;
    form.appendChild(inputTicket);

    const resumenData = [];
    document.querySelectorAll("#resumenTabla tbody tr").forEach(row => {
        resumenData.push({
            productoId: row.cells[0].getAttribute("data-id"),
            productoNombre: row.cells[0].textContent.trim(),
            cantidad: parseInt(row.cells[1].textContent),
            precio_unitario: parseFloat(row.cells[2].textContent.replace(/[^\d.-]/g, '')),
            subtotal: parseFloat(row.cells[3].textContent.replace(/[^\d.-]/g, ''))
        });
    });
    
    let inputResumen = form.querySelector('input[name="resumen_data"]') || document.createElement("input");
    inputResumen.type = "hidden"; inputResumen.name = "resumen_data"; inputResumen.value = JSON.stringify(resumenData);
    form.appendChild(inputResumen);

    document.getElementById('overlay-loading').classList.remove('d-none');
    form.submit();
}