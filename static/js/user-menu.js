// Script para el menú desplegable del usuario
document.addEventListener('DOMContentLoaded', function() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    
    if (userMenuBtn && userDropdown) {
        // Toggle del menú al hacer clic en el botón
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenuBtn.classList.toggle('active');
            userDropdown.classList.toggle('active');
        });
        
        // Cerrar el menú al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userMenuBtn.classList.remove('active');
                userDropdown.classList.remove('active');
            }
        });
        
        // Cerrar el menú al presionar ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                userMenuBtn.classList.remove('active');
                userDropdown.classList.remove('active');
            }
        });
    }
});