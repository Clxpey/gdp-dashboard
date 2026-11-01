import { defineConfig } from 'astro/config';
// Set `site` to the real domain once it exists (needed for canonical/OG URLs).
export default defineConfig({ build: { inlineStylesheets: 'auto' } });
