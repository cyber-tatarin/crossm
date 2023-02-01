let inputs = document.querySelectorAll('.file-input');
Array.prototype.forEach.call(inputs, function(input) {
    input.addEventListener('change', function(e) {
        test.style.transitionProperty = 'background-color';
        test.style.transitionDuration = "0.3s";
        test.style.float = 'right';
        document.querySelector('.choose-file-button').style.backgroundColor = 'rgba(5, 0, 255, 0.4)';
        document.querySelector('.button-file').innerText = 'Загружено';
        document.querySelector('.button-file').style.color = "#ffffff";
        document.querySelector('.choose-file-button').style.border = '2px solid #000000';
        document.querySelector('.choose-file-button').style.marginRight = '-2px';
    });
});