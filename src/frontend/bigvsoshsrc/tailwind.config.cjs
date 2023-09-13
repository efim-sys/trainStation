
/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: {
    enabled: process.env.NODE_ENV === 'production',
    safeList: [],
    content: ['./index.html', './src/**/*.tsx', './src/**/*.ts', './src/App.svelte'],
  },
  // 1. Apply the dark mode class setting:
  darkMode: 'class',
  content: [
    './src/**/*.{html,js,svelte,ts}',
    // 2. Append the path for the Skeleton NPM package and files:
    require('path').join(require.resolve(
            '@skeletonlabs/skeleton'),
        '../**/*.{html,js,svelte,ts}'
    )
  ],
  theme: {
    extend: {},
  },
  plugins: [
    // 3. Append the Skeleton plugin to the end of this list
    ...require('@skeletonlabs/skeleton/tailwind/skeleton.cjs')()
  ]
}
