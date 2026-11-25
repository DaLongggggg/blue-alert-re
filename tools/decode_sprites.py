#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""State of War (蓝色警戒 1/2) sprite decoder.

Decodes the sprite resources of State of War / State of War: Warmonger:

  * resource package  Data/sprites.info + Data/sprites.data  (CMegaFile, 381 entries)
  * loose containers  Data/Sprites2/**/*.tsp

Container layout (see research/FORMAT-sprites.md):
  [u32 block_size][block bytes][u32 block_size][block bytes]...[u32 0]

Block ("sprite frame") layout:
  u16 width, u16 height, s16 xoff, s16 yoff, 4x u16 (design fields, unused here),
  then height * u32 row offsets, each a WORD offset relative to the block start
  (byte position = 2 * value).
Row layout:
  u16 entry_count, u16 first_entry_type, then entry_count alternating entries:
  even entry = u16 transparent skip, odd entry = u16 pixel count followed by
  `count` u16 RGB565 pixels (.ps6/.tsp).  In pixelless containers (.msk/.sha)
  the opaque runs carry no pixel data (uniform fill).

Usage (always run with python -I):
  python -I decode_sprites.py --g1 "<g1 dir>" --g2 "<g2 dir>" --catalog "<out dir>" --list
  python -I decode_sprites.py --g1 ... --g2 ... --catalog ... --decode all
  python -I decode_sprites.py --g1 ... --g2 ... --catalog ... --decode units 1a
  python -I decode_sprites.py --g1 ... --g2 ... --catalog ... --media "<dir>" \
      --select <spec.json>
