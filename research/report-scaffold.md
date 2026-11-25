# 仓库与站点脚手架 — 任务汇报

> 任务会话：脚手架（scaffold）。完成时间：2026-11-25。本文是给主会话验收用的最终汇报。

## 一、状态总览

全部完成。`npm run build` / `npm run check` / `npm run test:pipeline` 均通过（VitePress 1.6.4 稳定版在 Node 26.13.1 下实测构建正常，未升级到 v2）。git 已 `git init -b main`，**无任何 commit**。

## 二、文件树（本会话创建/负责的文件）

```
REPO\
├─ .gitignore                      # node_modules/dist/cache/_work/sprite-catalog + 媒体策略段（mp4/webm/wav/mp3/ogg 不入库）
├─ package.json                    # scripts: dev / build / preview / content / check / test:pipeline；vitepress ^1.6.4 (devDep)
├─ package-lock.json               # npm 12 生成（CI 的 npm ci 依赖它，勿删）
├─ README.md                       # 简介/目录/开发/数据模型/媒体/发布说明
├─ .github\workflows\deploy.yml    # push main + workflow_dispatch；npm ci && npm run build；Pages (pages:write, id-token:write)
├─ docs\
│  ├─ .vitepress\config.ts         # lang=zh-CN，base 默认 '/blue-alert-re/'（BASE 环境变量可覆盖），nav/sidebar 从 data\*.json 生成，
│  │                               # 本地搜索 MiniSearch 中文分词（CJK 单字+二元组）+ 中文界面文案
│  ├─ .vitepress\theme\
│  │  ├─ index.ts                  # 扩展默认主题，全局注册 8 个组件
│  │  ├─ custom.css                # 蓝色主色，深浅色两套变量；占位框/探索器/卡片公共样式
│  │  └─ components\               # GameBadge / GameBadges / MediaImage / MediaVideo / MissionCard / UnitCard
│  │                               # / MuseumExplorer（按作品+类型+关键字筛选）/ UnitExplorer（按作品+分类+关键字筛选）
│  ├─ index.md  about.md           # 首页（两部作品卡 + 两入口 + 免责声明）、关于（版权声明）
│  ├─ museum\ index.md story.md credits.md network-maps.md   # 战役博物馆首页挂 MuseumExplorer
│  ├─ missions\ index.md           # 任务列表（挂 MuseumExplorer）；missions\<id>\index.md 由脚本生成
│  ├─ units\ index.md manual.md weapons.md                   # 单位图鉴首页挂 UnitExplorer
│  │                               # units\<id>\、units\<分类>\（7 个固定分类页）由脚本生成
│  └─ public\media\{missions,pictures,movies,units,ui}\.gitkeep
├─ data\
│  ├─ games.json                   # 真实值（按任务书契约）
│  ├─ missions.json units.json     # 空数组占位（写入时确认不存在，未覆盖任何并行会话文件）
│  ├─ credits.json                 # { sections: [], sources: [] }
│  ├─ hotkeys.json                 # []
│  └─ examples\ missions.json units.json credits.json hotkeys.json   # 冒烟样例（2 任务+3 单位+桩，纯数组、字段与正式契约一致）
├─ tools\
│  ├─ build-content.mjs            # data\*.json → 生成 missions\<id>\、units\<id>\、units\<分类>\ 页面；
│  │                               # 清理已删条目旧页；媒体缺失检查→占位；打印「生成 N 页，缺失媒体 M 个」
│  │                               # 参数：--root/--data/--docs；环境变量 DATA_DIR；games.json 缺失时回退主 data\
│  └─ check-content.mjs            # schema/games 取值/id 唯一/sources 非空/media 键/按作品目录扫描（g1,g2,g12,第一部,第二部）；退出码 1=失败
├─ research\DATA-MODEL.md          # 数据契约文档（字段表+管线行为+修改流程）
└─ _work\                          # gitignore，test:pipeline 输出在 _work\pipeline\
```

