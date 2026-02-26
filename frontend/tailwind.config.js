/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'mohi-deep-blue': '#1c3c54',
        'mohi-action-blue': '#4595d1',
        'mohi-green': '#8bc53f',
        'mohi-dark-bg': '#0a1a26',
        'mohi-dark-surface': '#122232',
      },
      fontFamily: {
        'caveat': ['Caveat', 'cursive'],
        'inter': ['Inter', 'sans-serif'],
      },
      animation: {
        'pulse-green': 'pulseGreen 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'fade-in': 'fadeIn 0.2s ease-out',
      },
      keyframes: {
        pulseGreen: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.7', transform: 'scale(1.05)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
