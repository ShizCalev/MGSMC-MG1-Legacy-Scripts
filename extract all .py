from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# ==========================================================
# CONFIG
# ==========================================================

SCRIPT_DIR = Path(__file__).resolve().parent
MGTOOLS_EXE = SCRIPT_DIR / "MGTools_Windows.exe"

TARGET_FILENAME = "english.raw"


# ==========================================================
# MAIN
# ==========================================================

def find_english_raw_files(root: Path) -> list[Path]:
    results: list[Path] = []

    for path in root.rglob(TARGET_FILENAME):
        if path.is_file():
            results.append(path)

    return results


def run_mgtools(raw_path: Path) -> bool:
    cmd = [
        str(MGTOOLS_EXE),
        "mg1",
        "export",
        str(raw_path)
    ]

    print(f"[RUN] {raw_path}")

    try:
        completed = subprocess.run(cmd, check=True)
        return completed.returncode == 0
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] MGTools failed on {raw_path}")
        print(exc)
        return False


def main() -> None:
    if not MGTOOLS_EXE.exists():
        print(f"[FATAL] MGTools_Windows.exe not found at: {MGTOOLS_EXE}")
        sys.exit(1)

    print(f"[INFO] Scanning under: {SCRIPT_DIR}")

    raw_files = find_english_raw_files(SCRIPT_DIR)

    if not raw_files:
        print("[INFO] No english.raw files found")
        return

    print(f"[INFO] Found {len(raw_files)} english.raw files")

    failed: list[Path] = []

    for raw in raw_files:
        ok = run_mgtools(raw)
        if not ok:
            failed.append(raw)

    print("")
    print("===== DONE =====")

    if failed:
        print(f"[WARN] {len(failed)} files failed:")
        for f in failed:
            print(f" - {f}")
    else:
        print("[INFO] All files processed successfully")


if __name__ == "__main__":
    main()
