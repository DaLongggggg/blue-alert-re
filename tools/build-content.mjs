#!/usr/bin/env node
/**
 * build-content.mjs — 内容生成管线（Node ESM，零依赖）
 *
 * 流程：读取 data/*.json -> 校验（宽松，缺字段按 null/空处理）
 *      -> 生成 docs/missions/<id>/index.md、docs/units/<id>/index.md、docs/units/<分类>/index.md
 *      -> 清理数据中已删除条目的旧页面
 *      -> 检查声明的每个媒体路径在 docs/public 下是否存在（缺失渲染占位，不报错）
 *
 * 用法：
 *   node tools/build-content.mjs                       # 默认：根目录=仓库根，数据=data，文档=docs
 *   node tools/build-content.mjs --data data/examples  # 冒烟测试：样例数据
 *   node tools/build-content.mjs --docs _work/pipeline/docs
 * 环境变量：DATA_DIR 等价于 --data；npm run dev/build 会先执行本脚本。
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url))
const DEFAULT_ROOT = resolve(SCRIPT_DIR, '..')

// ===== 白名单常量（分类与作品键均为固定值，不做动态键访问） =====
const CATEGORIES = [
  ['building', '建筑'],
  ['factory', '工厂'],
  ['defense', '防御设施'],
  ['land', '地面单位'],
  ['air', '空中单位'],
  ['superweapon', '超级武器'],
  ['other', '其他']
]
const CATEGORY_LABELS = new Map(CATEGORIES)
const TYPE_LABELS = { campaign: '战役任务', tutorial: '教学任务', network: '联机地图' }
const GAME_ORDER = ['g1', 'g2']
// 展示分组（units.json 的 group 字段，由 tools/link_units_images.py 计算写入）
const GROUP_LABELS = {
  unit: '作战单位',
  building: '建筑与防御',
  mode: '生产模式',
  weapon: '武器名表条目',
  other: '其他收录'
}
// 游戏内 ID 空间（research/notes-units.md §1，两作同表）
const ID_RANGES = [
  [1, 15, '陆战单位'],
  [16, 24, '建筑生产模式（流入）'],
  [25, 29, '炮塔'],
  [30, 34, '空袭'],
  [40, 46, '特种单位'],
  [100, 108, '建筑'],
  [109, 113, 'Top Sentry 塔炮'],
  [115, 115, '界面元素']
]

/** 游戏内 ID 所属段说明（不在已知段内返回 null） */
function idRangeLabel(unitId) {
  const n = Number(unitId)
  if (Number.isFinite(n) === false) return null
  for (const [lo, hi, label] of ID_RANGES) {
    if (n >= lo && n <= hi) return lo === hi ? String(lo) + '（' + label + '）' : lo + '–' + hi + '（' + label + '）'
  }
  return null
}

// ===== 命令行参数 =====
function parseArgs(argv) {
  const args = { root: DEFAULT_ROOT, data: process.env.DATA_DIR || join('data'), docs: join('docs') }
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--root') args.root = argv[++i] || args.root
    else if (argv[i] === '--data') args.data = argv[++i] || args.data
    else if (argv[i] === '--docs') args.docs = argv[++i] || args.docs
  }
  return args
}

const ARGS = parseArgs(process.argv.slice(2))
const ROOT = resolve(ARGS.root)
const DATA_DIR = resolve(ROOT, ARGS.data)
const DOCS_DIR = resolve(ROOT, ARGS.docs)
const PUBLIC_DIR = join(DOCS_DIR, 'public')
const MISSIONS_DIR = join(DOCS_DIR, 'missions')
const UNITS_DIR = join(DOCS_DIR, 'units')

const warnings = []

function readJsonArray(name) {
  const file = join(DATA_DIR, name)
  if (existsSync(file) === false) {
    warnings.push('缺少 ' + name + '（按空数组处理）')
    return []
  }
  try {
    const parsed = JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''))
    return Array.isArray(parsed) === true ? parsed : []
  } catch (err) {
    warnings.push(name + ' 解析失败，按空数组处理: ' + String(err && err.message ? err.message : err))
    return []
  }
}

