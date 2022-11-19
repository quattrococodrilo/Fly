/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./ui/templates/ui/**/*.{html,js}",
    "./ui/templatetags/**/*.{html,js,py}",
    "./apps/core/templates/core/**/*.{html,js}",
    "./templates/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
