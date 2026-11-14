// SEO helper: title, OG/Twitter cards, canonical, JSON-LD.
interface SeoOptions {
  title?: string;
  description?: string;
  image?: string;
  type?: "website" | "article";
  noindex?: boolean;
  publishedTime?: string | Date;
  modifiedTime?: string | Date;
  tags?: string[];
  author?: string;
  jsonLd?: Record<string, unknown> | null;
}

const DEFAULT_DESCRIPTION =
  "晨煦的个人博客：代码、物理、哲学与生活。烟花三月，雾与花之间。";

export function useSeo(opts: SeoOptions = {}) {
  const config = useRuntimeConfig();
  const route = useRoute();
  const siteUrl = String(config.public.siteUrl || "http://localhost:3000").replace(
    /\/$/,
    "",
  );

  const fullTitle = opts.title
    ? opts.title.includes("晨煦")
      ? opts.title
      : `${opts.title} · 晨煦 CHENXU`
    : "chenxu's homepage";

  const description = (opts.description || DEFAULT_DESCRIPTION)
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 180);

  const image = opts.image
    ? opts.image.startsWith("http")
      ? opts.image
      : siteUrl + (opts.image.startsWith("/") ? opts.image : `/${opts.image}`)
    : undefined;

  const canonical = siteUrl + (route.path === "/" ? "/home" : route.path);

  const meta = [
    { name: "description", content: description },
    { property: "og:title", content: fullTitle },
    { property: "og:description", content: description },
    { property: "og:type", content: opts.type || "website" },
    { property: "og:url", content: canonical },
    { property: "og:site_name", content: "晨煦 CHENXU" },
    { property: "og:locale", content: "zh_CN" },
    { name: "twitter:card", content: image ? "summary_large_image" : "summary" },
    { name: "twitter:title", content: fullTitle },
    { name: "twitter:description", content: description },
    ...(image
      ? [
          { property: "og:image", content: image },
          { name: "twitter:image", content: image },
        ]
      : []),
    ...(opts.noindex
      ? [{ name: "robots", content: "noindex, nofollow" }]
      : [{ name: "robots", content: "index, follow, max-image-preview:large" }]),
    ...(opts.type === "article" && opts.publishedTime
      ? [
          {
            property: "article:published_time",
            content: new Date(opts.publishedTime).toISOString(),
          },
        ]
      : []),
    ...(opts.type === "article" && opts.modifiedTime
      ? [
          {
            property: "article:modified_time",
            content: new Date(opts.modifiedTime).toISOString(),
          },
        ]
      : []),
    ...(opts.type === "article" && opts.author
      ? [{ property: "article:author", content: opts.author }]
      : []),
    ...(opts.tags?.length
      ? opts.tags.map((tag) => ({ property: "article:tag", content: tag }))
      : []),
  ];

  useHead({
    title: fullTitle,
    meta,
    link: [{ rel: "canonical", href: canonical }],
    script: opts.jsonLd
      ? [
          {
            type: "application/ld+json",
            innerHTML: JSON.stringify(opts.jsonLd).replace(/</g, "\\u003c"),
          },
        ]
      : [],
  });
}
