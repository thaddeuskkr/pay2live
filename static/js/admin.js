$(function () {
    $('#manageUserCancel').on('click', function () {
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
    $('#manage-user-form').on('submit', function (e) {
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
                $('#manage-user-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to update user: ${data.message}`);
            }
        });
    });
    $('#deleteUser').on('click', function () {
        if (!confirm('Are you sure you want to delete this user?')) return;
        const id = $('#manage-user-form').attr('data-id');
        fetch('/api/admin/users/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('User deleted successfully!');
                $('#manageUserPopup').addClass('hidden').removeClass('flex');
                window.location.reload();
            } else {
                alert(`Failed to delete user: ${data.message}`);
            }
        });
    });
    $('#newUserCancel').on('click', function () {
        $('#newUserPopup').removeClass('flex').addClass('hidden');
    });
    $('#new-user-form').on('submit', function (e) {
        e.preventDefault();
        const firstName = $('#newFirstName').val();
        const lastName = $('#newLastName').val();
        const email = $('#newEmail').val();
        const phone = $('#newPhone').val();
        const gender = $('#newGender').val();
        const nric = $('#newNric').val();
        const address1 = $('#newAddressLine1').val();
        const address2 = $('#newAddressLine2').val();
        const address3 = $('#newAddressLine3').val();
        const address4 = $('#newPostalCode').val();
        const role = $('#newRole').val();
        const admin = $('#newAdmin').val();
        const registered = $('#newRegistered').val();
        const active = $('#newActive').val();
        fetch('/api/admin/users/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
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
                alert('User added successfully!');
                $('#newUserPopup').addClass('hidden').removeClass('flex');
                $('#new-user-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to add user: ${data.message}`);
            }
        });
    });
    $('#new-user').on('click', function () {
        $('#newUserPopup').removeClass('hidden').addClass('flex');
    });
    $('#modifyItemCancel').on('click', function () {
        $('#modifyItemPopup').removeClass('flex').addClass('hidden');
    });
    $('.modify-item').on('click', function (e) {
        e.preventDefault();
        const id = $(e.currentTarget).attr('data-id');
        const name = $(e.currentTarget).attr('data-name');
        const price = $(e.currentTarget).attr('data-price');
        const image = $(e.currentTarget).attr('data-image');
        const visible = $(e.currentTarget).attr('data-visible');
        $('#itemName').val(name);
        $('#itemPrice').val(price);
        $('#itemImage').val(image);
        $('#itemVisible').val(visible);
        $('#modify-item-form').attr('data-id', id);
        $('#modifyItemPopup').removeClass('hidden').addClass('flex');
    });
    $('#modify-item-form').on('submit', function (e) {
        e.preventDefault();
        const id = $('#modify-item-form').attr('data-id');
        const name = $('#itemName').val();
        const price = $('#itemPrice').val();
        const image = $('#itemImage').val();
        const visible = $('#itemVisible').val();
        fetch('/api/admin/shop/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                name: name,
                price: price,
                image: image,
                visible: visible,
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Item updated successfully!');
                $('#modifyItemPopup').addClass('hidden').removeClass('flex');
                $('#modify-item-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to update item: ${data.message}`);
            }
        });
    });
    $('#deleteItem').on('click', function () {
        if (!confirm('Are you sure you want to delete this item?')) return;
        const id = $('#modify-item-form').attr('data-id');
        fetch('/api/admin/shop/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Item deleted successfully!');
                $('#modifyItemPopup').addClass('hidden').removeClass('flex');
                $('#modify-item-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to delete item: ${data.message}`);
            }
        });
    });
    $('#newItemCancel').on('click', function () {
        $('#newItemPopup').removeClass('flex').addClass('hidden');
    });
    $('#new-item').on('click', function () {
        $('#newItemPopup').removeClass('hidden').addClass('flex');
    });
    $('#new-item-form').on('submit', function (e) {
        e.preventDefault();
        const name = $('#newItemName').val();
        const price = $('#newItemPrice').val();
        const image = $('#newItemImage').val();
        const visible = $('#newItemVisible').val();
        fetch('/api/admin/shop/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                price: price,
                image: image,
                visible: visible,
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Item added successfully!');
                $('#newItemPopup').addClass('hidden').removeClass('flex');
                $('#new-item-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to add item: ${data.message}`);
            }
        });
    });
    $('#manageOrderCancel').on('click', function () {
        $('#manageOrderPopup').removeClass('flex').addClass('hidden');
    });
    $('.manage-order').on('click', function (e) {
        e.preventDefault();
        const id = $(e.currentTarget).attr('data-id');
        const shipping_firstName = $(e.currentTarget).attr('data-shipping-first_name');
        const shipping_lastName = $(e.currentTarget).attr('data-shipping-last_name');
        const shipping_email = $(e.currentTarget).attr('data-shipping-email');
        const shipping_phone = $(e.currentTarget).attr('data-shipping-phone');
        const shipping_address1 = $(e.currentTarget).attr('data-shipping-address1');
        const shipping_address2 = $(e.currentTarget).attr('data-shipping-address2');
        const shipping_address3 = $(e.currentTarget).attr('data-shipping-address3');
        const shipping_address4 = $(e.currentTarget).attr('data-shipping-address4');
        const paid = $(e.currentTarget).attr('data-paid');
        const fulfilled = $(e.currentTarget).attr('data-fulfilled');

        $('#orderPaid').val(paid);
        $('#orderFulfilled').val(fulfilled);
        $('#shippingFirstName').val(shipping_firstName);
        $('#shippingLastName').val(shipping_lastName);
        $('#shippingEmail').val(shipping_email);
        $('#shippingPhone').val(shipping_phone);
        $('#shippingAddress1').val(shipping_address1);
        $('#shippingAddress2').val(shipping_address2);
        $('#shippingAddress3').val(shipping_address3);
        $('#shippingPostalCode').val(shipping_address4);
        $('#manage-order-form').attr('data-id', id);
        $('#manageOrderPopup').removeClass('hidden').addClass('flex');
    });

    $('#manage-order-form').on('submit', function (e) {
        e.preventDefault();
        const id = $('#manage-order-form').attr('data-id');
        const paid = $('#orderPaid').val();
        const fulfilled = $('#orderFulfilled').val();
        const shippingFirstName = $('#shippingFirstName').val();
        const shippingLastName = $('#shippingLastName').val();
        const shippingEmail = $('#shippingEmail').val();
        const shippingPhone = $('#shippingPhone').val();
        const shippingAddress1 = $('#shippingAddress1').val();
        const shippingAddress2 = $('#shippingAddress2').val();
        const shippingAddress3 = $('#shippingAddress3').val();
        const shippingAddress4 = $('#shippingPostalCode').val();

        fetch('/api/admin/orders/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
                paid: paid,
                fulfilled: fulfilled,
                first_name: shippingFirstName,
                last_name: shippingLastName,
                email: shippingEmail,
                phone: shippingPhone,
                address1: shippingAddress1,
                address2: shippingAddress2,
                address3: shippingAddress3,
                address4: shippingAddress4,
            }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Order updated successfully!');
                $('#manageOrderPopup').addClass('hidden').removeClass('flex');
                $('#manage-order-form input').val('');
                window.location.reload();
            } else {
                alert(`Failed to update order: ${data.message}`);
            }
        });
    });
    $('#cancelOrder').on('click', function () {
        if (!confirm('Are you sure you want to cancel this order?')) return;
        const id = $('#manage-order-form').attr('data-id');
        fetch('/api/admin/orders/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id }),
        }).then(async (response) => {
            const data = await response.json();
            if (response.status == 200) {
                alert('Order deleted successfully!');
                $('#manageOrderPopup').addClass('hidden').removeClass('flex');
                window.location.reload();
            } else {
                alert(`Failed to delete order: ${data.message}`);
            }
        });
    });
});
