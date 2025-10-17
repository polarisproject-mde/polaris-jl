// Blog functionality
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const addContentBtn = document.getElementById('addContentBtn');
    const modal = document.getElementById('addContentModal');
    const closeModal = document.getElementById('closeModal');
    const cancelBtn = document.getElementById('cancelBtn');
    const contentForm = document.getElementById('contentForm');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    const articlesGrid = document.getElementById('articlesGrid');

    // Open modal
    addContentBtn.addEventListener('click', function() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    // Close modal functions
    function closeModalFunc() {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
        contentForm.reset();
    }

    closeModal.addEventListener('click', closeModalFunc);
    cancelBtn.addEventListener('click', closeModalFunc);

    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModalFunc();
        }
    });

    // Close modal with ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModalFunc();
        }
    });

    // Form submission
    contentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const contentType = document.getElementById('contentType').value;
        const category = document.getElementById('contentCategory').value;
        const title = document.getElementById('contentTitle').value;
        const description = document.getElementById('contentDescription').value;
        const url = document.getElementById('contentUrl').value;
        const imageUrl = document.getElementById('contentImage').value || 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg';
        const duration = document.getElementById('contentDuration').value;

        // Create new article card
        const articleCard = createArticleCard({
            type: contentType,
            category: category,
            title: title,
            description: description,
            url: url,
            image: imageUrl,
            duration: duration,
            date: new Date().toLocaleDateString('es-ES', { 
                day: 'numeric', 
                month: 'long', 
                year: 'numeric' 
            })
        });

        // Add to grid
        articlesGrid.insertBefore(articleCard, articlesGrid.firstChild);

        // Close modal and reset form
        closeModalFunc();

        // Show success message (optional)
        alert('¡Contenido agregado exitosamente!');
    });

    // Create article card function
    function createArticleCard(data) {
        const article = document.createElement('article');
        article.className = 'article-card';
        article.dataset.category = data.category;

        if (data.type === 'video') {
            article.classList.add('video-card');
        }

        const categoryNames = {
            'orientacion': 'Orientación',
            'estudio': 'Estudio',
            'desarrollo': 'Desarrollo'
        };

        article.innerHTML = `
            <div class="article-image ${data.type === 'video' ? 'video-thumbnail' : ''}">
                <img src="${data.image}" alt="${data.title}">
                ${data.type === 'video' ? `
                    <div class="play-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24" fill="white">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                    </div>
                ` : ''}
                <span class="article-badge ${data.type === 'video' ? 'video-badge' : ''}">${data.type === 'video' ? 'Video' : categoryNames[data.category]}</span>
            </div>
            <div class="article-content">
                <span class="article-date">${data.date}</span>
                <h3>${data.title}</h3>
                <p>${data.description}</p>
                <div class="article-footer">
                    <span class="article-read-time">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        ${data.duration} min
                    </span>
                    <a href="${data.url}" target="_blank" class="read-more">${data.type === 'video' ? 'Ver video' : 'Leer más'} →</a>
                </div>
            </div>
        `;

        return article;
    }

    // Filter functionality
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.dataset.filter;
            filterArticles(filter);
        });
    });

    function filterArticles(filter) {
        const articles = articlesGrid.querySelectorAll('.article-card');
        
        articles.forEach(article => {
            if (filter === 'all') {
                article.classList.remove('hidden');
            } else if (filter === 'videos') {
                if (article.classList.contains('video-card')) {
                    article.classList.remove('hidden');
                } else {
                    article.classList.add('hidden');
                }
            } else {
                if (article.dataset.category === filter) {
                    article.classList.remove('hidden');
                } else {
                    article.classList.add('hidden');
                }
            }
        });
    }

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const articles = articlesGrid.querySelectorAll('.article-card');
        
        articles.forEach(article => {
            const title = article.querySelector('h3').textContent.toLowerCase();
            const description = article.querySelector('p').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                article.classList.remove('hidden');
            } else {
                article.classList.add('hidden');
            }
        });

        // If search is empty, restore filter
        if (searchTerm === '') {
            const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
            filterArticles(activeFilter);
        }
    });

    // Make article cards clickable (open in new tab)
    articlesGrid.addEventListener('click', function(e) {
        const article = e.target.closest('.article-card');
        if (article && !e.target.closest('.read-more')) {
            const link = article.querySelector('.read-more');
            if (link) {
                window.open(link.href, '_blank');
            }
        }
    });
});