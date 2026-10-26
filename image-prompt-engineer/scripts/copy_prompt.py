#!/usr/bin/env python3
"""Copy text from stdin to the system clipboard (macOS, Windows, Linux).

Standard library only. Exits non-zero if no clipboard tool works.

  python3 copy_prompt.py <<'PROMPT'
  A ceramic mug of black coffee on a worn oak windowsill...
  PROMPT
"""

import os
import shutil
import subprocess
import sys

# Tried in order; the first one that succeeds is used.
CLIPBOARD_COMMANDS = [
    ["pbcopy"],                             # macOS
    ["clip.exe"],                           # Windows, including WSL
    ["clip"],                               # Windows
    ["wl-copy"],                            # Linux, Wayland
    ["xclip", "-selection", "clipboard"],   # Linux, X11
    ["xsel", "--clipboard", "--input"],     # Linux, X11
]


def main():
    # Read bytes and decode as UTF-8 so Japanese and other non-ASCII text survives on every platform.
    text = sys.stdin.buffer.read().decode("utf-8").strip()
    if not text:
        print("error: nothing to copy", file=sys.stderr)
        sys.exit(1)
    for command in CLIPBOARD_COMMANDS:
        if not shutil.which(command[0]):
            continue
        is_windows_clip = command[0].startswith("clip")
        encoding = "utf-16" if is_windows_clip else "utf-8"
        # pbcopy reads input in the current locale; force UTF-8 so non-ASCII text isn't garbled.
        env = {**os.environ, "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}
        try:
            subprocess.run(command, input=text.encode(encoding), env=env, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
        print(f"Copied {len(text)} characters to the clipboard.")
        return
    print("error: no working clipboard tool found (pbcopy, clip, wl-copy, xclip or xsel)", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
