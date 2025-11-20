from enum import Enum


class ImageArchitecture(str, Enum):
    ARM64 = "arm64"
    X86_64 = "x86_64"

    def __str__(self) -> str:
        return str(self.value)
