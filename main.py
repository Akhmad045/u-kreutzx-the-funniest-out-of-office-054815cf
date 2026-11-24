"""Funniest out-of-office entry for make.fun.

Writes one line of an out-of-office auto-reply to /output/entry.txt
(or $ENTRY_OUTPUT when set). Stdlib only, deterministic, no network.

Validation guard enforces the competition gate before writing:
UTF-8 text, 1-140 characters, not only whitespace, single line,
no surrounding whitespace, no trailing newline. Raises instead of
writing invalid output.
"""

import os

ENTRY = "I'm out of the office until Monday \u2014 my auto-reply is handling my inbox now, and it's already asked for a raise."

MAX_CHARS = 140  # competition gate: 1-140 characters


def validate(text: str) -> bytes:
    """Enforce the competition gate; return the UTF-8 bytes to write."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    data = text.encode("utf-8")  # raises on non-encodable input
    decoded = data.decode("utf-8")  # raises on invalid UTF-8
    if decoded != text:
        raise ValueError("entry is not valid UTF-8 round-trip text")
    if not 1 <= len(decoded) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d" % (MAX_CHARS, len(decoded)))
    if not decoded.strip():
        raise ValueError("entry must not be only whitespace")
    if decoded != decoded.strip():
        raise ValueError("entry must have no surrounding whitespace")
    if "\n" in decoded or "\r" in decoded:
        raise ValueError("entry must be a single line")
    return data


def main():
    data = validate(ENTRY)
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
