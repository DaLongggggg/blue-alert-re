# notes-missions.md —— 战役数据挖掘笔记（g1/g2）

整理：data 会话（战役/单位/说明书任务）。所有地址均针对分析副本
`E:\rea-tools\targets\sow1\SOW1_StateOfWar.exe` / `...\sow2\SOW2_Warmonger.exe`
（image base 0x400000，.data 文件偏移 = VA − 0x400000）。
原始转储：`research/mining-g1-briefing-region.txt`、`research/mining-g1-briefing-switch.asm`、
`research/mining-g2-briefings.txt`、`research/mining-g2-briefing-switch.asm`、
`research/mining-g1-levelloader.asm`、`research/mining-g2-leveldispatch.asm`、`research/mining-g1-tutorial.txt`。

## 1. 任务号全局变量与两条分发链（核心证据）

- `FUN_00424c00`（0x424c00.c，g1）仅一句：`return DAT_0070bde8;` —— 全局「当前任务号」。
- **关卡文件分发**（g1，0x430b5a–0x430b6e）：
  `call FUN_00424c00; dec eax; cmp eax,0x16; ja 默认(0x430d48); jmp dword [eax*4+0x430e4c]`
  跳表 23 项：索引 0 → 0x430b70（push `data\levels\m01.sgv` 0x4a24e0）… 索引 22 → 0x430d29（push `m23.sgv` 0x4a2328）。
  即 **任务号 N(1..23) → data\levels\mNN.sgv**，随后加载器用 `data\levels\` 0x4a0d4c + 扩展名
  `.map`(0x4a0d5c)/`.til`(0x4a0d84)/`.srfa`(0x4a0d94)/`.tmi`(0x4a0dbc) 等拼出全部文件。
- **简报 switch**（g1，`FUN_00438b90`，0x438b90–0x439240）：
  参数 = 任务号（调用点 0x438ac3：`call FUN_00424c00; push eax; call FUN_00438b90`；
  另一调用点 0x439958）。`lea eax,[ebx-1]; cmp eax,0x15; ja 默认; jmp [eax*4+0x439244]`，22 项。
  每个 case 按固定顺序 push 四个字符串，分别存入 this+8/+0xC/+0x10/+0x14：
  **[领土行, 基地代号行, 战况正文, 任务行]**。
  → **任务号 N ↔ 领土 N ↔ mNN 文件**，同一全局驱动，无重排（g1 无字节表）。
- g2 同构：文件分发表 0x42f65c（0x42f386 起 23 项，索引 0→m01 0x49f5b8…索引 22→m23 0x49f400）；
  简报 switch `FUN`(0x437065)：`lea eax,[ecx-1]; cmp eax,0x15; ja 0x4373ae;
  mov cl, byte [eax+0x4375c8]; jmp [edx*4+0x437598]` —— **多了一层字节索引表 0x4375c8**：
  ```
  任务号: 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22
  case:  0  1  2  3  11 4  5  11 11 11 6  7  11 11 8  11 11 11 11 9  11 10
  ```
  case 0–10 = 领土 01–11；case 11 = 默认（0x4373ae：领土行=「没有资料」0x4a0ce4，其余=空串 0x4a64e4）。
  **无效任务号 {5,8,9,10,13,14,16,17,18,19,21} 恰好对应磁盘上不存在的 m05,m08,m09,m10,m13,m14,m16–m19,m21** —— 与
  g2 Data\Levels 实际文件（M00,M01–M04,M06,M07,M11,M12,M15,M20,M22）完全吻合。
- g1 侧验证：调用简报 switch 与文件分发的是同一个 `FUN_00424c00()` 返回值（0x438ac3 与 0x430b5a 两处）。

**结论（已写入每条 missions 的 sources）**：
- g1：领土 N（=expectedNo）↔ 文件 MNN；领土 01–22 有简报；M23 在分发表与文件中存在但无简报。
- g2：任务号 {1,2,3,4,6,7,11,12,15,20,22} ↔ 文件 M01,M02,M03,M04,M06,M07,M11,M12,M15,M20,M22，
  依次对应领土 01–11（expectedNo 即此序号，与文件号无关！）。
  例：g2 领土05 = 任务号6 = 文件 M06；领土11 = 任务号22 = 文件 M22。

## 2. 简报文本结构

- g1 基地行格式 `基地代号: X8A   战场：加拿大`；领土行 `领土: 01   难度等级: 1`（部分作「难度: N」，U6F/R4G）。
- g2 基地行仅 `基地代号: M7J1`（**无战场字段**）；领土行 `领土 : 11   难度等级 : 7 / 10`；
  H2E6（M12）原文为 `领土 : 08   难度等级 : 5 z 10` ——「z」为原版排版错误，difficulty 取 5，note 已注明。
- 主会话背景中说「预期: NN」，实际两作原文均为「**领土**」。expectedNo 字段按实际「领土」号填写。
- opponent 字段 = g1「战场：」后文本（地区/国名，**非官方关卡名**；且部分简报与战场地名对不上，
  如 H2E（巴西）的战况提到「波多鄂莱哥利」——汉化翻译不严谨，一律照录原文）。
- 简报文本与基地块的**物理相邻关系不可靠**（作者乱序存放）：必须以 switch 的 push 顺序为准。
  典型例：领土22（M7J 伊朗）压入的战况是「超级防线」决战文本 0x4a3bf4；领土01（X8A 加拿大）
  压入的是 0x4a5394（「占领太阳能搜集器…岛上总部」新手关文本）。
- M7J（领土22，g1）的战况即「最后任务/超级防线」文本；g2 领土11（M7J1）的任务/战况是
  「不要让罗曼先生逃走」（0x4a0cf0/0x4a0d20），文中又作「雷曼先生」（领土10 A6H2，翻译不一致，照录）。

## 3. M00（教程关）与 M23

- 短名表 `m00,m01,…,m30` 位于 g1 .data 0x4a0cd0（m30）…0x4a0d48（m00），升序各差 4 字节；
  关卡加载器跳表 0x420e14（31 项，`cmp eax,0x1e; ja 0x420d8b`）：索引 0 → 0x420b47 `push "m00"`，
  索引 1 → `push "m01"`… 错误分支 0x420d94 push `'Wrong level to load. Unable to open level %d'`（0x4a0ca0）。
  → M00 是加载器支持的合法关卡名，战役分发只用 1–23；**M00 = 教程关**（教程课文、
  `data\sounds\Tutorial\%d.wav` 0x4a1c40 均独立于战役链）。
- M23：文件齐全（.map/.til/.tmi/.srfa/.srf，另有分发表引到的 .sgv），但简报 switch 无条目
  （>22 走默认「没有资料」）。**M23 在战役中的定位未确定**（可能是结局后追加关或
  「超级防线」本体关，无文本证据）。
- 另有 `data\levels\mI.sgv`(0x4a1918)/`mO.sgv`(0x4a1944) 被 0x42d8c0/0x42dd72 引用，
  疑为过场（intro/outro）地图，未进一步考证；`data\levels\mA.sgv`(0x4a3b78)/`mB.sgv`(0x4a3b8c)
  在菜单流程 0x4388ef/0x4389b5 被引用，用途未确定。均未写入数据。

## 4. 教程课文（g1 0x4a1c80–0x4a22cc；g2 0x49ed38 起同文）

- 每条课文以 `i `（课程标题/讲解）或 `! `（操作步骤）开头；内存中按**地址降序 = 播放顺序**存放
  （锚点：0x4a22cc「欢迎你来到蓝色警戒教练课堂」为第一句，0x4a1c80「很好！你成功地掌握了全部课程」为最后一句）。
  课程：A 飞碟（0x4a2278）→ B 炮塔（0x4a2088）→ C 空中力量（0x4a1f7c）→ D 技术水平（0x4a1ed0）→ E 最后的任务（0x4a1d38）。
- 两作 M00 关卡文件完全相同；课文全文已并入 missions.json 的 g12-m00 条目 briefing（换行分隔）。

## 5. 联机地图

- g1 8 张：`Data/Levels/01-First Spark.net` … `08-Island of Fate.net`。
  **官方中文名与逐图说明来自 g1 说明书「多人游戏任务」节**（01 热身行动 / 02 暴风雪 / 03 淘金热 /
  04 大扫荡 / 05 原子弹行动 / 06 流星风暴 / 07 战火篇 / 08 岛屿之命）。编号对应依据：说明书按 01–08 顺序列出，
  与文件名前缀一一吻合。
- g2 6 张：`00-the first step.net` … `05-ground zero.net`。g2 说明书**没有**联机图章节（其余章节与 g1 相同，
  连「22次任务」的 g1 文案都原样保留——值得在站点文案中注意），因此 g2 联机图 title=null、仅 nameEn。
- 说明书另载联机方式：IPX 局域网 + TCP/IP（winipcfg 查 IP），服务器选图；已收录进 manual-g1.md。

## 6. 未确定 / 未写入数据的事项

1. 所有战役关 title=null：游戏与说明书中均无官方中文关卡名（「战场」是地区名）。
2. M23 的战役定位（见 §3）。
3. g2 联机图中文名；g1 联机图与 .net 文件的官方英文名仅来自文件名本身。
4. mI/mO/mA/mB.sgv 的用途。
5. 简报中出现的专名（波多鄂莱哥利、雷曼/罗曼、克里斯托帮、BEHO-SUNNS、UFSC）按原文照录，未做统一。
6. 联机图 08 手册原文「除非你是拿破仑再世，否则能难取胜」中「能难」为原文错字。
