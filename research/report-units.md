# report-units.md —— 单位图鉴（units）任务最终汇报

> 任务会话：单位图鉴。完成时间：2026-11-25。自检截图存于 `_work/qa-units/shots/`（gitignore，未入库）。
> 验收状态：`npm run check` ✓、`npm run test:pipeline` ✓、`python -I research/validate_data.py` ✓、QA 构建 ✓（137 页 = 任务 49 + 单位 81 + 分类 7，**单位页数 81 = units 条目数 81**，缺失媒体 0）。

## 一、改了哪些文件

| 文件 | 改动 |
| --- | --- |
| `data/units.json` | 每条新增 3 个字段：`group`（展示分组）、`imageNote`（主图图注）、`gallery`（图集，`[{image,label}]`）；42 条填了 `image`、30 条填了 `gallery`。原有字段（含 sources、category、weapons/stats 留空铁律）全部未动 |
| `tools/link_units_images.py` | 新建。绑定脚本（`python -I` 运行，幂等可重跑）：精灵层按 selected-sprites.json 的 `unit` 与 name 匹配（精确/唯一前缀/括号注释中英文名反查），全息层按脚本内显式表绑定，另计算 `group`。含人工核对结论（DENY_BINDINGS / EXTRA_BINDINGS / HOLOGRAM_BINDINGS，均有理由注释） |
| `tools/build-content.mjs` | 仅动单位部分：新增 GROUP_LABELS / ID_RANGES 常量；`generateUnitPage` 重写（徽标+分类+分组+游戏内 ID 与 ID 段、summary、UnitGallery 主图+图集、description=null 时如实写「游戏内资料框无此条目的说明」/武器条目写「来自武器名表只有名称」、武器与属性空数据写「尚未考证」不显示空表格）；`generateCategoryPage` 按 group 拆分（武器名表条目集中为紧凑链接列表，不挤大卡片）。任务页部分（另一会话的）未动 |
| `docs/units/index.md` | 重写：导语 + UnitExplorer + 收录分组表 + 游戏内 ID 空间表（notes-units.md §1）+ 分类说明 + 图片说明 |
| `docs/units/weapons.md` | 重写：25 条武器名表（新组件 WeaponTable 渲染）+ 考证现状（含两作 .data 段地址），明确「对应关系未考证、未挂到单位名下」 |
| `docs/units/manual.md` | 重写（新兵手册）：鼠标设置/游戏热键设置（HotkeysTable）/主菜单（6+6 张界面按钮图）/主屏幕界面说明（雷达框体+光标图）/提示和诀窍/提速建议/联机指引；引文照录原文，错字旁注〔原文如此〕；热键表与诀窍节的 `*` `/` `-` 出入两处都保留并有 warning 块说明 |
| `docs/.vitepress/theme/index.ts` | 仅追加注册 3 个新组件：UnitGallery / HotkeysTable / WeaponTable（其余行未动） |
| `docs/.vitepress/theme/components/UnitGallery.vue` | 新建。单位页主图（深色展台、`image-rendering: pixelated` 最近邻放大）+ 可点击缩略图切换；`variant="grid"` 网格变体供手册界面图插页使用 |
| `docs/.vitepress/theme/components/HotkeysTable.vue` | 新建。渲染 data/hotkeys.json（26 条，按键 chip 样式）；出处含「两节表述略有出入」的行在备注列单独提示 |
| `docs/.vitepress/theme/components/WeaponTable.vue` | 新建。筛选 units.json 中 group=weapon 的 25 条，代码体链接网格 |
| `docs/.vitepress/theme/components/UnitCard.vue` | 无图时不再渲染 MediaImage 占位（紧凑卡片直接从文字开始，杜绝大占位框/裂图）；有图缩略图加深色展台底并 pixelated；有图集时显示「🖼 N 张图」 |
| `docs/.vitepress/theme/components/UnitExplorer.vue` | 新增「不限图片/有图片/无图片」筛选；搜索范围加入 summary；计数文案更新 |
| `docs/.vitepress/theme/components/MediaImage.vue` | compact 占位退化为一条细提示行（不再渲染大虚线框）；新增 `pixelated` 属性。非 compact 占位（任务页用）未动 |
| `research/DATA-MODEL.md` | units 表追加 `group` / `imageNote` / `gallery` 三字段说明与图片绑定流程注记 |
| `docs/public/media/units/holo-*.png` | 新增 40 张「资料框绿色全息图」单帧（经 `tools/decode_sprites.py --select` 从 `Data/Sprites2/InfoBox/**.tsp` 解码渲染，规格见 `_work/qa-units/spec-holo.json`） |

