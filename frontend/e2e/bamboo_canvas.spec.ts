import { test } from "@playwright/test";

const BASE = "http://127.0.0.1:3000";

test("bamboo canvas renders and scrolls", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (err) => errors.push(err.message));

  await page.goto(`${BASE}/home`, { timeout: 30000, waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  // canvas 存在且尺寸合理
  const canvasInfo = await page.evaluate(() => {
    const c = document.querySelector(
      ".bamboo-forest canvas",
    ) as HTMLCanvasElement | null;
    if (!c) return null;
    const ctx = c.getContext("2d")!;
    const data = ctx.getImageData(0, 0, c.width, c.height).data;
    let nonEmpty = 0;
    for (let i = 3; i < data.length; i += 4000) if (data[i] > 0) nonEmpty++;
    return { w: c.width, h: c.height, nonEmptyPixels: nonEmpty };
  });
  console.log(`canvas: ${JSON.stringify(canvasInfo)}`);

  // 滚动到 intro 区，竹子应产生视差位移（进度变化 → 重绘）
  await page.evaluate(() => window.scrollBy(0, window.innerHeight * 0.5));
  await page.waitForTimeout(500);
  const after = await page.evaluate(() => {
    const c = document.querySelector(
      ".bamboo-forest canvas",
    ) as HTMLCanvasElement | null;
    const ctx = c!.getContext("2d")!;
    const d = ctx.getImageData(0, 0, c!.width, c!.height).data;
    let nonEmpty = 0;
    for (let i = 3; i < d.length; i += 4000) if (d[i] > 0) nonEmpty++;
    return nonEmpty;
  });
  console.log(`after scroll nonEmpty: ${after}`);

  // 绘制耗时（模拟一帧 draw：统计 canvas 2D 调用开销）
  const drawTime = await page.evaluate(() => {
    const t0 = performance.now();
    const c = document.querySelector(
      ".bamboo-forest canvas",
    ) as HTMLCanvasElement | null;
    const ctx = c!.getContext("2d")!;
    // 强制一帧重绘的近似：获取像素触发 GPU flush
    ctx.getImageData(0, 0, 2, 2);
    return performance.now() - t0;
  });

  console.log(`errors: ${errors.length === 0 ? "NONE" : errors.join(" | ")}`);
  console.log(`pixel flush ms: ${drawTime.toFixed(2)}`);
});
