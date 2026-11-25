# extract_media.py 使用说明

把《蓝色警戒》I（State of War, 2001）/ II（Warmonger, 2003）游戏目录里的
图片、小地图、影片提取成网页可用的媒体文件。**只读游戏目录**，不运行其中任何程序。

## 用法

```bash
E:/rea-tools/venv-sow/Scripts/python.exe -I tools/extract_media.py \
    --game1 "E:/blue alert/蓝色警戒I完整版" \
    --game2 "E:/blue alert/蓝色警戒II完整版" \
    --out docs/public/media
```

参数：

| 参数 | 说明 |
| --- | --- |
| `--game1` / `--game2` | 两作的安装目录（至少给一个） |
| `--out` | 媒体输出根目录（相对仓库根），默认会创建 `missions/ pictures/ movies/` 三个子目录 |
| `--only minimaps\|missions\|pictures\|movies` | 只处理一类 |
| `--no-reencode` | JPEG 不重编码，保留容器内原始字节（只补 JPEG SOI 头） |
| `--skip-existing` | 目标 mp4/封面已存在则跳过 ffmpeg 转码（增量重跑用） |
| `--manifest <路径>` | 清单输出路径，默认 `<仓库根>/research/media-manifest.json` |
| `--quiet` | 只打印错误与统计 |

依赖：`pillow`、`numpy`（未直接用到但属环境基线）、`imageio-ffmpeg`（提供 ffmpeg），
安装在隔离环境 `E:/rea-tools/venv-sow`；务必用 `python -I` 运行。

## 产出与命名

| 源文件 | 产物 |
| --- | --- |
| `Data/Levels/*.tmi` | `missions/minimap-<code>-g<n>.png`（瓦片索引可视化，4× 最近邻） |
| `Data/Levels/Mxx.srf` | `missions/<code>-g<n>.jpg`（关卡地形大图，最长边 ≤1280、质量 82） |
| `Data/Levels/Mxx.srfa` | `missions/<code>-srfa-g<n>-<帧号>.jpg`（g2 小写 `m01.srfa` 等普通 JPEG 照此处理） |
| `Data/Pictures/*.srf` | `pictures/<name>-g<n>[-<帧号>].jpg` |
| `Data/Levels/Mxx.sgv`（M+数字） | `missions/<code>-g<n>.mp4` + 同名封面 `.jpg` |
| `Data/Levels/mI/mO/mA/mB.sgv` | `movies/mi|mo|ma|mb-g<n>.mp4` + 同名封面 `.jpg` |

- `<code>`/`<name>` 一律小写。`-g1`/`-g2` 标记来源作品；**两作 SHA-256 相同的源只输出一份，用 `-g12`**。
- 影片封面取影片 15% 处一帧；若封面名与关卡图像重名（如 `missions/m01-g1.jpg`），
  封面自动改用 `<名>-cover.jpg`。
- 影片统一转码：libx264 · crf 24 · preset slow · yuv420p · +faststart，音频 aac 96k，保持原始分辨率。
- 幂等：重复运行覆盖同名产物、重写清单，不会残留旧条目；不会删除任何非本脚本产出的文件。

## media-manifest.json

数组，每项一个媒体文件：

```json
{
  "output":   "missions/m01-g1.jpg",            // 相对媒体根目录，POSIX 风格
  "source":   ["g1:Data/Levels/M01.srf"],       // 源文件（g<n>:游戏内相对路径）
  "games":    ["g1"],                            // 该产物覆盖的作品；两作共用时为 ["g1","g2"]
  "kind":     "minimap | mission-image | picture | movie | movie-cover",
  "bytes":    12345,                             // 产物大小
  "sha256":   "…",                               // 产物 SHA-256
  "width":    1280,
  "height":   1280,
  "duration": null                               // 仅 movie 有（秒）
}
```

## 幕后格式结论（详见 research/FORMAT-media.md）

- `.srf/.srfa` 容器 = 48 字节魔数 + JPEG 流（缺 SOI，Adobe APP14 头被剥去 12 字节）。
  g1 写入函数 `FUN_00458c70`（0x458c70）、解码函数 `FUN_00458900`（0x458900）；
  g2 同构（写入函数 0x456470）。部分文件（g1 `M23.srfa`、g2 小写 `mXX.srfa`）未包装，是普通 JPEG。
- `.tmi` 不是 RGB565 位图：`[u16 LE 宽][u16 LE 高][宽×高 个 u16 LE 瓦片索引]`，
  0=无结构；游戏加载函数 `FUN_0044dbd0`（0x44dbd0），索引查 `.til` 瓦片表绘制
  （`FUN_0044d200` + `FUN_00450800`，瓦片步进 32px）。本脚本输出的是
  “每个索引一种颜色”的结构分布可视化图（0=黑），非游戏原色。
- `.sgv`：关卡简报与片头/片尾为 MPEG-1 节目流（320×208 / 320×240 + MP2 音频）；
  `mA.sgv`/`mB.sgv` 实为 AVI（Indeo 5 640×480 / MS Video 1 128×112），ffmpeg 均可直接转码。
