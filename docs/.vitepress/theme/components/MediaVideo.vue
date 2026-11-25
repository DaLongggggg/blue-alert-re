<script setup>
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

const props = defineProps({
  /** 站点根相对路径，如 /media/movies/mi-g1.mp4 */
  src: { type: String, default: '' },
  /** 封面图站点根相对路径（可选）；影片缺失时用它代替占位 */
  poster: { type: String, default: '' },
  /** 构建期已知文件缺失时置 true，直接渲染封面/占位 */
  missing: { type: Boolean, default: false },
  ratio: { type: String, default: '16 / 9' }
})

const failed = ref(false)
const absent = computed(() => props.missing === true || !props.src)
const shown = computed(() => absent.value === true || failed.value === true)
const hasPoster = computed(() => props.poster !== '')
</script>

<template>
  <figure class="media-video">
    <video
      v-if="shown === false"
      class="media-video__video"
      :src="withBase(src)"
      :poster="poster ? withBase(poster) : undefined"
      controls
      preload="metadata"
      playsinline
      :style="{ aspectRatio: ratio }"
      @error="failed = true"
    ></video>
    <template v-else-if="hasPoster === true">
      <!-- 线上只有封面：mp4 按方案不入 git，缺失/加载失败时显示封面图并注明 -->
      <img
        class="media-video__video"
        :src="withBase(poster)"
        alt="影片封面（影片文件未随站点发布）"
        loading="lazy"
        decoding="async"
        :style="{ aspectRatio: ratio, objectFit: 'cover' }"
      />
      <figcaption class="media-video__note">
        影片未随站点发布（体积原因），此处显示封面；可用 <code>tools/extract_media.py</code>
        从你自己的游戏目录生成影片。
      </figcaption>
    </template>
    <span v-else class="media-placeholder" :style="{ aspectRatio: ratio }">
      <span class="media-placeholder__icon">🎬</span>
      <span class="media-placeholder__text">影片素材未随站点发布</span>
      <code v-if="src" class="media-placeholder__path">{{ src }}</code>
    </span>
  </figure>
</template>

<style scoped>
.media-video__note {
  margin-top: 4px;
  font-size: 13px;
  color: var(--vp-c-text-3);
}

.media-video__note code {
  font-size: 12px;
}
</style>
