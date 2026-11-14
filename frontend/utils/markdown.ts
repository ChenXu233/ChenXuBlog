// Markdown rendering with syntax highlighting + TOC extraction
import markdownit from "markdown-it";
import hljs from "highlight.js/lib/common";

export interface TocItem {
  id: string;
  level: number;
  title: string;
}

function slugify(input: string) {
  return input
    .trim()
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fff\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

/**
 * Render markdown into HTML and collect a table of contents.
 * - h1..h6 are demoted by one level (the page owns the only h1)
 * - every heading gets a stable, unique id
 * - external links open in a new tab; images are lazy-loaded
 */
export function renderMarkdown(body: string): { html: string; toc: TocItem[] } {
  const toc: TocItem[] = [];
  const slugCount = new Map<string, number>();

  const md = markdownit({
    html: true,
    linkify: true,
    typographer: true,
    highlight(code: string, lang: string): string {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return `<pre class="hljs"><code>${
            hljs.highlight(code, { language: lang, ignoreIllegals: true }).value
          }</code></pre>`;
        } catch {
          /* fall through */
        }
      }
      return `<pre class="hljs"><code>${md.utils.escapeHtml(code)}</code></pre>`;
    },
  });

  md.renderer.rules.heading_open = (tokens, idx) => {
    const token = tokens[idx];
    const inline = tokens[idx + 1];
    const raw = inline?.content?.trim() || "";
    const sourceLevel = Number(token.tag.slice(1));
    const level = Math.min(sourceLevel + 1, 6);
    const base = slugify(raw) || `h-${idx}`;
    const count = (slugCount.get(base) ?? 0) + 1;
    slugCount.set(base, count);
    const id = count > 1 ? `${base}-${count}` : base;

    toc.push({ id, level, title: raw });
    return `<h${level} id="${md.utils.escapeHtml(id)}">`;
  };

  md.renderer.rules.heading_close = (tokens, idx) => {
    const sourceLevel = Number(tokens[idx].tag.slice(1));
    return `</h${Math.min(sourceLevel + 1, 6)}>`;
  };

  const defaultLinkOpen =
    md.renderer.rules.link_open ||
    ((tokens, idx, options, _env, self) =>
      self.renderToken(tokens, idx, options));

  md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
    const href = tokens[idx].attrGet("href") || "";
    if (/^https?:\/\//.test(href)) {
      tokens[idx].attrSet("target", "_blank");
      tokens[idx].attrSet("rel", "noopener noreferrer");
    }
    return defaultLinkOpen(tokens, idx, options, env, self);
  };

  const defaultImage =
    md.renderer.rules.image ||
    ((tokens, idx, options, _env, self) =>
      self.renderToken(tokens, idx, options));

  md.renderer.rules.image = (tokens, idx, options, env, self) => {
    tokens[idx].attrSet("loading", "lazy");
    tokens[idx].attrSet("decoding", "async");
    return defaultImage(tokens, idx, options, env, self);
  };

  return { html: md.render(body, {}), toc };
}
