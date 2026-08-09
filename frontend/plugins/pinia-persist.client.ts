// Register pinia-plugin-persistedstate for localStorage persistence
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

export default defineNuxtPlugin(({ $pinia }) => {
  $pinia.use(piniaPluginPersistedstate);
});
