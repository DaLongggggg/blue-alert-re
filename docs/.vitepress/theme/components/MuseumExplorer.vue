<script setup>
import { computed, ref } from 'vue'
import missions from '../../../../data/missions.json'
import MissionCard from './MissionCard.vue'

const q = ref('')
const game = ref('all')
const type = ref('all')

// 白名单：作品与任务类型选项
const GAME_OPTIONS = [
  { value: 'all', label: '全部作品' },
  { value: 'g1', label: '第一部' },
  { value: 'g2', label: '第二部' }
]
const TYPE_OPTIONS = [
  { value: 'all', label: '全部类型' },
  { value: 'campaign', label: '战役任务' },
  { value: 'tutorial', label: '教学任务' },
  { value: 'network', label: '联机地图' }
]

// 排序约定（与 research/validate_data.py 一致）：g1→g2→g12（game 字段分组，教程 g12-m00 归 g1 组）、
// 组内 campaign→tutorial→network、order 升序
const GAME_ORDER = { g1: 0, g2: 1 }
const TYPE_ORDER = { campaign: 0, tutorial: 1, network: 2 }

function orderedByConvention(items) {
  return items
    .map((m) => ({
      m,
      key: [
        GAME_ORDER[m.game === 'g2' ? 'g2' : 'g1'] ?? 9,
        TYPE_ORDER[m.type] ?? 9,
        typeof m?.order === 'number' ? m.order : 1e9
      ]
    }))
    .sort((a, b) => a.key[0] - b.key[0] || a.key[1] - b.key[1] || a.key[2] - b.key[2])
    .map((e) => e.m)
}

const filtered = computed(() => {
  const needle = q.value.trim().toLowerCase()
  const result = []
  for (const m of missions) {
    if (!m || !m.id) continue
    if (game.value !== 'all' && Array.isArray(m.games) && m.games.includes(game.value) === false) continue
    if (type.value !== 'all' && m.type !== type.value) continue
    if (needle) {
      // 可搜：编号、中文名、id、战场（opponent 字段）、基地代号
      const hay = [m.code, m.title, m.id, m.opponent, m.baseCode].filter(Boolean).join(' ').toLowerCase()
      if (hay.includes(needle) === false) continue
    }
    result.push(m)
  }
  return orderedByConvention(result)
})
</script>

<template>
  <div class="explorer">
    <div class="explorer__bar">
      <input v-model="q" type="search" placeholder="搜索任务名称 / 编号…" aria-label="搜索任务" />
      <select v-model="game" aria-label="按作品筛选">
        <option v-for="opt in GAME_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
      <select v-model="type" aria-label="按类型筛选">
        <option v-for="opt in TYPE_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
    <p class="explorer__count">共 {{ filtered.length }} 个任务</p>
    <div v-if="filtered.length > 0" class="explorer__grid">
      <MissionCard v-for="m in filtered" :key="m.id" :id="m.id" />
    </div>
    <p v-else class="explorer__empty">暂无任务数据（编写中，等待资料整理入库）。</p>
  </div>
</template>
