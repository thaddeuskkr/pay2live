$(function () {
    $('#edit-form').on('submit', (e) => {
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
        const phone = $('#phone').val();

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
                address1: address1,
                address2: address2,
                address3: address3,
                address4: address4,
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
    });
});

function deleteAccount() {
    $('#delete-button').text('Confirm Deactivation');
    $('#delete-button').addClass('bg-red').removeClass('bg-peach');
    $('#delete-button').attr('onclick', 'confirmDelete()');
    setTimeout(() => {
        $('#delete-button').text('Deactivate Account');
        $('#delete-button').addClass('bg-peach').removeClass('bg-red');
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
                window.location.href = '/logout?reset_token=1';
            }, 1000);
        } else {
            const data = await response.json();
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        }
    });
}
