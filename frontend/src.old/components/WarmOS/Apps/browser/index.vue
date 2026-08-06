<template>
  <div class="browser-app">
    <div class="browser-toolbar">
      <button class="toolbar-btn" @click="goBack" title="后退"><i class="fa fa-arrow-left"></i></button>
      <button class="toolbar-btn" @click="goForward" title="前进"><i class="fa fa-arrow-right"></i></button>
      <button class="toolbar-btn" @click="refresh" title="刷新"><i class="fa fa-refresh"></i></button>
      <input 
        class="address-bar" 
        v-model="inputValue" 
        @keyup.enter="navigate"
        placeholder="输入网址或搜索..."
      />
    </div>
    <div class="browser-content">
      <iframe :src="currentUrl" ref="iframeRef" frameborder="0" class="browser-iframe"></iframe>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  url: {
    type: String,
    default: 'https://duckduckgo.com'
  }
})

const inputValue = ref(props.url)
const currentUrl = ref(props.url)
const iframeRef = ref<HTMLIFrameElement | null>(null)

const navigate = () => {
  let url = inputValue.value
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url
  }
  currentUrl.value = url
  inputValue.value = url
}

const goBack = () => {
  // 注意：由于跨域等浏览器安全策略，直接操作iframe的history会有一定限制
  console.log('浏览器后退按钮被点击')
}

const goForward = () => {
  console.log('浏览器前进按钮被点击')
}

const refresh = () => {
  if (iframeRef.value) {
    iframeRef.value.src = String(iframeRef.value.src)
  }
}
</script>

<style scoped>
.browser-app {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: #f5f5f5;
}
.browser-toolbar {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #e0e0e0;
  border-bottom: 1px solid #ccc;
  gap: 8px;
}
.toolbar-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 4px;
  color: #333;
  transition: background 0.2s;
}
.toolbar-btn:hover {
  background: #cfcfcf;
}
.address-bar {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
  font-size: 13px;
  transition: all 0.2s;
}
.address-bar:focus {
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}
.browser-content {
  flex: 1;
  position: relative;
}
.browser-iframe {
  width: 100%;
  height: 100%;
  background: white;
  display: block;
}
</style>