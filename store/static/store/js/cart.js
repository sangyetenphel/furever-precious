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

// function getProductVariant(productId, sizeId, colorId) {
//     const url = '/get_productvariant'

//     return fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({
//             'productId': productId,
//             'sizeId': sizeId,
//             'colorId': colorId
//         })
//     })

//     .then((response) => response.json())
//     .then(data => {
//         console.log("Success:", data);
//         return data
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     })
// }

 
// Add to cart for authorized and unauthorized users
document.querySelector('#add_cart_form').addEventListener('submit', (event) => {
    const productId = document.querySelector('#productId').value
    const sizeId = event.target.elements.size.value;
    const colorId = event.target.elements.color.value;
    const quantity = document.querySelector('#inventory-qty').value 
    // const productVariantId = getProductVariant(productId, sizeId, colorId).then(function(result) {
    //     console.log(result)
    // })
    // console.log("--------" + productVariantId )
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
document.querySelectorAll('.cart-qty').forEach(qty => {
    qty.onchange = () => {
        const quantity = qty.value
        const productId = qty.dataset.product
        const productVariantId = qty.dataset.productvariant

        if (user === 'AnonymousUser') {
            console.log('hi')
        }
        else {
            updateUserOrder(quantity, productId, productVariantId)
        }
    }
})


// Add/Update cart for unauthorized users
function updateUserCookie(quantity, productId, sizeId, colorId) {
    quantity = parseInt(quantity)
    if (cart[productId] == undefined) {
        cart[productId] = [{'sizeId': sizeId, 'colorId': colorId, 'quantity': quantity}]
        // cart[productId][sizeId] = {'colorId': colorId}
        // cart[productId][sizeId][colorId] = {'quantity': quantity}
    }
    else {
        var found = false
        for (var i=0; i < cart[productId].length; i++) {
            if (cart[productId][i]['sizeId'] == sizeId && cart[productId][i]['colorId'] == colorId) {
                cart[productId][i]['quantity'] += 1
                found = true
            }
        }
        if (found == false) {
            cart[productId].push({'sizeId': sizeId, 'colorId': colorId, 'quantity': quantity})
        }

        // if (cart[productId]['sizeId'] == sizeId && cart[productId][sizeId]['colorId'] == colorId) {
        //     console.log('hi')
        //     cart[productId][sizeId][colorId]['quantity'] += quantity
        // } else if (cart[productId]['sizeId'] == sizeId) {
        //     console.log('bye')
        //     cart[productId][sizeId] = {'colorId': colorId}
        //     cart[productId][sizeId][colorId] = {'quantity': quantity}
        // } else {    
        //     console.log('hasdkhadshuk')
        //     cart[productId][sizeId] = {'colorId': colorId}
        //     cart[productId][sizeId][colorId] = {'quantity': quantity}
        // }
    }
    setCookie("cart", cart)
    console.log('Cart:', cart)
}


// Add/Update cart for authorized users
function updateUserOrder(quantity, productId, sizeId, colorId) {
    const url = '/cart'

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