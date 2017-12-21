function addProductModal() {
    let modalWin = document.getElementById('popupWin'); // находим наше "окно"
    let closeButton = document.getElementById('close-modal-adding');
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
        removeTipAfterClosing();
        return false;
    };

}
let descriptionArea = document.getElementById('descriptionArea');
let descriptionTip = document.createElement('div');
descriptionTip.className = 'description-tip';
descriptionTip.innerText = 'Введите более развёрнутое описание, чтобы его интересно было читать';


let showingDescriptionTip = false;

function productDescriptionValidate(event) {
    let target = event.target;
    let coords = target.getBoundingClientRect();

    let left = coords.left + (target.offsetWidth - descriptionTip.offsetWidth) / 2;
    if (left < 0) left = 0; // не вылезать за левую границу окна

    let top = coords.top - descriptionTip.offsetHeight - 5;
    if (top < 0) { // не вылезать за верхнюю границу окна
        top = coords.top + target.offsetHeight + 5;
    }

    descriptionTip.style.left = left + 'px';
    descriptionTip.style.top = top + 'px';

    if (descriptionArea.value.length < 15 && (showingDescriptionTip === false)) {
        document.body.appendChild(descriptionTip);
        showingDescriptionTip = true;
    } else if (descriptionArea.value.length >= 15) {
        descriptionTip.remove();
        showingDescriptionTip = false;
    }
}

function removeTipAfterClosing() {
    if (showingDescriptionTip) {
        descriptionTip.remove();
        showingDescriptionTip = false;
    }
}

function validateDescriptionAfterSubmit(event) {

    if (descriptionArea.value.length < 15 && descriptionArea.value.length > 0
        && (showingDescriptionTip === false)) {
        event.preventDefault();
        document.body.appendChild(descriptionTip);
        showingDescriptionTip = true;
    } else if (showingDescriptionTip === true) {
        event.preventDefault();
    }
}

function removeDescriptionTipOnBlur() {
    if (showingDescriptionTip) {
        descriptionTip.remove();
        showingDescriptionTip = false;
    }
}
