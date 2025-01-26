$(function () {
    $('#reload').click(function () {
        window.location.href = '/queue?room=' + $('#room').val();
    });
    $('.call').click(function (e) {
        const queue_number = $(e.currentTarget).attr('data-queue_number');
        fetch('/api/queue/call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ queue: queue_number, room: $('#room').val() }),
        }).then(function (response) {
            if (response.status === 200) {
                window.location.href = '/queue?room=' + $('#room').val();
            }
        });
    });
    $('.complete').click(function (e) {
        const queue_number = $(e.currentTarget).attr('data-queue_number');
        fetch('/api/queue/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ queue: queue_number }),
        }).then(function (response) {
            if (response.status === 200) {
                window.location.href = '/queue?room=' + $('#room').val();
            }
        });
    });
});
