module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'sans-serif'],
      },
      colors: {
        primary: '#0069FF',
        secondary: '#4B00E0',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        dark: '#1F2937',
      }
    },
  },
  plugins: [],
}