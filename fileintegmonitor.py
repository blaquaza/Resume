#!/usr/bin/env python3
"""
File Integrity Monitor
Baselines a directory's file hashes and later detects additions,
deletions, or modifications. Standard library only.
"""

import os
import json
import hashlib
import argparse
from datetime import datetime

BASELINE_FILE = ".integrity_baseline.json"
CHUNK_SIZE = 65536


def hash_file(path: str) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def walk_files(root: str, exclude: set[str]) -> list[str]:
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for name in filenames:
            if name == BASELINE_FILE:
                continue
            paths.append(os.path.join(dirpath, name))
    return paths


def build_baseline(root: str, exclude: set[str]) -> dict:
    baseline = {}
    for path in walk_files(root, exclude):
        rel = os.path.relpath(path, root)
        try:
            baseline[rel] = {
                "hash": hash_file(path),
                "size": os.path.getsize(path),
            }
        except (OSError, PermissionError):
            continue
    return baseline


def save_baseline(root: str, baseline: dict) -> None:
    data = {"created": datetime.now().isoformat(), "files": baseline}
    with open(os.path.join(root, BASELINE_FILE), "w") as f:
        json.dump(data, f, indent=2)


def load_baseline(root: str) -> dict:
    path = os.path.join(root, BASELINE_FILE)
    if not os.path.exists(path):
        raise FileNotFoundError("No baseline found. Run with --init first.")
    with open(path) as f:
        return json.load(f)["files"]


def compare(root: str, exclude: set[str]) -> dict:
    old = load_baseline(root)
    current_paths = walk_files(root, exclude)
    current = {}
    for path in current_paths:
        rel = os.path.relpath(path, root)
        try:
            current[rel] = {"hash": hash_file(path), "size": os.path.getsize(path)}
        except (OSError, PermissionError):
            continue

    added = sorted(set(current) - set(old))
    removed = sorted(set(old) - set(current))
    modified = sorted(
        rel for rel in (set(current) & set(old))
        if current[rel]["hash"] != old[rel]["hash"]
    )
    return {"added": added, "removed": removed, "modified": modified}


def print_report(changes: dict) -> None:
    print("\n--- File Integrity Report ---")
    total = len(changes["added"]) + len(changes["removed"]) + len(changes["modified"])
    if total == 0:
        print("No changes detected. All files match baseline.")
    else:
        if changes["modified"]:
            print(f"\nMODIFIED ({len(changes['modified'])}):")
            for f in changes["modified"]:
                print(f"  ~ {f}")
        if changes["added"]:
            print(f"\nADDED ({len(changes['added'])}):")
            for f in changes["added"]:
                print(f"  + {f}")
        if changes["removed"]:
            print(f"\nREMOVED ({len(changes['removed'])}):")
            for f in changes["removed"]:
                print(f"  - {f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Monitor a directory for file tampering.")
    parser.add_argument("directory", help="Directory to baseline or check")
    parser.add_argument("--init", action="store_true", help="Create a new baseline")
    parser.add_argument(
        "--exclude", nargs="*", default=[".git", "__pycache__", "node_modules"],
        help="Directory names to exclude"
    )
    args = parser.parse_args()

    root = os.path.abspath(args.directory)
    if not os.path.isdir(root):
        print(f"Not a valid directory: {root}")
        return

    exclude = set(args.exclude)

    if args.init:
        baseline = build_baseline(root, exclude)
        save_baseline(root, baseline)
        print(f"Baseline created for {len(baseline)} files in {root}")
    else:
        try:
            changes = compare(root, exclude)
            print_report(changes)
        except FileNotFoundError as e:
            print(e)


if __name__ == "__main__":
    main()