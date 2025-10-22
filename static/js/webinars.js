// Modal functionality
const addEventBtn = document.getElementById('addEventBtn');
const modal = document.getElementById('addEventModal');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const eventForm = document.getElementById('eventForm');
const eventsGrid = document.getElementById('eventsGrid');

// User menu dropdown
const userMenuBtn = document.getElementById('userMenuBtn');
const userDropdown = document.getElementById('userDropdown');

if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userMenuBtn.classList.toggle('active');
        userDropdown.classList.toggle('active');
    });

    document.addEventListener('click', () => {
        userMenuBtn.classList.remove('active');
        userDropdown.classList.remove('active');
    });

    userDropdown.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

// Open modal
addEventBtn.addEventListener('click', () => {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
});

// Close modal
const closeModalFunction = () => {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
    eventForm.reset();
};

closeModal.addEventListener('click', closeModalFunction);
cancelBtn.addEventListener('click', closeModalFunction);

// Close modal on outside click
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModalFunction();
    }
});

// Handle form submission
eventForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const eventType = document.getElementById('eventType').value;
    const eventTitle = document.getElementById('eventTitle').value;
    const eventDescription = document.getElementById('eventDescription').value;
    const eventDate = document.getElementById('eventDate').value;
    const eventTime = document.getElementById('eventTime').value;
    const eventLocation = document.getElementById('eventLocation').value;
    const eventUrl = document.getElementById('eventUrl').value;
    const eventImage = document.getElementById('eventImage').value;
    const eventCertificate = document.getElementById('eventCertificate').checked;

    // Format date
    const date = new Date(eventDate);
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    const formattedDate = date.toLocaleDateString('es-ES', options);

    // Create new event card
    const newEventCard = document.createElement('article');
    newEventCard.className = 'event-card';
    newEventCard.setAttribute('data-category', eventType);

    const imageUrl = eventImage || 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=500&h=300&fit=crop';

    newEventCard.innerHTML = `
        <div class="event-status upcoming">Próximamente</div>
        <div class="event-image">
            <img src="${imageUrl}" alt="${eventTitle}">
        </div>
        <div class="event-content">
            <div class="event-meta">
                <span class="event-type ${eventType}">${eventType.charAt(0).toUpperCase() + eventType.slice(1)}</span>
                ${eventCertificate ? `
                    <span class="event-certificate">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="8" r="7"/>
                            <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
                        </svg>
                        Certificado
                    </span>
                ` : ''}
            </div>
            <h3>${eventTitle}</h3>
            <p>${eventDescription}</p>
            <div class="event-info">
                <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    ${formattedDate}
                </div>
                ${eventTime ? `
                    <div class="info-item">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        ${eventTime}
                    </div>
                ` : ''}
                <div class="info-item">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                    ${eventLocation}
                </div>
            </div>
            <a href="${eventUrl}" target="_blank" class="event-btn">
                Más información
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="5" y1="12" x2="19" y2="12"/>
                    <polyline points="12 5 19 12 12 19"/>
                </svg>
            </a>
        </div>
    `;

    // Add to grid
    eventsGrid.insertBefore(newEventCard, eventsGrid.firstChild);

    // Close modal and reset form
    closeModalFunction();

    // Show success message (optional)
    alert('¡Evento agregado exitosamente!');
});

// Filter functionality
const filterBtns = document.querySelectorAll('.filter-btn');
const eventCards = document.querySelectorAll('.event-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');

        eventCards.forEach(card => {
            if (filter === 'all') {
                card.classList.remove('hidden');
            } else {
                const category = card.getAttribute('data-category');
                if (category === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            }
        });
    });
});

// Search functionality
const searchInput = document.getElementById('searchInput');

searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();

    eventCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();

        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });

    // If search is empty, reset filters
    if (searchTerm === '') {
        const activeFilter = document.querySelector('.filter-btn.active');
        const filter = activeFilter.getAttribute('data-filter');
        
        eventCards.forEach(card => {
            if (filter === 'all') {
                card.classList.remove('hidden');
            } else {
                const category = card.getAttribute('data-category');
                if (category === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            }
        });
    }
});