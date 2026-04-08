document.addEventListener('DOMContentLoaded', () => {
    // 1. Надежно забираем токен прямо из HTML (он теперь всегда там есть)
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrfInput ? csrfInput.value : '';

    const cartCounter = document.getElementById('cart-counter');
    const totalPriceElement = document.getElementById('cart-total-price');

    // 2. ДЕЛЕГИРОВАНИЕ СОБЫТИЙ: Один слушатель на весь документ (никогда не задублируется)
    document.body.addEventListener('click', function(e) {
        
        // --- ЛОГИКА ДОБАВЛЕНИЯ В КОРЗИНУ ---
        if (e.target.classList.contains('add-to-cart-btn')) {
            e.preventDefault(); // Останавливаем любые стандартные действия
            const button = e.target;
            const productId = button.getAttribute('data-id');

            // Защита от двойного клика (блокируем кнопку, пока идет запрос)
            button.disabled = true;

            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    if (cartCounter) cartCounter.innerText = data.total_items;
                    
                    const originalText = button.innerText;
                    button.innerText = "✓ В корзине";
                    button.style.backgroundColor = "#27ae60";
                    
                    // Возвращаем кнопку в норму через 1 секунду
                    setTimeout(() => {
                        button.innerText = originalText;
                        button.style.backgroundColor = "";
                        button.disabled = false; 
                    }, 1000);
                }
            })
            .catch(err => {
                console.error("Ошибка добавления:", err);
                button.disabled = false; // Разблокируем при ошибке
            });
        }

        // --- ЛОГИКА УДАЛЕНИЯ ИЗ КОРЗИНЫ ---
        if (e.target.classList.contains('remove-from-cart-btn')) {
            e.preventDefault();
            const button = e.target;
            const productId = button.getAttribute('data-id');
            
            button.disabled = true;

            fetch(`/cart/remove/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    if (cartCounter) cartCounter.innerText = data.total_items;
                    if (totalPriceElement) totalPriceElement.innerText = data.total_price;
                    
                    const row = document.getElementById(`cart-row-${productId}`);
                    if (row) {
                        row.style.transition = "opacity 0.3s ease";
                        row.style.opacity = "0";
                        setTimeout(() => row.remove(), 300);
                    }
                    
                    if (data.total_items === 0) {
                        setTimeout(() => window.location.reload(), 350);
                    }
                }
            })
            .catch(err => {
                console.error("Ошибка удаления:", err);
                button.disabled = false;
            });
        }
    });
});