# content-author

Companion workspace for the course **Master Content Workflows with Claude Code: From Research to Published Post, No Coding Required**.

You describe a topic in plain English. Claude researches it and writes a short post, a long post and an image prompt, then a simple viewer page lists everything.

## What you need

- [Node.js](https://nodejs.org/) (LTS)
- [Python 3.11+](https://www.python.org/downloads/) (add it to PATH on Windows)
- [VS Code](https://code.visualstudio.com/) with the **Live Server** (`ritwickdey.LiveServer`) and **Claude Code** (`anthropic.claude-code`) extensions
- Pillow for the placeholder images: `pip install pillow`

## Quick start

1. Open this folder in VS Code (**File → Open Folder**) and open the Claude Code panel.
2. Ask for a post: `/new-post Top 5 Cities to Visit in Europe`
3. Right-click `index.html` and choose **Open with Live Server** to browse all posts.

## How it works

Each topic is one folder under `posts/`, named in snake_case, and every file uses the folder name as its prefix:

```
posts/<name>/
    <name>.md          short post (~500 characters)
    <name>_long.md     long post (~1000 characters)
    <name>_prompt.md   image prompt to paste into GPT (16:9)
    <name>.png         placeholder, replaced by the generated image
    <name>.json        metadata for the viewer
```

- **Skill:** `.claude/skills/new-post/SKILL.md` holds the rules, so you only give a topic.
- **Hook:** `.claude/settings.json` runs `build_index.py` after every post edit, keeping `posts.json` and `posts-data.js` current for `index.html`.
- **Helpers:** `.claude/hooks/post_tools.py` makes the placeholder PNG and counts characters.

To rebuild the index by hand: `python .claude/hooks/build_index.py`

## Course lessons

| # | Lesson | Covers |
|---|--------|--------|
| 1 | Welcome to Master Content Workflows | Course overview, what we'll build, and what you need |
| 2 | Set Up Your AI Content Workspace | Install Node.js, Python, VS Code, Live Server and Claude Code, then check everything works |
| 3 | Your First Claude Code Session | Start from an empty folder, send a first prompt, and learn what skills and hooks are |

Lesson slides live in `docs/`, which links to the course content project.
