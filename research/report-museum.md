# report-museum.md —— 战役博物馆（museum）任务 最终汇报

> 任务会话：战役博物馆（museum）。完成时间：2026-11-25。
> 验收命令均已通过：`npm run check`、`python -I research/validate_data.py`、`npm run content`（137 页）、`npx vitepress build docs`（导出到 `_work/qa-museum/dist`，3.45s 通过）。

## 一、改了哪些文件

**校验器 / 数据（mine）**
- `tools/check-content.mjs`：difficulty 放宽为「字符串/数字/null」（简报原文「难度等级: N」，g2 为 N/10 制）；credits `sections[].title` 放宽为「非空字符串或 null」（null = 原文无标题）。
- `research/validate_data.py`：missions 排序检查改为与约定一致的三元组 (game组 g1→g2→g12，type campaign→tutorial→network，order 升序)，删除了与约定冲突的旧 `(game, order)` 检查；排序警告消失。数据本身本已按约定排列，未移动条目。
- `data/missions.json`：仅追加各条目 `media` 字段（其余字段未动）；`data/credits.json` 未改（title=null 保留，由组件处理）。
- 注意：`research/DATA-MODEL.md` 中 difficulty（string|null）与 credits title 两行类型描述未同步——该文件不归本会话，建议主会话改为「number | string | null」与「string | null（null=原文无标题）」。

**脚本（新）**
- `tools/link_missions_media.py`：`python -I` 运行；按命名规则从 `docs/public/media/missions` 实际存在的文件绑定 image/video/poster/minimap（清单 media-manifest.json 仅作对照）；两作相同文件用 `-g12`；不使用 srfa 系列；写回前校验目标在仓库根内；幂等（只覆盖这四个键，保留 gallery 等）。

**生成器与组件**
- `tools/build-content.mjs`（任务页生成部分）：新标题约定 `missionPageTitle()`、难度格式（g1 数字 / g2「N / 10」）、教程课文按行渲染（'i ' 讲解→无序列表、'! ' 操作步骤→连续编号列表）、M23 简报缺失说明框、媒体三节（地形底图 / 简报影片 / 关卡结构分布示意）、无影片关卡的如实说明。
- 新组件（均 scoped 样式）：`MissionMeta.vue`（信息条：类型/关卡文件/基地代号/领土(两位)/难度/战场）、`MediaZoom.vue`（图片点击新窗口放大，缺文件退化为占位）、`CreditsList.vue`（渲染 credits.json，title=null 显示「汉化人员」并注明「分组标题为站点所加，原文无标题」）、`NetworkMapGrid.vue`（14 张联机图混排卡片）。
- 修改组件：`MissionCard.vue`（标题约定 + 「对手」改「战场」 + g2 难度格式）、`MuseumExplorer.vue`（排序改为约定三元组；搜索词加入战场/基地代号）、`MediaVideo.vue`（missing/加载失败时显示封面图 + 「影片未随站点发布，可用 tools/extract_media.py…」说明）。
- `docs/.vitepress/config.ts`：museum 侧栏 missionLabel 改为同一标题约定；组内排序 campaign→tutorial→network→order（修复战役关与联机图按 order 交错的问题）。`theme/index.ts` 仅追加 4 个组件注册。

