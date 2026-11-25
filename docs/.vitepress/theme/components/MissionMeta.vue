<script setup>
import { computed } from 'vue'
import missions from '../../../../data/missions.json'

const props = defineProps({
  /** 任务 id，如 g1-m01 */
  id: { type: String, required: true }
})

const TYPE_LABELS = { campaign: '战役任务', tutorial: '教学任务', network: '联机地图' }

const mission = computed(() => missions.find((m) => m && m.id === props.id) || null)

// 信息条按数据里的实际值如实展示；缺的字段不显示（不编造）。
// 「战场」即游戏简报里的「战场：」行（数据里的 opponent 字段），不得标成「对手」。
const rows = computed(() => {
  const m = mission.value
  if (!m) return []
  const rows = []
  if (TYPE_LABELS[m.type]) rows.push(['类型', TYPE_LABELS[m.type]])
  if (m.code) rows.push([m.type === 'network' ? '地图编号' : '关卡文件', String(m.code)])
  if (m.baseCode) rows.push(['基地代号', String(m.baseCode)])
  if (m.expectedNo != null && m.expectedNo !== '') {
    rows.push(['领土', String(m.expectedNo).padStart(2, '0')])
  }
  if (m.difficulty != null && m.difficulty !== '') {
    // g1 简报原文「难度等级: N」；g2 原文「难度等级 : N / 10」
    const d = String(m.difficulty)
    rows.push(['难度', m.game === 'g2' ? d + ' / 10' : d])
  }
  if (m.opponent) rows.push(['战场', String(m.opponent)])
  return rows
})
</script>

<template>
  <p v-if="rows.length > 0" class="page-meta mission-meta">
    <span v-for="row in rows" :key="row[0]" class="mission-meta__item">
      <span class="mission-meta__key">{{ row[0] }}</span>
      <span class="mission-meta__value">{{ row[1] }}</span>
    </span>
  </p>
</template>

<style scoped>
.mission-meta.mission-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 18px;
}

.mission-meta__item {
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
  white-space: nowrap;
}

.mission-meta__key {
  color: var(--vp-c-text-3);
  font-size: 13px;
}

.mission-meta__value {
  color: var(--vp-c-text-1);
  font-weight: 600;
  font-size: 14px;
}
</style>
