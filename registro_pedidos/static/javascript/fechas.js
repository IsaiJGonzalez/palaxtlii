document.addEventListener('DOMContentLoaded', () => {
    const fechaActual = new Date();
    const dia = String(fechaActual.getDate()).padStart(2, '0'); // Día en formato 2 dígitos
    const mes = String(fechaActual.getMonth() + 1).padStart(2, '0'); // Mes (enero es 0)
    const anio = fechaActual.getFullYear(); // Año completo

    console.log(dia,mes,anio)

    document.getElementById('dia_reg').value = dia;
    document.getElementById('mes_reg').value = mes;
    document.getElementById('a_reg').value = anio;
});