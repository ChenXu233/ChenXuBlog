import { expect, test } from "@playwright/test";
import { renderMarkdown } from "../utils/markdown";
import { fetchAllPages } from "../utils/pagination";

test("Markdown escapes raw HTML and unsafe links", () => {
  const rendered = renderMarkdown(
    "# Safe title\n\n<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>\n\n**safe**\n\n[bad](javascript:alert(1))",
  );

  expect(rendered.html).not.toContain("<script>");
  expect(rendered.html).not.toContain("<img src=");
  expect(rendered.html).toContain("&lt;script&gt;");
  expect(rendered.html).toContain("<strong>safe</strong>");
  expect(rendered.html).not.toContain('href="javascript:');
  expect(rendered.toc[0]?.title).toBe("Safe title");
});

test("fetchAllPages retrieves every item in order", async () => {
  const values = Array.from({ length: 205 }, (_, index) => index);
  const requestedPages: number[] = [];

  const result = await fetchAllPages<number>(async (page, pageSize) => {
    requestedPages.push(page);
    const items = values.slice((page - 1) * pageSize, page * pageSize);
    return {
      items,
      total: values.length,
      page,
      page_size: pageSize,
      total_pages: Math.ceil(values.length / pageSize),
    };
  });

  expect(requestedPages).toEqual([1, 2, 3]);
  expect(result.items).toEqual(values);
  expect(result.total).toBe(205);
});
