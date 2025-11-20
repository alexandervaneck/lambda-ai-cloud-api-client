from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_region_code import PublicRegionCode

if TYPE_CHECKING:
    from ..models.firewall_rule import FirewallRule


T = TypeVar("T", bound="FirewallRulesetCreateRequest")


@_attrs_define
class FirewallRulesetCreateRequest:
    """Request to create a new firewall ruleset.

    Attributes:
        name (str): The name of the firewall ruleset.
        region (PublicRegionCode):
        rules (list[FirewallRule]): The firewall rules to include in the ruleset.
    """

    name: str
    region: PublicRegionCode
    rules: list[FirewallRule]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        region = self.region.value

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "region": region,
                "rules": rules,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_rule import FirewallRule

        d = dict(src_dict)
        name = d.pop("name")

        region = PublicRegionCode(d.pop("region"))

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = FirewallRule.from_dict(rules_item_data)

            rules.append(rules_item)

        firewall_ruleset_create_request = cls(
            name=name,
            region=region,
            rules=rules,
        )

        firewall_ruleset_create_request.additional_properties = d
        return firewall_ruleset_create_request

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
