document.addEventListener("DOMContentLoaded", function() {
    // Пример скрипта для добавления подтверждения перед удалением элемента
    const deleteLinks = document.querySelectorAll("a[href*=delete]");
    deleteLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            if (!confirm("Вы уверены, что хотите удалить этот элемент?")) {
                event.preventDefault(); // Отменяет переход по ссылке
            }
        });
    });

    // Пример динамического изменения данных с помощью AJAX (если есть необходимость)
    const createAssignmentForm = document.getElementById('assignment-form');
    if (createAssignmentForm) {
        createAssignmentForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Отменяет стандартную отправку формы

            // Получаем данные формы
            const formData = new FormData(createAssignmentForm);
            fetch('/assignments/' + createAssignmentForm.dataset.courseId, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Обновляем страницу или добавляем данные на страницу
                alert("Задание создано!");
                window.location.reload(); // Перезагружаем страницу после успешного создания задания
            })
            .catch(error => console.error('Ошибка:', error));
        });
    }
});
