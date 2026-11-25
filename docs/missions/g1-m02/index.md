---
title: "第 02 关 · 战场：摩洛哥"
---

<GameBadges :games='["g1"]' />

# 第 02 关 · 战场：摩洛哥

<MissionMeta id="g1-m02" />

## 战况

我们的运兵飞船被击落了！他们担负着运送一个小分队占领摩洛哥的任务。因此，你就必须承担起占领摩洛哥基地的任务。使用飞碟，逐步占领敌人的建筑，最后，摧毁敌人的总部。

## 任务目标

- 任务：占领敌人的建筑，聚集重兵力摧毁敌人的总部。

## 地形底图

<MediaZoom src="/media/missions/m02-g1.jpg" ratio="4 / 3" alt="第 02 关 · 战场：摩洛哥 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m02-g1.mp4" poster="/media/missions/m02-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m02-g1.png" ratio="1" alt="第 02 关 · 战场：摩洛哥 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 2（0x438bbb 起 22 分支）push 顺序: 领土行0x4a5320 基地行0x4a5300 战况0x4a525c 任务0x4a5228（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M02.map（文件存在）
- g1 Data/Levels/M02.til（文件存在）
- g1 Data/Levels/M02.tmi（文件存在）
- g1 Data/Levels/M02.srfa（文件存在）
- g1 Data/Levels/M02.srf（文件存在）
- g1 Data/Levels/M02.edt（文件存在）
- g1 Data/Levels/M02.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M02.map`（map）
- `Data/Levels/M02.til`（til）
- `Data/Levels/M02.tmi`（tmi）
- `Data/Levels/M02.srfa`（srfa）
- `Data/Levels/M02.srf`（srf）
- `Data/Levels/M02.edt`（edt）
- `Data/Levels/M02.sgv`（sgv）

:::
