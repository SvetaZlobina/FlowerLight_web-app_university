function orderingModal() {
    let modalWin = document.getElementById('popupWinOrdering'); // находим наше "окно"
    let closeButton = document.getElementById('close-modal-ordering');
    let darkLayer = document.createElement('div'); // слой затемнения
    darkLayer.id = 'shadow'; // id чтобы подхватить стиль
    document.body.appendChild(darkLayer); // включаем затемнение

    modalWin.style.display = 'block'; // "включаем" его

    closeButton.onclick = function () {
        darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
        modalWin.style.display = 'none'; // делаем окно невидимым
        return false;
    };
    // closeModalAdding(darkLayer, modalWin);
    darkLayer.onclick = function () {
        darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
        modalWin.style.display = 'none'; // делаем окно невидимым
        return false;
    };
}
