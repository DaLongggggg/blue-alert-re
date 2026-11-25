---
title: "第 18 关 · 战场：日本"
---

<GameBadges :games='["g1"]' />

# 第 18 关 · 战场：日本

<MissionMeta id="g1-m18" />

## 战况

注意！这个地区的敌人十分强大。他们有许多炮塔和空中作战单位。必须有一队重型陆地作战单位才能击败它。单独的作战单位是无法攻破敌人的防御的。

## 任务目标

- 任务：用大量的重型陆地作战单位击败敌人的防御。

## 地形底图

<MediaZoom src="/media/missions/m18-g1.jpg" ratio="4 / 3" alt="第 18 关 · 战场：日本 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m18-g1.mp4" poster="/media/missions/m18-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m18-g1.png" ratio="1" alt="第 18 关 · 战场：日本 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 18（0x438bbb 起 22 分支）push 顺序: 领土行0x4a40cc 基地行0x4a40b0 战况0x4a4024 任务0x4a3ff4（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M18.map（文件存在）
- g1 Data/Levels/M18.til（文件存在）
- g1 Data/Levels/M18.tmi（文件存在）
- g1 Data/Levels/M18.srfa（文件存在）
- g1 Data/Levels/M18.srf（文件存在）
- g1 Data/Levels/M18.edt（文件存在）
- g1 Data/Levels/M18.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M18.map`（map）
- `Data/Levels/M18.til`（til）
- `Data/Levels/M18.tmi`（tmi）
- `Data/Levels/M18.srfa`（srfa）
- `Data/Levels/M18.srf`（srf）
- `Data/Levels/M18.edt`（edt）
- `Data/Levels/M18.sgv`（sgv）

:::
