#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 docs/public/media/missions 下的提取产物按命名规则绑定到 data/missions.json 的 media 字段。

用法: python -I tools/link_missions_media.py

绑定规则（只引用磁盘上实际存在的文件；清单 research/media-manifest.json 仅作对照）:
  image   /media/missions/<code小写>-g<g>.jpg        地形底图（.srf 提取）
  video   /media/missions/<code小写>-g<g>.mp4        简报影片（mp4 不入 git，线上显示封面）
  poster  /media/missions/<code小写>-g<g>-cover.jpg  影片封面（仅在绑定到影片时写入）
  minimap /media/missions/minimap-<code小写>-g<g>.png 关卡结构分布示意（.tmi 索引着色）

<g> 取值: games 跨两作的条目用 g12（两作相同的文件只出一份）；否则用条目的 game（g1/g2）。
不含 -srfa- 的半分辨率副本。联机地图没有地形/影片文件，media 保持为空对象。
脚本幂等：重复运行会覆盖这四个键，保留 media 里的其他键（如 gallery）。
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEDIA_DIR = ROOT / "docs" / "public" / "media" / "missions"
MANIFEST = ROOT / "research" / "media-manifest.json"
DATA_FILE = ROOT / "data" / "missions.json"

# 读外部路径前先用 strict 解析并确认存在（防符号链接/路径欺骗）
for p in (MEDIA_DIR, MANIFEST):
    p.resolve(strict=True)
    if not p.is_file() and not p.is_dir():
        sys.exit(f"缺少输入: {p}")


def media_dir() -> pathlib.Path:
    resolved = MEDIA_DIR.resolve(strict=True)
    if not resolved.is_dir():
        sys.exit(f"媒体目录不存在: {resolved}")
    return resolved


def main() -> None:
    med = media_dir()
    missions = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    # 清单仅用于对照统计（kind 分布），实际绑定以磁盘文件为准
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_outputs = {
        item.get("output") for item in manifest if isinstance(item, dict)
    }

    stats = {"image": 0, "video": 0, "poster": 0, "minimap": 0}
    not_in_manifest = []

    def bind(site_name: str) -> str | None:
        """按文件名在媒体目录中查找；返回站点根相对路径，找不到返回 None。"""
        disk = med / site_name
        if not (disk.resolve(strict=False).is_file() if disk.exists() else False):
            return None
        site_path = "/media/missions/" + site_name
        rel = "missions/" + site_name
        if rel not in manifest_outputs:
            not_in_manifest.append(rel)
        return site_path

    for m in missions:
        code = m.get("code")
        if not code or m.get("type") == "network":
            continue  # 联机地图没有地形/影片/结构图文件
        slug = str(code).lower()
        games = m.get("games") or []
        g = "g12" if len(games) > 1 else str(m.get("game") or "g1")

        media = m.get("media")
        if not isinstance(media, dict):
            media = {}

        image = bind(f"{slug}-{g}.jpg")
        video = bind(f"{slug}-{g}.mp4")
        poster = bind(f"{slug}-{g}-cover.jpg") if video else None
        minimap = bind(f"minimap-{slug}-{g}.png")

        if image:
            media["image"] = image
            stats["image"] += 1
        if video:
            media["video"] = video
            stats["video"] += 1
        if poster:
            media["poster"] = poster
            stats["poster"] += 1
        if minimap:
            media["minimap"] = minimap
            stats["minimap"] += 1
        m["media"] = media

    # 写出前校验目标位于仓库根目录内（输出根校验）
    out = DATA_FILE.resolve(strict=False)
    root = ROOT.resolve(strict=True)
    if root not in out.parents:
        sys.exit(f"输出路径越出仓库根目录: {out}")
    text = json.dumps(missions, ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")

    total = len(missions)
    print(f"missions: {total} 条，绑定 image={stats['image']} video={stats['video']} "
          f"poster={stats['poster']} minimap={stats['minimap']}")
    if not_in_manifest:
        print(f"提示: {len(not_in_manifest)} 个引用未出现在 media-manifest.json（以磁盘为准）:")
        for rel in not_in_manifest[:10]:
            print("  - " + rel)


if __name__ == "__main__":
    main()
