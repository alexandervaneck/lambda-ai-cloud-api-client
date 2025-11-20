from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_types_item import InstanceTypesItem


T = TypeVar("T", bound="InstanceTypes")


@_attrs_define
class InstanceTypes:
    """
    Example:
        {'gpu_1x_gh200': {'instance_type': {'name': 'gpu_1x_gh200', 'description': '1x GH200 (96 GB)',
            'gpu_description': 'GH200 (96 GB)', 'price_cents_per_hour': 149, 'specs': {'vcpus': 64, 'memory_gib': 432,
            'storage_gib': 4096, 'gpus': 1}}, 'regions_with_capacity_available': [{'name': 'us-west-1', 'description':
            'California, USA'}]}}

    """

    additional_properties: dict[str, InstanceTypesItem] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_types_item import InstanceTypesItem

        d = dict(src_dict)
        instance_types = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = InstanceTypesItem.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        instance_types.additional_properties = additional_properties
        return instance_types

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> InstanceTypesItem:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: InstanceTypesItem) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
