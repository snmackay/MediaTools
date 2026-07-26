#!/usr/bin/env python3

import os
import argparse


def remove_empty_directories(root_path, dry_run=False):
    """
    Recursively remove empty directories starting from the bottom.

    Args:
        root_path (str): Root directory to scan.
        dry_run (bool): If True, only print what would be deleted.
    """
    removed_count = 0

    # Walk bottom-up so children are processed before parents.
    for current_dir, dirnames, filenames in os.walk(root_path, topdown=False):
        try:
            # If the directory is empty, remove it.
            if not os.listdir(current_dir):
                if dry_run:
                    print(f"[DRY RUN] Would remove: {current_dir}")
                else:
                    os.rmdir(current_dir)
                    print(f"Removed: {current_dir}")
                removed_count += 1
        except PermissionError:
            print(f"Permission denied: {current_dir}")
        except OSError as e:
            print(f"Could not remove {current_dir}: {e}")

    return removed_count


def main():
    parser = argparse.ArgumentParser(
        description="Delete empty directories recursively."
    )
    parser.add_argument(
        "path",
        help="Root directory to scan"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without deleting anything"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.")
        return

    count = remove_empty_directories(args.path, args.dry_run)

    if args.dry_run:
        print(f"\n{count} empty directories would be removed.")
    else:
        print(f"\nRemoved {count} empty directories.")


if __name__ == "__main__":
    main()