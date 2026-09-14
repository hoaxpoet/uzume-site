import { defineCollection } from "astro:content";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";

// ponytail: docs only. Starlight warns about a missing "i18n" collection at build
// time; defining an empty one produces the identical warning, so it is not defined.
export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
