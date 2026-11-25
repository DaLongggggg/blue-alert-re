#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 research/mining-*.txt 转储构建 data/ 下的四份 JSON。

所有地址映射均来自已核实的反汇编/字节表分析，出处见各 sources 字段与
research/notes-*.md。字符串正文一律从转储文件解析，避免转写错误。

用法: python -I tools/mine_build_data.py
"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

REPO = pathlib.Path(__file__).resolve().parent.parent
RES = REPO / "research"
DATA = REPO / "data"

G1_EXE = "g1 State of War.exe"
G2_EXE = "g2 State of War - Warmonger.exe"
NET_DISPATCH_G1 = "关卡分发 FUN(0x430b5a 调用取任务号→dec→跳表0x430e4c→0x430b7b 起 push data\\levels\\m01.sgv…m23.sgv)"
BRIEF_SWITCH_G1 = "简报 switch FUN_00438b90(参数=FUN_00424c00 返回的全局任务号 DAT_0070bde8)"
NET_DISPATCH_G2 = "关卡分发表0x42f65c（0x42f386 起 23 项）"


def parse_dump(path):
    """G|0xVA|enc|'text' → {va:int -> text}"""
    out = {}
    p = pathlib.Path(path)
    if not p.is_file():
        raise SystemExit("缺少转储: %s" % p)
    for ln in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"G\|0x([0-9a-f]+)\|[a-z]+\|'(.*)'$", ln)
        if m:
            out[int(m.group(1), 16)] = m.group(2).replace("\\'", "'")
    return out


S_G1_BRIEF = parse_dump(RES / "mining-g1-briefing-region.txt")
S_G1_INFOBOX = parse_dump(RES / "mining-g1-infobox.txt")
S_G1_UNIT = parse_dump(RES / "mining-g1-unitnames.txt")
S_G1_TUT = parse_dump(RES / "mining-g1-tutorial.txt")
S_G2_BRIEF = parse_dump(RES / "mining-g2-briefings.txt")
S_G2_UNIT = parse_dump(RES / "mining-g2-unitnames.txt")
S_G2_INFOBOX = parse_dump(RES / "mining-g2-infobox.txt")


def s(table, va):
    if va not in table:
        raise SystemExit("转储中缺少 0x%x（表大小 %d，检查转储范围）" % (va, len(table)))
    return table[va]


RE_LINE_TERR = re.compile(r"领土\s*:\s*(\d+)\s*难度(?:等级)?\s*:\s*(\d+)")
RE_LINE_BASE_G1 = re.compile(r"基地代号:\s*(\S+)\s+战场[:：]\s*(.+)")

# 领土号 -> (领土行VA, 基地行VA, 战况VA, 任务VA)
# 来源: 简报 switch FUN_00438b90 各 case 的 push 顺序（research/mining-g1-briefing-switch.asm）
G1_BRIEF = {
    1: (0x4A54DC, 0x4A54BC, 0x4A5394, 0x4A5338),
    2: (0x4A5320, 0x4A5300, 0x4A525C, 0x4A5228),
    3: (0x4A5210, 0x4A51F0, 0x4A5180, 0x4A514C),
    4: (0x4A5134, 0x4A5114, 0x4A50A4, 0x4A5074),
    5: (0x4A505C, 0x4A5040, 0x4A4F38, 0x4A4EF0),
    6: (0x4A4ED8, 0x4A4EBC, 0x4A4E0C, 0x4A4DDC),
    7: (0x4A4DC4, 0x4A4DA8, 0x4A4CC4, 0x4A4C7C),
    8: (0x4A4C64, 0x4A4C48, 0x4A4B98, 0x4A4B70),
    9: (0x4A4B58, 0x4A4B3C, 0x4A4A78, 0x4A4A60),
    10: (0x4A4A48, 0x4A4A28, 0x4A494C, 0x4A4914),
    11: (0x4A48FC, 0x4A48E0, 0x4A4820, 0x4A47EC),
    12: (0x4A47D4, 0x4A47B8, 0x4A46A0, 0x4A4658),
    13: (0x4A4640, 0x4A4620, 0x4A4594, 0x4A456C),
    14: (0x4A4558, 0x4A4538, 0x4A4494, 0x4A4458),
    15: (0x4A4440, 0x4A4424, 0x4A43A8, 0x4A4380),
    16: (0x4A4368, 0x4A4344, 0x4A42B0, 0x4A425C),
    17: (0x4A4248, 0x4A422C, 0x4A4130, 0x4A40E4),
    18: (0x4A40CC, 0x4A40B0, 0x4A4024, 0x4A3FF4),
    19: (0x4A3FE0, 0x4A3FC4, 0x4A3F28, 0x4A3F0C),
    20: (0x4A3EF4, 0x4A3ED8, 0x4A3E5C, 0x4A3E10),
    21: (0x4A3DF8, 0x4A3DD4, 0x4A3D1C, 0x4A3CE0),
    22: (0x4A3CC8, 0x4A3CAC, 0x4A3BF4, 0x4A3BC4),
}

