// RSS 2.0 feed generated from published blogs
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const siteUrl = (
    (config.public.siteUrl as string) || "http://localhost:3000"
  ).replace(/\/$/, "");
  const apiBase = (config.public.apiBase as string) || "/apis/v1";
  const backendUrl =
    process.env.NUXT_API_INTERNAL_URL || "http://127.0.0.1:8001";

  let items = "";
  try {
    const blogs = await $fetch<{
      items: {
        id: number;
        title: string;
        body: string;
        created_at: string;
      }[];
    }>(`${backendUrl}${apiBase}/blog/?page_size=50`);
    items = (blogs.items || [])
      .map(
        (b) =>
          `    <item>\n      <title>${escapeXml(
            b.title,
          )}</title>\n      <link>${siteUrl}/article/${
            b.id
          }</link>\n      <guid isPermaLink="true">${siteUrl}/article/${
            b.id
          }</guid>\n      <pubDate>${new Date(
            b.created_at,
          ).toUTCString()}</pubDate>\n      <description>${escapeXml(
            b.body.slice(0, 500),
          )}</description>\n    </item>`,
      )
      .join("\n");
  } catch (e) {
    console.warn("rss: backend unavailable, empty feed", e);
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>ChenXu's Blog</title>
    <link>${siteUrl}</link>
    <description>ChenXu 的个人博客，分享技术心得与生活记录</description>
    <language>zh-CN</language>
${items}
  </channel>
</rss>`;

  setHeader(event, "Content-Type", "application/rss+xml; charset=utf-8");
  return xml;
});

function escapeXml(s: string): string {
  return s.replace(
    /[<>&'"]/g,
    (c) =>
      ({
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        "'": "&apos;",
        '"': "&quot;",
      })[c]!,
  );
}
