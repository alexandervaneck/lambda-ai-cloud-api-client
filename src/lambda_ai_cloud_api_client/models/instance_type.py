from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_type_specs import InstanceTypeSpecs


T = TypeVar("T", bound="InstanceType")


@_attrs_define
class InstanceType:
    """
    Attributes:
        name (str): The name of the instance type.
        description (str): A description of the instance type.
        gpu_description (str): The type of GPU used by this instance type.
        price_cents_per_hour (int): The price of the instance type in US cents per hour.
        specs (InstanceTypeSpecs):
    """

    name: str
    description: str
    gpu_description: str
    price_cents_per_hour: int
    specs: InstanceTypeSpecs
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        gpu_description = self.gpu_description

        price_cents_per_hour = self.price_cents_per_hour

        specs = self.specs.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "gpu_description": gpu_description,
                "price_cents_per_hour": price_cents_per_hour,
                "specs": specs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_type_specs import InstanceTypeSpecs

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        gpu_description = d.pop("gpu_description")

        price_cents_per_hour = d.pop("price_cents_per_hour")

        specs = InstanceTypeSpecs.from_dict(d.pop("specs"))

        instance_type = cls(
            name=name,
            description=description,
            gpu_description=gpu_description,
            price_cents_per_hour=price_cents_per_hour,
            specs=specs,
        )

        instance_type.additional_properties = d
        return instance_type

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
