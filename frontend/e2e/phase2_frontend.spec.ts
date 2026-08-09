import { test, expect } from "@playwright/test";
import path from "path";

const SCREENSHOT_DIR = path.resolve(process.cwd(), "e2e-screenshots");

test.describe("Phase 2: Nuxt Frontend", () => {
  test("首页渲染正常", async ({ page }) => {
    const response = await page.goto("/home");
    expect(response?.status()).toBe(200);
    await expect(page.locator(".elegant-title")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "01-home.png"),
      fullPage: true,
    });
  });

  test("登录页面渲染正常", async ({ page }) => {
    await page.goto("/login");
    await expect(page.getByRole("heading", { name: "登录" })).toBeVisible();
    await expect(page.getByPlaceholder("输入用户名或邮箱")).toBeVisible();
    await expect(page.getByPlaceholder("输入密码")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "02-login.png"),
      fullPage: true,
    });
  });

  test("注册页面渲染正常", async ({ page }) => {
    await page.goto("/register");
    await expect(page.getByRole("heading", { name: "注册" })).toBeVisible();
    await expect(page.getByPlaceholder("输入用户名")).toBeVisible();
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "03-register.png"),
      fullPage: true,
    });
  });

  test("登录流程", async ({ page }) => {
    await page.goto("/login");
    await page.getByPlaceholder("输入用户名或邮箱").fill("admin");
    await page.getByPlaceholder("输入密码").fill("123456");
    await page.getByRole("button", { name: "登录" }).click();
    await page.waitForURL("/home", { timeout: 15000 });
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "04-login-success.png"),
      fullPage: true,
    });
  });

  test("文章列表页", async ({ page }) => {
    await page.goto("/article");
    await expect(page.locator("h1")).toContainText("文章列表");
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "05-article-list.png"),
      fullPage: true,
    });
  });

  test("未登录访问受保护页面", async ({ page }) => {
    await page.goto("/admin");
    await page.waitForURL(/\/login/);
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "06-auth-redirect.png"),
      fullPage: true,
    });
  });
});
