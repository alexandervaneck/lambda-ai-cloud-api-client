from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.firewall_rule import FirewallRule
    from ..models.region import Region


T = TypeVar("T", bound="FirewallRuleset")


@_attrs_define
class FirewallRuleset:
    """A collection of firewall rules that can be associated with instances.

    Attributes:
        id (str): The unique identifier of the firewall ruleset.
        name (str): The name of the firewall ruleset.
        region (Region):
        rules (list[FirewallRule]): The list of firewall rules in this ruleset.
        created (datetime.datetime): The date and time at which the firewall ruleset was created. Formatted as an ISO
            8601 timestamp.
        instance_ids (list[str]): The IDs of instances this firewall ruleset is associated with.
    """

    id: str
    name: str
    region: Region
    rules: list[FirewallRule]
    created: datetime.datetime
    instance_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        region = self.region.to_dict()

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        created = self.created.isoformat()

        instance_ids = self.instance_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "region": region,
                "rules": rules,
                "created": created,
                "instance_ids": instance_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_rule import FirewallRule
        from ..models.region import Region

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        region = Region.from_dict(d.pop("region"))

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = FirewallRule.from_dict(rules_item_data)

            rules.append(rules_item)

        created = isoparse(d.pop("created"))

        instance_ids = cast(list[str], d.pop("instance_ids"))

        firewall_ruleset = cls(
            id=id,
            name=name,
            region=region,
            rules=rules,
            created=created,
            instance_ids=instance_ids,
        )

        firewall_ruleset.additional_properties = d
        return firewall_ruleset

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
