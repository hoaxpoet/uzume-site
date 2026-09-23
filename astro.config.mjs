// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import sitemap from "@astrojs/sitemap";
import { CF_BEACON_SRC, CF_BEACON_DATA } from "./src/beacon.mjs";

// https://astro.build/config
export default defineConfig({
  site: "https://uzume.io",
  // This site ships zero client JS by default.
  prefetch: false,
  integrations: [
    // The three pages Base.astro marks `noindex` must not appear here either —
    // a sitemap entry is a request to index, which contradicts the tag on the
    // page and is the kind of mixed signal that gets a whole sitemap ignored.
    // /404 is excluded by the integration itself; named anyway so the set of
    // pages kept out of search lives in one readable place.
    sitemap({
      filter: (page) => !/\/(404|design|confirmed)\/$/.test(page),
    }),
    starlight({
      title: "Uzume",
      // Starlight renders its own layout, so Base.astro's beacon and
      // theme-color never reach these pages. Inject them here too.
      head: [
        {
          tag: "script",
          attrs: {
            type: "module",
            src: CF_BEACON_SRC,
            "data-cf-beacon": CF_BEACON_DATA,
          },
        },
        {
          tag: "meta",
          attrs: { name: "theme-color", content: "#0B0C10" },
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
        {
          label: "Docs",
          items: [
            { label: "Overview", slug: "docs" },
            { label: "Getting started", slug: "docs/getting-started" },
            { label: "Using Uzume", slug: "docs/using-uzume" },
            { label: "Contributing", slug: "docs/contributing" },
          ],
        },
      ],
    }),
  ],
});
