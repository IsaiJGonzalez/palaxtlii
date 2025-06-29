//MODAL

    document.addEventListener("DOMContentLoaded", function () {
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });

        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });



// CAMBIO DE CONTRASEÑA
document.addEventListener('DOMContentLoaded', function () {
    const botones = document.querySelectorAll('.btn_cambiar_contrasena');
    const ch_emp = document.querySelector('.ch_emp');
    const div_add_emp = document.getElementById('div-form');
    const div_ch_emp = document.getElementById('ch-psw-form');
    const cancelar = document.getElementById('cancelar_ch')


    botones.forEach(boton => {
        boton.addEventListener('click', function () {
            const numero = parseInt(this.dataset.idEmpleado, 10);
            ch_emp.value = numero;

            div_add_emp.classList.add('d-none');
            div_ch_emp.classList.remove('d-none');
        });
    });

    cancelar.addEventListener('click',function(){
        div_add_emp.classList.remove('d-none');
        div_ch_emp.classList.add('d-none');
    })

});

document.addEventListener('DOMContentLoaded', function () {
    // ... tu otro código ...

    const form = document.querySelector('#ch-psw-form'); // Asegúrate de que el formulario tenga este id
    const inputUno = document.getElementById('contrasena_uno');
    const inputDos = document.getElementById('contrasena_dos');

    form.addEventListener('submit', function (e) {
        if (inputUno.value !== inputDos.value) {
            e.preventDefault(); // detiene el envío del formulario
            alert("Las contraseñas no coinciden");
            inputUno.classList.add('is-invalid');
            inputDos.classList.add('is-invalid');
        } else {
            inputUno.classList.remove('is-invalid');
            inputDos.classList.remove('is-invalid');
        }
    });
});