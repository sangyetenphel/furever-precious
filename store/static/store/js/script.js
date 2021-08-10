//Generating CSRFToken
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    // Changing the main product image when smaller image thumbnail is clicked
    document.addEventListener('click', function(event) {
        if (event.target.className == 'small-img img-thumbnail') {
            document.querySelector("#product-img").src = event.target.src;
        }
    })

    // Changing the product image variant when size is changed
    const selectSize = document.querySelector('#select-size');
    if (selectSize) {
        selectSize.onchange = function() {
            fetch('/ajax_sizes', {
                method: "POST",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    productId: document.querySelector("#productId").value,
                    size: this.value,
                })
            }).then(response => response.json())
            .then(data => {
                document.querySelector('#ajax-variants').innerHTML = data.rendered_table;
                document.querySelector('#product-price').innerHTML = document.querySelector('#item-price').value;
                const maxQty = document.querySelector('#maxQty').value;
                document.querySelector('#inventory-qty').setAttribute("max", maxQty);
            })
            .catch(err => {
                console.log(err);
            });
        }
    }

    // Confirm before user delete a review
    document.querySelectorAll('.confirm-delete').forEach(link => {
        link.onclick = function(e) {
            e.preventDefault();
            const choice = confirm(link.dataset.confirm);

            if (choice) {
                window.location.href = link.href;
            }
        }
    })
}); 






