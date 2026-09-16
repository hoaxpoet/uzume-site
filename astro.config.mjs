// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { CF_BEACON_SRC, CF_BEACON_DATA } from "./src/beacon.mjs";

// https://astro.build/config
export default defineConfig({
  site: "https://uzume.io",
  // This site ships zero client JS by default.
  prefetch: false,
  integrations: [
    starlight({
      title: "Uzume",
      // Starlight renders its own layout, so Base.astro's beacon never reaches
      // these pages. Inject it here too.
      head: [
        {
          tag: "script",
          attrs: {
            type: "module",
            src: CF_BEACON_SRC,
            "data-cf-beacon": CF_BEACON_DATA,
          },
        },
      ],
      components: {
        // Pins /docs to dark and drops the picker; see each component's comment.
        ThemeProvider: "./src/components/DocsThemeProvider.astro",
        ThemeSelect: "./src/components/DocsThemeSelect.astro",
      },
      // Starlight defaults to /favicon.svg, which this site does not ship.
      favicon: "/favicon-32.png",
      // Docs live under /docs; the landing page at / is a plain Astro page.
      disable404Route: true,
      customCss: ["./src/styles/fonts.css", "./src/styles/docs.css"],
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/hoaxpoet/uzume",
        },
      ],
      sidebar: [
        { label: "Docs", items: [{ label: "Overview", slug: "docs" }] },
      ],
    }),
  ],
});
