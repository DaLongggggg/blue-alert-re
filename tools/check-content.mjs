#!/usr/bin/env node
/**
 * check-content.mjs — 数据校验（Node ESM，零依赖）
 *
 * 校验内容：
 *   1. data/*.json 的 schema 与必填约束
 *   2. games 取值（g1 | g2，id 前缀另允许 g12）
 *   3. id 唯一性
 *   4. sources 非空（missions / units）
 *   5. docs 下不存在按作品划分的目录（g1/、g2/、第一部/ 等）
 *
 * 用法：
 *   node tools/check-content.mjs                    # 校验 data/
 *   node tools/check-content.mjs --data data/examples
 * 退出码：0 通过；1 存在错误。
 */
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url))
const DEFAULT_ROOT = resolve(SCRIPT_DIR, '..')

const GAME_IDS = ['g1', 'g2']
const GAME_ID_PREFIXES = ['g1', 'g2', 'g12'] // id 前缀：两作相同条目允许 g12
const MISSION_TYPES = ['campaign', 'tutorial', 'network']
const UNIT_CATEGORIES = ['building', 'factory', 'defense', 'land', 'air', 'superweapon', 'other']
const MISSION_MEDIA_KEYS = ['image', 'video', 'poster', 'minimap', 'gallery']
const REQUIRED_GAME_KEYS = ['id', 'order', 'label', 'mark', 'title', 'subtitle', 'year', 'sourceDir', 'exe']
// 按作品划分的目录名（全站禁止出现）
const FORBIDDEN_DIR_NAMES = new Set(['g1', 'g2', 'g12', '第一部', '第二部'])
const SCAN_SKIP_DIRS = new Set(['node_modules', '.git', '.vitepress', 'dist', '_work'])

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

const errors = []

function err(scope, message) {
  errors.push('[' + scope + '] ' + message)
}

function isStr(v) {
  return typeof v === 'string'
}

function isStrOrNull(v) {
  return v == null || typeof v === 'string'
}

function readJson(name) {
  const file = join(DATA_DIR, name)
  if (existsSync(file) === false) {
    err(name, '文件不存在')
    return null
  }
  try {
    return JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''))
  } catch (e) {
    err(name, 'JSON 解析失败: ' + String(e && e.message ? e.message : e))
    return null
  }
}

function checkGames() {
  const file = join(DATA_DIR, 'games.json')
  const target = existsSync(file) === true ? file : join(ROOT, 'data', 'games.json')
  let games = null
  try {
    games = JSON.parse(readFileSync(target, 'utf8').replace(/^\uFEFF/, ''))
  } catch (e) {
    err('games.json', 'JSON 解析失败: ' + String(e && e.message ? e.message : e))
    return {}
  }
  if (games == null || typeof games !== 'object' || Array.isArray(games) === true) {
    err('games.json', '应为对象 { g1, g2 }')
    return {}
  }
  for (const gid of GAME_IDS) {
    const g = games[gid]
    if (g == null || typeof g !== 'object') {
      err('games.json', '缺少 ' + gid)
      continue
    }
    for (const key of REQUIRED_GAME_KEYS) {
      if (g[key] == null) err('games.json', gid + ' 缺少字段 ' + key)
    }
    if (g.id != null && g.id !== gid) err('games.json', gid + '.id 应为 ' + gid + '，实际 ' + JSON.stringify(g.id))
    if (g.year != null && Number.isFinite(Number(g.year)) === false) err('games.json', gid + '.year 应为数字')
  }
  return games
}

function checkGamesField(scope, item, field) {
  const games = item[field]
  if (games == null) {
    err(scope, 'id=' + item.id + ' 缺少 ' + field)
    return
  }
  if (Array.isArray(games) === false || games.length === 0) {
    err(scope, 'id=' + item.id + ' 的 ' + field + ' 应为非空数组')
    return
  }
  for (const g of games) {
    if (GAME_IDS.includes(g) === false) {
      err(scope, 'id=' + item.id + ' 的 ' + field + ' 含非法值 ' + JSON.stringify(g) + '（只允许 g1 | g2）')
    }
  }
}

