"""Helpers for the new-post skill.

  python .claude/hooks/post_tools.py png <name> "<Title>"   create the 1280x720 placeholder PNG
  python .claude/hooks/post_tools.py count <file> [<file>...] print body character counts
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
IMG_RE = re.compile(r"!\[.*?\]\(.*?\)\s*")


def placeholder_png(name: str, title: str):
    from PIL import Image, ImageDraw, ImageFont

    out = ROOT / "posts" / name / f"{name}.png"
    img = Image.new("RGB", (1280, 720), (230, 238, 248))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("segoeuib.ttf", 44)
    except OSError:
        font = ImageFont.load_default(44)
    draw.multiline_text((640, 360), f"{title}\n(placeholder 16:9)", font=font,
                        fill=(105, 105, 105), anchor="mm", align="center")
    img.save(out, "PNG")
    print(out)


def count(files):
    for f in files:
        text = IMG_RE.sub("", Path(f).read_text(encoding="utf-8")).strip()
        print(f"{len(text):6d}  {f}")


if __name__ == "__main__":
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd == "png" and len(args) == 2:
        placeholder_png(*args)
    elif cmd == "count" and args:
        count(args)
    else:
        sys.exit(__doc__)
