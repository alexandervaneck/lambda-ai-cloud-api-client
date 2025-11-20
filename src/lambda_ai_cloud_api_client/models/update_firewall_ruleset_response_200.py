from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.firewall_ruleset import FirewallRuleset


T = TypeVar("T", bound="UpdateFirewallRulesetResponse200")


@_attrs_define
class UpdateFirewallRulesetResponse200:
    """
    Attributes:
        data (FirewallRuleset): A collection of firewall rules that can be associated with instances.
    """

    data: FirewallRuleset

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_ruleset import FirewallRuleset

        d = dict(src_dict)
        data = FirewallRuleset.from_dict(d.pop("data"))

        update_firewall_ruleset_response_200 = cls(
            data=data,
        )

        return update_firewall_ruleset_response_200
