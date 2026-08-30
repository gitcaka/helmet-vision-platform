<script setup lang="ts">
import Logo from "@/views/logo.vue";

defineProps<{
  eyebrow: string;
  title: string;
  subtitle: string;
}>();
</script>

<template>
  <main class="auth-shell">
    <div class="auth-orb auth-orb--one" />
    <div class="auth-orb auth-orb--two" />

    <section class="auth-hero">
      <div class="auth-brand">
        <Logo compact />
        <div>
          <strong>Helmet Vision</strong>
          <span>智能交通感知平台</span>
        </div>
      </div>

      <div class="auth-hero__content">
        <v-chip color="cyan-accent-2" variant="tonal" size="small" prepend-icon="mdi-radar">
          AI 视觉实时感知
        </v-chip>
        <h1>让每一次骑行<br />都被安全守护</h1>
        <p>融合实时视频、头盔识别与交通统计，为非机动车安全治理提供清晰、可靠的决策视图。</p>

        <div class="hero-features">
          <div><v-icon>mdi-video-outline</v-icon><span>多路视频监控</span></div>
          <div><v-icon>mdi-chart-box-outline</v-icon><span>实时趋势分析</span></div>
          <div><v-icon>mdi-shield-check-outline</v-icon><span>异常抓拍告警</span></div>
        </div>
      </div>

      <div class="auth-hero__footer">
        <span class="status-dot" />
        <span>系统运行正常</span>
        <span class="footer-divider" />
        <span>示例数据模式可用</span>
      </div>
    </section>

    <section class="auth-form-panel">
      <v-card class="auth-card" elevation="0">
        <div class="auth-card__mobile-brand"><Logo compact /></div>
        <div class="auth-card__eyebrow">{{ eyebrow }}</div>
        <h2>{{ title }}</h2>
        <p class="auth-card__subtitle">{{ subtitle }}</p>
        <slot />
      </v-card>
      <p class="auth-copyright">Helmet Vision · 智慧交通安全感知</p>
    </section>
  </main>
</template>

<style scoped lang="scss">
.auth-shell {
  position: relative;
  display: grid;
  grid-template-columns: minmax(460px, 1.08fr) minmax(480px, 0.92fr);
  min-height: 100vh;
  overflow: hidden;
  background: #f4f7fb;
}

.auth-hero {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 42px clamp(44px, 6vw, 92px);
  color: #fff;
  background:
    linear-gradient(145deg, rgba(10, 25, 62, 0.96), rgba(22, 55, 128, 0.9)),
    radial-gradient(circle at 72% 24%, rgba(22, 211, 238, 0.48), transparent 35%);
  isolation: isolate;
}

.auth-hero::before,
.auth-hero::after {
  position: absolute;
  z-index: -1;
  content: "";
  border: 1px solid rgba(98, 225, 255, 0.16);
  border-radius: 50%;
}

.auth-hero::before { width: 430px; height: 430px; right: -160px; top: 18%; }
.auth-hero::after { width: 260px; height: 260px; right: -70px; top: calc(18% + 85px); }

.auth-brand {
  display: flex;
  align-items: center;
  gap: 13px;
}

.auth-brand div { display: flex; flex-direction: column; }
.auth-brand strong { font-size: 17px; letter-spacing: 0.015em; }
.auth-brand span { color: rgba(226, 241, 255, 0.64); font-size: 11px; letter-spacing: 0.14em; }

.auth-hero__content {
  width: min(610px, 100%);
  margin: auto 0;
}

.auth-hero__content h1 {
  margin: 24px 0 20px;
  font-size: clamp(46px, 5vw, 72px);
  font-weight: 850;
  letter-spacing: -0.055em;
  line-height: 1.08;
}

.auth-hero__content p {
  max-width: 560px;
  margin: 0;
  color: rgba(226, 241, 255, 0.72);
  font-size: 16px;
  line-height: 1.85;
}

.hero-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 38px;
}

.hero-features div {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 14px 15px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.055);
  color: rgba(241, 249, 255, 0.84);
  font-size: 13px;
  backdrop-filter: blur(12px);
}

.hero-features .v-icon { color: #67e8f9; }

.auth-hero__footer {
  display: flex;
  align-items: center;
  gap: 9px;
  color: rgba(226, 241, 255, 0.6);
  font-size: 12px;
}

.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 0 5px rgba(52, 211, 153, 0.12); }
.footer-divider { width: 1px; height: 12px; margin: 0 6px; background: rgba(255, 255, 255, 0.2); }

.auth-form-panel {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 48px clamp(30px, 6vw, 88px);
}

.auth-card {
  width: min(460px, 100%);
  padding: clamp(28px, 4vw, 48px);
  border: 1px solid rgba(30, 55, 94, 0.08) !important;
  border-radius: 28px !important;
  background: rgba(255, 255, 255, 0.9) !important;
  box-shadow: 0 30px 80px rgba(23, 42, 81, 0.13) !important;
  backdrop-filter: blur(18px);
}

.auth-card__eyebrow { color: #3157f6; font-size: 12px; font-weight: 800; letter-spacing: 0.13em; text-transform: uppercase; }
.auth-card h2 { margin: 8px 0 10px; color: #12213f; font-size: 32px; font-weight: 800; letter-spacing: -0.035em; }
.auth-card__subtitle { margin: 0 0 24px; color: #718096; font-size: 14px; line-height: 1.65; }
.auth-card__mobile-brand { display: none; margin-bottom: 24px; }
.auth-copyright { margin: 22px 0 0; color: #94a3b8; font-size: 12px; }

.auth-orb { position: absolute; border-radius: 50%; filter: blur(1px); pointer-events: none; }
.auth-orb--one { width: 260px; height: 260px; right: 4%; top: -130px; background: rgba(49, 87, 246, 0.12); }
.auth-orb--two { width: 190px; height: 190px; right: -80px; bottom: -70px; background: rgba(8, 169, 196, 0.1); }

@media (max-width: 980px) {
  .auth-shell { grid-template-columns: 1fr; }
  .auth-hero { display: none; }
  .auth-form-panel { min-height: 100vh; padding: 28px 20px; }
  .auth-card__mobile-brand { display: block; }
}
</style>
