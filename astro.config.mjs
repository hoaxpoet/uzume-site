// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  site: "https://uzume.io",
  // This site ships zero client JS by default.
  prefetch: false,
  integrations: [
    starlight({
      title: "Uzume",
      // Starlight defaults to /favicon.svg, which this site does not ship.
      favicon: "/favicon-32.png",
      // Docs live under /docs; the landing page at / is a plain Astro page.
      disable404Route: true,
      customCss: ["./src/styles/docs.css"],
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
