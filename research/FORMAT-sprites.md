# 精灵图格式（State of War / 蓝色警戒 1·2）

适用对象：`Data\sprites.info` + `Data\sprites.data` 资源包全部 381 个条目，以及
`Data\Sprites2\**\*.tsp` 松散文件。两作格式完全相同（包内 381 条目中 378 条字节级一致；
.tsp 67/68 个相同）。解码器：`tools/decode_sprites.py`；逐源联系表：`_work/sprite-catalog/`。

## 1. 资源包（CMegaFile）

`sprites.info`（g1: 10876 字节）：

```
u32 0x01010101          魔数
u32 条目数 (=381)
条目 × N：
  文件名：每个字符存为 (ASCII + 10)，0x00 结尾（如 "units\1a_blue.ps6"）
  u32 内容在 sprites.data 中的偏移
  u32 内容大小
```

`sprites.data` = 各条目内容原样拼接（无压缩、无对齐）。381 条目首尾相接、无间隙，
末尾正好 33603260 字节（g2 为 33606444）。

依据：`FUN_00433250`（g1，0x433250–0x43356a，CMegaFile::Open）逐字节读魔数与条目，
字符做 `-10` 还原；`FUN_00433570`（GetEntry）按名字查索引后 `fseek+fread` 原样读出，
**无任何解压步骤**。包全局对象在 `0x7169f8`，名字查找在 `FUN_004336a0`。

## 2. 容器：块序列

每个条目内容与每个 .tsp 文件都是同一容器格式：

```
[ u32 块大小 ][ 块数据 ][ u32 块大小 ][ 块数据 ] ... [ u32 0 ]
```

u32 0 为结束标志。一个块 = 一帧图像（一个"精灵"）。`.tsp` 里的多个块通常是同屏
控件（如 001_buttons.tsp 的 18 块 = 6 个按钮 × 3 种状态）；单位 .ps6 的几十个块是
32 向旋转 × 动作状态。依据：`FUN_0044f520`（0x44f520–0x44f7a8，.tsp 加载器）：
读 u32==0 终止、块指针存入数组，块计数超限时报 "file is corrupted"。

## 3. 块（精灵帧）结构

```
偏移  类型        含义
+0   u16        宽 w
+2   u16        高 h（= 行数）
+4   s16        锚点 xoff（绘制时 dest_x - xoff）
+6   s16        锚点 yoff
+8   4×u16      设计基准字段（常见 640/480/320/240 或 320/240/160/120；绘制不用）
+16  u32 × h    行偏移表：第 i 行数据在块内的【字偏移】（字节位置 = 值×2）
...             各行 RLE 数据
```

依据：`FUN_004500e0`（0x4500e0，精灵 blit）：`w=param_4[0]`、`h=param_4[1]`、
`xoff=param_4[2]`、`yoff=param_4[3]`（带符号），行查表 `param_4[clipY*2+8..9]`
（即 +16 起、每行 4 字节、按 u16 索引直接寻址 → 字偏移×2=字节位置）。
例证：compplay.ps6 块 184 字节，表值 32..87（12 项），帧数据在块内字节 64..184。

`w=0 或 h=0` 的块是合法空占位帧（如 units\1i_*、builds\mask\sentry0*.msk、
tur_04 无图等，共 688 帧）；`.po1/.po2` 不是本容器格式（见 §6）。

## 4. 行 RLE（两种变体）

行结构（绘制函数逐条目交替解析）：

```
u16 条目数 n
u16 首条目类型 t（0=透明跳过，1=不透明）
随后 n 个条目按 t 起交替：
  偶数条目（透明）：u16 跳过像素数
  奇数条目（不透明）：u16 像素数 k
```

- **含像素变体**（.ps6 / .tsp）：不透明条目的 k 后跟 k 个 u16 像素（RGB565）。
  行不必覆盖整宽，剩余像素透明。
- **无像素变体**（.msk / .sha）：不透明条目只有数量 k，无像素数据（整段填实心色；
  .sha 为阴影、.msk 为字体遮罩/选择遮罩）。

像素格式：RGB565（R=11..15, G=5..10, B=0..4）。绘制代码里有 565 与 555 两套掩码
（0xF800/0x7E0/0x1F 与 0x7C00/0x3E0/0x1F，按显示模式选择）；实测按 565 解码颜色正确
（蓝军坦克蓝色、金色建筑、绿字中文按钮均正常）。加亮层（001_lights 等）在
565 分支以饱和加法混合到背景。

