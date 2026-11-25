---
title: "第 01 关"
---

<GameBadges :games='["g2"]' />

# 第 01 关

<MissionMeta id="g2-m01" />

## 战况

占领地图中间的太阳能收集器，尽快收集500点研究指数。这样，你就能升级工厂，制造出更好的作战单位。第二个工厂升级后，你就能制造出空中力量了。用战斗机破坏炮塔，你的坦克就可以安全的通过敌方领域。如果你设法破坏了敌人的总部，你的任务就完成了。

## 任务目标

- 任务：收集1000点研究指数，升级工厂，消灭敌人总部。

## 地形底图

<MediaZoom src="/media/missions/m01-g2.jpg" ratio="4 / 3" alt="第 01 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m01-g2.mp4" poster="/media/missions/m01-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m01-g2.png" ratio="1" alt="第 01 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号1→case条目（push 顺序: 领土行0x4a18c4 基地行0x4a18b4 战况0x4a17c8 任务0x4a1794，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号1→data\levels\m01.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M01.map（文件存在）
- g2 Data/Levels/M01.til（文件存在）
- g2 Data/Levels/M01.tmi（文件存在）
- g2 Data/Levels/M01.srfa（文件存在）
- g2 Data/Levels/M01.srf（文件存在）
- g2 Data/Levels/M01.edt（文件存在）
- g2 Data/Levels/M01.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M01.map`（map）
- `Data/Levels/M01.til`（til）
- `Data/Levels/M01.tmi`（tmi）
- `Data/Levels/M01.srfa`（srfa）
- `Data/Levels/M01.srf`（srf）
- `Data/Levels/M01.edt`（edt）
- `Data/Levels/M01.sgv`（sgv）

:::
