document.addEventListener('DOMContentLoaded', () => {

    // Definir primero las variables
    let btn_prvh = document.getElementById('btn_prvh');
    let btn_prmc = document.getElementById('btn_prmc');
    let div_vh = document.getElementById('vhp');
    let div_mc = document.getElementById('mcp');


    // Luego agregar los listeners
    btn_prvh.addEventListener('click', () => cambiarProductos('vista_hermosa'));
    btn_prmc.addEventListener('click', () => cambiarProductos('moctezuma'));

    function cambiarProductos(sucursal) {
        // Eliminar clases anteriores
        btn_prvh.classList.remove('btn-success', 'btn-secondary');
        btn_prmc.classList.remove('btn-success', 'btn-secondary');
        div_vh.classList.remove('d-none');
        div_mc.classList.remove('d-none');


        // Agregar las nuevas clases según la sucursal
        if (sucursal === 'vista_hermosa') {
            btn_prvh.classList.add('btn-success');
            btn_prmc.classList.add('btn-secondary');
            div_mc.classList.add('d-none');
        } else if (sucursal === 'moctezuma') {
            btn_prmc.classList.add('btn-success');
            btn_prvh.classList.add('btn-secondary');
            div_vh.classList.add('d-none')
        }
    }

    // Si quieres iniciar con una opción activa
    cambiarProductos('vista_hermosa');
});
