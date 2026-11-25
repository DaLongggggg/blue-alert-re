# 媒体提取验收报告（media）

任务：把两作（g1=《蓝色警戒I》2001 / g2=《蓝色警戒II：战争狂人》2003）的
图片、小地图、影片提取成网页可用媒体。可复现脚本：
`tools/extract_media.py`（用法见 `tools/extract_README.md`），全部产物清单：
`research/media-manifest.json`（202 项）。游戏目录全程只读，未运行其中任何程序。

## 产出统计（0 失败）

| 类别 | 数量 | 大小 |
| --- | --- | --- |
| missions/ 小地图 minimap-*.png | 35 | 128,362 B |
| missions/ 关卡图（.srf→`<code>-g<n>.jpg`）| 36 | — |
| missions/ 附加图（.srfa→`<code>-srfa-g<n>-<帧>.jpg`）| 34 | — |
| mission-image 合计 | 70 | 28,515,597 B |
| pictures/ 资料图 | 19 | 1,154,386 B |
| movies+missions/ 影片 .mp4 | 39 | 91,372,837 B |
| 影片封面 .jpg | 39 | 1,047,254 B |
| **合计** | **202 项** | **122,218,436 B ≈ 116.6 MiB** |

- 影片 39 = g1 关卡 22（M01–M22，M00/M23 无 .sgv）+ g2 关卡 11（M01–M04、M06、M07、
  M11、M12、M15、M20、M22）+ movies/ 6（mi/mo 各两作 + ma-g12、mb-g12）。
- 跨作去重（SHA-256 相同 → `-g12`）共 20 项：m00 三件套（两作第一关地图同源）、
  13 张界面图（01/02/03/adapting/briefing/credits/cs/load/network/network2/options/
  presents/statistic）、ma/mb 影片及封面。`ci`、`mainmenu`、`nazov` 两作不同
  （中文版替换过），各自出 `-g1`/`-g2`。
- 同作去重 1 例：g1 `M05.tmi` ≡ `M23.tmi`，按规则各自产出
  （`minimap-m05-g1.png`、`minimap-m23-g1.png`），未误用 -g12。

## 格式结论（证据详见 research/FORMAT-media.md）

1. **`.srf/.srfa` 容器** = 48 字节魔数 + JPEG 流。JPEG 缺 SOI，且 Adobe APP14 标记头
   （FF EE 00 0E "Adobe" 共 10 字节）被剥去，故魔数后紧跟 `00 64 c0 00 00 00 01`
   （APP14 载荷）再到 FF DB。魔数由保存函数逐字节写出（g1 `0x458c70`、g2 `0x456470`），
   同一函数参数≠0 时写 JFIF 头存普通 JPEG——容器与裸 JPEG 同源。解码函数
   g1 `FUN_00458900`（0x458900，经 ijl15 的 ijlInit/ijlRead，IAT 0x8B1AE4/0x8B1AEC）。
   批量实验：92 个容器文件全部恰 1 个 FF D9（单图）；MainMenu.srf 是渐进式 JPEG，
   其"偏移表"实为 4 个 SOS 扫描起点。**`.srfa` = `.srf` 的半分辨率副本**
   （2048×2048→1024×1024、3072×2560→1536×1280），游戏按性能标志二选一作地形底图。
2. **`.tmi` 是瓦片索引图而非 RGB565**（主会话假设不成立）：头仅 4 字节
   = u16 LE 宽、高（非 8 字节），随后 宽×高 个 u16 LE 瓦片索引（0=无结构）。
   证据：文件大小恰为 4+w×h×2；加载函数 `FUN_0044dbd0`（0x44dbd0）；消费函数
   `FUN_0044d200`（0x44d200）以索引×4 查 `.til` 瓦片表、32px 步进绘制；
   索引最大值+1 与 .til 块数完全对应（264/513/801）。网站上的 minimap-*.png
   是"一索引一色相"的结构分布可视化（0=黑、4× 最近邻），**非游戏原色**。
3. **`.til`**（顺带查明，供关卡会话参考）= `[u24 LE 块大小][u8 类型=0][数据]` 块序列，
   块数=tmi 最大索引+1；瓦片为单色剪影 RLE（每行 `[段数][起始状态]`+交替跳过/填充段），
   填充色取全局字节 `[0x49FC00]`。
4. **`.sgv`**：关卡简报/片头片尾是 MPEG-1 节目流（g1 320×208、片头 320×240，
   g2 全部 768×432；MP2 44.1kHz 音频）。`mA.sgv`/`mB.sgv` 实为 AVI：
   mA=Indeo5 640×480+PCM（元数据标题 briefingA.avi，两作同文件）、
   mB=MS Video1 128×112 无声（两作同文件）。统一转码
   libx264 crf24 preset slow yuv420p +faststart / aac 96k / 保持原分辨率；
   封面取 15% 处一帧，与关卡图重名时封面加 `-cover`。

## 异常与坑

- **NTFS 大小写假象**：目录里同时看到 `M01.srfa` 与 `m01.srfa` 是同一真实文件
  （sha256sum 相同；`os.listdir` 证明磁盘只有小写条目）。两作 Levels 真实条目：
  g1 srfa = M00–M08、M10–M23 + m09；g2 srfa = M00 + m01…m22。
- **未包装的普通 JPEG**（不带魔数，Photoshop 保存）：g1 `M23.srfa`、
  g2 全部小写 `m01–m22.srfa`（11 个）。g2 小写 `m03.srf`、`m12.srf` 仍是容器。
- `mB` 影片无音频轨，已正确输出为纯视频 mp4。
- 提取脚本与游戏数据完全解耦（路径参数传入、只读源文件、输出白名单校验），
  `--skip-existing` 可增量重跑；清单为全量重写式，幂等。

## 验证方式

- 目验（Read 实开输出图）：mainmenu-g1.jpg（中文主菜单）、m01-g1.jpg（地形航拍）、
  m01-srfa-g1-1.jpg（同图 1024² 版）、ci-g1.jpg（EVSoft 地球村标识）、
  minimap-m13-g1.png（结构分布）、m01-g1-cover.jpg（简报 15% 处湖景帧）——内容均正确。
- 独立核对输出 mp4 流参数（ffmpeg -i）：320×208 h264+aac 96k、768×432、
  128×112 纯视频，时长与源一致（m01-g1 12.92s、mi-g2 50.02s、mb 8.0s）。
- `.tmi` 网格方向与结构簇位置和 `.srf` 地形图目验比对（非转置、行主序正确）。

## 未解决问题

1. `.tmi` 瓦片填充色 `[0x49FC00]` 的按瓦片上色链路未找到（只见到 250 归零的自增计数），
   小地图暂以索引配色呈现，无法复原游戏原色。
2. `.til` 瓦片 RLE 行级字段（起点状态、段边界的完整语义）只解到可解释层面，
   未做像素级复现验证——留给关卡/精灵会话。
3. MainMenu.srf 渐进扫描表前 9 字节（`03 00 15 04 03 06 0a 0d 00`）含义未定。
4. `mB.sgv`（8s 无声 128×112 CRAM 动画）的用途未定。
5. g2 图片目录名为 `PICTURES`（大写）、其余为 `Pictures`，脚本已做大小写无关处理。