# g2 任务号(=文件号) -> (领土行VA, 基地行VA, 战况VA, 任务VA)
# 来源: 简报 switch FUN(0x437065) 字节表0x4375c8 + 跳表0x437598
G2_BRIEF = {
    1: (0x4A18C4, 0x4A18B4, 0x4A17C8, 0x4A1794),
    2: (0x4A1774, 0x4A1764, 0x4A16A8, 0x4A1668),
    3: (0x4A1648, 0x4A1638, 0x4A15C0, 0x4A1598),
    4: (0x4A1578, 0x4A1568, 0x4A14C8, 0x4A1494),
    6: (0x4A1474, 0x4A1464, 0x4A1380, 0x4A1340),
    7: (0x4A1320, 0x4A1310, 0x4A1268, 0x4A1228),
    11: (0x4A1208, 0x4A11F8, 0x4A1180, 0x4A115C),
    12: (0x4A113C, 0x4A112C, 0x4A1070, 0x4A1040),
    15: (0x4A1020, 0x4A1010, 0x4A0F80, 0x4A0F58),
    20: (0x4A0F38, 0x4A0F28, 0x4A0E78, 0x4A0E48),
    22: (0x4A0E28, 0x4A0E18, 0x4A0D20, 0x4A0CF0),
}

G1_DIR = pathlib.Path(r"E:\blue alert\蓝色警戒I完整版")
G2_DIR = pathlib.Path(r"E:\blue alert\蓝色警戒II完整版")
EXT_ORDER = ["map", "til", "tmi", "srfa", "srf", "edt", "sgv"]


def level_files(game_dir, base):
    d = game_dir / "Data" / "Levels"
    files = {}
    for ext in EXT_ORDER:
        f = d / ("%s.%s" % (base, ext))
        if f.is_file():
            files[ext] = "Data/Levels/%s.%s" % (base, ext)
    return files


NET_G1 = [
    ("01-first-spark", "01-First Spark.net", "热身行动"),
    ("02-ice-blizzard", "02-Ice Blizzard.net", "暴风雪"),
    ("03-gold-rush", "03-Gold Rush.net", "淘金热"),
    ("04-great-crush", "04-Great Crush.net", "大扫荡"),
    ("05-nuclear-devastation", "05-Nuclear Devastation.net", "原子弹行动"),
    ("06-meteor-swarm", "06-Meteor Swarm.net", "流星风暴"),
    ("07-cross-of-fire", "07-Cross of Fire.net", "战火篇"),
    ("08-island-of-fate", "08-Island of Fate.net", "岛屿之命"),
]

MANUAL_NET_DESC = {
    "01-first-spark": "这次任务是为初学者设计的。这是一块美味的蛋糕。游戏中，只有两个建筑和轻型的作战单位。这样，可以帮助玩家学会多人游戏的基础。先试一下吧！",
    "02-ice-blizzard": "这是一次中等难度的任务。适合中选熟练程度的玩家。游戏中，有中选作战单位，炮塔和少量的空中作战力量。非常有趣！强力推荐！",
    "03-gold-rush": "这次任务适合有两次作战经验的玩家。游戏中，有几座金矿，你还会发现一些中选作战单位，和几个空中力量。酷极了！",
    "04-great-crush": "这次任务是为富有作战经验的玩家设计的。游戏中增加了许多中型作战单位，炮塔，空中力量，超级机器人和罗根炸弹设施。惊险而又刺激！",
    "05-nuclear-devastation": "游戏的双方都拥有中型作战单位，超级机器人，空中力量和炮塔。另外，每一方还有罗根炸弹。适合战术熟练的玩家。这是一次歼灭大行动！",
    "06-meteor-swarm": "这次任务极其艰巨。游戏中，有重型作战单位！准备好接受大量陆地作战单位的重型袭击。在这里，还会出现星体炸弹。它们的爆炸是一种非常壮观的景象。还等什么？",
    "07-cross-of-fire": "这可能会是你的一场恶梦。每一方都有两个总部和两个飞碟。你准备好重型作战单位，炮塔，空中力量和超级机器人和大量的建筑了吗？速速占领有利的地势。仅适用于专家级别的玩家。",
    "08-island-of-fate": "除非你是拿破仑再世，否则能难取胜。游戏中到处分散着大量的作战单位。右下角的岛屿是最重要的建筑。生死在天，试一下自己的运气吧！",
}

NET_G2 = [
    ("00-the-first-step", "00-the first step.net"),
    ("01-goldmine-valley", "01-goldmine valley.net"),
    ("02-air-attacks", "02-air attacks.net"),
    ("03-winter-war", "03-winter war.net"),
    ("04-burn-them-all", "04-burn them all.net"),
    ("05-ground-zero", "05-ground zero.net"),
]

# 教程课文顺序（内存地址倒序 = 播放顺序；锚点 0x4a22cc 首句 / 0x4a1c80 末句）
TUTORIAL_ORDER = [
    0x4A22CC, 0x4A22AC, 0x4A2288, 0x4A2278, 0x4A2244, 0x4A21F8, 0x4A21C0,
    0x4A2164, 0x4A20EC, 0x4A2098, 0x4A2088, 0x4A2020, 0x4A1F90, 0x4A1F7C,
    0x4A1F34, 0x4A1F24, 0x4A1EE4, 0x4A1ED0, 0x4A1E60, 0x4A1E0C, 0x4A1D88,
    0x4A1D50, 0x4A1D38, 0x4A1D10, 0x4A1CA4, 0x4A1C80,
]


