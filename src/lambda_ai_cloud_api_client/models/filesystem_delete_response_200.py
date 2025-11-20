from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.filesystem_delete_response import FilesystemDeleteResponse


T = TypeVar("T", bound="FilesystemDeleteResponse200")


@_attrs_define
class FilesystemDeleteResponse200:
    """
    Attributes:
        data (FilesystemDeleteResponse):
    """

    data: FilesystemDeleteResponse

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
        from ..models.filesystem_delete_response import FilesystemDeleteResponse

        d = dict(src_dict)
        data = FilesystemDeleteResponse.from_dict(d.pop("data"))

        filesystem_delete_response_200 = cls(
            data=data,
        )

        return filesystem_delete_response_200
