window.nextProductsPage = 2;

function makeEndlessScrolling(next_page_number) {
    next_page_number = window.nextProductsPage;
    console.log('on click - page: ', next_page_number);

    let productsContainer = document.getElementById('products-container');

    let url = '/api/products/?format=json&page=' + next_page_number;
    let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    fetch(url, {
        method: 'GET',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': "text/html;charset=utf-8"
        },
        credentials: 'include'
    })
        .then(function (response) {
            if (response.status === 200) {
                response.json().then(function (data) {
                    let newProducts = data['results'];
                    let newRow = document.createElement('div');
                    newRow.className = "row";

                    newProducts.forEach(function (nextProduct, i) {
                        let elemDiv = document.createElement('div');
                        elemDiv.className = "col-md-4 infinite-item";
                        elemDiv.style = "margin-top: 3%";

                        let img = document.createElement('img');
                        img.className = "rounded-circle";
                        img.src = nextProduct['image'];
                        img.alt = "Generic placeholder image";
                        img.width = '140';
                        img.height = '140';

                        let header = document.createElement('h2');
                        let anchor = document.createElement('a');
                        anchor.style = "color: inherit";
                        anchor.href = "/products/" + nextProduct['id'];
                        anchor.innerText = nextProduct['name'];

                        let description = document.createElement('p');
                        description.style = "height: 25%; overflow: hidden;";
                        description.innerText = nextProduct['description'];

                        let buttonMore = document.createElement('p');
                        let buttonMoreAnchor = document.createElement('a');
                        buttonMoreAnchor.className = "btn btn-secondary";
                        buttonMoreAnchor.href = "/products/" + nextProduct['id'];
                        buttonMoreAnchor.setAttribute('role', 'button');
                        buttonMoreAnchor.innerText = 'Подробнее';


                        header.appendChild(anchor);
                        buttonMore.appendChild(buttonMoreAnchor);
                        elemDiv.appendChild(img);
                        elemDiv.appendChild(header);
                        elemDiv.appendChild(description);
                        elemDiv.appendChild(buttonMore);

                        newRow.appendChild(elemDiv);
                        productsContainer.appendChild(newRow);
                    });

                    let productsCountAll = data['count'];
                    if (productsCountAll <= window.nextProductsPage * 6) {
                        console.log('зашли в удаление кнопки');
                        console.log(window.nextProductsPage);
                        let loadingButton = document.getElementById('button-more-loading');
                        loadingButton.remove();
                    }
                    console.log(productsCountAll);
                    window.nextProductsPage += 1;
                });
            }
            else {
                console.log('not 200 response');
                window.nextProductsPage = 2;
                let loadingButton = document.getElementById('button-more-loading');
                loadingButton.remove();
            }
        });
}

function changePageNumber(nextPageNumber) {
    console.log('on mouse down - page: ', nextPageNumber);
    if (nextPageNumber !== 2) {

        let loadingButton = document.getElementById('button-more-loading');
        loadingButton.removeAttribute('onclick');
        loadingButton.addEventListener('onclick', makeEndlessScrolling(nextPageNumber));

        console.log('onclick event was changed');
    }

}