// Variables
const addBecaBtn = document.getElementById('addBecaBtn');
const addBecaModal = document.getElementById('addBecaModal');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const becaForm = document.getElementById('becaForm');
const becasGrid = document.getElementById('becasGrid');
const searchInput = document.getElementById('searchInput');
const filterBtns = document.querySelectorAll('.filter-btn');

// User menu dropdown
const userMenuBtn = document.getElementById('userMenuBtn');
const userDropdown = document.getElementById('userDropdown');

if (userMenuBtn) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userMenuBtn.classList.toggle('active');
        userDropdown.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
            userMenuBtn.classList.remove('active');
            userDropdown.classList.remove('active');
        }
    });
}

// Abrir modal
addBecaBtn.addEventListener('click', () => {
    addBecaModal.classList.add('active');
    document.body.style.overflow = 'hidden';
});

// Cerrar modal
closeModal.addEventListener('click', () => {
    addBecaModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    becaForm.reset();
});

cancelBtn.addEventListener('click', () => {
    addBecaModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    becaForm.reset();
});

// Cerrar modal al hacer clic fuera
addBecaModal.addEventListener('click', (e) => {
    if (e.target === addBecaModal) {
        addBecaModal.classList.remove('active');
        document.body.style.overflow = 'auto';
        becaForm.reset();
    }
});

// Función para obtener el badge HTML según el tipo
function getBadgeHTML(tipo) {
    const badges = {
        'completas': '<span class="beca-badge completa">Beca Completa</span>',
        'creditos': '<span class="beca-badge credito">Crédito</span>',
        'parciales': '<span class="beca-badge parcial">Beca Parcial</span>'
    };
    return badges[tipo] || '';
}

// Función para obtener el ícono según el tipo
function getIconSVG(tipo) {
    if (tipo === 'creditos') {
        return `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                    <line x1="1" y1="10" x2="23" y2="10"></line>
                </svg>`;
    } else {
        return `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                    <path d="M6 12v5c3 3 9 3 12 0v-5"/>
                </svg>`;
    }
}

// Enviar formulario
becaForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Obtener valores
    const nombre = document.getElementById('becaNombre').value;
    const organizacion = document.getElementById('becaOrganizacion').value;
    const tipo = document.getElementById('becaTipo').value;
    const descripcion = document.getElementById('becaDescripcion').value;
    const ubicacion = document.getElementById('becaUbicacion').value;
    const convocatoria = document.getElementById('becaConvocatoria').value;
    const url = document.getElementById('becaUrl').value;
    
    // Crear nueva tarjeta de beca
    const nuevaBeca = document.createElement('article');
    nuevaBeca.className = 'beca-card';
    nuevaBeca.setAttribute('data-category', tipo);
    
    nuevaBeca.innerHTML = `
        <div class="beca-header">
            <div class="beca-logo">
                ${getIconSVG(tipo)}
            </div>
            ${getBadgeHTML(tipo)}
        </div>
        <div class="beca-content">
            <h3>${nombre}</h3>
            <p class="beca-organization">${organizacion}</p>
            <p class="beca-description">${descripcion}</p>
            <div class="beca-details">
                <div class="detail-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 1 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>${ubicacion}</span>
                </div>
                <div class="detail-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <span>${convocatoria}</span>
                </div>
            </div>
        </div>
        <div class="beca-footer">
            <a href="${url}" target="_blank" class="beca-link">
                Más información
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
            </a>
        </div>
    `;
    
    // Agregar al grid
    becasGrid.appendChild(nuevaBeca);
    
    // Cerrar modal y resetear
    addBecaModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    becaForm.reset();
    
    // Animación de entrada
    nuevaBeca.style.opacity = '0';
    nuevaBeca.style.transform = 'translateY(20px)';
    setTimeout(() => {
        nuevaBeca.style.transition = 'all 0.3s ease';
        nuevaBeca.style.opacity = '1';
        nuevaBeca.style.transform = 'translateY(0)';
    }, 100);
});

// Filtros
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remover active de todos los botones
        filterBtns.forEach(b => b.classList.remove('active'));
        
        // Agregar active al botón clickeado
        btn.classList.add('active');
        
        // Obtener categoría
        const filter = btn.getAttribute('data-filter');
        
        // Filtrar becas
        const becaCards = document.querySelectorAll('.beca-card');
        becaCards.forEach(card => {
            if (filter === 'all') {
                card.classList.remove('hidden');
                // Animación de aparición
                card.style.animation = 'fadeIn 0.3s ease';
            } else {
                const category = card.getAttribute('data-category');
                if (category === filter) {
                    card.classList.remove('hidden');
                    card.style.animation = 'fadeIn 0.3s ease';
                } else {
                    card.classList.add('hidden');
                }
            }
        });
    });
});

// Búsqueda
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();
    const becaCards = document.querySelectorAll('.beca-card');
    
    becaCards.forEach(card => {
        const nombre = card.querySelector('h3').textContent.toLowerCase();
        const organizacion = card.querySelector('.beca-organization').textContent.toLowerCase();
        const descripcion = card.querySelector('.beca-description').textContent.toLowerCase();
        
        const match = nombre.includes(searchTerm) || 
                     organizacion.includes(searchTerm) || 
                     descripcion.includes(searchTerm);
        
        if (match) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
    
    // Si hay un filtro activo, aplicarlo después de la búsqueda
    const activeFilter = document.querySelector('.filter-btn.active');
    if (activeFilter && activeFilter.getAttribute('data-filter') !== 'all') {
        const filter = activeFilter.getAttribute('data-filter');
        becaCards.forEach(card => {
            if (!card.classList.contains('hidden')) {
                const category = card.getAttribute('data-category');
                if (category !== filter) {
                    card.classList.add('hidden');
                }
            }
        });
    }
});

// Animación de fade in para las tarjetas
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);