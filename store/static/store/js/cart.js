// Update the item quantites in cart
document.querySelectorAll('.cart-qty').forEach(qty => {
    qty.onchange = () => {
        const quantity = qty.value
        const productId = qty.dataset.product
        const productVariantId = qty.dataset.productvariant

        if (user === 'AnonymousUser') {

        }
        else {
            updateUserOrder(quantity, productId, productVariantId)
        }
    }
})

function updateUserOrder(quantity, productId, productVariantId) {
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
            'productVariantId': productVariantId
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