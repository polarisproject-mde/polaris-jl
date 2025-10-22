// ============================================
// PLANIFICADOR FINANCIERO EDUCATIVO - POLARIS
// ============================================

// Elementos del DOM
const calcularBtn = document.getElementById('calcularBtn');
const resetBtn = document.getElementById('resetBtn');
const exportBtn = document.getElementById('exportBtn');
const resultsSection = document.getElementById('resultsSection');

// Checkboxes de fuentes de financiamiento
const usarAhorros = document.getElementById('usarAhorros');
const usarBeca = document.getElementById('usarBeca');
const usarPrestamo = document.getElementById('usarPrestamo');
const usarTrabajo = document.getElementById('usarTrabajo');

// Details containers
const ahorrosDetails = document.getElementById('ahorrosDetails');
const becaDetails = document.getElementById('becaDetails');
const prestamoDetails = document.getElementById('prestamoDetails');
const trabajoDetails = document.getElementById('trabajoDetails');

// Escenarios
const escenarioBeca = document.getElementById('escenarioBeca');
const escenarioAumento = document.getElementById('escenarioAumento');
const aumentoDetails = document.getElementById('aumentoDetails');

// Toggle visibility de detalles
usarAhorros.addEventListener('change', () => toggleDetails(usarAhorros, ahorrosDetails));
usarBeca.addEventListener('change', () => toggleDetails(usarBeca, becaDetails));
usarPrestamo.addEventListener('change', () => toggleDetails(usarPrestamo, prestamoDetails));
usarTrabajo.addEventListener('change', () => toggleDetails(usarTrabajo, trabajoDetails));
escenarioAumento.addEventListener('change', () => toggleDetails(escenarioAumento, aumentoDetails));

function toggleDetails(checkbox, detailsDiv) {
    detailsDiv.style.display = checkbox.checked ? 'block' : 'none';
}

// Función para formatear moneda
function formatearMoneda(numero) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(numero);
}

// Función para obtener valores
function getVal(id) {
    const element = document.getElementById(id);
    return parseFloat(element.value) || 0;
}

// Calcular plan financiero
calcularBtn.addEventListener('click', calcularPlan);

