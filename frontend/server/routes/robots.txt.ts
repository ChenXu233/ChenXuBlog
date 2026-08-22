// robots.txt with absolute Sitemap URL from runtime config
export default defineEventHandler((event) => {
  const config = useRuntimeConfig();
  const siteUrl = (
    (config.public.siteUrl as string) || "http://localhost:3000"
  ).replace(/\/$/, "");

  const txt = `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;
  setHeader(event, "Content-Type", "text/plain; charset=utf-8");
  return txt;
});