def tutorial_text():
    lines = []
    for va in TUTORIAL_ORDER:
        lines.append(s(S_G1_TUT, va))
    return "\n".join(lines)


def parse_g1_brief(terr):
    vas = G1_BRIEF[terr]
    line_terr, line_base, brief, obj = (S_G1_BRIEF[v] for v in vas)
    mt = RE_LINE_TERR.search(line_terr)
    mb = RE_LINE_BASE_G1.search(line_base)
    if not mt or not mb:
        raise SystemExit("g1 领土%d 行解析失败: %r / %r" % (terr, line_terr, line_base))
    return {
        "expectedNo": int(mt.group(1)), "difficulty": int(mt.group(2)),
        "baseCode": mb.group(1), "opponent": mb.group(2).strip(),
        "objective": obj, "briefing": brief, "vas": vas,
    }


def parse_g2_brief(file_no):
    vas = G2_BRIEF[file_no]
    line_terr, line_base, brief, obj = (S_G2_BRIEF[v] for v in vas)
    mt = RE_LINE_TERR.search(line_terr)
    mb = re.match(r"基地代号:\s*(\S+)$", line_base.strip())
    if not mt or not mb:
        raise SystemExit("g2 M%02d 行解析失败: %r / %r" % (file_no, line_terr, line_base))
    return {
        "expectedNo": int(mt.group(1)), "difficulty": int(mt.group(2)),
        "baseCode": mb.group(1), "opponent": None,
        "objective": obj, "briefing": brief, "vas": vas,
    }


def build_missions():
    out = []
    # g1 战役 M01–M22（领土1–22）
    for terr in range(1, 23):
        code = "M%02d" % terr
        b = parse_g1_brief(terr)
        files = level_files(G1_DIR, code)
        src = [
            "%s %s case %d（0x438bbb 起 22 分支）push 顺序: 领土行0x%x 基地行0x%x 战况0x%x 任务0x%x（正文见 research/mining-g1-briefing-region.txt）"
            % (G1_EXE, BRIEF_SWITCH_G1, terr, b["vas"][0], b["vas"][1], b["vas"][2], b["vas"][3]),
            "%s %s；同全局 DAT_0070bde8 亦驱动简报 switch（0x438ac3 call FUN_00424c00 后 push 参数）"
            % (G1_EXE, NET_DISPATCH_G1),
        ]
        for k in files:
            src.append("g1 Data/Levels/%s.%s（文件存在）" % (code, k))
        out.append({
            "id": "g1-%s" % code.lower(), "game": "g1", "games": ["g1"],
            "code": code, "order": terr, "type": "campaign",
            "title": None, "baseCode": b["baseCode"], "expectedNo": b["expectedNo"],
            "difficulty": b["difficulty"], "opponent": b["opponent"],
            "objective": b["objective"], "briefing": b["briefing"], "note": None,
            "files": files, "media": {}, "sources": src,
        })
    # g1 M23：在分发表中存在，无简报
    files = level_files(G1_DIR, "M23")
    out.append({
        "id": "g1-m23", "game": "g1", "games": ["g1"],
        "code": "M23", "order": 23, "type": "campaign",
        "title": None, "baseCode": None, "expectedNo": None,
        "difficulty": None, "opponent": None,
        "objective": None, "briefing": None,
        "note": "M23 存在于关卡分发表（0x430d34 push data\\levels\\m23.sgv，跳表0x430e4c 第23项）且关卡文件存在；但简报 switch 仅覆盖任务号1–22，超出时走默认分支显示「没有资料」（0x439059 push 0x4a3bb8）。其在战役中的定位未确定。",
        "files": files, "media": {},
        "sources": ["%s %s；简报 switch 默认分支 0x439059（「没有资料」0x4a3bb8）" % (G1_EXE, NET_DISPATCH_G1)],
    })
    # g1 联机图
    for i, (slug, fname, cn) in enumerate(NET_G1, start=1):
        f = G1_DIR / "Data" / "Levels" / fname
        if not f.is_file():
            raise SystemExit("缺少联机图 %s" % f)
        out.append({
            "id": "g1-%s" % slug, "game": "g1", "games": ["g1"],
            "code": slug, "order": i, "type": "network",
            "title": cn, "baseCode": None, "expectedNo": None,
            "difficulty": None, "opponent": None,
            "objective": None, "briefing": MANUAL_NET_DESC[slug], "note": None,
            "files": {"net": "Data/Levels/%s" % fname}, "media": {},
            "sources": [
                "g1 Data/Levels/%s（文件存在；文件名即英文名）" % fname,
                "g1 ReadMe.doc「多人游戏任务」节（说明书按编号01–08给出中文名与说明，编号与文件名前缀一致）",
            ],
        })
    # g2 战役
    for file_no in sorted(G2_BRIEF):
        code = "M%02d" % file_no
        b = parse_g2_brief(file_no)
        files = level_files(G2_DIR, code)
        if not files:
            raise SystemExit("g2 %s 无关卡文件" % code)
        src = [
            "%s 简报 switch FUN(0x437065) 字节表0x4375c8: 任务号%d→case条目（push 顺序: 领土行0x%x 基地行0x%x 战况0x%x 任务0x%x，正文见 research/mining-g2-briefings.txt）"
            % (G2_EXE, file_no, b["vas"][0], b["vas"][1], b["vas"][2], b["vas"][3]),
            "%s: 任务号%d→data\\levels\\m%02d.sgv；字节表中任务号5/8/9/10/13/14/16–19/21 指向默认「没有资料」，与磁盘缺失的 mNN 文件一一对应"
            % (NET_DISPATCH_G2, file_no, file_no),
        ]
        for k in files:
            src.append("g2 Data/Levels/%s.%s（文件存在）" % (code, k))
        note = None
        if file_no == 12:
            note = "「领土 : 08   难度等级 : 5 z 10」中的 z 系原文如此（分隔符排版错误）。"
        if file_no == 2:
            note = "战况正文以「第二个工厂」结尾，原文即在此截断。"
        out.append({
            "id": "g2-%s" % code.lower(), "game": "g2", "games": ["g2"],
            "code": code, "order": b["expectedNo"], "type": "campaign",
            "title": None, "baseCode": b["baseCode"], "expectedNo": b["expectedNo"],
            "difficulty": b["difficulty"], "opponent": b["opponent"],
            "objective": b["objective"], "briefing": b["briefing"], "note": note,
            "files": files, "media": {}, "sources": src,
        })
    # g2 联机图
    for i, (slug, fname) in enumerate(NET_G2):
        f = G2_DIR / "Data" / "Levels" / fname
        if not f.is_file():
            raise SystemExit("缺少联机图 %s" % f)
        out.append({
            "id": "g2-%s" % slug, "game": "g2", "games": ["g2"],
            "code": slug, "order": i, "type": "network",
            "title": None, "baseCode": None, "expectedNo": None,
            "difficulty": None, "opponent": None,
            "objective": None, "briefing": None,
            "note": "g2 说明书（ReadME.doc）无联机地图说明章节；中文名未确定，nameEn/英文名来自文件名。",
            "files": {"net": "Data/Levels/%s" % fname}, "media": {},
            "sources": ["g2 Data/Levels/%s（文件存在；文件名即英文名）" % fname],
        })
    # 教程关 M00（两作相同）
    files1 = level_files(G1_DIR, "M00")
    files2 = level_files(G2_DIR, "M00")
    if not files1 or not files2:
        raise SystemExit("M00 文件缺失")
    out.append({
        "id": "g12-m00", "game": "g1", "games": ["g1", "g2"],
        "code": "M00", "order": 0, "type": "tutorial",
        "title": None, "baseCode": None, "expectedNo": None,
        "difficulty": None, "opponent": None,
        "objective": None,
        "briefing": tutorial_text(),
        "note": "课文顺序按 .data 内存地址倒序重建（首锚点 0x4a22cc 欢迎语、尾锚点 0x4a1c80 结束语）；'i ' 开头为课程标题/讲解，'! ' 开头为操作步骤。两作 M00 关卡文件完全相同，g2 教程文本（0x49ed38 起）与 g1 相同。",
        "files": files1, "media": {},
        "sources": [
            "%s .data 0x4a1c80–0x4a22cc（正文见 research/mining-g1-tutorial.txt）" % G1_EXE,
            "%s .data 0x49ed38 起（II_strings.txt 同文）" % G2_EXE,
            "g1 Data/Levels/M00.* 与 g2 Data/Levels/M00.*（两作文件相同）",
            '%s 关卡短名表 0x4a0d30–0x4a0d48（m00–m30，加载器 0x420b47 push "m00"，跳表0x420e14 索引0）' % G1_EXE,
        ],
    })
    return out


