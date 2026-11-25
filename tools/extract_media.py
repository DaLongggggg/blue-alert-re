#!/usr/bin/env python3
"""extract_media.py —— 把《蓝色警戒》I/II 的图片、小地图、影片提取成网页可用媒体。

用法:
  python -I tools/extract_media.py --game1 "<g1目录>" --game2 "<g2目录>" --out docs/public/media
      [--only minimaps|missions|pictures|movies] [--no-reencode] [--skip-existing]
      [--manifest <路径>] [--quiet]

产出（写入 --out 指定的媒体根目录）:
  missions/minimap-<code>-g<n>.png            .tmi 瓦片索引可视化小地图（4x 最近邻）
  missions/<code>-g<n>.jpg                    Levels/*.srf 关卡地形图
  missions/<code>-srfa-g<n>-<帧>.jpg          Levels/*.srfa 关卡附加图（含小写普通 JPEG）
  pictures/<name>-g<n>[-<帧>].jpg             Pictures/*.srf 资料图
  missions/<code>-g<n>.mp4 + 封面 .jpg        Levels/Mxx.sgv 关卡简报影片
  movies/<mi|mo|ma|mb>-g<n>.mp4 + 封面 .jpg   片头/片尾/简报A/B 影片
两作 SHA-256 相同的源文件只输出一份，命名用 -g12。
所有产物清单写入 --manifest（默认 <repo>/research/media-manifest.json）。

安全约定：游戏文件视为不可信数据，本脚本只读它们；输出路径做白名单校验。
"""
from __future__ import annotations

import argparse
import io
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# .srf/.srfa 容器 48 字节魔数（g1 FUN_00458c70 / g2 0x456470 内嵌字节，逐一比对）
SRF_MAGIC = bytes.fromhex(
    "4103cdb79d1c401c81412164b2303faf"
    "d2a8c81807e0c235820f7d738db8f699"
    "b1d75834d4c49b13315410cc2429e3fd"
)
assert len(SRF_MAGIC) == 48

NAME_RE = re.compile(r"^[a-z0-9._-]+$")  # 输出文件名白名单
MAX_EDGE = 1280
JPEG_QUALITY = 82
IMAGE_KINDS = ("minimaps", "missions", "pictures")
KINDS = IMAGE_KINDS + ("movies",)

STATS = {"minimap": [0, 0], "mission-image": [0, 0], "picture": [0, 0],
         "movie": [0, 0], "movie-cover": [0, 0], "fail": 0}


def log(msg: str) -> None:
    if not QUIET:
        print(msg, flush=True)


def safe_out_path(out_root: Path, *parts: str) -> Path:
    """用白名单逐段校验后拼出 out_root 内的输出路径，防止路径穿越。"""
    for part in parts:
        if not NAME_RE.match(part):
            raise ValueError("非法输出名: %r" % part)
    path = out_root.joinpath(*parts)
    resolved = path.resolve()
    if not resolved.is_relative_to(out_root.resolve()):
        raise ValueError("输出越界: %r" % part)
    return resolved


def read_source(path: Path) -> bytes:
    """只读方式打开源文件（须已存在的普通文件）。"""
    p = path.resolve(strict=True)
    if not p.is_file():
        raise FileNotFoundError(str(p))
    return p.read_bytes()


def sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------- .srf 容器

def first_jpeg_marker(data: bytes, start: int) -> int | None:
    """在 [start,) 中找第一个 JPEG 关键标记（DQT/SOF/DHT/DRI），即 JPEG 流起点。"""
    for i in range(start, len(data) - 1):
        if data[i] == 0xFF and data[i + 1] in (0xC0, 0xC1, 0xC2, 0xC4, 0xDB, 0xDD):
            return i
    return None


def split_jpegs(data: bytes) -> list[bytes]:
    """把 .srf/.srfa 内容拆成若干完整 JPEG 字节流（每个以 FF D9 结尾）。

    容器 = 48 字节魔数 + 写入器杂项 + JPEG 流（缺 SOI，且 Adobe APP14 的
    'FF EE 00 0E Adobe' 12 字节头被剥去）。实测每个文件只有 1 张图，
    这里仍按 FF D9 通用切分并逐段交由调用方用 Pillow 校验。
    普通文件（FF D8 开头，如 g2 小写 mXX.srfa）原样返回。
    """
    if data.startswith(b"\xff\xd8\xff"):
        return [data]
    if not data.startswith(SRF_MAGIC):
        raise ValueError("不是 .srf 容器也不是 JPEG（头 16 字节: %s）" % data[:16].hex())
    start = first_jpeg_marker(data, len(SRF_MAGIC))
    if start is None:
        raise ValueError("容器中未找到 JPEG 标记")
    segs = []
    pos = start
    while True:
        end = data.find(b"\xff\xd9", pos)
        if end < 0:
            break
        segs.append(b"\xff\xd8" + data[pos:end + 2])
        nxt = first_jpeg_marker(data, end + 2)
        if nxt is None:
            break
        pos = nxt
    return segs or [b"\xff\xd8" + data[start:]]


