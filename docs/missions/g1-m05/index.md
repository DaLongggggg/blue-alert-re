---
title: "第 05 关 · 战场：中国"
---

<GameBadges :games='["g1"]' />

# 第 05 关 · 战场：中国

<MissionMeta id="g1-m05" />

## 战况

中国的基地建立在宇宙飞船碰撞的地区。由于敌人不断地袭击这个战略要地，我们的研究受到了很大的威胁。首先，用战斗机摧毁敌人的罗根炸弹。然后，占领位于你方总部北部的建筑。这样，你就会得到超级机器人和罗根炸弹的充足的供应。用它们占领敌人所有的建筑，最后，摧毁敌人的总部。

## 任务目标

- 任务：你的任务是消灭企图控制这个地区的每一个敌人，并占领敌人的建筑。

## 地形底图

<MediaZoom src="/media/missions/m05-g1.jpg" ratio="4 / 3" alt="第 05 关 · 战场：中国 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m05-g1.mp4" poster="/media/missions/m05-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m05-g1.png" ratio="1" alt="第 05 关 · 战场：中国 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 5（0x438bbb 起 22 分支）push 顺序: 领土行0x4a505c 基地行0x4a5040 战况0x4a4f38 任务0x4a4ef0（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M05.map（文件存在）
- g1 Data/Levels/M05.til（文件存在）
- g1 Data/Levels/M05.tmi（文件存在）
- g1 Data/Levels/M05.srfa（文件存在）
- g1 Data/Levels/M05.srf（文件存在）
- g1 Data/Levels/M05.edt（文件存在）
- g1 Data/Levels/M05.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M05.map`（map）
- `Data/Levels/M05.til`（til）
- `Data/Levels/M05.tmi`（tmi）
- `Data/Levels/M05.srfa`（srfa）
- `Data/Levels/M05.srf`（srf）
- `Data/Levels/M05.edt`（edt）
- `Data/Levels/M05.sgv`（sgv）

:::
