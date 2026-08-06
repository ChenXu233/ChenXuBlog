import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router/index.ts";
import "./style.css";
import "font-awesome/css/font-awesome.min.css";
import App from "./App.vue";
import LiquidGlass from "./components/LiquidGlass.vue";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.component("LiquidGlass", LiquidGlass);
app.mount("#app");
