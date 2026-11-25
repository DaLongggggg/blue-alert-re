<script setup>
import { computed } from 'vue'
import GameBadge from './GameBadge.vue'

const props = defineProps({
  /** 作品标识数组，如 ['g1', 'g2']；按固定白名单顺序展示 */
  games: { type: Array, required: true }
})

// 白名单顺序：g1 在前，g2 在后
const GAME_ORDER = ['g1', 'g2']

const ordered = computed(() => {
  const seen = new Set()
  const result = []
  for (const gid of GAME_ORDER) {
    if (props.games.includes(gid) && !seen.has(gid)) {
      seen.add(gid)
      result.push(gid)
    }
  }
  // 白名单之外的值附加在后面
  for (const gid of props.games) {
    if (!seen.has(gid)) {
      seen.add(gid)
      result.push(gid)
    }
  }
  return result
})
</script>

<template>
  <span class="game-badges">
    <GameBadge v-for="gid in ordered" :key="gid" :game="gid" />
  </span>
</template>

<style scoped>
.game-badges {
  display: inline-flex;
  gap: 0.35em;
  flex-wrap: wrap;
  align-items: center;
}
</style>
