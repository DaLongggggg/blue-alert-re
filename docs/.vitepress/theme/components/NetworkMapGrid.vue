<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'
import missions from '../../../../data/missions.json'
import GameBadges from './GameBadges.vue'

// 联机地图卡片网格：两作混排（g1 → g2，order 升序）。
// g1 的 8 张有官方中文名（title，出自 g1 说明书「多人游戏任务」节）；
// g2 的 6 张说明书没有联机章节，无官方中文名，标题如实显示文件名 slug。
const maps = computed(() => {
  const list = missions.filter((m) => m && m.type === 'network' && m.id)
  const gorder = { g1: 0, g2: 1 }
  return list
    .map((m) => ({
      m,
      key: [
        gorder[m.game === 'g2' ? 'g2' : 'g1'] ?? 9,
        typeof m.order === 'number' ? m.order : 1e9
      ]
    }))
    .sort((a, b) => a.key[0] - b.key[0] || a.key[1] - b.key[1])
    .map((e) => e.m)
})

function title(m) {
  return String(m.title || m.code || m.id)
}
</script>

<template>
  <div class="nm-grid">
    <a v-for="m in maps" :key="m.id" class="nm-card" :href="withBase('/missions/' + m.id + '/')">
      <div class="nm-card__head">
        <GameBadges :games="m.games || []" />
        <span class="nm-card__no">{{ typeof m.order === 'number' ? String(m.order).padStart(2, '0') : '--' }}</span>
      </div>
      <p class="nm-card__title">{{ title(m) }}</p>
      <p class="nm-card__slug">{{ m.title ? m.code : '（无官方中文名，标题为文件名 slug）' }}</p>
      <p v-if="m.briefing" class="nm-card__desc">{{ m.briefing }}</p>
      <p v-else class="nm-card__desc nm-card__desc--empty">说明书没有本图说明（g2 说明书无联机地图章节）。</p>
    </a>
  </div>
</template>

<style scoped>
.nm-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
  margin: 1.25rem 0;
}

.nm-card {
  display: block;
  margin: 0;
  padding: 12px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1) !important;
  text-decoration: none !important;
  font-weight: 400;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

.nm-card:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 2px 12px var(--vp-c-brand-soft);
  transform: translateY(-1px);
}

.nm-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.nm-card__no {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
}

.nm-card__title {
  margin: 8px 0 2px;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}

.nm-card__slug {
  margin: 0;
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono, monospace);
}

.nm-card__desc {
  margin: 8px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-2);
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.nm-card__desc--empty {
  color: var(--vp-c-text-3);
}
</style>
