import { defineConfig } from 'vitepress'
import type { Plugin } from 'vite'
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

// docs/.vitepress/config.ts -> 仓库根目录
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
// 数据目录可用环境变量 DATA_DIR 覆盖（如测试时指向 data/examples），默认 data/
const DATA_DIR = process.env.DATA_DIR ? resolve(ROOT, process.env.DATA_DIR) : resolve(ROOT, 'data')
// base 默认 '/blue-alert-re/'，环境变量 BASE 可覆盖（本地整站预览时设 BASE=/）
const BASE = (() => {
  let b = process.env.BASE?.trim()
  if (!b) return '/blue-alert-re/'
  if (!b.startsWith('/')) b = '/' + b
  if (!b.endsWith('/')) b += '/'
  return b
})()

// docs/public 下的文件在构建期登记成一张「存在表」，以虚拟模块交给 MediaVideo：
// 手写页里的影片也能按文件是否存在降级（mp4 不入库，线上构建时自动改为封面）。
const PUBLIC_DIR = resolve(ROOT, 'docs/public')
const MEDIA_EXISTS_ID = 'virtual:media-exists'

function listPublicFiles(dir: string, out: string[] = []): string[] {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name)
    if (statSync(full).isDirectory()) listPublicFiles(full, out)
    else out.push('/' + relative(PUBLIC_DIR, full).split(sep).join('/'))
  }
  return out
}

function mediaExistsPlugin(): Plugin {
  const resolvedId = '\0' + MEDIA_EXISTS_ID
  return {
    name: 'blue-alert-re:media-exists',
    resolveId(id) {
      return id === MEDIA_EXISTS_ID ? resolvedId : null
    },
    load(id) {
      if (id !== resolvedId) return null
      let files: string[] = []
      try {
        files = listPublicFiles(PUBLIC_DIR)
      } catch {
        // docs/public 不存在时按「没有任何媒体」处理，组件自会渲染占位
      }
      return 'export const exists = new Set(' + JSON.stringify(files) + ')'
    }
  }
}

function parseJsonFile(file: string): any {
  try {
    return JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''))
  } catch (err: any) {
    console.warn('[vitepress] 数据文件读取失败: ' + String(err?.message ?? err))
    return null
  }
}

function readData(name: string): any {
  const primary = resolve(DATA_DIR, name)
  if (existsSync(primary) === true) return parseJsonFile(primary)
  return parseJsonFile(resolve(ROOT, 'data', name))
}

const _games = readData('games.json')
const _missions = readData('missions.json')
const _units = readData('units.json')

const GAMES: Record<string, any> = _games && typeof _games === 'object' ? _games : {}
const MISSIONS: any[] = Array.isArray(_missions) === true ? _missions : []
const UNITS: any[] = Array.isArray(_units) === true ? _units : []

const CATEGORY_LABELS: Record<string, string> = {
  building: '建筑',
  factory: '工厂',
  defense: '防御设施',
  land: '地面单位',
  air: '空中单位',
  superweapon: '超级武器',
  other: '其他'
}
// 白名单：分类与作品的合法键，分组与排序只使用这些固定键
const CATEGORY_ORDER = ['building', 'factory', 'defense', 'land', 'air', 'superweapon', 'other']
const GAME_ORDER = ['g1', 'g2']
const TYPE_LABELS: Record<string, string> = {
  campaign: '战役任务',
  tutorial: '教学任务',
  network: '联机地图'
}

function gameOrder(gameId: string): number {
  const idx = GAME_ORDER.indexOf(gameId)
  return idx === -1 ? GAME_ORDER.length : idx
}

// MiniSearch 中文分词：拉丁/数字按词，CJK 按单字 + 相邻二元组
function tokenize(text: string): string[] {
  const tokens: string[] = []
  const segments = text.match(/[\u3400-\u4dbf\u4e00-\u9fff]+|[a-zA-Z0-9_]+/g) ?? []
  for (const seg of segments) {
    if (/^[a-zA-Z0-9_]+$/.test(seg) === true) {
      tokens.push(seg.toLowerCase())
      continue
    }
    const chars = Array.from(seg)
    for (let i = 0; i < chars.length; i++) {
      tokens.push(chars[i])
      if (i + 1 < chars.length) tokens.push(chars[i] + chars[i + 1])
    }
  }
  return tokens
}

// 站点标题约定（与 tools/build-content.mjs 的 missionPageTitle、MissionCard.vue 一致）：
// 战役关 = 第 NN 关 · 战场：XX（NN 取 order 补零两位，XX 为战场字段）；
// 联机地图 = 官方中文名或文件名 slug；教程 = 教学模式
function missionLabel(m: any): string {
  if (!m) return ''
  if (m.type === 'tutorial') return '教学模式'
  if (m.type === 'network') return String(m.title || m.code || m.id)
  let head: string
  if (m.order != null) head = '第 ' + String(m.order).padStart(2, '0') + ' 关'
  else if (m.code) head = '关卡 ' + String(m.code)
  else head = String(m.id ?? '')
  if (m.opponent) head += ' · 战场：' + String(m.opponent)
  return head
}

