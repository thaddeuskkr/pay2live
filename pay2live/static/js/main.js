$(() => {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) $('#dark-theme').removeClass('hidden');
    else $('#light-theme').removeClass('hidden');
    $('#theme-toggle').on('click', () => {
        $(document.documentElement).toggleClass('mocha');
        $('#light-theme').toggleClass('hidden');
        $('#dark-theme').toggleClass('hidden');
        localStorage.theme = $(document.documentElement).hasClass('mocha') ? 'dark' : 'light';
    });
})