window.onload = function() {
    setTimeout(function() {
        // Ocultar la pantalla de carga
        document.getElementById('loadingScreen').style.display = 'none';

        // Mostrar el encabezado, la sección principal y el footer
        document.getElementById('mainHeader').style.display = 'block';
        document.getElementById('mainSection').style.display = 'block';
        document.getElementById('mainFooter').style.display = 'block';
    }, 500); // Retraso de 500ms para asegurar que los elementos estén listos

    // Verifica si hay un mensaje de error
    if (errorMessage) {
        // Asigna el mensaje de error al contenido del modal
        document.getElementById('errorMessage').textContent = errorMessage;
    
        // Muestra el modal
        var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
        errorModal.show();
    }
};
const registerError = "{{ register_error|default('') }}";
if (registerError) {
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
};




