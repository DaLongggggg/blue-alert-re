---
title: "第 07 关"
---

<GameBadges :games='["g2"]' />

# 第 07 关

<MissionMeta id="g2-m11" />

## 战况

这次的任务比较困难，因为敌方拥有大量的空中力量。我们的空中力量不占优势。但是，我们可以巧妙的调集炮塔资源，打击敌人。

## 任务目标

- 任务：消灭敌人，占领他们的基地。

## 地形底图

<MediaZoom src="/media/missions/m11-g2.jpg" ratio="4 / 3" alt="第 07 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m11-g2.mp4" poster="/media/missions/m11-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m11-g2.png" ratio="1" alt="第 07 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号11→case条目（push 顺序: 领土行0x4a1208 基地行0x4a11f8 战况0x4a1180 任务0x4a115c，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号11→data\levels\m11.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M11.map（文件存在）
- g2 Data/Levels/M11.til（文件存在）
- g2 Data/Levels/M11.tmi（文件存在）
- g2 Data/Levels/M11.srfa（文件存在）
- g2 Data/Levels/M11.srf（文件存在）
- g2 Data/Levels/M11.edt（文件存在）
- g2 Data/Levels/M11.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M11.map`（map）
- `Data/Levels/M11.til`（til）
- `Data/Levels/M11.tmi`（tmi）
- `Data/Levels/M11.srfa`（srfa）
- `Data/Levels/M11.srf`（srf）
- `Data/Levels/M11.edt`（edt）
- `Data/Levels/M11.sgv`（sgv）

:::
