// ============================================
// CONFIGURACIÓN GLOBAL Y CONSTANTES
// ============================================

const API_URL = '/api';
const COMMENTS_PER_PAGE = 10;
const AUTO_SAVE_INTERVAL = 3000; // Auto-guardar borrador cada 3 segundos
const ANIMATION_DURATION = 300;

// Estado global mejorado
let state = {
    comments: [],
    offset: 0,
    hasMore: true,
    isLoading: false,
    editingCommentId: null,
    currentSort: 'newest',
    currentFilter: 'all',
    currentView: 'list',
    autoSaveTimer: null,
    searchQuery: '',
    likedComments: new Set(JSON.parse(localStorage.getItem('likedComments') || '[]'))
};

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initializeForum();
});

function initializeForum() {
    loadComments();
    loadPopularTopics();
    setupEventListeners();
    loadDraft();
    setupAutoSave();
    addSearchFunctionality();
    setupInfiniteScroll();
    setupKeyboardShortcuts();
}

// ============================================
// EVENT LISTENERS MEJORADOS
// ============================================

function setupEventListeners() {
    // Formulario de comentarios
    const commentForm = document.getElementById('comment-form');
    commentForm.addEventListener('submit', handleCommentSubmit);
    
    // Contador de caracteres en tiempo real
    const commentInput = document.getElementById('comment-input');
    commentInput.addEventListener('input', debounce(updateCharacterCount, 100));
    
    // Auto-expandir textarea
    commentInput.addEventListener('input', autoResizeTextarea);
    
    // Botón de reiniciar
    window.resetCommentForm = resetForm;
    
    // Botón de guardar borrador
    const saveDraftBtn = document.getElementById('save-draft');
    saveDraftBtn.addEventListener('click', saveDraft);
    
    // Controles de vista
    const viewBtns = document.querySelectorAll('.view-btn');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', handleViewChange);
    });
    
    // Ordenamiento
    const sortSelect = document.getElementById('sort-comments');
    sortSelect.addEventListener('change', handleSortChange);
    
    // Filtro por tema
    const filterSelect = document.getElementById('filter-topic');
    filterSelect.addEventListener('change', handleFilterChange);
    
    // Cargar más comentarios
    const loadMoreBtn = document.getElementById('load-more-btn');
    loadMoreBtn.addEventListener('click', loadMoreComments);
    
    // FAQ Accordion
    setupFAQAccordion();
    
    // Filtro de temas desde el sidebar
    setupTopicFilters();
    
    // Detectar salida de página con cambios sin guardar
    window.addEventListener('beforeunload', handleBeforeUnload);
}

// ============================================
// AUTO-GUARDAR BORRADOR
// ============================================

function setupAutoSave() {
    const commentInput = document.getElementById('comment-input');
    const userName = document.getElementById('user-name');
    const userTopic = document.getElementById('user-topic');
    
    [commentInput, userName, userTopic].forEach(element => {
        element.addEventListener('input', () => {
            clearTimeout(state.autoSaveTimer);
            state.autoSaveTimer = setTimeout(() => {
                autoSaveDraft();
            }, AUTO_SAVE_INTERVAL);
        });
    });
}

