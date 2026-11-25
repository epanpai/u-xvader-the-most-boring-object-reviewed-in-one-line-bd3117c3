#!/usr/bin/env python3
"""The Most Boring Object, Reviewed in One Line — entry writer.

Writes the chosen one-line review of the bottle cap to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), then verifies
the written bytes match exactly.

The entry is a fixed constant: a one-star review of a bottle cap, 177
characters, one line. Why a bottle cap: the field is crowded with
doorstops, rubber bands, paperclips, dustpans and tea towels, while no
entry reviews the cap — yet its behaviour is instantly recognisable
(months guarding the fizz, one twist, one hiss, straight in the bin),
so the dullness itself carries the joke and the last words
("zero seconds of fame") sharpen it instead of trailing off.
The gate requires UTF-8 text of 1-200 characters,
not only whitespace, so this program validates length, single-line shape
and whitespace content before writing anything.
"""

import os
import sys

ENTRY = (
    "One star. The bottle cap guards the fizz for months, earns one "
    "twist and one hiss, then lands in the bin before you've taken a "
    "sip \u2014 a lifetime of loyalty, zero seconds of fame."
)


def validate(text: str) -> None:
    """Enforce the competition gate: 1-200 chars, single line, not blank.

    Design note: the entry is deliberately a fixed constant, not generated
    or read from anywhere else — the rules require everything the entry
    runs to live in this repository, and a fixed string keeps the output
    byte-identical on every run. The trailing-whitespace check below
    guards the punchline: the judge reads the entry exactly as written,
    so a stray space or newline at the end would be part of the text
    and could dull the final words ("zero seconds of fame.").
    """
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry length {len(text)} outside 1-200 chars")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip() or text.strip() == "":
        raise ValueError("entry must not be only whitespace or padded")
    if text != text.rstrip():
        raise ValueError("entry must not end with trailing whitespace")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise RuntimeError("written bytes differ from entry")
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
