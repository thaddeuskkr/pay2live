$(function () {
    $('#bookBtn').click(() => {
        $('#bookingPopup').removeClass('hidden').addClass('flex');
    });
    $('#cancelBtn').click(() => {
        $('#bookingPopup').addClass('hidden').removeClass('flex');
    });
    $('.deleteBtn').click((e) => {
        const dataId = $(e.currentTarget).attr('data-id');
        const confirmation = confirm('Are you sure you want to cancel this appointment? This action cannot be undone.');
        if (confirmation) {
            fetch(`/api/appointments/delete`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: dataId }),
            }).then(async (response) => {
                if (response.status == 200) {
                    alert('Appointment cancelled successfully!');
                    window.location.reload();
                } else {
                    alert('Failed to delete appointment!');
                }
            });
        }
    });
    $('#bookingForm').submit((e) => {
        e.preventDefault();
        fetch('/api/appointments/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                service: $('#service').val(),
                timestamp: new Date($('#date').val() + 'T' + $('#time').val()).valueOf(),
            }),
        }).then(async (response) => {
            if (response.status == 200) {
                alert('Appointment booked successfully!');
                $('#bookingPopup').addClass('hidden').removeClass('flex');
                window.location.reload();
            } else {
                alert('Failed to book appointment!');
            }
        });
    });
});
