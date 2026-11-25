---
title: "第 10 关 · 战场：澳大利亚"
---

<GameBadges :games='["g1"]' />

# 第 10 关 · 战场：澳大利亚

<MissionMeta id="g1-m10" />

## 战况

敌人以迅雷不及掩耳的速度占领了我方澳大利亚的南部联络中心，使我们的卫星失去了与其他卫星的联络。敌人的炮塔防御非常强大，但是由于他们急于求成，拥有的空中力量并不多，所以你可以得到大量的空中力量支持。用它们去收复失地吧！

## 任务目标

- 任务：用你的空中力量除去敌人的防御，摧毁他们的总部。

## 地形底图

<MediaZoom src="/media/missions/m10-g1.jpg" ratio="4 / 3" alt="第 10 关 · 战场：澳大利亚 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m10-g1.mp4" poster="/media/missions/m10-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m10-g1.png" ratio="1" alt="第 10 关 · 战场：澳大利亚 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 10（0x438bbb 起 22 分支）push 顺序: 领土行0x4a4a48 基地行0x4a4a28 战况0x4a494c 任务0x4a4914（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M10.map（文件存在）
- g1 Data/Levels/M10.til（文件存在）
- g1 Data/Levels/M10.tmi（文件存在）
- g1 Data/Levels/M10.srfa（文件存在）
- g1 Data/Levels/M10.srf（文件存在）
- g1 Data/Levels/M10.edt（文件存在）
- g1 Data/Levels/M10.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M10.map`（map）
- `Data/Levels/M10.til`（til）
- `Data/Levels/M10.tmi`（tmi）
- `Data/Levels/M10.srfa`（srfa）
- `Data/Levels/M10.srf`（srf）
- `Data/Levels/M10.edt`（edt）
- `Data/Levels/M10.sgv`（sgv）

:::