# ID -> 中文名 VA(g1)；g2 同映射（字节表0x42a178→跳表0x42a090，字符串VA不同）
UNIT_CN_G1 = {
    1: 0x4A1768, 2: 0x4A1758, 3: 0x4A1748, 4: 0x4A173C, 5: 0x4A1730, 6: 0x4A1724,
    7: 0x4A1714, 8: 0x4A1704, 9: 0x4A16F4, 10: 0x4A16E8, 11: 0x4A16DC, 12: 0x4A16D0,
    13: 0x4A16C0, 14: 0x4A16B0, 15: 0x4A16A0,
    16: 0x4A1558, 17: 0x4A154C, 18: 0x4A1540, 19: 0x4A150C, 20: 0x4A14FC, 21: 0x4A14EC,
    22: 0x4A1534, 23: 0x4A1528, 24: 0x4A151C,
    25: 0x4A1644, 26: 0x4A1638, 27: 0x4A162C, 28: 0x4A1620, 29: 0x4A1614,
    30: 0x4A1608, 31: 0x4A15EC, 32: 0x4A15D0, 33: 0x4A15DC, 34: 0x4A15F8,
    40: 0x4A165C, 41: 0x4A1694, 42: 0x4A1684, 43: 0x4A167C, 44: 0x4A1670, 45: 0x4A1664, 46: 0x4A1650,
    100: 0x4A15C8, 101: 0x4A15BC, 102: 0x4A15B0, 103: 0x4A15A4, 104: 0x4A1588,
    105: 0x4A1580, 106: 0x4A1570, 107: 0x4A1564, 108: 0x4A1598,
    109: 0x4A1258, 110: 0x4A1248, 111: 0x4A1238, 112: 0x4A1228, 113: 0x4A1218,
    115: 0x4A1778,
}