function checkSources(scope, item) {
  const sources = item.sources
  if (Array.isArray(sources) === false || sources.length === 0) {
    err(scope, 'id=' + item.id + ' 的 sources 不能为空（须给出至少一条数据来源）')
    return
  }
  sources.forEach((s, i) => {
    if (isStr(s) === false || s.trim() === '') {
      err(scope, 'id=' + item.id + ' 的 sources[' + i + '] 应为非空字符串')
    }
  })
}

function checkMissions() {
  const missions = readJson('missions.json')
  if (Array.isArray(missions) === false) return 0
  const seen = new Map()
  let count = 0
  missions.forEach((m, idx) => {
    const scope = 'missions[' + idx + ']'
    if (m == null || typeof m !== 'object' || Array.isArray(m) === true) {
      err(scope, '应为对象')
      return
    }
    count++
    // id：${g}-${code小写}，g 取 g1|g2|g12；联机图可用文件名 slug
    if (isStr(m.id) === false || /^[a-z0-9][a-z0-9-]*$/.test(m.id) === false) {
      err(scope, 'id 应为小写字母/数字/连字符，实际 ' + JSON.stringify(m.id))
    } else {
      const prefix = m.id.split('-')[0]
      if (GAME_ID_PREFIXES.includes(prefix) === false) {
        err(scope, 'id 应以 g1- / g2- / g12- 开头，实际 ' + JSON.stringify(m.id))
      }
      if (seen.has(m.id) === true) err(scope, 'id 重复：' + m.id + '（首次出现于 ' + seen.get(m.id) + '）')
      else seen.set(m.id, scope)
    }
    if (m.game != null && GAME_IDS.includes(m.game) === false) {
      err(scope, 'id=' + m.id + ' 的 game 应为 g1 | g2，实际 ' + JSON.stringify(m.game))
    }
    checkGamesField(scope, m, 'games')
    if (m.type != null && MISSION_TYPES.includes(m.type) === false) {
      err(scope, 'id=' + m.id + ' 的 type 应为 campaign | tutorial | network，实际 ' + JSON.stringify(m.type))
    }
    if (m.order != null && Number.isFinite(Number(m.order)) === false) {
      err(scope, 'id=' + m.id + ' 的 order 应为数字或 null')
    }
    if (m.expectedNo != null && Number.isFinite(Number(m.expectedNo)) === false) {
      err(scope, 'id=' + m.id + ' 的 expectedNo 应为数字或 null')
    }
    for (const field of ['title', 'baseCode', 'opponent', 'briefing', 'note']) {
      if (m[field] != null && isStr(m[field]) === false) {
        err(scope, 'id=' + m.id + ' 的 ' + field + ' 应为字符串或 null')
      }
    }
    // difficulty 允许数字：简报原文为「难度等级: N」（g2 为 N/10 制），数据按数字收录
    if (m.difficulty != null && isStr(m.difficulty) === false && Number.isFinite(Number(m.difficulty)) === false) {
      err(scope, 'id=' + m.id + ' 的 difficulty 应为字符串/数字或 null')
    }
    if (m.objective != null && isStr(m.objective) === false && Array.isArray(m.objective) === false) {
      err(scope, 'id=' + m.id + ' 的 objective 应为字符串/字符串数组或 null')
    }
    if (m.objective != null && Array.isArray(m.objective) === true) {
      m.objective.forEach((o, i) => {
        if (isStr(o) === false) err(scope, 'id=' + m.id + ' 的 objective[' + i + '] 应为字符串')
      })
    }
    if (m.files != null && (typeof m.files !== 'object' || Array.isArray(m.files) === true)) {
      err(scope, 'id=' + m.id + ' 的 files 应为对象或 null')
    }
    const media = m.media
    if (media != null && (typeof media !== 'object' || Array.isArray(media) === true)) {
      err(scope, 'id=' + m.id + ' 的 media 应为对象或 null')
    } else if (media != null) {
      for (const key of Object.keys(media)) {
        if (MISSION_MEDIA_KEYS.includes(key) === false) {
          err(scope, 'id=' + m.id + ' 的 media 含未知键 ' + JSON.stringify(key) + '（允许：' + MISSION_MEDIA_KEYS.join('/') + '）')
        }
      }
      if (media.gallery != null && Array.isArray(media.gallery) === false) {
        err(scope, 'id=' + m.id + ' 的 media.gallery 应为字符串数组')
      } else if (Array.isArray(media.gallery) === true) {
        media.gallery.forEach((g, i) => {
          if (isStr(g) === false || g.startsWith('/') === false) {
            err(scope, 'id=' + m.id + ' 的 media.gallery[' + i + '] 应为以 / 开头的站点根相对路径')
          }
        })
      }
      for (const key of ['image', 'video', 'poster', 'minimap']) {
        if (media[key] != null && (isStr(media[key]) === false || media[key].startsWith('/') === false)) {
          err(scope, 'id=' + m.id + ' 的 media.' + key + ' 应为以 / 开头的站点根相对路径或 null')
        }
      }
    }
    checkSources(scope, m)
  })
  return count
}

