document.addEventListener('DOMContentLoaded', function() {
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
    const csrftoken = getCookie('csrftoken');

    // Changing the main product image when smaller image thumbnail is clicked
    document.querySelectorAll('.small-img').forEach(img => {
        img.onclick = function() {
            document.querySelector("#product-img").src = img.src;
        }
    })

    // document.querySelectorAll('.radio-color').forEach(color => {
    //     color.addEventListener('change', function() {
    //         // location.reload();
    //     })
    // })

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
            document.querySelector('#ajax-color-variants').innerHTML = data.rendered_table;
        })
        .catch(err => {
            console.log(err);
        });
    }
}); 






