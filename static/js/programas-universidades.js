// blog.js - VERSIÓN OPTIMIZADA Y RÁPIDA

const API_URL = '/api';
const COMMENTS_PER_PAGE = 10;

// Estado global
let currentComments = [];
let currentOffset = 0;
let hasMore = true;
let editingCommentId = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeForum();
});

function initializeForum() {
    loadComments();
    loadPopularTopics();
    setupEventListeners();
    loadDraft();
}

// ================================
// EVENT LISTENERS
// ================================

function setupEventListeners() {
    const commentForm = document.getElementById('comment-form');
    commentForm.addEventListener('submit', handleCommentSubmit);
    
    const commentInput = document.getElementById('comment-input');
    commentInput.addEventListener('input', updateCharacterCount);
    
    window.resetCommentForm = resetForm;
    
    const saveDraftBtn = document.getElementById('save-draft');
    saveDraftBtn.addEventListener('click', saveDraft);
    
    const viewBtns = document.querySelectorAll('.view-btn');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', handleViewChange);
    });
    
    const sortSelect = document.getElementById('sort-comments');
    sortSelect.addEventListener('change', handleSortChange);
    
    const filterSelect = document.getElementById('filter-topic');
    filterSelect.addEventListener('change', handleFilterChange);
    
    const loadMoreBtn = document.getElementById('load-more-btn');
    loadMoreBtn.addEventListener('click', loadMoreComments);
    
    setupFAQAccordion();
    setupTopicFilters();
}

// ================================
// CARGAR COMENTARIOS - OPTIMIZADO
// ================================

async function loadComments(reset = true) {
    if (reset) {
        currentOffset = 0;
        currentComments = [];
    }
    
    const sortSelect = document.getElementById('sort-comments');
    const filterSelect = document.getElementById('filter-topic');
    const orden = sortSelect.value;
    const tema = filterSelect.value;
    
    try {
        showLoading();
        
        // Timeout de 8 segundos
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);
        
        const url = `${API_URL}/comentarios?orden=${orden}&tema=${tema}&limit=${COMMENTS_PER_PAGE}&offset=${currentOffset}`;
        const response = await fetch(url, { signal: controller.signal });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error('Error al cargar comentarios');
        }
        
        const data = await response.json();
        
        if (reset) {
            currentComments = data.comentarios;
        } else {
            currentComments = [...currentComments, ...data.comentarios];
        }
        
        hasMore = data.has_more;
        currentOffset += data.comentarios.length;
        
        displayComments(currentComments);
        updateLoadMoreButton();
        
    } catch (error) {
        if (error.name === 'AbortError') {
            showNotification('La carga está tardando mucho. Intenta recargar la página.', 'warning');
        } else {
            console.error('Error al cargar comentarios:', error);
            showNotification('Error al cargar comentarios', 'error');
        }
    } finally {
        hideLoading();
    }
}

function displayComments(comments) {
    const commentsList = document.getElementById('comments-list');
    const noComments = document.getElementById('no-comments');
    
    if (comments.length === 0) {
        commentsList.style.display = 'none';
        noComments.style.display = 'flex';
        return;
    }
    
    commentsList.style.display = 'flex';
    noComments.style.display = 'none';
    
    commentsList.innerHTML = comments.map(comment => createCommentHTML(comment)).join('');
    
    comments.forEach(comment => {
        setupCommentActions(comment.id);
    });
}

