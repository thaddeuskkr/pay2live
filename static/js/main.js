$(() => {
    if (
        localStorage.theme === 'dark' ||
        (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
    )
        $('#dark-theme').removeClass('hidden');
    else $('#light-theme').removeClass('hidden');
    $('#theme-toggle').on('click', () => {
        $(document.documentElement).toggleClass('mocha');
        $('#light-theme').toggleClass('hidden');
        $('#dark-theme').toggleClass('hidden');
        localStorage.theme = $(document.documentElement).hasClass('mocha') ? 'dark' : 'light';
    });
    $('button[aria-controls="mobile-menu"]').on('click', () => {
        var menu = $('#mobile-menu');
        var menuButton = $(this);
        var isExpanded = menuButton.attr('aria-expanded') === 'true';
        menuButton.attr('aria-expanded', !isExpanded);
        menu.toggleClass('hidden');
        menuButton.find('svg').toggleClass('hidden');
    });
    const cookies = Object.fromEntries(
        document.cookie.split(/; */).map(function (c) {
            var index = c.indexOf('='); // Find the index of the first equal sign
            var key = c.slice(0, index); // Everything upto the index is the key
            var value = c.slice(index + 1); // Everything after the index is the value

            // Return the key and value
            return [decodeURIComponent(key), decodeURIComponent(value)];
        }),
    );
    if (cookies.session_token && cookies.session_token !== 'null' && cookies.session_token.length > 5) {
        $('#login').addClass('sm:hidden').removeClass('sm:flex');
        $('#profile').addClass('sm:flex').removeClass('sm:hidden');
        $('#logout').addClass('sm:flex').removeClass('sm:hidden');
        $('#login-mobile').addClass('hidden').removeClass('flex');
        $('#profile-mobile').addClass('flex').removeClass('hidden');
        $('#logout-mobile').addClass('flex').removeClass('hidden');
    }
});

function logout() {
    document.cookie.split(';').forEach(function (c) {
        document.cookie = c.replace(/^ +/, '').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
    });
    location.reload();
}
