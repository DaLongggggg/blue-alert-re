---
title: "第 02 关"
---

<GameBadges :games='["g2"]' />

# 第 02 关

<MissionMeta id="g2-m02" />

## 战况

我们得到消息雷曼先生藏在此区域的某个地方。因此，为完成此项任务，我们打算准备一队重型机器人，来破坏敌方所有的抵抗力量和建筑。需要特别注意，在此任务中没有援军，并且敌人的作战力量优于我方。

## 任务目标

- 任务：用少量的重型战斗机器人消灭敌方所有的作战单位和建筑。

## 注意

战况正文以「第二个工厂」结尾，原文即在此截断。

## 地形底图

<MediaZoom src="/media/missions/m02-g2.jpg" ratio="4 / 3" alt="第 02 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m02-g2.mp4" poster="/media/missions/m02-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m02-g2.png" ratio="1" alt="第 02 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号2→case条目（push 顺序: 领土行0x4a1774 基地行0x4a1764 战况0x4a16a8 任务0x4a1668，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号2→data\levels\m02.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M02.map（文件存在）
- g2 Data/Levels/M02.til（文件存在）
- g2 Data/Levels/M02.tmi（文件存在）
- g2 Data/Levels/M02.srfa（文件存在）
- g2 Data/Levels/M02.srf（文件存在）
- g2 Data/Levels/M02.edt（文件存在）
- g2 Data/Levels/M02.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M02.map`（map）
- `Data/Levels/M02.til`（til）
- `Data/Levels/M02.tmi`（tmi）
- `Data/Levels/M02.srfa`（srfa）
- `Data/Levels/M02.srf`（srf）
- `Data/Levels/M02.edt`（edt）
- `Data/Levels/M02.sgv`（sgv）

:::
