<script setup>
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps({
  /** 站点根相对路径，如 /media/missions/g1-m01.jpg */
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  /** 构建期已知文件缺失时置 true，直接渲染占位 */
  missing: { type: Boolean, default: false },
  /** 占位框宽高比，如 "16 / 9"、"1" */
  ratio: { type: String, default: '16 / 9' },
  /** 紧凑模式（卡片缩略图用）：占位退化为一条细提示，不占大框 */
  compact: { type: Boolean, default: false },
  /** 像素图（游戏精灵）最近邻放大，保持硬边清晰 */
  pixelated: { type: Boolean, default: false }
})

const failed = ref(false)
const absent = computed(() => props.missing === true || !props.src)
const shown = computed(() => absent.value === true || failed.value === true)
</script>

<template>
  <figure class="media-image" :class="{ 'media-image--compact': compact }">
    <img
      v-if="shown === false"
      class="media-image__img"
      :class="{ 'media-image__img--pixelated': pixelated === true }"
      :src="withBase(src)"
      :alt="alt"
      loading="lazy"
      decoding="async"
      @error="failed = true"
    />
    <span
      v-else
      class="media-placeholder"
      :class="{ 'media-placeholder--compact': compact === true }"
      :style="compact === true ? undefined : { aspectRatio: ratio }"
    >
      <span class="media-placeholder__icon">🖼️</span>
      <span class="media-placeholder__text">素材未随站点发布</span>
      <code v-if="src && compact === false" class="media-placeholder__path">{{ src }}</code>
    </span>
  </figure>
</template>

<style scoped>
/* 像素精灵放大（UnitCard 缩略图 / 单位页主图用） */
.media-image__img--pixelated {
  image-rendering: pixelated;
}

/* 紧凑占位：一行细提示，不再渲染大占位框（避免列表/卡片里出现大空框） */
.media-placeholder--compact {
  flex-direction: row;
  gap: 6px;
  padding: 3px 8px;
  border-style: dashed;
  font-size: 11px;
}

.media-placeholder--compact .media-placeholder__icon {
  display: none;
}

.media-placeholder--compact .media-placeholder__text {
  font-weight: 400;
}
</style>
