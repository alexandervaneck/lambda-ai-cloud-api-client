from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_type import InstanceType
    from ..models.region import Region


T = TypeVar("T", bound="InstanceTypesItem")


@_attrs_define
class InstanceTypesItem:
    """Detailed information and regional availability for the instance type.

    Attributes:
        instance_type (InstanceType):
        regions_with_capacity_available (list[Region]): A list of the regions in which this instance type is available.
    """

    instance_type: InstanceType
    regions_with_capacity_available: list[Region]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        instance_type = self.instance_type.to_dict()

        regions_with_capacity_available = []
        for regions_with_capacity_available_item_data in self.regions_with_capacity_available:
            regions_with_capacity_available_item = regions_with_capacity_available_item_data.to_dict()
            regions_with_capacity_available.append(regions_with_capacity_available_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "instance_type": instance_type,
                "regions_with_capacity_available": regions_with_capacity_available,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_type import InstanceType
        from ..models.region import Region

        d = dict(src_dict)
        instance_type = InstanceType.from_dict(d.pop("instance_type"))

        regions_with_capacity_available = []
        _regions_with_capacity_available = d.pop("regions_with_capacity_available")
        for regions_with_capacity_available_item_data in _regions_with_capacity_available:
            regions_with_capacity_available_item = Region.from_dict(regions_with_capacity_available_item_data)

            regions_with_capacity_available.append(regions_with_capacity_available_item)

        instance_types_item = cls(
            instance_type=instance_type,
            regions_with_capacity_available=regions_with_capacity_available,
        )

        instance_types_item.additional_properties = d
        return instance_types_item

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
