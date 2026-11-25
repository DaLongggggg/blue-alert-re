---
title: "第 14 关 · 战场：委内瑞拉"
---

<GameBadges :games='["g1"]' />

# 第 14 关 · 战场：委内瑞拉

<MissionMeta id="g1-m14" />

## 战况

敌人在这个地区的陆地作战单位非常多。首先，你要掌握许多金矿和飞机生产基地。然后，用战斗机摧毁敌人的高射炮，这样，你就能安全地用运兵飞船把坦克运送到敌人的领土上了。

## 任务目标

- 任务：用运兵飞船把我方的陆地作战单位运送到敌人的领土上。

## 地形底图

<MediaZoom src="/media/missions/m14-g1.jpg" ratio="4 / 3" alt="第 14 关 · 战场：委内瑞拉 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m14-g1.mp4" poster="/media/missions/m14-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m14-g1.png" ratio="1" alt="第 14 关 · 战场：委内瑞拉 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 14（0x438bbb 起 22 分支）push 顺序: 领土行0x4a4558 基地行0x4a4538 战况0x4a4494 任务0x4a4458（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M14.map（文件存在）
- g1 Data/Levels/M14.til（文件存在）
- g1 Data/Levels/M14.tmi（文件存在）
- g1 Data/Levels/M14.srfa（文件存在）
- g1 Data/Levels/M14.srf（文件存在）
- g1 Data/Levels/M14.edt（文件存在）
- g1 Data/Levels/M14.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M14.map`（map）
- `Data/Levels/M14.til`（til）
- `Data/Levels/M14.tmi`（tmi）
- `Data/Levels/M14.srfa`（srfa）
- `Data/Levels/M14.srf`（srf）
- `Data/Levels/M14.edt`（edt）
- `Data/Levels/M14.sgv`（sgv）

:::
