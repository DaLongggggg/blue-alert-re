#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 Word 二进制 .doc 中提取 UTF-16LE 正文（只读取证工具）。

用法: python -I mine_extract_doc_text.py INPUT.doc OUTPUT.md --out-root DIR
原理: 在文件字节流中扫描 UTF-16LE 可读文本游程（CJK/ASCII/常见标点），
拼接成长段落；丢弃短噪声。输出前打印 sha256 与游程统计。
安全: resolve(strict=True) 校验输入；输出必须位于 --out-root 指定目录内。
"""
import argparse
import hashlib
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

MIN_RUN = 12  # 最少字符数


def looks_ok(ch):
    o = ord(ch)
    if ch in "\r\n\t":
        return True
    if 0x20 <= o < 0x7F:
        return True
    if o in (0x00A0, 0x00A9, 0x00AE, 0x00B0, 0x00B7, 0x00D7):
        return True
    if 0x2010 <= o <= 0x2027:
        return True
    if 0x4E00 <= o <= 0x9FFF:
        return True
    if 0x3000 <= o <= 0x303F:
        return True
    if 0xFF00 <= o <= 0xFFEF:
        return True
    if o in (0x2026, 0x2018, 0x2019, 0x201C, 0x201D):
        return True
    return False


def extract(data):
    runs = []
    i = 0
    n = len(data)
    while i + 1 < n:
        ch = data[i] | (data[i + 1] << 8)
        if looks_ok(chr(ch)):
            start = i
            chars = []
            while i + 1 < n:
                ch = data[i] | (data[i + 1] << 8)
                c = chr(ch)
                if not looks_ok(c):
                    break
                chars.append(c)
                i = i + 2
            text = "".join(chars)
            if len(text) >= MIN_RUN:
                runs.append((start, text))
        else:
            i = i + 1
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--out-root", required=True)
    args = ap.parse_args()
    src = pathlib.Path(args.input)
    if not src.is_file():
        raise SystemExit("输入不存在")
    src = src.resolve(strict=True)
    root = pathlib.Path(args.out_root).resolve()
    dst = pathlib.Path(args.output).resolve()
    if not dst.is_relative_to(root):
        raise SystemExit("输出路径越界")
    data = src.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    runs = extract(data)
    print("source:", src)
    print("sha256:", sha)
    print("runs>=", MIN_RUN, ":", len(runs))
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for off, text in runs:
            f.write("<!-- off=0x%x -->\n%s\n\n" % (off, text))
    print("written:", dst)


if __name__ == "__main__":
    main()
