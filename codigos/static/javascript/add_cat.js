document.addEventListener('DOMContentLoaded',function(){
    const add_cat = document.getElementById('guardar_cat');
    add_cat.addEventListener('click',function(e){
        e.preventDefault();

        const form = document.getElementById('form_cat');
        const formData = new FormData(form);

        fetch('/codigos/agregar_cat/',{
            method : 'POST',
            headers: {
                'X-CSRFToken': obtenerCSRFToken() // no pongas Content-Type aquí
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta:", data);
            alert(data.mensaje || "Categoria añadida");
            location.reload(); 
        })
        .catch(error => console.error("Error:", error));
    })
})

function obtenerCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
