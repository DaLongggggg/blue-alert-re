# report-data.md —— 战役/单位/说明书任务 最终汇报

（data 会话产出。详细证据见 research/notes-missions.md、notes-units.md；原始转储 mining-*.txt/json；说明书全文 manual-g1.md / manual-g2.md。）

## 一、交付物

| 文件 | 内容 |
|---|---|
| data/missions.json | 49 条：g1 战役 23（M01–M23）+ g1 联机 8 + g2 战役 11 + g2 联机 6 + 教程 M00×1（g12，两作同关） |
| data/units.json | 81 条：单位/建筑 56（含 ID、中文名、英文名、分类、InfoBox 说明）+ 武器名 25 |
| data/credits.json | 5 组：Programming(1)/Artwork and Animations(1)/Music and Sfx(1)/Special thanks to(11)/无标题汉化组(11)，共 26 人 |
| data/hotkeys.json | 26 条（两作说明书热键表 + 诀窍节补充，games=[g1,g2]） |
| research/manual-g1.md | g1 说明书全文（12 小节，含 8 张联机图中文名与逐图说明） |
| research/manual-g2.md | g2 说明书全文（12 小节；无联机图章节，其余文本与 g1 相同） |
| research/validate_data.py | `python -I research/validate_data.py` 校验 schema/id/games/sources/枚举/排序 —— 当前通过 |
| tools/*.py | mine_data_region.py / mine_disasm_scan.py / mine_parse_push_cases.py / mine_extract_doc_text.py / mine_build_data.py / mine_build_manuals.py（全部只读取证+生成，python -I 可重跑） |

## 二、关键结论（均有代码级证据）

1. **关卡对应关系完全确定**。全局任务号 `FUN_00424c00()`(g1 DAT_0070bde8) 同时驱动：关卡文件分发
   （跳表 g1 0x430e4c / g2 0x42f65c → `data\levels\mNN.sgv`→`.map/.til/.tmi/.srfa/.srf`）与简报 switch
   （g1 FUN_00438b90 直跳 0x439244；g2 经字节表 0x4375c8 → 0x437598）。
   - g1：领土 N ↔ 文件 MNN（N=1–22 有简报；**M23 有文件有分发无简报**，简报屏显示「没有资料」）。
   - g2：任务号→文件→领土 三者经字节表解耦：文件 M01–M04,M06,M07,M11,M12,M15,M20,M22 依次对应
     领土 01–11；无效任务号 {5,8,9,10,13,14,16–19,21} 恰为磁盘缺失文件。
2. **简报文本按 switch push 顺序归属**，物理相邻不可靠（例：g1 领土22压入的是「超级防线」决战文本）。
   g1 22 份 + g2 11 份的 基地代号/领土/难度/任务/战况 全部结构化完成，逐字段带 VA。
3. **实际标签是「领土」**（主会话备忘中的「预期」在两作中均不存在）；难度 g2 为「N / 10」制。
4. **单位 ID 两作完全一致**（g2 名称函数经字节表 0x42a178 映射，与 g1 FUN_0042b180 同表）；
   ID 空间 1–15 陆战 / 16–24 三种流入模式 / 25–29 炮塔 / 30–34 空袭 / 40–46 特种 / 100–108 建筑 /
   109–113 Top Sentry / 115 缩略地图。英文名函数（g1 字节表 0x42b108、g2 0x429b28）同 ID 同名，
   已全量核对——注意非直译：飞碟=Advancer、太阳能搜集器=Research Lab、飞机生产基地=Air Navigator。
5. InfoBox 说明两作逐字相同（g2 轻型防空条被字符串扫描分段，已拼接）；ID 40 飞碟两作皆无说明、
   20/21 共用同一条说明（原文如此）。
6. **联机图官方中文名**（热身行动/暴风雪/淘金热/大扫荡/原子弹行动/流星风暴/战火篇/岛屿之命）
   来自 g1 说明书「多人游戏任务」节，编号与 .net 文件名前缀一一对应；g2 说明书无此章节。
7. g1 制作名单的显示顺序由 FUN(0x42df50–0x42e337) push 顺序确定；汉化人员 11 人无分组标题，
   以「@」「!」空行标记与原团队分隔；g2 无汉化名单。

## 三、字段覆盖率

- missions 49 条：briefing 42/49（全部战役+教程；14 张联机图仅 g1 8 张有手册说明）、objective 33/33 战役全有、
  baseCode/expectedNo/difficulty 33/33、opponent 22/22（仅 g1 有「战场」字段）、title 8/49（仅 g1 联机图）。
- units 81 条：中文名 56/56 单位全有；英文名 55/56（缩略地图无英文表项）；InfoBox 说明 49/56
  （缺：飞碟、Top Sentry×5、缩略地图——原文即无）；weapons/stats 按铁律留空。
- credits 26 人 / hotkeys 26 条 / 说明书两作全文。

## 四、未能确定事项清单

1. 所有战役关的官方名称（title=null——「战场」是地区名，不构成关卡名）。
2. g1 M23 的战役定位（有文件、在分发表中，无简报文本；简报屏会显示「没有资料」）。
3. g2 六张联机图的中文名（说明书无联机章节；g2 手册其余部分沿用 g1 文案，连「22次任务」也未改）。
4. 武器名 ↔ 单位对应关系（weapons 留空）。
5. 单位数值属性（.data 无静态属性表；判定存于代码立即数或 SGV 数据，需逐类逆向或动态验证 → stats 留空，
   入口建议见 notes-units.md §6）。
6. mI/mO/mA/mB.sgv 用途（疑过场/菜单用图，未考证，未写入数据）。
7. 原文级疑点（照录未改）：g2 M12 难度「5 z 10」、M02 战况以「第二个工厂」截断、
   雷曼/罗曼译名不一致、20/21 说明共用、手册错字（「中选」「决窍」「能难取胜」「集结指分」）。

## 五、给后续页面会话的提示

1. **排序**：missions 已按 (g1→g2→g12, campaign→tutorial→network, order) 排序；g2 的 order=领土号
   （1–11），**与文件号不同**——展示"第 N 关"用 order，引用文件用 code/files。
2. games 字段语义：单作条目 games=[g1] 或 [g2]；M00 教程为 g12（games=[g1,g2]，game 字段填 g1）。
   units 全部条目 games=[g1,g2]（两作 ID/名称/说明完全一致）。
3. title 大多为 null：站点不要编造关卡名；可用「领土 NN · 战场：XX」式的组合标题，
   联机图用 title（g1）/nameEn（.net 文件名 slug 在 code 字段）。
4. units 的 summary 是一句话导语、description 是 InfoBox 原文（可直接引用展示）；
   category 七值可用于图标/筛选；image 留 null 待媒体会话填充（media 字段同理）。
5. hotkeys 与说明书文本高度重合：页面可引用 manual-g1.md 对应小节；
   注意热键表与「提示和诀窍」节对 数字键*/、- 的描述略有出入（两处均已原样收录）。
6. credits 第 5 组 title=null（原文无标题），渲染时建议显示为「汉化人员」之类由站点自定的标题，
   数据侧不预设。
7. 教程条目 briefing 是按地址倒序重建的整篇课文（'i '为讲解、'!'为步骤），换行保留，
   可直接按行渲染；若需逐步演示可按行拆分。
8. validate_data.py 可在 CI/构建前跑一遍（python -I research/validate_data.py）。

## 六、方法学备忘（复现路径）

- 简报映射：`python -I tools/mine_disasm_scan.py <exe> 0x438b90 0x439240 --pairs`（g1）/ 直接读
  research/mining-g1-briefing-switch.asm；g2 字节表读取见 notes-missions.md §1。
- 名称/说明映射：tools/mine_build_data.py 内嵌全部 ID→VA 映射（含出处），字符串正文从 mining 转储解析，
  改动后 `python -I tools/mine_build_data.py && python -I research/validate_data.py` 可复现全部数据。
- 说明书：tools/mine_extract_doc_text.py（UTF-16LE 游程）→ manual-g*-raw.md → tools/mine_build_manuals.py 整理成节。
