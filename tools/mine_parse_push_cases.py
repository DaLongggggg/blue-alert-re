#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 disasm.py 生成的反汇编文本：提取 switch 各 case 压栈的字符串常量序列。

用法: python -I mine_parse_push_cases.py ASMFILE
输出: 每个 case 入口地址 -> 依序的 push 0x…… 常量列表（只读取证辅助）。
"""
import argparse
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asm")
    ap.add_argument("--jmp-table", default=None, help="0xADDR:COUNT dword 跳转表所在 ASM 无用，另行读取")
    args = ap.parse_args()
    p = pathlib.Path(args.asm)
    if not p.is_file():
        raise SystemExit(f"不存在: {p}")
    lines = p.resolve().read_text(encoding="utf-8", errors="replace").splitlines()
    addr_re = re.compile(r"^([0-9a-f]{8})\s")
    push_re = re.compile(r"push\s+(0x[0-9a-f]+)")
    for ln in lines:
        m = addr_re.match(ln)
        if not m:
            continue
        pm = push_re.search(ln)
        if pm:
            print(f"push @{int(m.group(1), 16):#x} -> {int(pm.group(1), 16):#x}")


if __name__ == "__main__":
    main()
