/**
 * Custom JavaScript для проекта ООО «Мостоотряд-69»
 * Автоматизация сдачи-приёмки строительных работ
 */

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle functionality
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
        });
    }

    // Автозаполнение полей при выборе вида работ
    const workTypeSelects = document.querySelectorAll('.work-type-select');
    workTypeSelects.forEach(select => {
        select.addEventListener('change', function() {
            const row = this.closest('.work-item') || this.closest('tr');
            if (row) {
                // Здесь можно добавить логику автозаполнения из справочника
                console.log('Выбран вид работ:', this.value);
            }
        });
    });

    // Подсветка обязательных полей
    const requiredInputs = document.querySelectorAll('[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Форматирование чисел в полях ввода
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.select();
        });
    });
});

/**
 * Функция добавления новой строки работ в форму создания акта
 */
function addWorkItem() {
    const container = document.getElementById('workItemsContainer');
    if (!container) return;
    
    const totalForms = document.getElementById('id_items-TOTAL_FORMS');
    if (!totalForms) return;
    
    const newIndex = parseInt(totalForms.value);
    
    const newRow = document.createElement('div');
    newRow.className = 'work-item row mb-3 border-bottom pb-3';
    newRow.innerHTML = `
        <div class="col-md-1">
            <label class="form-label">№</label>
            <input type="number" name="items-${newIndex}-number" class="form-control" min="1" value="${newIndex + 1}">
        </div>
        <div class="col-md-3">
            <label class="form-label">Наименование работ *</label>
            <input type="text" name="items-${newIndex}-name" class="form-control work-name" required>
        </div>
        <div class="col-md-2">
            <label class="form-label">Ед. изм.</label>
            <input type="text" name="items-${newIndex}-unit" class="form-control work-unit" value="м3">
        </div>
        <div class="col-md-2">
            <label class="form-label">Количество *</label>
            <input type="number" name="items-${newIndex}-quantity" class="form-control work-quantity" step="0.0001" required>
        </div>
        <div class="col-md-2">
            <label class="form-label">Цена за ед. *</label>
            <input type="number" name="items-${newIndex}-price" class="form-control work-price" step="0.01" required>
        </div>
        <div class="col-md-2">
            <label class="form-label">Действия</label>
            <button type="button" class="btn btn-danger btn-sm" onclick="removeWorkItem(this)">
                <i class="bi bi-trash"></i>
            </button>
            <input type="checkbox" name="items-${newIndex}-DELETE" id="id_items-${newIndex}-DELETE" style="display:none;">
        </div>
        <input type="hidden" name="items-${newIndex}-work_type" class="work-type-select">
        <input type="hidden" name="items-${newIndex}-notes" class="form-control">
    `;
    
    container.appendChild(newRow);
    totalForms.value = newIndex + 1;
}

/**
 * Функция удаления строки работ из формы
 * @param {HTMLElement} button - кнопка удаления
 */
function removeWorkItem(button) {
    const row = button.closest('.work-item');
    if (!row) return;
    
    const deleteCheckbox = row.querySelector('input[type="checkbox"][name*="DELETE"]');
    if (deleteCheckbox) {
        // Если это форма Django formset, помечаем на удаление
        deleteCheckbox.checked = true;
        row.style.display = 'none';
    } else {
        // Иначе просто удаляем элемент
        row.remove();
    }
}

/**
 * Валидация формы перед отправкой
 * @returns {boolean} - результат валидации
 */
function validateActForm() {
    const form = document.getElementById('actForm');
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        alert('Пожалуйста, заполните все обязательные поля!');
    }
    
    return isValid;
}

/**
 * Форматирование числа с разделителями тысяч
 * @param {number|string} num - число для форматирования
 * @returns {string} - отформатированное число
 */
function formatNumber(num) {
    if (!num) return '0';
    return Number(num).toLocaleString('ru-RU', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Расчёт итоговой суммы по строкам
 */
function calculateTotal() {
    const rows = document.querySelectorAll('.work-item');
    let total = 0;
    
    rows.forEach(row => {
        const quantityInput = row.querySelector('.work-quantity');
        const priceInput = row.querySelector('.work-price');
        
        if (quantityInput && priceInput) {
            const quantity = parseFloat(quantityInput.value) || 0;
            const price = parseFloat(priceInput.value) || 0;
            total += quantity * price;
        }
    });
    
    return total;
}

// Экспорт функций в глобальную область видимости
window.addWorkItem = addWorkItem;
window.removeWorkItem = removeWorkItem;
window.validateActForm = validateActForm;
window.formatNumber = formatNumber;
window.calculateTotal = calculateTotal;