UNIT_EN_G1 = {
    1: 0x4A14B4, 2: 0x4A14A4, 3: 0x4A1494, 4: 0x4A1484, 5: 0x4A1470, 6: 0x4A1460,
    7: 0x4A1450, 8: 0x4A1440, 9: 0x4A1430, 10: 0x4A1420, 11: 0x4A1410, 12: 0x4A1400,
    13: 0x4A13F0, 14: 0x4A13E0, 15: 0x4A13D0,
    16: 0x4A1208, 17: 0x4A11F8, 18: 0x4A11E8, 19: 0x4A11A4, 20: 0x4A1190, 21: 0x4A117C,
    22: 0x4A11D8, 23: 0x4A11C8, 24: 0x4A11B8,
    25: 0x4A1374, 26: 0x4A1364, 27: 0x4A1358, 28: 0x4A134C, 29: 0x4A133C,
    30: 0x4A132C, 31: 0x4A1310, 32: 0x4A12F0, 33: 0x4A1300, 34: 0x4A131C,
    40: 0x4A1390, 41: 0x4A13C8, 42: 0x4A13B8, 43: 0x4A13B0, 44: 0x4A13A8, 45: 0x4A139C, 46: 0x4A1384,
    100: 0x4A12E0, 101: 0x4A12D0, 102: 0x4A12C0, 103: 0x4A12B0, 104: 0x4A1290,
    105: 0x4A1284, 106: 0x4A1274, 107: 0x4A1268, 108: 0x4A12A0,
    109: 0x4A1258, 110: 0x4A1248, 111: 0x4A1238, 112: 0x4A1228, 113: 0x4A1218,
}

UNIT_CN_G2 = {
    1: 0x49E878, 2: 0x49E868, 3: 0x49E858, 4: 0x49E84C, 5: 0x49E840, 6: 0x49E834,
    7: 0x49E824, 8: 0x49E814, 9: 0x49E804, 10: 0x49E7F8, 11: 0x49E7EC, 12: 0x49E7E0,
    13: 0x49E7D0, 14: 0x49E7C0, 15: 0x49E7B0,
    16: 0x49E668, 17: 0x49E65C, 18: 0x49E650, 19: 0x49E61C, 20: 0x49E60C, 21: 0x49E5FC,
    22: 0x49E644, 23: 0x49E638, 24: 0x49E62C,
    25: 0x49E754, 26: 0x49E748, 27: 0x49E73C, 28: 0x49E730, 29: 0x49E724,
    30: 0x49E718, 31: 0x49E6FC, 32: 0x49E6E0, 33: 0x49E6EC, 34: 0x49E708,
    40: 0x49E76C, 41: 0x49E7A4, 42: 0x49E794, 43: 0x49E78C, 44: 0x49E780, 45: 0x49E774, 46: 0x49E760,
    100: 0x49E6D8, 101: 0x49E6CC, 102: 0x49E6C0, 103: 0x49E6B4, 104: 0x49E698,
    105: 0x49E690, 106: 0x49E680, 107: 0x49E674, 108: 0x49E6A8,
    109: 0x49E368, 110: 0x49E358, 111: 0x49E348, 112: 0x49E338, 113: 0x49E328,
    115: 0x49E888,
}

# InfoBox 说明 VA（g1 FUN_00437130；g2 字节表0x435a18→跳表0x435954）
INFO_G1 = {
    1: 0x4A3A08, 2: 0x4A39A4, 3: 0x4A3948, 4: 0x4A38E8, 5: 0x4A38A0, 6: 0x4A3838,
    7: 0x4A37F8, 8: 0x4A379C, 9: 0x4A3750, 10: 0x4A3708, 11: 0x4A36BC, 12: 0x4A3670,
    13: 0x4A3620, 14: 0x4A35C8, 15: 0x4A356C,
    16: 0x4A32FC, 17: 0x4A32C8, 18: 0x4A3288, 19: 0x4A31A8, 20: 0x4A3184, 21: 0x4A3184,
    22: 0x4A3240, 23: 0x4A31FC, 24: 0x4A31D0,
    25: 0x4A2BB0, 26: 0x4A2B50, 27: 0x4A2B00, 28: 0x4A2AB4, 29: 0x4A2A40,
    30: 0x4A3118, 31: 0x4A30CC, 32: 0x4A3058, 33: 0x4A2FEC, 34: 0x4A2FA8,
    41: 0x4A3514, 42: 0x4A34B4, 43: 0x4A347C, 44: 0x4A341C, 45: 0x4A33AC, 46: 0x4A3348,
    100: 0x4A2F38, 101: 0x4A2EE4, 102: 0x4A2E84, 103: 0x4A2E08, 104: 0x4A2D58,
    105: 0x4A2D08, 106: 0x4A2C7C, 107: 0x4A2C2C, 108: 0x4A2D98,
}

