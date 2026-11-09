---
name: "design-decision-rules"
description: "Use when choosing design-system styles, constraints, layout patterns or light/dark mode for a UI from a product brief, or when writing/validating design-system decision rules (condition -> action JSON such as if_mobile, if_dashboard, style:..., constraint:..., pattern:..., mode:dark)."
---

# Design-system decision rules

A closed, non-executable grammar that maps a product brief (free text) to deterministic
design decisions. Rules are pure data: nothing in them is ever evaluated as code.

## Rule format
A JSON object mapping a **condition** to a non-empty array of unique **actions**:

```json
{
  "must_have": ["constraint:wcag-aa-contrast"],
  "if_dashboard": ["style:data-dense", "pattern:sidebar + KPI grid"],
  "if_mobile": ["constraint:touch-target-44px"],
  "if_luxury": ["style:editorial-serif", "mode:dark"]
}
```

- Conditions: `must_have` (always active) or one of the `if_*` keys in
  `scripts/decision_rules.py` (`CONDITION_SIGNALS`). A condition activates when any of
  its signal words appears as a whole word in the query (case-insensitive).
  Run `python3 scripts/apply_rules.py --conditions` to list them with their signals.
- Actions (prefix:value):
  - `style:<kebab-token>` — style id, collected in order, de-duplicated.
  - `constraint:<kebab-token>` — constraint id, collected, de-duplicated.
  - `pattern:<free text>` — layout pattern; last active rule wins.
  - `mode:dark` | `mode:light` — colour mode; last active rule wins.
- Duplicate keys, unknown conditions/prefixes, empty arrays and malformed tokens are rejected.

## Workflow
1. Write the rules to a JSON file (or use the project's existing one).
2. Validate and apply them to the brief:
   ```bash
   python3 .claude/skills/design-decision-rules/scripts/apply_rules.py rules.json "mobile booking app for a luxury spa"
   ```
   Output: `{"valid": true, "result": {"activated": [...], "style_ids": [...], "constraints": [...], "pattern": ..., "mode": ...}}`.
   Validation errors return `{"valid": false, "error": "..."}` with exit code 1.
3. Build the UI from `style_ids`, `constraints`, `pattern` and `mode`; cite the
   `activated` audit trail when explaining why a choice was made.

From Python, import `parse_decision_rules` and `apply_decision_rules` from
`scripts/decision_rules.py`.