function autoSaveDraft() {
    const nombre = document.getElementById('user-name').value.trim();
    const tema = document.getElementById('user-topic').value;
    const contenido = document.getElementById('comment-input').value.trim();
    
    if (contenido.length > 0) {
        const draft = {
            nombre,
            tema,
            contenido,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('comment_draft', JSON.stringify(draft));
        showAutoSaveIndicator();
    }
}

function showAutoSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'auto-save-indicator';
    indicator.textContent = '✓ Borrador guardado';
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--success-green);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s;
    `;
    
    document.body.appendChild(indicator);
    
    setTimeout(() => indicator.style.opacity = '1', 10);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => indicator.remove(), 300);
    }, 2000);
}

// ============================================
// BÚSQUEDA EN TIEMPO REAL
// ============================================

function addSearchFunctionality() {
    const searchHTML = `
        <div class="search-container" style="margin-bottom: 24px;">
            <div class="search-box">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input type="text" id="search-comments" placeholder="Buscar en los comentarios..." />
                <button id="clear-search" style="display: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>
        </div>
    `;
    
    const commentsHeader = document.querySelector('.comments-header');
    commentsHeader.insertAdjacentHTML('afterend', searchHTML);
    
    const searchInput = document.getElementById('search-comments');
    const clearBtn = document.getElementById('clear-search');
    
    searchInput.addEventListener('input', debounce((e) => {
        state.searchQuery = e.target.value.trim().toLowerCase();
        clearBtn.style.display = state.searchQuery ? 'block' : 'none';
        filterCommentsLocally();
    }, 300));
    
    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        state.searchQuery = '';
        clearBtn.style.display = 'none';
        filterCommentsLocally();
    });
}

function filterCommentsLocally() {
    if (!state.searchQuery) {
        displayComments(state.comments);
        return;
    }
    
    const filtered = state.comments.filter(comment => {
        return comment.nombre.toLowerCase().includes(state.searchQuery) ||
               comment.contenido.toLowerCase().includes(state.searchQuery) ||
               (comment.tema && comment.tema.toLowerCase().includes(state.searchQuery));
    });
    
    displayComments(filtered);
    
    if (filtered.length === 0) {
        const commentsList = document.getElementById('comments-list');
        commentsList.innerHTML = `
            <div class="no-results" style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 3rem; margin-bottom: 16px;">🔍</div>
                <h4 style="margin-bottom: 8px; color: var(--azul-dark);">No se encontraron resultados</h4>
                <p style="color: var(--gray-500);">Intenta con otros términos de búsqueda</p>
            </div>
        `;
    }
}

// ============================================
// INFINITE SCROLL
// ============================================

function setupInfiniteScroll() {
    const commentsList = document.getElementById('comments-list');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && state.hasMore && !state.isLoading && !state.searchQuery) {
                loadMoreComments();
            }
        });
    }, {
        root: null,
        rootMargin: '100px',
        threshold: 0.1
    });
    
    // Observar el botón "Cargar más"
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (loadMoreBtn) {
        observer.observe(loadMoreBtn);
    }
}

// ============================================
// ATAJOS DE TECLADO
// ============================================

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K: Enfocar búsqueda
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('search-comments');
            if (searchInput) searchInput.focus();
        }
        
        // Escape: Cancelar edición
        if (e.key === 'Escape' && state.editingCommentId) {
            resetForm();
        }
        
        // Ctrl/Cmd + Enter: Enviar formulario
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const commentInput = document.getElementById('comment-input');
            if (document.activeElement === commentInput) {
                e.preventDefault();
                document.getElementById('comment-form').dispatchEvent(new Event('submit'));
            }
        }
    });
}

// ============================================
// CARGAR COMENTARIOS (MEJORADO)
// ============================================

async function loadComments(reset = true) {
    if (state.isLoading) return;
    
    if (reset) {
        state.offset = 0;
        state.comments = [];
    }
    
    state.isLoading = true;
    
    const sortSelect = document.getElementById('sort-comments');
    const filterSelect = document.getElementById('filter-topic');
    const orden = sortSelect.value;
    const tema = filterSelect.value;
    
    try {
        showLoading();
        
        const url = `${API_URL}/comentarios?orden=${orden}&tema=${tema}&limit=${COMMENTS_PER_PAGE}&offset=${state.offset}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Error al cargar comentarios');
        }
        
        const data = await response.json();
        
        if (reset) {
            state.comments = data.comentarios;
        } else {
            state.comments = [...state.comments, ...data.comentarios];
        }
        
        state.hasMore = data.has_more;
        state.offset += data.comentarios.length;
        
        displayComments(state.comments);
        updateLoadMoreButton();
        
        // Animar entrada de comentarios
        animateCommentsIn();
        
    } catch (error) {
        console.error('Error al cargar comentarios:', error);
        showNotification('Error al cargar comentarios', 'error');
    } finally {
        hideLoading();
        state.isLoading = false;
    }
}

function animateCommentsIn() {
    const comments = document.querySelectorAll('.comment-item');
    comments.forEach((comment, index) => {
        comment.style.opacity = '0';
        comment.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            comment.style.transition = 'all 0.4s ease-out';
            comment.style.opacity = '1';
            comment.style.transform = 'translateY(0)';
        }, index * 50);
    });
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
    
    // Agregar event listeners a los botones de acción
    comments.forEach(comment => {
        setupCommentActions(comment.id);
    });
}

