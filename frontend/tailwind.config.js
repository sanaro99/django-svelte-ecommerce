module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './static/**/*.{html,js}'
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light', 'dark'],
    styled: true,
    base: true,
    utils: true,
    logs: true,
    rtl: false
  }
};
