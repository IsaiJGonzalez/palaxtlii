document.addEventListener("DOMContentLoaded", function () {
    const denominaciones = {
        billetes_1000: 1000,
        billetes_500: 500,
        billetes_200: 200,
        billetes_100: 100,
        billetes_50: 50,
        billetes_20: 20,
        monedas: 1 // El valor real de monedas se toma directamente del input como decimal
    };

    function calcularFondoCaja() {
        let total = 0;

        for (let nombre in denominaciones) {
            const input = document.querySelector(`input[name="${nombre}"]`);
            let cantidad = parseFloat(input.value) || 0;

            if (nombre === "monedas") {
                total += cantidad;
            } else {
                total += cantidad * denominaciones[nombre];
            }
        }

        // Mostrar el total en el input de fondo de caja con dos decimales
        document.getElementById("fondo_caja").value = total.toFixed(2);
    }

    // Agrega el evento a todos los inputs relevantes
    for (let nombre in denominaciones) {
        const input = document.querySelector(`input[name="${nombre}"]`);
        input.addEventListener("input", calcularFondoCaja);
    }
});

