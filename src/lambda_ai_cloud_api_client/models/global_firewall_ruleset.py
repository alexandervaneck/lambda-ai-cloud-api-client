from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.firewall_rule import FirewallRule


T = TypeVar("T", bound="GlobalFirewallRuleset")


@_attrs_define
class GlobalFirewallRuleset:
    """Legacy type for the global firewall ruleset, now the default workspace.

    Attributes:
        id (Literal['global']): The unique identifier of the firewall ruleset.
        name (Literal['Global Firewall Rules']): The name of the firewall ruleset.
        rules (list[FirewallRule]): The list of firewall rules in this ruleset.
    """

    id: Literal["global"]
    name: Literal["Global Firewall Rules"]
    rules: list[FirewallRule]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "rules": rules,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_rule import FirewallRule

        d = dict(src_dict)
        id = cast(Literal["global"], d.pop("id"))
        if id != "global":
            raise ValueError(f"id must match const 'global', got '{id}'")

        name = cast(Literal["Global Firewall Rules"], d.pop("name"))
        if name != "Global Firewall Rules":
            raise ValueError(f"name must match const 'Global Firewall Rules', got '{name}'")

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = FirewallRule.from_dict(rules_item_data)

            rules.append(rules_item)

        global_firewall_ruleset = cls(
            id=id,
            name=name,
            rules=rules,
        )

        global_firewall_ruleset.additional_properties = d
        return global_firewall_ruleset

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
