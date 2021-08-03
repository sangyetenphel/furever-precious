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

 
// Add to cart for authorized and unauthorized users
document.querySelector('#add_cart_form').addEventListener('submit', (event) => {
    const productId = document.querySelector('#productId').value
    const sizeId = event.target.elements.size.value;
    const colorId = event.target.elements.color.value;
    const quantity = document.querySelector('#inventory-qty').value 

    if (user === 'AnonymousUser') {
        // Handle cart for unauthenticated user
        updateUserCookie(quantity, productId, sizeId, colorId)
    }
    else {
        updateUserOrder(quantity, productId, sizeId, colorId)
    }
    event.preventDefault();
})




// Update the item quantites in cart
// document.querySelectorAll('.cart-qty').forEach(qty => {
//     qty.onchange = () => {
//         const quantity = qty.value
//         const productId = qty.dataset.product
//         const sizeId = qty.dataset.size
//         const colorId = qty.dataset.color

//         if (user == 'AnonymousUser') {
//             updateUserCookie(quantity, productId, sizeId, colorId)
//         }
//         else {
//             updateUserOrder(quantity, productId, sizeId, colorId)
//         }
//     }
// })


// Update item quantities
var plusMinus = document.querySelector('.plus-minus')
plusMinus.addEventListener('click', function(e) {
    const productId = e.currentTarget.dataset.productId
    const sizeId = e.currentTarget.dataset.sizeId
    const colorId = e.currentTarget.dataset.colorId
    var action = ''

    if (e.target.classList.contains('add') || e.target.classList.contains('fa-plus')) {
        action = 'add';
    } else if (e.target.classList.contains('subtract') || e.target.classList.contains('fa-minus')) {
        action = 'subtract';
    }

    if (user == 'AnonymousUser') {
        updateUserCookie(quantity, productId, sizeId, colorId, action)
    }
    else {
        updateUserOrder(quantity, productId, sizeId, colorId, action)
    }
})



// Add/Update cart for unauthorized users
function updateUserCookie(quantity=1, productId, sizeId, colorId, action) {
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
                } else {
                    cart[productId][i]['quantity'] += quantity
                }
                found = true
            }
        }
        if (found == false) {
            cart[productId].push({'sizeId': sizeId, 'colorId': colorId, 'quantity': quantity})
        }
    }
    setCookie("cart", cart)
    console.log('Cart:', cart)
}


// Add/Update cart for authorized users
function updateUserOrder(quantity=1, productId, sizeId, colorId) {
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
            'colorId': colorId
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