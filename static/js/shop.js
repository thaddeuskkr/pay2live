function addToCart(itemId) {
    fetch('/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item: itemId, quantity: 1 }),
    }).then(async (res) => {
        const data = await res.json();
        if (res.status == 200) {
            window.location.reload();
        } else {
            alert(data.message);
        }
    });
}

function removeFromCart(itemId) {
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item: itemId, quantity: 1 }),
    }).then(async (res) => {
        const data = await res.json();
        if (res.status == 200) {
            window.location.reload();
        } else {
            alert(data.message);
        }
    });
}
