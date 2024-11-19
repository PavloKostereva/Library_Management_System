document.getElementById('sendMessageButton').addEventListener('click', function() {
    // Показуємо повідомлення про успіх
    var responseMessage = document.getElementById('responseMessage');
    responseMessage.style.display = 'block';  // Показуємо елемент
    responseMessage.innerText = 'Your message has been sent!';  // Текст повідомлення

    // Затримка, після якої повідомлення зникне через 1 секунду
    setTimeout(function() {
        responseMessage.style.display = 'none';  // Сховуємо повідомлення
    }, 1000);  // 1000 мілісекунд = 1 секунда
});