function createCommentHTML(comment) {
    const date = new Date(comment.fecha_creacion);
    const formattedDate = formatDate(date);
    const initials = getInitials(comment.nombre);
    const wasEdited = comment.fecha_creacion !== comment.fecha_actualizacion;
    const isLiked = state.likedComments.has(comment.id);
    
    const temaLabels = {
        'orientacion': 'Orientación',
        'universidades': 'Universidades',
        'carreras': 'Carreras',
        'becas': 'Becas',
        'experiencias': 'Experiencias',
        'otros': 'Otros'
    };
    
    const temaColors = {
        'orientacion': '#3b82f6',
        'universidades': '#8b5cf6',
        'carreras': '#10b981',
        'becas': '#f59e0b',
        'experiencias': '#ec4899',
        'otros': '#6b7280'
    };
    
    const temaDisplay = comment.tema ? temaLabels[comment.tema] || comment.tema : '';
    const temaColor = comment.tema ? temaColors[comment.tema] || '#6b7280' : '';
    
    // Highlight del texto de búsqueda
    let contenidoDisplay = escapeHtml(comment.contenido);
    if (state.searchQuery) {
        const regex = new RegExp(`(${state.searchQuery})`, 'gi');
        contenidoDisplay = contenidoDisplay.replace(regex, '<mark style="background: #fef08a; padding: 2px 4px; border-radius: 3px;">$1</mark>');
    }
    
    return `
        <div class="comment-item" data-comment-id="${comment.id}" style="opacity: 0; transform: translateY(20px);">
            <div class="comment-header">
                <div class="comment-author">
                    <div class="author-avatar" style="background: linear-gradient(135deg, ${temaColor || '#010c1e'}, ${adjustColor(temaColor || '#010c1e', 30)})">${initials}</div>
                    <div class="author-info">
                        <h4>${escapeHtml(comment.nombre)}</h4>
                        <time datetime="${comment.fecha_creacion}" title="${date.toLocaleString('es-ES')}">${formattedDate}</time>
                        ${wasEdited ? '<span class="edited-label">(editado)</span>' : ''}
                        ${temaDisplay ? `<span class="comment-topic" style="background: ${temaColor}">${temaDisplay}</span>` : ''}
                    </div>
                </div>
                <div class="comment-actions-top">
                    <button class="edit-btn" onclick="editComment(${comment.id})" title="Editar (E)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                    </button>
                    <button class="delete-btn" onclick="deleteComment(${comment.id})" title="Eliminar (Del)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="comment-content">
                <p>${contenidoDisplay}</p>
            </div>
            <div class="comment-actions">
                <button class="like-btn ${isLiked ? 'liked' : ''}" onclick="likeComment(${comment.id})" data-likes="${comment.likes}" title="Me gusta (L)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="${isLiked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                        <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
                    </svg>
                    <span class="like-count">${comment.likes}</span>
                </button>
                <button class="share-btn" onclick="shareComment(${comment.id})" title="Compartir">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="18" cy="5" r="3"></circle>
                        <circle cx="6" cy="12" r="3"></circle>
                        <circle cx="18" cy="19" r="3"></circle>
                        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                    </svg>
                </button>
            </div>
        </div>
    `;
}

function setupCommentActions(commentId) {
    const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
    if (!commentItem) return;
    
    // Efecto hover mejorado
    commentItem.addEventListener('mouseenter', () => {
        commentItem.style.transform = 'translateY(-4px)';
    });
    
    commentItem.addEventListener('mouseleave', () => {
        commentItem.style.transform = 'translateY(0)';
    });
}

// ============================================
// CREAR/EDITAR COMENTARIO (MEJORADO)
// ============================================

