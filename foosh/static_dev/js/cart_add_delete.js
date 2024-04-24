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

var cart_items = document.getElementsByClassName('update-cart');

for (var i = 0; i < cart_items.length; i++){
    cart_items[i].addEventListener('click', function(){
        var product_id=this.dataset.product;
        var action=this.dataset.action;

        if (user === "AnonymousUser"){
            UpdateUserCartItem(product_id, action)
        } else {
            UpdateUserCartItem(product_id, action)
        }
    })
}


function UpdateUserCartItem(product_id, action){
    var url = '/cart/update_item_in_cart/'
    console.log('update')
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'aplication/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({
            'product_id': product_id,
            'action':action,
        })
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
    })
}