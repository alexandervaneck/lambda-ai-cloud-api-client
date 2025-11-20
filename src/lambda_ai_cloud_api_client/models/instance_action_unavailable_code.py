from enum import Enum


class InstanceActionUnavailableCode(str, Enum):
    VM_HAS_NOT_LAUNCHED = "vm-has-not-launched"
    VM_IS_TERMINATING = "vm-is-terminating"
    VM_IS_TOO_OLD = "vm-is-too-old"

    def __str__(self) -> str:
        return str(self.value)
