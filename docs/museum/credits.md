---
title: 制作名单
---

# 制作名单

《蓝色警戒》系列的制作团队名单，数据来自游戏程序内的名单数据（`data/credits.json`），共 5 组 26 人。名单数据为两作程序的比对结果：斯洛伐克原开发团队名单在两作中完全一致，而**汉化人员名单只出现在第一部中**（第二部没有汉化名单）。

<CreditsList />

## 关于「汉化人员」分组

游戏内的名单原本只有 Programming / Artwork and Animations / Music and Sfx / Special thanks to 四个分组标题；第 11 位之后的中文名单**没有分组标题**，在程序里以分隔标记与原团队名单区隔。「汉化人员」四个字是站点自定的展示标题，**原文无标题**。

## 显示顺序

各分组与组内人名的显示顺序按游戏程序内名单构建函数的压栈顺序整理（第一部 FUN(0x42df50–0x42e337)），与游戏内制作名单的实际显示一致。

## 数据来源

- 第一部：`State of War.exe` .data 0x4a1958–0x4a1ae8（提取记录见仓库 `research/mining-g1-weapons-credits.txt`）。
- 第二部：`State of War - Warmonger.exe` .data 0x49ea6c–0x49eb8c（`research/mining-g2-credits.txt`；斯洛伐克团队名单与第一部相同，无汉化名单）。
