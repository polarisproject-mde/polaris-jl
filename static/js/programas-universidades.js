// programas-universidades.js - VERSIÓN CORREGIDA

const API_BASE = '/api';

// Estado global
let allPrograms = [];
let filteredPrograms = [];
let allUniversities = [];
let allAreas = [];
let allModalidades = [];
let currentView = 'grid';

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Iniciando carga de programas...');
    initializePage();
});

async function initializePage() {
    try {
        console.log('📡 Cargando datos de la API...');
        showLoadingSpinner();
        
        // Cargar datos en paralelo con timeout
        const timeout = 15000; // 15 segundos máximo
        
        const [programs, universities, areas, modalidades] = await Promise.race([
            Promise.all([
                fetchWithTimeout(`${API_BASE}/programas`, timeout),
                fetchWithTimeout(`${API_BASE}/universidades`, timeout),
                fetchWithTimeout(`${API_BASE}/areas`, timeout),
                fetchWithTimeout(`${API_BASE}/modalidades`, timeout)
            ]),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout')), timeout)
            )
        ]);
        
        console.log(`✅ Datos cargados: ${programs.length} programas, ${universities.length} universidades`);
        
        allPrograms = programs;
        filteredPrograms = programs;
        allUniversities = universities;
        allAreas = areas;
        allModalidades = modalidades;
        
        // Inicializar UI
        populateFilters();
        updateStats();
        displayPrograms(filteredPrograms);
        setupEventListeners();
        
        // Mostrar secciones
        hideLoadingSpinner();
        document.getElementById('stats-section').style.display = 'grid';
        document.getElementById('filter-section').style.display = 'block';
        document.getElementById('results-section').style.display = 'block';
        
        console.log('✨ Página inicializada correctamente');
        
    } catch (error) {
        console.error('❌ Error al cargar datos:', error);
        hideLoadingSpinner();
        showError('Error al cargar la información. Por favor, recarga la página.');
    }
}

// ================================
// FETCH CON TIMEOUT
// ================================

async function fetchWithTimeout(url, timeout = 10000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('La solicitud tardó demasiado');
        }
        throw error;
    }
}

// ================================
// POBLAR FILTROS
// ================================

function populateFilters() {
    // Áreas
    const areaSelect = document.getElementById('area-conocimiento');
    areaSelect.innerHTML = '<option value="">Todas las áreas</option>';
    allAreas.forEach(area => {
        const option = document.createElement('option');
        option.value = area.id;
        option.textContent = area.nombre;
        areaSelect.appendChild(option);
    });
    
    // Modalidades
    const modalidadSelect = document.getElementById('modalidad');
    modalidadSelect.innerHTML = '<option value="">Todas las modalidades</option>';
    allModalidades.forEach(modalidad => {
        const option = document.createElement('option');
        option.value = modalidad.id;
        option.textContent = modalidad.nombre;
        modalidadSelect.appendChild(option);
    });
    
    // Universidades
    const uniSelect = document.getElementById('universidad');
    uniSelect.innerHTML = '<option value="">Todas las universidades</option>';
    allUniversities.forEach(uni => {
        const option = document.createElement('option');
        option.value = uni.id;
        option.textContent = `${uni.nombre}${uni.sigla ? ' (' + uni.sigla + ')' : ''}`;
        uniSelect.appendChild(option);
    });
}

// ================================
// ESTADÍSTICAS
// ================================

function updateStats() {
    document.getElementById('total-programs').textContent = allPrograms.length;
    document.getElementById('total-universities').textContent = allUniversities.length;
    document.getElementById('total-areas').textContent = allAreas.length;
    
    const avgDuration = allPrograms.reduce((sum, p) => sum + (p.duracion_semestres || 0), 0) / allPrograms.length;
    document.getElementById('avg-duration').textContent = `${Math.round(avgDuration)} semestres`;
}

// ================================
// EVENT LISTENERS
// ================================

function setupEventListeners() {
    // Búsqueda
    document.getElementById('btn-search').addEventListener('click', applyFilters);
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') applyFilters();
    });
    
    // Limpiar
    document.getElementById('btn-clear').addEventListener('click', clearFilters);
    
    // Ordenar
    document.getElementById('sort-select').addEventListener('change', handleSort);
    
    // Vista
    document.getElementById('btn-toggle-view').addEventListener('click', toggleView);
    
    // Reset
    const btnReset = document.getElementById('btn-reset-filters');
    if (btnReset) {
        btnReset.addEventListener('click', clearFilters);
    }
    
    // Modal
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('program-modal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

// ================================
// FILTROS
// ================================

function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
    const areaId = document.getElementById('area-conocimiento').value;
    const modalidadId = document.getElementById('modalidad').value;
    const tipoUni = document.getElementById('tipo-universidad').value;
    const uniId = document.getElementById('universidad').value;
    
    filteredPrograms = allPrograms.filter(program => {
        // Búsqueda por texto
        if (searchTerm) {
            const matchName = program.nombre.toLowerCase().includes(searchTerm);
            const matchUni = program.universidad_nombre.toLowerCase().includes(searchTerm);
            if (!matchName && !matchUni) return false;
        }
        
        // Área
        if (areaId && program.area_nombre !== allAreas.find(a => a.id == areaId)?.nombre) {
            return false;
        }
        
        // Modalidad
        if (modalidadId) {
            const modalidadName = allModalidades.find(m => m.id == modalidadId)?.nombre;
            if (!program.modalidades.includes(modalidadName)) {
                return false;
            }
        }
        
        // Tipo universidad
        if (tipoUni && program.tipo_universidad !== tipoUni) {
            return false;
        }
        
        // Universidad específica
        if (uniId && program.universidad_id != uniId) {
            return false;
        }
        
        return true;
    });
    
    displayPrograms(filteredPrograms);
}

