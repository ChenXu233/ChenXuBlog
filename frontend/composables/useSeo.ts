// SEO helper: unified useHead with OG tags
interface SeoOptions {
  title?: string;
  description?: string;
  image?: string;
  type?: "website" | "article";
  noindex?: boolean;
}

export function useSeo(opts: SeoOptions = {}) {
  const config = useRuntimeConfig();
  const siteUrl = (config.public.siteUrl as string) || "http://localhost:3000";
  const route = useRoute();

  const title = computed(() =>
    opts.title
      ? `${opts.title} - ChenXuBlog`
      : "ChenXuBlog - 技术分享与生活记录",
  );
  const description =
    opts.description || "ChenXu 的个人博客，分享技术心得与生活记录";
  const image = opts.image
    ? opts.image.startsWith("http")
      ? opts.image
      : siteUrl + opts.image
    : undefined;

  useHead({
    title,
    meta: [
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
      { property: "og:type", content: opts.type || "website" },
      { property: "og:url", content: siteUrl + route.fullPath },
      ...(image ? [{ property: "og:image", content: image }] : []),
      ...(opts.noindex
        ? [{ name: "robots", content: "noindex, nofollow" }]
        : []),
    ],
    link: [{ rel: "canonical", href: siteUrl + route.fullPath }],
  });
}
