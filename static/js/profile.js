$(function () {
    const cookies = Object.fromEntries(
        document.cookie.split(/; */).map(function (c) {
            var index = c.indexOf('='); // Find the index of the first equal sign
            var key = c.slice(0, index); // Everything upto the index is the key
            var value = c.slice(index + 1); // Everything after the index is the value

            // Return the key and value
            return [decodeURIComponent(key), decodeURIComponent(value)];
        }),
    );
    if (!cookies.session_token || cookies.session_token === 'null' || cookies.session_token.length < 5)
        window.location.href = './login';

    fetch('./api/get_user').then(async (response) => {
        if (response.status === 200) {
            const data = await response.json();
            $('#firstName').val(data.user.first_name);
            $('#lastName').val(data.user.last_name);
            $('#email').val(data.user.email);
            $('#gender').val(data.user.gender);
            $('#nric').val(data.user.nric);
            $('#address').val(data.user.address);
            $('#phone').val(data.user.phone);
        } else {
            const data = await response.json();
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        }
    });
});

function edit() {
    const fName = $('#firstName').val();
    const lName = $('#lastName').val();
    const email = $('#email').val();
    const gender = $('#gender').val();
    const nric = $('#nric').val();
    const address = $('#address').val();
    const phone = $('#phone').val();

    if (
        fName.length === 0 ||
        lName.length === 0 ||
        !email.includes('@') ||
        !gender ||
        nric.length !== 9 ||
        address.length === 0 ||
        phone.length !== 8
    ) {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').text('Please fill in all required fields.');
    } else {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').html('Applying changes...');
        fetch('./api/update_user', {
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
                phone: phone,
            }),
        }).then(async (response) => {
            console.log(response);
            if (response.status === 200) {
                $('#message-box').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html('Applied changes successfully! Reloading...');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                const data = await response.json();
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
            }
        });
    }
}

function deleteAccount() {
    $('#delete-button').text('Confirm Delete');
    $('#delete-button').attr('onclick', 'confirmDelete()');
    setTimeout(() => {
        $('#delete-button').text('Delete Account');
        $('#delete-button').attr('onclick', 'deleteAccount()');
    }, 5000);
}

function confirmDelete() {
    $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
    $('#message-content').html('Deleting account...');
    fetch('./api/delete_user', {
        method: 'DELETE',
    }).then(async (response) => {
        if (response.status === 200) {
            $('#message-box').removeClass('bg-red').addClass('bg-green');
            $('#message-content').html('Account deleted successfully! Redirecting...');
            setTimeout(() => {
                logout();
            }, 1000);
        } else {
            const data = await response.json();
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        }
    });
}
