from enum import Enum


class NetworkProtocol(str, Enum):
    ALL = "all"
    ICMP = "icmp"
    TCP = "tcp"
    UDP = "udp"

    def __str__(self) -> str:
        return str(self.value)
