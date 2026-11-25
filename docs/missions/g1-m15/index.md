---
title: "第 15 关 · 战场：埃及"
---

<GameBadges :games='["g1"]' />

# 第 15 关 · 战场：埃及

<MissionMeta id="g1-m15" />

## 战况

敌人的援军就要到达我方埃及西部的基地了。在他们到达之前，占领这个基地。你仅仅有30分钟的时间。充分利用空中力量完成这次任务。

## 任务目标

- 任务：用30分钟的时间占领敌人的基地。

## 地形底图

<MediaZoom src="/media/missions/m15-g1.jpg" ratio="4 / 3" alt="第 15 关 · 战场：埃及 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m15-g1.mp4" poster="/media/missions/m15-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m15-g1.png" ratio="1" alt="第 15 关 · 战场：埃及 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 15（0x438bbb 起 22 分支）push 顺序: 领土行0x4a4440 基地行0x4a4424 战况0x4a43a8 任务0x4a4380（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M15.map（文件存在）
- g1 Data/Levels/M15.til（文件存在）
- g1 Data/Levels/M15.tmi（文件存在）
- g1 Data/Levels/M15.srfa（文件存在）
- g1 Data/Levels/M15.srf（文件存在）
- g1 Data/Levels/M15.edt（文件存在）
- g1 Data/Levels/M15.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M15.map`（map）
- `Data/Levels/M15.til`（til）
- `Data/Levels/M15.tmi`（tmi）
- `Data/Levels/M15.srfa`（srfa）
- `Data/Levels/M15.srf`（srf）
- `Data/Levels/M15.edt`（edt）
- `Data/Levels/M15.sgv`（sgv）

:::