// 稳定插入排序：按数值键升序（order 缺失视为排最后）
function orderedByNumber(items: { key: number }[]): any[] {
  const out: any[] = []
  for (const item of items) {
    let i = 0
    while (i < out.length && out[i].key <= item.key) i++
    out.splice(i, 0, item)
  }
  return out
}

function buildMuseumSidebar() {
  const base = [
    {
      text: '战役博物馆',
      collapsed: false,
      items: [
        { text: '博物馆首页', link: '/museum/' },
        { text: '任务列表', link: '/missions/' },
        { text: '剧情', link: '/museum/story' },
        { text: '制作名单', link: '/museum/credits' },
        { text: '联机地图', link: '/museum/network-maps' }
      ]
    }
  ]
  // 组内排序约定：campaign→tutorial→network，再按 order 升序（战役与联机图 order 各自从 1 计数，
  // 不能只按 order 混排，否则战役关与联机图会交错）
  const TYPE_ORDER: Record<string, number> = { campaign: 0, tutorial: 1, network: 2 }
  const keyed = MISSIONS.filter((m) => !!m?.id).map((m) => ({
    typeIdx: TYPE_ORDER[m.type] ?? 9,
    key: typeof m?.order === 'number' ? m.order : 1e9,
    text: missionLabel(m),
    link: '/missions/' + m.id + '/',
    gid: m.game === 'g2' ? 'g2' : 'g1'
  }))
  const ordered = keyed.sort((a, b) => a.typeIdx - b.typeIdx || a.key - b.key)
  // 分组只按白名单中的 g1/g2，两作徽标亦由此生成
  const gameSections = GAME_ORDER.filter((gid) => ordered.some((e) => e.gid === gid)).map((gid) => ({
    text: GAMES[gid] ? String(GAMES[gid].label) + ' · ' + String(GAMES[gid].title) : gid,
    collapsed: true,
    items: ordered
      .filter((e) => e.gid === gid)
      .map((e) => ({ text: e.text, link: e.link }))
  }))
  return base.concat(gameSections)
}

function buildUnitsSidebar() {
  const base = [
    {
      text: '单位图鉴',
      collapsed: false,
      items: [
        { text: '图鉴首页', link: '/units/' },
        { text: '新兵手册', link: '/units/manual' },
        { text: '武器一览', link: '/units/weapons' }
      ]
    }
  ]
  const sections = CATEGORY_ORDER.filter((cat) => UNITS.some((u) => u?.category === cat)).map(
    (cat) => ({
      text: CATEGORY_LABELS[cat],
      collapsed: true,
      items: orderedByNumber(
        UNITS.filter((u) => u?.category === cat && !!u?.id).map((u) => {
          const num = parseInt(String(u.id).replace(/^u-/, ''), 10)
          return { key: Number.isNaN(num) === true ? 1e9 : num, text: String(u.name || u.id), link: '/units/' + u.id + '/' }
        })
      ).map((e) => ({ text: e.text, link: e.link }))
    })
  )
  return base.concat(sections)
}

const museumSidebar = buildMuseumSidebar()
const unitsSidebar = buildUnitsSidebar()

export default defineConfig({
  lang: 'zh-CN',
  title: '蓝色警戒中文维基',
  description:
    '《蓝色警戒》(State of War, 2001) 与《蓝色警戒II：战争狂人》(Warmonger, 2003) 非营利粉丝资料维基：战役博物馆与单位图鉴。',
  base: BASE,
  head: [['meta', { name: 'theme-color', content: '#2f6fdb' }]],
  themeConfig: {
    siteTitle: '蓝色警戒中文维基',
    nav: [
      { text: '首页', link: '/' },
      {
        text: '战役博物馆',
        items: [
          { text: '博物馆首页', link: '/museum/' },
          { text: '任务列表', link: '/missions/' },
          { text: '剧情', link: '/museum/story' },
          { text: '制作名单', link: '/museum/credits' },
          { text: '联机地图', link: '/museum/network-maps' }
        ]
      },
      {
        text: '单位图鉴',
        items: [
          { text: '图鉴首页', link: '/units/' },
          { text: '新兵手册', link: '/units/manual' },
          { text: '武器一览', link: '/units/weapons' }
        ]
      },
      { text: '关于', link: '/about' }
    ],
    sidebar: {
      '/museum/': museumSidebar,
      '/missions/': museumSidebar,
      '/units/': unitsSidebar
    },
    footer: {
      message: '非营利粉丝资料站 · 数据来自玩家自有游戏文件的整理',
      copyright: '游戏版权归 Cypron Studios 及其发行商/汉化方所有'
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    search: {
      provider: 'local',
      options: {
        locale: 'zh-CN',
        translations: {
          button: { buttonText: '搜索资料', buttonAriaLabel: '搜索资料' },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清除查询条件',
            backButtonTitle: '关闭搜索',
            noResultsText: '没有找到相关结果',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '选择',
              navigateText: '切换',
              navigateUpText: '上移',
              navigateDownText: '下移',
              closeText: '关闭'
            }
          }
        },
        miniSearch: {
          options: { tokenize },
          searchOptions: { tokenize }
        }
      }
    }
  },
  vite: {
    plugins: [mediaExistsPlugin()]
  }
})
