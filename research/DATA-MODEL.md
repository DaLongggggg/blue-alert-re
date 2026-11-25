# 数据契约 (DATA-MODEL)

站点唯一数据源是 `data/*.json`；`tools/build-content.mjs` 读取它们生成 `docs/missions/<id>/index.md`、`docs/units/<id>/index.md` 与 `docs/units/<分类>/index.md`，`docs/.vitepress/config.ts` 从同一批 JSON 生成导航与侧栏。**字段名一经发布不再改动；允许增加字段，不允许删改本文列出的字段名。** 生成器对缺字段宽容：缺的按 `null` / 空处理，页面显示「编写中」。

## 通用约定

- **作品标识**：`g1` = 第一部《蓝色警戒》(State of War, 2001)；`g2` = 第二部《蓝色警戒II：战争狂人》(Warmonger, 2003)；`g12` 仅用作「两作相同条目」的 id 前缀，不出现在任何 `games` 数组里。
- **统一收录**：两作内容混排在同一路径下，全站不得出现按作品划分的目录（`g1/`、`g2/`、`第一部/` 等会被 `tools/check-content.mjs` 判错）。
- **id 规范**：任务 `g1-m01`（`${g}-${code小写}`，联机图用地图文件名去扩展名的 slug）；单位 `u-001`（三位序号，全站唯一）。
- **媒体路径**：一律为**站点根相对路径**（以 `/` 开头，如 `/media/missions/g1-m01.jpg`）。文件名以 `-g1` / `-g2` / `-g12` 结尾标注归属；两作相同的文件只出一份用 `-g12`。
- **sources 约束**：`missions` / `units` 的 `sources` 必须是非空字符串数组（至少一条，注明提取/推断依据）；`credits.json` 顶层 `sources` 允许为空数组。
- **null 语义**：`null` = 尚未整理（页面显示「编写中」）；空字符串请写成 `null`，不要用 `""`。

## games.json（对象，固定两键）

