/* main.js optimizado y corregido */

document.addEventListener('DOMContentLoaded', () => {
    // ─────────────────────────────────────────
    // 📌 Referencias del DOM
    // ─────────────────────────────────────────
    const equationInput = document.getElementById('equationInput');
    const solveButton = document.getElementById('solveButton');
    const solutionOutput = document.getElementById('solutionOutput');
    const loadingIndicator = document.getElementById('loading');
    const errorDisplay = document.getElementById('error');
    const calculatorButtonsContainer = document.getElementById('calculatorButtons');
    const initialConditionsContainer = document.getElementById('initialConditionsContainer');
    const addConditionButton = document.getElementById('addCondition');
    const removeConditionButton = document.getElementById('removeCondition');
    const toastContainer = document.getElementById('toastContainer');

    const examplesBtn = document.getElementById('examplesBtn');
    const helpBtn = document.getElementById('helpBtn');
    const examplesModal = document.getElementById('examplesModal');
    const helpModal = document.getElementById('helpModal');
    const closeExamples = document.getElementById('closeExamples');
    const closeHelp = document.getElementById('closeHelp');
    const examplesList = document.getElementById('examplesList');

    const copyrightBtn = document.getElementById('copyrightBtn');
    const creditsModal = document.getElementById('creditsModal');
    const closeModal = document.getElementById('closeModal');

    let conditionCount = 1;

    // ─────────────────────────────────────────
    // 🔔 Sistema de TOAST (éxito / error)
    // ─────────────────────────────────────────
    function showToast(message, type = 'success') {
        if (!toastContainer) return;

        const toast = document.createElement('div');
        const iconColor = type === 'success' ? 'text-green-500' : 'text-red-500';
        const borderColor = type === 'success' ? 'border-green-600' : 'border-red-600';
        const icon = type === 'success' ? '✔' : '✖';

        toast.className = `bg-[#1f1f1f] text-gray-200 border ${borderColor} px-4 py-3 rounded shadow-lg flex items-center gap-2 animate-slide-in`;
        toast.innerHTML = `
            <span class="${iconColor} font-bold">${icon}</span>
            <p class="text-sm">${message}</p>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('animate-slide-in');
            toast.classList.add('animate-fade-out');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // ─────────────────────────────────────────
    // 🧮 Normalización de notación de derivadas
    // ─────────────────────────────────────────
    function normalizeEquation(raw) {
        let eq = raw;

        // √(...) -> sqrt(...)
        eq = eq.replace(/√\s*\(/g, 'sqrt(');
        
        // √x o √variable -> sqrt(variable)
        eq = eq.replace(/√\s*([a-zA-Z0-9_]+)/g, 'sqrt($1)');
        
        // √ solo -> sqrt
        eq = eq.replace(/√/g, 'sqrt');

        // Normalizar apóstrofes (y''', y'', y') - orden descendente
        eq = eq.replace(/y'''/g, 'd^3/dx^3(y)');
        eq = eq.replace(/y''/g, 'd^2/dx^2(y)');
        eq = eq.replace(/y'/g, 'd/dx(y)');

        // d/dx y -> d/dx(y)
        eq = eq.replace(/d\/dx\s+([a-zA-Z][a-zA-Z0-9_]*)/g, 'd/dx($1)');

        // dy/dx mantener como está
        // d2y/dx2 mantener como está
        // d3y/dx3 mantener como está

        return eq;
    }

    // ─────────────────────────────────────────
    // ⚙️ Gestión de Condiciones Iniciales
    // ─────────────────────────────────────────
    const updateConditionButtons = () => {
        if (!addConditionButton || !removeConditionButton) return;
        addConditionButton.disabled = conditionCount >= 3;
        removeConditionButton.disabled = conditionCount <= 1;
    };

    if (addConditionButton) {
        addConditionButton.addEventListener('click', () => {
            if (conditionCount < 3) {
                conditionCount++;

                const conditionItem = document.createElement('div');
                conditionItem.classList.add('initial-condition-item', 'flex', 'items-center', 'gap-2');
                conditionItem.innerHTML = `
                    <input 
                        type="text" 
                        class="initial-condition-input flex-1 bg-[#1a1a1a] text-gray-300 text-sm px-3 py-2 rounded border border-[#3a3a3a] outline-none focus:border-[#4a4a4a]" 
                        placeholder="Ej: y(0)=1"
                    >
                `;

                initialConditionsContainer.appendChild(conditionItem);
                updateConditionButtons();
            }
        });
    }

    if (removeConditionButton) {
        removeConditionButton.addEventListener('click', () => {
            if (conditionCount > 1) {
                initialConditionsContainer.lastElementChild.remove();
                conditionCount--;
                updateConditionButtons();
            }
        });
    }

    updateConditionButtons();

    // ─────────────────────────────────────────
    // 🧮 Resolver ecuación (botón CALCULAR)
    // ─────────────────────────────────────────
    if (solveButton) {
        solveButton.addEventListener('click', async () => {
            const rawEquation = equationInput.value.trim();

            if (!rawEquation) {
                showToast('Por favor, ingresa una ecuación.', 'error');
                addShakeAnimation(equationInput);
                return;
            }

            const equation = normalizeEquation(rawEquation);

            solutionOutput.innerHTML = `
                <div class="flex justify-center py-8">
                    <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            `;

            hideElement(errorDisplay);
            solveButton.textContent = 'Resolviendo ecuación...';
            solveButton.disabled = true;

            const initialConditions = Array.from(
                initialConditionsContainer.querySelectorAll('.initial-condition-input')
            )
                .map(input => input.value.trim())
                .filter(value => value !== '');

            try {
                const response = await fetch('/solve_ode', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        equation: equation,
                        initial_conditions: initialConditions
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    const formatted = formatSolution(data.solution);
                    solutionOutput.innerHTML = formatted;

                    if (window.MathJax) {
                        MathJax.typesetPromise();
                    }

                    showToast('Ecuación procesada correctamente', 'success');
                } else {
                    solutionOutput.innerHTML = `
                        <div class="text-center py-8 text-gray-600">
                            <p class="text-sm">Ingresa una ecuación diferencial y presiona Calcular</p>
                        </div>
                    `;
                    showToast(data.error || 'Ocurrió un error al resolver la ecuación.', 'error');
                }
            } catch (error) {
                solutionOutput.innerHTML = `
                    <div class="text-center py-8 text-gray-600">
                        <p class="text-sm">Ingresa una ecuación diferencial y presiona Calcular</p>
                    </div>
                `;
                showToast('Error de conexión con el servidor.', 'error');
            } finally {
                hideElement(loadingIndicator);
                solveButton.textContent = 'CALCULAR';
                solveButton.disabled = false;
            }
        });
    }

    // ─────────────────────────────────────────
    // ⌨️ Teclado de la calculadora
    // ─────────────────────────────────────────
    if (calculatorButtonsContainer) {
        calculatorButtonsContainer.addEventListener('click', (event) => {
            const target = event.target.closest('.calc-btn');
            if (!target || target.classList.contains('empty')) return;

            const value = target.dataset.value;
            if (!value) return;

            const start = equationInput.selectionStart;
            const end = equationInput.selectionEnd;

            addButtonPressAnimation(target);

            if (value === 'C') {
                equationInput.value = '';
            } else if (value.endsWith('(') && value !== '(') {
                equationInput.value =
                    equationInput.value.substring(0, start) +
                    value +
                    equationInput.value.substring(end);
                equationInput.selectionStart = equationInput.selectionEnd = start + value.length;
            } else {
                equationInput.value =
                    equationInput.value.substring(0, start) +
                    value +
                    equationInput.value.substring(end);
                equationInput.selectionStart = equationInput.selectionEnd = start + value.length;
            }

            equationInput.focus();
        });
    }

    // ─────────────────────────────────────────
    // ⌨️ Restringir caracteres y Enter = calcular
    // ─────────────────────────────────────────
    if (equationInput) {
        equationInput.addEventListener('input', () => {
            hideElement(errorDisplay);
        });

        equationInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                solveButton.click();
                return;
            }

            const allowedKeys = [
                'Backspace',
                'ArrowLeft',
                'ArrowRight',
                'ArrowUp',
                'ArrowDown',
                'Delete',
                'Tab',
                'Home',
                'End'
            ];

            if (allowedKeys.includes(event.key) || event.ctrlKey || event.metaKey) {
                return;
            }

            // Expandir regex para aceptar más caracteres matemáticos
            const allowedCharsRegex = /^[a-zA-Z0-9+\-*/().,=^' √_]$/;
            if (!allowedCharsRegex.test(event.key)) {
                event.preventDefault();
            }
        });
    }

    // ─────────────────────────────────────────
    // 📄 Formateo de la solución
    // ─────────────────────────────────────────
    function formatSolution(text) {
        if (!text) return '';

        let cleaned = text;

        cleaned = cleaned.replace(
            /\*\*(Paso.*?)\*\*/g,
            "<h3 class='text-gray-300 font-bold mt-4 mb-2'>$1</h3>"
        );

        cleaned = cleaned.replace(/\*\*/g, '');
        cleaned = cleaned.replace(/\n/g, '<br>');

        cleaned = cleaned.replace(
            /\\\[([\s\S]*?)\\\]/g,
            "<div class='my-3 p-2 bg-[#1a1a1a] rounded border border-[#3a3a3a]'>\\[$1\\]</div>"
        );

        cleaned = cleaned.replace(/\\\((.*?)\\\)/g, '\\($1\\)');
        cleaned = cleaned.replace(/\\\( (.*?) \\\)/g, '\\($1\\)');

        return cleaned;
    }

    // ─────────────────────────────────────────
    // 👀 Helpers de visibilidad y animación
    // ─────────────────────────────────────────
    function showElement(element) {
        if (!element) return;
        element.classList.remove('hidden');
    }

    function hideElement(element) {
        if (!element) return;
        element.classList.add('hidden');
    }

    function addShakeAnimation(element) {
        if (!element) return;
        element.classList.add('shake');
        setTimeout(() => element.classList.remove('shake'), 400);
    }

    function addButtonPressAnimation(button) {
        if (!button) return;
        button.style.transform = 'scale(0.9)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    // ─────────────────────────────────────────
    // 📚 Modal EJEMPLOS
    // ─────────────────────────────────────────
    if (examplesBtn && examplesModal && examplesList && equationInput) {
        examplesBtn.addEventListener('click', () => {
            examplesModal.classList.remove('hidden');
        });

        if (closeExamples) {
            closeExamples.addEventListener('click', () => {
                examplesModal.classList.add('hidden');
            });
        }

        examplesModal.addEventListener('click', (e) => {
            if (e.target === examplesModal) {
                examplesModal.classList.add('hidden');
            }
        });

        examplesList.addEventListener('click', (e) => {
            const btn = e.target.closest('button[data-equation]');
            if (!btn) return;

            const eq = btn.dataset.equation;
            equationInput.value = eq;
            equationInput.focus();

            examplesModal.classList.add('hidden');
            showToast('Ejemplo aplicado a la pantalla', 'success');
        });
    }

    // ─────────────────────────────────────────
    // ❔ Modal AYUDA
    // ─────────────────────────────────────────
    if (helpBtn && helpModal) {
        helpBtn.addEventListener('click', () => {
            helpModal.classList.remove('hidden');
        });

        if (closeHelp) {
            closeHelp.addEventListener('click', () => {
                helpModal.classList.add('hidden');
            });
        }

        helpModal.addEventListener('click', (e) => {
            if (e.target === helpModal) {
                helpModal.classList.add('hidden');
            }
        });
    }

    // ─────────────────────────────────────────
    // © Modal CRÉDITOS
    // ─────────────────────────────────────────
    if (copyrightBtn && creditsModal && closeModal) {
        copyrightBtn.addEventListener('click', () => {
            creditsModal.classList.remove('hidden');
        });

        closeModal.addEventListener('click', () => {
            creditsModal.classList.add('hidden');
        });

        creditsModal.addEventListener('click', (e) => {
            if (e.target === creditsModal) {
                creditsModal.classList.add('hidden');
            }
        });
    }

    // ─────────────────────────────────────────
    // Mensaje inicial en la zona de solución
    // ─────────────────────────────────────────
    if (solutionOutput) {
        solutionOutput.innerHTML = `
            <div class="text-center py-8 text-gray-600">
                <p class="text-sm">Ingresa una ecuación diferencial y presiona Calcular</p>
            </div>
        `;
    }
});