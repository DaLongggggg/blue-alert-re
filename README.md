# 蓝色警戒中文维基 (blue-alert-re)

收录《蓝色警戒》(State of War, 2001) 与《蓝色警戒II：战争狂人》(State of War: Warmonger, 2003) 两作资料的非营利粉丝静态维基，基于 [VitePress](https://vitepress.dev) 构建。

**收录原则：两作内容混排、不按作品分目录。** 每个条目以「第一部 / 第二部」徽标标注归属作品；两作完全相同的条目只出一份（id 前缀 `g12`）。

**线上地址：<https://dalongggggg.github.io/blue-alert-re/>**（推送到 `main` 后由 GitHub Actions 自动部署）。

站内收录：战役任务 34 关（第一部 23 + 第二部 11）、教学模式 1 个、联机地图 14 张；单位 / 建筑 / 生产模式 / 武器名表条目 81 条；新兵手册与武器一览。每条数据都注明出处，拿不准的地方如实标注「尚未考证」，不做推断。

## 目录结构

```
REPO\
├─ docs\                     # VitePress 站点根
│  ├─ .vitepress\
│  │  ├─ config.ts           # 站点配置（导航/侧栏从 data/*.json 读取生成）
│  │  ├─ theme\              # 自定义主题（默认主题扩展）
│  │  │  ├─ index.ts
│  │  │  ├─ custom.css
│  │  │  └─ components\      # GameBadge / GameBadges / MediaImage / MediaVideo
│  │  │                      # MissionCard / UnitCard / MuseumExplorer / UnitExplorer
│  │  └─ (cache/ dist/ 已忽略)
│  ├─ index.md  about.md
│  ├─ museum\                # 战役博物馆首页 / 剧情 / 制作名单 / 联机地图
│  ├─ missions\              # 任务列表 + missions/<id>/index.md（脚本生成）
│  ├─ units\                 # 单位图鉴首页 / 新兵手册 / 武器一览
│  │                         # + units/<id>/、units/<分类>/（脚本生成）
│  └─ public\media\          # 媒体文件（missions / pictures / movies / units / ui）
├─ data\                     # 数据契约（站点唯一数据源）
│  ├─ games.json             # 两部作品元信息（真实值）
│  ├─ missions.json          # 任务数组（战役/教学/联机图）
│  ├─ units.json             # 单位数组
│  ├─ credits.json           # 制作名单
│  ├─ hotkeys.json           # 快捷键
│  └─ examples\              # 冒烟测试样例（仅 test:pipeline 使用）
├─ tools\                     # 生成/校验脚本 + 媒体提取与精灵解码 + 逆向取证脚本
├─ research\                 # 格式文档与逆向笔记（DATA-MODEL.md 为数据契约）
├─ _work\                    # 大体量中间产物（不入库）
└─ .github\workflows\deploy.yml
```

## 本地开发

要求 Node ≥ 18（在 Node 26 上验证）。

```bash
npm install          # 安装依赖
npm run dev          # 先生成内容页，再启动开发服务器
npm run build        # 先生成内容页，再构建整站到 docs/.vitepress/dist
npm run preview      # 预览构建产物
```

其它命令：

```bash
npm run content      # 仅重新生成 missions/<id>/、units/<id>/、units/<分类>/ 页面
npm run check        # 校验 data/*.json 与目录结构
npm run test:pipeline  # 冒烟测试：用 data/examples 样例在 _work/ 生成页面并校验
npm run check:links   # 构建后检查 dist 里的站内链接（导航/侧栏/组件里写的链接也覆盖）
```

`base` 默认为 `/blue-alert-re/`（GitHub Pages 子路径）。本地想整站预览时用站点根：

```bash
BASE=/ npm run build && BASE=/ npm run preview
```

数据目录可用环境变量 `DATA_DIR` 覆盖（例如用样例数据构建验证：`DATA_DIR=data/examples npm run build`，之后执行 `npm run content` 恢复）。

## 数据模型（统一收录 + 作品标注）

- **missions.json**：`id`（`g1-m01` 风格，两作相同条目用 `g12-` 前缀）、`game`（主归属）、`games`（出现的作品数组）、`type`（campaign / tutorial / network）、`title`、`objective`、`briefing`、`files`（相对游戏目录的原始文件）、`media`（站点根相对路径）、`sources`（必填）等。
- **units.json**：`id`（`u-001` 三位序号）、`games`、`category`（building / factory / defense / land / air / superweapon / other）、`name` / `nameEn`、`summary` / `description`、`weapons`、`stats`、`image`、`sources`（必填）。
- **credits.json / hotkeys.json**：制作名单分节与快捷键表，均带 `games` 标注。
- 生成器与前端组件对缺字段宽容：缺的按 null / 空处理，页面显示「编写中」。

完整字段规范见 [research/DATA-MODEL.md](research/DATA-MODEL.md)。**修改字段名前先同步该文档与 `tools/` 两个脚本。**

## 工具一览（`tools/`）

| 文件 | 作用 |
| --- | --- |
| `build-content.mjs` / `check-content.mjs` | 由 `data/*.json` 生成任务页、单位页与分类页；校验数据契约（`npm run content` / `npm run check`） |
| `extract_media.py` | 从游戏目录提取地形底图、小地图、界面资料图与影片（用法见 [tools/extract_README.md](tools/extract_README.md)） |
| `decode_sprites.py` | 解码 `sprites.info/.data` 精灵包（RGB565 行 RLE），渲染精灵图与资料框全息图 |
| `link_missions_media.py` / `link_units_images.py` | 把提取产物按命名规则绑定到 `data/missions.json` 的 `media` 与 `data/units.json` 的图片字段（幂等，可重跑） |
| `mine_*.py` | 逆向取证脚本：从程序数据段、反汇编文本与说明书中还原名称表、简报与热键，生成 `data/` 与 `research/` 的原始材料 |

格式说明与逆向笔记见 `research/`（`FORMAT-media.md`、`FORMAT-sprites.md`、`notes-*.md`）。提取与解码脚本只读取游戏目录，产物写入仓库内；全程不运行游戏程序。

## 媒体说明

- 媒体文件放在 `docs/public/media/{missions,pictures,movies,units,ui}/`，文件名以 `-g1` / `-g2` / `-g12` 结尾标注归属作品。
- **入库策略：图片入库，影片与音频不入库**（`.gitignore` 忽略 `docs/public/media/**/*.mp4|webm|wav|mp3|ogg`），片源体积大且有版权风险，仅保留在本地。
- 站内媒体路径一律写成站点根相对路径（如 `/media/missions/g1-m01.jpg`）。页面内引用请用 Markdown 图片语法或 `withBase()`（原始 HTML 的 `/media/...` 不会自动加 base）；推荐直接使用 `MediaImage` / `MediaVideo` 组件。
- **媒体由提取脚本从玩家自己的游戏目录离线生成**：本仓库的提取/解码脚本不运行游戏程序、不分发游戏资源，仅解析本地已购安装目录中的数据；未随站点发布的素材在页面中渲染「素材未随站点发布」占位。

## 发布

GitHub Actions（`.github/workflows/deploy.yml`）在 `push` 到 `main` 或手动触发时执行 `npm ci && npm run build`，随后用 `tools/check-links.mjs` 检查构建产物里的站内链接，通过后发布到 GitHub Pages。本仓库的 Pages Source 已设为 **GitHub Actions**；fork 后自行部署时，需在仓库 **Settings → Pages** 把 Source 设为 **GitHub Actions**。

线上构建不含影片文件（不入库）：生成器检测到文件缺失时，任务页自动改为显示影片封面与说明；在本地运行提取脚本即可补齐影片。
