/* anadir_producto.js CORREGIDO */

// Variables globales
let subtotalGlobal = 0;
let totalConDescuento = 0;
let descuentoMonto = 0;
let descuentoActivo = {
    tipo: 'none',
    valor: 0,
    info: 'Ninguno',
    codigo: null
};

document.addEventListener("DOMContentLoaded", function() {

    // --- 1. REFERENCIAS A ELEMENTOS (CON VALIDACIÓN) ---
    const selectProducto = $('#producto-select');
    const cantInput = document.getElementById('cantidad');
    const precInput = document.getElementById('precio-unitario');
    const totTabInput = document.getElementById('total-tab');
    const btnAnadir = document.getElementById('btnAnadir');

    // --- 2. LOGICA DE SELECT2 Y PRECIOS ---
    if (selectProducto.length > 0) {
        selectProducto.on('select2:select', function (e) {
            const selected = e.params.data.element;
            const precio = selected.getAttribute("data-precio");
            const existencias = selected.getAttribute("data-cant");

            if (precInput) precInput.value = precio || 0;
            if (cantInput) {
                cantInput.setAttribute('placeholder', 'Max: ' + existencias);
                cantInput.value = 1;
                // Disparar evento input manualmente para calcular total inicial
                const event = new Event('input');
                cantInput.dispatchEvent(event);
            }
        });
    }

    // Función de cálculo en los inputs (fila azul)
    function calcRowInput() {
        if (!cantInput || !precInput || !totTabInput) return;
        const c = parseFloat(cantInput.value) || 0;
        const p = parseFloat(precInput.value) || 0;
        totTabInput.value = (c * p).toFixed(2);
    }

    if (cantInput) {
        cantInput.addEventListener('input', calcRowInput);
    }

    // --- 3. AGREGAR A LA TABLA ---
    if (btnAnadir) {
        btnAnadir.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (selectProducto.val() === null || selectProducto.val() === "") {
                alert("Selecciona un producto primero");
                return;
            }

            const nombre = $('#producto-select option:selected').text();
            const precio = parseFloat(precInput.value) || 0;
            const cant = parseInt(cantInput.value) || 1;
            const importe = precio * cant;
            const prodId = selectProducto.val();

            // Crear fila
            const tbody = document.querySelector('#resumenTabla tbody');
            if (tbody) {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td data-id="${prodId}">${nombre}</td>
                    <td class="text-center">${cant}</td>
                    <td class="text-end">$${precio.toFixed(2)}</td>
                    <td class="text-end fw-bold">$${importe.toFixed(2)}</td>
                    <td class="text-center">
                        <button type="button" class="btn btn-sm btn-outline-danger btn-circle btn-elim">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                `;

                // Botón eliminar
                const btnElim = row.querySelector('.btn-elim');
                if (btnElim) {
                    btnElim.addEventListener('click', function() {
                        row.remove();
                        recalcularTodo();
                    });
                }
            }

            // Limpiar
            selectProducto.val(null).trigger('change');
            if (cantInput) cantInput.value = '';
            if (precInput) precInput.value = '';
            if (totTabInput) totTabInput.value = '';

            recalcularTodo();
        });
    }

    // --- 4. DESCUENTOS (MANUAL Y TARJETA) ---
    
    // Botón Manual
    const btnManual = document.getElementById('btnAplicarManual');
    if (btnManual) {
        btnManual.addEventListener('click', function() {
            const tipoElem = document.getElementById('manual_desc_type');
            const valElem = document.getElementById('manual_desc_val');
            
            if (!tipoElem || !valElem) return;

            const valorInput = parseFloat(valElem.value) || 0;
            if (valorInput <= 0) {
                alert("Ingrese un valor válido");
                return;
            }

            descuentoActivo = {
                tipo: tipoElem.value === '%' ? 'manual_percent' : 'manual_fixed',
                valor: valorInput,
                info: `Manual ${valorInput}${tipoElem.value}`,
                codigo: null
            };
            recalcularTodo();
            alert("Descuento aplicado.");
        });
    }

    // Botón Tarjeta
    const btnTarjeta = document.getElementById('btnBuscarTarjeta');
    if (btnTarjeta) {
        btnTarjeta.addEventListener('click', function() {
            const codeElem = document.getElementById('card_code_input');
            const msgDiv = document.getElementById('card_msg');
            
            if (!codeElem) return;
            // Lo que el usuario escribe/escanea (La REFERENCIA)
            const referenciaInput = codeElem.value.trim(); 

            if (msgDiv) msgDiv.textContent = "";

            let tarjetaEncontrada = null;
            let keyInterna = null; // 'san_valentin'

            // BUCLES PARA BUSCAR POR REFERENCIA
            // TARJETAS_DB es un objeto: { 'san_valentin': {referencia: '...', ...}, 'otro': {...} }
            if (typeof TARJETAS_DB !== 'undefined') {
                for (const [key, data] of Object.entries(TARJETAS_DB)) {
                    // Comparamos como string para evitar errores de tipos
                    if (String(data.referencia) === String(referenciaInput)) {
                        tarjetaEncontrada = data;
                        keyInterna = key;
                        break; // Ya la encontramos
                    }
                }
            }

            if (tarjetaEncontrada) {
                // Validar activo y existencias
                if (tarjetaEncontrada.activo === false || (tarjetaEncontrada.existencias !== undefined && tarjetaEncontrada.existencias <= 0)) {
                    if (msgDiv) {
                        msgDiv.className = 'small mt-1 fw-bold text-danger';
                        msgDiv.textContent = "Tarjeta agotada o inactiva.";
                    }
                    return;
                }

                // Guardamos el descuento
                descuentoActivo = {
                    tipo: tarjetaEncontrada.tipo === '%' ? 'card_percent' : 'card_fixed',
                    valor: parseFloat(tarjetaEncontrada.descuento),
                    info: `Ref: ${referenciaInput} (${tarjetaEncontrada.descuento}${tarjetaEncontrada.tipo})`,
                    codigo: keyInterna // GUARDAMOS 'san_valentin' PARA EL BACKEND
                };

                recalcularTodo();
                
                if (msgDiv) {
                    msgDiv.className = 'small mt-1 fw-bold text-success';
                    msgDiv.textContent = "Tarjeta válida.";
                }

                // Asignar al input oculto
                const hiddenCode = document.getElementById('hidden_card_code');
                if(hiddenCode) hiddenCode.value = keyInterna;

            } else {
                // No encontrada
                descuentoActivo = { tipo: 'none', valor: 0, info: 'Ninguno', codigo: null };
                recalcularTodo();
                if (msgDiv) {
                    msgDiv.className = 'small mt-1 fw-bold text-danger';
                    msgDiv.textContent = "Referencia no encontrada.";
                }
                const hiddenCode = document.getElementById('hidden_card_code');
                if(hiddenCode) hiddenCode.value = '';
            }
        });
    }

    // Reset al cambiar tabs
    const tabs = document.querySelectorAll('button[data-bs-toggle="pill"]');
    if (tabs) {
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', function (event) {
                if (event.target.id === 'pills-none-tab') {
                    descuentoActivo = { tipo: 'none', valor: 0, info: 'Ninguno', codigo: null };
                    recalcularTodo();
                    
                    const manualIn = document.getElementById('manual_desc_val');
                    const cardIn = document.getElementById('card_code_input');
                    const msgDiv = document.getElementById('card_msg');
                    
                    if (manualIn) manualIn.value = '';
                    if (cardIn) cardIn.value = '';
                    if (msgDiv) msgDiv.textContent = '';
                }
            });
        });
    }
});

// --- FUNCION MAESTRA DE RECALCULO ---
function recalcularTodo() {
    let subtotal = 0;
    const rows = document.querySelectorAll('#resumenTabla tbody tr');
    
    rows.forEach(r => {
        // Asumiendo columna 3 es el importe
        if (r.cells.length > 3) {
            const txt = r.cells[3].textContent.replace('$','').trim();
            subtotal += parseFloat(txt) || 0;
        }
    });

    subtotalGlobal = subtotal;

    // Calcular descuento
    let descuento = 0;
    if (descuentoActivo.tipo === 'manual_percent' || descuentoActivo.tipo === 'card_percent') {
        descuento = subtotal * (descuentoActivo.valor / 100);
    } else if (descuentoActivo.tipo === 'manual_fixed' || descuentoActivo.tipo === 'card_fixed') {
        descuento = descuentoActivo.valor;
    }

    if (descuento > subtotal) descuento = subtotal;

    descuentoMonto = descuento;
    totalConDescuento = subtotal - descuento;

    // Actualizar UI
    const subElem = document.getElementById('subtotal_display');
    const totElem = document.getElementById('total');
    const modalTot = document.getElementById('modal_total_confirm');
    const descRow = document.getElementById('row_descuento_display');
    const descLabel = document.getElementById('desc_label_display');
    const descMonto = document.getElementById('desc_monto_display');

    if (subElem) subElem.textContent = subtotal.toFixed(2);
    if (totElem) totElem.textContent = totalConDescuento.toFixed(2);
    if (modalTot) modalTot.textContent = '$' + totalConDescuento.toFixed(2);

    if (descRow && descLabel && descMonto) {
        if (descuento > 0) {
            descRow.style.setProperty('display', 'flex', 'important');
            descLabel.textContent = descuentoActivo.info;
            descMonto.textContent = descuento.toFixed(2);
        } else {
            descRow.style.setProperty('display', 'none', 'important');
        }
    }

    // Actualizar Inputs Hidden
    const hTotal = document.getElementById('hidden_total_final');
    const hDescM = document.getElementById('hidden_desc_monto');
    const hDescI = document.getElementById('hidden_desc_info');
    
    if (hTotal) hTotal.value = totalConDescuento.toFixed(2);
    if (hDescM) hDescM.value = descuentoMonto.toFixed(2);
    if (hDescI) hDescI.value = descuentoActivo.info;

    // Input hidden para tarjeta
    let cardInput = document.getElementById('hidden_card_code');
    if (!cardInput) {
        const form = document.getElementById('venta_form');
        if (form) {
            cardInput = document.createElement('input');
            cardInput.type = 'hidden';
            cardInput.id = 'hidden_card_code';
            cardInput.name = 'codigo_tarjeta_usada';
            form.appendChild(cardInput);
        }
    }
    if (cardInput) cardInput.value = descuentoActivo.codigo || '';

    // Notificar cambio
    if (totElem) {
        const evt = new Event('change');
        totElem.dispatchEvent(evt);
    }
}