from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.firewall_rule import FirewallRule


T = TypeVar("T", bound="FirewallRulesListResponse200")


@_attrs_define
class FirewallRulesListResponse200:
    """
    Attributes:
        data (list[FirewallRule]):
    """

    data: list[FirewallRule]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_rule import FirewallRule

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = FirewallRule.from_dict(data_item_data)

            data.append(data_item)

        firewall_rules_list_response_200 = cls(
            data=data,
        )

        return firewall_rules_list_response_200
