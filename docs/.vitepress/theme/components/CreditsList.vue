<script setup>
import { computed } from 'vue'
import credits from '../../../../data/credits.json'
import GameBadges from './GameBadges.vue'

// 第 5 组（汉化人员）在游戏内没有分组标题（title=null），
// 「汉化人员」为站点自定的展示标题，页面上需注明。
const UNTITLED_LABEL = '汉化人员'

const sections = computed(() => (Array.isArray(credits.sections) === true ? credits.sections : []))
</script>

<template>
  <div class="credits-list">
    <section v-for="(sec, i) in sections" :key="i" class="credits-list__section">
      <h3 class="credits-list__title">
        <span v-if="sec.title">{{ sec.title }}</span>
        <span v-else>{{ UNTITLED_LABEL }}</span>
        <GameBadges :games="sec.games || []" />
      </h3>
      <p v-if="!sec.title" class="credits-list__note">
        分组标题为站点所加，原文无标题（在游戏内名单中以分隔标记与上方各组区隔）。
      </p>
      <ul class="credits-list__people">
        <li v-for="(p, j) in sec.people" :key="j">{{ p }}</li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.credits-list__section {
  margin: 1.5rem 0;
  padding: 14px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
}

.credits-list__title {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin: 0 0 8px;
  font-size: 16px;
  line-height: 1.6;
}

.credits-list__note {
  margin: 0 0 8px;
  font-size: 13px;
  color: var(--vp-c-text-3);
}

.credits-list__people {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 2px 16px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  color: var(--vp-c-text-1);
}

.credits-list__people li {
  padding: 2px 0;
}
</style>
