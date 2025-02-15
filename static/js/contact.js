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
});