共享文件（build-content.mjs / theme\index.ts）改动前均重读了最新内容（另一会话其间升级过任务页生成器与组件注册，已避开其改动区）。

## 二、图片绑定情况（核心工作量，全部逐张看图核对）

**结果：81 条中 42 条有主图，30 条有图集（共发布 40 张新全息图 + 引用 46 张既有精灵中的 32 张）。**

### 2.1 绑定成功（核对通过）

- **蓝军涂装精灵 31 张**：陆战单位 15（防空×3/炮兵×3/坦克×3/喷火×3/特派×3，与 InfoBox 全息图形状逐一互证）、空袭 5（轰炸机/运兵飞船/战斗机/连环轰炸机/飞碟）、建筑 9（总部/金矿/太阳能搜集器/风能搜集器/轻中重工厂/飞机基地/机器人工厂）、阿基里斯、罗根炸弹（见 2.3）、缩略地图（雷达框体，ui/ 图）。
- **资料框绿色全息图 40 张**（InfoBox/\*.tsp 解码，g1/g2 逐文件 md5 相同故用 -g12 命名）：
  - 作主图 10 张：9 个生产模式（gold/research/energy 1-3，图标上金锭/脑纹球/闪电的数量即流入等级，非常直观）+ 星体炸弹风暴（绿色球体，无精灵可用）。
  - 作图集 30 张：9 建筑、15 陆战单位（InfoBox/3/4/5 = 轻/中/重，已用「5_Ar 双管=重型炮兵、5_Ca 三管=重型坦克、尺寸 3→4→5 递增」验证等级顺序）、空袭 4、阿基里斯（7/5 无远程武器双爪近战与说明唯一吻合）、罗根炸弹（7/N 履带车+顶部圆鼓与辐射车精灵同形）。

### 2.2 核对后放弃绑定（image=null，如实展示）

- **tank-cougar / tank-gatling / tank-kodiak 三张蓝色履带车精灵**（精灵会话原标注美洲狮/格林机关炮/科迪亚克，medium 推测）——**放弃，且是本任务最重要的发现**：InfoBox/7/1–5 的五张机器人全息图全部是**步行机甲**，与说明「超级机器人」吻合；这三张精灵是履带车体，形态对不上。原归属推断（cha/chb/chc=三机器人）与全息图证据矛盾，故科迪亚克/美洲狮/格林机关炮/空对空复仇者 4 条暂无图。
- **哨塔 sentry-01/02/03**：确认是 Top Sentry 系列，但 3 张图对不上 5 个型号（G10–G50），无法唯一归属。
- **turret-1/2/3/5 四张蓝色炮塔**：与全息图 Tur1–Tur5 逐形对应（tur_01↔Tur1 等），但 TurN→ID 25–29 的对应无证据，不猜。
- **unit-5w1–5w5 五张**：精灵会话即标注「名称待考」，无法归属。
- 25 条武器名：本质是名称表条目，无图像概念，页面如实说明。

### 2.3 两处「证据升级」的绑定（medium，已在脚本与图注中写明依据）

- `unit-radiation-g12.png` → **u-081 罗根炸弹**主图：辐射圆鼓+履带车体与 InfoBox/7/N 全息图同形；7/N 是特种家族（41–45 步行机器人之外）唯一履带条目。精灵会话原 low 置疑（罗根/复仇者/飞碟三选一），其中复仇者=步行机甲、飞碟=飞碟已排除，故升为罗根。
- `holo-achilles-g12.png`（InfoBox/7/5）→ 阿基里斯图集：五张全息图中唯一无远程武器、双爪近战，与说明「不能向敌人直接攻击…瞬间毁掉」唯一吻合。

## 三、新增字段说明（DATA-MODEL.md 已同步）

- `group`：`unit` 作战单位 24 / `building` 建筑与防御 22 / `mode` 生产模式 9 / `weapon` 武器名表 25 / `other` 其他 1。由脚本按既有字段推导（category=other 无 unitId→weapon；unitId 16–24→mode；category=other→other；building/factory/defense→building；其余→unit）。`category` 七值白名单原值未动。
- `imageNote`：主图图注（精灵取 selected-sprites 的 what 文案；全息图写「资料框绿色全息图…」）。
- `gallery`：`[{ "image": 路径, "label": 图注 }]`，页面 UnitGallery 可点击切换。

