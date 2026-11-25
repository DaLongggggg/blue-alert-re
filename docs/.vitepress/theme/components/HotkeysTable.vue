<script setup>
import hotkeys from '../../../../data/hotkeys.json'

// 出处字段里标注了两节表述有出入的条目（如数字键 * / -），表格中单独提示
function isDivergent(h) {
  return typeof h.source === 'string' && h.source.indexOf('出入') !== -1
}
</script>

<template>
  <div class="hk">
    <div class="hk__scroll">
      <table class="hk__table">
        <thead>
          <tr>
            <th>操作</th>
            <th>热键</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(h, i) in hotkeys" :key="i">
            <td>{{ h.action }}</td>
            <td><code class="hk__key">{{ h.keys }}</code></td>
            <td class="hk__note">
              <template v-if="isDivergent(h)">说明书两节表述略有出入，原样收录</template>
              <template v-else>—</template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p class="hk__src">
      共 {{ hotkeys.length }} 条，两作相同（games 均为第一部+第二部）。
      出自说明书「游戏热键设置」节，部分条目另见于「提示和诀窍」节（原文作「决窍」）。
    </p>
  </div>
</template>

<style scoped>
.hk {
  margin: 1rem 0;
}

.hk__scroll {
  overflow-x: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
}

.hk__table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 14px;
}

.hk__table th,
.hk__table td {
  padding: 7px 14px;
  border-bottom: 1px solid var(--vp-c-divider);
  text-align: left;
  white-space: nowrap;
}

.hk__table th {
  background: var(--vp-c-bg-soft);
  font-size: 13px;
  color: var(--vp-c-text-2);
}

.hk__table tr:last-child td {
  border-bottom: none;
}

.hk__key {
  display: inline-block;
  padding: 1px 8px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  font-size: 12.5px;
  white-space: nowrap;
}

.hk__note {
  color: var(--vp-c-text-3);
  font-size: 12.5px;
}

.hk__src {
  margin: 8px 2px 0;
  font-size: 12.5px;
  color: var(--vp-c-text-3);
}
</style>
