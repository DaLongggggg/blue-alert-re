---
title: "第 12 关 · 战场：巴西"
---

<GameBadges :games='["g1"]' />

# 第 12 关 · 战场：巴西

<MissionMeta id="g1-m12" />

## 战况

敌人袭击了我们波多鄂莱哥利的基地。因此，我们的很大一部分基地都控制在敌人的手中了。你的任务是消灭敌人的所有力量。但是，你只有少数几个作战单位，你必须坚持到援军到达。援军会给你送来金钱，研究指数和陆地作战单位。你必须在他们到达之后，立即升级你的作战单位，用它们去摧毁敌人的总部。

## 任务目标

- 任务：占领地图东部的建筑，坚守阵地直到援军到达。然后，摧毁敌人的总部。

## 地形底图

<MediaZoom src="/media/missions/m12-g1.jpg" ratio="4 / 3" alt="第 12 关 · 战场：巴西 地形底图" />

> 地形航拍底图，提取自本关地形文件（.srf）。点击图片可在新窗口查看原始分辨率。

## 简报影片

<MediaVideo src="/media/missions/m12-g1.mp4" poster="/media/missions/m12-g1-cover.jpg" ratio="320 / 208" />

## 关卡结构分布示意（按瓦片索引着色，非游戏原色）

<MediaZoom src="/media/missions/minimap-m12-g1.png" ratio="1" alt="第 12 关 · 战场：巴西 关卡结构分布示意" />

> 本图由关卡结构索引文件（.tmi）可视化生成：每个瓦片按其索引着色（黑色为无结构区域），仅用于示意建筑与结构的分布位置，并非游戏内小地图的原始配色。

::: details 数据来源

- g1 State of War.exe 简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8) case 12（0x438bbb 起 22 分支）push 顺序: 领土行0x4a47d4 基地行0x4a47b8 战况0x4a46a0 任务0x4a4658（正文见 research/mining-g1-briefing-region.txt）
- g1 State of War.exe 关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\levels\m01.sgv…m23.sgv)；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）
- g1 Data/Levels/M12.map（文件存在）
- g1 Data/Levels/M12.til（文件存在）
- g1 Data/Levels/M12.tmi（文件存在）
- g1 Data/Levels/M12.srfa（文件存在）
- g1 Data/Levels/M12.srf（文件存在）
- g1 Data/Levels/M12.edt（文件存在）
- g1 Data/Levels/M12.sgv（文件存在）

原始文件（相对游戏安装目录）：

- `Data/Levels/M12.map`（map）
- `Data/Levels/M12.til`（til）
- `Data/Levels/M12.tmi`（tmi）
- `Data/Levels/M12.srfa`（srfa）
- `Data/Levels/M12.srf`（srf）
- `Data/Levels/M12.edt`（edt）
- `Data/Levels/M12.sgv`（sgv）

:::
