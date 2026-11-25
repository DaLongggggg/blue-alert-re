<script setup>
import { computed } from 'vue'
import games from '../../../../data/games.json'

const props = defineProps({
  /** 作品标识：g1 | g2 */
  game: { type: String, required: true }
})

const info = computed(() => {
  const g = games[props.game]
  if (!g) return { label: props.game, mark: '', title: props.game, cls: 'game-badge--unknown' }
  return {
    label: String(g.label ?? props.game),
    mark: String(g.mark ?? ''),
    title: g.subtitle ? g.title + '（' + g.subtitle + '）' : String(g.title ?? ''),
    cls: 'game-badge--' + props.game
  }
})
</script>

<template>
  <span class="game-badge" :class="info.cls" :title="info.title">
    <span v-if="info.mark" class="game-badge__mark">{{ info.mark }}</span>
    <span class="game-badge__text">{{ info.label }}</span>
  </span>
</template>

<style scoped>
.game-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3em;
  padding: 0.05em 0.6em;
  border-radius: 999px;
  font-size: 0.82em;
  font-weight: 600;
  line-height: 1.6;
  vertical-align: middle;
  white-space: nowrap;
  border: 1px solid transparent;
}

.game-badge__mark {
  font-family: Georgia, 'Times New Roman', serif;
  font-weight: 700;
}

.game-badge--g1 {
  color: #1d5dc2;
  background: rgba(47, 111, 219, 0.12);
  border-color: rgba(47, 111, 219, 0.4);
}

.game-badge--g2 {
  color: #b2540e;
  background: rgba(224, 120, 32, 0.12);
  border-color: rgba(224, 120, 32, 0.4);
}

.game-badge--unknown {
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border-color: var(--vp-c-divider);
}

.dark .game-badge--g1 {
  color: #8ab6f8;
  background: rgba(106, 162, 247, 0.14);
  border-color: rgba(106, 162, 247, 0.42);
}

.dark .game-badge--g2 {
  color: #f0a568;
  background: rgba(240, 165, 104, 0.14);
  border-color: rgba(240, 165, 104, 0.42);
}
</style>
