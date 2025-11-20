from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.global_firewall_ruleset import GlobalFirewallRuleset


T = TypeVar("T", bound="GetGlobalFirewallRulesetResponse200")


@_attrs_define
class GetGlobalFirewallRulesetResponse200:
    """
    Attributes:
        data (GlobalFirewallRuleset): Legacy type for the global firewall ruleset, now the default workspace.
    """

    data: GlobalFirewallRuleset

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
        from ..models.global_firewall_ruleset import GlobalFirewallRuleset

        d = dict(src_dict)
        data = GlobalFirewallRuleset.from_dict(d.pop("data"))

        get_global_firewall_ruleset_response_200 = cls(
            data=data,
        )

        return get_global_firewall_ruleset_response_200
