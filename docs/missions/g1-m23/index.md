---
title: "第 23 关"
---

<GameBadges :games='["g1"]' />

# 第 23 关

<MissionMeta id="g1-m23" />

## 战况

::: warning 简报缺失
游戏内本关没有简报资料——简报界面显示「没有资料」。本页依据关卡文件与程序内关卡分发表的存在性整理；该关在战役中的定位尚无文本证据，本站不作推断。程序内的定位记录见下方「注意」与「数据来源」。
:::

## 任务目标

游戏内未提供本关的任务目标（简报显示「没有资料」）。

## 注意

M23 存在于关卡分发表（0x430d34 push data\levels\m23.sgv，跳表0x430e4c 第23项）且关卡文件存在；但简报 switch 仅覆盖任务号1–22，超出时走默认分支显示「没有资料」（0x439059 push 0x4a3bb8）。其在战役中的定位未确定。

## 地形底图

<MediaZoom src="/media/missions/m23-g1.jpg" ratio="4 / 3" alt="第 23 关 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

::: tip 简报影片
游戏文件中未包含本关的简报影片，故无影片可展示。
:::

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m23-g1.png" ratio="1" alt="第 23 关 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；简报 switch 默认分支 0x439059（「没有资料」0x4a3bb8）

原始文件（相对游戏安装目录）：

- `Data/Levels/M23.map`（map）
- `Data/Levels/M23.til`（til）
- `Data/Levels/M23.tmi`（tmi）
- `Data/Levels/M23.srfa`（srfa）
- `Data/Levels/M23.srf`（srf）

:::
