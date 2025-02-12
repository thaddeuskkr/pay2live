$(function () {
    const urlParams = new URLSearchParams(window.location.search);
    $('#phone').val(urlParams.get('phone'));

    $('#register-form').on('submit', function (e) {
        e.preventDefault();

        const fName = $('#firstName').val();
        const lName = $('#lastName').val();
        const email = $('#email').val();
        const gender = $('#gender').val();
        const nric = $('#nric').val();
        const address1 = $('#addressLine1').val();
        const address2 = $('#addressLine2').val();
        const address3 = $('#addressLine3').val();
        const address4 = $('#postalCode').val();

        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').html('Registering...');
        fetch('/api/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: fName,
                last_name: lName,
                email: email,
                gender: gender,
                nric: nric,
                address1: address1,
                address2: address2,
                address3: address3,
                address4: address4,
            }),
        }).then(async (response) => {
            console.log(response);
            if (response.status === 200) {
                $('#message-box').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html('Your profile is complete! Redirecting...');
                setTimeout(() => {
                    window.location.href = './';
                }, 1000);
            } else {
                const data = await response.json();
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
            }
        });
    });
});