function clearFilters() {
    document.getElementById('search-input').value = '';
    document.getElementById('area-conocimiento').value = '';
    document.getElementById('modalidad').value = '';
    document.getElementById('tipo-universidad').value = '';
    document.getElementById('universidad').value = '';
    document.getElementById('sort-select').value = 'nombre';
    
    filteredPrograms = [...allPrograms];
    displayPrograms(filteredPrograms);
}

// ================================
// ORDENAR
// ================================

function handleSort() {
    const sortBy = document.getElementById('sort-select').value;
    
    filteredPrograms.sort((a, b) => {
        switch(sortBy) {
            case 'nombre':
                return a.nombre.localeCompare(b.nombre);
            case 'universidad':
                return a.universidad_nombre.localeCompare(b.universidad_nombre);
            case 'area':
                return a.area_nombre.localeCompare(b.area_nombre);
            case 'duracion':
                return (b.duracion_semestres || 0) - (a.duracion_semestres || 0);
            default:
                return 0;
        }
    });
    
    displayPrograms(filteredPrograms);
}

// ================================
// MOSTRAR PROGRAMAS
// ================================

function displayPrograms(programs) {
    const container = document.getElementById('programs-container');
    const noResults = document.getElementById('no-results');
    const resultsCount = document.getElementById('results-count');
    
    resultsCount.textContent = `(${programs.length} programa${programs.length !== 1 ? 's' : ''})`;
    
    if (programs.length === 0) {
        container.style.display = 'none';
        noResults.style.display = 'flex';
        return;
    }
    
    container.style.display = 'grid';
    noResults.style.display = 'none';
    
    container.innerHTML = programs.map(program => createProgramCard(program)).join('');
    
    // Event listeners para cards
    document.querySelectorAll('.program-card').forEach(card => {
        card.addEventListener('click', () => {
            const programId = card.dataset.programId;
            openProgramDetail(programId);
        });
    });
}