function calcularPlan() {
    // Validaciones
    const costoSemestre = getVal('costoSemestre');
    const duracion = getVal('duracion');

    if (costoSemestre === 0 || duracion === 0) {
        alert('Por favor, ingresa el costo por semestre y la duración de la carrera');
        return;
    }

    // Datos básicos
    const gastosExtra = getVal('gastosExtra');
    const inflacion = getVal('inflacion') / 100;
    const inicioCarrera = getVal('inicioCarrera');
    const fondoEmergencia = getVal('fondoEmergencia');

    // Calcular costo total con inflación
    let costoTotalAcumulado = 0;
    let costosPorSemestre = [];
    
    for (let i = 0; i < duracion; i++) {
        const anio = Math.floor(i / 2);
        const factorInflacion = Math.pow(1 + inflacion, anio);
        const costoSemestreAjustado = (costoSemestre + gastosExtra) * factorInflacion;
        costoTotalAcumulado += costoSemestreAjustado;
        costosPorSemestre.push({
            semestre: i + 1,
            costo: costoSemestreAjustado,
            costoAcumulado: costoTotalAcumulado
        });
    }

    // Calcular fondo de emergencia
    const costoFondoEmergencia = (costoSemestre + gastosExtra) * fondoEmergencia * Math.pow(1 + inflacion, Math.floor(duracion / 4));
    const inversionTotalNecesaria = costoTotalAcumulado + costoFondoEmergencia;

    // Calcular fuentes de financiamiento
    let fuentesFinanciamiento = [];
    let totalCubierto = 0;

    // AHORROS
    if (usarAhorros.checked) {
        const ahorroActual = getVal('ahorroActual');
        const ahorroMensual = getVal('ahorroMensual');
        const mesesAhorro = inicioCarrera + (duracion * 6);
        const totalAhorros = ahorroActual + (ahorroMensual * mesesAhorro);
        
        fuentesFinanciamiento.push({
            nombre: 'Ahorros Propios',
            monto: totalAhorros,
            porcentaje: 0,
            color: '#4caf50'
        });
        totalCubierto += totalAhorros;
    }

    // BECA
    let montoBeca = 0;
    if (usarBeca.checked) {
        const porcentajeBeca = getVal('porcentajeBeca') / 100;
        montoBeca = costoTotalAcumulado * porcentajeBeca;
        
        fuentesFinanciamiento.push({
            nombre: 'Beca/Apoyo Familiar',
            monto: montoBeca,
            porcentaje: 0,
            color: '#2196f3'
        });
        totalCubierto += montoBeca;
    }

    // TRABAJO
    if (usarTrabajo.checked) {
        const ingresoMensual = getVal('ingresoMensual');
        const mesesTrabajo = duracion * 6;
        const totalTrabajo = ingresoMensual * mesesTrabajo * 0.7; // 70% destinado a estudios
        
        fuentesFinanciamiento.push({
            nombre: 'Trabajo Part-time',
            monto: totalTrabajo,
            porcentaje: 0,
            color: '#ff9800'
        });
        totalCubierto += totalTrabajo;
    }

    // PRÉSTAMO (si es necesario o seleccionado)
    let montoPrestamo = 0;
    let cuotaMensual = 0;
    let interesesTotales = 0;
    
    const deficit = Math.max(0, inversionTotalNecesaria - totalCubierto);
    
    if (usarPrestamo.checked || deficit > 0) {
        montoPrestamo = usarPrestamo.checked ? Math.max(deficit, inversionTotalNecesaria * 0.3) : deficit;
        const tasaInteres = getVal('tasaInteres') / 100 / 12;
        const plazoPago = getVal('plazoPago') * 12;
        
        // Calcular cuota mensual con interés compuesto
        if (tasaInteres > 0) {
            cuotaMensual = (montoPrestamo * tasaInteres * Math.pow(1 + tasaInteres, plazoPago)) / 
                          (Math.pow(1 + tasaInteres, plazoPago) - 1);
            interesesTotales = (cuotaMensual * plazoPago) - montoPrestamo;
        } else {
            cuotaMensual = montoPrestamo / plazoPago;
        }
        
        fuentesFinanciamiento.push({
            nombre: 'Préstamo Educativo',
            monto: montoPrestamo,
            porcentaje: 0,
            color: '#f44336'
        });
        totalCubierto += montoPrestamo;
    }

    // Calcular porcentajes
    fuentesFinanciamiento.forEach(fuente => {
        fuente.porcentaje = (fuente.monto / totalCubierto) * 100;
    });

    const cobertura = (totalCubierto / inversionTotalNecesaria) * 100;

    // Mostrar resultados
    mostrarResultados({
        inversionTotal: costoTotalAcumulado,
        inversionTotalNecesaria,
        costoFondoEmergencia,
        cobertura,
        deficit,
        fuentesFinanciamiento,
        costosPorSemestre,
        duracion,
        inicioCarrera,
        montoPrestamo,
        cuotaMensual,
        interesesTotales,
        plazoPago: getVal('plazoPago'),
        inflacion: inflacion * 100
    });

    // Escenarios
    if (escenarioBeca.checked || escenarioAumento.checked) {
        calcularEscenarios(costoTotalAcumulado, duracion, inflacion, costoSemestre, gastosExtra);
    }

    // Scroll a resultados
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function mostrarResultados(datos) {
    resultsSection.style.display = 'block';

    // Resumen general
    document.getElementById('inversionTotal').textContent = formatearMoneda(datos.inversionTotal);
    document.getElementById('inversionAjustada').textContent = 
        `(Incluye ${datos.inflacion}% inflación anual)`;
    document.getElementById('coberturaActual').textContent = 
        `${datos.cobertura.toFixed(1)}%`;
    document.getElementById('deficit').textContent = formatearMoneda(datos.deficit);
    document.getElementById('fondoEmergenciaValor').textContent = 
        formatearMoneda(datos.costoFondoEmergencia);

    // Distribución de financiamiento
    mostrarDistribucion(datos.fuentesFinanciamiento);

    // Timeline
    mostrarTimeline(datos.costosPorSemestre, datos.inicioCarrera);

    // Plan de ahorro
    mostrarPlanAhorro(datos.inversionTotalNecesaria, datos.inicioCarrera, datos.duracion);

    // Análisis de préstamo
    if (datos.montoPrestamo > 0) {
        mostrarAnalisisPrestamo(datos);
    }

    // Recomendaciones
    generarRecomendaciones(datos);
}

function mostrarDistribucion(fuentes) {
    const legendContainer = document.getElementById('distributionLegend');
    legendContainer.innerHTML = '';

    fuentes.forEach(fuente => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `
            <div class="legend-color" style="background: ${fuente.color}"></div>
            <span>${fuente.nombre}: ${formatearMoneda(fuente.monto)} (${fuente.porcentaje.toFixed(1)}%)</span>
        `;
        legendContainer.appendChild(legendItem);
    });

    // Gráfico simple con Canvas
    const canvas = document.getElementById('distributionChart');
    const ctx = canvas.getContext('2d');
    canvas.width = 300;
    canvas.height = 300;

    const centerX = 150;
    const centerY = 150;
    const radius = 120;
    let currentAngle = -Math.PI / 2;

    fuentes.forEach(fuente => {
        const sliceAngle = (fuente.porcentaje / 100) * 2 * Math.PI;
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = fuente.color;
        ctx.fill();
        
        currentAngle += sliceAngle;
    });

    // Círculo blanco en el centro para efecto donut
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.5, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(26, 26, 46, 0.95)';
    ctx.fill();
}

