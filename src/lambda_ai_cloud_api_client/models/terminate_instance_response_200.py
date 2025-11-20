from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.instance_terminate_response import InstanceTerminateResponse


T = TypeVar("T", bound="TerminateInstanceResponse200")


@_attrs_define
class TerminateInstanceResponse200:
    """
    Attributes:
        data (InstanceTerminateResponse):
    """

    data: InstanceTerminateResponse

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
        from ..models.instance_terminate_response import InstanceTerminateResponse

        d = dict(src_dict)
        data = InstanceTerminateResponse.from_dict(d.pop("data"))

        terminate_instance_response_200 = cls(
            data=data,
        )

        return terminate_instance_response_200