function createCommentHTML(comment) {
    const date = new Date(comment.fecha_creacion);
    const formattedDate = formatDate(date);
    const initials = getInitials(comment.nombre);
    const wasEdited = comment.fecha_creacion !== comment.fecha_actualizacion;
    
    const temaLabels = {
        'orientacion': 'Orientación',
        'universidades': 'Universidades',
        'carreras': 'Carreras',
        'becas': 'Becas',
        'experiencias': 'Experiencias',
        'otros': 'Otros'
    };
    
    const temaDisplay = comment.tema ? temaLabels[comment.tema] || comment.tema : '';
    
    return `
        <div class="comment-item" data-comment-id="${comment.id}">
            <div class="comment-header">
                <div class="comment-author">
                    <div class="author-avatar">${initials}</div>
                    <div class="author-info">
                        <h4>${escapeHtml(comment.nombre)}</h4>
                        <time datetime="${comment.fecha_creacion}">${formattedDate}</time>
                        ${wasEdited ? '<span class="edited-label">(editado)</span>' : ''}
                        ${temaDisplay ? `<span class="comment-topic">${temaDisplay}</span>` : ''}
                    </div>
                </div>
                <div class="comment-actions-top">
                    <button class="edit-btn" onclick="editComment(${comment.id})" title="Editar">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                    </button>
                    <button class="delete-btn" onclick="deleteComment(${comment.id})" title="Eliminar">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="comment-content">
                <p>${escapeHtml(comment.contenido)}</p>
            </div>
            <div class="comment-actions">
                <button class="like-btn" onclick="likeComment(${comment.id})" data-likes="${comment.likes}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                    </svg>
                    <span class="like-count">${comment.likes}</span>
                </button>
            </div>
        </div>
    `;
}

function setupCommentActions(commentId) {
    // Ya están configurados con onclick
}

// ================================
// CREAR/EDITAR COMENTARIO - OPTIMIZADO
// ================================

async function handleCommentSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.querySelector('.btn-text').textContent;
    
    const nombre = document.getElementById('user-name').value.trim();
    const tema = document.getElementById('user-topic').value;
    const contenido = document.getElementById('comment-input').value.trim();
    
    // Validaciones
    if (nombre.length < 2) {
        showNotification('El nombre debe tener al menos 2 caracteres', 'error');
        document.getElementById('user-name').focus();
        return;
    }
    
    if (contenido.length < 10) {
        showNotification('El comentario debe tener al menos 10 caracteres', 'error');
        document.getElementById('comment-input').focus();
        return;
    }
    
    if (contenido.length > 500) {
        showNotification('El comentario no puede superar 500 caracteres', 'error');
        document.getElementById('comment-input').focus();
        return;
    }
    
    // Deshabilitar botón
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Publicando...';
    
    try {
        const comentarioData = {
            nombre: nombre,
            tema: tema || null,
            contenido: contenido
        };
        
        let response;
        let url;
        let method;
        
        if (editingCommentId) {
            url = `${API_URL}/comentarios/${editingCommentId}`;
            method = 'PUT';
            delete comentarioData.nombre;
        } else {
            url = `${API_URL}/comentarios`;
            method = 'POST';
        }
        
        // Timeout de 10 segundos
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(comentarioData),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al procesar el comentario');
        }
        
        await response.json();
        
        // Limpiar formulario
        resetForm();
        
        // Mostrar notificación
        showNotification(
            editingCommentId ? '✓ Comentario actualizado' : '✓ Comentario publicado', 
            'success'
        );
        
        // Resetear modo edición
        editingCommentId = null;
        updateFormMode(false);
        
        // Recargar en background (NO ESPERAR)
        setTimeout(() => {
            loadComments(true);
            loadPopularTopics();
        }, 500);
        
    } catch (error) {
        console.error('Error:', error);
        
        if (error.name === 'AbortError') {
            showNotification('La solicitud está tardando mucho. Intenta de nuevo.', 'warning');
        } else {
            showNotification(error.message || 'Error al publicar el comentario', 'error');
        }
    } finally {
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = originalText;
    }
}

// ================================
// EDITAR COMENTARIO
// ================================

window.editComment = async function(commentId) {
    try {
        const comment = currentComments.find(c => c.id === commentId);
        if (!comment) {
            showNotification('Comentario no encontrado', 'error');
            return;
        }
        
        document.getElementById('user-name').value = comment.nombre;
        document.getElementById('user-topic').value = comment.tema || '';
        document.getElementById('comment-input').value = comment.contenido;
        
        updateCharacterCount();
        
        editingCommentId = commentId;
        updateFormMode(true);
        
        document.getElementById('comment-form').scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error al editar comentario:', error);
        showNotification('Error al cargar el comentario para editar', 'error');
    }
};

