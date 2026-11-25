---
title: "第 17 关 · 战场：南韩"
---

<GameBadges :games='["g1"]' />

# 第 17 关 · 战场：南韩

<MissionMeta id="g1-m17" />

## 战况

我们要用一小组力量进攻南韩的这个基地。你的任务是用这些军事力量控制富产金矿的东部。这样，你就会得到丰富的金钱。用它们防御，直到援军到达，它们会送来金钱、研究指数和装满重型武器的运兵飞船。在援军到达后，立即升级工厂。然后，你就可以很容易地消灭敌人了。

## 任务目标

- 任务：你必须坚守30分钟。当援军到达后，立即升级你的工厂，并摧毁敌人的总部。

## 地形底图

<MediaZoom src="/media/missions/m17-g1.jpg" ratio="4 / 3" alt="第 17 关 · 战场：南韩 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m17-g1.mp4" poster="/media/missions/m17-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m17-g1.png" ratio="1" alt="第 17 关 · 战场：南韩 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 17（0x438bbb 起 22 分支）push 顺序: 领土行0x4a4248 基地行0x4a422c 战况0x4a4130 任务0x4a40e4（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M17.map（文件存在）
- g1 Data/Levels/M17.til（文件存在）
- g1 Data/Levels/M17.tmi（文件存在）
- g1 Data/Levels/M17.srfa（文件存在）
- g1 Data/Levels/M17.srf（文件存在）
- g1 Data/Levels/M17.edt（文件存在）
- g1 Data/Levels/M17.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M17.map`（map）
- `Data/Levels/M17.til`（til）
- `Data/Levels/M17.tmi`（tmi）
- `Data/Levels/M17.srfa`（srfa）
- `Data/Levels/M17.srf`（srf）
- `Data/Levels/M17.edt`（edt）
- `Data/Levels/M17.sgv`（sgv）

:::
