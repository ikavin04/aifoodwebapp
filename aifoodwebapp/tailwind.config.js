/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        butter: '#FFF4D8',
        cherry: '#7D0C1C',
        olive: '#4D6B30',
        oat: '#F4EDDA',
        primary: '#7D0C1C',
        secondary: '#4D6B30',
      }
    },
  },
  plugins: [],
}