function updateFormMode(isEditing) {
    const formHeader = document.querySelector('.form-header h3');
    const submitBtn = document.querySelector('.submit-btn .btn-text');
    
    if (isEditing) {
        formHeader.textContent = 'Editar comentario';
        submitBtn.textContent = 'Actualizar Comentario';
        document.getElementById('comment-form').classList.add('editing-mode');
    } else {
        formHeader.textContent = 'Comparte tu experiencia';
        submitBtn.textContent = 'Publicar Comentario';
        document.getElementById('comment-form').classList.remove('editing-mode');
    }
}

// ================================
// ELIMINAR COMENTARIO
// ================================

window.deleteComment = async function(commentId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este comentario? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(`${API_URL}/comentarios/${commentId}`, {
            method: 'DELETE',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error('Error al eliminar el comentario');
        }
        
        showNotification('✓ Comentario eliminado', 'success');
        
        // Recargar en background
        setTimeout(() => {
            loadComments(true);
            loadPopularTopics();
        }, 300);
        
    } catch (error) {
        if (error.name === 'AbortError') {
            showNotification('Operación demorada. Recarga la página.', 'warning');
        } else {
            console.error('Error al eliminar comentario:', error);
            showNotification('Error al eliminar el comentario', 'error');
        }
    }
};

// ================================
// DAR LIKE
// ================================

window.likeComment = async function(commentId) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(`${API_URL}/comentarios/${commentId}/like`, {
            method: 'POST',
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error('Error al dar like');
        }
        
        const data = await response.json();
        
        // Actualizar el contador en el DOM
        const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
        const likeCount = commentItem.querySelector('.like-count');
        likeCount.textContent = data.likes;
        
        // Animación
        const likeBtn = commentItem.querySelector('.like-btn');
        likeBtn.classList.add('liked');
        setTimeout(() => {
            likeBtn.classList.remove('liked');
        }, 300);
        
        // Actualizar en el array local
        const comment = currentComments.find(c => c.id === commentId);
        if (comment) {
            comment.likes = data.likes;
        }
        
    } catch (error) {
        if (error.name === 'AbortError') {
            showNotification('Operación demorada', 'warning');
        } else {
            console.error('Error al dar like:', error);
            showNotification('Error al dar like', 'error');
        }
    }
};

// ================================
// TEMAS POPULARES
// ================================

async function loadPopularTopics() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(`${API_URL}/temas-populares?limit=10`, {
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error('Error al cargar temas populares');
        }
        
        const temas = await response.json();
        displayPopularTopics(temas);
        
    } catch (error) {
        console.error('Error al cargar temas populares:', error);
    }
}

function displayPopularTopics(temas) {
    const topicCloud = document.getElementById('topic-cloud');
    
    if (temas.length === 0) {
        topicCloud.innerHTML = '<p style="text-align: center; color: var(--gray-500);">No hay temas activos aún</p>';
        return;
    }
    
    topicCloud.innerHTML = temas.map(tema => `
        <span class="topic-tag" data-topic="${tema.tema}" data-count="${tema.contador}">
            ${tema.nombre_display} <span class="topic-count">(${tema.contador})</span>
        </span>
    `).join('');
}

function setupTopicFilters() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.topic-tag')) {
            const topicTag = e.target.closest('.topic-tag');
            const tema = topicTag.dataset.topic;
            
            const filterSelect = document.getElementById('filter-topic');
            filterSelect.value = tema;
            
            loadComments(true);
            
            document.getElementById('comments-container').scrollIntoView({ behavior: 'smooth' });
        }
    });
}

// ================================
// CONTROLES DE VISTA Y FILTROS
// ================================

function handleViewChange(e) {
    const btn = e.currentTarget;
    const view = btn.dataset.view;
    
    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    const commentsContainer = document.getElementById('comments-container');
    const commentsList = document.getElementById('comments-list');
    
    if (view === 'grid') {
        commentsContainer.classList.add('grid-view');
        commentsContainer.classList.remove('list-view');
        commentsList.classList.add('grid-view');
    } else {
        commentsContainer.classList.add('list-view');
        commentsContainer.classList.remove('grid-view');
        commentsList.classList.remove('grid-view');
    }
}

