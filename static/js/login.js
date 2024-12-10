$(function () {
    const phoneInput = $('#phone');
    const otpInput = $('#otp');
    phoneInput.on('input', () => {
        phoneInput.val(phoneInput.val().replace(/[^0-9]/g, ''));
        if (phoneInput.val().length > 8) phoneInput.val(phoneInput.val().slice(0, 8));
    });
    otpInput.on('input', () => {
        otpInput.val(otpInput.val().replace(/[^0-9]/g, ''));
        if (otpInput.val().length > 6) otpInput.val(otpInput.val().slice(0, 6));
    });
    phoneInput.on('keypress', (e) => {
        if (e.key == 'Enter') login();
    });
    otpInput.on('keypress', (e) => {
        if (e.key == 'Enter') verifyOTP();
    });
})

function login() {
    const phoneInput = $('#phone');
    const phone = phoneInput.val();
    if (phone.length < 8) {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').text('Please enter a valid phone number.');
    } else {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').html('Sending an OTP via WhatsApp...');
        fetch('./api/send_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                phone: phone
            })
        }).then(response => {
            if (response.status == 200) {
                $('#message-box').removeClass('hidden').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html('An OTP was sent to you via WhatsApp.<br>Please enter the code above to sign in.');
                $('#otp-div').removeClass('hidden');
                $('#login-button').text('Verify OTP');
                $('#phone').prop('disabled', true);
                $('#login-button').attr('onclick', 'verifyOTP()');
            } else {
                $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text('An error occurred while sending an OTP. Please try again.');
            }
        })
    }
}
function verifyOTP() {
    const phoneInput = $('#phone');
    const otpInput = $('#otp');
    const phone = phoneInput.val();
    const otp = otpInput.val();
    if (otp.length < 6) {
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').text('Please enter a valid OTP.');
    } else {
        fetch('./api/verify_otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                phone: phone,
                otp: otp
            })
        }).then(async response => {
            if (response.status == 200) {
                $('#message-box').removeClass('hidden').removeClass('bg-red').addClass('bg-green');
                $('#message-content').text('Logged in, redirecting...');
            } else {
                $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text('Invalid OTP. Please try again.');
            }
        });
    }
}