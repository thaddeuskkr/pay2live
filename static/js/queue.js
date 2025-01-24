$(function () {
    $('#getNumber').click(function () {
        if (!$('#get-service').val()) {
            $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
            $('#message-content').text('Please select a service.');
            return;
        }
        $('#message-box').removeClass('hidden').removeClass('bg-green').addClass('bg-red');
        $('#message-content').text('Processing...');
        fetch('/api/queue/get', {
            method: 'POST',
            body: JSON.stringify({
                service: $('#get-service').val(),
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                $('#message-box').removeClass('hidden').addClass('bg-green').removeClass('bg-red');
                $('#message-content').text(`Your queue number is ${data.number}.`);
            } else {
                alert(`Failed to get queue number: ${data.message}`);
            }
        });
    });
});
