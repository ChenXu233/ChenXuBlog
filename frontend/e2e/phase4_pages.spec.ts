// Phase 4 E2E: admin pages, article detail, error pages
import { test, expect } from "@playwright/test";
import path from "path";

const SCREENSHOT_DIR = path.resolve(process.cwd(), "e2e-screenshots");

// Warm up Nuxt dev server (on-demand compilation) before any test
test.beforeAll(async ({ browser }) => {
  test.setTimeout(180000);
  const page = await browser.newPage();
  const pages = ["/home", "/login", "/article", "/admin/users"];
  for (const p of pages) {
    await page.goto(p, { timeout: 120000 }).catch(() => {});
  }
  await page.close();
});

// Helper: login as admin via UI
async function loginAsAdmin(page) {
  await page.goto("/login", { timeout: 60000 });
  await page.waitForLoadState("networkidle", { timeout: 30000 });
  // If already logged in (persisted), clear and reload
  if (!page.url().includes("/login")) {
    await page.evaluate(() => localStorage.clear());
    await page.goto("/login", { timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 30000 });
  }
  await page.getByPlaceholder("输入用户名或邮箱").fill("admin");
  await page.getByPlaceholder("输入密码").fill("123456");
  await page.getByRole("button", { name: "登录" }).click();
  await page.waitForURL("/home", { timeout: 30000 });
}

test.describe("Phase 4: Admin Pages", () => {
  test("仪表盘渲染", async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto("/admin");
    await expect(page.getByRole("heading", { name: "仪表盘" })).toBeVisible();
    await expect(page.getByText("用户总数")).toBeVisible();
    await expect(page.getByText("文章总数")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-01-admin-dashboard.png"),
      fullPage: true,
    });
  });

  test("用户管理页", async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto("/admin/users");
    await expect(page.getByRole("heading", { name: "用户管理" })).toBeVisible();
    await expect(
      page.getByRole("cell", { name: "admin", exact: true }),
    ).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-02-admin-users.png"),
      fullPage: true,
    });
  });

  test("角色管理页", async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto("/admin/roles");
    await expect(page.getByRole("heading", { name: "角色管理" })).toBeVisible();
    await expect(page.getByText("superuser")).toBeVisible();
    await expect(page.getByText("default")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-03-admin-roles.png"),
      fullPage: true,
    });
  });

  test("文章管理页", async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto("/admin/articles");
    await expect(page.getByRole("heading", { name: "文章管理" })).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-04-admin-articles.png"),
      fullPage: true,
    });
  });

  test("评论管理页", async ({ page }) => {
    await loginAsAdmin(page);
    await page.goto("/admin/comments");
    await expect(page.getByRole("heading", { name: "评论管理" })).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-05-admin-comments.png"),
      fullPage: true,
    });
  });

  test("普通用户访问 admin 被拒绝", async ({ page }) => {
    // Register + login a normal user (unique username to avoid conflicts)
    const username = `normal_${Date.now()}`;
    await page.goto("/register", { timeout: 60000 });
    await page.waitForLoadState("networkidle");
    await page.getByPlaceholder("输入用户名").fill(username);
    await page.getByPlaceholder("输入邮箱").fill(`${username}@example.com`);
    await page.getByPlaceholder("输入密码").fill("NormalPass123!");
    await page.getByRole("button", { name: "注册" }).click();
    await page.waitForURL(/login/, { timeout: 30000 });
    await page.getByPlaceholder("输入用户名或邮箱").fill(username);
    await page.getByPlaceholder("输入密码").fill("NormalPass123!");
    await page.getByRole("button", { name: "登录" }).click();
    await page.waitForURL("/home", { timeout: 15000 });

    await page.goto("/admin");
    await page.waitForURL("/home", { timeout: 15000 });
    expect(page.url()).toContain("/home");
  });
});

test.describe("Phase 4: Article Detail", () => {
  test("文章详情 + TOC 目录", async ({ page }) => {
    // Create an article via API first (admin token from localStorage after login)
    await loginAsAdmin(page);
    const token = await page.evaluate(() => {
      const raw = localStorage.getItem("chenxu-auth");
      return raw ? JSON.parse(raw).token : null;
    });
    expect(token).toBeTruthy();
    const createResp = await page.request.post("/apis/v1/blog/", {
      headers: { Authorization: `Bearer ${token}` },
      data: {
        title: "TOC Test Article 目录测试",
        body: "# 第一章\n内容一\n\n## 第二章\n内容二\n\n```python\nprint(1)\n```",
        tags: ["toc"],
        published: true,
      },
    });
    expect(createResp.status()).toBe(200);
    const blogId = (await createResp.json()).id;

    await page.goto(`/article/${blogId}`);
    await expect(page.locator("h1").first()).toBeVisible();
    await expect(page.getByText("内容一", { exact: true })).toBeVisible();
    await expect(page.getByRole("link", { name: "第一章" })).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-06-article-detail.png"),
      fullPage: true,
    });
  });

  test("404 页面", async ({ page }) => {
    await page.goto("/nonexistent-page-xyz");
    await expect(page.getByText("404").first()).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("页面不存在")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "p4-07-404.png"),
      fullPage: true,
    });
  });
});

test.describe("Phase 4: SEO", () => {
  test("sitemap.xml 可访问", async ({ page }) => {
    const resp = await page.request.get("/sitemap.xml");
    expect(resp.status()).toBe(200);
    const body = await resp.text();
    expect(body).toContain("<urlset");
    expect(body).toContain("<loc>");
  });

  test("首页 OG 标签", async ({ page }) => {
    await page.goto("/home");
    const ogTitle = await page
      .locator('meta[property="og:title"]')
      .getAttribute("content");
    expect(ogTitle).toBeTruthy();
    const canonical = await page
      .locator('link[rel="canonical"]')
      .getAttribute("href");
    expect(canonical).toContain("/home");
  });
});
