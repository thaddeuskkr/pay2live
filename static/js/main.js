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
});

function logout() {
    document.cookie.split(';').forEach(function (c) {
        document.cookie = c.replace(/^ +/, '').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
    });
    location.reload();
}