async function handleCommentSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.querySelector('.btn-text').textContent;
    
    const nombre = document.getElementById('user-name').value.trim();
    const tema = document.getElementById('user-topic').value;
    const contenido = document.getElementById('comment-input').value.trim();
    
    // Validaciones mejoradas
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
    
    // Deshabilitar botón mientras se procesa
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Publicando...';
    
    try {
        const comentarioData = {
            nombre: nombre,
            tema: tema || null,
            contenido: contenido
        };
        
        let response;
        
        if (state.editingCommentId) {
            response = await fetch(`${API_URL}/comentarios/${state.editingCommentId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contenido: contenido,
                    tema: tema || null
                })
            });
        } else {
            response = await fetch(`${API_URL}/comentarios`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(comentarioData)
            });
        }
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al procesar el comentario');
        }
        
        const newComment = await response.json();
        
        // Animación de éxito
        submitBtn.classList.add('success-animation');
        submitBtn.querySelector('.btn-text').textContent = '✓ Publicado';
        
        setTimeout(() => {
            resetForm();
            submitBtn.classList.remove('success-animation');
            submitBtn.querySelector('.btn-text').textContent = originalText;
        }, 1500);
        
        // Recargar comentarios
        await loadComments(true);
        
        // Recargar temas populares
        await loadPopularTopics();
        
        // Mostrar notificación
        showNotification(
            state.editingCommentId ? '✓ Comentario actualizado correctamente' : '✓ Comentario publicado correctamente', 
            'success'
        );
        
        // Resetear modo edición
        state.editingCommentId = null;
        updateFormMode(false);
        
        // Scroll al comentario nuevo con efecto
        setTimeout(() => {
            const firstComment = document.querySelector('.comment-item');
            if (firstComment) {
                firstComment.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstComment.style.animation = 'highlight-pulse 1s ease-out';
            }
        }, 100);
        
    } catch (error) {
        console.error('Error al procesar comentario:', error);
        showNotification(error.message || 'Error al procesar el comentario', 'error');
    } finally {
        submitBtn.disabled = false;
        if (!submitBtn.classList.contains('success-animation')) {
            submitBtn.querySelector('.btn-text').textContent = originalText;
        }
    }
}

// ============================================
// EDITAR COMENTARIO (MEJORADO)
// ============================================

window.editComment = async function(commentId) {
    try {
        const comment = state.comments.find(c => c.id === commentId);
        if (!comment) {
            showNotification('Comentario no encontrado', 'error');
            return;
        }
        
        // Llenar el formulario con los datos del comentario
        document.getElementById('user-name').value = comment.nombre;
        document.getElementById('user-topic').value = comment.tema || '';
        document.getElementById('comment-input').value = comment.contenido;
        
        // Actualizar contador de caracteres
        updateCharacterCount();
        
        // Marcar que estamos en modo edición
        state.editingCommentId = commentId;
        updateFormMode(true);
        
        // Scroll al formulario con animación suave
        const form = document.getElementById('comment-form');
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Pulso visual en el formulario
        form.style.animation = 'highlight-pulse 1s ease-out';
        setTimeout(() => form.style.animation = '', 1000);
        
        // Focus en el textarea
        setTimeout(() => {
            const textarea = document.getElementById('comment-input');
            textarea.focus();
            textarea.setSelectionRange(textarea.value.length, textarea.value.length);
        }, 500);
        
    } catch (error) {
        console.error('Error al editar comentario:', error);
        showNotification('Error al cargar el comentario para editar', 'error');
    }
};

function updateFormMode(isEditing) {
    const formHeader = document.querySelector('.form-header h3');
    const submitBtn = document.querySelector('.submit-btn .btn-text');
    const form = document.getElementById('comment-form');
    
    if (isEditing) {
        formHeader.innerHTML = '✏️ Editar comentario';
        submitBtn.textContent = 'Actualizar Comentario';
        form.classList.add('editing-mode');
        
        // Agregar botón de cancelar
        if (!document.getElementById('cancel-edit-btn')) {
            const cancelBtn = document.createElement('button');
            cancelBtn.id = 'cancel-edit-btn';
            cancelBtn.type = 'button';
            cancelBtn.className = 'btn-reset';
            cancelBtn.textContent = 'Cancelar';
            cancelBtn.onclick = resetForm;
            document.querySelector('.form-actions-left').appendChild(cancelBtn);
        }
    } else {
        formHeader.innerHTML = 'Comparte tu experiencia';
        submitBtn.textContent = 'Publicar Comentario';
        form.classList.remove('editing-mode');
        
        // Remover botón de cancelar
        const cancelBtn = document.getElementById('cancel-edit-btn');
        if (cancelBtn) cancelBtn.remove();
    }
}

// ============================================
// ELIMINAR COMENTARIO (MEJORADO)
// ============================================

window.deleteComment = async function(commentId) {
    const comment = state.comments.find(c => c.id === commentId);
    if (!comment) return;
    
    // Modal de confirmación mejorado
    const confirmed = await showConfirmDialog({
        title: '¿Eliminar comentario?',
        message: 'Esta acción no se puede deshacer. ¿Estás seguro de que quieres eliminar este comentario?',
        confirmText: 'Eliminar',
        cancelText: 'Cancelar',
        type: 'danger'
    });
    
    if (!confirmed) return;
    
    try {
        const response = await fetch(`${API_URL}/comentarios/${commentId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar el comentario');
        }
        
        // Animación de salida
        const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
        if (commentItem) {
            commentItem.style.transition = 'all 0.3s ease-out';
            commentItem.style.opacity = '0';
            commentItem.style.transform = 'translateX(-100%)';
            
            setTimeout(async () => {
                await loadComments(true);
                await loadPopularTopics();
                showNotification('✓ Comentario eliminado correctamente', 'success');
            }, 300);
        }
        
    } catch (error) {
        console.error('Error al eliminar comentario:', error);
        showNotification('Error al eliminar el comentario', 'error');
    }
};

// ============================================
// DAR LIKE (MEJORADO)
// ============================================

window.likeComment = async function(commentId) {
    const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
    const likeBtn = commentItem.querySelector('.like-btn');
    const likeCount = commentItem.querySelector('.like-count');
    
    // Prevenir múltiples clicks
    if (likeBtn.disabled) return;
    likeBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/comentarios/${commentId}/like`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Error al dar like');
        }
        
        const data = await response.json();
        
        // Actualizar el contador con animación
        const oldCount = parseInt(likeCount.textContent);
        const newCount = data.likes;
        
        animateNumber(likeCount, oldCount, newCount, 300);
        
        // Animación de like
        likeBtn.classList.add('liked');
        state.likedComments.add(commentId);
        localStorage.setItem('likedComments', JSON.stringify([...state.likedComments]));
        
        // Actualizar SVG
        const svg = likeBtn.querySelector('svg');
        svg.setAttribute('fill', 'currentColor');
        
        // Efecto de partículas
        createLikeParticles(likeBtn);
        
        // Actualizar en el array local
        const comment = state.comments.find(c => c.id === commentId);
        if (comment) {
            comment.likes = data.likes;
        }
        
    } catch (error) {
        console.error('Error al dar like:', error);
        showNotification('Error al dar like', 'error');
    } finally {
        setTimeout(() => {
            likeBtn.disabled = false;
        }, 300);
    }
};

// ============================================
// COMPARTIR COMENTARIO
// ============================================

window.shareComment = async function(commentId) {
    const comment = state.comments.find(c => c.id === commentId);
    if (!comment) return;
    
    const shareText = `"${comment.contenido}" - ${comment.nombre} en Foro Polaris`;
    const shareUrl = `${window.location.origin}/blog#comment-${commentId}`;
    
    // Intentar usar la API nativa de compartir
    if (navigator.share) {
        try {
            await navigator.share({
                title: 'Comentario de Foro Polaris',
                text: shareText,
                url: shareUrl
            });
            showNotification('✓ Compartido correctamente', 'success');
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Error al compartir:', error);
            }
        }
    } else {
        // Fallback: copiar al portapapeles
        try {
            await navigator.clipboard.writeText(shareUrl);
            showNotification('✓ Enlace copiado al portapapeles', 'success');
        } catch (error) {
            console.error('Error al copiar:', error);
            showNotification('No se pudo compartir', 'error');
        }
    }
};

