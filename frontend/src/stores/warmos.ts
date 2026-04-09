import { ref, shallowRef } from 'vue'

export interface AppConfig {
  id: string
  title: string
  icon: string
  type: 'iframe' | 'component'
  url?: string
  component?: any
  props?: any
  defaultWidth?: number
  defaultHeight?: number
  defaultX?: number
  defaultY?: number
  minimized?: boolean
}

export const openApps = shallowRef<AppConfig[]>([])
export const activeAppId = ref<string | null>(null)
export const zIndexCounter = ref(10)
export const appZIndices = ref<Record<string, number>>({})

export const focusApp = (id: string) => {
  activeAppId.value = id
  zIndexCounter.value++
  appZIndices.value[id] = zIndexCounter.value
}

export const getBaseZIndex = (id: string) => {
  return appZIndices.value[id] || 10
}

export const openApp = (appConfig: AppConfig) => {
  const existingApp = openApps.value.find(app => app.id === appConfig.id)

  if (existingApp) {
    existingApp.minimized = false
    focusApp(existingApp.id)
  } else {
    const newApp = { ...appConfig, minimized: false, id: `${appConfig.id}-${Date.now()}` }
    openApps.value = [...openApps.value, newApp]
    focusApp(newApp.id)
  }
}

export const closeApp = (id: string) => {
  openApps.value = openApps.value.filter(app => app.id !== id)
  if (activeAppId.value === id) {
    activeAppId.value = null
  }
}

export const minimizeApp = (id: string) => {
  openApps.value = openApps.value.map(app =>
    app.id === id ? { ...app, minimized: true } : app
  )
  if (activeAppId.value === id) {
    activeAppId.value = null
  }
}

export const toggleAppVisibility = (app: AppConfig) => {
  if (app.minimized) {
    openApps.value = openApps.value.map(a =>
      a.id === app.id ? { ...a, minimized: false } : a
    )
    focusApp(app.id)
  } else if (activeAppId.value === app.id) {
    minimizeApp(app.id)
  } else {
    focusApp(app.id)
  }
}
