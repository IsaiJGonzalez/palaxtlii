
//ingresar la data del pedido al modal de abonos
const abonoModal = document.getElementById('abonoModal');

abonoModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    // Extrae los valores del botón
    const folio = button.getAttribute('data-folio-a');
    const granTotal = button.getAttribute('data-gran-total-a');

    // Asigna los valores a los inputs del modal
    const inputFolio = abonoModal.querySelector('#id');
    const inputGranTotal = abonoModal.querySelector('#gran_total');

    inputFolio.value = folio || '';
    inputGranTotal.value = granTotal || '';
});



//calcúla el total restante en base a gran total - abono ingresado
document.addEventListener('DOMContentLoaded', function () {
    const granTotalInput = document.getElementById('gran_total');
    const abonoInput = document.getElementById('abono');
    const restanteInput = document.getElementById('gran_total_restante');

    function actualizarRestante() {
        const granTotal = parseFloat(granTotalInput.value) || 0;
        const abono = parseFloat(abonoInput.value) || 0;
        const restante = granTotal - abono;

        // Evita que el resultado sea negativo
        restanteInput.value = restante >= 0 ? restante.toFixed(2) : 0;
    }

    abonoInput.addEventListener('input', actualizarRestante);
});


const btnAbono = document.getElementById('btnAbono');
btnAbono.addEventListener('click',function(){
    const overlay = document.getElementById('overlay-loading');
    overlay.classList.remove('d-none');
})