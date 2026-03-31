import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const AuthRoutes = {
  path: "/auth",
  component: () => import("@/views/BlankLayout.vue"),
  meta: {
    requiresAuth: false,
  },
  children: [
    {
      name: "Login",
      path: "/login",
      component: () => import("@/views/Login.vue"),
    },
    {
      name: "Register",
      path: "/register",
      component: () => import("@/views/Register.vue"),
    },
    {
      name: "Error 404",
      path: "/error",
      component: () => import("@/views/Error404.vue"),
    },
  ],
};

const MainRoutes = {
  path: "/main",
  meta: {
    requiresAuth: true,
  },
  redirect: "/Dashboard",
  component: () => import("@/views/FullLayout.vue"),
  children: [
    {
      name: "LandingPage",
      path: "/",
      component: () => import("@/views/Dashboard.vue"),
    },
    {
      name: "Dashboard",
      path: "/Dashboard",
      component: () => import("@/views/Dashboard.vue"),
    },
    {
      name: "Monitor",
      path: "/Monitor",
      component: () => import("@/views/Monitor.vue"),
    },
    {
      name: "Analysis",
      path: "/Analysis",
      component: () => import("@/views/Analysis.vue"),
    },
    {
      name: "History",
      path: "/History",
      component: () => import("@/views/History.vue"),
    },
    {
      name: "Member",
      path: "/Member",
      component: () => import("@/views/Member.vue"),
    }
  ],
};

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    MainRoutes,
    AuthRoutes,
    {
      path: "/:pathMatch(.*)*",
      component: () => import("@/views/Error404.vue"),
    },
  ],
});

interface User {
  // Define the properties and their types for the user data here
  // For example:
  id: number;
  name: string;
}

interface AuthStore {
  user: User | null;
  returnUrl: string | null;
  login(username: string, password: string): Promise<void>;
  logout(): void;
}

router.beforeEach(async (to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const auth: AuthStore = useAuthStore();

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (authRequired && !auth.user) {
      auth.returnUrl = to.fullPath;
      return next("/login");
    } else next();
  } else {
    next();
  }
});