function mostrarTimeline(costosPorSemestre, inicioCarrera) {
    const container = document.getElementById('timelineContainer');
    container.innerHTML = '';

    const mesesHastaInicio = inicioCarrera;
    
    if (mesesHastaInicio > 0) {
        const inicioItem = crearTimelineItem(
            'Inicio',
            `Dentro de ${mesesHastaInicio} meses`,
            'Comienza tu carrera',
            '',
            false
        );
        container.appendChild(inicioItem);
    }

    costosPorSemestre.forEach((item, index) => {
        const esCritico = item.costo > costosPorSemestre[0].costo * 1.3;
        const mesesDesdeAhora = mesesHastaInicio + (index * 6);
        
        const timelineItem = crearTimelineItem(
            `S${item.semestre}`,
            `Mes ${mesesDesdeAhora}`,
            `Semestre ${item.semestre} - ${index % 2 === 0 ? 'Primer' : 'Segundo'} semestre del año ${Math.floor(index / 2) + 1}`,
            formatearMoneda(item.costo),
            esCritico
        );
        container.appendChild(timelineItem);
    });
}

function crearTimelineItem(marker, tiempo, titulo, monto, critico) {
    const div = document.createElement('div');
    div.className = 'timeline-item';
    div.innerHTML = `
        <div class="timeline-marker ${critico ? 'critical' : ''}">${marker}</div>
        <div class="timeline-content">
            <div class="timeline-title">${titulo}</div>
            <div class="timeline-description">${tiempo}</div>
            ${monto ? `<div class="timeline-amount">${monto}</div>` : ''}
        </div>
    `;
    return div;
}

