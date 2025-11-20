from enum import Enum


class InstanceStatus(str, Enum):
    ACTIVE = "active"
    BOOTING = "booting"
    PREEMPTED = "preempted"
    TERMINATED = "terminated"
    TERMINATING = "terminating"
    UNHEALTHY = "unhealthy"

    def __str__(self) -> str:
        return str(self.value)
