from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.instance import Instance


T = TypeVar("T", bound="PostInstanceResponse200")


@_attrs_define
class PostInstanceResponse200:
    """
    Attributes:
        data (Instance): Detailed information about the instance.
    """

    data: Instance

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
        from ..models.instance import Instance

        d = dict(src_dict)
        data = Instance.from_dict(d.pop("data"))

        post_instance_response_200 = cls(
            data=data,
        )

        return post_instance_response_200
