document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".question");
    const finishBtn = document.getElementById("fin-tecn");

    const totalQuestions = questions.length;
    const questionsPerBlock = 5;
    const totalBlocks = Math.ceil(totalQuestions / questionsPerBlock);

    // Agrupar preguntas en bloques
    const blocks = [];
    for (let i = 0; i < totalBlocks; i++) {
        const block = [];
        for (let j = 0; j < questionsPerBlock; j++) {
            const question = questions[i * questionsPerBlock + j];
            if (question) block.push(question);
        }
        blocks.push(block);
    }

    // Ocultar todos los bloques excepto el primero
    for (let i = 1; i < blocks.length; i++) {
        blocks[i].forEach(q => q.style.display = "none");
    }

    // Ocultar botón finalizar al inicio
    finishBtn.style.display = "none";

    // Detectar respuesta en cada botón
    questions.forEach((question, index) => {
        const buttons = question.querySelectorAll("button");
        buttons.forEach(button => {
            button.addEventListener("click", () => {
                // Marcar la respuesta seleccionada
                buttons.forEach(b => b.classList.remove("selected"));
                button.classList.add("selected");

                // Verifica si todas las preguntas del bloque actual están respondidas
                const blockIndex = Math.floor(index / questionsPerBlock);
                const currentBlock = blocks[blockIndex];

                const allAnswered = currentBlock.every(q =>
                    q.querySelector("button.selected")
                );

                // Si todas están respondidas, mostrar siguiente bloque
                if (allAnswered && blockIndex + 1 < blocks.length) {
                    blocks[blockIndex + 1].forEach(q => q.style.display = "block");
                }

                // Mostrar el botón finalizar solo si todas están respondidas
                const allQuestionsAnswered = Array.from(questions).every(q =>
                    q.querySelector("button.selected")
                );
                if (allQuestionsAnswered) {
                    finishBtn.style.display = "block";
                }
            });
        });
    });
});