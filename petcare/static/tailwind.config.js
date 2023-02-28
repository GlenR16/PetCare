/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        dmserif: ["DM Serif", "serif"],
        com: ["Comfortaa", "cursive"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
