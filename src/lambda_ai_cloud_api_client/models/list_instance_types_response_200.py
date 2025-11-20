from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.instance_types import InstanceTypes


T = TypeVar("T", bound="ListInstanceTypesResponse200")


@_attrs_define
class ListInstanceTypesResponse200:
    """
    Attributes:
        data (InstanceTypes):  Example: {'gpu_1x_gh200': {'instance_type': {'name': 'gpu_1x_gh200', 'description': '1x
            GH200 (96 GB)', 'gpu_description': 'GH200 (96 GB)', 'price_cents_per_hour': 149, 'specs': {'vcpus': 64,
            'memory_gib': 432, 'storage_gib': 4096, 'gpus': 1}}, 'regions_with_capacity_available': [{'name': 'us-west-1',
            'description': 'California, USA'}]}}.
    """

    data: InstanceTypes

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_types import InstanceTypes

        d = dict(src_dict)
        data = InstanceTypes.from_dict(d.pop("data"))

        list_instance_types_response_200 = cls(
            data=data,
        )

        return list_instance_types_response_200
