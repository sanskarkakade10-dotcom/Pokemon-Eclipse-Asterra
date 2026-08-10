#!/usr/bin/env python3
"""Validate the pinned FireRed starter integration points before a ROM build.

This is intentionally a source-validation gate, not a ROM patcher. It prevents
us from silently building against a different upstream script layout.
"""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
source = root / "build" / "pokefirered" / "data" / "maps" / "PalletTown_ProfessorOaksLab" / "scripts.inc"

if not source.exists():
    raise SystemExit(f"Missing FireRed starter script: {source}")

text = source.read_text(encoding="utf-8")
required = [
    "PalletTown_ProfessorOaksLab_ChooseStarterScene::",
    "VAR_TEMP_1",
    "VAR_TEMP_2",
    "VAR_TEMP_3",
    "VAR_TEMP_4",
    "PalletTown_ProfessorOaksLab_EventScript_RivalBattle::",
]

missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("Starter integration source changed; missing: " + ", ".join(missing))

print("FireRed starter integration points validated.")
