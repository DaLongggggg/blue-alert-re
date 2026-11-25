<script setup>
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

/**
 * 单位图集：主图（最近邻放大，深色展台）+ 可点击缩略图。
 * variant="grid" 时渲染为小图网格（新兵手册的界面图插页用）。
 */
const props = defineProps({
  /** 主图（站点根相对路径）；与 gallery 一起构成可切换的图集 */
  image: { type: String, default: '' },
  /** 主图说明（图注） */
  imageNote: { type: String, default: '' },
  alt: { type: String, default: '' },
  /** 额外图片：[{ image: '/media/units/…', label: '资料框绿色全息图' }] */
  gallery: { type: Array, default: () => [] },
  variant: { type: String, default: 'unit' }
})

const items = computed(() => {
  const list = []
  if (props.image) list.push({ image: props.image, label: props.imageNote })
  for (const g of props.gallery) {
    if (g && g.image && list.some((x) => x.image === g.image) === false) list.push(g)
  }
  return list
})
const current = ref(0)
const active = computed(() => items.value[current.value] ?? items.value[0] ?? null)

function hasText(v) {
  return typeof v === 'string' && v.trim() !== ''
}
</script>

<template>
  <div v-if="variant === 'grid' && items.length > 0" class="ugrid">
    <figure v-for="(it, i) in items" :key="it.image" class="ugrid__cell">
      <div class="ugrid__stage">
        <img :src="withBase(it.image)" :alt="alt + ' ' + (i + 1)" loading="lazy" decoding="async" />
      </div>
      <figcaption v-if="hasText(it.label)" class="ugrid__cap">{{ it.label }}</figcaption>
    </figure>
  </div>
  <figure v-else-if="active" class="ugal">
    <div class="ugal__stage">
      <img :key="active.image" class="ugal__img" :src="withBase(active.image)" :alt="alt" decoding="async" />
    </div>
    <figcaption v-if="hasText(active.label)" class="ugal__cap">{{ active.label }}</figcaption>
    <div v-if="items.length > 1" class="ugal__thumbs" role="tablist" aria-label="更多图片">
      <button
        v-for="(it, i) in items"
        :key="it.image"
        type="button"
        class="ugal__thumb"
        :class="{ 'ugal__thumb--on': i === current }"
        :aria-label="'查看第 ' + (i + 1) + ' 张：' + alt"
        @click="current = i"
      >
        <img :src="withBase(it.image)" alt="" loading="lazy" decoding="async" />
      </button>
    </div>
  </figure>
</template>

<style scoped>
/* 深色展台：精灵与绿色全息图都是透明 PNG，深底更接近游戏内观感 */
.ugal__stage,
.ugrid__stage {
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0)),
    #131a26;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 16px;
}

.ugal__img {
  height: 240px;
  width: auto;
  max-width: 100%;
  object-fit: contain;
  image-rendering: pixelated;
}

.ugal__cap,
.ugrid__cap {
  margin: 8px 2px 0;
  font-size: 12px;
  color: var(--vp-c-text-2);
  text-align: center;
}

.ugal__thumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.ugal__thumb {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 76px;
  height: 60px;
  padding: 4px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: #131a26;
  cursor: pointer;
  transition: border-color 0.15s;
}

.ugal__thumb img {
  max-width: 100%;
  max-height: 100%;
  image-rendering: pixelated;
}

.ugal__thumb:hover {
  border-color: var(--vp-c-brand-1);
}

.ugal__thumb--on {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 1px var(--vp-c-brand-1);
}

/* 网格变体：界面图插页 */
.ugrid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  margin: 1rem 0;
}

.ugrid__stage {
  padding: 10px;
}

.ugrid__stage img {
  max-height: 90px;
  max-width: 100%;
  width: auto;
  image-rendering: pixelated;
}
</style>
