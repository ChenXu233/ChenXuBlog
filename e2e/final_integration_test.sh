#!/bin/bash
# 生产集成测试 —— 部署后运行，验证完整链路
# 用法: bash e2e/final_integration_test.sh [BASE_URL]
set -e

BASE_URL="${1:-https://chenxu233.cn}"
API_URL="$BASE_URL/apis/v1"
PASS=0
FAIL=0

check() {
  local desc="$1" cond="$2"
  if eval "$cond"; then
    echo "  ✓ $desc"
    PASS=$((PASS+1))
  else
    echo "  ✗ $desc"
    FAIL=$((FAIL+1))
  fi
}

echo "=== ChenXuBlog 集成测试 ($BASE_URL) ==="

echo "[1/7] 健康检查"
check "首页 SSR 可访问 (200)" "curl -sf -o /dev/null $BASE_URL/"

echo "[2/7] 静态资源"
check "Nuxt 页面含应用标记" "curl -sf $BASE_URL/home | grep -q '__nuxt'"

echo "[3/7] API 层"
check "文章列表 API" "curl -sf -o /dev/null '$API_URL/blog/'"
check "文章详情 404 处理" "curl -s -o /dev/null -w '%{http_code}' '$API_URL/blog/99999' | grep -q 404"

echo "[4/7] 认证流程"
LOGIN=$(curl -sf -X POST "$API_URL/auth/login" -H 'Content-Type: application/json' \
  -d '{"evidence":"admin","password":"123456"}') || LOGIN=""
check "管理员登录" "echo '$LOGIN' | grep -q access_token"

echo "[5/7] MinIO 图床"
TOKEN=$(echo "$LOGIN" | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')
UPLOAD=$(curl -sf -X POST "$API_URL/img_bed/" -H "Authorization: Bearer $TOKEN" \
  -F "image=@/etc/hostname;type=text/plain" 2>/dev/null) || UPLOAD=""
check "图片上传" "echo '$UPLOAD' | grep -q url"
IMG_URL=$(echo "$UPLOAD" | sed -n 's/.*"url":"\([^"]*\)".*/\1/p')
if [ -n "$IMG_URL" ]; then
  check "图片可访问" "curl -sf -o /dev/null '$BASE_URL$IMG_URL'"
else
  echo "  ✗ 图片可访问 (无 URL)"
  FAIL=$((FAIL+1))
fi

echo "[6/7] 权限隔离"
check "未登录上传被拒" "curl -s -o /dev/null -w '%{http_code}' -X POST '$API_URL/img_bed/' -F 'image=@/etc/hostname' | grep -qE '401|403'"
check "普通用户访问 admin 被拒" "curl -s -o /dev/null -w '%{http_code}' '$API_URL/admin/stats' | grep -q 403"

echo "[7/7] SEO"
check "sitemap.xml" "curl -sf $BASE_URL/sitemap.xml | grep -q '<urlset'"

echo ""
echo "=== 结果: $PASS 通过, $FAIL 失败 ==="
if [ "$FAIL" -gt 0 ]; then exit 1; fi