// ============================================
// TEMAS POPULARES (MEJORADO)
// ============================================

async function loadPopularTopics() {
    try {
        const response = await fetch(`${API_URL}/temas-populares?limit=10`);
        
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
        topicCloud.innerHTML = '<p style="text-align: center; color: var(--gray-500); font-style: italic;">No hay temas activos aún</p>';
        return;
    }
    
    // Calcular tamaño de fuente basado en popularidad
    const maxCount = Math.max(...temas.map(t => t.contador));
    const minCount = Math.min(...temas.map(t => t.contador));
    
    topicCloud.innerHTML = temas.map(tema => {
        const scale = maxCount > minCount 
            ? 0.8 + (tema.contador - minCount) / (maxCount - minCount) * 0.5
            : 1;
        
        return `
            <span class="topic-tag" 
                  data-topic="${tema.tema}" 
                  data-count="${tema.contador}"
                  style="transform: scale(${scale}); cursor: pointer;">
                ${tema.nombre_display} <span class="topic-count">(${tema.contador})</span>
            </span>
        `;
    }).join('');
}

function setupTopicFilters() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.topic-tag')) {
            const topicTag = e.target.closest('.topic-tag');
            const tema = topicTag.dataset.topic;
            
            // Efecto visual
            topicTag.style.transform = 'scale(0.95)';
            setTimeout(() => topicTag.style.transform = '', 100);
            
            // Actualizar el filtro
            const filterSelect = document.getElementById('filter-topic');
            filterSelect.value = tema;
            
            // Recargar comentarios
            loadComments(true);
            
            // Scroll a los comentarios con animación
            setTimeout(() => {
                document.getElementById('comments-container').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100);
        }
    });
}

// ============================================
// CONTROLES DE VISTA Y FILTROS
// ============================================

function handleViewChange(e) {
    const btn = e.currentTarget;
    const view = btn.dataset.view;
    
    // Actualizar botones activos
    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Cambiar vista con animación
    const commentsContainer = document.getElementById('comments-container');
    const commentsList = document.getElementById('comments-list');
    
    commentsList.style.opacity = '0';
    
    setTimeout(() => {
        if (view === 'grid') {
            commentsContainer.classList.add('grid-view');
            commentsContainer.classList.remove('list-view');
            commentsList.classList.add('grid-view');
        } else {
            commentsContainer.classList.add('list-view');
            commentsContainer.classList.remove('grid-view');
            commentsList.classList.remove('grid-view');
        }
        
        state.currentView = view;
        
        setTimeout(() => {
            commentsList.style.opacity = '1';
            animateCommentsIn();
        }, 50);
    }, 200);
}

function handleSortChange() {
    const sortSelect = document.getElementById('sort-comments');
    state.currentSort = sortSelect.value;
    loadComments(true);
    showNotification(`Ordenando por: ${getSortLabel(state.currentSort)}`, 'info');
}

function handleFilterChange() {
    const filterSelect = document.getElementById('filter-topic');
    state.currentFilter = filterSelect.value;
    loadComments(true);
    
    if (state.currentFilter !== 'all') {
        const filterLabel = filterSelect.options[filterSelect.selectedIndex].text;
        showNotification(`Filtrando por: ${filterLabel}`, 'info');
    }
}

function getSortLabel(sort) {
    const labels = {
        'newest': 'Más recientes',
        'oldest': 'Más antiguos',
        'popular': 'Más populares'
    };
    return labels[sort] || sort;
}

function loadMoreComments() {
    if (!state.hasMore || state.isLoading) return;
    loadComments(false);
}

