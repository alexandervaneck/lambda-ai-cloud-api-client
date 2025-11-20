from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance import Instance


T = TypeVar("T", bound="InstanceTerminateResponse")


@_attrs_define
class InstanceTerminateResponse:
    """
    Attributes:
        terminated_instances (list[Instance]): The list of instances that were successfully terminated.
    """

    terminated_instances: list[Instance]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        terminated_instances = []
        for terminated_instances_item_data in self.terminated_instances:
            terminated_instances_item = terminated_instances_item_data.to_dict()
            terminated_instances.append(terminated_instances_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminated_instances": terminated_instances,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance import Instance

        d = dict(src_dict)
        terminated_instances = []
        _terminated_instances = d.pop("terminated_instances")
        for terminated_instances_item_data in _terminated_instances:
            terminated_instances_item = Instance.from_dict(terminated_instances_item_data)

            terminated_instances.append(terminated_instances_item)

        instance_terminate_response = cls(
            terminated_instances=terminated_instances,
        )

        instance_terminate_response.additional_properties = d
        return instance_terminate_response

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
