#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_units_images.py — 把精灵图/资料框全息图绑定到 data/units.json。

绑定来源（两层，都只引用 docs/public/media/units/ 下实际存在的文件）：

1. 精灵层：research/selected-sprites.json（精灵解码会话的标注数据）。
   按 unit 字段与 units.json 的 name 匹配：先精确匹配，再唯一前缀匹配
   （如「战斗机」→「战斗机袭击」），最后用括号注释里的中文名/英文名反查
   （如「研究实验室（Research Lab…）」→ 太阳能搜集器）。
   匹配后须人工看图核对；核对不通过的条目写入 DENY_BINDINGS 不予绑定。

2. 全息图层：资料框绿色全息图（InfoBox/*.tsp 解码单帧，经
   tools/decode_sprites.py --select 渲染进 docs/public/media/units/holo-*.png）。
   文件名与单元的对应关系来自目录结构（InfoBox/1=空袭、2=建筑+炮塔、
   3/4/5=轻/中/重型陆战单位、6=生产模式、7=特种家族），逐张人工看图核对后
   以显式表格写在本脚本内（HOLOGRAM_BINDINGS）。

同时为每条数据计算展示分组字段 group（unit/building/weapon/mode/other），
规则见 assign_group()，完全由既有字段推导。

用法（python -I）：
    python -I tools/link_units_images.py            # 绑定并写回 data/units.json
    python -I tools/link_units_images.py --dry      # 只打印报告，不写文件
"""
import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 人工核对结论（看图核对后做出的绑定/拒绝决定，均记录在 research/report-units.md）
# ---------------------------------------------------------------------------

# 形态与单位说明矛盾、归属存疑的精灵：暂不绑定（InfoBox/7 全息图证明
# 41-45 五台「超级机器人」均为步行机甲，而这三张蓝色精灵是履带车体）。
DENY_BINDINGS = {
    "units/tank-cougar-g12.png": "蓝色履带车精灵；InfoBox/7 全息图显示美洲狮等五台机器人均为步行机甲，形态不符，归属待考",
    "units/tank-gatling-g12.png": "蓝色履带车精灵；同上（格林机关炮为「双旋转炮台的超级机器人」），归属待考",
    "units/tank-kodiak-g12.png": "蓝色履带车精灵；同上（科迪亚克为「双离子炮」超级机器人），归属待考",
}

# 精灵层自动匹配不到、但看图核对后确认归属的额外绑定。
# 键为 selected-sprites.json 的 file 原值（含 units/ 或 ui/ 前缀），站点路径即 /media/<file>。
EXTRA_BINDINGS = {
    "units/unit-radiation-g12.png": {
        "id": "u-081",
        "note": "蓝军涂装游戏精灵（履带车体+顶部辐射圆鼓，与 InfoBox/7/N 全息图同形）",
    },
    "ui/radar-frame-g12.png": {
        "id": "u-054",
        "note": "游戏内界面图（雷达/缩略地图框体）",
    },
}

# 资料框绿色全息图绑定表：文件 →（单位 id, 角色 image/gallery, 图注）
HOLO_LABEL = "资料框绿色全息图"
HOLO_MODE_LABEL = "资料框绿色全息图（生产模式图标）"
HOLOGRAM_BINDINGS = {
    # 生产模式（InfoBox/6，文件名 1/2/3 与流入等级一一对应）
    "holo-gold-influx-1-g12.png": ("u-006", "image", HOLO_MODE_LABEL),
    "holo-gold-influx-2-g12.png": ("u-007", "image", HOLO_MODE_LABEL),
    "holo-gold-influx-3-g12.png": ("u-008", "image", HOLO_MODE_LABEL),
    "holo-research-influx-1-g12.png": ("u-009", "image", HOLO_MODE_LABEL),
    "holo-research-influx-2-g12.png": ("u-010", "image", HOLO_MODE_LABEL),
    "holo-research-influx-3-g12.png": ("u-011", "image", HOLO_MODE_LABEL),
    "holo-energy-influx-1-g12.png": ("u-012", "image", HOLO_MODE_LABEL),
    "holo-energy-influx-2-g12.png": ("u-013", "image", HOLO_MODE_LABEL),
    "holo-energy-influx-3-g12.png": ("u-014", "image", HOLO_MODE_LABEL),
    # 建筑（InfoBox/2，文件名即建筑英文名缩写）
    "holo-headquarters-g12.png": ("u-015", "gallery", HOLO_LABEL),
    "holo-gold-mine-g12.png": ("u-016", "gallery", HOLO_LABEL),
    "holo-research-lab-g12.png": ("u-017", "gallery", HOLO_LABEL),
    "holo-windtrap-g12.png": ("u-018", "gallery", HOLO_LABEL),
    "holo-light-factory-g12.png": ("u-032", "gallery", HOLO_LABEL),
    "holo-medium-factory-g12.png": ("u-033", "gallery", HOLO_LABEL),
    "holo-heavy-factory-g12.png": ("u-034", "gallery", HOLO_LABEL),
    "holo-air-navigator-g12.png": ("u-035", "gallery", HOLO_LABEL),
    "holo-walker-factory-g12.png": ("u-036", "gallery", HOLO_LABEL),
    # 空袭（InfoBox/1，五文件对应五条空袭条目）
    "holo-bomber-g12.png": ("u-001", "gallery", HOLO_LABEL),
    "holo-carryall-g12.png": ("u-002", "gallery", HOLO_LABEL),
    "holo-fighter-g12.png": ("u-003", "gallery", HOLO_LABEL),
    "holo-tripler-g12.png": ("u-004", "gallery", HOLO_LABEL),
    "holo-meteor-g12.png": ("u-080", "image", HOLO_LABEL),
    # 陆战单位（InfoBox/3/4/5 = 轻/中/重型，大小与武器数量随等级递增，已逐张核对）
    "holo-light-antiair-g12.png": ("u-019", "gallery", HOLO_LABEL),
    "holo-medium-antiair-g12.png": ("u-020", "gallery", HOLO_LABEL),
    "holo-heavy-antiair-g12.png": ("u-021", "gallery", HOLO_LABEL),
    "holo-light-artillery-g12.png": ("u-037", "gallery", HOLO_LABEL),
    "holo-medium-artillery-g12.png": ("u-038", "gallery", HOLO_LABEL),
    "holo-heavy-artillery-g12.png": ("u-039", "gallery", HOLO_LABEL),
    "holo-light-panzer-g12.png": ("u-040", "gallery", HOLO_LABEL),
    "holo-medium-panzer-g12.png": ("u-041", "gallery", HOLO_LABEL),
    "holo-heavy-panzer-g12.png": ("u-042", "gallery", HOLO_LABEL),
    "holo-light-flamer-g12.png": ("u-043", "gallery", HOLO_LABEL),
    "holo-medium-flamer-g12.png": ("u-044", "gallery", HOLO_LABEL),
    "holo-heavy-flamer-g12.png": ("u-045", "gallery", HOLO_LABEL),
    "holo-light-special-g12.png": ("u-046", "gallery", HOLO_LABEL),
    "holo-medium-special-g12.png": ("u-047", "gallery", HOLO_LABEL),
    "holo-heavy-special-g12.png": ("u-048", "gallery", HOLO_LABEL),
    # 特种家族（InfoBox/7）：仅绑定看图核对可断定的两条，其余三台机器人
    # （科迪亚克/空对空复仇者/美洲狮/格林机关炮中的未定者）暂不绑定。
    "holo-achilles-g12.png": ("u-053", "gallery", HOLO_LABEL + "（步行机甲，双爪近战与说明吻合）"),
    "holo-rogon-g12.png": ("u-081", "gallery", HOLO_LABEL + "（特种家族中唯一履带式全息图）"),
}

# ---------------------------------------------------------------------------
# 展示分组（group 字段）：完全由既有字段推导，不引入新事实
# ---------------------------------------------------------------------------

def assign_group(u):
    uid = u.get("unitId")
    try:
        uid_n = int(uid)
    except (TypeError, ValueError):
        uid_n = None
    category = u.get("category")
    if category == "other":
        # category=other 且无游戏内 ID → 武器名表条目；有 ID → 界面元素（缩略地图）
        return "weapon" if uid_n is None else "other"
    if uid_n is not None and 16 <= uid_n <= 24:
        return "mode"  # 金币/研究指数/能量流入 1-3（建筑生产模式）
    if category in ("building", "factory", "defense"):
        return "building"
    return "unit"


# ---------------------------------------------------------------------------
# 精灵层匹配
# ---------------------------------------------------------------------------

def base_name(unit_field):
    """取标注中括号前的主体名称；以括号开头（无主体名）返回空串。"""
    s = str(unit_field).strip()
    if s.startswith(("（", "(")):
        return ""
    for ch in ("（", "("):
        i = s.find(ch)
        if i > 0:
            return s[:i].strip()
    return s.strip()


def find_unit_by_sprite(sprite, units):
    """精灵条目 → (unit, 匹配方式)；匹配不到返回 (None, 原因)。"""
    raw = str(sprite.get("unit", ""))
    name = base_name(raw)
    if not name:
        return None, "无主体名称（标注待考）"
    exact = [u for u in units if u.get("name") == name]
    if len(exact) == 1:
        return exact[0], "精确匹配"
    prefixes = [u for u in units if str(u.get("name", "")).startswith(name) and len(name) >= 2]
    if len(prefixes) == 1:
        return prefixes[0], "唯一前缀匹配"
    # 括号注释反查：注释里出现某单位的中文名或英文名（候选唯一才绑定）
    cands = set()
    for u in units:
        if u.get("name") and u["name"] in raw:
            cands.add(u["id"])
        if u.get("nameEn") and u["nameEn"] in raw:
            cands.add(u["id"])
    if len(cands) == 1:
        target = cands.pop()
        for u in units:
            if u["id"] == target:
                return u, "注释反查（中/英文名）"
    return None, "无法唯一匹配"


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def site_path(name):
    return "/media/units/" + name


def main():
    ap = argparse.ArgumentParser(description="绑定单位图片到 data/units.json")
    ap.add_argument("--dry", action="store_true", help="只打印报告，不写文件")
    args = ap.parse_args()

    units_file = (ROOT / "data" / "units.json").resolve(strict=True)
    sprites_file = (ROOT / "research" / "selected-sprites.json").resolve(strict=True)
    media_dir = (ROOT / "docs" / "public" / "media" / "units").resolve(strict=True)
    out_file = (ROOT / "data" / "units.json").resolve()
    if not out_file.is_relative_to(ROOT / "data"):
        raise SystemExit("输出路径越界")
    if not (ROOT / "data").is_relative_to(ROOT):
        raise SystemExit("数据目录异常")

    units = json.loads(units_file.read_text(encoding="utf-8"))
    sprites = json.loads(sprites_file.read_text(encoding="utf-8"))
    units_by_id = {u["id"]: u for u in units if u.get("id")}

    # --- 精灵层 ---
    bound = 0
    unmatched = []
    for sp in sprites:
        fname = str(sp.get("file", ""))
        if fname in EXTRA_BINDINGS:
            # 额外绑定优先（含 ui/ 图，如雷达框体），站点路径 = /media/<file 原值>
            extra = EXTRA_BINDINGS[fname]
            u = units_by_id.get(extra["id"])
            disk = (ROOT / "docs" / "public" / "media" / fname).resolve()
            if u is None or not str(disk).startswith(str(media_dir.parent)) or not disk.is_file():
                unmatched.append((fname, "EXTRA 绑定不可用（单位缺失或文件不存在）"))
                continue
            u["image"] = "/media/" + fname
            u["imageNote"] = extra["note"]
            bound += 1
            continue
        if not fname.startswith("units/"):
            continue  # 其余 ui/ 图（菜单按钮等）不参与单位绑定
        filename = fname.split("/", 1)[1]
        disk = media_dir / filename
        if not disk.is_file():
            unmatched.append((fname, "媒体文件不存在"))
            continue
        if fname in DENY_BINDINGS:
            unmatched.append((fname, "人工核对拒绝：" + DENY_BINDINGS[fname]))
            continue
        u, how = find_unit_by_sprite(sp, units)
        if u is None:
            unmatched.append((fname, how))
            continue
        u["image"] = site_path(filename)
        # 图注只取 what 文案；置信度留在 selected-sprites.json 与汇报里，不上页面
        note = str(sp.get("what", "") or "").strip()
        u["imageNote"] = note or None
        bound += 1

    # --- 全息图层 ---
    holo_bound = 0
    holo_missing = []
    for filename, (uid, role, label) in HOLOGRAM_BINDINGS.items():
        disk = media_dir / filename
        if not disk.is_file():
            holo_missing.append(filename)
            continue
        u = units_by_id.get(uid)
        if u is None:
            holo_missing.append(filename + "（单位 " + uid + " 不存在）")
            continue
        gallery = u.get("gallery")
        if not isinstance(gallery, list):
            gallery = []
        entry = {"image": site_path(filename), "label": label}
        if role == "image" and not u.get("image"):
            u["image"] = site_path(filename)
            u["imageNote"] = label
        else:
            if entry not in gallery and u.get("image") != site_path(filename):
                gallery.append(entry)
            u["gallery"] = gallery
        holo_bound += 1

    # --- group 字段 ---
    groups = {"unit": 0, "building": 0, "mode": 0, "weapon": 0, "other": 0}
    for u in units:
        g = assign_group(u)
        u["group"] = g
        groups[g] += 1

    # --- 汇总 ---
    with_image = [u for u in units if u.get("image")]
    with_gallery = [u for u in units if isinstance(u.get("gallery"), list) and u["gallery"]]
    print("精灵层绑定 %d 张；全息层绑定 %d 张（缺文件 %d）" % (bound, holo_bound, len(holo_missing)))
    for m in holo_missing:
        print("  全息图缺文件:", m)
    print("未绑定精灵 %d 张：" % len(unmatched))
    for fname, why in unmatched:
        print("  -", fname, "→", why)
    print("group 分布:", groups)
    print("有主图单位 %d / %d；有图集单位 %d" % (len(with_image), len(units), len(with_gallery)))

    if args.dry:
        print("（--dry，未写文件）")
        return

    # --- 写回（固定字段顺序）---
    order = ["id", "games", "name", "nameEn", "category", "group", "unitId",
             "summary", "description", "weapons", "stats",
             "image", "imageNote", "gallery", "sources"]
    out_units = []
    for u in units:
        rest = {k: v for k, v in u.items() if k not in order}
        rebuilt = {}
        for k in order:
            if k in u:
                rebuilt[k] = u[k]
            elif k == "gallery":
                rebuilt[k] = None
        rebuilt.update(rest)
        out_units.append(rebuilt)
    text = json.dumps(out_units, ensure_ascii=False, indent=2) + "\n"
    out_file.write_text(text, encoding="utf-8")
    print("已写回", out_file)


if __name__ == "__main__":
    main()
