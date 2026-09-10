"""
Renumbers TC-### IDs in a markdown test plan sequentially, in the order
they appear in the file, regardless of gaps or duplicates.

Usage:
    python renumber_testcases.py Test_Plan_ParaBank_Specific.md

Rewrites the file in place. Run this any time you insert, delete, or
reorder test cases and don't want to renumber everything by hand.
"""
import re
import sys

def renumber(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    counter = [0]

    def replace(match):
        counter[0] += 1
        return f"TC-{counter[0]:03d}"

    new_text = re.sub(r"TC-\d{3}", replace, text)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

    print(f"Renumbered {counter[0]} test case IDs in {path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python renumber_testcases.py <path_to_test_plan.md>")
        sys.exit(1)
    renumber(sys.argv[1])