INFO_G2 = {
    1: 0x4A0B38, 2: 0x4A0AD0, 3: 0x4A0A70, 4: 0x4A0A10, 5: 0x4A09C8, 6: 0x4A0960,
    7: 0x4A091C, 8: 0x4A08C0, 9: 0x4A0870, 10: 0x4A0828, 11: 0x4A07D8, 12: 0x4A0788,
    13: 0x4A0738, 14: 0x4A06E0, 15: 0x4A0680,
    16: 0x4A0408, 17: 0x4A03D0, 18: 0x4A0390, 19: 0x4A02A8, 20: 0x4A0284, 21: 0x4A0284,
    22: 0x4A0348, 23: 0x4A0300, 24: 0x4A02D0,
    25: 0x49FC90, 26: 0x49FC30, 27: 0x49FBE0, 28: 0x49FB90, 29: 0x49FB18,
    30: 0x4A0218, 31: 0x4A01C8, 32: 0x4A0150, 33: 0x4A00E0, 34: 0x4A0098,
    41: 0x4A0628, 42: 0x4A05C8, 43: 0x4A0590, 44: 0x4A0530, 45: 0x4A04C0, 46: 0x4A0458,
    100: 0x4A0028, 101: 0x49FFD0, 102: 0x49FF70, 103: 0x49FEF0, 104: 0x49FE40,
    105: 0x49FDF0, 106: 0x49FD60, 107: 0x49FD10, 108: 0x49FE80,
}

CATEGORY = {
    1: "defense", 2: "defense", 3: "defense", 4: "land", 5: "land", 6: "land",
    7: "land", 8: "land", 9: "land", 10: "land", 11: "land", 12: "land",
    13: "land", 14: "land", 15: "land",
    16: "building", 17: "building", 18: "building", 19: "building", 20: "building", 21: "building",
    22: "building", 23: "building", 24: "building",
    25: "defense", 26: "defense", 27: "defense", 28: "defense", 29: "defense",
    30: "air", 31: "air", 32: "air", 33: "air", 34: "superweapon",
    40: "air", 41: "land", 42: "land", 43: "land", 44: "land", 45: "land", 46: "superweapon",
    100: "building", 101: "factory", 102: "factory", 103: "factory", 104: "factory",
    105: "building", 106: "building", 107: "building", 108: "factory",
    109: "defense", 110: "defense", 111: "defense", 112: "defense", 113: "defense",
    115: "other",
}

CAT_BASIS = {
    1: "名称「防空设施」+说明（发射两枚对空导弹）", 2: "名称+说明（四枚对空导弹）", 3: "名称+说明（六枚对空导弹）",
    4: "名称「炮兵」+说明（远距离射击）", 5: "同左", 6: "同左",
    7: "名称「装甲坦克」+说明（移动最快）", 8: "同左", 9: "同左",
    10: "名称「喷火器」+说明（火焰喷射器）", 11: "同左", 12: "同左",
    13: "名称「特派坦克」+说明（激光发射器）", 14: "同左", 15: "同左",
    16: "名称「流入」+说明（提炼10g黄金）", 17: "同左(20g)", 18: "同左(30g)",
    19: "名称「流入」+说明（研究指数模式）", 20: "同左", 21: "同左（与20共用同一说明）",
    22: "名称「流入」+说明（生产模式提速10%）", 23: "同左(20%)", 24: "同左(30%)",
    25: "说明「便宜的炮塔」", 26: "说明「防空系统…发射四个地对空导弹」", 27: "说明「炮塔装配有离子武器」",
    28: "说明「快速开火的旋转炮塔」", 29: "说明「集束炮塔…」",
    30: "说明「轰炸机…空投多枚炸弹」", 31: "说明「运兵飞船…运送陆地作战单位」",
    32: "说明「战斗机…不会被击落」", 33: "说明「连环轰炸机…」", 34: "说明「星体炸弹能毁掉整个地区」→大杀器",
    40: "说明/任务文本：飞碟可飞行、占领/升级/修理", 41: "说明「阿莫科斯…超级机器人」", 42: "说明「阿它默德…地对空导弹（机器人）」",
    43: "说明「四个高速火炮的机器人」", 44: "说明「超远距离射程的超级机器人」", 45: "说明「阿基里斯…瞬间毁掉陆地单位」",
    46: "说明「罗根炸弹…毁掉整个地区」→大杀器",
    100: "说明「这是你的总部…」", 101: "说明「这种工厂生产得很快」", 102: "同左（中级作战单位）", 103: "同左（重型单位）",
    104: "说明「能提供空中打击力量」", 105: "说明「把金子转变成金钱」", 106: "说明「研究指数是在这儿得到的」",
    107: "说明「利用风能制造能源」", 108: "说明「工厂生产的超级机器人…」",
    109: "英文名 Top Sentry 系列（塔炮哨戒）", 110: "同左", 111: "同左", 112: "同左", 113: "同左",
    115: "名称「缩略地图」为界面元素",
}

