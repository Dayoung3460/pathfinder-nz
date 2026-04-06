/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', '-apple-system', 'system-ui', 'Segoe UI', 'Helvetica', 'Arial', 'sans-serif'],
      },
      colors: {
        notion: {
          blue:        '#0075de',
          'blue-dark': '#005bab',
          'blue-focus':'#097fe8',
          'badge-bg':  '#f2f9ff',
          'badge-txt': '#097fe8',
          warm:        '#f6f5f4',
          dark:        '#31302e',
          'gray-500':  '#615d59',
          'gray-300':  '#a39e98',
          border:      'rgba(0,0,0,0.1)',
          text:        'rgba(0,0,0,0.95)',
          'text-soft': 'rgba(0,0,0,0.9)',
          'input-border': '#dddddd',
        },
      },
      boxShadow: {
        card: [
          'rgba(0,0,0,0.04) 0px 4px 18px',
          'rgba(0,0,0,0.027) 0px 2.025px 7.847px',
          'rgba(0,0,0,0.02) 0px 0.8px 2.925px',
          'rgba(0,0,0,0.01) 0px 0.175px 1.041px',
        ].join(', '),
      },
      letterSpacing: {
        'display':    '-2.125px',
        'heading-xl': '-1.5px',
        'heading-md': '-0.625px',
        'card-title': '-0.25px',
        'body-lg':    '-0.125px',
      },
      borderColor: {
        notion: 'rgba(0,0,0,0.1)',
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
