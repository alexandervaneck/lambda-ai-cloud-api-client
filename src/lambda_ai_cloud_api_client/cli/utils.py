from __future__ import annotations

from pathlib import Path

def get_rsync_ignore_args(project_root: Path | None = None) -> list[str]:
    """
    Check for .lambda-ai-ignore or .gitignore and return rsync --exclude-from args.
    """
    if project_root is None:
        project_root = Path.cwd()

    ignore_files = [".lambda-ai-ignore", ".gitignore"]
    for ignore_file in ignore_files:
        path = project_root / ignore_file
        if path.exists():
            return ["--exclude-from", str(path)]
    
    return []