function createProgramCard(program) {
    return `
        <div class="program-card" data-program-id="${program.id}">
            <div class="program-card-header" style="background-color: ${program.area_color};">
                <span class="program-icon">${program.area_icono}</span>
            </div>
            <div class="program-card-body">
                <h3 class="program-name">${escapeHtml(program.nombre)}</h3>
                <div class="program-university">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                        <polyline points="9 22 9 12 15 12 15 22"/>
                    </svg>
                    <span>${escapeHtml(program.universidad_nombre)}</span>
                </div>
                <div class="program-details">
                    <span class="program-detail">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        ${program.duracion_semestres} semestres
                    </span>
                    <span class="program-detail">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                        </svg>
                        ${program.creditos} créditos
                    </span>
                </div>
                ${program.modalidades.length > 0 ? `
                    <div class="program-tags">
                        ${program.modalidades.slice(0, 2).map(m => `
                            <span class="tag">${escapeHtml(m)}</span>
                        `).join('')}
                        ${program.modalidades.length > 2 ? `
                            <span class="tag">+${program.modalidades.length - 2}</span>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// ================================
// DETALLE DEL PROGRAMA
// ================================

async function openProgramDetail(programId) {
    try {
        showLoadingModal();
        
        const program = await fetchWithTimeout(`${API_BASE}/programas/${programId}`, 10000);
        
        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = createProgramDetailHTML(program);
        
        document.getElementById('modal-program-name').textContent = program.nombre;
        document.getElementById('program-modal').style.display = 'flex';
        
    } catch (error) {
        console.error('Error al cargar detalle:', error);
        alert('Error al cargar el detalle del programa');
    }
}

function createProgramDetailHTML(program) {
    return `
        <div class="program-detail-section">
            <h3>Información General</h3>
            <div class="detail-grid">
                <div class="detail-item">
                    <strong>Universidad:</strong>
                    <p>${escapeHtml(program.universidad_nombre)}</p>
                </div>
                <div class="detail-item">
                    <strong>Tipo:</strong>
                    <p>${program.tipo_universidad}</p>
                </div>
                <div class="detail-item">
                    <strong>Ciudad:</strong>
                    <p>${program.ciudad}, ${program.departamento}</p>
                </div>
                ${program.codigo_snies ? `
                <div class="detail-item">
                    <strong>Código SNIES:</strong>
                    <p>${program.codigo_snies}</p>
                </div>
                ` : ''}
            </div>
        </div>
        
        <div class="program-detail-section">
            <h3>Detalles Académicos</h3>
            <div class="detail-grid">
                <div class="detail-item">
                    <strong>Área:</strong>
                    <p>${program.area_nombre}</p>
                </div>
                <div class="detail-item">
                    <strong>Duración:</strong>
                    <p>${program.duracion_semestres} semestres</p>
                </div>
                <div class="detail-item">
                    <strong>Créditos:</strong>
                    <p>${program.creditos}</p>
                </div>
                ${program.titulo_otorgado ? `
                <div class="detail-item">
                    <strong>Título:</strong>
                    <p>${escapeHtml(program.titulo_otorgado)}</p>
                </div>
                ` : ''}
            </div>
        </div>
        
        ${program.modalidades.length > 0 ? `
        <div class="program-detail-section">
            <h3>Modalidades</h3>
            <div class="tags-container">
                ${program.modalidades.map(m => `
                    <span class="tag-large">${escapeHtml(m)}</span>
                `).join('')}
            </div>
        </div>
        ` : ''}
        
        ${program.descripcion ? `
        <div class="program-detail-section">
            <h3>Descripción</h3>
            <p>${escapeHtml(program.descripcion)}</p>
        </div>
        ` : ''}
        
        ${program.perfil_profesional ? `
        <div class="program-detail-section">
            <h3>Perfil Profesional</h3>
            <p>${escapeHtml(program.perfil_profesional)}</p>
        </div>
        ` : ''}
        
        ${program.campo_laboral && program.campo_laboral.length > 0 ? `
        <div class="program-detail-section">
            <h3>Campo Laboral</h3>
            <ul class="campo-laboral-list">
                ${program.campo_laboral.map(campo => `
                    <li>${escapeHtml(campo)}</li>
                `).join('')}
            </ul>
        </div>
        ` : ''}
        
        ${program.costo_semestre ? `
        <div class="program-detail-section">
            <h3>Inversión</h3>
            <p class="costo-info">Costo aproximado por semestre: <strong>$${formatCurrency(program.costo_semestre)}</strong></p>
        </div>
        ` : ''}
        
        ${program.campus.length > 0 ? `
        <div class="program-detail-section">
            <h3>Sedes</h3>
            <div class="campus-list">
                ${program.campus.map(campus => `
                    <div class="campus-item">
                        <h4>${escapeHtml(campus.nombre)} ${campus.es_principal ? '<span class="badge">Principal</span>' : ''}</h4>
                        <p>${escapeHtml(campus.direccion)}</p>
                        ${campus.ciudad ? `<p class="campus-city">${escapeHtml(campus.ciudad)}</p>` : ''}
                        ${campus.telefono ? `<p class="campus-phone">📞 ${campus.telefono}</p>` : ''}
                    </div>
                `).join('')}
            </div>
        </div>
        ` : ''}
        
        <div class="program-detail-section">
            <h3>Contacto</h3>
            <div class="contact-info">
                ${program.universidad_website ? `
                <p><strong>Sitio web:</strong> <a href="${program.universidad_website}" target="_blank" rel="noopener">${program.universidad_website}</a></p>
                ` : ''}
                ${program.universidad_telefono ? `
                <p><strong>Teléfono:</strong> ${program.universidad_telefono}</p>
                ` : ''}
                ${program.universidad_email ? `
                <p><strong>Email:</strong> <a href="mailto:${program.universidad_email}">${program.universidad_email}</a></p>
                ` : ''}
                ${program.universidad_direccion ? `
                <p><strong>Dirección:</strong> ${escapeHtml(program.universidad_direccion)}</p>
                ` : ''}
            </div>
        </div>
    `;
}

function closeModal() {
    document.getElementById('program-modal').style.display = 'none';
}

// ================================
// CAMBIO DE VISTA
// ================================

function toggleView() {
    const btn = document.getElementById('btn-toggle-view');
    const container = document.getElementById('programs-container');
    
    if (currentView === 'grid') {
        currentView = 'list';
        container.classList.remove('programs-grid');
        container.classList.add('programs-list');
        btn.querySelector('span').textContent = 'Vista de cuadrícula';
    } else {
        currentView = 'grid';
        container.classList.remove('programs-list');
        container.classList.add('programs-grid');
        btn.querySelector('span').textContent = 'Vista de lista';
    }
}

// ================================
// UTILIDADES
// ================================

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

function showLoadingSpinner() {
    document.getElementById('loading-spinner').style.display = 'flex';
}

function hideLoadingSpinner() {
    document.getElementById('loading-spinner').style.display = 'none';
}

function showLoadingModal() {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Cargando información...</p>
        </div>
    `;
    document.getElementById('program-modal').style.display = 'flex';
}

function showError(message) {
    const main = document.querySelector('.main-container');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <h2>Error al cargar</h2>
        <p>${message}</p>
        <button onclick="location.reload()" class="btn-primary">Recargar página</button>
    `;
    main.appendChild(errorDiv);
}