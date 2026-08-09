<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800"
  >
    <UCard class="w-full max-w-md">
      <template #header
        ><h1 class="text-2xl font-bold text-center">登录</h1></template
      >
      <div class="space-y-4">
        <UFormField label="用户名或邮箱" name="evidence">
          <UInput
            v-model="form.evidence"
            class="w-full"
            placeholder="输入用户名或邮箱"
          />
        </UFormField>
        <UFormField label="密码" name="password">
          <UInput
            v-model="form.password"
            type="password"
            class="w-full"
            placeholder="输入密码"
          />
        </UFormField>
        <UButton color="primary" block :loading="loading" @click="handleLogin"
          >登录</UButton
        >
      </div>
      <template #footer>
        <div class="text-center text-sm text-gray-400">
          还没有账号？<NuxtLink
            to="/register"
            class="text-primary-400 hover:underline"
            >注册</NuxtLink
          >
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const loading = ref(false);
const form = reactive({ evidence: "", password: "" });

const toast = useToast();

async function handleLogin() {
  loading.value = true;
  try {
    await auth.login(form.evidence, form.password);
    toast.add({
      title: "登录成功",
      color: "success",
      icon: "i-heroicons-check-circle",
    });
    const redirect = (route.query.redirect as string) || "/home";
    router.push(redirect);
  } catch (e: any) {
    toast.add({
      title: e?.data?.detail || "登录失败",
      color: "error",
      icon: "i-heroicons-exclamation-circle",
    });
  } finally {
    loading.value = false;
  }
}
</script>
