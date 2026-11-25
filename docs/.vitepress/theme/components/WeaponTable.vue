<script setup>
import { computed } from 'vue'
import { withBase } from 'vitepress'
import units from '../../../../data/units.json'

// 武器名表条目（units.json 中 group=weapon 的 25 条英文原名，游戏内未汉化）
const weapons = computed(() =>
  units
    .filter((u) => u && u.id && u.group === 'weapon')
    .slice()
    .sort((a, b) => String(a.id).localeCompare(String(b.id)))
)
</script>

<template>
  <div class="wt">
    <p class="wt__count">共 {{ weapons.length }} 个条目，点击可查看对应收录页（含数据来源）。</p>
    <div class="wt__grid">
      <a v-for="w in weapons" :key="w.id" class="wt__item" :href="withBase('/units/' + w.id + '/')">
        <code class="wt__name">{{ w.name }}</code>
      </a>
    </div>
  </div>
</template>

<style scoped>
.wt {
  margin: 1rem 0;
}

.wt__count {
  margin: 0 0 10px;
  font-size: 13px;
  color: var(--vp-c-text-2);
}

.wt__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 8px;
}

.wt__item {
  display: block;
  padding: 7px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1) !important;
  text-decoration: none !important;
  font-weight: 400;
  transition: border-color 0.15s;
}

.wt__item:hover {
  border-color: var(--vp-c-brand-1);
}

.wt__name {
  font-size: 13px;
  background: none;
  padding: 0;
  white-space: nowrap;
}
</style>
