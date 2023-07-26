/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./ui/templates/**/*.{html,js}",
    "./ui/templatetags/**/*.{html,js,py}",
    "./core/templates/**/*.{html,js}",
    "./fly_admin/templates/**/*.{html,js}",
    "./fly_admin/forms/*.py",
    "./fly_admin/forms.py",
    "./account/templates/**/*.{html,js}",
    "./account/forms/*.py",
    "./account/forms.py",
    "./apps/**/templates/**/*.{html,js}",
    "./apps/**/templatetags/**/*.{html,js,py}",
    "./apps/**/forms/*.py",
    "./apps/**/forms.py",
    "./templates/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