function updateLoadMoreButton() {
    const loadMoreContainer = document.getElementById('load-more-container');
    const loadMoreBtn = document.getElementById('load-more-btn');
    
    if (state.hasMore && state.comments.length > 0) {
        loadMoreContainer.style.display = 'block';
        loadMoreBtn.disabled = false;
        loadMoreBtn.innerHTML = `
            Cargar más comentarios
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-left: 8px;">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        `;
    } else if (state.comments.length > 0) {
        loadMoreContainer.style.display = 'block';
        loadMoreBtn.disabled = true;
        loadMoreBtn.textContent = '✓ No hay más comentarios';
    } else {
        loadMoreContainer.style.display = 'none';
    }
}

// ============================================
// FORMULARIO
// ============================================

function resetForm() {
    document.getElementById('comment-form').reset();
    updateCharacterCount();
    state.editingCommentId = null;
    updateFormMode(false);
    clearDraft();
    
    // Limpiar timer de auto-guardado
    if (state.autoSaveTimer) {
        clearTimeout(state.autoSaveTimer);
    }
}

function updateCharacterCount() {
    const commentInput = document.getElementById('comment-input');
    const charCount = document.getElementById('char-count');
    const length = commentInput.value.length;
    
    charCount.textContent = length;
    
    if (length > 500) {
        charCount.style.color = 'var(--error-red)';
        charCount.style.fontWeight = 'bold';
    } else if (length > 450) {
        charCount.style.color = 'var(--warning-orange)';
        charCount.style.fontWeight = '600';
    } else if (length > 400) {
        charCount.style.color = 'var(--gray-600)';
        charCount.style.fontWeight = '500';
    } else {
        charCount.style.color = 'inherit';
        charCount.style.fontWeight = 'normal';
    }
}