**编辑页（中文，内容可溯源至 data/*.json 与 manual-*.md，页内注明出处）**
- `docs/index.md`：主视觉用界面资料图 `pictures/briefing-g12.jpg`；新增「本站是什么 / 数据从哪里来 / 徽标速查」；「进入战役博物馆」「浏览单位图鉴」两个入口及图鉴卡片文案未动。
- `docs/museum/index.md`：导语 + MuseumExplorer + 两作概览（两作主菜单图 + 数据事实：23 关/22 份简报、11 领土、任务号与文件号解耦、教学模式双徽标）。
- `docs/museum/story.md`：故事背景（两作说明书此节文字相同→合并引用 + 双徽标，「个自的利益」等错字照录并注明原文如此）；片头/片尾影片（mi/mo，本地内嵌播放、线上封面）；第一部按领土 01–22 的战役脉络（只串联战况原文的地点与事件，注明领土号≠文件号）；结局关领土 22「超级防线」（简报原文引用，呼应故事背景的 22 基地设定）；M23 无简报说明；第二部领土 01–11 脉络 + 结局关（罗曼先生）+ 雷曼/罗曼译名照录说明。
- `docs/museum/credits.md`：CreditsList 渲染 5 组 26 人（分组徽标）；「汉化人员」分组说明；显示顺序与数据来源（VA 出处）。
- `docs/museum/network-maps.md`：14 张混排卡片；g1 8 张有官方中文名（说明书「多人游戏任务」节）、g2 6 张无官方中文名如实说明；联机方式说明书原文引用。
- `docs/missions/index.md`：标题与字段约定说明。

## 二、页面清单

任务页 49 个（= missions 条目数，`docs/missions/<id>/`）+ 上述 6 个编辑页。任务页结构：徽标 → 标题 → 信息条 → 战况（教程关为「教程课程」）→ 任务目标 → 注意 → 地形底图 → 简报影片 → 关卡结构分布示意 → 数据来源（折叠）。

## 三、媒体绑定覆盖率

| 媒体 | 覆盖 | 说明 |
| --- | --- | --- |
| 地形底图 image | 35/49 | 33 战役（含 M23）+ 教学模式；14 联机图无此类文件 |
| 简报影片 video+poster | 33/49 | g1 M01–M22 + g2 全部 11 关；M23/M00 游戏文件本无 .sgv，页面如实注明 |
| 结构图 minimap | 35/49 | 同地形图 |
| 联机地图 14 张 | 0 | 无可提取媒体，页面有说明性提示 |

mp4 未入 git：线上构建时生成器检测文件缺失 → 自动改为「封面 + 提示」，封面图已入库不受影响。

## 四、自检截图结论

11 张截图（`E:\blue alert\_rea\out\qa-museum\shots\`，端口 4181 已关闭）：

1. **首页**：主视觉/徽标速查/两入口正常，hero 图带 base 正常加载。
2. **博物馆首页**：卡片 49 个、新标题、「战场」字段正确。
3. **g1-m01**：徽标、「第 01 关 · 战场：加拿大」、信息条（基地代号 X8A/领土 01/难度 1/战场 加拿大）、地形图可点击、HTML5 播放器（12s）。
4. **g2-m15**：徽标、「第 09 关」（领土号）、关卡文件 M15、难度「8 / 10」、无战场字段——文件号/领土号解耦正确。
5. **剧情**：故事背景双徽标合并引用、原文照录注记、片头影片内嵌播放。
6. **制作名单**：5 组带徽标；汉化组显示「汉化人员」+「分组标题为站点所加，原文无标题」。
7. **联机地图**：g1 8 张中文名卡 + g2 6 张 slug 卡（注明无官方中文名）。
8. **教程**：双徽标、「教学模式」、课程按讲解/操作步骤分列渲染。
9. **M23**：「简报缺失」说明框（游戏内显示「没有资料」）+ 技术性注意 + 地形图。
10. **移动端 390px（g2-m15）**：信息条换行正常、版式无溢出。
11. **影片回退**：删 QA 副本中的 m01-g1.mp4 后刷新 → 显示封面 + 「影片未随站点发布」说明（运行时 @error 回退路径）。

## 五、未解决问题 / 备忘

1. **并发写入事故**：本会话进行中发现 `data/missions.json` 被外部进程整体覆盖一次（media 清空、sources 措辞微调、文件字节数变化，疑似并行会话写入）。已核对 49 条 id、排序与字段语义无变化后，用绑定脚本重新填充 media。该脚本幂等且只动 media 四键——若后续仍有会话写 missions.json，写入后重跑 `python -I tools/link_missions_media.py` 即可恢复绑定。
2. `DATA-MODEL.md` 的 difficulty / credits title 类型描述待主会话同步修订（见上）。
3. CI（无 mp4）构建走「封面 + 提示」分支：本地已验证同等代码路径（回退截图 + 生成器构建期分支），CI 实跑一次可最终确认。
4. 联机图任务页的说明书说明含原版错字（「中选」「能难取胜」等），按内容铁律照录，已在联机地图页统一注明。
5. MuseumExplorer 空态文案、M23 战役定位、g2 联机图中文名等维持「宁缺毋造」原则未作推断。
