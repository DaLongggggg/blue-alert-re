<script setup>
import { withBase } from 'vitepress'
import MediaImage from './MediaImage.vue'

const props = defineProps({
  /** 站点根相对路径，如 /media/missions/m01-g1.jpg */
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  /** 构建期已知文件缺失时置 true，直接渲染占位（不提供放大链接） */
  missing: { type: Boolean, default: false },
  /** 占位框宽高比，如 "16 / 9"、"1" */
  ratio: { type: String, default: '16 / 9' }
})
</script>

<template>
  <a
    v-if="missing === false && src"
    class="media-zoom"
    :href="withBase(src)"
    target="_blank"
    rel="noopener"
    title="点击查看原图"
  >
    <MediaImage :src="src" :alt="alt" :ratio="ratio" />
    <span class="media-zoom__hint">点击查看原始分辨率 ↗</span>
  </a>
  <MediaImage v-else :src="src" :alt="alt" :missing="missing" :ratio="ratio" />
</template>

<style scoped>
.media-zoom {
  display: block;
  margin: 1rem 0;
  color: inherit !important;
  text-decoration: none !important;
  font-weight: 400;
}

.media-zoom:hover img,
.media-zoom:hover :deep(.media-image__img) {
  box-shadow: 0 2px 14px var(--vp-c-brand-soft);
}

.media-zoom__hint {
  display: inline-block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.media-zoom:hover .media-zoom__hint {
  color: var(--vp-c-brand-1);
}
</style>
