document.addEventListener('DOMContentLoaded', function() {
    // Changing the main product image when smaller image thumbnail is clicked
    document.addEventListener('click', function(event) {
        if (event.target.className == 'small-img img-thumbnail') {
            document.querySelector("#product-img").src = event.target.src;
        }
    })

    // Changing the product image variant when size is changed
    document.querySelector('#select-size').onchange = function() {
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
}); 






