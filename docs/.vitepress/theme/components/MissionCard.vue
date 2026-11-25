<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'
import missions from '../../../../data/missions.json'
import GameBadges from './GameBadges.vue'

const props = defineProps({
  /** 任务 id，如 g1-m01 */
  id: { type: String, required: true }
})

// 白名单：任务类型标签
const TYPE_LABELS = { campaign: '战役任务', tutorial: '教学任务', network: '联机地图' }

const mission = computed(() => missions.find((m) => m && m.id === props.id))

// 站点标题约定（与 tools/build-content.mjs 的 missionPageTitle、config.ts 的 missionLabel 一致）：
// 战役关 = 第 NN 关 · 战场：XX（NN 取 order）；联机图 = 中文名或 slug；教程 = 教学模式
function missionTitle(m) {
  if (!m) return props.id
  if (m.type === 'tutorial') return '教学模式'
  if (m.type === 'network') return String(m.title || m.code || m.id)
  let head
  if (m.order != null) head = '第 ' + String(m.order).padStart(2, '0') + ' 关'
  else if (m.code) head = '关卡 ' + String(m.code)
  else head = String(m.id)
  if (m.opponent) head += ' · 战场：' + String(m.opponent)
  return head
}

const title = computed(() => missionTitle(mission.value))

const meta = computed(() => {
  const m = mission.value || {}
  const rows = []
  if (TYPE_LABELS[m.type]) rows.push(['类型', TYPE_LABELS[m.type]])
  if (m.difficulty != null && m.difficulty !== '') {
    // g1 简报原文「难度等级: N」；g2 原文「难度等级 : N / 10」
    const d = String(m.difficulty)
    rows.push(['难度', m.game === 'g2' ? d + ' / 10' : d])
  }
  // 数据里的 opponent 字段是简报的「战场：」行，展示为「战场」而非「对手」
  if (m.opponent) rows.push(['战场', String(m.opponent)])
  return rows
})

const objectiveText = computed(() => {
  const o = mission.value?.objective
  if (Array.isArray(o)) return String(o[0] ?? '')
  if (typeof o === 'string') return o
  return ''
})
</script>

<template>
  <a v-if="mission" class="mission-card mission-card--link" :href="withBase('/missions/' + mission.id + '/')">
    <div class="mission-card__head">
      <GameBadges :games="mission.games || []" />
      <span v-if="TYPE_LABELS[mission.type]" class="mission-card__type">{{ TYPE_LABELS[mission.type] }}</span>
    </div>
    <p class="mission-card__title">{{ title }}</p>
    <div v-if="meta.length > 0" class="mission-card__meta">
      <div v-for="row in meta" :key="row[0]" class="mission-card__meta-row">
        <span class="mission-card__meta-key">{{ row[0] }}</span>
        <span class="mission-card__meta-value">{{ row[1] }}</span>
      </div>
    </div>
    <p v-if="objectiveText" class="mission-card__objective">{{ objectiveText }}</p>
  </a>
  <span v-else class="mission-card mission-card--missing">任务 {{ id }} 数据缺失</span>
</template>

<style scoped>
/* 双写类名提升优先级，覆盖 .vp-doc 内的默认链接样式 */
.mission-card.mission-card--link {
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

.mission-card.mission-card--link:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 2px 12px var(--vp-c-brand-soft);
  transform: translateY(-1px);
}

.mission-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.mission-card__type {
  font-size: 12px;
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0 8px;
  line-height: 1.7;
}

.mission-card__title {
  margin: 8px 0 4px;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}

.mission-card__meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 0;
  font-size: 13px;
}

.mission-card__meta-row {
  display: flex;
  gap: 8px;
}

.mission-card__meta-key {
  color: var(--vp-c-text-3);
  flex: 0 0 3em;
}

.mission-card__meta-value {
  color: var(--vp-c-text-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mission-card__objective {
  margin: 8px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-2);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mission-card--missing {
  display: block;
  padding: 12px;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 10px;
  color: var(--vp-c-text-3);
  font-size: 13px;
}
</style>
