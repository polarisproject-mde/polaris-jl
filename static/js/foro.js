/**
 * POLARIS BLOG - ENHANCED FUNCTIONALITY 2025
 * Comprehensive blog management system with modern features
 */

class PolarisForumManager {
    constructor() {
        // State management
        this.comments = [];
        this.commentCount = 0;
        this.currentView = 'list';
        this.currentSort = 'newest';
        this.currentFilter = 'all';
        this.drafts = this.loadDrafts();
        
        // Configuration
        this.config = {
            maxCommentLength: 500,
            maxNameLength: 50,
            commentsPerPage: 10,
            autoSaveInterval: 3000
        };
        
        // Initialize
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeUI();
        this.loadSampleComments();
        this.updateDisplay();
        this.initFAQ();
        this.startAutoSave();
        this.initScrollAnimations();
    }

    /**
     * Event Binding
     */
    bindEvents() {
        // Form events
        const form = document.getElementById('comment-form');
        const commentInput = document.getElementById('comment-input');
        const nameInput = document.getElementById('user-name');
        const saveDraftBtn = document.getElementById('save-draft');

        if (form) form.addEventListener('submit', (e) => this.handleCommentSubmit(e));
        if (commentInput) {
            commentInput.addEventListener('input', () => this.updateCharacterCount());
            commentInput.addEventListener('input', () => this.autoSaveDraft());
        }
        if (nameInput) nameInput.addEventListener('input', () => this.autoSaveDraft());
        if (saveDraftBtn) saveDraftBtn.addEventListener('click', () => this.saveDraft());

        // Display controls
        const sortSelect = document.getElementById('sort-comments');
        const filterSelect = document.getElementById('filter-topic');
        const viewButtons = document.querySelectorAll('.view-btn');

        if (sortSelect) sortSelect.addEventListener('change', () => this.sortComments());
        if (filterSelect) filterSelect.addEventListener('change', () => this.filterComments());
        
        viewButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.changeView(e.target.dataset.view));
        });

        // Topic tags
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('topic-tag')) {
                this.filterByTopic(e.target.dataset.topic);
            }
        });

        // Load more
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => this.loadMoreComments());
        }

        // Window events
        window.addEventListener('beforeunload', () => this.saveDrafts());
        window.addEventListener('scroll', () => this.handleScroll());
    }

    /**
     * UI Initialization
     */
    initializeUI() {
        this.updateCharacterCount();
        this.loadDraft();
        this.updateOnlineStatus();
        
        // Initialize tooltips
        this.initTooltips();
        
        // Set initial view
        this.updateViewControls();
    }

    /**
     * Sample Comments for Demo
     */
    loadSampleComments() {
        const sampleComments = [
            {
                id: 1,
                name: "María González",
                text: "¡Hola a todos! Estoy en 11° y súper confundida sobre qué carrera estudiar. Me gusta mucho la biología pero también las matemáticas. ¿Alguien conoce carreras que combinen ambas? ¡Gracias!",
                topic: "orientacion",
                timestamp: new Date(Date.now() - 1800000), // 30 min ago
                likes: 5
            },
            {
                id: 2,
                name: "Carlos Rodríguez",
                text: "Estudié Ingeniería de Sistemas en la Universidad Nacional y fue la mejor decisión. Si alguien tiene preguntas sobre la carrera o el proceso de admisión, con gusto ayudo.",
                topic: "experiencias",
                timestamp: new Date(Date.now() - 3600000), // 1 hour ago
                likes: 8
            },
            {
                id: 3,
                name: "Ana López",
                text: "¿Saben si hay becas disponibles para estudiantes de estratos bajos? Mi familia no puede costear una universidad privada pero quiero estudiar Psicología.",
                topic: "becas",
                timestamp: new Date(Date.now() - 7200000), // 2 hours ago
                likes: 3
            }
        ];

        this.comments = sampleComments;
        this.commentCount = sampleComments.length;
    }

    /**
     * Comment Submission Handler
     */
    handleCommentSubmit(e) {
        e.preventDefault();
        
        const nameInput = document.getElementById('user-name');
        const commentInput = document.getElementById('comment-input');
        const topicSelect = document.getElementById('user-topic');
        
        const name = nameInput.value.trim();
        const text = commentInput.value.trim();
        const topic = topicSelect.value;

        // Validation
        if (!this.validateComment(name, text)) return;

        // Create comment object
        const comment = {
            id: Date.now(),
            name: name,
            text: text,
            topic: topic,
            timestamp: new Date(),
            likes: 0,
            isNew: true
        };

        // Add to comments
        this.comments.unshift(comment);
        this.commentCount++;
        
        // Reset form
        this.resetForm();
        
        // Update display
        this.updateDisplay();
        
        // Show success notification
        this.showNotification('¡Comentario publicado exitosamente!', 'success');
        
        // Clear drafts
        this.clearDraft();
        
        // Scroll to new comment
        setTimeout(() => this.scrollToLatestComment(), 500);
    }

    /**
     * Comment Validation
     */
    validateComment(name, text) {
        if (!name || name.length > this.config.maxNameLength) {
            this.showNotification('Por favor ingresa un nombre válido (máximo 50 caracteres)', 'error');
            return false;
        }

        if (!text || text.length > this.config.maxCommentLength) {
            this.showNotification(`El comentario debe tener entre 1 y ${this.config.maxCommentLength} caracteres`, 'error');
            return false;
        }

        // Check for spam patterns
        if (this.isSpam(text)) {
            this.showNotification('Tu comentario parece spam. Por favor, escribe contenido constructivo.', 'warning');
            return false;
        }

        return true;
    }

    /**
     * Simple spam detection
     */
    isSpam(text) {
        const spamPatterns = [
            /(.)\1{4,}/, // Repeated characters
            /^[A-Z\s!]{10,}$/, // All caps
            /(https?:\/\/[^\s]+.*){3,}/, // Multiple URLs
        ];
        
        return spamPatterns.some(pattern => pattern.test(text));
    }

    /**
     * Form Reset
     */
    resetForm() {
        const nameInput = document.getElementById('user-name');
        const commentInput = document.getElementById('comment-input');
        const topicSelect = document.getElementById('user-topic');
        
        if (nameInput) nameInput.value = '';
        if (commentInput) commentInput.value = '';
        if (topicSelect) topicSelect.value = '';
        
        this.updateCharacterCount();
    }

    /**
     * Display Update
     */
    updateDisplay() {
        const commentsList = document.getElementById('comments-list');
        const noComments = document.getElementById('no-comments');
        const countElement = document.getElementById('comment-count');
        const container = document.getElementById('comments-container');
        
        if (countElement) {
            this.animateNumber(countElement, this.commentCount);
        }

        const filteredComments = this.getFilteredComments();

        if (filteredComments.length === 0) {
            if (commentsList) commentsList.style.display = 'none';
            if (noComments) noComments.style.display = 'flex';
            return;
        }

        if (commentsList) commentsList.style.display = 'block';
        if (noComments) noComments.style.display = 'none';
        
        // Update view class
        if (container) {
            container.className = `comments-container ${this.currentView}-view`;
        }
        
        if (commentsList) {
            commentsList.innerHTML = filteredComments
                .map(comment => this.createCommentHTML(comment))
                .join('');
            
            // Bind events for new elements
            this.bindCommentEvents();
        }
    }

    /**
     * Get Filtered Comments
     */
    getFilteredComments() {
        let filtered = [...this.comments];

        // Apply topic filter
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(comment => 
                comment.topic === this.currentFilter
            );
        }

        // Apply sorting
        filtered.sort((a, b) => {
            switch (this.currentSort) {
                case 'newest':
                    return b.timestamp - a.timestamp;
                case 'oldest':
                    return a.timestamp - b.timestamp;
                case 'popular':
                    return b.likes - a.likes;
                default:
                    return b.timestamp - a.timestamp;
            }
        });

        return filtered;
    }

    /**
     * Create Comment HTML
     */
    createCommentHTML(comment) {
        const timeAgo = this.getTimeAgo(comment.timestamp);
        const topicLabel = this.getTopicLabel(comment.topic);
        const isNew = comment.isNew ? 'comment-new' : '';
        
        return `
            <article class="comment-item ${isNew}" data-id="${comment.id}">
                <div class="comment-header">
                    <div class="comment-author">
                        <div class="author-avatar" style="background: ${this.getAvatarColor(comment.name)}">
                            ${comment.name.charAt(0).toUpperCase()}
                        </div>
                        <div class="author-info">
                            <h4>${this.escapeHtml(comment.name)}</h4>
                            <time datetime="${comment.timestamp.toISOString()}" title="${comment.timestamp.toLocaleString()}">
                                ${timeAgo}
                            </time>
                            ${comment.topic ? `<span class="comment-topic">${topicLabel}</span>` : ''}
                        </div>
                    </div>
                    <button class="delete-btn" data-id="${comment.id}" title="Eliminar comentario" aria-label="Eliminar comentario">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 6H21M8 6V4C8 3.44772 8.44772 3 9 3H15C15.5523 3 16 3.44772 16 4V6M19 6V20C19 20.5523 18.5523 21 18 21H6C5.44772 21 5 20.5523 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                </div>
                <div class="comment-content">
                    <p>${this.formatCommentText(comment.text)}</p>
                </div>
                <div class="comment-actions">
                    <button class="like-btn" data-id="${comment.id}" aria-label="Me gusta este comentario">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M7 22H4C3.46957 22 2.96086 21.7893 2.58579 21.4142C2.21071 21.0391 2 20.5304 2 20V13C2 12.4696 2.21071 11.9609 2.58579 11.5858C2.96086 11.2107 3.46957 11 4 11H7M14 9V5C14 4.20435 13.6839 3.44129 13.1213 2.87868C12.5587 2.31607 11.7956 2 11 2L7 11V22H18.28C18.7623 22.0055 19.2304 21.8364 19.5979 21.524C19.9654 21.2116 20.2077 20.7769 20.28 20.3L21.66 11.3C21.7035 11.0134 21.6842 10.7207 21.6033 10.4423C21.5225 10.1638 21.3821 9.90629 21.1919 9.68751C21.0016 9.46873 20.7661 9.29393 20.5016 9.17522C20.2371 9.0565 19.9495 8.99672 19.66 9H14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <span>${comment.likes}</span>
                    </button>
                    <button class="reply-btn" data-id="${comment.id}" aria-label="Responder comentario">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 10H13C16.3137 10 19 12.6863 19 16V18M3 10L9 16M3 10L9 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        Responder
                    </button>
                </div>
            </article>
        `;
    }

    /**
     * Bind Comment Events
     */
    bindCommentEvents() {
        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.deleteComment(e));
        });

        // Like buttons
        document.querySelectorAll('.like-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.likeComment(e));
        });

        // Reply buttons
        document.querySelectorAll('.reply-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.replyToComment(e));
        });
    }

    /**
     * Delete Comment
     */
    deleteComment(e) {
        const commentId = parseInt(e.currentTarget.dataset.id);
        
        if (confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
            this.comments = this.comments.filter(comment => comment.id !== commentId);
            this.commentCount--;
            this.updateDisplay();
            this.showNotification('Comentario eliminado', 'success');
        }
    }

    /**
     * Like Comment
     */
    likeComment(e) {
        const commentId = parseInt(e.currentTarget.dataset.id);
        const comment = this.comments.find(c => c.id === commentId);
        
        if (comment) {
            comment.likes++;
            this.updateDisplay();
            
            // Add visual feedback
            e.currentTarget.style.transform = 'scale(1.2)';
            setTimeout(() => {
                e.currentTarget.style.transform = 'scale(1)';
            }, 200);
        }
    }

    /**
     * Reply to Comment
     */
    replyToComment(e) {
        const commentId = parseInt(e.currentTarget.dataset.id);
        const comment = this.comments.find(c => c.id === commentId);
        
        if (comment) {
            const commentInput = document.getElementById('comment-input');
            
            if (commentInput) {
                commentInput.focus();
                commentInput.value = `@${comment.name} `;
                this.updateCharacterCount();
                
                // Scroll to form
                document.getElementById('comment-form').scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        }
    }

    /**
     * Sorting
     */
    sortComments() {
        const sortSelect = document.getElementById('sort-comments');
        this.currentSort = sortSelect.value;
        this.updateDisplay();
    }

    /**
     * Filtering
     */
    filterComments() {
        const filterSelect = document.getElementById('filter-topic');
        this.currentFilter = filterSelect.value;
        this.updateDisplay();
    }

    /**
     * Filter by Topic (from topic tags)
     */
    filterByTopic(topic) {
        const filterSelect = document.getElementById('filter-topic');
        if (filterSelect) {
            filterSelect.value = topic;
            this.currentFilter = topic;
            this.updateDisplay();
        }
    }

    /**
     * Change View
     */
    changeView(view) {
        if (['list', 'grid'].includes(view)) {
            this.currentView = view;
            this.updateDisplay();
            this.updateViewControls();
        }
    }

    /**
     * Update View Controls
     */
    updateViewControls() {
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === this.currentView);
        });
    }

    /**
     * Character Count
     */
    updateCharacterCount() {
        const commentInput = document.getElementById('comment-input');
        const charCount = document.getElementById('char-count');
        
        if (commentInput && charCount) {
            const length = commentInput.value.length;
            charCount.textContent = length;
            
            // Color coding
            if (length > this.config.maxCommentLength * 0.9) {
                charCount.style.color = '#ef4444';
            } else if (length > this.config.maxCommentLength * 0.7) {
                charCount.style.color = '#f59e0b';
            } else {
                charCount.style.color = '#6b7280';
            }
        }
    }

    /**
     * Draft Management - Fixed localStorage usage for environment compatibility
     */
    autoSaveDraft() {
        clearTimeout(this.draftTimer);
        this.draftTimer = setTimeout(() => {
            this.saveDraft(false);
        }, this.config.autoSaveInterval);
    }

    saveDraft(showNotification = true) {
        const nameInput = document.getElementById('user-name');
        const commentInput = document.getElementById('comment-input');
        const topicSelect = document.getElementById('user-topic');
        
        const draft = {
            name: nameInput?.value || '',
            comment: commentInput?.value || '',
            topic: topicSelect?.value || '',
            timestamp: Date.now()
        };
        
        if (draft.name || draft.comment) {
            try {
                localStorage.setItem('polaris_forum_draft', JSON.stringify(draft));
                
                if (showNotification) {
                    this.showNotification('Borrador guardado', 'success');
                }
            } catch (e) {
                // Fallback to memory storage if localStorage isn't available
                this.memoryDraft = draft;
                if (showNotification) {
                    this.showNotification('Borrador guardado temporalmente', 'success');
                }
            }
        }
    }

    loadDraft() {
        try {
            const saved = localStorage.getItem('polaris_forum_draft');
            if (saved) {
                const draft = JSON.parse(saved);
                this.populateDraftFields(draft);
            }
        } catch (e) {
            // Fallback to memory draft
            if (this.memoryDraft) {
                this.populateDraftFields(this.memoryDraft);
            }
        }
    }

    populateDraftFields(draft) {
        const nameInput = document.getElementById('user-name');
        const commentInput = document.getElementById('comment-input');
        const topicSelect = document.getElementById('user-topic');
        
        if (nameInput) nameInput.value = draft.name || '';
        if (commentInput) commentInput.value = draft.comment || '';
        if (topicSelect) topicSelect.value = draft.topic || '';
        
        this.updateCharacterCount();
    }

    clearDraft() {
        try {
            localStorage.removeItem('polaris_forum_draft');
        } catch (e) {
            this.memoryDraft = null;
        }
    }

    loadDrafts() {
        try {
            const saved = localStorage.getItem('polaris_forum_drafts');
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            return [];
        }
    }

    saveDrafts() {
        try {
            localStorage.setItem('polaris_forum_drafts', JSON.stringify(this.drafts));
        } catch (e) {
            // Silent fail for environments without localStorage
        }
    }

    startAutoSave() {
        setInterval(() => {
            this.saveDraft(false);
        }, 30000); // Auto-save every 30 seconds
    }

    /**
     * FAQ Management
     */
    initFAQ() {
        const faqQuestions = document.querySelectorAll('.faq-question');
        
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const faqItem = question.parentElement;
                const isActive = faqItem.classList.contains('active');
                
                // Close all FAQ items
                document.querySelectorAll('.faq-item').forEach(item => {
                    item.classList.remove('active');
                });
                
                // Open clicked item if it wasn't active
                if (!isActive) {
                    faqItem.classList.add('active');
                }
            });
        });
    }

    /**
     * Utilities
     */
    getTimeAgo(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Ahora mismo';
        if (minutes < 60) return `Hace ${minutes} min`;
        if (hours < 24) return `Hace ${hours}h`;
        if (days < 7) return `Hace ${days}d`;
        return timestamp.toLocaleDateString();
    }

    getTopicLabel(topic) {
        const topics = {
            'orientacion': 'Orientación',
            'universidades': 'Universidades',
            'carreras': 'Carreras',
            'becas': 'Becas',
            'experiencias': 'Experiencias',
            'otros': 'Otros'
        };
        return topics[topic] || topic;
    }

    getAvatarColor(name) {
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
            'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
            'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
        ];
        
        let hash = 0;
        for (let i = 0; i < name.length; i++) {
            const char = name.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        
        return colors[Math.abs(hash) % colors.length];
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatCommentText(text) {
        // First escape HTML to prevent XSS
        let escapedText = this.escapeHtml(text);
        
        // Auto-link URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        escapedText = escapedText.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Format @mentions
        const mentionRegex = /@(\w+)/g;
        escapedText = escapedText.replace(mentionRegex, '<span class="mention">@$1</span>');
        
        return escapedText;
    }

    animateNumber(element, targetNumber) {
        const startNumber = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentNumber = Math.round(startNumber + (targetNumber - startNumber) * easeOutQuart);
            
            element.textContent = currentNumber;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    /**
     * Notifications
     */
    showNotification(message, type = 'success') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => notification.classList.add('show'), 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    /**
     * Scroll Animations
     */
    initScrollAnimations() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, {
                threshold: 0.1
            });

            // Observe elements as they're added
            const observeElements = () => {
                document.querySelectorAll('.comment-item:not(.animate-in), .guideline-item:not(.animate-in), .faq-item:not(.animate-in)').forEach(el => {
                    observer.observe(el);
                });
            };

            observeElements();
            
            // Re-observe after updates
            const originalUpdateDisplay = this.updateDisplay;
            this.updateDisplay = () => {
                originalUpdateDisplay.call(this);
                setTimeout(observeElements, 100);
            };
        }
    }

    scrollToLatestComment() {
        const firstComment = document.querySelector('.comment-item');
        if (firstComment) {
            firstComment.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }

    updateOnlineStatus() {
        const indicators = document.querySelectorAll('.online-indicator span');
        const count = Math.floor(Math.random() * 20) + 5; // 5-25 people
        
        indicators.forEach(indicator => {
            indicator.textContent = `${count} personas conectadas`;
        });
    }

    handleScroll() {
        const scrollY = window.scrollY;
        const heroSection = document.querySelector('.hero-section');
        
        if (heroSection) {
            const parallaxSpeed = 0.5;
            heroSection.style.transform = `translateY(${scrollY * parallaxSpeed}px)`;
        }

        // Remove existing tooltips on scroll
        const tooltips = document.querySelectorAll('.tooltip');
        tooltips.forEach(tooltip => tooltip.remove());
    }

    initTooltips() {
        // Simple tooltip implementation with improved cleanup
        const tooltipElements = document.querySelectorAll('[title]');
        
        tooltipElements.forEach(element => {
            let tooltip;
            
            element.addEventListener('mouseenter', (e) => {
                // Clean up existing tooltips
                document.querySelectorAll('.tooltip').forEach(t => t.remove());
                
                tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = e.target.dataset.title || e.target.title;
                
                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                const tooltipRect = tooltip.getBoundingClientRect();
                
                let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
                let top = rect.top - tooltipRect.height - 8;
                
                // Boundary checks
                if (left < 5) left = 5;
                if (left + tooltipRect.width > window.innerWidth - 5) {
                    left = window.innerWidth - tooltipRect.width - 5;
                }
                if (top < 5) {
                    top = rect.bottom + 8;
                }
                
                tooltip.style.left = left + 'px';
                tooltip.style.top = top + 'px';
                
                setTimeout(() => tooltip.classList.add('show'), 50);
            });
            
            element.addEventListener('mouseleave', () => {
                if (tooltip) {
                    tooltip.classList.remove('show');
                    setTimeout(() => {
                        if (tooltip && document.body.contains(tooltip)) {
                            document.body.removeChild(tooltip);
                        }
                    }, 200);
                }
            });
            
            // Store original title and remove to prevent native tooltip
            if (!element.dataset.title && element.title) {
                element.dataset.title = element.title;
                element.title = '';
            }
        });
    }

    loadMoreComments() {
        // Placeholder for load more functionality
        this.showNotification('Función "Cargar más" en desarrollo', 'info');
    }
}