## 四、自检截图结论（_work/qa-units/shots/）

- **图鉴首页**（units-index.png）：筛选栏（搜索/作品/分类/有图）+ 计数「共 81 个条目（其中 42 个有游戏内图像）」；有图卡片显示精灵缩略图+「🖼 N 张图」，无图卡片紧凑无占位框，无裂图。
- **有图单位页**（u040.png）：最近邻放大的精灵在深色展台上清晰；缩略图可切换蓝色精灵/绿色全息图；meta 行含「分类·收录分组·游戏内 ID（ID 段：1–15 陆战单位）」；说明为 InfoBox 原文；武器/属性为「尚未考证」占位文案。
- **无图单位页**（u049.png 科迪亚克）：斜体一句「现有素材尚无法唯一确认归属，宁缺毋造」，无空表格无占位框。
- **武器条目页**（u055.png）与**武器一览**（weapons.png）：25 条代码体链接网格；考证现状含两作 .data 地址。
- **新兵手册**（manual.png / manual-full.png）：热键表 26 行含备注列出入提示；warning 块解释 `*` 键两节出入；主菜单/游戏内菜单按钮图、雷达框体、光标均正常显示；错字照录并旁注。
- **分类页**（cat-other.png）：缩略地图紧凑卡 + 25 条武器集中链接列表。
- **移动端**（browser-use 390×844 真实视口）：单位页无横向溢出、图片自适应。（注：直接 `chrome --window-size=390` 会被 Windows 最小窗宽钳到 ~500 导致截图裁切假象，已用真实 390 视口复验排除。）

## 五、未解决问题

1. **cha/chb/chc_blue（tank-cougar/gatling/kodiak）真实归属**：现存证据（InfoBox/7 全息图）只证明它们不是三台机器人；会话间已把可确认的两张机器人图（阿基里斯精灵、7/5 全息）绑定，其余 4 条机器人暂无图。建议精灵解码会话复核（InfoBox/7/1–5 内部顺序仍未知：7_1 多管≈格林机关炮、7_2 双肩炮≈科迪亚克、7_4 四管≈美洲狮只是形态猜测，未采信）。
2. Tur1–Tur5 全息图↔ID 25–29（炮塔五条）的对应、sentry-01–03↔Top Sentry G10–G50 的对应，需逆向建造菜单/攻击代码后才能绑定。
3. 空对空复仇者（42）：说明为「四枚地对空导弹」，7_1–7_4 中无一明确呈导弹巢形态，未绑定。
4. unit-5w1–5w5 用途未考（沿用精灵会话结论）。
5. 手册页面的「雷达和资料框」第 7 条原文脱「（」（已照录旁注）；热键表与诀窍节的 `*` `/` `-` 出入无裁定依据，两处并存。

## 六、需要主会话处理的校验器改动（建议，非阻塞）

`tools/check-content.mjs` 目前忽略未知字段，本次改动不阻塞 `npm run check`。若主会话愿意收紧，建议给 units 增加两条软校验（我可代劳，属于共享文件故未擅动）：

1. `group` 枚举校验：`unit|building|mode|weapon|other`（缺省视为 null，报错或警告皆可）。
2. `gallery` 形状校验：数组元素须为 `{ image: 以/开头的字符串, label?: 字符串 }`；`imageNote` 须为字符串或 null。
3. 另发现一个小坑供参考：生成页与手写页链接 `weapons.md` 必须写 `/units/weapons`（**不带尾斜杠**），否则 VitePress 死链检查报 82 个死链（本次已在生成器中修正）。

## 七、复现命令

```bash
python -I tools/link_units_images.py        # 重新绑定（先重读 selected-sprites.json，幂等）
npm run check && npm run content            # 校验 + 重新生成页面
npx vitepress build docs --outDir "E:/blue alert/blue-alert-re/_work/qa-units/dist"
```

全息图重渲染（如需换帧）：`_work/qa-units/spec-holo.json` + `python tools/decode_sprites.py --g1 <g1目录> --g2 <g2目录> --catalog <临时目录> --stats-only --select <spec> --media docs/public/media/units`（该脚本需 PIL，装在用户 site-packages，`python -I` 不可见，故未加 -I 运行；脚本自身对输入路径 resolve(strict=True)、输出 ensure_in 白名单校验）。
