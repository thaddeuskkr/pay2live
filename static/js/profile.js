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
        const otp = $('#otp').val();

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
                otp: otp,
            }),
        }).then(async (response) => {
            if (response.status === 200) {
                $('#message-box').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html('Applied changes successfully! Reloading...');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else if (response.status === 418) {
                const data = await response.json();
                $('#otp-div').removeClass('hidden').attr('required', 'required');
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
            } else {
                const data = await response.json();
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
            }
        });
    });
});

function deleteAccount() {
    const otp = $('#otp').val();
    $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
    $('#message-content').html('Deactivating account...');
    fetch('/api/users/deactivate', {
        method: 'POST',
        body: JSON.stringify({
            otp: otp,
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(async (response) => {
        if (response.status === 200) {
            $('#message-box').removeClass('bg-red').addClass('bg-green');
            $('#message-content').html('Account deactivated successfully! Redirecting...');
            setTimeout(() => {
                window.location.href = '/logout?reset_token=1';
            }, 1000);
        } else if (response.status === 418) {
            const data = await response.json();
            $('#otp-div').removeClass('hidden').attr('required', 'required');
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        } else {
            const data = await response.json();
            $('#message-box').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text(data.message);
        }
    });
}

function logoutAllDevices() {
    $('#logout-all-devices-button').text('Confirm Logout of All Devices');
    $('#logout-all-devices-button').addClass('bg-red').removeClass('bg-lavender');
    $('#logout-all-devices-button').attr('onclick', 'confirmLogoutAllDevices()');
    setTimeout(() => {
        $('#logout-all-devices-button').text('Logout All Devices');
        $('#logout-all-devices-button').addClass('bg-lavender').removeClass('bg-red');
        $('#logout-all-devices-button').attr('onclick', 'logoutAllDevices()');
    }, 5000);
}

function confirmLogoutAllDevices() {
    $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
    $('#message-content').html('Logging out of all devices...');
    setTimeout(() => {
        window.location.href = '/logout?reset_token=1';
    }, 1000);
}