UNIT_SUMMARY = {
    1: "可发射两枚对空导弹的轻型防空炮塔", 2: "可发射四枚对空导弹的中型防空炮塔", 3: "可发射六枚对空导弹的重型防空炮塔",
    4: "射速慢但射程远的轻型炮兵", 5: "长炮管大口径的中型炮兵", 6: "双炮管远射的重型炮兵",
    7: "移动最快的标准轻型坦克", 8: "双炮管可旋转炮台的中型坦克", 9: "三炮筒重型装甲坦克",
    10: "装配火焰喷射器的快速轻型单位", 11: "威力更大的喷火器与更好装甲的中型单位", 12: "重型装甲双喷火装置单位",
    13: "机动性与远距离激光兼备的轻型特派坦克", 14: "熔解粒子炮筒的中型特派坦克", 15: "重型粒子炮特派坦克",
    16: "金矿生产模式：一次提炼10克黄金", 17: "金矿生产模式：一次提炼20克黄金", 18: "金矿生产模式：一次提炼30克黄金",
    19: "研究指数生产模式：一次两个研究指数", 20: "研究指数生产模式：一次一个研究指数", 21: "同20（共用说明）",
    22: "工厂生产模式：制造提速10%", 23: "工厂生产模式：制造提速20%", 24: "工厂生产模式：制造提速30%",
    25: "打击轻型单位的便宜炮塔", 26: "发射四枚对空导弹的防空炮塔", 27: "装配离子武器、射程较远的炮塔",
    28: "快速开火的旋转炮塔", 29: "装甲厚重、爆炸性强的集束炮塔",
    30: "一次空投多枚炸弹的轰炸机", 31: "运送陆地单位的运兵飞船", 32: "高速不会被击落的战斗机",
    33: "一次释放很强能量的连环轰炸机", 34: "能毁掉整个地区的星体炸弹风暴",
    40: "可占领/升级/修理建筑的飞行单位", 41: "装配双离子炮的超级机器人", 42: "发射四枚地对空导弹的机器人",
    43: "装备四个高速火炮的机器人", 44: "超远射程双旋转炮台的机器人", 45: "瞬间毁掉陆地单位的近战机器人",
    46: "可毁掉整个地区的罗根炸弹",
    100: "玩家基地核心，生产飞碟，唯一天然免疫空袭/罗根炸弹的建筑",
    101: "快速生产轻型单位的工厂", 102: "生产中级单位的工厂（需研究指数）", 103: "生产重型慢速单位的工厂",
    104: "提供空中打击力量的建筑", 105: "把金子转变成金钱的建筑", 106: "产出研究指数的建筑",
    107: "利用风能制造能源的建筑", 108: "生产超级机器人的工厂",
    109: "塔炮 Top Sentry G10", 110: "塔炮 Top Sentry A20", 111: "塔炮 Top Sentry G30",
    112: "塔炮 Top Sentry G40", 113: "塔炮 Top Sentry G50",
    115: "界面：缩略地图",
}

WEAPONS = [
    "4x AG bombs", "F-M waves", "reinforcements", "body", "HE bombs", "18x grenades",
    "44mm", "plasma", "4x antiair rockets", "Nuclear bomb", "laser", "atomic hyperblast",
    "4x magma", "2x laser", "black hole mass", "fusion lambda", "2x R.X. napalm",
    "R.X. napalm", "napalm", "armour piercing", "2x 50lbs shell", "50lbs shell",
    "25lbs shell", "6x antiair rockets", "2x antiair rockets",
]


def build_units():
    out = []

    def make_unit(uid, n):
        cn_g1 = s(S_G1_UNIT, UNIT_CN_G1[uid])
        cn_g2 = s(S_G2_UNIT, UNIT_CN_G2[uid])
        if cn_g1 != cn_g2:
            raise SystemExit("ID %d 两作中文名不一致: %r vs %r" % (uid, cn_g1, cn_g2))
        name = cn_g1
        name_en = s(S_G1_UNIT, UNIT_EN_G1[uid]) if uid in UNIT_EN_G1 else None
        info = None
        info_src = []
        if uid in INFO_G1:
            info = s(S_G1_INFOBOX, INFO_G1[uid])
            info_src.append("FUN_00437130 case 分支→0x%x" % INFO_G1[uid])
        if uid in INFO_G2:
            g2_info = s(S_G2_INFOBOX, INFO_G2[uid])
            if uid == 1 and 0x4A0B80 in S_G2_INFOBOX:
                g2_info = g2_info + S_G2_INFOBOX[0x4A0B80]
            if (info is not None and g2_info.replace("。", "").strip() != info.replace("。", "").strip()
                    and g2_info.strip(". ") not in info and info not in g2_info):
                raise SystemExit("ID %d 两作说明不一致:\nG1: %r\nG2: %r" % (uid, info, g2_info))
            info_src.append("g2 InfoBox 字节表0x435a18→0x%x" % INFO_G2[uid])
        if uid in (109, 110, 111, 112, 113, 115):
            info = None
            info_src = []
        src = [
            "%s 名称函数 FUN_0042b180（case %d→0x%x）" % (G1_EXE, uid, UNIT_CN_G1[uid]),
            "%s 名称函数字节表0x42a178→跳表0x42a090（ID %d→0x%x）" % (G2_EXE, uid, UNIT_CN_G2[uid]),
        ]
        if uid in UNIT_EN_G1:
            src.append("%s 英文名函数字节表0x42b108→跳表0x42b020（ID %d→0x%x）"
                       % (G1_EXE, uid, UNIT_EN_G1[uid]))
        if info_src:
            src.append("%s InfoBox %s" % (G1_EXE, "；".join(info_src)))
        src.append("分类依据: %s" % CAT_BASIS[uid])
        return {
            "id": "u-%03d" % n, "games": ["g1", "g2"],
            "name": name, "nameEn": name_en,
            "category": CATEGORY[uid], "unitId": uid,
            "summary": UNIT_SUMMARY[uid], "description": info,
            "weapons": [], "stats": [], "image": None,
            "sources": src,
        }

    def make_weapon(w, n):
        return {
            "id": "u-%03d" % n, "games": ["g1", "g2"],
            "name": w, "nameEn": None,
            "category": "other", "unitId": None,
            "summary": "武器名称表条目（英文原文，游戏内未汉化）", "description": None,
            "weapons": [], "stats": [], "image": None,
            "sources": [
                "%s .data 0x4a1798–0x4a18dc 武器名表（research/mining-g1-weapons-credits.txt）" % G1_EXE,
                "%s .data 0x49e8a8–0x49e9ec 同表" % G2_EXE,
            ],
        }

    units = [make_unit(uid, 0) for uid in CATEGORY]
    units = units + [make_weapon(w, 0) for w in WEAPONS]
    units.sort(key=lambda u: (u["category"], u["unitId"] if u["unitId"] is not None else 10**9))
    for i, u in enumerate(units, start=1):
        u["id"] = "u-%03d" % i
    return units


