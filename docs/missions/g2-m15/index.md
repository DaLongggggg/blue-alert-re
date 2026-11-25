---
title: "第 09 关"
---

<GameBadges :games='["g2"]' />

# 第 09 关

<MissionMeta id="g2-m15" />

## 战况

你的战役进行得非常精彩，胜利在望了。雷曼先生将自己的残余势力撤回了基地，你只有很短的时间消灭他的四个总部。呵呵，说起来容易，相信你一定能成功。

## 任务目标

- 任务：在40分钟之内消灭敌人的4个总部。

## 地形底图

<MediaZoom src="/media/missions/m15-g2.jpg" ratio="4 / 3" alt="第 09 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m15-g2.mp4" poster="/media/missions/m15-g2-cover.jpg" ratio="16 / 9" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m15-g2.png" ratio="1" alt="第 09 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g2 State of War - Warmonger.exe 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号15→case条目（push 顺序: 领土行0x4a1020 基地行0x4a1010 战况0x4a0f80 任务0x4a0f58，正文见 research/mining-g2-briefings.txt）
- 关卡分发表0x42f65c（0x42f386 起 23 项）: 任务号15→data\levels\m15.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应
- g2 Data/Levels/M15.map（文件存在）
- g2 Data/Levels/M15.til（文件存在）
- g2 Data/Levels/M15.tmi（文件存在）
- g2 Data/Levels/M15.srfa（文件存在）
- g2 Data/Levels/M15.srf（文件存在）
- g2 Data/Levels/M15.edt（文件存在）
- g2 Data/Levels/M15.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M15.map`（map）
- `Data/Levels/M15.til`（til）
- `Data/Levels/M15.tmi`（tmi）
- `Data/Levels/M15.srfa`（srfa）
- `Data/Levels/M15.srf`（srf）
- `Data/Levels/M15.edt`（edt）
- `Data/Levels/M15.sgv`（sgv）

:::
