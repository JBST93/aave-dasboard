/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'body-light': '#000000', // Default text color for light mode
        'body-dark': '#ffffff', // Default text color for dark mode
      },
    },
  },
  plugins: [],
};
