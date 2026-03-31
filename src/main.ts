/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins";

// Components
import App from "./App.vue";
import { router } from "./router";

// Composables
import { createApp } from "vue";
import { createPinia } from "pinia";
import VueApexCharts from "vue3-apexcharts";
import VueTablerIcons from 'vue-tabler-icons';


const pinia = createPinia();
const app = createApp(App);

registerPlugins(app);
app.use(router);
app.use(VueTablerIcons);
app.use(VueApexCharts);
app.use(pinia);
app.mount("#app");
