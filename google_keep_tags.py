#!/usr/bin/env python3
"""Simple script to apply labels in Google Keep using gkeepapi.

Usage:
 1. Install dependencies:
      pip install gkeepapi
 2. Set environment variables KEEP_EMAIL and KEEP_PASSWORD with your
    Google account credentials. Using an app password is recommended.
 3. Run the script:
      python google_keep_tags.py --note NOTE_ID --label LABEL

This script logs in to Google Keep, finds or creates the given label,
then applies it to the specified note.
"""

import os
import argparse
import gkeepapi


def login():
    email = os.environ.get("KEEP_EMAIL")
    password = os.environ.get("KEEP_PASSWORD")
    if not email or not password:
        raise ValueError("KEEP_EMAIL and KEEP_PASSWORD must be set")
    keep = gkeepapi.Keep()
    success = keep.login(email, password)
    if not success:
        raise RuntimeError("Login to Google Keep failed")
    return keep


def add_label(keep, note_id: str, label_name: str) -> None:
    note = keep.get(note_id)
    if note is None:
        raise ValueError(f"Note {note_id} not found")
    label = keep.findLabel(label_name)
    if label is None:
        label = keep.createLabel(label_name)
    note.labels.add(label)
    keep.sync()


def main() -> None:
    parser = argparse.ArgumentParser(description="Add or modify Google Keep labels")
    parser.add_argument("--note", required=True, help="ID of the note to modify")
    parser.add_argument("--label", required=True, help="Label to add to the note")
    args = parser.parse_args()

    keep = login()
    add_label(keep, args.note, args.label)
    print(f"Label '{args.label}' added to note {args.note}")


if __name__ == "__main__":
    main()
