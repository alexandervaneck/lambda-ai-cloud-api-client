from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.network_protocol import NetworkProtocol
from ..types import UNSET, Unset

T = TypeVar("T", bound="FirewallRule")


@_attrs_define
class FirewallRule:
    """
    Attributes:
        protocol (NetworkProtocol):
        source_network (str): The set of source IPv4 addresses from which you want to allow inbound
            traffic. These addresses must be specified in CIDR notation. You can
            specify individual public IPv4 CIDR blocks such as `1.2.3.4` or
            `1.2.3.4/32`, or you can specify `0.0.0.0/0` to allow access from any
            address.

            This value is a string consisting of a public IPv4 address optionally
            followed by a slash (/) and an integer mask (the network prefix).
            If no mask is provided, the API assumes `/32` by default.
        description (str): A human-readable description of the rule.
        port_range (list[int] | Unset): An inclusive range of network ports specified as `[min, max]`.
            Not allowed for the `icmp` protocol but required for the others.

            To specify a single port, list it twice (for example, `[22,22]`).
    """

    protocol: NetworkProtocol
    source_network: str
    description: str
    port_range: list[int] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        protocol = self.protocol.value

        source_network = self.source_network

        description = self.description

        port_range: list[int] | Unset = UNSET
        if not isinstance(self.port_range, Unset):
            port_range = self.port_range

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "protocol": protocol,
                "source_network": source_network,
                "description": description,
            }
        )
        if port_range is not UNSET:
            field_dict["port_range"] = port_range

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        protocol = NetworkProtocol(d.pop("protocol"))

        source_network = d.pop("source_network")

        description = d.pop("description")

        port_range = cast(list[int], d.pop("port_range", UNSET))

        firewall_rule = cls(
            protocol=protocol,
            source_network=source_network,
            description=description,
            port_range=port_range,
        )

        firewall_rule.additional_properties = d
        return firewall_rule

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
