$(function () {
    $('#contact-method').on('change', function () {
        var value = $(this).val();
        if (value === 'phone') {
            $('#phone-input').removeClass('hidden');
            $('#phone').attr('required', 'required');
            $('#email-input').addClass('hidden');
            $('#email').removeAttr('required');
        } else {
            $('#phone-input').addClass('hidden');
            $('#phone').removeAttr('required');
            $('#email-input').removeClass('hidden');
            $('#email').attr('required', 'required');
        }
    });
    $('#contact-form').on('submit', function (e) {
        e.preventDefault();
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').html('Creating a support ticket...');
        $('#submit-button').prop('disabled', true);
        const name = $('#name').val();
        const contactMethod = $('#contact-method').val();
        const email = $('#email').val();
        const phone = $('#phone').val();
        const subject = $('#subject').val();
        const message = $('#message').val();
        const data = {
            name: name,
            contact_method: contactMethod,
            email: email,
            phone: phone,
            subject: subject,
            message: message,
        };
        fetch('/api/tickets/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }).then(async function (response) {
            const data = await response.json();
            if (response.status === 200) {
                $('#message-box').removeClass('bg-red').addClass('bg-green');
                $('#message-content').html(
                    `Message sent successfully! Redirecting...<br>Your ticket ID is <code>${data.id}</code>.`,
                );
                setTimeout(() => {
                    window.location.href = './';
                }, 5000);
            } else {
                $('#message-box').removeClass('bg-green').addClass('bg-red');
                $('#message-content').text(data.message);
                $('#submit-button').prop('disabled', false);
            }
        });
    });
});
