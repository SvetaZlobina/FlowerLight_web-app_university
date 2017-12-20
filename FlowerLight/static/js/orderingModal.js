'use strict';

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
    darkLayer.onclick = function () {
        darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
        modalWin.style.display = 'none'; // делаем окно невидимым
        return false;
    };
}

function addOrderByPromise(e, product_id) {
    e.preventDefault();
    let closeButton = document.getElementById('close-modal-ordering');

    let url = '/order_adding/' + product_id.toString();

    let amount = $('input#form-amount-id').val();
    let delivery_year = $('select#id_delivery_date_year').val();
    let delivery_month = $('select#id_delivery_date_month').val();
    let delivery_day = $('select#id_delivery_date_day').val();

    let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    console.log(csrftoken);
    fetch(url, {
        method: 'POST',
        body: 'csrfmiddlewaretoken=' + csrftoken +
        '&amount=' + amount +
        '&delivery_date=' + delivery_year + '-' + delivery_month + '-' + delivery_day,
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': "application/x-www-form-urlencoded;charset=utf-8"
        },
        credentials: 'include'
    }).then(function (response) {
        if (response.status === 200) {
            closeButton.click();
            alert('Ваш заказ принят! Благодарим за использование услуг нашего магазина');
        }
        else {
            alert('Что-то пошло не так. ' +
                'Попробуйте обновить страницу и повторить оформление заказа');
        }
    });
}