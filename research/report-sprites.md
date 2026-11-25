# 任务汇报：精灵图逆向与解码（sprites / Sprites2）

交付物：`tools/decode_sprites.py`、`research/FORMAT-sprites.md`、`research/sprite-map.json`、
`research/selected-sprites.json`、`_work/sprite-catalog/`（763 张联系表 + 清单）、
`docs/public/media/units/`（46 张）与 `docs/public/media/ui/`（17 张）。

## 一、解码成功/失败统计（g1+g2 全量）

- 资源包条目 + .tsp 共 793 个图形源：**完全解码 763，失败 0，部分失败 0**；
  另 30 个源只含合法空占位帧（w=0/h=0：units\1i_*、builds\mask 与 shadow 的
  sentry0X/_walker 等），共 26247 帧中 688 帧为空占位。
- 104 个 .po1/.po2 为每帧 (s16 dx,dy) 锚点表（非图形），按原样记录未解码。
- 所有行 RLE 均通过宽度/边界一致性校验；RGB565 配色经看图验证正确
  （蓝军坦克、金色建筑、绿色中文按钮）。
- g1/g2 差异：包内 381 条目仅 extras\chinese_actionsit、money、money_ 不同；
  .tsp 67/68 相同（g2 多 Extras\radar2.tsp，credits 内容不同、creditsB 大小写不同）。
  故单位/建筑精选图一律用 `-g12` 后缀。

## 二、格式结论（细节见 FORMAT-sprites.md）

1. 包：`[u32 0x01010101][u32 381]` + 条目（字符+10 存储的名字 + u32 偏移 + u32 大小），
   .data 原样拼接、无压缩。依据 FUN_00433250（Open）/FUN_00433570（GetEntry）。
2. 容器（包条目与 .tsp 同构）：`[u32 块大小][块][u32 0]`。依据 FUN_0044f520。
3. 块=单帧精灵：`u16 w, u16 h, s16 xoff, s16 yoff, 4×u16 设计字段, h×u32 行字偏移`
   （行字节位置 = 表值×2）。依据 FUN_004500e0（blit）+ compplay/Base/buttons 实测。
4. 行 RLE：`[u16 条目数][u16 首类型]` + 交替“透明跳过 u16 / 不透明数量 u16(+像素)”；
   .ps6/.tsp 带像素（RGB565），.msk/.sha 无像素（实心段）。行不必铺满宽度。
5. CHuffcomp（0x4338c0–0x434047）只用于存档，与精灵无关（已排除）。

## 三、InfoBox 子目录对应结论（看图确认）

- InfoBox/1 = 空袭放置投影（绿框 32 向）：Bmbf=轰炸机、Caryf=运兵飞船、Metf=星体炸弹、
  Stif=战斗机、Trif=连环轰炸机。
- InfoBox/2 = 建筑放置投影（绿框 32 向）：Air/Base/Heavy/Light/Med/Mine/Rlab/Walk/Wind
  对应 9 建筑，Tur1..5 对应炮塔。
- InfoBox/3/4/5 = 单位放置投影：Aa/Ar/Ca/Fl/Sp = 防空/炮兵/装甲坦克/喷火器/特派坦克，
  3/4/5 体型递增（疑轻/中/重）。
- InfoBox/6 = 能量/金币/研究流入 1..3 级动画（对应字符串 Energy/Gold/Research Influx）。
- InfoBox/7 = 特种单位：1..5 = 彩色旋转画像（对应 5W1..5W5 平台，顺序待考），
  N = 辐射标志车（对应 units\chn）。

## 四、单位映射要点

- 字母后缀即英文兵种首字母：a=炮兵(Artillery)、c=装甲坦克(Panzer)、f=喷火器(Flamer)、
  s=特派坦克(Special)、aa=防空(AntiAir)；数字 1/2/3=轻/中/重。
- chi1=飞碟(CUfo)、chw=阿基里斯(Achilles 步行机甲)为高置信；cha/chb/chc=美洲狮/
  格林机关炮/科迪亚克为形态推断（中置信）；chn（辐射车）与 5W1..5W5 名称待考（低置信）。
- 中文名依据：g2 .data 中文字符串 0x49e674–0x49e888 与英文注册序一一对应
  （防护大炮=Guard Cannon、集束炮塔=Defragmentator、离子炮塔=Plasma Mob、
  莱德风暴=LedStorm、连环轰炸机轰炸=Tripler Strafe 等）。

## 五、精选图清单摘要（63 张）

- units/ 46 张：15 标准单位（5 兵种×轻中重，蓝军）、cha/chb/chc/chi1/chn/chw 6 特战、
  5W1..5W5、运兵飞船/轰炸机/战斗机/连环轰炸机、9 蓝军建筑（总部/三工厂/飞机基地/
  机器人工厂/研究实验室/金矿/风能搜集器）、哨塔×3、炮塔×4。
- ui/ 17 张：主菜单 6 按钮（新游戏/读取游戏/教学模式/多人游戏/选项/退出游戏）、
  游戏内菜单 6 项（继续/读取/保存/选项/重新开始/主菜单）、设置界面 取消/确定、
  胜负整屏、光标、雷达框。
- 每张的来源、帧号、中文名、置信度记录在 selected-sprites.json；文件名含 -g12 后缀。

## 六、未解决问题

1. chn（辐射车）与 5W1..5W5 的中文名/用途；cha/chb/chc 的名称对应需与关卡/单位数据
   会话交叉验证。
2. tur_01..05、sentry01..03 与 Top Sentry G10/G30/G40/G50/A20 的具体对应。
3. tur_04 只有锚点表无精灵图；中文名“太阳能搜集器”找不到独立建筑精灵。
4. 块头 +8..+14 四个 u16（640/480/320/240 等）的准确语义（绘制不用）。
5. InfoBox/7 的 1..5 与 5W1..5W5 的顺序对应未逐一锚点比对。

## 七、给站点会话的提示

- 单位图均为原始分辨率透明 PNG（蓝军涂装，坦克类取朝向镜头的旋转帧）；
  绿军、开火、被毁、阴影等变体全量联系表在 `_work/sprite-catalog/`（763 张，文件名
  即源名），需要更多素材可直接从联系表对应的源帧提取（decode_sprites.py --select）。
- `_work/sprite-catalog/_manifest.json` 记录每个源的帧数、尺寸、空帧数。
