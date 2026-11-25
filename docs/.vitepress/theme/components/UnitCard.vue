<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'
import units from '../../../../data/units.json'
import GameBadges from './GameBadges.vue'
import MediaImage from './MediaImage.vue'

const props = defineProps({
  /** 单位 id，如 u-001 */
  id: { type: String, required: true }
})

// 白名单：单位分类标签
const CATEGORY_LABELS = {
  building: '建筑',
  factory: '工厂',
  defense: '防御',
  land: '地面',
  air: '空中',
  superweapon: '超级武器',
  other: '其他'
}

const unit = computed(() => units.find((u) => u && u.id === props.id))
const galleryCount = computed(() => {
  const g = unit.value && unit.value.gallery
  const extra = Array.isArray(g) === true ? g.length : 0
  return unit.value && unit.value.image ? extra + 1 : extra
})
</script>

<template>
  <a v-if="unit" class="unit-card unit-card--link" :href="withBase('/units/' + unit.id + '/')">
    <!-- 无图时不再渲染占位框：紧凑卡片直接从文字主体开始 -->
    <MediaImage
      v-if="unit.image"
      class="unit-card__thumb"
      :src="unit.image"
      :alt="String(unit.name || unit.id)"
      ratio="4 / 3"
      compact
      pixelated
    />
    <div class="unit-card__body">
      <div class="unit-card__head">
        <GameBadges :games="unit.games || []" />
        <span v-if="unit.category" class="unit-card__cat">{{ CATEGORY_LABELS[unit.category] || unit.category }}</span>
      </div>
      <p class="unit-card__title">{{ unit.name || unit.id }}</p>
      <p v-if="unit.nameEn" class="unit-card__en">{{ unit.nameEn }}</p>
      <p v-if="unit.summary" class="unit-card__summary">{{ unit.summary }}</p>
      <p v-if="galleryCount > 1" class="unit-card__gal">🖼 {{ galleryCount }} 张图</p>
    </div>
  </a>
  <span v-else class="unit-card unit-card--missing">单位 {{ id }} 数据缺失</span>
</template>

<style scoped>
/* 双写类名提升优先级，覆盖 .vp-doc 内的默认链接样式 */
.unit-card.unit-card--link {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1) !important;
  text-decoration: none !important;
  font-weight: 400;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

.unit-card.unit-card--link:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 2px 12px var(--vp-c-brand-soft);
  transform: translateY(-1px);
}

.unit-card__thumb {
  border-bottom: 1px solid var(--vp-c-divider);
  border-radius: 0;
}

/* 缩略图展台：透明精灵在深底上更接近游戏内观感 */
.unit-card__thumb :deep(.media-image__img) {
  background:
    linear-gradient(rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0)),
    #131a26;
}

.unit-card__body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 10px 12px 12px;
}

.unit-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.unit-card__cat {
  font-size: 12px;
  color: var(--vp-c-text-2);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0 8px;
  line-height: 1.7;
}

.unit-card__title {
  margin: 6px 0 0;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.4;
}

.unit-card__en {
  margin: 0;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.unit-card__summary {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-2);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.unit-card__gal {
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.unit-card--missing {
  display: block;
  padding: 12px;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 10px;
  color: var(--vp-c-text-3);
  font-size: 13px;
}
</style>
