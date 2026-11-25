<script setup>
import { computed, ref } from 'vue'
import units from '../../../../data/units.json'
import UnitCard from './UnitCard.vue'

const q = ref('')
const game = ref('all')
const category = ref('all')
const hasImage = ref('all')

// 白名单：作品与分类选项
const GAME_OPTIONS = [
  { value: 'all', label: '全部作品' },
  { value: 'g1', label: '第一部' },
  { value: 'g2', label: '第二部' }
]
const CATEGORY_OPTIONS = [
  { value: 'all', label: '全部分类' },
  { value: 'building', label: '建筑' },
  { value: 'factory', label: '工厂' },
  { value: 'defense', label: '防御' },
  { value: 'land', label: '地面单位' },
  { value: 'air', label: '空中单位' },
  { value: 'superweapon', label: '超级武器' },
  { value: 'other', label: '其他' }
]
const IMAGE_OPTIONS = [
  { value: 'all', label: '不限图片' },
  { value: 'with', label: '有图片' },
  { value: 'without', label: '无图片' }
]

// 稳定插入排序（按 u-001 这样的三位序号）
function orderedById(items) {
  const out = []
  for (const item of items) {
    const num = parseInt(String(item.id).replace(/^u-/, ''), 10)
    const key = Number.isNaN(num) === true ? 1e9 : num
    let i = 0
    while (i < out.length && out[i][1] <= key) i++
    out.splice(i, 0, [item, key])
  }
  return out.map((pair) => pair[0])
}

function imageCount(u) {
  const extra = Array.isArray(u.gallery) === true ? u.gallery.length : 0
  return (u.image ? 1 : 0) + extra
}

const filtered = computed(() => {
  const needle = q.value.trim().toLowerCase()
  const result = []
  for (const u of units) {
    if (!u || !u.id) continue
    if (game.value !== 'all' && Array.isArray(u.games) && u.games.includes(game.value) === false) continue
    if (category.value !== 'all' && u.category !== category.value) continue
    if (hasImage.value === 'with' && imageCount(u) === 0) continue
    if (hasImage.value === 'without' && imageCount(u) > 0) continue
    if (needle) {
      // 中英文关键字：名称（中/英）、id、一句话简介
      const hay = [u.name, u.nameEn, u.id, u.summary].filter(Boolean).join(' ').toLowerCase()
      if (hay.includes(needle) === false) continue
    }
    result.push(u)
  }
  return orderedById(result)
})

const withImageCount = computed(() => units.filter((u) => u && u.id && imageCount(u) > 0).length)
</script>

<template>
  <div class="explorer">
    <div class="explorer__bar">
      <input v-model="q" type="search" placeholder="搜索单位名称（中英文均可）…" aria-label="搜索单位" />
      <select v-model="game" aria-label="按作品筛选">
        <option v-for="opt in GAME_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
      <select v-model="category" aria-label="按分类筛选">
        <option v-for="opt in CATEGORY_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
      <select v-model="hasImage" aria-label="按是否有图片筛选">
        <option v-for="opt in IMAGE_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>
    <p class="explorer__count">共 {{ filtered.length }} 个条目（其中 {{ withImageCount }} 个有游戏内图像）</p>
    <div v-if="filtered.length > 0" class="explorer__grid">
      <UnitCard v-for="u in filtered" :key="u.id" :id="u.id" />
    </div>
    <p v-else class="explorer__empty">没有符合筛选条件的条目。</p>
  </div>
</template>
