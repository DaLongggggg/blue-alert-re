#!/usr/bin/env node
/**
 * check-links.mjs — 构建产物站内链接检查（Node ESM，零依赖）
 *
 * VitePress 构建时的死链检查只覆盖 Markdown 里的链接；导航栏、侧栏和组件里写的链接
 * 不在其列（例如把 /about 写成 /about/ 就会在线上 404）。本脚本在构建之后扫描
 * docs/.vitepress/dist 下全部 HTML 的 href / src：凡是以站点 base 开头的站内路径，
 * 都必须能在 dist 里找到对应文件。
 *
 * 用法: node tools/check-links.mjs [--dist docs/.vitepress/dist]
 *   --dist  构建产物目录（相对仓库根，必须位于仓库内），默认 docs/.vitepress/dist
 *   BASE    站点 base 环境变量，与 config.ts 的取值规则相同，默认 /blue-alert-re/
 * 退出码: 0 = 通过；1 = 发现死链（逐条列出）；2 = 参数或目录错误
 */
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const BASE = (() => {
  let b = process.env.BASE?.trim()
  if (!b) return '/blue-alert-re/'
  if (!b.startsWith('/')) b = '/' + b
  if (!b.endsWith('/')) b += '/'
  return b
})()

function parseArgs(argv) {
  const out = { dist: 'docs/.vitepress/dist' }
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--dist' && argv[i + 1]) out.dist = argv[++i]
  }
  return out
}

function walkHtml(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = resolve(dir, name)
    if (statSync(full).isDirectory()) walkHtml(full, out)
    else if (name.endsWith('.html')) out.push(full)
  }
  return out
}

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
}

function fail(message) {
  console.error('check-links: ' + message)
  process.exit(2)
}

const args = parseArgs(process.argv.slice(2))
const distRoot = resolve(ROOT, args.dist)
if (distRoot.startsWith(ROOT + sep) !== true) fail('--dist 必须位于仓库目录内: ' + args.dist)
if (statSync(distRoot, { throwIfNoEntry: false })?.isDirectory() !== true) {
  fail('找不到构建产物目录 ' + args.dist + '（先执行 npm run build）')
}

const pages = walkHtml(distRoot)
const isFile = (file) => statSync(file, { throwIfNoEntry: false })?.isFile() === true
// 站点根相对路径 -> dist 内的文件；越出 dist 的路径一律视为不存在
const toFile = (sitePath) => {
  const file = resolve(distRoot, '.' + sitePath)
  return file.startsWith(distRoot + sep) ? file : null
}
const targetOf = (sitePath) => (sitePath === '' || sitePath.endsWith('/') ? sitePath + 'index.html' : sitePath)

const status = new Map()
const dead = new Map()
let references = 0

for (const page of pages) {
  const html = readFileSync(page, 'utf8')
  const referrer = page.slice(distRoot.length + 1).split(sep).join('/')
  for (const m of html.matchAll(/\b(?:href|src)="([^"]*)"/g)) {
    const url = decodeEntities(m[1])
    if (url.startsWith(BASE) !== true) continue
    // 去掉 base，保留开头的 '/'，得到站点根相对路径
    const sitePath = url.slice(BASE.length - 1)
    references += 1
    if (status.has(sitePath) !== true) {
      const plain = toFile(targetOf(sitePath))
      const withHtml = toFile(targetOf(sitePath) + '.html')
      status.set(sitePath, (plain !== null && isFile(plain)) || (withHtml !== null && isFile(withHtml)))
    }
    if (status.get(sitePath) === false) {
      if (dead.has(sitePath) !== true) dead.set(sitePath, new Set())
      dead.get(sitePath).add(referrer)
    }
  }
}

console.log('检查 ' + pages.length + ' 个页面，站内引用 ' + references + ' 处（目标 ' + status.size + ' 个），死链 ' + dead.size + ' 个')
for (const [target, referrers] of dead) {
  const where = [...referrers].slice(0, 3).join('、') + (referrers.size > 3 ? ' 等 ' + referrers.size + ' 个页面' : '')
  console.log('  ✗ ' + BASE.slice(0, -1) + target + '  ←  ' + where)
}
if (dead.size > 0) process.exit(1)