function autoResizeTextarea() {
    const textarea = document.getElementById('comment-input');
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// ============================================
// BORRADOR
// ============================================

function saveDraft() {
    const nombre = document.getElementById('user-name').value.trim();
    const tema = document.getElementById('user-topic').value;
    const contenido = document.getElementById('comment-input').value.trim();
    
    if (!contenido) {
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
    showNotification('✓ Borrador guardado correctamente', 'success');
}

function loadDraft() {
    const draftStr = localStorage.getItem('comment_draft');
    
    if (!draftStr) return;
    
    try {
        const draft = JSON.parse(draftStr);
        const draftDate = new Date(draft.timestamp);
        const now = new Date();
        const daysDiff = (now - draftDate) / (1000 * 60 * 60 * 24);
        
        // No cargar borradores de más de 7 días
        if (daysDiff > 7) {
            clearDraft();
            return;
        }
        
        // Mostrar modal de confirmación personalizado
        showDraftDialog(draft);
        
    } catch (error) {
        console.error('Error al cargar borrador:', error);
        clearDraft();
    }
}

function showDraftDialog(draft) {
    const draftDate = new Date(draft.timestamp);
    const relativeTime = formatDate(draftDate);
    
    const modal = document.createElement('div');
    modal.className = 'draft-modal';
    modal.innerHTML = `
        <div class="draft-modal-overlay"></div>
        <div class="draft-modal-content">
            <div class="draft-modal-header">
                <h3>📝 Borrador encontrado</h3>
                <p>Se encontró un borrador guardado ${relativeTime}</p>
            </div>
            <div class="draft-modal-body">
                <div class="draft-preview">
                    <strong>Contenido:</strong>
                    <p>${escapeHtml(draft.contenido).substring(0, 150)}${draft.contenido.length > 150 ? '...' : ''}</p>
                </div>
            </div>
            <div class="draft-modal-actions">
                <button class="btn-secondary" onclick="dismissDraft()">Descartar</button>
                <button class="btn-primary" onclick="loadDraftData()">Cargar borrador</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    setTimeout(() => modal.classList.add('show'), 10);
    
    // Guardar referencia al borrador
    window.currentDraft = draft;
}

window.loadDraftData = function() {
    const draft = window.currentDraft;
    if (draft) {
        document.getElementById('user-name').value = draft.nombre || '';
        document.getElementById('user-topic').value = draft.tema || '';
        document.getElementById('comment-input').value = draft.contenido || '';
        updateCharacterCount();
        autoResizeTextarea();
        showNotification('✓ Borrador cargado', 'success');
    }
    dismissDraft();
};

window.dismissDraft = function() {
    const modal = document.querySelector('.draft-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    }
    window.currentDraft = null;
};

function clearDraft() {
    localStorage.removeItem('comment_draft');
}

// ============================================
// FAQ ACCORDION
// ============================================

function setupFAQAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const isActive = faqItem.classList.contains('active');
            
            // Cerrar todos los demás con animación
            document.querySelectorAll('.faq-item').forEach(item => {
                if (item !== faqItem) {
                    item.classList.remove('active');
                }
            });
            
            // Toggle el actual
            if (!isActive) {
                faqItem.classList.add('active');
            } else {
                faqItem.classList.remove('active');
            }
        });
    });
}

// ============================================
// UTILIDADES MEJORADAS
// ============================================

function formatDate(date) {
    const now = new Date();
    const diff = now - date;
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const weeks = Math.floor(days / 7);
    const months = Math.floor(days / 30);
    const years = Math.floor(days / 365);
    
    if (seconds < 10) return 'Ahora mismo';
    if (seconds < 60) return `Hace ${seconds} segundo${seconds !== 1 ? 's' : ''}`;
    if (minutes < 60) return `Hace ${minutes} minuto${minutes !== 1 ? 's' : ''}`;
    if (hours < 24) return `Hace ${hours} hora${hours !== 1 ? 's' : ''}`;
    if (days < 7) return `Hace ${days} día${days !== 1 ? 's' : ''}`;
    if (weeks < 4) return `Hace ${weeks} semana${weeks !== 1 ? 's' : ''}`;
    if (months < 12) return `Hace ${months} mes${months !== 1 ? 'es' : ''}`;
    if (years < 2) return 'Hace 1 año';
    
    return date.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });
}

function getInitials(name) {
    if (!name) return '?';
    
    const words = name.trim().split(' ').filter(w => w.length > 0);
    
    if (words.length === 0) return '?';
    if (words.length === 1) return words[0].substring(0, 2).toUpperCase();
    
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

function adjustColor(color, amount) {
    const num = parseInt(color.replace('#', ''), 16);
    const r = Math.min(255, Math.max(0, (num >> 16) + amount));
    const g = Math.min(255, Math.max(0, ((num >> 8) & 0x00FF) + amount));
    const b = Math.min(255, Math.max(0, (num & 0x0000FF) + amount));
    return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
}

function debounce(func, wait) {
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

function animateNumber(element, from, to, duration) {
    const start = performance.now();
    const diff = to - from;
    
    function update(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = easeOutQuad(progress);
        const current = Math.round(from + diff * easeProgress);
        
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function easeOutQuad(t) {
    return t * (2 - t);
}

function createLikeParticles(button) {
    const rect = button.getBoundingClientRect();
    const particles = 8;
    
    for (let i = 0; i < particles; i++) {
        const particle = document.createElement('div');
        particle.className = 'like-particle';
        particle.style.cssText = `
            position: fixed;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            width: 6px;
            height: 6px;
            background: var(--accent-blue);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
        `;
        
        document.body.appendChild(particle);
        
        const angle = (i / particles) * Math.PI * 2;
        const distance = 30 + Math.random() * 20;
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance;
        
        particle.animate([
            { transform: 'translate(0, 0) scale(1)', opacity: 1 },
            { transform: `translate(${tx}px, ${ty}px) scale(0)`, opacity: 0 }
        ], {
            duration: 600,
            easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
        }).onfinish = () => particle.remove();
    }
}

// ============================================
// NOTIFICACIONES MEJORADAS
// ============================================

function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${icons[type] || icons.info}</span>
        <span class="notification-message">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => notification.classList.add('show'), 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
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
        loadingContainer.style.opacity = '0';
        setTimeout(() => loadingContainer.remove(), 200);
    }
}

// ============================================
// MODAL DE CONFIRMACIÓN
// ============================================

function showConfirmDialog({ title, message, confirmText, cancelText, type = 'warning' }) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'confirm-modal';
        modal.innerHTML = `
            <div class="confirm-modal-overlay"></div>
            <div class="confirm-modal-content ${type}">
                <div class="confirm-modal-icon">
                    ${type === 'danger' ? '⚠️' : 'ℹ️'}
                </div>
                <h3>${title}</h3>
                <p>${message}</p>
                <div class="confirm-modal-actions">
                    <button class="btn-cancel">${cancelText}</button>
                    <button class="btn-confirm">${confirmText}</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        setTimeout(() => modal.classList.add('show'), 10);
        
        const btnConfirm = modal.querySelector('.btn-confirm');
        const btnCancel = modal.querySelector('.btn-cancel');
        
        const closeModal = (result) => {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
            resolve(result);
        };
        
        btnConfirm.onclick = () => closeModal(true);
        btnCancel.onclick = () => closeModal(false);
        modal.querySelector('.confirm-modal-overlay').onclick = () => closeModal(false);
    });
}

// ============================================
// PREVENIR PÉRDIDA DE DATOS
// ============================================

function handleBeforeUnload(e) {
    const commentInput = document.getElementById('comment-input');
    if (commentInput && commentInput.value.trim().length > 10) {
        e.preventDefault();
        e.returnValue = '¿Estás seguro de que quieres salir? Tienes cambios sin guardar.';
        return e.returnValue;
    }
}

// ============================================
// ESTILOS ADICIONALES INYECTADOS
// ============================================