function handleSortChange() {
    loadComments(true);
}

function handleFilterChange() {
    loadComments(true);
}

function loadMoreComments() {
    loadComments(false);
}

function updateLoadMoreButton() {
    const loadMoreContainer = document.getElementById('load-more-container');
    const loadMoreBtn = document.getElementById('load-more-btn');
    
    if (hasMore && currentComments.length > 0) {
        loadMoreContainer.style.display = 'block';
        loadMoreBtn.disabled = false;
        loadMoreBtn.textContent = 'Cargar más comentarios';
    } else if (currentComments.length > 0) {
        loadMoreContainer.style.display = 'block';
        loadMoreBtn.disabled = true;
        loadMoreBtn.textContent = 'No hay más comentarios';
    } else {
        loadMoreContainer.style.display = 'none';
    }
}

// ================================
// FORMULARIO
// ================================

function resetForm() {
    document.getElementById('comment-form').reset();
    updateCharacterCount();
    editingCommentId = null;
    updateFormMode(false);
    clearDraft();
}

function updateCharacterCount() {
    const commentInput = document.getElementById('comment-input');
    const charCount = document.getElementById('char-count');
    const length = commentInput.value.length;
    
    charCount.textContent = length;
    
    if (length > 500) {
        charCount.style.color = 'var(--error-red)';
    } else if (length > 400) {
        charCount.style.color = 'var(--warning-orange)';
    } else {
        charCount.style.color = 'inherit';
    }
}

// ================================
// BORRADOR
// ================================

function saveDraft() {
    const nombre = document.getElementById('user-name').value;
    const tema = document.getElementById('user-topic').value;
    const contenido = document.getElementById('comment-input').value;
    
    if (!contenido.trim()) {
        showNotification('No hay contenido para guardar', 'warning');
        return;
    }
    
    const draft = {
        nombre,
        tema,
        contenido,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('comment_draft', JSON.stringify(draft));
    showNotification('✓ Borrador guardado', 'success');
}

function loadDraft() {
    const draftStr = localStorage.getItem('comment_draft');
    
    if (!draftStr) return;
    
    try {
        const draft = JSON.parse(draftStr);
        
        const loadDraft = confirm('Se encontró un borrador guardado. ¿Deseas cargarlo?');
        
        if (loadDraft) {
            document.getElementById('user-name').value = draft.nombre || '';
            document.getElementById('user-topic').value = draft.tema || '';
            document.getElementById('comment-input').value = draft.contenido || '';
            updateCharacterCount();
            showNotification('✓ Borrador cargado', 'success');
        }
    } catch (error) {
        console.error('Error al cargar borrador:', error);
    }
}

function clearDraft() {
    localStorage.removeItem('comment_draft');
}

// ================================
// FAQ ACCORDION
// ================================

function setupFAQAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const isActive = faqItem.classList.contains('active');
            
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });
            
            if (!isActive) {
                faqItem.classList.add('active');
            }
        });
    });
}

// ================================
// UTILIDADES
// ================================

function formatDate(date) {
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'Ahora mismo';
    if (minutes < 60) return `Hace ${minutes} minuto${minutes !== 1 ? 's' : ''}`;
    if (hours < 24) return `Hace ${hours} hora${hours !== 1 ? 's' : ''}`;
    if (days < 7) return `Hace ${days} día${days !== 1 ? 's' : ''}`;
    
    return date.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
}

function getInitials(name) {
    if (!name) return '?';
    
    const words = name.trim().split(' ');
    if (words.length === 1) {
        return words[0].substring(0, 2).toUpperCase();
    }
    
    return (words[0][0] + words[words.length - 1][0]).toUpperCase();
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function showLoading() {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Cargando comentarios...</p>
        </div>
    `;
}

function hideLoading() {
    const loadingContainer = document.querySelector('.loading-container');
    if (loadingContainer) {
        loadingContainer.remove();
    }
}