function mostrarPlanAhorro(montoTotal, mesesHastaInicio, duracion) {
    const container = document.getElementById('savingsContent');
    container.innerHTML = '';

    const estrategias = [
        {
            nombre: 'Conservadora',
            tipo: 'conservative',
            mesesAhorro: mesesHastaInicio + (duracion * 6),
            porcentajeAnticipado: 0.3
        },
        {
            nombre: 'Moderada',
            tipo: 'moderate',
            mesesAhorro: mesesHastaInicio + (duracion * 4),
            porcentajeAnticipado: 0.5
        },
        {
            nombre: 'Agresiva',
            tipo: 'aggressive',
            mesesAhorro: mesesHastaInicio,
            porcentajeAnticipado: 0.8
        }
    ];

    estrategias.forEach(estrategia => {
        const montoAnticipado = montoTotal * estrategia.porcentajeAnticipado;
        const ahorroMensual = estrategia.mesesAhorro > 0 ? 
            montoAnticipado / estrategia.mesesAhorro : 0;

        const div = document.createElement('div');
        div.className = 'savings-strategy';
        div.innerHTML = `
            <div class="strategy-header">
                <div class="strategy-name">${estrategia.nombre}</div>
                <div class="strategy-badge ${estrategia.tipo}">${estrategia.tipo}</div>
            </div>
            <div class="strategy-details">
                <div class="strategy-row">
                    <span>Ahorro mensual:</span>
                    <strong>${formatearMoneda(ahorroMensual)}</strong>
                </div>
                <div class="strategy-row">
                    <span>Total anticipado:</span>
                    <strong>${formatearMoneda(montoAnticipado)}</strong>
                </div>
                <div class="strategy-row">
                    <span>Período de ahorro:</span>
                    <strong>${estrategia.mesesAhorro} meses</strong>
                </div>
                <div class="strategy-row">
                    <span>Cobertura inicial:</span>
                    <strong>${(estrategia.porcentajeAnticipado * 100).toFixed(0)}%</strong>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

function mostrarAnalisisPrestamo(datos) {
    const card = document.getElementById('loanCard');
    const container = document.getElementById('loanContent');
    card.style.display = 'block';

    const totalPagar = datos.cuotaMensual * datos.plazoPago * 12;
    const tasaMensual = getVal('tasaInteres') / 12;

    container.innerHTML = `
        <div class="loan-info">
            <div class="loan-detail">
                <span class="loan-label">Monto del Préstamo:</span>
                <span class="loan-value">${formatearMoneda(datos.montoPrestamo)}</span>
            </div>
            <div class="loan-detail">
                <span class="loan-label">Cuota Mensual:</span>
                <span class="loan-value">${formatearMoneda(datos.cuotaMensual)}</span>
            </div>
            <div class="loan-detail">
                <span class="loan-label">Intereses Totales:</span>
                <span class="loan-value">${formatearMoneda(datos.interesesTotales)}</span>
            </div>
            <div class="loan-detail">
                <span class="loan-label">Total a Pagar:</span>
                <span class="loan-value">${formatearMoneda(totalPagar)}</span>
            </div>
            <div class="loan-detail">
                <span class="loan-label">Plazo de Pago:</span>
                <span class="loan-value">${datos.plazoPago} años (${datos.plazoPago * 12} meses)</span>
            </div>
            <div class="loan-detail">
                <span class="loan-label">Tasa de Interés:</span>
                <span class="loan-value">${getVal('tasaInteres')}% anual (${tasaMensual.toFixed(2)}% mensual)</span>
            </div>
        </div>
        <div style="margin-top: 20px; padding: 20px; background: rgba(255, 152, 0, 0.1); border-radius: 12px; border-left: 4px solid #ff9800;">
            <p style="color: #d9d9d9; font-family: 'Montserrat', sans-serif; margin: 0; line-height: 1.6;">
                <strong>Importante:</strong> Después de graduarte, deberás pagar ${formatearMoneda(datos.cuotaMensual)} mensuales durante ${datos.plazoPago} años. 
                Esto representa aproximadamente el ${((datos.cuotaMensual / 3000000) * 100).toFixed(1)}% de un salario promedio inicial.
            </p>
        </div>
    `;
}

function calcularEscenarios(costoBase, duracion, inflacion, costoSemestre, gastosExtra) {
    const card = document.getElementById('scenariosCard');
    const container = document.getElementById('scenariosContent');
    card.style.display = 'block';

    let escenarios = [];

    // Escenario: Pérdida de beca
    if (escenarioBeca.checked) {
        const porcentajeBeca = getVal('porcentajeBeca') / 100;
        const semestresPerdidos = Math.ceil(duracion / 2);
        const costoPerdidaBeca = (costoSemestre + gastosExtra) * semestresPerdidos * 
            Math.pow(1 + inflacion, Math.floor(duracion / 4));
        
        escenarios.push({
            nombre: 'Pérdida de Beca a Mitad de Carrera',
            impacto: `Necesitarías ${formatearMoneda(costoPerdidaBeca)} adicionales para cubrir los últimos ${semestresPerdidos} semestres sin apoyo de beca.`,
            warning: true
        });
    }

    // Escenario: Aumento adicional de costos
    if (escenarioAumento.checked) {
        const aumentoExtra = getVal('aumentoExtra') / 100;
        const costoConAumento = costoBase * (1 + aumentoExtra);
        const diferencia = costoConAumento - costoBase;
        
        escenarios.push({
            nombre: `Aumento de Costos del ${(aumentoExtra * 100).toFixed(0)}%`,
            impacto: `Si los costos aumentan más de lo esperado, necesitarías ${formatearMoneda(diferencia)} adicionales durante toda la carrera.`,
            warning: true
        });
    }

    container.innerHTML = '<div class="scenario-comparison"></div>';
    const grid = container.querySelector('.scenario-comparison');

    escenarios.forEach(escenario => {
        const div = document.createElement('div');
        div.className = `scenario-box ${escenario.warning ? 'warning' : ''}`;
        div.innerHTML = `
            <div class="scenario-name">${escenario.nombre}</div>
            <div class="scenario-impact">${escenario.impacto}</div>
        `;
        grid.appendChild(div);
    });
}

function generarRecomendaciones(datos) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';

    const recomendaciones = [];

    // Recomendación: Cobertura
    if (datos.cobertura >= 100) {
        recomendaciones.push({
            tipo: 'success',
            titulo: '¡Excelente Planificación!',
            texto: 'Tu plan cubre completamente la inversión necesaria. Mantén tu disciplina de ahorro y considera crear un fondo adicional para oportunidades académicas extras.',
            icono: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
        });
    } else if (datos.cobertura >= 80) {
        recomendaciones.push({
            tipo: 'normal',
            titulo: 'Buena Cobertura',
            texto: `Cubres el ${datos.cobertura.toFixed(1)}% de los costos. Considera aumentar tu ahorro mensual o buscar becas adicionales para cerrar la brecha de ${formatearMoneda(datos.deficit)}.`,
            icono: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'
        });
    } else {
        recomendaciones.push({
            tipo: 'critical',
            titulo: 'Atención: Déficit Importante',
            texto: `Tu cobertura actual es del ${datos.cobertura.toFixed(1)}%. Necesitas ${formatearMoneda(datos.deficit)} adicionales. Considera combinar más fuentes de financiamiento o buscar opciones de becas.`,
            icono: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'
        });
    }

    // Recomendación: Ahorro anticipado
    if (datos.inicioCarrera >= 12) {
        recomendaciones.push({
            tipo: 'success',
            titulo: 'Aprovecha el Tiempo',
            texto: `Tienes ${datos.inicioCarrera} meses antes de empezar. Usa este tiempo para ahorrar agresivamente y reducir la necesidad de préstamos.`,
            icono: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
        });
    } else if (datos.inicioCarrera > 0) {
        recomendaciones.push({
            tipo: 'normal',
            titulo: 'Tiempo Limitado',
            texto: `Solo tienes ${datos.inicioCarrera} meses. Enfócate en ahorrar lo máximo posible y asegura tus fuentes de financiamiento ahora.`,
            icono: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
        });
    }

    // Recomendación: Préstamo
    if (datos.montoPrestamo > datos.inversionTotal * 0.5) {
        recomendaciones.push({
            tipo: 'critical',
            titulo: 'Alto Nivel de Endeudamiento',
            texto: `Tu préstamo representa más del 50% de la inversión. Busca alternativas como becas, trabajo part-time o reducir gastos no esenciales para disminuir la deuda.`,
            icono: '<path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'
        });
    } else if (datos.montoPrestamo > 0) {
        const porcentajeSalario = (datos.cuotaMensual / 3000000) * 100;
        if (porcentajeSalario > 30) {
            recomendaciones.push({
                tipo: 'critical',
                titulo: 'Cuota Muy Alta',
                texto: `Tu cuota mensual de ${formatearMoneda(datos.cuotaMensual)} representa el ${porcentajeSalario.toFixed(1)}% de un salario promedio. Considera extender el plazo o reducir el monto del préstamo.`,
                icono: '<rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/>'
            });
        }
    }

    // Recomendación: Fondo de emergencia
    if (datos.costoFondoEmergencia > 0) {
        recomendaciones.push({
            tipo: 'normal',
            titulo: 'Fondo de Emergencia',
            texto: `Es crucial tener ${formatearMoneda(datos.costoFondoEmergencia)} como fondo de emergencia para imprevistos académicos. Intégralo en tu plan de ahorro.`,
            icono: '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>'
        });
    }

    // Recomendación: Inflación
    if (datos.inflacion > 7) {
        recomendaciones.push({
            tipo: 'normal',
            titulo: 'Alta Inflación Educativa',
            texto: `Con una inflación del ${datos.inflacion}% anual, tus costos aumentarán significativamente. Considera negociar pagos anticipados o buscar universidades con costos más estables.`,
            icono: '<line x1="12" y1="1" x2="12" y2="23"/><polyline points="17 6 12 1 7 6"/><polyline points="7 18 12 23 17 18"/>'
        });
    }

    // Mostrar recomendaciones
    recomendaciones.forEach(rec => {
        const div = document.createElement('div');
        div.className = `recommendation-item ${rec.tipo}`;
        div.innerHTML = `
            <div class="recommendation-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    ${rec.icono}
                </svg>
            </div>
            <div class="recommendation-content">
                <div class="recommendation-title">${rec.titulo}</div>
                <div class="recommendation-text">${rec.texto}</div>
            </div>
        `;
        container.appendChild(div);
    });
}

// Reset
resetBtn.addEventListener('click', () => {
    if (confirm('¿Estás seguro de que quieres iniciar una nueva planificación? Se perderán los datos actuales.')) {
        location.reload();
    }
});

// Export
exportBtn.addEventListener('click', () => {
    window.print();
});

// Enter key support
const allInputs = document.querySelectorAll('input[type="number"]');
allInputs.forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            calcularBtn.click();
        }
    });
});