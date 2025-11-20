from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.firewall_rule import FirewallRule


T = TypeVar("T", bound="GlobalFirewallRulesetPatchRequest")


@_attrs_define
class GlobalFirewallRulesetPatchRequest:
    """Request to update the global firewall ruleset.

    Attributes:
        rules (list[FirewallRule] | Unset): The new firewall rules for the ruleset. If not provided, the rules will not
            be updated.
    """

    rules: list[FirewallRule] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_rule import FirewallRule

        d = dict(src_dict)
        _rules = d.pop("rules", UNSET)
        rules: list[FirewallRule] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = FirewallRule.from_dict(rules_item_data)

                rules.append(rules_item)

        global_firewall_ruleset_patch_request = cls(
            rules=rules,
        )

        global_firewall_ruleset_patch_request.additional_properties = d
        return global_firewall_ruleset_patch_request

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
