"""
Staging script: copy templates + references from the old naive-ui-skills repo
into the new naive-ui/ skill layout. Idempotent; run once after init_skill.py.
"""
import os
import shutil
from pathlib import Path

OLD = Path(r"d:/1 code/naive-ui-skills")
NEW = Path(r"d:/1 code/naive-ui-skill/naive-ui")

def ensure(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def copytree_if_exists(src: Path, dst: Path):
    if not src.exists():
        print(f"[skip] missing {src}")
        return 0
    ensure(dst)
    count = 0
    for f in src.iterdir():
        target = dst / f.name
        if f.is_dir():
            count += copytree_if_exists(f, target)
        else:
            shutil.copy2(f, target)
            count += 1
    return count

# 1) 6 templates
n = copytree_if_exists(OLD / "templates", NEW / "assets" / "templates")
print(f"templates copied: {n}")

# 2) 36 rules
n = copytree_if_exists(OLD / "naive-ui" / "references", NEW / "references" / "rules")
print(f"rules copied: {n}")

# 3) 9 foundation/design skills (only their SKILL.md as <name>.md)
foundation_map = {
    "naive-ui-quickstart": "quickstart.md",
    "naive-ui-theming": "theming.md",
    "naive-ui-dark-mode": "dark-mode.md",
    "naive-ui-i18n": "i18n.md",
    "naive-ui-ssr": "ssr.md",
    "naive-ui-design-color": "design-color.md",
    "naive-ui-design-border": "design-border.md",
    "naive-ui-design-typography": "design-typography.md",
    "naive-ui-design-layout": "design-layout.md",
    "naive-ui-design-overview": "design-overview.md",
}
fd_count = 0
for src_dir, dst_name in foundation_map.items():
    src = OLD / src_dir / "SKILL.md"
    dst = NEW / "references" / "foundation" / dst_name
    if src.exists():
        ensure(dst)
        shutil.copy2(src, dst)
        fd_count += 1
print(f"foundation copied: {fd_count}")

print("Done.")
