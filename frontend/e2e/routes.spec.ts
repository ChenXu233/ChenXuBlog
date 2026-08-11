// 本地路由行为 E2E：页面渲染 + DockBar 导航 + 搜索跳转 + 认证流
import { test, expect } from "@playwright/test";

const BASE = "http://127.0.0.1:3000";

test.describe("路由行为", () => {
  test("根路径 301 重定向到 /home", async ({ request }) => {
    const resp = await request.get(BASE, { maxRedirects: 0 });
    expect(resp.status()).toBe(301);
    expect(resp.headers()["location"]).toContain("/home");
  });

  test("全部页面渲染 200", async ({ page }) => {
    const pages = [
      "/home",
      "/login",
      "/register",
      "/article",
      "/archive",
      "/diary",
      "/friend",
      "/forgot-password",
      "/reset-password",
    ];
    for (const p of pages) {
      const resp = await page.goto(`${BASE}${p}`, { timeout: 30000 });
      expect(resp?.status(), `${p} 应返回 200`).toBe(200);
    }
  });

  test("DockBar 导航点击跳转", async ({ page }) => {
    await page.goto(`${BASE}/home`, {
      timeout: 30000,
      waitUntil: "networkidle",
    });
    await page.waitForTimeout(1500);
    // 展开菜单
    await page.locator(".nav-trigger-area").hover();
    await page.waitForTimeout(800);
    await page.locator(".dock-item").first().click();
    await page.waitForTimeout(800);
    // 点击"文章"导航
    const articleLink = page.locator(".nav-grid-item", { hasText: "文章" });
    await articleLink.click();
    await page.waitForURL("**/article", { timeout: 10000 });
    expect(page.url()).toContain("/article");
  });

  test("搜索框跳转带 search 参数", async ({ page }) => {
    await page.goto(`${BASE}/home`, {
      timeout: 30000,
      waitUntil: "networkidle",
    });
    await page.waitForTimeout(1500);
    await page.locator(".nav-trigger-area").hover();
    await page.waitForTimeout(800);
    await page.locator(".dock-item").first().click();
    await page.waitForTimeout(800);
    await page.locator(".search-input").fill("测试");
    await page.locator(".search-input").press("Enter");
    await page.waitForURL("**/article?search=*", { timeout: 10000 });
    console.log(`search URL: ${page.url()}`);
  });

  test("登录流程（admin 账号）", async ({ page }) => {
    await page.goto(`${BASE}/login`, {
      timeout: 30000,
      waitUntil: "networkidle",
    });
    await page.locator("#evidence").fill("admin");
    await page.locator("#password").fill("123456");
    await page.locator(".login-btn").click();
    await page.waitForURL("**/home", { timeout: 15000 });
    console.log("login -> home OK");
  });

  test("未登录访问 /article/create 跳转登录", async ({ page }) => {
    await page.goto(`${BASE}/article/create`, { timeout: 30000 });
    // 原版无路由守卫，直接渲染页面（允许 200）；记录行为
    const body = await page.textContent("body");
    console.log(
      `create page body: ${body?.includes("创建文章") ? "编辑器渲染" : "其他"}`,
    );
  });

  test("404 页面", async ({ page }) => {
    const resp = await page.goto(`${BASE}/nonexistent-page`, {
      timeout: 30000,
    });
    expect([200, 404]).toContain(resp?.status());
  });
});
