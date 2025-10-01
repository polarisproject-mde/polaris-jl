document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const overlay = document.getElementById('overlay');
    const menu = document.getElementById('menu');
    
    // Cerrar menú al hacer clic en el overlay
    overlay.addEventListener('click', function() {
        menuToggle.checked = false;
    });
    
    // Prevenir que el clic en el menú cierre el menú
    menu.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // También cerrar con la tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && menuToggle.checked) {
            menuToggle.checked = false;
        }
    });
});
