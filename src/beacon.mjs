// Cloudflare Web Analytics. Two layouts render this site — Base.astro and
// Starlight's own — so the tag is emitted twice; the token lives here once so
// the two cannot drift apart. It is public by design: it identifies the site,
// it does not authenticate anything.
export const CF_BEACON_SRC =
  "https://static.cloudflareinsights.com/beacon.min.js";
export const CF_BEACON_DATA = '{"token": "3e2bb034da354c8b8eaf7e762e88bbd1"}';
