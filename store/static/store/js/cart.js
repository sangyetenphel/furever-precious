function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + JSON.stringify(cvalue) + ";"  + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function checkCookie() {
    let cart = getCookie("cart");
    if (cart == "") {
        cart = {}
        console.log("Cart was created!")
        setCookie("cart", cart);
    }
    return JSON.parse(cart)
}

let cart = checkCookie();
console.log("Cart:", cart)

document.addEventListener('DOMContentLoaded', function() {
    // Event listener for when a Product is added to cart
    document.querySelector('#add_cart_form').addEventListener('submit', (event) => {
        console.log('add cart form clicked')
        const productId = document.querySelector('#productId').value
        const sizeId = event.target.elements.size.value;
        const colorId = event.target.elements.color.value;
        const quantity = document.querySelector('#inventory-qty').value 
    
        // Handle cart if user is unauthenticated or not
        if (user === 'AnonymousUser') {
            updateUserCookie(quantity, productId, sizeId, colorId)
        }
        else {
            updateUserOrder(quantity, productId, sizeId, colorId)
        }
        event.preventDefault();
    });
})


// Update the item quantites in cart for unauthorized users
function updateUserCookie(quantity=1, productId, sizeId, colorId, action='add') {
    quantity = parseInt(quantity)
    if (cart[productId] == undefined) {
        cart[productId] = [{'sizeId': sizeId, 'colorId': colorId, 'quantity': quantity}]
    }
    else {
        var found = false
        for (var i=0; i < cart[productId].length; i++) {
            if (cart[productId][i]['sizeId'] == sizeId && cart[productId][i]['colorId'] == colorId) {
                if (action == 'subtract') {
                    cart[productId][i]['quantity'] -= quantity
                    // delete the item if quantity is 0 
                    if (cart[productId][i]['quantity'] == 0) {
                        delete cart[productId][i];
                        // Filtering out all null elements in the array since delete will replace item array with null
                        var filteredCart = cart[productId].filter((item) => {
                            return item != null
                        })
                        cart[productId] = filteredCart
                    }
                } else {
                    cart[productId][i]['quantity'] += quantity
                }
                found = true
            }
        }
        // The product is in the cart but not the product variant, so append the new dic to the list 
        if (found == false) {
            cart[productId].push({'sizeId': sizeId, 'colorId': colorId, 'quantity': quantity})
        }
    }
    setCookie("cart", cart)
    location.reload();
    console.log('Cart:', cart)
}


// Add/Update cart for authorized users
function updateUserOrder(quantity=1, productId, sizeId, colorId, action='add') {
    // console.log('Update user items')
    const url = '/add_cart'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'quantity': quantity,
            'productId': productId,
            'sizeId': sizeId,
            'colorId': colorId,
            'action': action
        })
    })

    .then((response) => response.json())
    .then(data => {
        console.log("Success:", data);
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    })
}


// When user updates item quantites through the cart
document.querySelectorAll('.plus-minus-button').forEach(button => {
    button.onclick = () => {
        const productId = button.dataset.product
        const sizeId = button.dataset.size
        const colorId = button.dataset.color
        let action = ''

        if (button.classList.contains('fa-plus')) {
            action = 'add';
        } else if (button.classList.contains('fa-minus')) {
            action = 'subtract';
        }

        if (user == 'AnonymousUser') {
            updateUserCookie(quantity=1, productId, sizeId, colorId, action)
        }
        else {
            updateUserOrder(quantity=1, productId, sizeId, colorId, action)
        }
    }
});

    