class UniversidadesApp {
    constructor() {
        this.universities = [];
        this.filteredUniversities = [];
        this.filters = {
            area: '',
            modalidad: '',
            tipo: '',
            nivel: '',
            duracion: '',
            search: ''
        };
        this.currentSort = 'nombre';
        this.isListView = false;
        
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadData();
        this.renderAll();
    }

    // Event Listeners
    bindEvents() {
        // Búsqueda
        document.getElementById('btn-search').addEventListener('click', () => this.applyFilters());
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.applyFilters();
        });
        
        // Filtros
        document.getElementById('area-conocimiento').addEventListener('change', () => this.applyFilters());
        document.getElementById('modalidad').addEventListener('change', () => this.applyFilters());
        document.getElementById('tipo-universidad').addEventListener('change', () => this.applyFilters());
        document.getElementById('nivel-educativo').addEventListener('change', () => this.applyFilters());
        document.getElementById('duracion').addEventListener('change', () => this.applyFilters());
        
        // Botones de control
        document.getElementById('btn-clear').addEventListener('click', () => this.clearFilters());
        document.getElementById('btn-reset-filters').addEventListener('click', () => this.clearFilters());
        document.getElementById('sort-select').addEventListener('change', (e) => this.sortResults(e.target.value));
        document.getElementById('btn-toggle-view').addEventListener('click', () => this.toggleView());
        
        // Modal
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal') || e.target.classList.contains('modal-close')) {
                this.closeModal();
            }
        });
    }

    // Carga de datos desde la API/BD
    async loadData() {
        try {
            this.showLoading();
            
            // Aquí deberías hacer las llamadas a tu API/backend
            // Por ahora, simulo datos basados en tu estructura de BD
            const [universities, areas, modalidades, niveles, duraciones] = await Promise.all([
                this.fetchUniversities(),
                this.fetchAreas(),
                this.fetchModalidades(),
                this.fetchNiveles(),
                this.fetchDuraciones()
            ]);
            
            this.universities = universities;
            this.filteredUniversities = [...universities];
            
            this.populateFilters({
                areas,
                modalidades,
                niveles,
                duraciones
            });
            
            this.hideLoading();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Error al cargar los datos. Intenta recargar la página.');
        }
    }

    // Simulación de llamadas a API - reemplazar con llamadas reales
    async fetchUniversities() {
        // Simular delay de red
        await this.delay(1000);
        
        return [
            {
                id: 1,
                nombre: "Universidad de Antioquia",
                sigla: "UdeA",
                tipo_universidad: "Pública",
                ciudad: "Medellín",
                departamento: "Antioquia",
                direccion: "Calle 70 No 52-21",
                telefono: "(574) 219-8332",
                website: "https://www.udea.edu.co",
                activo: true,
                campus: [
                    {
                        id: 1,
                        nombre: "Campus Central",
                        direccion: "Calle 70 No 52-21",
                        principal: true
                    },
                    {
                        id: 2,
                        nombre: "Campus Robledo",
                        direccion: "Carrera 53 No 61-30",
                        principal: false
                    }
                ],
                programas: [
                    {
                        id: 1,
                        nombre: "Medicina",
                        codigo_snies: "101",
                        duracion_semestres: 12,
                        creditos: 240,
                        area: "Ciencias de la Salud",
                        nivel: "Pregrado",
                        modalidades: ["Presencial"]
                    },
                    {
                        id: 2,
                        nombre: "Ingeniería de Sistemas",
                        codigo_snies: "102",
                        duracion_semestres: 10,
                        creditos: 180,
                        area: "Ingeniería",
                        nivel: "Pregrado",
                        modalidades: ["Presencial", "Virtual"]
                    }
                ],
                total_programas: 89
            },
            {
                id: 2,
                nombre: "Universidad EAFIT",
                sigla: "EAFIT",
                tipo_universidad: "Privada",
                ciudad: "Medellín",
                departamento: "Antioquia",
                direccion: "Carrera 49 No 7 Sur-50",
                telefono: "(574) 261-9500",
                website: "https://www.eafit.edu.co",
                activo: true,
                campus: [
                    {
                        id: 3,
                        nombre: "Campus El Poblado",
                        direccion: "Carrera 49 No 7 Sur-50",
                        principal: true
                    }
                ],
                programas: [
                    {
                        id: 3,
                        nombre: "Administración de Empresas",
                        codigo_snies: "201",
                        duracion_semestres: 8,
                        creditos: 144,
                        area: "Economía y Negocios",
                        nivel: "Pregrado",
                        modalidades: ["Presencial"]
                    },
                    {
                        id: 4,
                        nombre: "Ingeniería de Sistemas",
                        codigo_snies: "202",
                        duracion_semestres: 10,
                        creditos: 162,
                        area: "Ingeniería",
                        nivel: "Pregrado",
                        modalidades: ["Presencial"]
                    }
                ],
                total_programas: 45
            },
            // Más universidades simuladas...
            {
                id: 3,
                nombre: "Universidad Pontificia Bolivariana",
                sigla: "UPB",
                tipo_universidad: "Privada",
                ciudad: "Medellín",
                departamento: "Antioquia",
                direccion: "Circular 1 No 70-01",
                telefono: "(574) 448-8388",
                website: "https://www.upb.edu.co",
                activo: true,
                campus: [
                    {
                        id: 4,
                        nombre: "Campus Laureles",
                        direccion: "Circular 1 No 70-01",
                        principal: true
                    }
                ],
                programas: [
                    {
                        id: 5,
                        nombre: "Arquitectura",
                        codigo_snies: "301",
                        duracion_semestres: 10,
                        creditos: 170,
                        area: "Arquitectura y Diseño",
                        nivel: "Pregrado",
                        modalidades: ["Presencial"]
                    }
                ],
                total_programas: 67
            }
        ];
    }

    async fetchAreas() {
        await this.delay(500);
        return [
            { id: 1, nombre: "Ingeniería", color_hex: "#2E86C1", icono: "🔧" },
            { id: 2, nombre: "Ciencias de la Salud", color_hex: "#E74C3C", icono: "🏥" },
            { id: 3, nombre: "Humanidades", color_hex: "#8E44AD", icono: "📚" },
            { id: 4, nombre: "Economía y Negocios", color_hex: "#F39C12", icono: "💼" },
            { id: 5, nombre: "Ciencias Sociales", color_hex: "#27AE60", icono: "👥" },
            { id: 6, nombre: "Arquitectura y Diseño", color_hex: "#E67E22", icono: "🎨" }
        ];
    }

    async fetchModalidades() {
        await this.delay(300);
        return [
            { id: 1, nombre: "Presencial", descripcion: "Clases presenciales" },
            { id: 2, nombre: "Virtual", descripcion: "Clases en línea" },
            { id: 3, nombre: "Híbrida", descripcion: "Combinación presencial y virtual" }
        ];
    }

    async fetchNiveles() {
        await this.delay(300);
        return [
            { id: 1, nombre: "Pregrado", orden: 1 },
            { id: 2, nombre: "Especialización", orden: 2 },
            { id: 3, nombre: "Maestría", orden: 3 },
            { id: 4, nombre: "Doctorado", orden: 4 }
        ];
    }

    async fetchDuraciones() {
        await this.delay(300);
        return [
            { id: 1, rango: "Corta (1-4 semestres)", min_semestres: 1, max_semestres: 4, orden: 1 },
            { id: 2, rango: "Media (5-8 semestres)", min_semestres: 5, max_semestres: 8, orden: 2 },
            { id: 3, rango: "Larga (9-12 semestres)", min_semestres: 9, max_semestres: 12, orden: 3 },
            { id: 4, rango: "Muy larga (más de 12 semestres)", min_semestres: 13, max_semestres: 20, orden: 4 }
        ];
    }

    // Utilidades
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Poblar filtros
    populateFilters(data) {
        this.populateSelect('area-conocimiento', data.areas, 'nombre');
        this.populateSelect('modalidad', data.modalidades, 'nombre');
        this.populateSelect('nivel-educativo', data.niveles, 'nombre');
        this.populateSelect('duracion', data.duraciones, 'rango');
    }

    populateSelect(selectId, options, valueField) {
        const select = document.getElementById(selectId);
        const currentOptions = Array.from(select.querySelectorAll('option:not([value=""])'));
        currentOptions.forEach(option => option.remove());
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option[valueField];
            optionElement.textContent = option[valueField];
            select.appendChild(optionElement);
        });
    }

    // Manejo de loading
    showLoading() {
        document.getElementById('loading-spinner').style.display = 'flex';
        document.getElementById('stats-section').style.display = 'none';
        document.getElementById('filter-section').style.display = 'none';
        document.getElementById('results-section').style.display = 'none';
    }

    hideLoading() {
        document.getElementById('loading-spinner').style.display = 'none';
        document.getElementById('stats-section').style.display = 'grid';
        document.getElementById('filter-section').style.display = 'block';
        document.getElementById('results-section').style.display = 'block';
    }

    showError(message) {
        // Implementar manejo de errores
        alert(message);
    }

    // Render principal
    renderAll() {
        this.renderStats();
        this.renderUniversities();
    }

    renderStats() {
        const totalUnis = this.universities.length;
        const totalPrograms = this.universities.reduce((sum, uni) => sum + uni.total_programas, 0);
        const publicUnis = this.universities.filter(uni => uni.tipo_universidad === 'Pública').length;
        const privateUnis = this.universities.filter(uni => uni.tipo_universidad === 'Privada').length;

        document.getElementById('total-universities').textContent = totalUnis;
        document.getElementById('total-programs').textContent = `${totalPrograms}+`;
        document.getElementById('public-unis').textContent = publicUnis;
        document.getElementById('private-unis').textContent = privateUnis;
    }

    // Filtros y búsqueda
    applyFilters() {
        this.filters.area = document.getElementById('area-conocimiento').value;
        this.filters.modalidad = document.getElementById('modalidad').value;
        this.filters.tipo = document.getElementById('tipo-universidad').value;
        this.filters.nivel = document.getElementById('nivel-educativo').value;
        this.filters.duracion = document.getElementById('duracion').value;
        this.filters.search = document.getElementById('search-input').value.toLowerCase();

        this.filteredUniversities = this.universities.filter(uni => {
            // Filtro por búsqueda (nombre universidad o programas)
            const matchesSearch = !this.filters.search || 
                uni.nombre.toLowerCase().includes(this.filters.search) ||
                uni.programas.some(prog => prog.nombre.toLowerCase().includes(this.filters.search));

            // Filtro por área de conocimiento
            const matchesArea = !this.filters.area ||
                uni.programas.some(prog => prog.area === this.filters.area);

            // Filtro por modalidad
            const matchesModalidad = !this.filters.modalidad ||
                uni.programas.some(prog => prog.modalidades.includes(this.filters.modalidad));

            // Filtro por tipo de universidad
            const matchesTipo = !this.filters.tipo || uni.tipo_universidad === this.filters.tipo;

            // Filtro por nivel educativo
            const matchesNivel = !this.filters.nivel ||
                uni.programas.some(prog => prog.nivel === this.filters.nivel);

            // Filtro por duración (necesitaría lógica más compleja con los rangos)
            const matchesDuracion = !this.filters.duracion || this.matchesDurationFilter(uni, this.filters.duracion);

            return matchesSearch && matchesArea && matchesModalidad && matchesTipo && matchesNivel && matchesDuracion;
        });

        this.sortResults(this.currentSort);
        this.renderUniversities();
    }

    matchesDurationFilter(university, durationFilter) {
        // Implementar lógica de filtro por duración basada en los rangos de la BD
        // Por ahora, retorno true
        return true;
    }

    clearFilters() {
        document.getElementById('search-input').value = '';
        document.getElementById('area-conocimiento').value = '';
        document.getElementById('modalidad').value = '';
        document.getElementById('tipo-universidad').value = '';
        document.getElementById('nivel-educativo').value = '';
        document.getElementById('duracion').value = '';
        
        this.filters = {
            area: '',
            modalidad: '',
            tipo: '',
            nivel: '',
            duracion: '',
            search: ''
        };
        
        this.filteredUniversities = [...this.universities];
        this.renderUniversities();
    }

    // Ordenamiento
    sortResults(sortBy) {
        this.currentSort = sortBy;
        
        this.filteredUniversities.sort((a, b) => {
            switch (sortBy) {
                case 'nombre':
                    return a.nombre.localeCompare(b.nombre);
                case 'tipo_universidad':
                    return a.tipo_universidad.localeCompare(b.tipo_universidad);
                case 'total_programas':
                    return b.total_programas - a.total_programas;
                case 'sigla':
                    return a.sigla.localeCompare(b.sigla);
                default:
                    return 0;
            }
        });
        
        this.renderUniversities();
    }

    // Toggle vista
    toggleView() {
        this.isListView = !this.isListView;
        const container = document.getElementById('universities-container');
        const button = document.getElementById('btn-toggle-view');
        
        if (this.isListView) {
            container.className = 'universities-list';
            button.innerHTML = '<span>Vista de tarjetas</span>';
        } else {
            container.className = 'universities-grid';
            button.innerHTML = '<span>Vista de lista</span>';
        }
        
        this.renderUniversities();
    }

    // Render universidades
    renderUniversities() {
        const container = document.getElementById('universities-container');
        const noResults = document.getElementById('no-results');
        const resultsCount = document.getElementById('results-count');
        
        if (this.filteredUniversities.length === 0) {
            container.innerHTML = '';
            noResults.style.display = 'block';
            resultsCount.textContent = '(0 universidades)';
            return;
        }
        
        noResults.style.display = 'none';
        resultsCount.textContent = `(${this.filteredUniversities.length} universidades)`;
        
        container.innerHTML = '';
        
        this.filteredUniversities.forEach((uni, index) => {
            const card = this.createUniversityCard(uni, index);
            container.appendChild(card);
        });
    }

    createUniversityCard(uni, index) {
        const card = document.createElement('div');
        card.className = `university-card ${this.isListView ? 'list-view' : ''}`;
        card.style.animationDelay = `${index * 0.1}s`;
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Ver detalles de ${uni.nombre}`);
        
        // Obtener área principal para el indicador de color
        const mainArea = uni.programas[0]?.area || 'Sin área';
        const areaColor = this.getAreaColor(mainArea);
        
        // Obtener programas destacados (máximo 4)
        const featuredPrograms = uni.programas.slice(0, 4);
        
        // Obtener campus principales
        const mainCampus = uni.campus.filter(c => c.principal)[0] || uni.campus[0];
        const campusList = uni.campus.length > 1 ? 
            `${mainCampus.nombre} (+${uni.campus.length - 1} más)` : 
            mainCampus.nombre;
        
        card.innerHTML = `
            <div class="area-indicator" style="background-color: ${areaColor}"></div>
            
            <div class="university-header">
                <div class="university-logo">${uni.sigla}</div>
                <div class="university-info">
                    <h3>${uni.nombre}</h3>
                    <span class="university-type">${uni.tipo_universidad}</span>
                </div>
            </div>
            
            <div class="university-details">
                <div class="detail-item">
                    <div class="detail-icon"></div>
                    <span>${uni.total_programas} programas</span>
                </div>
                <div class="detail-item">
                    <div class="detail-icon"></div>
                    <span>${uni.ciudad}, ${uni.departamento}</span>
                </div>
                <div class="detail-item">
                    <div class="detail-icon"></div>
                    <span>Teléfono: ${uni.telefono}</span>
                </div>
                <div class="detail-item">
                    <div class="detail-icon"></div>
                    <span>Campus: ${campusList}</span>
                </div>
            </div>
            
            <div class="programs-preview">
                <h4>Programas destacados:</h4>
                <div class="programs-tags">
                    ${featuredPrograms.map(prog => 
                        `<span class="program-tag">${prog.nombre}</span>`
                    ).join('')}
                </div>
            </div>
            
            <div class="campus-info">
                <h4>Campus principal:</h4>
                <div class="campus-list">${mainCampus.direccion}</div>
            </div>
            
            <div class="university-actions">
                <button class="btn-primary" onclick="window.open('${uni.website}', '_blank')" 
                        aria-label="Visitar sitio web de ${uni.nombre}">
                    Ver sitio web
                </button>
                <button class="btn-secondary" onclick="universidadesApp.showUniversityDetails(${uni.id})"
                        aria-label="Ver más detalles de ${uni.nombre}">
                    Ver detalles
                </button>
            </div>
        `;
        
        // Agregar evento de clic para abrir modal
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.university-actions')) {
                this.showUniversityDetails(uni.id);
            }
        });
        
        // Soporte para teclado
        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.showUniversityDetails(uni.id);
            }
        });
        
        return card;
    }

    getAreaColor(areaName) {
        const areaColors = {
            'Ingeniería': '#2E86C1',
            'Ciencias de la Salud': '#E74C3C',
            'Humanidades': '#8E44AD',
            'Economía y Negocios': '#F39C12',
            'Ciencias Sociales': '#27AE60',
            'Arquitectura y Diseño': '#E67E22',
            'Ciencias Básicas': '#3498DB',
            'Educación': '#16A085'
        };
        return areaColors[areaName] || '#95A5A6';
    }

    // Modal de detalles
    showUniversityDetails(universityId) {
        const university = this.universities.find(uni => uni.id === universityId);
        if (!university) return;
        
        const modal = document.getElementById('university-modal');
        const modalTitle = document.getElementById('modal-university-name');
        const modalBody = document.getElementById('modal-body');
        
        modalTitle.textContent = university.nombre;
        
        modalBody.innerHTML = this.createUniversityDetailContent(university);
        
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        modal.querySelector('.modal-close').focus();
    }

    createUniversityDetailContent(uni) {
        return `
            <div class="modal-section">
                <h3>Información General</h3>
                <div class="contact-info">
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Tipo:</strong> ${uni.tipo_universidad}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Ciudad:</strong> ${uni.ciudad}, ${uni.departamento}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Dirección:</strong> ${uni.direccion}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Teléfono:</strong> ${uni.telefono}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Sitio web:</strong> <a href="${uni.website}" target="_blank" style="color: #010c1e;">${uni.website}</a></span>
                    </div>
                </div>
            </div>

            <div class="modal-section">
                <h3>Campus (${uni.campus.length})</h3>
                <div class="modal-campus-grid">
                    ${uni.campus.map(campus => `
                        <div class="modal-campus-card">
                            <h4>${campus.nombre} ${campus.principal ? '(Principal)' : ''}</h4>
                            <p><strong>Dirección:</strong> ${campus.direccion}</p>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="modal-section">
                <h3>Programas Académicos (${uni.programas.length})</h3>
                <div class="modal-programs-grid">
                    ${uni.programas.map(programa => `
                        <div class="modal-program-card">
                            <h4>${programa.nombre}</h4>
                            <div class="modal-program-details">
                                <div><strong>Código SNIES:</strong> ${programa.codigo_snies}</div>
                                <div><strong>Nivel:</strong> ${programa.nivel}</div>
                                <div><strong>Área:</strong> ${programa.area}</div>
                                <div><strong>Duración:</strong> ${programa.duracion_semestres} semestres</div>
                                <div><strong>Créditos:</strong> ${programa.creditos}</div>
                                <div><strong>Modalidades:</strong> ${programa.modalidades.join(', ')}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="modal-section">
                <h3>Estadísticas</h3>
                <div class="contact-info">
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Total de programas:</strong> ${uni.total_programas}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Programas de pregrado:</strong> ${uni.programas.filter(p => p.nivel === 'Pregrado').length}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Programas de posgrado:</strong> ${uni.programas.filter(p => p.nivel !== 'Pregrado').length}</span>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon"></div>
                        <span><strong>Modalidades disponibles:</strong> ${this.getUniqueModalidades(uni).join(', ')}</span>
                    </div>
                </div>
            </div>
        `;
    }

    getUniqueModalidades(university) {
        const modalidades = new Set();
        university.programas.forEach(programa => {
            programa.modalidades.forEach(modalidad => modalidades.add(modalidad));
        });
        return Array.from(modalidades);
    }

    closeModal() {
        const modal = document.getElementById('university-modal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Funciones de utilidad
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Manejo de errores
    handleError(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        // Aquí podrías implementar un sistema de notificaciones más sofisticado
        const errorMessage = `Ha ocurrido un error${context ? ` en ${context}` : ''}. Por favor, intenta nuevamente.`;
        this.showNotification(errorMessage, 'error');
    }

    showNotification(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#e74c3c' : '#27ae60'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            font-family: 'Montserrat', sans-serif;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
        
        // Permitir cerrar haciendo clic
        notification.addEventListener('click', () => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });
    }

    // Funciones para integración con backend real
    async callAPI(endpoint, options = {}) {
        try {
            const baseURL = '/api'; // Ajustar según tu configuración
            const response = await fetch(`${baseURL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            this.handleError(error, `API call to ${endpoint}`);
            throw error;
        }
    }

    // Métodos para llamadas reales a la API (reemplazar los métodos simulados)
    async fetchUniversitiesReal() {
        return this.callAPI('/universidades?ciudad=Medellín');
    }

    async fetchAreasReal() {
        return this.callAPI('/areas-conocimiento');
    }

    async fetchModalidadesReal() {
        return this.callAPI('/modalidades');
    }

    async fetchNivelesReal() {
        return this.callAPI('/niveles-educativos');
    }

    async fetchDuracionesReal() {
        return this.callAPI('/duraciones');
    }

    // Funciones de análisis y métricas
    trackUserInteraction(action, data = {}) {
        // Implementar tracking de eventos para análisis
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                event_category: 'Universities',
                event_label: data.label || '',
                value: data.value || 0
            });
        }
        
        console.log('User interaction:', action, data);
    }

    // Funciones de accesibilidad
    announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }

    // Funciones de exportación/compartir
    exportResults() {
        const data = this.filteredUniversities.map(uni => ({
            nombre: uni.nombre,
            tipo: uni.tipo_universidad,
            ciudad: uni.ciudad,
            programas: uni.total_programas,
            telefono: uni.telefono,
            website: uni.website
        }));
        
        const csv = this.convertToCSV(data);
        this.downloadFile(csv, 'universidades-medellin.csv', 'text/csv');
    }

    convertToCSV(data) {
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
        ].join('\n');
        
        return csvContent;
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    shareResults() {
        if (navigator.share) {
            navigator.share({
                title: 'Universidades en Medellín - Polaris',
                text: `Encontré ${this.filteredUniversities.length} universidades que coinciden con mis criterios`,
                url: window.location.href
            });
        } else {
            // Fallback para navegadores que no soportan Web Share API
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showNotification('URL copiada al portapapeles');
            });
        }
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.universidadesApp = new UniversidadesApp();
});

// Exportar para uso global si es necesario
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UniversidadesApp;
}