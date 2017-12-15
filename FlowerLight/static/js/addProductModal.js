function addProductModal() {
    let modalWin = document.getElementById('popupWin'); // находим наше "окно"
    // modalWin.style.display.print;
    // if (modalWin.style.display === 'none') {
        let darkLayer = document.createElement('div'); // слой затемнения
        darkLayer.id = 'shadow'; // id чтобы подхватить стиль
        document.body.appendChild(darkLayer); // включаем затемнение

        modalWin.style.display = 'block'; // "включаем" его

        darkLayer.onclick = function () {  // при клике на слой затемнения все исчезнет
            darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
            modalWin.style.display = 'none'; // делаем окно невидимым
            return false;
        };
    // }

}