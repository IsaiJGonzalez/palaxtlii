document.addEventListener('DOMContentLoaded', () => {
    let btn_vv = document.getElementById('btn_vv');
    let btn_vm = document.getElementById('btn_vm');
    let div_vv = document.getElementById('vv_div');
    let div_vm = document.getElementById('vm_div');

    btn_vv.addEventListener('click', () => cambiarVistaVentas('vista_hermosa'));
    btn_vm.addEventListener('click', () => cambiarVistaVentas('moctezuma'));

    function cambiarVistaVentas(sucursal) {
        btn_vv.classList.remove('btn-success', 'btn-secondary');
        btn_vm.classList.remove('btn-success', 'btn-secondary');
        div_vv.classList.remove('d-none');
        div_vm.classList.remove('d-none');

        if (sucursal === 'vista_hermosa') {
            btn_vv.classList.add('btn-success');
            btn_vm.classList.add('btn-secondary');
            div_vm.classList.add('d-none');
        } else if (sucursal === 'moctezuma') {
            btn_vm.classList.add('btn-success');
            btn_vv.classList.add('btn-secondary');
            div_vv.classList.add('d-none');
        }
    }

    // Mostrar por defecto Vista Hermosa
    cambiarVistaVentas('vista_hermosa');
});
