from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance import Instance


T = TypeVar("T", bound="InstanceRestartResponse")


@_attrs_define
class InstanceRestartResponse:
    """
    Attributes:
        restarted_instances (list[Instance]): The list of instances that were successfully restarted.
    """

    restarted_instances: list[Instance]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        restarted_instances = []
        for restarted_instances_item_data in self.restarted_instances:
            restarted_instances_item = restarted_instances_item_data.to_dict()
            restarted_instances.append(restarted_instances_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "restarted_instances": restarted_instances,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance import Instance

        d = dict(src_dict)
        restarted_instances = []
        _restarted_instances = d.pop("restarted_instances")
        for restarted_instances_item_data in _restarted_instances:
            restarted_instances_item = Instance.from_dict(restarted_instances_item_data)

            restarted_instances.append(restarted_instances_item)

        instance_restart_response = cls(
            restarted_instances=restarted_instances,
        )

        instance_restart_response.additional_properties = d
        return instance_restart_response

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