const additionalStyles = `
<style>
/* Estilos para búsqueda */
.search-box {
    display: flex;
    align-items: center;
    background: white;
    border: 2px solid var(--gray-200);
    border-radius: 12px;
    padding: 12px 16px;
    gap: 12px;
    transition: all 0.3s;
}

.search-box:focus-within {
    border-color: var(--azul-dark);
    box-shadow: 0 0 0 3px rgba(1, 12, 30, 0.1);
}

.search-box svg {
    color: var(--gray-400);
    flex-shrink: 0;
}

.search-box input {
    border: none;
    outline: none;
    flex: 1;
    font-size: 1rem;
    font-family: var(--font-family-sans);
    color: var(--azul-dark);
}

#clear-search {
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--gray-400);
    border-radius: 4px;
    transition: all 0.2s;
}

#clear-search:hover {
    background: var(--gray-100);
    color: var(--gray-600);
}

/* Animación de éxito en botón */
.success-animation {
    background: var(--success-green) !important;
    transform: scale(1.05);
}

/* Animación de highlight */
@keyframes highlight-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    50% { box-shadow: 0 0 0 8px rgba(37, 99, 235, 0.3); }
}

/* Modal de borrador */
.draft-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s;
}

.draft-modal.show {
    opacity: 1;
}

.draft-modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
}

.draft-modal-content {
    position: relative;
    background: var(--blanco-gris);
    border-radius: 16px;
    max-width: 500px;
    width: 90%;
    box-shadow: var(--shadow-2xl);
    overflow: hidden;
    transform: scale(0.9);
    transition: transform 0.3s;
}

.draft-modal.show .draft-modal-content {
    transform: scale(1);
}

.draft-modal-header {
    padding: 32px 32px 24px;
    border-bottom: 2px solid var(--gray-200);
}

.draft-modal-header h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--azul-dark);
    margin: 0 0 8px;
}

.draft-modal-header p {
    color: var(--gray-600);
    margin: 0;
}

.draft-modal-body {
    padding: 24px 32px;
}

.draft-preview {
    background: #cfcfcf;
    padding: 16px;
    border-radius: 10px;
}

.draft-preview strong {
    color: var(--azul-dark);
    display: block;
    margin-bottom: 8px;
}

.draft-preview p {
    color: var(--gray-600);
    margin: 0;
    line-height: 1.5;
}

.draft-modal-actions {
    padding: 24px 32px 32px;
    display: flex;
    gap: 12px;
    justify-content: flex-end;
}

.btn-primary, .btn-secondary {
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-family: var(--font-family-sans);
}

.btn-primary {
    background: var(--azul-dark);
    color: var(--blanco-gris);
}

.btn-primary:hover {
    background: var(--azul-negro);
    transform: translateY(-2px);
}

.btn-secondary {
    background: var(--gray-200);
    color: var(--gray-700);
}

.btn-secondary:hover {
    background: var(--gray-300);
}

/* Modal de confirmación */
.confirm-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s;
}

.confirm-modal.show {
    opacity: 1;
}

.confirm-modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
}

.confirm-modal-content {
    position: relative;
    background: var(--blanco-gris);
    border-radius: 16px;
    max-width: 450px;
    width: 90%;
    padding: 32px;
    box-shadow: var(--shadow-2xl);
    text-align: center;
    transform: scale(0.9);
    transition: transform 0.3s;
}

.confirm-modal.show .confirm-modal-content {
    transform: scale(1);
}

.confirm-modal-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.confirm-modal-content h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--azul-dark);
    margin: 0 0 12px;
}

.confirm-modal-content p {
    color: var(--gray-600);
    line-height: 1.6;
    margin: 0 0 24px;
}

.confirm-modal-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
}

.btn-confirm, .btn-cancel {
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-family: var(--font-family-sans);
}

.btn-confirm {
    background: var(--error-red);
    color: white;
}

.btn-confirm:hover {
    background: #dc2626;
    transform: translateY(-2px);
}

.btn-cancel {
    background: var(--gray-200);
    color: var(--gray-700);
}

.btn-cancel:hover {
    background: var(--gray-300);
}

/* Botón de compartir */
.share-btn {
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--gray-500);
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
}

.share-btn:hover {
    background: var(--gray-100);
    color: var(--gray-700);
}

/* Notificación mejorada */
.notification {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 24px;
    min-width: 300px;
}

.notification-icon {
    font-size: 1.2rem;
    font-weight: bold;
    flex-shrink: 0;
}

.notification-message {
    flex: 1;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .search-box {
        padding: 10px 12px;
    }
    
    .draft-modal-content,
    .confirm-modal-content {
        width: 95%;
        padding: 24px;
    }
    
    .draft-modal-header {
        padding: 24px 24px 16px;
    }
    
    .draft-modal-body,
    .draft-modal-actions {
        padding: 16px 24px;
    }
}
</style>
`;

// Inyectar estilos adicionales
document.head.insertAdjacentHTML('beforeend', additionalStyles);