#!/usr/bin/env python3
"""CLI: validate a decision-rules JSON file and apply it to a query.

Usage:
  python3 apply_rules.py RULES.json "query text"     # validate + apply
  python3 apply_rules.py RULES.json                  # validate only
  python3 apply_rules.py --conditions                # list allowed conditions
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decision_rules import (  # noqa: E402
    CONDITION_SIGNALS, apply_decision_rules, parse_decision_rules)


def main(argv):
    if len(argv) == 2 and argv[1] == "--conditions":
        listing = {"must_have": ["(always active)"]}
        listing.update({k: list(v) for k, v in sorted(CONDITION_SIGNALS.items())})
        print(json.dumps(listing, indent=2))
        return 0
    if len(argv) not in (2, 3):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        raw = handle.read()
    try:
        rules = parse_decision_rules(raw)
    except ValueError as error:
        print(json.dumps({"valid": False, "error": str(error)}, indent=2))
        return 1
    output = {"valid": True}
    if len(argv) == 3:
        output["result"] = apply_decision_rules(rules, argv[2])
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
