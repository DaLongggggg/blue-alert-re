---
title: "第 03 关"
---

<GameBadges :games='["g2"]' />

# 第 03 关

<MissionMeta id="g2-m03" />

## 战况

这次任务是保护罗根炸弹通过这个地区，你只有几个作战单位随行。特别要注意敌人的空中力量会毫不留情的破坏你的护航行动的。

## 任务目标

- 任务：抵制敌人的进攻，完成护航任务。

## 地形底图

<MediaZoom src="/media/missions/m03-g2.jpg" ratio="4 / 3" alt="第 03 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m03-g2.mp4" poster="/media/missions/m03-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m03-g2.png" ratio="1" alt="第 03 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号3→case条目（push 顺序: 领土行0x4a1648 基地行0x4a1638 战况0x4a15c0 任务0x4a1598，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号3→data\levels\m03.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M03.map（文件存在）
- g2 Data/Levels/M03.til（文件存在）
- g2 Data/Levels/M03.tmi（文件存在）
- g2 Data/Levels/M03.srfa（文件存在）
- g2 Data/Levels/M03.srf（文件存在）
- g2 Data/Levels/M03.edt（文件存在）
- g2 Data/Levels/M03.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M03.map`（map）
- `Data/Levels/M03.til`（til）
- `Data/Levels/M03.tmi`（tmi）
- `Data/Levels/M03.srfa`（srfa）
- `Data/Levels/M03.srf`（srf）
- `Data/Levels/M03.edt`（edt）
- `Data/Levels/M03.sgv`（sgv）

:::
