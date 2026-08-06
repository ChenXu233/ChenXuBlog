<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
    <UCard class="w-full max-w-md">
      <template #header><h1 class="text-2xl font-bold text-center">注册</h1></template>
      <UForm :state="form" @submit="handleRegister" class="space-y-4">
        <UFormField label="用户名" name="username">
          <UInput v-model="form.username" class="w-full" placeholder="输入用户名" />
        </UFormField>
        <UFormField label="邮箱" name="email">
          <UInput v-model="form.email" type="email" class="w-full" placeholder="输入邮箱" />
        </UFormField>
        <UFormField label="密码" name="password">
          <UInput v-model="form.password" type="password" class="w-full" placeholder="输入密码" />
        </UFormField>
        <UButton type="submit" color="primary" block :loading="loading">注册</UButton>
      </UForm>
      <template #footer>
        <div class="text-center text-sm text-gray-400">
          已有账号？<NuxtLink to="/login" class="text-primary-400 hover:underline">登录</NuxtLink>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup lang="ts">
const auth = useAuthStore()
const toast = useToast()
const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', email: '', password: '' })

async function handleRegister() {
  loading.value = true
  try {
    await auth.register(form.username, form.email, form.password)
    toast.success('注册成功，请查收验证邮件')
    router.push('/login')
  } catch (e: any) {
    toast.error(e?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>