def build_credits():
    people_slovak = ["Vlado Hudak", "Ludo Velas", "Richard Max", "Martin Sabo Balog",
                     "Marcel Ratvaj", "Pavol Kovacik", "Juraj Koci", "Kathleen Gallen",
                     "Michal Pekarik", "Radoslav Marusa", "Vlado Saffa"]
    cn = ["宋文韬", "董敏", "王雯", "徐欢", "肖峰", "向涛", "韩慧侠", "岩月", "张立刚", "延美花", "张学峰"]
    return {
        "sections": [
            {"title": "Programming", "people": ["Emil Popovic"], "games": ["g1", "g2"]},
            {"title": "Artwork and Animations", "people": ["Stefan Pavelka"], "games": ["g1", "g2"]},
            {"title": "Music and Sfx", "people": ["Martin Demsky"], "games": ["g1", "g2"]},
            {"title": "Special thanks to", "people": people_slovak, "games": ["g1", "g2"]},
            {"title": None, "people": cn, "games": ["g1"],
             "note": "汉化人员：原文无分组标题，位于 Special thanks 组之后，以「@」(0x4a1ae4) 与「!」(0x4a19b0) 空行标记分隔；显示顺序按 FUN(0x42df50–0x42e337) push 顺序转写（先 push 者先显示）。"},
        ],
        "sources": [
            "%s .data 0x4a1958–0x4a1ae8（research/mining-g1-weapons-credits.txt）；名单构建 FUN push 顺序 0x42df6d(!Programming)→0x42e325(@张学峰)，空行标记 0x4a19b0='!' 0x4a1ae4='@'" % G1_EXE,
            "%s .data 0x49ea6c–0x49eb8c（research/mining-g2-credits.txt，斯洛伐克团队同，无汉化人员名单）" % G2_EXE,
        ],
    }


def build_hotkeys():
    hk = [
        ("在地图上浏览", "方向键"), ("选择飞碟", "H 或 数字键 +"),
        ("回到已选择的作战单位", "数字键 回车"), ("返回上一则信息", "空格键 或 数字键 0"),
        ("返回总部", "Back Space"), ("查看战火下的作战单位", "Tab"),
        ("选择所有看得见的作战单位", "数字键 *"), ("选择所有看得见的对空作战单位", "数字键 /"),
        ("选择所有看得见的坦克单位", "数字键 -"), ("附加选项", "Esc"),
        ("浏览地图上的每一处", "数字键 1-9"), ("选择位置（定义战略位置）", "Shift + 数字键 1-9"),
        ("选择集结指分（集结点）", "R"), ("分散", "X"),
        ("迫使作战单位袭击（推动袭击）", "Ctrl 或 Alt"), ("放置一个炮塔", "1 – 5"),
        ("增加作战单位", "Shift"), ("快速保存", "F5"), ("快速读取", "Shift + F5"),
        ("暂停", "P"), ("显示游戏中的热键", "F1"), ("显示简报", "F2"),
        ("直接退出", "F12"), ("聊天（多人游戏）", "回车"),
        ("优先指挥飞碟", "数字键 + 且鼠标左键"), ("居中观察飞碟", "数字键 + 且 数字键 回车"),
    ]
    out = []
    for action, keys in hk:
        src = "g1 ReadMe.doc「游戏热键设置」节"
        if "坦克" in action or "对空作战单位" in action or "飞碟" in action:
            src = "g1 ReadMe.doc「游戏热键设置」/「提示和决窍」节（两处表述略有出入，原样收录）"
        out.append({"action": action, "keys": keys, "games": ["g1", "g2"], "source": src})
    return out


def main():
    missions = build_missions()
    games_order = {"g1": 0, "g2": 1, "g12": 2}
    type_order = {"campaign": 0, "tutorial": 1, "network": 2}
    missions.sort(key=lambda m: (games_order.get("g12" if len(m["games"]) > 1 else m["game"], 9),
                                 type_order[m["type"]], m["order"]))
    units = build_units()
    credits = build_credits()
    hotkeys = build_hotkeys()
    DATA.mkdir(exist_ok=True)
    for name, obj in [("missions.json", missions), ("units.json", units),
                      ("credits.json", credits), ("hotkeys.json", hotkeys)]:
        p = (DATA / name).resolve()
        if not p.is_relative_to(DATA.resolve()):
            raise SystemExit("输出越界")
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("written %s" % p)


if __name__ == "__main__":
    main()

