"""Merge posts/<name>/<name>.json into posts.json and posts-data.js (used by index.html).

Manual run (from anywhere):  python .claude/hooks/build_index.py
PostToolUse hook (Write|Edit): python .claude/hooks/build_index.py --hook
    reads the hook payload on stdin and rebuilds only when a post's .md/.json changed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
IMG_RE = re.compile(r"!\[.*?\]\(.*?\)\s*")
HOOK_PATH_RE = re.compile(r"posts[\\/][^\\/]+[\\/][^\\/]+\.(md|json)$")


def body_length(path: Path):
    if not path.exists():
        return None
    return len(IMG_RE.sub("", path.read_text(encoding="utf-8")).strip())


def build():
    posts = []
    for d in sorted((ROOT / "posts").iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        meta_path = d / f"{name}.json"
        if not meta_path.exists():
            print(f"skipping {name} (no {name}.json)", file=sys.stderr)
            continue
        m = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        posts.append({
            "name": name,
            "title": m.get("title"),
            "emoji": m.get("emoji"),
            "subtitle": m.get("subtitle"),
            "summary": m.get("summary"),
            "category": m.get("category"),
            "tags": list(m.get("tags") or []),
            "created": m.get("created"),
            "status": m.get("status"),
            "shortChars": body_length(d / f"{name}.md"),
            "longChars": body_length(d / f"{name}_long.md"),
            "files": {
                "short": (d / f"{name}.md").exists(),
                "long": (d / f"{name}_long.md").exists(),
                "prompt": (d / f"{name}_prompt.md").exists(),
                "image": (d / f"{name}.png").exists(),
            },
        })
    posts.sort(key=lambda p: p["name"])
    posts.sort(key=lambda p: p["created"] or "", reverse=True)  # stable: newest first, then name

    text = json.dumps(posts, indent=2, ensure_ascii=False)
    (ROOT / "posts.json").write_text(text, encoding="utf-8")
    (ROOT / "posts-data.js").write_text(f"window.POSTS = {text};\n", encoding="utf-8")
    print(f"Indexed {len(posts)} posts -> posts.json, posts-data.js")


def main():
    if "--hook" in sys.argv:
        try:
            payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
            path = payload.get("tool_input", {}).get("file_path", "")
        except (ValueError, AttributeError):
            return
        if not HOOK_PATH_RE.search(path or ""):
            return
    build()


if __name__ == "__main__":
    main()
