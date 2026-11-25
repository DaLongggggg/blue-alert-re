---
title: "第 01 关 · 战场：加拿大"
---

<GameBadges :games='["g1"]' />

# 第 01 关 · 战场：加拿大

<MissionMeta id="g1-m01" />

## 战况

首先要占领位于你方初始位置左边的太阳能搜集器。它将会给你提供大量的研究指数。你需要积500分指数来提升你方工厂的技术水平。随即，你要制造出强大的战斗单位。在你完成这项任务后，你的援军就来了。最后，你必须摧毁敌人位于岛上的总部。你必须先摧毁敌人的高射炮，这样我们的运兵飞船才能安全地把坦克运到岛上。

## 任务目标

- 任务：增加你的陆地作战单位的技术水平，并得到空中力量的援助。用它们去摧毁岛上敌人的总部。

## 地形底图

<MediaZoom src="/media/missions/m01-g1.jpg" ratio="4 / 3" alt="第 01 关 · 战场：加拿大 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m01-g1.mp4" poster="/media/missions/m01-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m01-g1.png" ratio="1" alt="第 01 关 · 战场：加拿大 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 1（0x438bbb 起 22 分支）push 顺序: 领土行0x4a54dc 基地行0x4a54bc 战况0x4a5394 任务0x4a5338（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M01.map（文件存在）
- g1 Data/Levels/M01.til（文件存在）
- g1 Data/Levels/M01.tmi（文件存在）
- g1 Data/Levels/M01.srfa（文件存在）
- g1 Data/Levels/M01.srf（文件存在）
- g1 Data/Levels/M01.edt（文件存在）
- g1 Data/Levels/M01.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M01.map`（map）
- `Data/Levels/M01.til`（til）
- `Data/Levels/M01.tmi`（tmi）
- `Data/Levels/M01.srfa`（srfa）
- `Data/Levels/M01.srf`（srf）
- `Data/Levels/M01.edt`（edt）
- `Data/Levels/M01.sgv`（sgv）

:::
