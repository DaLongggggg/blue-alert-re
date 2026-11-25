---
title: "第 06 关"
---

<GameBadges :games='["g2"]' />

# 第 06 关

<MissionMeta id="g2-m07" />

## 战况

首先尽量多的控制金矿，你需要足够的资源保护基地30分钟。如果你能坚持到这一刻的话，就会获得支援，从而消灭敌方的总部。援军还包括金钱，所有这些援助将帮助你成功的完成任务。

## 任务目标

- 任务：保护基地30分钟，一旦援军到达，迅速破坏敌方的总部。

## 地形底图

<MediaZoom src="/media/missions/m07-g2.jpg" ratio="4 / 3" alt="第 06 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m07-g2.mp4" poster="/media/missions/m07-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m07-g2.png" ratio="1" alt="第 06 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号7→case条目（push 顺序: 领土行0x4a1320 基地行0x4a1310 战况0x4a1268 任务0x4a1228，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号7→data\levels\m07.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M07.map（文件存在）
- g2 Data/Levels/M07.til（文件存在）
- g2 Data/Levels/M07.tmi（文件存在）
- g2 Data/Levels/M07.srfa（文件存在）
- g2 Data/Levels/M07.srf（文件存在）
- g2 Data/Levels/M07.edt（文件存在）
- g2 Data/Levels/M07.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M07.map`（map）
- `Data/Levels/M07.til`（til）
- `Data/Levels/M07.tmi`（tmi）
- `Data/Levels/M07.srfa`（srfa）
- `Data/Levels/M07.srf`（srf）
- `Data/Levels/M07.edt`（edt）
- `Data/Levels/M07.sgv`（sgv）

:::