// Enhanced CSS for fixes and improvements
const additionalStyles = `
.tooltip {
    position: absolute;
    background: var(--primary-dark);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    z-index: 1000;
    opacity: 0;
    transform: translateY(5px);
    transition: all 0.2s ease;
    pointer-events: none;
    white-space: nowrap;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    max-width: 250px;
    text-align: center;
}

.tooltip.show {
    opacity: 1;
    transform: translateY(0);
}

.tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: var(--primary-dark);
}

.comment-new {
    animation: newCommentHighlight 3s ease-out;
    border-left: 4px solid var(--success-green);
}

.mention {
    color: var(--accent-blue);
    font-weight: 600;
    background: rgba(37, 99, 235, 0.1);
    padding: 2px 4px;
    border-radius: 4px;
}

.animate-in {
    animation: fadeInUp 0.6s ease-out;
}

/* Prevent text overflow in comments */
.comment-content p {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}

/* Fix avatar positioning */
.author-avatar {
    flex-shrink: 0;
    min-width: 48px;
    min-height: 48px;
}

/* Improve button spacing */
.comment-actions {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--gray-200);
}

/* Fix notification positioning */
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--success-green);
    color: white;
    padding: 16px 24px;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-xl);
    font-weight: 600;
    z-index: 10000;
    transform: translateX(100%);
    transition: transform var(--transition-normal);
    max-width: 300px;
    word-wrap: break-word;
}

.notification.show {
    transform: translateX(0);
}

.notification.error {
    background: var(--error-red);
}

.notification.warning {
    background: var(--warning-orange);
}

.notification.info {
    background: var(--accent-blue);
}

@keyframes newCommentHighlight {
    0% {
        background: rgba(16, 185, 129, 0.1);
        transform: scale(1.02);
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3);
    }
    50% {
        background: rgba(16, 185, 129, 0.05);
    }
    100% {
        background: white;
        transform: scale(1);
        box-shadow: var(--shadow-sm);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Loading states */
.loading {
    opacity: 0.7;
    pointer-events: none;
    position: relative;
}

.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 20px;
    margin: -10px 0 0 -10px;
    border: 2px solid var(--gray-300);
    border-top: 2px solid var(--accent-blue);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    z-index: 10;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Enhanced focus states for accessibility */
.comment-item:focus-within {
    outline: 2px solid var(--accent-blue);
    outline-offset: 4px;
    border-radius: var(--border-radius-lg);
}

/* Responsive improvements */
@media (max-width: 640px) {
    .comment-actions {
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .like-btn, .reply-btn {
        flex: 1;
        justify-content: center;
        min-width: 100px;
    }
    
    .tooltip {
        position: fixed !important;
        left: 50% !important;
        top: 50% !important;
        transform: translate(-50%, -50%) !important;
        max-width: 250px;
        white-space: normal;
    }
    
    .notification {
        left: 10px;
        right: 10px;
        transform: translateY(-100%);
        max-width: none;
    }
    
    .notification.show {
        transform: translateY(0);
    }
    
    .comment-header {
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .delete-btn {
        opacity: 1;
        position: relative;
        margin-top: 8px;
    }
}

/* Print styles */
@media print {
    .hero-section,
    .sidebar,
    .comment-form,
    .notification {
        display: none !important;
    }
    
    .comment-item {
        break-inside: avoid;
        box-shadow: none;
        border: 1px solid #ccc;
        margin-bottom: 20px;
    }
    
    .comment-actions {
        display: none;
    }
}

/* Smooth transitions for all interactive elements */
* {
    transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease;
}

/* Fix potential z-index issues */
.hero-section {
    z-index: 1;
}

.blog-main {
    z-index: 2;
    position: relative;
}

.notification {
    z-index: 10000;
}

.tooltip {
    z-index: 9999;
}
`;

