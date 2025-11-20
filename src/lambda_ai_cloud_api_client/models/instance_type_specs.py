from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InstanceTypeSpecs")


@_attrs_define
class InstanceTypeSpecs:
    """
    Attributes:
        vcpus (int): The number of virtual CPUs.
        memory_gib (int): The amount of RAM in gibibytes (GiB).
        storage_gib (int): The amount of storage in gibibytes (GiB).
        gpus (int): The number of GPUs.
    """

    vcpus: int
    memory_gib: int
    storage_gib: int
    gpus: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vcpus = self.vcpus

        memory_gib = self.memory_gib

        storage_gib = self.storage_gib

        gpus = self.gpus

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vcpus": vcpus,
                "memory_gib": memory_gib,
                "storage_gib": storage_gib,
                "gpus": gpus,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vcpus = d.pop("vcpus")

        memory_gib = d.pop("memory_gib")

        storage_gib = d.pop("storage_gib")

        gpus = d.pop("gpus")

        instance_type_specs = cls(
            vcpus=vcpus,
            memory_gib=memory_gib,
            storage_gib=storage_gib,
            gpus=gpus,
        )

        instance_type_specs.additional_properties = d
        return instance_type_specs

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