并行会话已有的 `research\mining-*`、`tools\disasm_scan.py` 等未触碰；`.mimosa\`（钩子状态）已加入 .gitignore。

## 三、命令

| 命令 | 作用 |
| --- | --- |
| `npm run dev` | 生成内容页 + 开发服务器 |
| `npm run build` | 生成内容页 + 整站构建（dist 在 `docs\.vitepress\dist`） |
| `npm run preview` | 预览构建产物 |
| `npm run content` | 仅生成/清理内容页 |
| `npm run check` | 数据校验 |
| `npm run test:pipeline` | 样例 → `_work\pipeline\docs` 生成 12 页 → 校验 → 断言必需页面存在 |
| `BASE=/ npm run build` | 整站根路径构建（本地全量预览用）；`DATA_DIR=data/examples npm run build` 可用样例数据构建（结束后跑 `npm run content` 恢复） |

## 四、数据契约文档

`research\DATA-MODEL.md`：games/missions/units/credits/hotkeys 全字段表、id 与媒体命名规范（-g1/-g2/-g12）、null 语义、管线行为与「填数据五步流程」。**字段名以该文档为准，改字段须同步两个 tools 脚本。**

## 五、验收结果（样例数据构建验证）

- 任务页 HTML：`game-badge` 徽标 ✓；`media-placeholder`「素材未随站点发布」图片占位 ✓、影片占位 ✓（媒体文件不存在时生成器直接渲染占位，不报错）。
- u-001（games g1+g2）双徽标同时显示 ✓；筛选组件（搜索框 + 「全部作品/全部分类」下拉）SSR 渲染 ✓。
- 侧栏由 JSON 生成（样例构建含 `M01 · 边境冲突（示例）`→`/missions/g1-m01/`）✓；资源路径带 base（`/blue-alert-re/assets/...`）✓；首页免责声明 ✓；搜索索引含中文内容、自定义分词已打包 ✓。
- 清理机制：`npm run content` 用空数据移除了 5 个样例页 ✓；缺失/损坏 JSON 宽容处理并告警 ✓。

## 六、给填数据 / 写页面会话的注意事项

1. **只改 `data\*.json` 与放媒体**，页面交给管线：改完 → `npm run check` → `npm run content`。不要手写 `missions\<id>\`、`units\<id>\`、`units\<分类>\`（`npm run content` 会删除数据里不存在的条目目录）。
2. **`data\missions.json`、`units.json` 必须始终是合法 JSON**：前端组件（卡片/筛选器）构建时直接 import 这两个文件与 `games.json`，坏 JSON 会让 vite 构建失败（build-content 脚本本身宽容，但整站构建不容错）。DATA_DIR 环境变量只影响生成页与侧栏，不影响前端组件的数据。
3. id 规则：任务 `${g}-${code小写}`（g1-/g2-/g12- 开头，小写字母数字连字符）；单位 `u-001` 三位序号（全局唯一，和 missions 的 id 不共用校验）。`sources` 必须非空，否则 `check` 报错。
4. 媒体：路径以 `/` 开头（站点根相对），对应 `docs\public\` 下文件；引用一律用 `<MediaImage>` / `<MediaVideo>`（自动 withBase + 占位）或 Markdown 图片语法——原始 HTML 的 `/media/...` 不会加 base。文件名后缀 -g1/-g2/-g12；mp4/webm/wav/mp3/ogg 不入库（本地放好即可，页面正常引用）。
5. `data\examples\` 仅是测试样例，别把它当数据源或从中复制正式条目而不改标注。
6. 影片嵌入条件：`media.video` 声明且文件存在 → HTML5 video；poster 同理。任务页 sections（资料图/影片/小地图/画廊）只在数据声明时出现。

## 七、未决问题

1. **credits / hotkeys 页面是静态骨架**：两页面目前写「编写中」；数据到位后若要渲染成表，需要给这两个页面补组件或改为生成页（超出本任务范围，契约字段已定义好）。
2. **npm 12 的 allowScripts 拦了 esbuild postinstall**：实测不影响构建（esbuild 0.21.5 走 optionalDependencies 平台二进制）。若新环境安装后报 esbuild 缺二进制，执行 `npm install-scripts approve esbuild` 再重装。
3. 搜索分词是「CJK 单字 + 相邻二元组」，召回好但索引稍大；若嫌噪音可在 config.ts 的 `tokenize` 调整。
4. 侧栏任务分组按 `game`（主归属）分到两作；`g12` 前缀条目需正确填写 `game` 字段否则默认归 g1。
5. CI 用 Node 22 + `npm ci`（依赖 package-lock.json 入库；本会话未做任何 git 提交，提交由主会话决定）。
6. 单位分类页固定生成 7 个（building/factory/defense/land/air/superweapon/other），URL 稳定；若数据出现白名单外分类，`check` 会报错（属预期防线）。
