from __future__ import annotations

import os
import sys

def print_completion_script(shell: str) -> None:
    """
    Print the shell completion script for the given shell.
    """
    if shell not in ("bash", "zsh", "fish"):
        raise ValueError(f"Unsupported shell: {shell}")

    env_name = f"_LAI_COMPLETE"
    
    # We use click's built-in completion mechanism
    # The command to generate the script is usually:
    # _LAI_COMPLETE=bash_source lai
    
    if shell == "bash":
        print(f'eval "$({env_name}=bash_source lai)"')
    elif shell == "zsh":
        print(f'eval "$({env_name}=zsh_source lai)"')
    elif shell == "fish":
        print(f'eval "$({env_name}=fish_source lai)"')
