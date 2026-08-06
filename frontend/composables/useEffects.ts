// Unified effects composable for homepage animations
export function useEffects() {
  const scrollProgress = ref(0)
  const windForce = ref(0)
  const windDirection = ref(1)
  const isActive = ref(true)

  let rafId: number | null = null
  const effects: ((time: number) => void)[] = []

  function updateWind(time: number) {
    windForce.value = (Math.sin(time * 0.0003) + 1) * 0.5
    windDirection.value = Math.sin(time * 0.0005) > 0 ? 1 : -1
  }

  function updateScroll() {
    if (import.meta.client) {
      scrollProgress.value = Math.min(window.scrollY / window.innerHeight, 1)
    }
  }

  function registerEffect(fn: (time: number) => void) {
    effects.push(fn)
  }

  function startLoop() {
    if (!import.meta.client) return
    function loop(time: number) {
      if (!isActive.value) return
      updateWind(time)
      effects.forEach(fn => fn(time))
      rafId = requestAnimationFrame(loop)
    }
    rafId = requestAnimationFrame(loop)
    window.addEventListener('scroll', updateScroll)
  }

  function stopLoop() {
    if (rafId) cancelAnimationFrame(rafId)
    window.removeEventListener('scroll', updateScroll)
  }

  onMounted(() => { startLoop() })
  onUnmounted(() => { stopLoop() })

  return { scrollProgress, windForce, windDirection, registerEffect, isActive }
}