// Inject additional styles with proper cleanup
const existingStyleSheet = document.getElementById('polaris-additional-styles');
if (existingStyleSheet) {
    existingStyleSheet.remove();
}

const styleSheet = document.createElement('style');
styleSheet.id = 'polaris-additional-styles';
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Initialize the forum manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Prevent multiple initializations
    if (window.forumManager) {
        console.log('Forum Manager already initialized');
        return;
    }
    
    const forumManager = new PolarisForumManager();
    
    // Make it globally accessible for debugging
    window.forumManager = forumManager;
    
    // Performance monitoring
    if (window.performance && window.performance.mark) {
        window.performance.mark('forum-initialized');
    }
    
    console.log('Polaris Forum Manager initialized successfully!');
});

// Error handling for the entire application
window.addEventListener('error', (event) => {
    console.error('Forum Manager Error:', event.error);
    
    // Show user-friendly error message
    if (window.forumManager) {
        window.forumManager.showNotification('Ha ocurrido un error. Por favor, recarga la página.', 'error');
    }
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled Promise Rejection:', event.reason);
    event.preventDefault();
});

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

window.resetCommentForm = function() {
    // Obtener campos
    const nameInput = document.getElementById('user-name');
    const commentInput = document.getElementById('comment-input');
    const topicSelect = document.getElementById('user-topic');

    // Vaciar valores
    if (nameInput) nameInput.value = '';
    if (commentInput) commentInput.value = '';
    if (topicSelect) topicSelect.value = '';

    // Borrar borrador guardado en localStorage
    localStorage.removeItem('polaris_forum_draft');

    // Opcional: mostrar notificación o alerta
    console.log("Formulario reiniciado y borrador eliminado.");
};
