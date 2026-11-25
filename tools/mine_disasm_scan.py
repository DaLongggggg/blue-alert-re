#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""容错反汇编扫描：列出 VA 区间内的 cmp/push 立即数指令对（用于重建 cmp 链 switch）。

用法: python -I mine_disasm_scan.py EXE STARTVA ENDVA [--pairs]
--pairs: 按 (cmp eax, imm -> push imm) 配对输出；条件跳转不重置 cmp（cmp; jne; push 链）。
capstone skipdata 容错，坏字节按 .byte 跳过；只读，不写任何文件。
"""
import argparse
import pathlib
import sys

sys.path.insert(0, r"E:\blue alert\_rea\scripts")
sys.path.insert(0, r"E:\rea-tools\py")
from pe_triage import PE, read_regular_file  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_32  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("exe")
    ap.add_argument("startva")
    ap.add_argument("endva")
    ap.add_argument("--pairs", action="store_true")
    args = ap.parse_args()
    exe = pathlib.Path(args.exe)
    if not exe.is_file():
        raise SystemExit("目标不存在")
    _, data = read_regular_file(str(exe.resolve(strict=True)))
    pe = PE(data)
    va0 = int(args.startva, 16)
    va1 = int(args.endva, 16)
    off = pe.rva_to_off(va0 - pe.image_base)
    end = pe.rva_to_off(va1 - pe.image_base)
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    md.skipdata = True
    cur_cmp = None
    for ins in md.disasm(data[off:end], va0):
        if args.pairs:
            if ins.mnemonic == "cmp" and ins.op_str.startswith("eax, 0x"):
                cur_cmp = int(ins.op_str.split(", ")[1], 16)
            elif ins.mnemonic == "push" and ins.op_str.startswith("0x"):
                v = int(ins.op_str, 16)
                if pe.image_base + 0x90000 <= v <= pe.image_base + 0xb0000:
                    tag = f"cmp {cur_cmp} (0x{cur_cmp:x})" if cur_cmp is not None else "cmp ???"
                    print(f"{tag} -> push {v:#x}  @{ins.address:#x}")
            elif ins.mnemonic.startswith("j"):
                pass  # 条件跳转不重置（cmp; jne; push 链）
            else:
                cur_cmp = None
        else:
            print(f"{ins.address:08x}  {ins.mnemonic:<7} {ins.op_str}")


if __name__ == "__main__":
    main()
