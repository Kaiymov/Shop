var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var quantityElement = document.querySelector('[name="quantity"]');

        if (quantityElement != null) {
            quantityInt = parseInt(quantityElement.value);
            if (quantityInt >= 1) {
                quantity = quantityInt
            }
        }
        else {
            quantity = 1;
        }

        if (user == 'AnonymousUser'){
            addCookieItem(productId, action, quantity)
        }else{
            console.log('productId:', productId, 'action:', action, 'quantity:', quantity);
            console.log('USER:', user);
            updateUserOrder(productId, action, quantity)
        }
    });
}

function addCookieItem(productId, action, quantity) {
    console.log('User is not authenticated')
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': quantity}
        }
    }
    if(action == 'remove'){
        delete cart[productId]
    }

    window.location.reload()
    console.log('Cart', cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
}

function updateUserOrder(productId, action, quantity) {
    console.log('User is logged in, sending data...')

    var url = '/order/update_item/';
    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action, 'quantity': quantity})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload()
    });
}

