


function deleteRecord(button) {
    var recordId = button.getAttribute('data-id');
    var confirmed = confirm('¿Está seguro de eliminar este registro?');
    if (confirmed) {
        var xhr = new XMLHttpRequest();
        var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0];
        console.log(csrfToken)
        //var csrfToken = document.cookie.match(/csrfToken=([^;]+)/)[1];
        //const csrfToken = document.querySelector('input[name="_csrf"]').value;
        xhr.open('DELETE', '/formulariofundoc/delete/' + recordId);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRF-Token', csrfToken);
        xhr.onload = function() {
            if (xhr.status === 204) {
                // La solicitud se ha procesado correctamente
                // Actualizar la página o hacer cualquier otra cosa que desees
                console.log("funciono")
            } else {
                // La solicitud ha fallado
                // Mostrar un mensaje de error o hacer cualquier otra cosa que desees
                console.log("fallo")
            }
        };
        xhr.send();
    }
}
