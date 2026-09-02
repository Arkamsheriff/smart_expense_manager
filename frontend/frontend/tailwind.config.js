/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#10151C',
          soft: '#4B5563',
          faint: '#8A93A0',
        },
        paper: '#F4F5F1',
        surface: '#FFFFFF',
        line: '#E1E3DD',
        emerald: {
          50: '#EAF5F0',
          100: '#CDE8DC',
          400: '#1C9A6C',
          500: '#0B6E4F',
          600: '#08573F',
        },
        rose: {
          50: '#F7EAEC',
          100: '#EDCBD0',
          400: '#C24C5E',
          500: '#A6394A',
          600: '#852D3A',
        },
        amber: {
          50: '#F9F0DE',
          100: '#F0DBAA',
          400: '#BC8517',
          500: '#9C6B0B',
          600: '#7A5309',
        },
      },
      fontFamily: {
        display: ['"Fraunces"', 'Georgia', 'serif'],
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 2px rgba(16,21,28,0.04), 0 1px 12px rgba(16,21,28,0.04)',
      },
      borderRadius: {
        card: '10px',
      },
    },
  },
  plugins: [],
}