function readGames() {
  const primary = join(DATA_DIR, 'games.json')
  const file = existsSync(primary) === true ? primary : join(ROOT, 'data', 'games.json')
  try {
    const parsed = JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''))
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch (err) {
    warnings.push('games.json 解析失败: ' + String(err && err.message ? err.message : err))
    return {}
  }
}

const GAMES = readGames()
const MISSIONS = readJsonArray('missions.json')
const UNITS = readJsonArray('units.json')

// ===== 小工具 =====

/** 数组/标量转成 JSON 属性值（用于 Vue 属性，单引号属性内的单引号转义） */
function jsonAttr(value) {
  const list = Array.isArray(value) === true ? value : []
  return JSON.stringify(list).replace(/'/g, '&#39;')
}

/** HTML 静态属性转义 */
function attr(value) {
  return String(value ?? '').replace(/"/g, '&quot;')
}

/** YAML/前端 matter 中的字符串（JSON 双引号串是合法 YAML 标量） */
function yamlStr(value) {
  return JSON.stringify(String(value ?? ''))
}

/** 防止数据文本以 Markdown 结构符开头破坏版式 */
function mdLine(text) {
  const line = String(text ?? '')
  if (/^(#{1,6}\s|>|:::)/.test(line) === true) return '\\' + line
  return line
}

/** 把多行文本拆成 Markdown 段落 */
function mdParagraphs(text) {
  const raw = String(text ?? '').replace(/\r\n/g, '\n').trim()
  if (raw === '') return []
  return raw
    .split('\n')
    .map((s) => s.trim())
    .filter((s) => s !== '')
    .map(mdLine)
}

/** objectives 兼容：数组 / 字符串 / null */
function objectiveList(objective) {
  if (Array.isArray(objective) === true) return objective.map((o) => String(o)).filter((o) => o !== '')
  if (objective == null) return []
  const s = String(objective).trim()
  return s === '' ? [] : [s]
}

/** 插入排序：按数值键稳定升序（避免动态排序键） */
function orderedByNumber(pairs) {
  const out = []
  for (const pair of pairs) {
    let i = 0
    while (i < out.length && out[i][1] <= pair[1]) i++
    out.splice(i, 0, pair)
  }
  return out.map((pair) => pair[0])
}

function missionGameList(m) {
  const games = Array.isArray(m.games) === true && m.games.length > 0 ? m.games : [m.game === 'g2' ? 'g2' : 'g1']
  return games.filter((g) => GAME_ORDER.includes(g))
}

/**
 * 站点标题约定（与 docs/.vitepress/config.ts 的 missionLabel、MissionCard.vue 保持一致）：
 *   战役关 = 第 NN 关 · 战场：XX（NN 取 order 补零两位；XX 取数据里的战场字段，游戏原文即「战场：」，不得标成「对手」）
 *   联机地图 = 官方中文名（title，g1 联机图有）或地图文件名 slug（code）
 *   教学任务 = 教学模式
 */
function missionPageTitle(m) {
  if (m.type === 'tutorial') return '教学模式'
  if (m.type === 'network') return String(m.title || m.code || m.id)
  let head
  if (m.order != null) head = '第 ' + String(m.order).padStart(2, '0') + ' 关'
  else if (m.code) head = '关卡 ' + String(m.code)
  else head = String(m.id)
  if (m.opponent) head += ' · 战场：' + String(m.opponent)
  return head
}

/** 难度显示：g1 简报原文为「难度等级: N」；g2 原文为「难度等级 : N / 10」制 */
function difficultyText(m) {
  if (m.difficulty == null || m.difficulty === '') return ''
  const d = String(m.difficulty)
  return m.game === 'g2' ? d + ' / 10' : d
}

function mediaSiteToDisk(sitePath) {
  const rel = String(sitePath).replace(/^\/+/, '')
  return join(PUBLIC_DIR, ...rel.split('/'))
}

function mediaExists(sitePath) {
  return existsSync(mediaSiteToDisk(sitePath)) === true
}

// ===== 媒体计数 =====
const missingMedia = []
const declaredMedia = []

function checkMedia(sitePath, owner) {
  if (sitePath == null) return
  const s = String(sitePath)
  if (s === '') return
  declaredMedia.push(s)
  if (mediaExists(s) === false) missingMedia.push(owner + ' → ' + s)
}

function mediaImageTag(sitePath, altText, ratio) {
  const missingFlag = mediaExists(sitePath) === true ? '' : ' :missing="true"'
  const ratioAttr = ratio ? ' ratio="' + ratio + '"' : ''
  return '<MediaImage src="' + attr(sitePath) + '"' + ratioAttr + ' alt="' + attr(altText) + '"' + missingFlag + ' />'
}

function mediaVideoTag(sitePath, posterPath, ratio) {
  const missingFlag = mediaExists(sitePath) === true ? '' : ' :missing="true"'
  let posterAttr = ''
  if (posterPath) {
    if (mediaExists(posterPath) === true) posterAttr = ' poster="' + attr(posterPath) + '"'
  }
  const ratioAttr = ratio ? ' ratio="' + ratio + '"' : ''
  return '<MediaVideo src="' + attr(sitePath) + '"' + posterAttr + ratioAttr + missingFlag + ' />'
}

/** 可点击放大的图片（新窗口打开原图）；文件缺失时退化为普通占位 */
function mediaZoomTag(sitePath, altText, ratio) {
  const missingFlag = mediaExists(sitePath) === true ? '' : ' :missing="true"'
  const ratioAttr = ratio ? ' ratio="' + ratio + '"' : ''
  return '<MediaZoom src="' + attr(sitePath) + '"' + ratioAttr + ' alt="' + attr(altText) + '"' + missingFlag + ' />'
}

/** 教程课文按行渲染：'! ' 开头为操作步骤（连续编号列表），其余为讲解（无序列表） */
function renderTutorialCourse(briefing, lines) {
  const raw = String(briefing ?? '').replace(/\r\n/g, '\n')
  const rows = raw.split('\n').map((s) => s.trim()).filter((s) => s !== '')
  const runs = []
  for (const line of rows) {
    const kind = line.startsWith('! ') === true ? 'step' : 'talk'
    const text = mdLine(line.replace(/^[i!]\s/, ''))
    const last = runs[runs.length - 1]
    if (last != null && last.kind === kind) last.items.push(text)
    else runs.push({ kind, items: [text] })
  }
  let stepNo = 0
  for (const run of runs) {
    if (run.kind === 'talk') {
      for (const t of run.items) lines.push('- ' + t)
    } else {
      for (const t of run.items) {
        stepNo++
        lines.push(String(stepNo) + '. ' + t)
      }
    }
    lines.push('')
  }
}

// ===== 页面生成 =====

function generateMissionPage(m) {
  const label = missionPageTitle(m)
  const isTutorial = m.type === 'tutorial'
  const lines = []
  lines.push('---')
  lines.push('title: ' + yamlStr(label))
  lines.push('---')
  lines.push('')
  lines.push("<GameBadges :games='" + jsonAttr(missionGameList(m)) + "' />")
  lines.push('')
  lines.push('# ' + label)
  lines.push('')
  // 信息条（类型/关卡文件/基地代号/领土/难度/战场）由组件按数据渲染，格式见 MissionMeta.vue
  lines.push('<MissionMeta id="' + attr(String(m.id)) + '" />')
  lines.push('')

  // —— 正文：战况（教程关为整篇课文）——
  const hasBriefing = m.briefing != null && String(m.briefing).trim() !== ''
  lines.push('## ' + (isTutorial === true ? '教程课程' : '战况'))
  lines.push('')
  if (isTutorial === true) {
    if (hasBriefing === true) renderTutorialCourse(m.briefing, lines)
    else {
      lines.push('编写中。')
      lines.push('')
    }
  } else {
    const paras = mdParagraphs(m.briefing)
    if (paras.length > 0) {
      for (const p of paras) {
        lines.push(p)
        lines.push('')
      }
    } else {
      // 该条目在游戏内没有简报（如 g1 的 M23，简报界面显示「没有资料」）：说明情况而不是留空
      lines.push('::: warning 简报缺失')
      lines.push('游戏内本关没有简报资料——简报界面显示「没有资料」。本页依据关卡文件与程序内关卡分发表的存在性整理；该关在战役中的定位尚无文本证据，本站不作推断。程序内的定位记录见下方「注意」与「数据来源」。')
      lines.push(':::')
      lines.push('')
    }
  }

  // —— 任务目标 ——
  const objectives = objectiveList(m.objective)
  lines.push('## 任务目标')
  lines.push('')
  if (objectives.length > 0) {
    for (const o of objectives) lines.push('- ' + mdLine(o))
  } else if (isTutorial === true) {
    lines.push('教学关没有独立的任务目标文字；上方课程即游戏内的全部教学内容。')
  } else if (hasBriefing === false) {
    lines.push('游戏内未提供本关的任务目标（简报显示「没有资料」）。')
  } else {
    lines.push('编写中。')
  }
  lines.push('')

  // —— 注意（站点注记 / 原文照录说明）——
  if (m.note) {
    lines.push('## 注意')
    lines.push('')
    for (const p of mdParagraphs(m.note)) {
      lines.push(p)
      lines.push('')
    }
  }

  // —— 媒体 ——
  const media = m.media && typeof m.media === 'object' ? m.media : {}
  if (media.image) {
    checkMedia(media.image, m.id)
    lines.push('## 地形底图')
    lines.push('')
    lines.push(mediaZoomTag(media.image, label + ' 地形底图', '4 / 3'))
    lines.push('')
    lines.push('> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。')
    lines.push('')
  }
  const videoDeclared = media.video != null && media.video !== ''
  if (videoDeclared === true) {
    checkMedia(media.video, m.id)
    if (media.poster) checkMedia(media.poster, m.id)
    lines.push('## 简报影片')
    lines.push('')
    if (mediaExists(media.video) === true) {
      // 本地/CI 有 mp4 时内嵌 HTML5 播放器；比例与原片一致（g1 简报 320×208，g2 简报 768×432）
      const videoRatio = m.game === 'g2' ? '16 / 9' : '320 / 208'
      lines.push(mediaVideoTag(media.video, media.poster || '', videoRatio))
    } else {
      // mp4 不入 git（线上无影片）：显示封面并注明
      lines.push(mediaZoomTag(media.poster || '', label + ' 简报影片封面', ''))
      lines.push('')
      lines.push('::: tip 影片未随站点发布')
      lines.push('简报影片体积较大，未随站点发布，上方为影片封面。可用 `tools/extract_media.py` 从你自己的游戏目录生成影片本地观看。')
      lines.push(':::')
    }
    lines.push('')
  } else if (m.type === 'campaign' || isTutorial === true) {
    const files = m.files && typeof m.files === 'object' && Array.isArray(m.files) === false ? m.files : {}
    const hasSgv = files.sgv != null && String(files.sgv) !== ''
    lines.push('::: tip 简报影片')
    if (hasSgv === true) {
      lines.push('游戏文件中包含本关的简报影片，但尚未随站点发布。可用 `tools/extract_media.py` 从你自己的游戏目录生成影片。')
    } else {
      lines.push('游戏文件中未包含本关的简报影片，故无影片可展示。')
    }
    lines.push(':::')
    lines.push('')
  }
  if (media.minimap) {
    checkMedia(media.minimap, m.id)
    lines.push('## 关卡结构分布示意（按瓦片索引着色，非游戏原色）')
    lines.push('')
    lines.push(mediaZoomTag(media.minimap, label + ' 关卡结构分布示意', '1'))
    lines.push('')
    lines.push('> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。')
    lines.push('')
  }
  const gallery = Array.isArray(media.gallery) === true ? media.gallery : []
  if (gallery.length > 0) {
    lines.push('## 更多图片')
    lines.push('')
    let idx = 0
    for (const g of gallery) {
      idx++
      checkMedia(g, m.id)
      lines.push(mediaZoomTag(g, label + ' 图片 ' + idx, ''))
      lines.push('')
    }
  }
  if (media.image == null && videoDeclared === false && media.minimap == null && gallery.length === 0) {
    lines.push('::: tip 素材')
    lines.push('该条目暂无媒体资料。')
    lines.push(':::')
    lines.push('')
  }

  const sources = Array.isArray(m.sources) === true ? m.sources.filter(Boolean) : []
  const files = m.files && typeof m.files === 'object' && Array.isArray(m.files) === false ? m.files : {}
  const fileEntries = Object.keys(files).filter((k) => files[k] != null && String(files[k]) !== '')
  lines.push('::: details 数据来源')
  lines.push('')
  if (sources.length > 0) {
    for (const s of sources) lines.push('- ' + mdLine(s))
  } else {
    lines.push('- 编写中')
  }
  if (fileEntries.length > 0) {
    lines.push('')
    lines.push('原始文件（相对游戏安装目录）：')
    lines.push('')
    for (const k of fileEntries) lines.push('- `' + String(files[k]) + '`（' + k + '）')
  }
  lines.push('')
  lines.push(':::')
  lines.push('')
  return lines.join('\n')
}

function generateUnitPage(u) {
  const name = String(u.name || u.id)
  const groupLabel = u.group != null ? GROUP_LABELS[u.group] || null : null
  const isWeaponEntry = u.group === 'weapon'
  const lines = []
  lines.push('---')
  lines.push('title: ' + yamlStr(name))
  lines.push('---')
  lines.push('')
  const games = Array.isArray(u.games) === true && u.games.length > 0 ? u.games : []
  lines.push("<GameBadges :games='" + jsonAttr(games) + "' />")
  lines.push('')
  lines.push('# ' + name)
  lines.push('')
  if (u.nameEn) {
    lines.push('> ' + mdLine(u.nameEn))
    lines.push('')
  }
  const meta = []
  if (u.category && CATEGORY_LABELS.has(u.category) === true) meta.push('**分类**：' + CATEGORY_LABELS.get(u.category))
  else if (u.category) meta.push('**分类**：' + mdLine(u.category))
  if (groupLabel != null) meta.push('**收录分组**：' + groupLabel)
  if (u.unitId != null && u.unitId !== '') {
    let idText = '**游戏内 ID**：' + mdLine(u.unitId)
    const range = idRangeLabel(u.unitId)
    if (range != null) idText += '（ID 段：' + range + '）'
    meta.push(idText)
  }
  if (meta.length > 0) {
    lines.push(meta.join(' · '))
    lines.push('')
  }

  if (u.summary) {
    lines.push(mdLine(u.summary))
    lines.push('')
  }

  // —— 图片：主图（最近邻放大显示）+ 图集（UnitGallery 组件）——
  const galleryItems = Array.isArray(u.gallery) === true ? u.gallery.filter((g) => g && g.image) : []
  if (u.image || galleryItems.length > 0) {
    if (u.image) checkMedia(u.image, u.id)
    for (const g of galleryItems) checkMedia(g.image, u.id)
    lines.push(
      '<UnitGallery image="' + attr(u.image || '') + '" image-note="' + attr(u.imageNote || '') + '"' +
      ' alt="' + attr(name + ' 游戏内图像') + '" :gallery=\'' + jsonAttr(galleryItems) + "' />"
    )
    lines.push('')
  } else {
    if (isWeaponEntry === true) {
      lines.push('*武器名表条目：游戏内只有名称，无对应图像；与单位的对应关系尚未考证。*')
    } else {
      lines.push('*该条目暂无可用图片——现有素材尚无法唯一确认归属，宁缺毋造。*')
    }
    lines.push('')
  }

  const description = mdParagraphs(u.description)
  lines.push('## 说明')
  lines.push('')
  if (description.length > 0) {
    for (const p of description) {
      lines.push(p)
      lines.push('')
    }
  } else if (u.description === null) {
    // null = 原文即无；undefined = 尚未整理
    if (isWeaponEntry === true) lines.push('该条目来自游戏内武器名表，只有名称，无资料框说明。')
    else lines.push('游戏内资料框无此条目的说明。')
    lines.push('')
  } else {
    lines.push('编写中。')
    lines.push('')
  }

  const weaponTexts = Array.isArray(u.weapons) === true
    ? u.weapons
        .map((w) => {
          if (w == null) return ''
          if (typeof w === 'object' && w.name != null) return String(w.name)
          return String(w)
        })
        .filter((t) => t.trim() !== '')
    : []
  const stats = Array.isArray(u.stats) === true ? u.stats.filter((s) => s && s != null) : []
  lines.push('## 武器与属性')
  lines.push('')
  lines.push('**武器**')
  lines.push('')
  if (weaponTexts.length > 0) {
    for (const t of weaponTexts) {
      lines.push('- ' + mdLine(t))
    }
  } else if (Array.isArray(u.weapons) === true) {
    lines.push('暂无记录——武器与单位的对应关系尚未考证（见[武器一览](/units/weapons)）。')
  } else {
    lines.push('编写中。')
  }
  lines.push('')
  lines.push('**属性**')
  lines.push('')
  if (stats.length > 0) {
    lines.push('| 属性 | 数值 | 来源 |')
    lines.push('| --- | --- | --- |')
    for (const s of stats) {
      const n = mdLine(String(s.name ?? '—')).replace(/\|/g, '\\|')
      const v = mdLine(String(s.value ?? '—')).replace(/\|/g, '\\|')
      const src = s.source == null ? '—' : mdLine(String(s.source)).replace(/\|/g, '\\|')
      lines.push('| ' + n + ' | ' + v + ' | ' + src + ' |')
    }
  } else if (Array.isArray(u.stats) === true) {
    lines.push('数值属性尚未考证。')
  } else {
    lines.push('编写中。')
  }
  lines.push('')

  const sources = Array.isArray(u.sources) === true ? u.sources.filter(Boolean) : []
  lines.push('::: details 数据来源')
  lines.push('')
  if (sources.length > 0) {
    for (const s of sources) lines.push('- ' + mdLine(s))
  } else {
    lines.push('- 编写中')
  }
  lines.push('')
  lines.push(':::')
  lines.push('')
  return lines.join('\n')
}

function generateCategoryPage(categoryId, units) {
  const label = CATEGORY_LABELS.get(categoryId) || categoryId
  const owned = units.filter((u) => u.category === categoryId && !!u.id)
  const sorted = orderedByNumber(
    owned.map((u) => {
      const num = parseInt(String(u.id).replace(/^u-/, ''), 10)
      return [u, Number.isNaN(num) === true ? 1e9 : num]
    })
  )
  // 武器名表条目集中列示，不与单位/建筑混排为大卡片
  const cards = sorted.filter((u) => u.group !== 'weapon')
  const weaponEntries = sorted.filter((u) => u.group === 'weapon')
  const lines = []
  lines.push('---')
  lines.push('title: ' + yamlStr(label + '（单位分类）'))
  lines.push('---')
  lines.push('')
  lines.push('# ' + label)
  lines.push('')
  const countText = weaponEntries.length > 0
    ? '本分类共 ' + sorted.length + ' 个条目（单位/建筑 ' + cards.length + ' · 武器名表条目 ' + weaponEntries.length + '）'
    : '本分类共 ' + sorted.length + ' 个单位'
  lines.push('归类为「' + label + '」的条目，两作统一收录并以徽标标注归属作品。' + countText + '。')
  lines.push('')
  if (cards.length > 0) {
    for (const u of cards) {
      lines.push('<UnitCard id="' + attr(u.id) + '" />')
      lines.push('')
    }
  } else if (weaponEntries.length === 0) {
    lines.push('本分类暂无收录单位（编写中）。')
    lines.push('')
  }
  if (weaponEntries.length > 0) {
    lines.push('## 武器名表条目')
    lines.push('')
    lines.push('以下 ' + weaponEntries.length + ' 个条目是游戏内武器名表的原文（英文原名，游戏内未汉化）。' +
      '武器与单位的对应关系尚未考证，故集中列示，详见[武器一览](/units/weapons)。')
    lines.push('')
    for (const u of weaponEntries) {
      lines.push('- [' + mdLine(String(u.name || u.id)) + '](/units/' + String(u.id) + '/)')
    }
    lines.push('')
  }
  lines.push('返回 [单位图鉴](/units/)。')
  lines.push('')
  return lines.join('\n')
}

// ===== 写入与清理 =====

function writePage(dir, id, content, writtenIds) {
  const target = join(dir, id)
  mkdirSync(target, { recursive: true })
  writeFileSync(join(target, 'index.md'), content, 'utf8')
  writtenIds.add(id)
}

function cleanupStaleDirs(dir, keepIds) {
  if (existsSync(dir) === false) return 0
  let removed = 0
  const names = readdirSync(dir)
  for (const name of names) {
    const p = join(dir, name)
    if (statSync(p).isDirectory() === false) continue
    if (keepIds.has(name) === false) {
      rmSync(p, { recursive: true, force: true })
      removed++
    }
  }
  return removed
}

// ===== 主流程 =====
function main() {
  const pages = { missions: 0, units: 0, categories: 0 }
  const missionIds = new Set()
  const unitIds = new Set()
  const validUnits = UNITS.filter((u) => u && u.id)
  const validMissions = MISSIONS.filter((m) => m && m.id)

  // 任务页（按 order 稳定排序生成）
  const sortedMissions = orderedByNumber(
    validMissions.map((m) => {
      const key = typeof m.order === 'number' ? m.order : 1e9
      return [m, key]
    })
  )
  for (const m of sortedMissions) {
    writePage(MISSIONS_DIR, String(m.id), generateMissionPage(m), missionIds)
    pages.missions++
  }

  // 单位页
  const sortedUnits = orderedByNumber(
    validUnits.map((u) => {
      const num = parseInt(String(u.id).replace(/^u-/, ''), 10)
      return [u, Number.isNaN(num) === true ? 1e9 : num]
    })
  )
  for (const u of sortedUnits) {
    writePage(UNITS_DIR, String(u.id), generateUnitPage(u), unitIds)
    pages.units++
  }

  // 分类页（固定 7 个白名单分类，稳定 URL）
  const categoryIds = new Set()
  for (const [categoryId] of CATEGORIES) {
    writePage(UNITS_DIR, categoryId, generateCategoryPage(categoryId, validUnits), categoryIds)
    pages.categories++
  }

  // 清理已删除条目的旧页面
  const removedMissions = cleanupStaleDirs(MISSIONS_DIR, missionIds)
  const removedUnits = cleanupStaleDirs(UNITS_DIR, new Set([...unitIds, ...categoryIds]))

  // 汇总输出
  const total = pages.missions + pages.units + pages.categories
  console.log('任务页 ' + pages.missions + '，单位页 ' + pages.units + '，分类页 ' + pages.categories)
  if (removedMissions + removedUnits > 0) {
    console.log('清理旧页面 ' + (removedMissions + removedUnits) + ' 个')
  }
  if (missingMedia.length > 0) {
    const shown = missingMedia.slice(0, 20)
    for (const item of shown) console.log('缺失媒体: ' + item)
    if (missingMedia.length > shown.length) {
      console.log('……另有 ' + (missingMedia.length - shown.length) + ' 个缺失媒体未列出')
    }
  }
  for (const w of warnings) console.warn('警告: ' + w)
  console.log('生成 ' + total + ' 页，缺失媒体 ' + missingMedia.length + ' 个')
}

main()
