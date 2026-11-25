#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 research/manual-g{1,2}-raw.md（UTF-16LE 抽取转储）生成 research/manual-g{1,2}.md。

只做排版整理：按原书小节切分、给热键条目断行、去掉控制噪声游程；不改写任何正文。

用法: python -I tools/mine_build_manuals.py
"""
import hashlib
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = pathlib.Path(__file__).resolve().parent.parent
RES = REPO / "research"

SECTIONS = [
    "硬件要求:", "软件要求:", "安装游戏:", "技术支持:", "故事背景:", "鼠标设置:",
    "游戏热键设置:", "主菜单：", "主屏幕:", "提示和决窍:", "怎样使游戏运行得更快",
    "怎样运行多人游戏:", "多人游戏任务:",
]
# 热键条目的键名（按原文），用于在长段落中插入换行
HOTKEY_KEYS = [
    "方向键――――――", "H,数字键 + ―――――", "数字键回车―――――", "空格键, 数字键0――",
    "Back Space 键――――", "Tab――――――――", "数字键*―――――――", "数字键/ ―――――――",
    "数字键-―――――――", "Esc――――――――", "数字键1-9 ―――――", "Shift + 数字键1-9 ――",
    "R ―――――――――", "X ―――――――――", "Ctrl, Alt ――――――", "1 – 5――――――――",
    "Shift――――――――", "F5―――――――――", "Shift + F5 ――――――", "P――――――――――",
    "F1――――――――――", "F2――――――――――", "F12 ―――――――――", "回车―――――――――",
]
TITLES = {
    "硬件要求:": "硬件要求", "软件要求:": "软件要求", "安装游戏:": "安装游戏",
    "技术支持:": "技术支持", "故事背景:": "故事背景", "鼠标设置:": "鼠标设置",
    "游戏热键设置:": "游戏热键设置", "主菜单：": "主菜单", "主屏幕:": "主屏幕（界面说明）",
    "提示和决窍:": "提示和诀窍（原文作「决窍」）", "怎样使游戏运行得更快": "怎样使游戏运行得更快",
    "怎样运行多人游戏:": "怎样运行多人游戏", "多人游戏任务:": "多人游戏任务",
}


def load_runs(game):
    raw = RES / ("manual-%s-raw.md" % game)
    text = raw.read_text(encoding="utf-8")
    blocks = re.findall(r"<!-- off=(0x[0-9a-f]+) -->\n(.*?)(?=\n\n<!--|\Z)", text, re.S)
    runs = []
    for off, t in blocks:
        t = t.strip()
        cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
        if len(t) >= 60 and cjk >= 20:
            runs.append((int(off, 16), t))
    return runs


def clean(t):
    t = t.replace(" HYPERLINK mailto:support@cypron.sk ", " support@cypron.sk ")
    t = re.sub(r"[\x00-\x08\x0b-\x1f]", "", t)
    return t


def split_sections(runs):
    parts = []
    for off, t in runs:
        idxs = []
        for sec in SECTIONS:
            p = t.find(sec)
            if p >= 0:
                idxs.append((p, sec))
        if not idxs:
            parts.append((None, off, t))
            continue
        idxs.sort()
        first = idxs[0][0]
        if first > 0:
            parts.append((None, off, t[:first]))
        for j, (p, sec) in enumerate(idxs):
            end = idxs[j + 1][0] if j + 1 < len(idxs) else len(t)
            parts.append((sec, off, t[p:end]))
    return parts


def render(game, src_name, sha):
    runs = load_runs(game)
    parts = split_sections(runs)
    name = "蓝色警戒I" if game == "g1" else "蓝色警戒II：战争狂人"
    out = [
        "# 《%s》说明书全文" % name,
        "",
        "- 来源文件：`%s`（SHA-256 `%s`）" % (src_name, sha),
        "- 抽取方式：Word 二进制中的 UTF-16LE 正文游程（tools/mine_extract_doc_text.py，"
        "转储 research/manual-%s-raw.md），仅做小节切分与断行，正文未改动。" % game,
        "- 原文以连续段落存放，无换行；下文小节标题为整理者按原文小节名添加。",
        "- 原书为中文汉化说明书，错别字/怪异表述（如「中选」「决窍」「能难取胜」「集结指分」）均为原文照录。",
        "",
    ]
    for sec, off, t in parts:
        t = clean(t).strip()
        if not t:
            continue
        title = TITLES.get(sec)
        if title:
            out += ["## " + title, ""]
        else:
            out += ["<!-- off=0x%x -->" % off, ""]
        if sec == "游戏热键设置:":
            body = t[len(sec):]
            for k in HOTKEY_KEYS:
                body = body.replace(k, "\n" + k)
            out += [sec, body.strip(), ""]
        else:
            out += [t, ""]
    return "\n".join(out)


def main():
    for game, exe in [("g1", r"E:\blue alert\蓝色警戒I完整版\ReadMe.doc"),
                      ("g2", r"E:\blue alert\蓝色警戒II完整版\ReadME.doc")]:
        p = pathlib.Path(exe)
        if not p.is_file():
            raise SystemExit("缺少说明书文件")
        p = p.resolve(strict=True)
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        doc = render(game, str(p), sha)
        dst = (RES / ("manual-%s.md" % game)).resolve()
        if not dst.is_relative_to(RES.resolve()):
            raise SystemExit("输出越界")
        dst.write_text(doc, encoding="utf-8")
        print("written %s (%d chars)" % (dst, len(doc)))


if __name__ == "__main__":
    main()
