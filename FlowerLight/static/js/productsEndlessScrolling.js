function makeEndlessScrolling(next_page_number) {
    let productsContainer = document.getElementById('products-container');

    let url = '/api/products/?format=json&page=' + next_page_number;
    let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    console.log(url);
    fetch(url, {
        method: 'GET',
        // body: 'csrfmiddlewaretoken=' + csrftoken +
        // '&amount=' + amount +
        // '&delivery_date=' + delivery_year + '-' + delivery_month + '-' + delivery_day,
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': "text/html;charset=utf-8"
        },
        credentials: 'include'
    })
        .then(function (response) {
            if (response.status === 200) {
                response.json().then(function (data) {
                    console.log(data);
                    let nextElem = data['results'][0];

                    let elemDiv = document.createElement('div');
                    elemDiv.className = "col-md-4 infinite-item";

                    let img = document.createElement('img');
                    img.className = "rounded-circle";
                    img.src = nextElem['image'];
                    img.alt = "Generic placeholder image";
                    img.width = '140';
                    img.height = '140';
                    elemDiv.appendChild(img);

                    let header = document.createElement('h2');
                    let anchor = document.createElement('a');
                    anchor.style = "color: inherit";
                    anchor.href = "{% url 'product_page' " + nextElem['id'] + " %}";
                    anchor.innerText = nextElem['name'];
                    header.appendChild(anchor);
                    elemDiv.appendChild(header);



                    let newRow = document.createElement('row');
                    newRow.style = "margin-top: 100%";
                    newRow.appendChild(elemDiv);
                    productsContainer.appendChild(newRow);
                });
            }
        });
    // $.ajax({
    //      type: 'GET',
    //      url: '{% url '/products/' %}', //Ссылка на вьюху
    //      dataType: "json",
    //      data: {'value': 10},  //Здесь можно передать данные в GET запросе, например сколько значений получить
    //      success: function(data) {
    //          // Ответ приходит в переменную data. Её и рендерим на страницу
    //      }
    //  });
}