def jpeg_size(stream: bytes) -> tuple[int, int] | None:
    """用 Pillow 校验 JPEG 流并返回尺寸；无效返回 None。"""
    try:
        with Image.open(io.BytesIO(stream)) as im:
            im.load()
            return im.width, im.height
    except Exception:
        return None


def reencode_jpeg(stream: bytes, no_reencode: bool) -> tuple[bytes, int, int]:
    """网页化：最长边 <=1280、质量 82；--no-reencode 则保留原始字节。"""
    if no_reencode:
        with Image.open(io.BytesIO(stream)) as im:
            return stream, im.width, im.height
    with Image.open(io.BytesIO(stream)) as im:
        im.load()
        w, h = im.size
        if max(w, h) > MAX_EDGE:
            im = contain_image(im)
        buf = io.BytesIO()
        im.convert("RGB").save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
        return buf.getvalue(), im.width, im.height


def contain_image(im: Image.Image) -> Image.Image:
    """等比缩到最长边 <= MAX_EDGE（用 resize 保证确定性，等价 ImageOps.contain）。"""
    w, h = im.size
    scale = min(1.0, MAX_EDGE / max(w, h))
    return im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)


# ---------------------------------------------------------------- .tmi 小地图

def tmi_to_png(data: bytes, zoom: int = 4) -> tuple[bytes, int, int]:
    """把 .tmi 瓦片索引图渲染成 PNG。

    .tmi = [u16 LE 宽][u16 LE 高][宽*高 个 u16 LE 瓦片索引]（游戏 0x44dbd0 加载，
    0x44d200 用它索引 .til 瓦片表，步进 0x20=32px）。0 = 无结构。
    可视化：0 -> 黑，索引 i -> HSV 色相 (i*47)%360，4x 最近邻放大。
    """
    if len(data) < 4:
        raise ValueError(".tmi 太小")
    w, h = struct.unpack_from("<HH", data, 0)
    if w <= 0 or h <= 0 or len(data) != 4 + w * h * 2:
        raise ValueError(".tmi 尺寸不符: 头 %s, 大小 %d" % (data[:4].hex(), len(data)))
    import colorsys
    words = struct.unpack_from("<%dH" % (w * h), data, 4)
    rgb = bytearray()
    for v in words:
        if v == 0:
            rgb += b"\x00\x00\x00"
        else:
            r, g, b = colorsys.hsv_to_rgb(((v * 47) % 360) / 360.0, 0.75, 1.0)
            rgb += bytes((round(r * 255), round(g * 255), round(b * 255)))
    img = Image.frombytes("RGB", (w, h), bytes(rgb))
    img = img.resize((w * zoom, h * zoom), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue(), img.width, img.height


# ---------------------------------------------------------------- 影片

def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ff(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def probe_movie(ff: str, src: Path) -> tuple[float, int, int]:
    """从 `ffmpeg -i` 的 stderr 解析 (时长秒, 宽, 高)。"""
    r = run_ff([ff, "-hide_banner", "-i", str(src)])
    text = r.stderr
    dur = None
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if m:
        dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    size = None
    vm = re.search(r"Stream #\d+:\d+.*: Video: .*?, (\d+)x(\d+)", text)
    if vm:
        size = (int(vm.group(1)), int(vm.group(2)))
    if dur is None or size is None:
        raise ValueError("无法从 ffmpeg 获取影片信息: %s" % src.name)
    return dur, size[0], size[1]


def transcode_movie(ff: str, src: Path, dst: Path, skip_existing: bool) -> tuple[float, int, int]:
    """MPEG-1/AVI -> H.264+AAC MP4（crf24 preset slow, yuv420p, +faststart, aac 96k）。"""
    dur, w, h = probe_movie(ff, src)
    if skip_existing and dst.is_file():
        return dur, w, h
    vf = []
    if w % 2 or h % 2:  # yuv420p 需要偶数尺寸
        vf.append("pad=ceil(iw/2)*2:ceil(ih/2)*2")
    args = [ff, "-y", "-hide_banner", "-i", str(src),
            "-map", "0:v:0", "-map", "0:a:0?",
            "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"]
    if vf:
        args += ["-vf", ",".join(vf)]
    args.append(str(dst))
    r = run_ff(args)
    if r.returncode != 0 or not dst.is_file():
        raise RuntimeError("转码失败 %s: %s" % (src.name, r.stderr[-500:]))
    return dur, w, h


def extract_cover(ff: str, src: Path, dst: Path, dur: float, skip_existing: bool) -> tuple[int, int]:
    """取影片 15% 处一帧存 JPEG 封面。"""
    if skip_existing and dst.is_file():
        with Image.open(dst) as im:
            return im.width, im.height
    t = max(0.0, dur * 0.15)
    r = run_ff([ff, "-y", "-hide_banner", "-ss", "%.3f" % t, "-i", str(src),
                "-frames:v", "1", "-q:v", "3", str(dst)])
    if r.returncode != 0 or not dst.is_file():
        raise RuntimeError("封面失败 %s: %s" % (src.name, r.stderr[-300:]))
    with Image.open(dst) as im:
        return im.width, im.height


# ---------------------------------------------------------------- 采集计划

def find_data_dir(game_root: Path) -> Path:
    d = game_root / "Data"
    if d.is_dir():
        return d.resolve()
    for child in game_root.iterdir():
        if child.is_dir() and child.name.lower() == "data":
            return child.resolve()
    raise FileNotFoundError("%s 下没有 Data 目录" % game_root)


def find_pictures_dir(data_dir: Path) -> Path | None:
    for child in sorted(data_dir.iterdir()):
        if child.is_dir() and child.name.lower() == "pictures":
            return child.resolve()
    return None


def collect(out_root: Path, games: dict[str, Path]) -> list[dict]:
    """扫描两作，生成待产出去重后的工作项列表。

    项: {kind, out(相对路径), sources:[(game, 相对路径, 绝对路径)], data(bytes, 仅图片类)}
    去重规则：同类(kind)且 SHA-256 相同的源合并；覆盖两作 -> -g12。
    """
    plans: dict[tuple, dict] = {}
    for game, root in sorted(games.items()):
        data_dir = find_data_dir(root)
        levels = (data_dir / "Levels").resolve(strict=True)

        # ---- 小地图 (.tmi)
        for p in sorted(levels.glob("*.tmi")):
            code = p.stem.lower()
            data = read_source(p)
            out = safe_out_path(out_root, "missions", "minimap-%s-%s.png" % (code, game))
            key = ("minimap", sha256(data), out.name)
            plans[key] = {"kind": "minimap", "out": out, "out_rel": out.relative_to(out_root).as_posix(),
                          "sources": [(game, rel(levels, p))], "file": p}

        # ---- 关卡图像 (.srf / .srfa)
        for p in sorted(levels.glob("*.srf")) + sorted(levels.glob("*.srfa")):
            code = p.stem.lower()
            is_srfa = p.suffix.lower() == ".srfa"
            data = read_source(p)
            try:
                streams = [s for s in split_jpegs(data) if jpeg_size(s) is not None]
            except ValueError as e:
                log("!! 跳过 %s: %s" % (p.name, e))
                STATS["fail"] += 1
                continue
            if not streams:
                log("!! 跳过 %s: 无有效 JPEG 段" % p.name)
                STATS["fail"] += 1
                continue
            for fi, stream in enumerate(streams, 1):
                frame = ("-%d" % fi) if (is_srfa or len(streams) > 1) else ""
                name = "%s-srfa-%s%s.jpg" % (code, game, frame) if is_srfa else "%s-%s%s.jpg" % (code, game, frame)
                out = safe_out_path(out_root, "missions", name)
                key = ("mission-image", sha256(stream), out.name)
                item = plans.setdefault(key, {"kind": "mission-image", "out": out,
                                              "out_rel": out.relative_to(out_root).as_posix(),
                                              "sources": [], "streams": []})
                item["sources"].append((game, rel(levels, p)))
                item["streams"].append((game, stream))

        # ---- 资料图 (Pictures/*.srf)
        pics = find_pictures_dir(data_dir)
        if pics:
            for p in sorted(pics.glob("*.srf")):
                name = p.stem.lower()
                data = read_source(p)
                try:
                    streams = [s for s in split_jpegs(data) if jpeg_size(s) is not None]
                except ValueError as e:
                    log("!! 跳过 %s: %s" % (p.name, e))
                    STATS["fail"] += 1
                    continue
                if not streams:
                    log("!! 跳过 %s: 无有效 JPEG 段" % p.name)
                    STATS["fail"] += 1
                    continue
                for fi, stream in enumerate(streams, 1):
                    frame = ("-%d" % fi) if len(streams) > 1 else ""
                    out = safe_out_path(out_root, "pictures", "%s-%s%s.jpg" % (name, game, frame))
                    key = ("picture", sha256(stream), out.name)
                    item = plans.setdefault(key, {"kind": "picture", "out": out,
                                                  "out_rel": out.relative_to(out_root).as_posix(),
                                                  "sources": [], "streams": []})
                    item["sources"].append((game, rel(pics, p)))
                    item["streams"].append((game, stream))

        # ---- 影片 (.sgv)
        for p in sorted(levels.glob("*.sgv")):
            stem = p.stem
            code = stem.lower()
            if re.fullmatch(r"M\d{2}", stem):  # 关卡简报 -> missions/
                subdir, name = "missions", "%s-%s.mp4" % (code, game)
            else:  # mA/mB/mI/mO -> movies/
                subdir, name = "movies", "%s-%s.mp4" % (code, game)
            out = safe_out_path(out_root, subdir, name)
            key = ("movie", sha256(read_source(p)), out.name)
            item = plans.setdefault(key, {"kind": "movie", "out": out,
                                          "out_rel": out.relative_to(out_root).as_posix(),
                                          "subdir": subdir, "sources": [], "file": p})
            item["sources"].append((game, rel(levels, p)))

    # 合并去重：同一内容出现在不同作品 -> 输出一份并改名 -g12；
    # 同一作品内的重复内容（如 g1 的 M05.tmi == M23.tmi）各自保留产物。
    groups: dict[tuple, list[dict]] = {}
    for key, item in plans.items():
        groups.setdefault((key[0], key[1]), []).append(item)
    out_items: list[dict] = []
    for items in groups.values():
        acc = items[0]
        out_items.append(acc)
        for item in items[1:]:
            acc_games = {g for g, _ in acc["sources"]}
            item_games = {g for g, _ in item["sources"]}
            if item_games <= acc_games:
                out_items.append(item)  # 未覆盖新作品，各自出文件
                continue
            new_name = to_g12(acc["out"].name)
            new_out = safe_out_path(out_root, item.get("subdir", parent_rel(acc["out_rel"])), new_name)
            acc["out"] = new_out
            acc["out_rel"] = new_out.relative_to(out_root).as_posix()
            acc["sources"].extend(item["sources"])
            if "streams" in item:
                acc["streams"].extend(item["streams"])
            elif "file" in item:
                acc["file"] = item["file"]  # 内容相同的影片源，任选其一
    return out_items


def to_g12(name: str) -> str:
    """'m00-g1.jpg' / 'm01-srfa-g2-1.jpg' -> 对应 -g12 版本。"""
    stem, dot, suffix = name.rpartition(".")
    parts = stem.split("-")
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in ("g1", "g2"):
            parts[i] = "g12"
            break
    return "-".join(parts) + dot + suffix


def parent_rel(out_rel: str) -> str:
    return out_rel.rsplit("/", 1)[0]


def rel(base: Path, p: Path) -> str:
    return p.relative_to(base).as_posix()


# ---------------------------------------------------------------- 主流程

def main() -> int:
    global QUIET
    ap = argparse.ArgumentParser(description="提取《蓝色警戒》I/II 媒体（只读游戏文件）")
    ap.add_argument("--game1", help="《蓝色警戒I》安装目录")
    ap.add_argument("--game2", help="《蓝色警戒II》安装目录")
    ap.add_argument("--out", required=True, help="媒体输出根目录，如 docs/public/media")
    ap.add_argument("--only", choices=KINDS, help="只处理一类")
    ap.add_argument("--no-reencode", action="store_true", help="JPEG 保留原始字节（仅补 SOI）")
    ap.add_argument("--skip-existing", action="store_true", help="影片已存在则跳过转码")
    ap.add_argument("--manifest", help="清单输出路径（默认 <repo>/research/media-manifest.json）")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    QUIET = args.quiet

    games: dict[str, Path] = {}
    if args.game1:
        games["g1"] = Path(args.game1).resolve(strict=True)
    if args.game2:
        games["g2"] = Path(args.game2).resolve(strict=True)
    if not games:
        ap.error("至少提供 --game1 或 --game2")

    out_root = Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    for sub in ("missions", "pictures", "movies"):
        safe_out_path(out_root, sub).mkdir(parents=True, exist_ok=True)

    repo_root = out_root.parent.parent.parent  # docs/public/media -> 仓库根
    manifest_path = Path(args.manifest).resolve() if args.manifest else \
        (repo_root / "research" / "media-manifest.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    ff = ffmpeg_exe()
    log("ffmpeg: %s" % ff)

    plans = collect(out_root, games)
    if args.only:
        want = {"minimaps": "minimap", "missions": "mission-image",
                "pictures": "picture", "movies": "movie"}[args.only]
        plans = [p for p in plans if p["kind"] == want]
    log("计划产物 %d 项" % len(plans))

    # 先算出所有 mission-image 的最终路径，供影片封面避让命名冲突
    image_names = {p["out"].name for p in plans if p["kind"] == "mission-image"}
    manifest = []

    for item in plans:
        kind = item["kind"]
        try:
            if kind == "minimap":
                if args.only and args.only != "minimaps":
                    continue
                data = read_source(item["file"])
                blob, w, h = tmi_to_png(data)
                item["out"].write_bytes(blob)
                rec = _rec(item, blob, w, h)
            elif kind == "mission-image":
                if args.only and args.only != "missions":
                    continue
                # 多游戏来源内容一致（SHA 相同），取任一即可
                stream = item["streams"][0][1]
                blob, w, h = reencode_jpeg(stream, args.no_reencode)
                item["out"].write_bytes(blob)
                rec = _rec(item, blob, w, h)
            elif kind == "picture":
                if args.only and args.only != "pictures":
                    continue
                stream = item["streams"][0][1]
                blob, w, h = reencode_jpeg(stream, args.no_reencode)
                item["out"].write_bytes(blob)
                rec = _rec(item, blob, w, h)
            elif kind == "movie":
                if args.only and args.only != "movies":
                    continue
                src = item["file"].resolve(strict=True)
                dur, w, h = transcode_movie(ff, src, item["out"], args.skip_existing)
                rec = _rec(item, None, w, h, duration=round(dur, 2))
                # 封面
                cover_name = item["out"].stem + ".jpg"
                if item.get("subdir") == "missions" and cover_name in image_names:
                    cover_name = item["out"].stem + "-cover.jpg"
                cover = safe_out_path(out_root, item.get("subdir", "movies"), cover_name)
                cw, ch = extract_cover(ff, src, cover, dur, args.skip_existing)
                cover_rel = cover.relative_to(out_root).as_posix()
                manifest.append({"output": cover_rel,
                                 "source": ["%s:%s" % (g, s) for g, s in item["sources"]],
                                 "games": sorted({g for g, _ in item["sources"]}),
                                 "kind": "movie-cover", "bytes": cover.stat().st_size,
                                 "sha256": sha256(cover.read_bytes()), "width": cw, "height": ch,
                                 "duration": None})
                STATS["movie-cover"][0] += 1
                STATS["movie-cover"][1] += cover.stat().st_size
            else:
                continue
            manifest.append(rec)
            STATS[kind][0] += 1
            STATS[kind][1] += rec["bytes"]
            log("  %-9s %-34s %8d B  %sx%s%s" % (
                kind, rec["output"], rec["bytes"], rec["width"], rec["height"],
                ("  %.1fs" % rec["duration"]) if rec.get("duration") else ""))
        except Exception as e:  # 单项失败不中断整体
            STATS["fail"] += 1
            log("!! 失败 %s %s: %s" % (kind, item["out_rel"], e))

    manifest.sort(key=lambda r: r["output"])
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    total = sum(v[1] for v in STATS.values() if isinstance(v, list))
    log("")
    log("== 统计 ==")
    for k in ("minimap", "mission-image", "picture", "movie", "movie-cover"):
        log("  %-12s %4d 个  %10d B" % (k, STATS[k][0], STATS[k][1]))
    log("  %-12s %4d 项" % ("失败", STATS["fail"]))
    log("  媒体合计: %d B；清单: %s (%d 项)" % (total, manifest_path, len(manifest)))
    return 0 if STATS["fail"] == 0 else 1


def _rec(item: dict, blob: bytes | None, w: int, h: int, duration: float | None = None) -> dict:
    path = item["out"]
    size = path.stat().st_size
    digest = sha256(blob) if blob is not None else sha256(path.read_bytes())
    return {"output": item["out_rel"],
            "source": ["%s:%s" % (g, s) for g, s in item["sources"]],
            "games": sorted({g for g, _ in item["sources"]}),
            "kind": item["kind"], "bytes": size, "sha256": digest,
            "width": w, "height": h, "duration": duration}


if __name__ == "__main__":
    sys.exit(main())
