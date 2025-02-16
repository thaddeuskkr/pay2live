const DateTime = luxon.DateTime;

$(function () {
    $('#bookBtn').on('click', () => {
        $('#bookingPopup').removeClass('hidden').addClass('flex');
    });
    $('#cancelBtn').on('click', () => {
        $('#bookingPopup').addClass('hidden').removeClass('flex');
    });
    $('.claimBtn').on('click', (e) => {
        const dataId = $(e.currentTarget).attr('data-id');
        fetch(`/api/appointments/claim`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: dataId }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Appointment claimed successfully!');
                window.location.reload();
            } else {
                alert(`Failed to claim appointment: ${data.message}`);
            }
        });
    });
    $('.deleteBtn').on('click', (e) => {
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
                const data = await response.json();
                if (response.status == 200) {
                    alert('Appointment cancelled successfully!');
                    window.location.reload();
                } else {
                    alert(`Failed to cancel appointment: ${data.message}`);
                }
            });
        }
    });
    $('.editBtn').on('click', (e) => {
        const dataId = $(e.currentTarget).attr('data-id');
        const dataTimestamp = $(e.currentTarget).attr('data-timestamp');
        const dataDate = DateTime.fromMillis(parseInt(dataTimestamp)).toISODate();
        const dataTime = DateTime.fromMillis(parseInt(dataTimestamp)).toISOTime().slice(0, 5);
        $('#selected-service')
            .text($(e.currentTarget).attr('data-service-text'))
            .attr('value', $(e.currentTarget).attr('data-service'));
        $('#editService').attr('disabled', 'disabled');
        $('#editDate').val(dataDate);
        $('#editTime').val(dataTime);
        $('#e-patient-id').val($(e.currentTarget).attr('data-patient'));
        $('#e-doctor-id').val($(e.currentTarget).attr('data-doctor'));
        $('#editPopup').removeClass('hidden').addClass('flex');
        $('#editPopup').append(`<input type="hidden" name="id" value="${escapeHtml(dataId)}">`);
    });
    $('#cancelEditBtn').on('click', () => {
        $('#editPopup').addClass('hidden').removeClass('flex');
    });
    $('#editForm').on('submit', (e) => {
        e.preventDefault();
        const datetime = DateTime.fromISO($('#editDate').val() + 'T' + $('#editTime').val(), {
            zone: 'Asia/Singapore',
        });
        fetch('/api/appointments/edit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: $('#editPopup input[name="id"]').val(),
                timestamp: datetime.toMillis(),
                doctor: $('#e-doctor-id').val(),
                patient: $('#e-patient-id').val(),
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Appointment updated successfully!');
                $('#editPopup').addClass('hidden').removeClass('flex');
                $('#editForm input').val('');
                window.location.reload();
            } else {
                alert(`Failed to update appointment: ${data.message}`);
            }
        });
    });
    $('#bookingForm').on('submit', (e) => {
        e.preventDefault();
        const datetime = DateTime.fromISO($('#date').val() + 'T' + $('#time').val(), { zone: 'Asia/Singapore' });
        fetch('/api/appointments/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                patient: $('#patient-id').val(),
                service: $('#service').val(),
                timestamp: datetime.toMillis(),
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Appointment booked successfully!');
                $('#bookingPopup').addClass('hidden').removeClass('flex');
                $('#bookingForm input').val('');
                window.location.reload();
            } else {
                alert(`Failed to book appointment: ${data.message}`);
            }
        });
    });
});

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
