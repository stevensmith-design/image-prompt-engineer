#!/usr/bin/env python3
"""Copy text from stdin to the system clipboard (macOS, Windows, Linux).

Standard library only. Exits non-zero if no clipboard tool is available.

  python3 copy_prompt.py <<'PROMPT'
  A ceramic mug of black coffee on a worn oak windowsill...
  PROMPT
"""

import shutil
import subprocess
import sys

# Tried in order; the first one installed is used.
CLIPBOARD_COMMANDS = [
    ["pbcopy"],                             # macOS
    ["clip.exe"],                           # Windows, including WSL
    ["clip"],                               # Windows
    ["wl-copy"],                            # Linux, Wayland
    ["xclip", "-selection", "clipboard"],   # Linux, X11
    ["xsel", "--clipboard", "--input"],     # Linux, X11
]


def main():
    text = sys.stdin.read().strip()
    if not text:
        print("error: nothing to copy", file=sys.stderr)
        sys.exit(1)
    for command in CLIPBOARD_COMMANDS:
        if shutil.which(command[0]):
            encoding = "utf-16" if command[0].startswith("clip") else "utf-8"
            subprocess.run(command, input=text.encode(encoding), check=True)
            print(f"Copied {len(text)} characters to the clipboard.")
            return
    print("error: no clipboard tool found (pbcopy, clip, wl-copy, xclip or xsel)", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