```json
{
  "g1": { "id": "g1", "order": 1, "label": "第一部", "mark": "Ⅰ", "title": "蓝色警戒",
          "subtitle": "State of War", "year": 2001,
          "sourceDir": "蓝色警戒I完整版", "exe": "State of War.exe" },
  "g2": { "id": "g2", "order": 2, "label": "第二部", "mark": "Ⅱ", "title": "蓝色警戒II：战争狂人",
          "subtitle": "State of War: Warmonger", "year": 2003,
          "sourceDir": "蓝色警戒II完整版", "exe": "State of War - Warmonger.exe" }
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | string | 固定 `g1` / `g2` |
| order | number | 展示顺序（侧栏分组排序） |
| label | string | 徽标文案：第一部 / 第二部 |
| mark | string | 徽标字符：Ⅰ / Ⅱ |
| title / subtitle | string | 中文名 / 英文名 |
| year | number | 发售年 |
| sourceDir | string | 本地游戏目录名（只读，禁止运行其中 exe） |
| exe | string | 主程序文件名（仅记录，不执行） |

## missions.json（数组）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | ✓ | `${g}-${code小写}`；g ∈ g1/g2/g12；小写字母数字连字符 |
| game | string | ✓ | 主归属 `g1` \| `g2`（侧栏分组依据） |
| games | string[] | ✓ | 出现的作品数组，元素 ∈ {g1, g2}，非空 |
| code | string | – | 关卡编号如 `M01`；联机图为地图 slug |
| order | number \| null | – | 展示序号（侧栏与列表排序） |
| type | string | ✓ | `campaign`（战役）/ `tutorial`（教学）/ `network`（联机地图） |
| title | string \| null | – | 中文名 |
| baseCode | string \| null | – | 游戏内基础编号 |
| expectedNo | number \| null | – | 领土号（简报「领土: NN」；字段名为历史沿用） |
| difficulty | number \| string \| null | – | 难度：简报「难度等级」后的数字（g2 为 N / 10 制，按原值存 N） |
| opponent | string \| null | – | 简报的「战场」行（地名/地区名，仅 g1 有）。字段名为历史沿用，页面上标作「战场」 |
| objective | string \| string[] \| null | – | 任务目标（可多条） |
| briefing | string \| null | – | 简报正文（多行文本，`\n` 分段） |
| note | string \| null | – | 备注 |
| files | object \| null | – | 原始文件路径表（**相对游戏安装目录**），如 `{ "map": "Data/Levels/M01.map" }` |
| media | object \| null | – | 见下 |
| sources | string[] | ✓ | 非空 |

`media` 允许的键（值均为站点根相对路径）：

- `image`：资料图
- `video`：影片（`/media/movies/*.mp4` 等；文件存在时页面嵌 HTML5 video）
- `poster`：影片封面
- `minimap`：关卡结构分布示意（`.tmi` 瓦片索引着色，非游戏原色；展示时须如实标注）
- `gallery`：字符串数组，更多图片

## units.json（数组）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| id | string | ✓ | `u-001` 三位序号，全站唯一 |
| games | string[] | ✓ | 出现的作品数组，非空 |
| name | string | ✓ | 中文名 |
| nameEn | string \| null | – | 英文名 |
| category | string | ✓ | `building` 建筑 / `factory` 工厂 / `defense` 防御 / `land` 地面 / `air` 空中 / `superweapon` 超级武器 / `other` 其他 |
| unitId | string \| number \| null | – | 游戏内部 ID |
| summary | string \| null | – | 一句话简介（卡片与页首展示） |
| description | string \| null | – | 详细说明 |
| weapons | array | – | 武器列表（字符串，或 `{ name, ... }` 对象） |
| stats | array | – | `[{ "name": "生命值", "value": "1000", "source": "M01.map" }]` |
| image | string \| null | – | 站点根相对路径 |
| group | string \| null | – | 展示分组：`unit` 作战单位 / `building` 建筑与防御 / `mode` 生产模式 / `weapon` 武器名表条目 / `other` 其他。由 `tools/link_units_images.py` 按既有字段推导写入（category=other 且无 unitId → weapon；unitId 16–24 → mode；category=other → other；building/factory/defense → building；其余 → unit）。`category` 字段保持原七值白名单不变 |
| imageNote | string \| null | – | 主图说明（图注）：精灵图写涂装/来源，全息图写「资料框绿色全息图」等 |
| gallery | array \| null | – | 额外图集 `[{ "image": "/media/units/holo-…-g12.png", "label": "资料框绿色全息图" }]`；由 `tools/link_units_images.py` 绑定（全息图 = InfoBox/\*.tsp 解码单帧，经 `tools/decode_sprites.py --select` 渲染） |
| sources | string[] | ✓ | 非空 |

> 图片绑定流程：`python -I tools/link_units_images.py` 按 `research/selected-sprites.json` 的 `unit` 字段与本表 `name` 匹配填 `image`，再按脚本内人工核对的显式表填 `gallery`/补 `image`；只引用 `docs/public/media/units/` 下实际存在的文件。可重复运行（幂等，重跑前会重读 selected-sprites.json）。

## credits.json（对象）

```json
{ "sections": [ { "title": "Programming", "people": ["…"], "games": ["g1", "g2"] } ], "sources": [] }
```

`sections[].title` 分节名（`string | null`：`null` 表示原文无分组标题，页面以站点自定的「汉化人员」显示并注明）；`people` 名单；`games` 归属作品（允许两作）。顶层 `sources` 可为空数组。

## hotkeys.json（数组）

```json
[ { "action": "建造菜单", "keys": "B", "games": ["g1"], "source": "manual / 实测" } ]
```

## 管线行为

- `tools/build-content.mjs`：
  1. 读 `data/*.json`（宽松校验：JSON 损坏按空数组处理并告警）；
  2. 生成任务页 / 单位页 / 7 个固定分类页（分类页 URL 稳定：`/units/building/` 等）；
  3. **清理旧页面**：`docs/missions/<目录>`、`docs/units/<目录>` 中不属于当前数据的子目录会被删除；
  4. 对数据声明的每个媒体路径检查 `docs/public` 下是否存在；缺失 → 组件带 `:missing="true"` 渲染「素材未随站点发布」占位，**不报错**；
  5. 结束打印 `生成 N 页，缺失媒体 M 个`。
- `docs/.vitepress/config.ts`：导航 / 侧栏直接从 JSON 生成（任务按 `game` 分组、`order` 排序；单位按 `category` 分组）；数据目录可用 `DATA_DIR` 环境变量覆盖。
- `tools/check-content.mjs`：严格 schema 校验（games 取值、id 格式与唯一、sources 非空、media 键、按作品目录扫描），`npm run check`。
- 前端组件（`MuseumExplorer` / `UnitExplorer` 等）直接 `import` `data/*.json`，构建后随站点打包；数据更新需重新构建。

## 修改流程（给填数据的会话）

1. 改 `data/*.json`（遵循上述字段；新增条目 id 必须唯一）；
2. `npm run check` 通过；
3. `npm run content` 重新生成页面（会自动清理已删除条目）；
4. 需要的媒体放入 `docs/public/media/**`（图片入库；mp4/webm/wav/mp3/ogg 不入库）；
5. 若 `npm run build` 时希望用样例数据自测：`DATA_DIR=data/examples npm run build`，结束后执行 `npm run content` 恢复正式数据。
