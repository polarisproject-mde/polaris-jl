// ================================================
// DELETE-TEST.JS - Funcionalidad de Eliminar Tests
// Guardar en: static/js/delete-test.js
// ================================================

/**
 * Muestra una notificación toast
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo: 'success', 'error', 'warning'
 */
function showToast(message, type = 'success') {
    // Crear elemento toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    // Agregar icono según tipo
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️'
    };
    
    toast.innerHTML = `
        <span>${icons[type] || '📢'}</span>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Mostrar con animación
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Ocultar y eliminar
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Función principal para eliminar un test desde la lista
 * @param {number} testId - ID del test a eliminar
 * @param {Event} event - Evento del click
 */
async function eliminarTest(testId, event) {
    // Prevenir propagación al card
    if (event) {
        event.stopPropagation();
    }
    
    // Confirmación con mensaje detallado
    const confirmacion = confirm(
        '⚠️ ¿ESTÁS SEGURO?\n\n' +
        'Vas a eliminar este test permanentemente.\n\n' +
        'Se eliminarán:\n' +
        '• Todas las respuestas\n' +
        '• Todos los resultados\n' +
        '• El análisis vocacional\n\n' +
        'Esta acción NO se puede deshacer.\n\n' +
        '¿Deseas continuar?'
    );
    
    if (!confirmacion) {
        return;
    }
    
    // Obtener elementos del DOM
    const btn = event.target.closest('.delete-test-btn');
    const card = btn.closest('.test-card');
    const textoOriginal = btn.innerHTML;
    
    // Deshabilitar botón y mostrar loading
    btn.disabled = true;
    btn.classList.add('btn-loading');
    btn.innerHTML = '<span class="spinner"></span> Eliminando...';
    
    try {
        // Hacer petición DELETE al servidor
        const response = await fetch(`/test/${testId}/eliminar`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Animación de salida de la tarjeta
            card.classList.add('deleting');
            
            // Mostrar notificación de éxito
            showToast('Test eliminado correctamente', 'success');
            
            // Esperar animación y recargar página
            setTimeout(() => {
                window.location.reload();
            }, 400);
        } else {
            throw new Error(data.detail || 'Error al eliminar el test');
        }
    } catch (error) {
        console.error('Error al eliminar test:', error);
        
        // Restaurar botón a estado original
        btn.disabled = false;
        btn.classList.remove('btn-loading');
        btn.innerHTML = textoOriginal;
        
        // Mostrar error al usuario
        showToast(`Error: ${error.message}`, 'error');
    }
}

/**
 * Función para eliminar test desde la página de detalle
 * @param {number} testId - ID del test a eliminar
 */
async function eliminarTestDetalle(testId) {
    const confirmacion = confirm(
        '⚠️ ADVERTENCIA FINAL\n\n' +
        'Vas a eliminar este test de forma PERMANENTE.\n\n' +
        'Se perderán:\n' +
        '✗ Todos los resultados del test\n' +
        '✗ Todas las respuestas guardadas\n' +
        '✗ El análisis vocacional completo\n' +
        '✗ Las recomendaciones de carreras\n\n' +
        'Esta acción es IRREVERSIBLE.\n\n' +
        '¿Confirmar eliminación definitiva?'
    );
    
    if (!confirmacion) {
        return;
    }
    
    // Obtener botón de eliminar
    const btn = document.querySelector('.btn-delete-detail');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Eliminando...';
    }
    
    try {
        const response = await fetch(`/test/${testId}/eliminar`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showToast('Test eliminado correctamente', 'success');
            
            // Redirigir a lista de tests después de 1 segundo
            setTimeout(() => {
                window.location.href = '/mis-tests';
            }, 1000);
        } else {
            throw new Error(data.detail || 'Error al eliminar');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast(`Error: ${error.message}`, 'error');
        
        // Restaurar botón
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🗑️ Eliminar Test';
        }
    }
}

/**
 * Modal personalizado de confirmación (opcional, más elegante)
 * @param {number} testId - ID del test
 * @param {Function} callback - Función a ejecutar tras confirmar
 */
function mostrarModalEliminacion(testId, callback) {
    // Crear modal
    const modal = document.createElement('div');
    modal.className = 'delete-modal';
    modal.innerHTML = `
        <div class="delete-modal-content">
            <h3>🗑️ Eliminar Test</h3>
            <p>
                ¿Estás seguro de que deseas eliminar este test?<br><br>
                <strong>Esta acción no se puede deshacer.</strong><br>
                Se eliminarán todos los resultados y respuestas.
            </p>
            <div class="delete-modal-actions">
                <button class="btn-cancel" onclick="cerrarModalEliminacion()">
                    Cancelar
                </button>
                <button class="btn-confirm-delete" onclick="confirmarEliminacionModal(${testId})">
                    Eliminar Definitivamente
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Activar modal con animación
    setTimeout(() => modal.classList.add('active'), 10);
    
    // Cerrar al hacer clic fuera del contenido
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            cerrarModalEliminacion();
        }
    });
    
    // Cerrar con tecla ESC
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            cerrarModalEliminacion();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);
}

