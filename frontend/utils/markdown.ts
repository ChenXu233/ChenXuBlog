// Markdown rendering with syntax highlighting + TOC extraction
import markdownit from "markdown-it";
import hljs from "highlight.js/lib/common";

const md = markdownit({
  html: true,
  linkify: true,
  highlight(code: string, lang: string): string {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${
          hljs.highlight(code, { language: lang, ignoreIllegals: true }).value
        }</code></pre>`;
      } catch {
        /* fallthrough */
      }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(code)}</code></pre>`;
  },
});

export interface TocItem {
  id: string;
  level: number;
  title: string;
}

// Render markdown and collect heading anchors for TOC
export function renderMarkdown(body: string): { html: string; toc: TocItem[] } {
  const toc: TocItem[] = [];
  const env: Record<string, unknown> = {};

  md.renderer.rules.heading_open = (tokens, idx) => {
    const token = tokens[idx];
    const inline = tokens[idx + 1];
    const title = inline?.content || "";
    const id =
      title
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fff\s-]/g, "")
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-") || `h-${idx}`;
    token.attrSet("id", id);
    toc.push({ id, level: Number(token.tag.slice(1)), title });
    return "";
  };

  const html = md.render(body, env);
  return { html, toc };
}
