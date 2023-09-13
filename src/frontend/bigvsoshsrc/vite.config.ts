import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { viteSingleFile } from "vite-plugin-singlefile";
import htmlPurge from 'vite-plugin-purgecss'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    cssMinify: true
  },
  plugins: [
      svelte(),
      // htmlPurge({}) as Plugin,
      viteSingleFile(),
  ],
})
