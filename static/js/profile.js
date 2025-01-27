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
        fetch('/api/users/update', {
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
    $('#delete-button').addClass('bg-red').removeClass('bg-yellow');
    $('#delete-button').attr('onclick', 'confirmDelete()');
    setTimeout(() => {
        $('#delete-button').text('Delete Account');
        $('#delete-button').addClass('bg-yellow').removeClass('bg-red');
        $('#delete-button').attr('onclick', 'deleteAccount()');
    }, 5000);
}

function confirmDelete() {
    $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
    $('#message-content').html('Deactivating account...');
    fetch('/api/users/deactivate', {
        method: 'DELETE',
    }).then(async (response) => {
        if (response.status === 200) {
            $('#message-box').removeClass('bg-red').addClass('bg-green');
            $('#message-content').html('Account deactivated successfully! Redirecting...');
            setTimeout(() => {
                window.location.href = '/logout';
            }, 1000);
        } else {
            const data = await response.json();
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        }
    });
}