依据：`FUN_004500e0` 主循环 —— 读 `n`、`t`，`t==0` 时 `x += next_u16`，
`t==1` 时读 `k` 并复制 k 像素（565 加法分支 / 覆盖分支），类型自动交替、无逐条类型字节。

## 5. 与哈夫曼的关系（澄清）

`CHuffcomp`（构造 0x4338c0，压缩 0x433970，解压 0x433b90，位写器 0x434580）**只用于
存档**（savegame）：调用者为 FUN_00421a50（保存）/0x422400（读取）。压缩流格式为
`u32 原始大小 + u16 根节点 + 每节点 [u8 符号][u16 child0][u16 child1]×N + 位流`。
精灵资源不走哈夫曼。

## 6. .po1 / .po2 锚点表

单位附带的 `units\*.po1/.po2`（128/256/384/512/768 字节 = 每帧 8 字节）是 **每帧一组
(s16 dx, dy)** 的锚点/炮口偏移表，与 32 向旋转帧一一对应。例如 units\1a.po1 =
32 组 s16 对，围绕 (0,0) 旋转分布。不是容器格式，解码器按原样跳过（--list 可见）。

## 7. 条目命名 → 内容映射

### 单位（units\）

| 前缀 | 兵种（中文名） | 依据 |
|---|---|---|
| `1a/2a/3a` | 轻/中/重型炮兵（Artillery） | 看图（大口径火炮）+ g2 字符串名序 |
| `1c/2c/3c` | 轻/中/重型装甲坦克（Panzer） | 看图（履带坦克）+ "Panzer" |
| `1f/2f/3f` | 轻/中/重型喷火器（Flamer） | 看图（燃料罐+喷嘴）+ "Flamer" |
| `1s/2s/3s` | 轻/中/重型特派坦克（Special） | 看图（轮式）+ "Special" |
| `1aa/2aa/3aa` | 轻/中/重型防空设施（AntiAir） | 看图（双管高炮）+ "AntiAir" |
| `cha/chb/chc` | 特战战车（推测：美洲狮/格林机关炮/科迪亚克） | 看图形态；EN 名串 0x4a13a8–0x4a13c8 |
| `chi1` | 飞碟（UFO） | exe 类名 `CUfo` + 圆盘造型 |
| `chn` | 辐射标志特种车（待考：罗根炸弹载体/空对空复仇者/Advancer） | 看图辐射标志，无字符串对应 |
| `chw` | 阿基里斯（Achilles）巨型步行机甲 | 字符串 "Achilles"+'TYPE: Walker robot'+walker 音效路径 |
| `5w1..5w5` | 5 种小型多足/气垫平台（名称待考，InfoBox/7 有其彩色画像） | 看图 |
| `tur_01..05` | Top Sentry 炮塔系列（G10/G30/G40/G50/A20 与哪号对应待考） | 字符串 'Top Sentry G10' 等 + 看图 |

变体后缀：`_blue`（蓝军）`_gren`（绿军）`_fire`（开火）`_blueboom/_grenboom`（被毁）
`_bluesmoke/_grensmoke`（损毁烟）`.sha`（阴影）`.po1/.po2`（锚点）。
块数规律：普通单位 32 帧=32 向；64/96 帧=32 向×2/3 状态；chw 160 帧=行走动画。

英文名注册序列（g1 0x42ab30–0x42ae48，函数表形式）：CarryAll、Meteor Storm、
Bomber Attack、Defragmentator、LedStorm、Plasma Mob、A.A. Defence、Guard Cannon、
Rogon Bomb、Advancer、Achilles、Gatling、Cougar、A.A. Avenger、Kodiak、
重/中/轻型 Special、Flamer、Panzer、Artillery、AntiAir、Radar。
g2 中文对照（0x49e674–0x49e888）：风能搜集器、太阳能搜集器、金矿、飞机生产基地、
机器人工厂、重型/中型/轻型工厂、总部、战斗机袭击、连环轰炸机轰炸（=Tripler Strafe）、
运兵飞船、星体炸弹风暴、轰炸机袭击（=Bomber Attack）、集束炮塔（=Defragmentator）、
莱德风暴（=LedStorm）、离子炮塔（=Plasma Mob）、防空设施（=A.A. Defence）、
防护大炮（=Guard Cannon）、罗根炸弹（=Rogon Bomb）、飞碟、阿基里斯、格林机关炮、
美洲狮、空对空复仇者、科迪亚克、重/中/轻型特派坦克/喷火器/装甲坦克/炮兵/防空设施、
缩略地图（=Radar）。注意：中文表无 "Advancer"。

