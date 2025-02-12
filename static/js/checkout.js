$(function () {
    $('#payment-form').on('submit', function (e) {
        e.preventDefault();
        const firstName = $('#firstName').val();
        const lastName = $('#lastName').val();
        const email = $('#email').val();
        const phone = $('#phone').val();
        const address1 = $('#addressLine1').val();
        const address2 = $('#addressLine2').val();
        const address3 = $('#addressLine3').val();
        const address4 = $('#postalCode').val();
        const nameOnCard = $('#nameOnCard').val();
        const cardNumber = $('#cardNumber').val();
        const cardExpiry = $('#cardExpiry').val();
        const cardCVV = $('#cardCVV').val();

        const orderId = window.location.pathname.split('/').pop();
        const data = {
            order: orderId,
            firstName: firstName,
            lastName: lastName,
            email: email,
            phone: phone,
            address1: address1,
            address2: address2,
            address3: address3,
            address4: address4,
            nameOnCard: nameOnCard,
            cardNumber: cardNumber,
            cardExpiry: cardExpiry,
            cardCVV: cardCVV,
        };

        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').html('Processing payment...');
        fetch('/api/cart/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        }).then(async (res) => {
            const data = await res.json();
            if (res.status == 200) {
                $('#message-box').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html('Payment complete! Redirecting...');
                setTimeout(() => {
                    window.location.href = `/checkout/${data.order_id}/complete`;
                }, 1000);
            } else {
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
            }
        });
    });
});
