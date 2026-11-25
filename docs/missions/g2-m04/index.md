---
title: "第 04 关"
---

<GameBadges :games='["g2"]' />

# 第 04 关

<MissionMeta id="g2-m04" />

## 战况

在这个任务中，敌人的基地有很强的防御系统。你的工厂能生产破坏性极强的罗根炸弹，再借助3个飞碟的帮助，将有效破坏敌人的防御系统。你必须尽快，在35分钟内完成任务。

## 任务目标

- 任务：在35分钟之内，破坏敌人的防御系统和建筑。

## 地形底图

<MediaZoom src="/media/missions/m04-g2.jpg" ratio="4 / 3" alt="第 04 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m04-g2.mp4" poster="/media/missions/m04-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m04-g2.png" ratio="1" alt="第 04 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号4→case条目（push 顺序: 领土行0x4a1578 基地行0x4a1568 战况0x4a14c8 任务0x4a1494，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号4→data\levels\m04.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M04.map（文件存在）
- g2 Data/Levels/M04.til（文件存在）
- g2 Data/Levels/M04.tmi（文件存在）
- g2 Data/Levels/M04.srfa（文件存在）
- g2 Data/Levels/M04.srf（文件存在）
- g2 Data/Levels/M04.edt（文件存在）
- g2 Data/Levels/M04.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M04.map`（map）
- `Data/Levels/M04.til`（til）
- `Data/Levels/M04.tmi`（tmi）
- `Data/Levels/M04.srfa`（srfa）
- `Data/Levels/M04.srf`（srf）
- `Data/Levels/M04.edt`（edt）
- `Data/Levels/M04.sgv`（sgv）

:::