function checkUnits() {
  const units = readJson('units.json')
  if (Array.isArray(units) === false) return 0
  const seen = new Map()
  let count = 0
  units.forEach((u, idx) => {
    const scope = 'units[' + idx + ']'
    if (u == null || typeof u !== 'object' || Array.isArray(u) === true) {
      err(scope, '应为对象')
      return
    }
    count++
    if (isStr(u.id) === false || /^u-\d{3}$/.test(u.id) === false) {
      err(scope, 'id 应为 u-001 形式的三位序号，实际 ' + JSON.stringify(u.id))
    } else {
      if (seen.has(u.id) === true) err(scope, 'id 重复：' + u.id + '（首次出现于 ' + seen.get(u.id) + '）')
      else seen.set(u.id, scope)
    }
    checkGamesField(scope, u, 'games')
    if (isStr(u.name) === false || u.name.trim() === '') err(scope, 'id=' + u.id + ' 的 name 应为非空字符串')
    if (u.nameEn != null && isStr(u.nameEn) === false) err(scope, 'id=' + u.id + ' 的 nameEn 应为字符串或 null')
    if (u.category != null && UNIT_CATEGORIES.includes(u.category) === false) {
      err(scope, 'id=' + u.id + ' 的 category 应为 ' + UNIT_CATEGORIES.join(' | ') + '，实际 ' + JSON.stringify(u.category))
    }
    if (u.unitId != null && isStr(u.unitId) === false && typeof u.unitId !== 'number') {
      err(scope, 'id=' + u.id + ' 的 unitId 应为字符串/数字或 null')
    }
    for (const field of ['summary', 'description']) {
      if (u[field] != null && isStr(u[field]) === false) err(scope, 'id=' + u.id + ' 的 ' + field + ' 应为字符串或 null')
    }
    if (u.weapons != null && Array.isArray(u.weapons) === false) err(scope, 'id=' + u.id + ' 的 weapons 应为数组')
    if (u.stats != null) {
      if (Array.isArray(u.stats) === false) {
        err(scope, 'id=' + u.id + ' 的 stats 应为数组')
      } else {
        u.stats.forEach((s, i) => {
          if (s == null || typeof s !== 'object' || Array.isArray(s) === true) {
            err(scope, 'id=' + u.id + ' 的 stats[' + i + '] 应为 { name, value, source }')
          } else if (isStr(s.name) === false) {
            err(scope, 'id=' + u.id + ' 的 stats[' + i + '].name 应为字符串')
          }
        })
      }
    }
    if (u.image != null && (isStr(u.image) === false || u.image.startsWith('/') === false)) {
      err(scope, 'id=' + u.id + ' 的 image 应为以 / 开头的站点根相对路径或 null')
    }
    checkSources(scope, u)
  })
  return count
}

