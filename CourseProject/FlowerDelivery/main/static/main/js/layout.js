
document.addEventListener('DOMContentLoaded', function () {
    //
    // Загрузка картинки на форме add_product.html
    //
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imageWidthField = document.querySelector('input[name="image_width"]');
    const imageHeightField = document.querySelector('input[name="image_height"]');

    if (imageInput) {
        imageInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();

                // Отображение превью
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';

                    // Получение размеров изображения
                    const img = new Image();
                    img.src = e.target.result;
                    img.onload = function () {
                        const width = img.width;
                        const height = img.height;

                        // Заполнение полей ширины и высоты
                        imageWidthField.value = width;
                        imageHeightField.value = height;
                    };
                };

                reader.readAsDataURL(file);
            } else {
                // Если файл не выбран, скрыть превью и очистить поля
                imagePreview.src = '#';
                imagePreview.style.display = 'none';
                imageWidthField.value = '';
                imageHeightField.value = '';
            }
        });
    }
});

