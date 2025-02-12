$(function () {
    $('#manageUserCancel').click(() => {
        $('#manageUserPopup').removeClass('flex').addClass('hidden');
    });
    $('.manage-user').on('click', function (e) {
        e.preventDefault();
        const id = $(e.currentTarget).attr('data-id');
        const phone = $(e.currentTarget).attr('data-phone');
        const firstName = $(e.currentTarget).attr('data-first_name');
        const lastName = $(e.currentTarget).attr('data-last_name');
        const email = $(e.currentTarget).attr('data-email');
        const gender = $(e.currentTarget).attr('data-gender');
        const nric = $(e.currentTarget).attr('data-nric');
        const role = $(e.currentTarget).attr('data-role');
        const admin = $(e.currentTarget).attr('data-admin');
        const registered = $(e.currentTarget).attr('data-registered');
        const active = $(e.currentTarget).attr('data-active');
        const address1 = $(e.currentTarget).attr('data-address1');
        const address2 = $(e.currentTarget).attr('data-address2');
        const address3 = $(e.currentTarget).attr('data-address3');
        const address4 = $(e.currentTarget).attr('data-address4');
        $('#firstName').val(firstName);
        $('#lastName').val(lastName);
        $('#email').val(email);
        $('#phone').val(phone);
        $('#gender').val(gender);
        $('#nric').val(nric);
        $('#addressLine1').val(address1);
        $('#addressLine2').val(address2);
        $('#addressLine3').val(address3);
        $('#postalCode').val(address4);
        $('#role').val(role);
        $('#admin').val(admin);
        $('#registered').val(registered);
        $('#active').val(active);
        $('#manage-user-form').attr('data-id', id);
        $('#manageUserPopup').removeClass('hidden').addClass('flex');
    });
    $('#manage-user-form').submit(function (e) {
        e.preventDefault();
        const id = $('#manage-user-form').attr('data-id');
        const firstName = $('#firstName').val();
        const lastName = $('#lastName').val();
        const email = $('#email').val();
        const phone = $('#phone').val();
        const gender = $('#gender').val();
        const nric = $('#nric').val();
        const address1 = $('#addressLine1').val();
        const address2 = $('#addressLine2').val();
        const address3 = $('#addressLine3').val();
        const address4 = $('#postalCode').val();
        const role = $('#role').val();
        const admin = $('#admin').val();
        const registered = $('#registered').val();
        const active = $('#active').val();
        fetch('/api/admin/users/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                first_name: firstName,
                last_name: lastName,
                email: email,
                phone: phone,
                gender: gender,
                nric: nric,
                address1: address1,
                address2: address2,
                address3: address3,
                address4: address4,
                role: role,
                admin: admin,
                registered: registered,
                active: active,
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('User updated successfully!');
                $('#manageUserPopup').addClass('hidden').removeClass('flex');
                window.location.reload();
            } else {
                alert(`Failed to update user: ${data.message}`);
            }
        });
    });
});