### 建筑（builds\）

`_base`=总部(Headquarters)、`_wind`=风能搜集器(WindTrap)、`_mine`=金矿(Gold Mine)、
`_air`=飞机生产基地(Air Navigator)、`_walker`=机器人工厂(Walker Factory)、
`_rlab`=研究实验室(Research Lab)、`_heavy/_med/_light`=重/中/轻型工厂、
`sentry01..03`=哨塔（Top Sentry A20/G10 系列之一，具体对应待考）。
`builds\blue\`=蓝军实体图、`builds\green\`=绿军实体图、`builds\mask\`=遮罩层、
`builds\shadow\`=阴影层。块 0=施工地基，中段=建成态，尾部=受损态。
待考：中文名"太阳能搜集器"在 EN 表中无直接对应（疑与 Research Lab 的中文版定位有关）。

### InfoBox 子目录结论（看图确认）

| 子目录 | 内容 |
|---|---|
| `InfoBox/1/` | 空袭单位放置投影（绿色线框 32 向）：Bmbf=轰炸机、Caryf=运兵飞船、Metf=星体炸弹、Stif=战斗机、Trif=连环轰炸机 |
| `InfoBox/2/` | 建筑放置投影（绿色线框 32 向）：Air/Base/Heavy/Light/Med/Mine/Rlab/Tur1-5/Walk/Wind，与 buildings\ 各建筑一一对应；Tur1-5 对应炮塔 |
| `InfoBox/3/4/5/` | 单位放置投影（绿色线框）：Aa=防空、Ar=炮兵、Ca=装甲坦克、Fl=喷火器、Sp=特派坦克；3/4/5 体型递增（疑轻/中/重） |
| `InfoBox/6/` | 资源流入指示动画：energy/gold/research 1..3 ↔ 字符串 "Energy/Gold/Research Influx 1..3"（中文版：能量/金币/研究指数流入 1..3） |
| `InfoBox/7/` | 特种单位：1..5=彩色旋转画像（步行平台，对应 5W1..5W5，顺序待考）；N=辐射标志车（对应 chn） |

## 8. 解码算法（decode_sprites.py 已实现）

1. 解析 sprites.info → 条目表；.tsp 按相对路径枚举。
2. 容器走块序列；块头取 w/h/xoff/yoff 与行偏移表。
3. 逐行按 [n][t] 交替解析；.msk/.sha 用无像素变体；像素 RGB565→RGBA，
   未覆盖像素 alpha=0；空块（w=0/h=0）记为空帧。
4. `--list` 列条目；`--decode all|关键词` 输出每源联系表 PNG 到
   `_work\sprite-catalog\`（<源名>-<g1|g2>.png）+ `_manifest.json`；
   `--select spec.json --media docs\public\media` 按清单挑帧输出精选图。

## 9. 统计（g1+g2 全量）

- 容器源 793 个：完全解码 763、仅空占位帧 30（1i 单位、sentry/walker 的 msk/sha 等）、
  失败 0；部分失败 0（全部行 RLE 解析通过）。
- 帧 26247 个，其中空占位帧 688。
- .po1/.po2 锚点表 104 个（52×2）按原样记录。
- 像素格式 RGB565、透明=行未覆盖，全量看图验证（蓝军/绿军/建筑/中文 UI 色彩正常）。

## 10. 未解决问题

1. chn（辐射车）与 5W1..5W5 的中文名/用途；cha/chb/chc 与 美洲狮/格林机关炮/科迪亚克
   的一一对应是形态推断（待关卡/单位数据会话交叉验证）。
2. tur_01..05 / sentry01..03 与 Top Sentry G10/G30/G40/G50/A20 的具体对应。
3. tur_04 只有 .po1/.po2，无精灵图（运行时可能复用其他图或为占位）。
4. 中文名"太阳能搜集器"对应的建筑精灵（EN 表只有 WindTrap/Research Lab）。
5. 块头 +8..+14 四个 u16（640/480/320/240 等）的准确语义（绘制不用，疑为设计基准屏）。
6. InfoBox/7 的 1..5 与 5W1..5W5 的顺序对应（画像形态相近，未逐一比对锚点）。
