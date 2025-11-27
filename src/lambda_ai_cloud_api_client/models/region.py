from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_region_code import PublicRegionCode

T = TypeVar("T", bound="Region")


@_attrs_define
class Region:
    """
    Attributes:
        name (PublicRegionCode):
        description (str): The location represented by the region code.
    """

    name: PublicRegionCode
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def __eq__(self, other: str | Region | PublicRegionCode) -> bool:
        if isinstance(other, (Region, PublicRegionCode)):
            return self.name == other.name

        return self.name.value == other

    def to_dict(self) -> dict[str, Any]:
        name = self.name.value

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = PublicRegionCode(d.pop("name"))

        description = d.pop("description")

        region = cls(
            name=name,
            description=description,
        )

        region.additional_properties = d
        return region

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
