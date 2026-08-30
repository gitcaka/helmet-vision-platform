/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins";

// Components
import App from "./App.vue";
import "./styles/main.scss";
import { router } from "./router";
import { pinia } from "./stores";

// Composables
import { createApp } from "vue";

const app = createApp(App);

registerPlugins(app);
app.use(pinia);
app.use(router);
app.mount("#app");
