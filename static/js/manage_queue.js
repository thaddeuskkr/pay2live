$(function () {
    $('#reload').on('click', function () {
        window.location.href = '/queue?room=' + encodeURIComponent($('#room').val());
    });
    $('.call').on('click', function (e) {
        if ($('#room').val() === '') {
            alert('Please enter a room before calling a queue number.');
            return;
        }
        const queue_number = $(e.currentTarget).attr('data-queue_number');
        fetch('/api/queue/call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ queue: queue_number, room: $('#room').val() }),
        }).then(function (response) {
            if (response.status === 200) {
                window.location.href = '/queue?room=' + encodeURIComponent($('#room').val());
            }
        });
    });
    $('.complete').on('click', function (e) {
        const queue_number = $(e.currentTarget).attr('data-queue_number');
        fetch('/api/queue/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ queue: queue_number }),
        }).then(function (response) {
            if (response.status === 200) {
                window.location.href = '/queue?room=' + encodeURIComponent($('#room').val());
            }
        });
    });
    $('.delete').on('click', function (e) {
        const queue_number = $(e.currentTarget).attr('data-queue_number');
        if (confirm('Are you sure you want to delete this queue number?')) {
            fetch('/api/queue/delete', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ queue: queue_number }),
            }).then(function (response) {
                if (response.status === 200) {
                    window.location.href = '/queue?room=' + encodeURIComponent($('#room').val());
                }
            });
        }
    });
});