/**
 * Cierra el modal de confirmación
 */
function cerrarModalEliminacion() {
    const modal = document.querySelector('.delete-modal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    }
}

/**
 * Confirma la eliminación desde el modal
 * @param {number} testId - ID del test
 */
async function confirmarEliminacionModal(testId) {
    cerrarModalEliminacion();
    
    // Buscar el botón en la tarjeta
    const card = document.querySelector(`[data-test-id="${testId}"]`);
    if (card) {
        const btn = card.querySelector('.delete-test-btn');
        const mockEvent = { target: btn, stopPropagation: () => {} };
        await eliminarTest(testId, mockEvent);
    }
}

/**
 * Función para eliminar múltiples tests (opcional)
 * Útil si implementas selección múltiple
 */
async function eliminarTestsSeleccionados() {
    const checkboxes = document.querySelectorAll('.test-checkbox:checked');
    const ids = Array.from(checkboxes).map(cb => parseInt(cb.value));
    
    if (ids.length === 0) {
        showToast('Selecciona al menos un test para eliminar', 'warning');
        return;
    }
    
    const confirmacion = confirm(
        `¿Eliminar ${ids.length} test(s) seleccionado(s)?\n\n` +
        'Esta acción no se puede deshacer.'
    );
    
    if (!confirmacion) return;
    
    let eliminados = 0;
    let errores = 0;
    
    // Eliminar cada test
    for (const id of ids) {
        try {
            const response = await fetch(`/test/${id}/eliminar`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                eliminados++;
            } else {
                errores++;
            }
        } catch (error) {
            console.error(`Error al eliminar test ${id}:`, error);
            errores++;
        }
    }
    
    // Mostrar resultado
    if (eliminados > 0) {
        showToast(`${eliminados} test(s) eliminado(s) correctamente`, 'success');
    }
    
    if (errores > 0) {
        showToast(`${errores} error(es) al eliminar`, 'error');
    }
    
    // Recargar después de 1.5 segundos
    setTimeout(() => window.location.reload(), 1500);
}

/**
 * Versión con promesa para usar con async/await
 * @param {number} testId - ID del test
 * @returns {Promise}
 */
function eliminarTestAsync(testId) {
    return new Promise((resolve, reject) => {
        const confirmacion = confirm('¿Eliminar este test permanentemente?');
        
        if (!confirmacion) {
            reject(new Error('Cancelado por el usuario'));
            return;
        }
        
        fetch(`/test/${testId}/eliminar`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resolve(data);
            } else {
                reject(new Error(data.detail || 'Error desconocido'));
            }
        })
        .catch(error => reject(error));
    });
}

/**
 * Manejo de confirmación antes de cerrar página durante eliminación
 */
window.addEventListener('beforeunload', (e) => {
    const deletingCards = document.querySelectorAll('.test-card.deleting');
    if (deletingCards.length > 0) {
        e.preventDefault();
        e.returnValue = 'Hay una eliminación en proceso. ¿Estás seguro de salir?';
    }
});

/**
 * Inicialización cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ Delete-test.js cargado correctamente');
    
    // Agregar data-attribute a las tarjetas (opcional, para mejor manejo)
    const testCards = document.querySelectorAll('.test-card');
    testCards.forEach(card => {
        const deleteBtn = card.querySelector('.delete-test-btn');
        if (deleteBtn) {
            const onclick = deleteBtn.getAttribute('onclick');
            const match = onclick?.match(/eliminarTest\((\d+)/);
            if (match) {
                card.setAttribute('data-test-id', match[1]);
            }
        }
    });
});

// Exportar funciones si usas módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        eliminarTest,
        eliminarTestDetalle,
        eliminarTestAsync,
        showToast,
        mostrarModalEliminacion
    };
}