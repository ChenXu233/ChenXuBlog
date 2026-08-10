// Sitemap.xml generated from published blogs
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const siteUrl = (
    (config.public.siteUrl as string) || "http://localhost:3000"
  ).replace(/\/$/, "");
  const apiBase = (config.public.apiBase as string) || "/apis/v1";

  // 直连后端（SSR 服务端无 vite proxy），本地默认 8001
  const backendUrl =
    process.env.NUXT_API_INTERNAL_URL || "http://127.0.0.1:8001";

  let urls: string[] = [];
  try {
    const blogs = await $fetch<{ items: { id: number; updated_at: string }[] }>(
      `${backendUrl}${apiBase}/blog/?page_size=100`,
    );
    urls = (blogs.items || []).map(
      (b) =>
        `  <url>\n    <loc>${siteUrl}/article/${b.id}</loc>\n    <lastmod>${b.updated_at}</lastmod>\n  </url>`,
    );
  } catch (e) {
    // API unavailable: serve static pages only
    console.warn("sitemap: backend unavailable, static only", e);
  }

  const staticPages = [
    "",
    "/home",
    "/article",
    "/archive",
    "/friend",
    "/diary",
    "/warmos",
  ].map((p) => `  <url>\n    <loc>${siteUrl}${p || "/"}</loc>\n  </url>`);

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${staticPages.join(
    "\n",
  )}\n${urls.join("\n")}\n</urlset>`;

  setHeader(event, "Content-Type", "application/xml");
  return xml;
});
