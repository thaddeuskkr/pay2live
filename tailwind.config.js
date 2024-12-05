/** @type {import('tailwindcss').Config} */
const catppuccin = require('@catppuccin/tailwindcss')
module.exports = {
    content: ["./templates/*.html"],
    theme: {
        extend: {},
    },
    darkMode: 'selector',
    plugins: [
        catppuccin({
            defaultFlavour: 'latte',
            prefix: false
        })
    ]
}

