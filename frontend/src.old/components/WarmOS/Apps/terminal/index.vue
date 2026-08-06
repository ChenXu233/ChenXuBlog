<template>
  <div class="terminal-app" @click="focusInput">
    <div class="terminal-output" ref="outputContainer">
      <div v-for="(line, index) in output" :key="index" :class="['terminal-line', line.type]">
        <span v-if="line.type === 'input'" class="prompt">{{ prompt }}</span>
        <span class="text">{{ line.text }}</span>
      </div>
      <div class="terminal-input-line">
        <span class="prompt">{{ prompt }}</span>
        <input 
          ref="inputRef"
          v-model="currentCommand"
          @keydown.enter="handleCommand"
          @keydown.up.prevent="historyUp"
          @keydown.down.prevent="historyDown"
          class="terminal-input"
          type="text"
          spellcheck="false"
          autocomplete="off"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

const prompt = 'admin@warm-os:~$ '
const currentCommand = ref('')
const inputRef = ref<HTMLInputElement | null>(null)
const outputContainer = ref<HTMLDivElement | null>(null)

interface LogLine {
  text: string
  type: 'input' | 'output' | 'error' | 'system'
}

const output = ref<LogLine[]>([
  { text: 'Welcome to WarmOS Terminal (v1.0.0)', type: 'system' },
  { text: 'Type "help" to see available commands.', type: 'system' }
])

const commandHistory = ref<string[]>([])
const historyIndex = ref(-1)

const focusInput = () => {
  inputRef.value?.focus()
}

onMounted(() => {
  focusInput()
})

const scrollToBottom = async () => {
  await nextTick()
  if (outputContainer.value) {
    outputContainer.value.scrollTop = outputContainer.value.scrollHeight
  }
}

const historyUp = () => {
  if (commandHistory.value.length === 0) return
  if (historyIndex.value < commandHistory.value.length - 1) {
    historyIndex.value++
    const cmd = commandHistory.value[commandHistory.value.length - 1 - historyIndex.value]
    currentCommand.value = cmd ?? ''
  }
}

const historyDown = () => {
  if (historyIndex.value > 0) {
    historyIndex.value--
    const cmd = commandHistory.value[commandHistory.value.length - 1 - historyIndex.value]
    currentCommand.value = cmd ?? ''
  } else if (historyIndex.value === 0) {
    historyIndex.value = -1
    currentCommand.value = ''
  }
}

const handleCommand = () => {
  const cmd = currentCommand.value.trim()
  if (!cmd) return

  output.value.push({ text: cmd, type: 'input' })
  commandHistory.value.push(cmd)
  historyIndex.value = -1

  const parts = cmd.split(' ').filter(Boolean)
  const mainCmd = parts[0]?.toLowerCase() ?? ''

  switch (mainCmd) {
    case 'help':
      output.value.push({ text: 'Available commands: help, clear, echo, date, whoami', type: 'output' })
      break
    case 'clear':
      output.value = []
      break
    case 'echo':
      output.value.push({ text: parts.slice(1).join(' '), type: 'output' })
      break
    case 'date':
      output.value.push({ text: new Date().toString(), type: 'output' })
      break
    case 'whoami':
      output.value.push({ text: 'admin', type: 'output' })
      break
    default:
      output.value.push({ text: `Command not found: ${mainCmd}`, type: 'error' })
  }

  currentCommand.value = ''
  scrollToBottom()
}
</script>

<style scoped>
.terminal-app {
  width: 100%;
  height: 100%;
  background: rgba(30, 30, 30, 0.98);
  color: #d4d4d4;
  font-family: 'Consolas', 'Courier New', monospace;
  padding: 10px;
  overflow-y: auto;
  box-sizing: border-box;
  font-size: 14px;
}

.terminal-output {
  display: flex;
  flex-direction: column;
}

.terminal-line {
  margin-bottom: 4px;
  word-wrap: break-word;
  white-space: pre-wrap;
  line-height: 1.4;
}

.terminal-line.error .text {
  color: #f44336;
}

.terminal-line.system .text {
  color: #4caf50;
}

.terminal-line.output .text {
  color: #cccccc;
}

.prompt {
  color: #2196f3;
  margin-right: 8px;
  user-select: none;
}

.terminal-input-line {
  display: flex;
  align-items: center;
  margin-top: 4px;
}

.terminal-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #d4d4d4;
  font-family: inherit;
  font-size: inherit;
  outline: none;
  caret-color: #d4d4d4;
}
</style>