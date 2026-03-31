#!/usr/bin/env python3
from __future__ import annotations

import argparse

from skillbank.inventory import entries_to_json, entries_to_markdown, scan_tree
from skillbank.paths import reports_root, skillbank_root
from skillbank.reports import write_json_report, write_markdown_report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true", help="Print markdown report")
    ap.add_argument("--write", action="store_true", help="Write markdown/json reports")
    args = ap.parse_args()

    entries = scan_tree(skillbank_root())
    data = entries_to_json(entries)
    body = entries_to_markdown(entries)

    if args.print and not args.write:
        print(body, end="")
        return

    if args.write:
        write_json_report(reports_root() / "skillbank-inventory.json", data)
        write_markdown_report(reports_root() / "skillbank-inventory.md", "SkillBank Inventory", body)
        print(f"Wrote inventory reports to {reports_root()}")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
