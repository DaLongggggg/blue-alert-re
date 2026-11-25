#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 data/ 下的四份 JSON 是否符合数据契约。

用法: python -I research/validate_data.py
校验项: schema 字段、id 唯一、games 合法、sources 非空、枚举值、排序、类型。
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
GAMES = {"g1", "g2"}
MISSION_TYPES = {"campaign", "tutorial", "network"}
UNIT_CATS = {"building", "factory", "defense", "land", "air", "superweapon", "other"}

errors = []
warns = []


def err(msg):
    errors.append(msg)


def check_games(obj, where):
    gs = obj.get("games")
    if not isinstance(gs, list) or not gs or not all(g in GAMES for g in gs):
        err(f"{where}: games 非法: {gs!r}")
    if obj.get("game") not in GAMES:
        err(f"{where}: game 非法: {obj.get('game')!r}")


def main():
    # missions.json
    p = DATA / "missions.json"
    missions = json.loads(p.read_text(encoding="utf-8"))
    ids = set()
    req_m = ["id", "game", "games", "code", "order", "type", "title", "baseCode",
             "expectedNo", "difficulty", "opponent", "objective", "briefing",
             "note", "files", "media", "sources"]
    for m in missions:
        w = f"missions[{m.get('id')}]"
        for k in req_m:
            if k not in m:
                err(f"{w}: 缺字段 {k}")
        if m["id"] in ids:
            err(f"{w}: id 重复")
        ids.add(m["id"])
        check_games(m, w)
        if m["type"] not in MISSION_TYPES:
            err(f"{w}: type 非法 {m['type']!r}")
        if not isinstance(m["sources"], list) or not m["sources"]:
            err(f"{w}: sources 为空")
        if not isinstance(m["files"], dict):
            err(f"{w}: files 非法")
        if m["type"] == "campaign" and not m["files"].get("map"):
            err(f"{w}: campaign 缺 map 文件")
        if m["type"] == "network" and not m["files"].get("net"):
            err(f"{w}: network 缺 net 文件")
        for k in ("title", "baseCode", "expectedNo", "difficulty", "opponent",
                  "objective", "briefing", "note"):
            if m.get(k) is not None and not isinstance(m[k], (str, int)):
                err(f"{w}: {k} 类型异常 {type(m[k])}")
    # 排序约定：g1→g2→g12（games 跨两作的条目归 g12 组），组内 campaign→tutorial→network，
    # order 升序（order 缺失视为排最后）。战役与联机图的 order 各自从 1 计数，故不能只按 (game, order) 排。
    gorder = {"g1": 0, "g2": 1, "g12": 2}
    torder = {"campaign": 0, "tutorial": 1, "network": 2}
    full = [(gorder["g12" if len(m["games"]) > 1 else m["game"]],
             torder[m["type"]],
             m["order"] if m["order"] is not None else 10**9) for m in missions]
    if full != sorted(full):
        warns.append("missions 未按 (game组, type, order) 排序")
    print(f"missions.json: {len(missions)} 条")

    # units.json
    units = json.loads((DATA / "units.json").read_text(encoding="utf-8"))
    ids = set()
    req_u = ["id", "games", "name", "nameEn", "category", "unitId", "summary",
             "description", "weapons", "stats", "image", "sources"]
    for u in units:
        w = f"units[{u.get('id')}]"
        for k in req_u:
            if k not in u:
                err(f"{w}: 缺字段 {k}")
        if u["id"] in ids:
            err(f"{w}: id 重复")
        ids.add(u["id"])
        gs = u.get("games")
        if not isinstance(gs, list) or not gs or not all(g in GAMES for g in gs):
            err(f"{w}: games 非法")
        if u["category"] not in UNIT_CATS:
            err(f"{w}: category 非法 {u['category']!r}")
        if not isinstance(u["sources"], list) or not u["sources"]:
            err(f"{w}: sources 为空")
        if not u.get("name"):
            err(f"{w}: name 为空")
    uk = [(u["category"], u["unitId"] if u["unitId"] is not None else 10**9) for u in units]
    if uk != sorted(uk):
        warns.append("units 未按 (category, unitId) 排序")
    print(f"units.json: {len(units)} 条")

    # credits.json
    credits = json.loads((DATA / "credits.json").read_text(encoding="utf-8"))
    if "sections" not in credits or not isinstance(credits["sections"], list):
        err("credits: 缺 sections")
    else:
        for i, s_ in enumerate(credits["sections"]):
            if "people" not in s_ or not isinstance(s_["people"], list) or not s_["people"]:
                err(f"credits.sections[{i}]: people 为空")
            if "games" not in s_ or not s_["games"]:
                err(f"credits.sections[{i}]: games 为空")
        if not credits.get("sources"):
            err("credits: sources 为空")
    print(f"credits.json: {len(credits.get('sections', []))} 组")

    # hotkeys.json
    hotkeys = json.loads((DATA / "hotkeys.json").read_text(encoding="utf-8"))
    for i, h in enumerate(hotkeys):
        if not h.get("action") or not h.get("keys"):
            err(f"hotkeys[{i}]: action/keys 为空")
        if not isinstance(h.get("games"), list) or not h["games"]:
            err(f"hotkeys[{i}]: games 为空")
        if not h.get("source"):
            err(f"hotkeys[{i}]: source 为空")
    print(f"hotkeys.json: {len(hotkeys)} 条")

    for w in warns:
        print(f"WARN: {w}")
    if errors:
        print(f"FAIL: {len(errors)} 个错误")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: 全部校验通过")


if __name__ == "__main__":
    main()
