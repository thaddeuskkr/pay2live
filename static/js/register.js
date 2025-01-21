$(function () {
    const urlParams = new URLSearchParams(window.location.search);
    $('#phone').val(urlParams.get('phone'));
});

function register() {
    const fName = $('#firstName').val();
    const lName = $('#lastName').val();
    const email = $('#email').val();
    const gender = $('#gender').val();
    const nric = $('#nric').val();
    const address = $('#address').val();

    if (
        fName.length === 0 ||
        lName.length === 0 ||
        !email.includes('@') ||
        !gender ||
        nric.length !== 9 ||
        address.length === 0
    ) {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').text('Please fill in all required fields.');
    } else {
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
                address: address,
                role: 'patient',
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
    }
}
