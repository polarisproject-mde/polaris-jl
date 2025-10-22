// Variables globales
let currentQuestionIndex = 0;
const questions = document.querySelectorAll('.question-card');
const totalQuestions = questions.length;
const progressBar = document.getElementById('progressBar');
const currentQuestionSpan = document.getElementById('currentQuestion');

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    updateProgress();
    
    // Agregar listeners a las opciones para auto-avance (opcional)
    const optionInputs = document.querySelectorAll('.option-input');
    optionInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Opcional: auto-avanzar después de seleccionar
            // setTimeout(() => {
            //     if (currentQuestionIndex < totalQuestions - 1) {
            //         nextQuestion();
            //     }
            // }, 500);
        });
    });
});

// Función para avanzar a la siguiente pregunta
function nextQuestion() {
    // Validar que se haya seleccionado una opción
    const currentQuestion = questions[currentQuestionIndex];
    const selectedOption = currentQuestion.querySelector('.option-input:checked');
    
    if (!selectedOption) {
        // Mostrar error visual
        const optionsContainer = currentQuestion.querySelector('.options-container');
        optionsContainer.classList.add('error');
        
        // Mostrar mensaje de error
        showNotification('Por favor, selecciona una respuesta antes de continuar', 'error');
        
        setTimeout(() => {
            optionsContainer.classList.remove('error');
        }, 500);
        
        return;
    }
    
    // Ocultar pregunta actual
    questions[currentQuestionIndex].style.display = 'none';
    
    // Avanzar índice
    currentQuestionIndex++;
    
    // Mostrar siguiente pregunta
    if (currentQuestionIndex < totalQuestions) {
        questions[currentQuestionIndex].style.display = 'block';
        updateProgress();
        scrollToTop();
    }
}

// Función para retroceder a la pregunta anterior
function previousQuestion() {
    // Ocultar pregunta actual
    questions[currentQuestionIndex].style.display = 'none';
    
    // Retroceder índice
    currentQuestionIndex--;
    
    // Mostrar pregunta anterior
    if (currentQuestionIndex >= 0) {
        questions[currentQuestionIndex].style.display = 'block';
        updateProgress();
        scrollToTop();
    }
}

// Actualizar barra de progreso
function updateProgress() {
    const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    progressBar.style.width = progress + '%';
    currentQuestionSpan.textContent = currentQuestionIndex + 1;
}

// Scroll suave al inicio del contenedor
function scrollToTop() {
    const testContainer = document.querySelector('.test-container');
    testContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Validación antes de enviar el formulario
document.getElementById('testForm').addEventListener('submit', function(e) {
    // Verificar que todas las preguntas estén respondidas
    let allAnswered = true;
    
    questions.forEach((question, index) => {
        const questionNumber = index + 1;
        const input = question.querySelector('.option-input:checked');
        
        if (!input) {
            allAnswered = false;
        }
    });
    
    if (!allAnswered) {
        e.preventDefault();
        showNotification('Por favor, responde todas las preguntas antes de finalizar', 'error');
        return false;
    }
    
    // Mostrar estado de carga
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span>Procesando...</span>';
    
    // El formulario se enviará normalmente
    return true;
});

// Sistema de notificaciones
function showNotification(message, type = 'info') {
    // Remover notificación existente si la hay
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Crear nueva notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${type === 'error' ? 
                    '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>' :
                    '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
                }
            </svg>
            <span>${message}</span>
        </div>
    `;
    
    // Agregar estilos inline
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'error' ? 'rgba(255, 82, 82, 0.95)' : 'rgba(33, 150, 243, 0.95)'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 350px;
    `;
    
    notification.querySelector('.notification-content').style.cssText = `
        display: flex;
        align-items: center;
        gap: 10px;
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 4 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Agregar estilos de animación para las notificaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Prevenir navegación accidental
window.addEventListener('beforeunload', function(e) {
    // Verificar si hay preguntas respondidas
    const answeredQuestions = document.querySelectorAll('.option-input:checked').length;
    
    if (answeredQuestions > 0 && currentQuestionIndex < totalQuestions - 1) {
        e.preventDefault();
        e.returnValue = '¿Estás seguro de que quieres salir? Perderás tu progreso en el test.';
        return e.returnValue;
    }
});

// Atajos de teclado (opcional)
document.addEventListener('keydown', function(e) {
    // Enter o flecha derecha para siguiente
    if (e.key === 'Enter' || e.key === 'ArrowRight') {
        if (currentQuestionIndex < totalQuestions - 1) {
            const nextBtn = questions[currentQuestionIndex].querySelector('.btn-primary');
            if (nextBtn) {
                nextBtn.click();
            }
        }
    }
    
    // Flecha izquierda para anterior
    if (e.key === 'ArrowLeft') {
        if (currentQuestionIndex > 0) {
            const prevBtn = questions[currentQuestionIndex].querySelector('.btn-secondary');
            if (prevBtn) {
                prevBtn.click();
            }
        }
    }
    
    // Números 1-5 para seleccionar opciones
    if (e.key >= '1' && e.key <= '5') {
        const optionIndex = parseInt(e.key) - 1;
        const options = questions[currentQuestionIndex].querySelectorAll('.option-input');
        if (options[optionIndex]) {
            options[optionIndex].checked = true;
        }
    }
});