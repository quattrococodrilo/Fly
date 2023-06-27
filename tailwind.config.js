/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./ui/templates/ui/**/*.{html,js}",
    "./ui/templatetags/**/*.{html,js,py}",
    "./core/templates/core/**/*.{html,js}",
    "./apps/**/templates/**/*.{html,js}",
    "./templates/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
