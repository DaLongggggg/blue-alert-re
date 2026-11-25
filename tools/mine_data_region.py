#!/usr/bin/env python3
"""从 PE 的 .data 段挖掘字符串与指针表（只读取证工具，绝不写入目标文件）。

用法:
  python -I mine_data_region.py strings EXE STARTVA ENDVA
  python -I mine_data_region.py ptrs   EXE STARTVA ENDVA --into LOW-HIGH [--align 1|4]
  python -I mine_data_region.py bytes  EXE STARTVA ENDVA

VA 以 0x 前缀十六进制（镜像基址 0x400000）。输出 UTF-8 到 stdout。
路径安全：对输入 exe 做 resolve(strict=True) 校验，禁止写入任何文件。
"""
import argparse
import pathlib
import struct
import sys


def load_pe(exe: pathlib.Path):
    """读取 PE 头，返回 (data, sections, image_base)。sections: (va, rawsize_raw, vsize, name)"""
    b = exe.read_bytes()
    if b[:2] != b"MZ":
        raise SystemExit("not MZ")
    pe_off = struct.unpack_from("<I", b, 0x3C)[0]
    if b[pe_off:pe_off + 4] != b"PE\0\0":
        raise SystemExit("not PE")
    nsec = struct.unpack_from("<H", b, pe_off + 6)[0]
    opt_size = struct.unpack_from("<H", b, pe_off + 20)[0]
    opt_off = pe_off + 24
    magic = struct.unpack_from("<H", b, opt_off)[0]
    if magic == 0x10B:
        image_base = struct.unpack_from("<I", b, opt_off + 28)[0]
    elif magic == 0x20B:
        image_base = struct.unpack_from("<Q", b, opt_off + 24)[0]
    else:
        raise SystemExit("bad optional magic")
    sec_off = opt_off + opt_size
    sections = []
    for i in range(nsec):
        o = sec_off + 40 * i
        name = b[o:o + 8].rstrip(b"\0").decode("ascii", "replace")
        vsize = struct.unpack_from("<I", b, o + 8)[0]
        va = struct.unpack_from("<I", b, o + 12)[0]
        rawsize = struct.unpack_from("<I", b, o + 16)[0]
        raw = struct.unpack_from("<I", b, o + 20)[0]
        sections.append((name, image_base + va, raw, rawsize, vsize))
    return b, sections, image_base


def va_to_off(sections, image_base, va):
    """VA -> 文件偏移；只落在节的 raw 范围内才可读。"""
    for name, sva, raw, rawsize, vsize in sections:
        if sva <= va < sva + rawsize:
            return raw + (va - sva), name
    return None, None


def is_gbk_lead(x):
    return 0x81 <= x <= 0xFE


def scan_strings(b, sections, image_base, start_va, end_va):
    """扫描 VA 区间内的 ASCII 与 GBK 字符串（遇到 NUL/控制字节断开）。"""
    out = []
    off0, _ = va_to_off(sections, image_base, start_va)
    off1, _ = va_to_off(sections, image_base, end_va)
    if off0 is None or off1 is None:
        raise SystemExit("VA 超出可读节范围")
    i = off0
    cur_start = None
    cur_bytes = bytearray()
    has_cn = False
    while i < off1:
        x = b[i]
        ok = False
        if 0x20 <= x < 0x7F:
            ok = True
        elif x >= 0x80 and i + 1 < len(b):
            # GBK 双字节（含全角标点），次字节范围放宽以兼容汉化组编码
            if is_gbk_lead(x):
                ok = True
                has_cn = True
        if ok:
            if cur_start is None:
                cur_start = i
                cur_bytes = bytearray()
                has_cn = False
            cur_bytes.append(x)
            if x >= 0x80:
                cur_bytes.append(b[i + 1])
                i += 2
                continue
            i += 1
            continue
        # 断开
        if cur_start is not None and len(cur_bytes) >= 3:
            va = image_base + 0x400000 // 0x400000 * 0  # placeholder
            va = start_va + (cur_start - off0)
            enc = "gbk" if has_cn else "ascii"
            try:
                text = cur_bytes.decode(enc, "replace")
            except Exception:
                text = repr(bytes(cur_bytes))
            out.append((va, enc, text))
        cur_start = None
        cur_bytes = bytearray()
        i += 1
    if cur_start is not None and len(cur_bytes) >= 3:
        va = start_va + (cur_start - off0)
        enc = "gbk" if has_cn else "ascii"
        out.append((va, enc, cur_bytes.decode(enc, "replace")))
    return out


def scan_ptrs(b, sections, image_base, start_va, end_va, into_lo, into_hi, align):
    """扫描区间内的指针值，返回 (va, value, 目标节名)。"""
    res = []
    off0, _ = va_to_off(sections, image_base, start_va)
    off1, _ = va_to_off(sections, image_base, end_va)
    if off0 is None or off1 is None:
        raise SystemExit("VA 超出可读节范围")
    step = align
    i = off0
    while i + 4 <= off1:
        v = struct.unpack_from("<I", b, i)[0]
        if into_lo <= v < into_hi:
            _, sec = va_to_off(sections, image_base, v)
            res.append((start_va + (i - off0), v, sec))
        i += step
    return res


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["strings", "ptrs", "bytes"])
    ap.add_argument("exe")
    ap.add_argument("startva")
    ap.add_argument("endva")
    ap.add_argument("--into", default=None, help="LOW-HIGH 目标 VA 区间")
    ap.add_argument("--align", type=int, default=4)
    args = ap.parse_args()

    exe = pathlib.Path(args.exe)
    if not exe.is_file():
        raise SystemExit(f"目标不存在: {exe}")
    exe = exe.resolve(strict=True)
    data, sections, image_base = load_pe(exe)
    sva = int(args.startva, 16)
    eva = int(args.endva, 16)

    if args.mode == "strings":
        for va, enc, text in scan_strings(data, sections, image_base, sva, eva):
            print(f"G|{va:#x}|{enc}|{text!r}")
    elif args.mode == "bytes":
        off0, sec = va_to_off(sections, image_base, sva)
        off1, _ = va_to_off(sections, image_base, eva)
        chunk = data[off0:off1]
        for row in range(0, len(chunk), 16):
            va = sva + row
            piece = chunk[row:row + 16]
            hexs = " ".join(f"{x:02x}" for x in piece)
            asc = "".join(chr(x) if 0x20 <= x < 0x7F else "." for x in piece)
            print(f"{va:#010x}  {hexs:<47}  {asc}")
    else:
        if not args.into:
            raise SystemExit("ptrs 需要 --into LOW-HIGH")
        lo_s, hi_s = args.into.split("-")
        lo, hi = int(lo_s, 16), int(hi_s, 16)
        for va, v, sec in scan_ptrs(data, sections, image_base, sva, eva, lo, hi, args.align):
            print(f"P|{va:#x}|{v:#x}|{sec}")


if __name__ == "__main__":
    main()