function checkCredits() {
  const credits = readJson('credits.json')
  if (credits == null) return 0
  if (typeof credits !== 'object' || Array.isArray(credits) === true) {
    err('credits.json', '应为对象 { sections, sources }')
    return 0
  }
  if (Array.isArray(credits.sections) === false) {
    err('credits.json', 'sections 应为数组')
    return 0
  }
  credits.sections.forEach((sec, idx) => {
    const scope = 'credits.sections[' + idx + ']'
    if (sec == null || typeof sec !== 'object') {
      err(scope, '应为对象 { title, people, games }')
      return
    }
    // title 允许 null：原文即无标题的分组（如汉化人员），页面显示站点自定的标题
    if (sec.title != null && (isStr(sec.title) === false || sec.title.trim() === '')) {
      err(scope, 'title 应为非空字符串或 null')
    }
    if (Array.isArray(sec.people) === false) err(scope, 'people 应为字符串数组')
    else sec.people.forEach((p, i) => {
      if (isStr(p) === false) err(scope, 'people[' + i + '] 应为字符串')
    })
    checkGamesField(scope, sec, 'games')
  })
  if (credits.sources != null && Array.isArray(credits.sources) === false) err('credits.json', 'sources 应为数组')
  return credits.sections.length
}

function checkHotkeys() {
  const hotkeys = readJson('hotkeys.json')
  if (hotkeys == null) return 0
  if (Array.isArray(hotkeys) === false) {
    err('hotkeys.json', '应为数组')
    return 0
  }
  hotkeys.forEach((h, idx) => {
    const scope = 'hotkeys[' + idx + ']'
    if (h == null || typeof h !== 'object') {
      err(scope, '应为对象 { action, keys, games, source }')
      return
    }
    if (isStr(h.action) === false || h.action.trim() === '') err(scope, 'action 应为非空字符串')
    if (isStr(h.keys) === false || h.keys.trim() === '') err(scope, 'keys 应为非空字符串')
    checkGamesField(scope, h, 'games')
    if (isStr(h.source) === false || h.source.trim() === '') err(scope, 'source 应为非空字符串')
  })
  return hotkeys.length
}

// 扫描 docs 下按作品划分的目录
function scanForbiddenDirs() {
  if (existsSync(DOCS_DIR) === false) return
  const stack = [DOCS_DIR]
  while (stack.length > 0) {
    const dir = stack.pop()
    let entries
    try {
      entries = readdirSync(dir, { withFileTypes: true })
    } catch (e) {
      continue
    }
    for (const entry of entries) {
      if (entry.isDirectory() === false) continue
      if (FORBIDDEN_DIR_NAMES.has(entry.name) === true) {
        err('目录结构', '存在按作品划分的目录: ' + join(dir, entry.name).slice(DOCS_DIR.length + 1) + '（全站两作混排，禁止 g1/g2/第一部/第二部 等目录）')
        continue
      }
      if (SCAN_SKIP_DIRS.has(entry.name) === true) continue
      stack.push(join(dir, entry.name))
    }
  }
}

function main() {
  const gameCount = Object.keys(checkGames()).length
  const missionCount = checkMissions()
  const unitCount = checkUnits()
  const creditSections = checkCredits()
  const hotkeyCount = checkHotkeys()
  scanForbiddenDirs()

  if (errors.length > 0) {
    console.log('校验未通过，共 ' + errors.length + ' 处错误：')
    const shown = errors.slice(0, 50)
    for (const e of shown) console.log('  - ' + e)
    if (errors.length > shown.length) console.log('  ……另有 ' + (errors.length - shown.length) + ' 处错误未列出')
    process.exit(1)
  }

  console.log(
    '校验通过：作品 ' + gameCount + '，任务 ' + missionCount + '，单位 ' + unitCount + '，制作名单 ' + creditSections + ' 节，快捷键 ' + hotkeyCount + ' 条，目录结构 OK'
  )
  process.exit(0)
}

main()