"""
import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")

# ---------------------------------------------------------------------------
# small safety helpers
# ---------------------------------------------------------------------------

def resolve_existing(p):
    q = Path(p).resolve(strict=True)
    if not q.is_file():
        raise SystemExit("not a file: %s" % q)
    return q


def safe_stem(name):
    """sanitise a sprite name into a safe file stem, keep uniqueness"""
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    s = s.strip("._-") or "unnamed"
    if not SAFE_NAME.match(s):
        s = "unnamed"
    return s


def ensure_in(child, root):
    c = Path(child).resolve()
    r = Path(root).resolve()
    if not c.is_relative_to(r):
        raise SystemExit("refusing to write outside output root: %s" % c)
    c.parent.mkdir(parents=True, exist_ok=True)
    return c


# ---------------------------------------------------------------------------
# format layer
# ---------------------------------------------------------------------------

def read_info(info_path):
    """parse sprites.info -> [(name, offset, size)]"""
    b = info_path.read_bytes()
    magic, count = struct.unpack_from("<II", b, 0)
    if magic != 0x01010101:
        raise SystemExit("%s: bad magic 0x%08x" % (info_path, magic))
    off = 8
    entries = []
    for _ in range(count):
        chars = bytearray()
        while off < len(b):
            c = b[off]
            off += 1
            if c == 0:
                break
            if c < 10:
                raise SystemExit("%s: bad name byte at %d" % (info_path, off))
            chars.append(c - 10)
        o, s = struct.unpack_from("<II", b, off)
        off += 8
        entries.append((chars.decode("ascii", "replace"), o, s))
    return entries


def walk_blocks(buf):
    """container -> [(data_offset, data_size)]"""
    out = []
    off = 0
    n = len(buf)
    while off + 4 <= n:
        (sz,) = struct.unpack_from("<I", buf, off)
        if sz == 0:
            break
        if off + 4 + sz > n:
            break  # truncated tail
        out.append((off + 4, sz))
        off += 4 + sz
    return out


class BlockHeader:
    __slots__ = ("w", "h", "xoff", "yoff", "design", "rows")

    def __init__(self, buf, boff):
        self.w, self.h = struct.unpack_from("<HH", buf, boff)
        self.xoff, self.yoff = struct.unpack_from("<hh", buf, boff + 4)
        self.design = struct.unpack_from("<4H", buf, boff + 8)
        self.rows = []
        if 0 < self.h <= 4096:
            for i in range(self.h):
                if boff + 16 + 4 * i + 4 > len(buf):
                    break
                (v,) = struct.unpack_from("<I", buf, boff + 16 + 4 * i)
                self.rows.append(v)

    @property
    def empty(self):
        return self.w == 0 or self.h == 0


def decode_rows(buf, boff, blen, pixelless):
    """decode one block -> (header, ok_row_count, bad_row_count, rows data)

    rows data: list of (skip, [(x, [pixels])]) per row (pixel runs), or for
    pixelless containers [(x, count)] solid runs.  None fields on failure.
    """
    bh = BlockHeader(buf, boff)
    bad = 0
    rows = []
    bend = boff + blen
    if bh.empty:
        return bh, 0, 0, []          # valid placeholder frame, nothing to draw
    if not (0 < bh.w <= 4096) or not (0 < bh.h <= 4096):
        return bh, 0, 1, None
    if boff + 16 + 4 * bh.h > bend:
        return bh, 0, bh.h, None
    for i in range(bh.h):
        rpos = boff + bh.rows[i] * 2
        if i + 1 < bh.h:
            rend = boff + bh.rows[i + 1] * 2
        else:
            rend = bend
        if rpos < boff or rpos + 4 > rend:
            bad += 1
            rows.append(None)
            continue
        n, t = struct.unpack_from("<HH", buf, rpos)
        if n > 16384:
            bad += 1
            rows.append(None)
            continue
        p = rpos + 4
        x = 0
        runs = []
        okrow = True
        for _ in range(n):
            if p + 2 > rend:
                okrow = False
                break
            (v,) = struct.unpack_from("<H", buf, p)
            p += 2
            if t == 0:
                x += v
                t = 1
            else:
                if pixelless:
                    runs.append((x, v))
                    x += v
                else:
                    if p + 2 * v > rend:
                        okrow = False
                        break
                    px = struct.unpack_from("<%dH" % v, buf, p)
                    p += 2 * v
                    runs.append((x, px))
                    x += v
                t = 0
        if not okrow:
            bad += 1
            rows.append(None)
        else:
            rows.append(runs)
    return bh, bh.h - bad, bad, rows


def render_block(buf, boff, blen, pixelless):
    """-> (PIL RGBA Image or None, stats dict)"""
    bh, ok, bad, rows = decode_rows(buf, boff, blen, pixelless)
    stats = dict(w=bh.w, h=bh.h, xoff=bh.xoff, yoff=bh.yoff, ok_rows=ok, bad_rows=bad)
    if rows is None or bad > 0 and ok == 0:
        return None, stats
    buf_px = bytearray(bh.w * bh.h * 4)  # RGBA, zero-filled = transparent
    for y, runs in enumerate(rows):
        if runs is None:
            continue
        rowbase = y * bh.w * 4
        for x0, data in runs:
            if pixelless:
                for dx in range(data):
                    xx = x0 + dx
                    if 0 <= xx < bh.w:
                        o = rowbase + xx * 4
                        buf_px[o:o + 4] = b"\x00\x00\x00\xff"
            else:
                for dx, pv in enumerate(data):
                    xx = x0 + dx
                    if 0 <= xx < bh.w:
                        o = rowbase + xx * 4
                        buf_px[o] = ((pv >> 11) & 0x1F) * 255 // 31
                        buf_px[o + 1] = ((pv >> 5) & 0x3F) * 255 // 63
                        buf_px[o + 2] = (pv & 0x1F) * 255 // 31
                        buf_px[o + 3] = 0xFF
    img = None
    if bh.w and bh.h:
        img = Image.frombytes("RGBA", (bh.w, bh.h), bytes(buf_px))
    return img, stats


def render_entry(buf, pixelless):
    """decode all blocks of one container -> [(idx, img, stats)]"""
    out = []
    for i, (boff, blen) in enumerate(walk_blocks(buf)):
        img, st = render_block(buf, boff, blen, pixelless)
        out.append((i, img, st))
    return out


# ---------------------------------------------------------------------------
# sources: package entries + tsp files
# ---------------------------------------------------------------------------

PIXELESS_EXT = {".msk", ".sha"}


class Source:
    def __init__(self, game, name, data):
        self.game = game           # 'g1' / 'g2'
        self.name = name           # entry name or tsp relative path
        self.data = data           # bytes
        ext = Path(name).suffix.lower()
        self.kind = ("anchor" if ext in (".po1", ".po2")
                     else "sprite")
        self.pixelless = ext in PIXELESS_EXT
        self.stem = safe_stem(name)
        self.file_id = "%s-%s" % (self.stem, game)

    def decode_all(self):
        return render_entry(self.data, self.pixelless)

    def anchors(self):
        """.po1/.po2: table of (s16 dx, s16 dy) pairs, one pair per frame"""
        n = len(self.data) // 4
        return [struct.unpack_from("<hh", self.data, i * 4) for i in range(n)]


def load_sources(game_dir, game_tag):
    """package entries + tsp files of one game"""
    data_dir = Path(game_dir) / "Data"
    info_p = resolve_existing(data_dir / "sprites.info")
    data_p = resolve_existing(data_dir / "sprites.data")
    sources = []
    data = data_p.read_bytes()
    for name, off, size in read_info(info_p):
        if off + size > len(data):
            continue
        sources.append(Source(game_tag, name, data[off:off + size]))
    for p in sorted((data_dir / "Sprites2").rglob("*.tsp")):
        rel = p.relative_to(data_dir / "Sprites2").as_posix()
        sources.append(Source(game_tag, rel, p.read_bytes()))
    return sources


# ---------------------------------------------------------------------------
# contact sheets
# ---------------------------------------------------------------------------

CELL_MAX = 96
BORDER = 2


def contact_sheet(frames, path):
    imgs = [f for _, f, _ in frames if f is not None]
    if not imgs:
        return False
    scaled = []
    for im in imgs:
        s = min(1.0, CELL_MAX / max(im.width, im.height))
        if s < 1.0:
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        scaled.append(im)
    cols = min(len(scaled), 10)
    rows = (len(scaled) + cols - 1) // cols
    cw = max(im.width for im in scaled) + BORDER * 2
    ch = max(im.height for im in scaled) + BORDER * 2
    sheet = Image.new("RGB", (cols * cw, rows * ch), (40, 40, 48))
    for k, im in enumerate(scaled):
        cx = (k % cols) * cw
        cy = (k // cols) * ch
        sheet.paste(im, (cx + BORDER + (cw - BORDER * 2 - im.width) // 2,
                         cy + BORDER + (ch - BORDER * 2 - im.height) // 2), im)
    sheet.save(path)
    return True


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="State of War sprite decoder")
    ap.add_argument("--g1", required=True, help="game 1 install dir (read-only)")
    ap.add_argument("--g2", required=True, help="game 2 install dir (read-only)")
    ap.add_argument("--catalog", required=True, help="output dir for contact sheets")
    ap.add_argument("--list", action="store_true", help="list entries and blocks")
    ap.add_argument("--decode", nargs="+", metavar="PAT",
                    help="decode sources whose name contains any pattern, or 'all'")
    ap.add_argument("--stats-only", action="store_true",
                    help="decode but only report statistics")
    ap.add_argument("--media", help="root dir for --select output")
    ap.add_argument("--select", help="JSON spec: [{out, source, block, game?, unit?, what?}]"
                                     "; writes <media>/<out> and <media>/../research/selected-sprites.json"
                                     " is NOT written (caller does that)")
    ap.add_argument("--select-report", help="where to write the selection report json")
    args = ap.parse_args()

    g1 = Path(args.g1).resolve(strict=True)
    g2 = Path(args.g2).resolve(strict=True)
    catalog = Path(args.catalog).resolve()
    catalog.mkdir(parents=True, exist_ok=True)

    sources = []
    failures = []
    for gd, tag in ((g1, "g1"), (g2, "g2")):
        try:
            sources.extend(load_sources(gd, tag))
        except Exception as e:  # noqa: BLE001 - report and continue
            failures.append((tag, "<load>", str(e)))

    if args.list:
        for s in sources:
            blocks = walk_blocks(s.data)
            dims = []
            for boff, blen in blocks[:4]:
                bh = BlockHeader(s.data, boff)
                dims.append("%dx%d" % (bh.w, bh.h))
            print("%-3s %-46s size=%-8d blocks=%-4d %s" %
                  (s.game, s.name, len(s.data), len(blocks), " ".join(dims)))
        print("total sources: %d" % len(sources))
        return

    if args.select:
        run_select(args, sources)
        if not args.decode:
            return

    if not args.decode:
        ap.error("--list or --decode is required")

    pats = args.decode
    sel = [s for s in sources if s.kind == "sprite"]
    if "all" not in pats:
        sel = [s for s in sel if any(p.lower() in s.name.lower() for p in pats)]

    n_ok = n_partial = n_fail = 0
    n_frames = 0
    n_empty = 0
    manifest = []
    for s in sel:
        try:
            frames = s.decode_all()
        except Exception as e:  # noqa: BLE001
            failures.append((s.game, s.name, "decode: %s" % e))
            n_fail += 1
            continue
        good = sum(1 for _, img, _ in frames if img is not None)
        empty = sum(1 for _, _, st in frames if st.get("w") == 0 or st.get("h") == 0)
        bad = len(frames) - good - empty
        n_frames += len(frames)
        n_empty += empty
        if good == 0 and bad == 0:
            n_fail += 1
            failures.append((s.game, s.name, "only empty placeholder frames"))
        elif bad:
            n_partial += 1
        else:
            n_ok += 1
        manifest.append(dict(source=s.name, game=s.game, blocks=len(frames),
                             ok_blocks=good, empty_blocks=empty, pixelless=s.pixelless,
                             frames=[st for _, _, st in frames]))
        if args.stats_only:
            continue
        out = ensure_in(catalog / (s.file_id + ".png"), catalog)
        if not contact_sheet(frames, out) and good > 0:
            failures.append((s.game, s.name, "sheet write failed"))

    (catalog / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    print("sources decoded: ok=%d partial=%d failed=%d  frames=%d (empty=%d)  skipped=%d"
          % (n_ok, n_partial, n_fail, n_frames, n_empty, len(sources) - len(sel)))
    if failures:
        print("failures:")
        for g, n, why in failures[:40]:
            print("  %s %-40s %s" % (g, n, why))
        if len(failures) > 40:
            print("  ... %d more" % (len(failures) - 40))


def run_select(args, sources):
    """write curated frames into the media tree from a JSON spec"""
    media = Path(args.media).resolve()
    media.mkdir(parents=True, exist_ok=True)
    spec = json.loads(Path(args.select).resolve(strict=True).read_text(encoding="utf-8"))
    report = []
    n_written = 0
    for item in spec:
        name = item["source"]
        game = item.get("game")
        norm = name.replace("\\", "/").removeprefix("Sprites2/")
        cand = [s for s in sources
                if (s.name == name or s.name.replace("\\", "/") == norm)
                and (game is None or s.game == game)]
        if not cand:
            print("select: source not found: %s (%s)" % (name, game))
            continue
        src = cand[0]
        frames = src.decode_all()
        idx = item.get("block", 0)
        if idx >= len(frames) or frames[idx][1] is None:
            print("select: bad block %d in %s" % (idx, name))
            continue
        img = frames[idx][1]
        out = ensure_in(media / item["out"], media)
        if not SAFE_NAME.match(out.name):
            raise SystemExit("bad output name: %s" % out.name)
        img.save(out)
        n_written += 1
        report.append({
            "file": item["out"],
            "game": src.game,
            "source": src.name,
            "block": idx,
            "size": [img.width, img.height],
            "unit": item.get("unit", ""),
            "what": item.get("what", ""),
            "confidence": item.get("confidence", ""),
        })
    if args.select_report:
        rp = Path(args.select_report).resolve()
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("select: wrote %d/%d images to %s" % (n_written, len(spec), media))


if __name__ == "__main__":
    main()
