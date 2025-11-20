from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.filesystem import Filesystem


T = TypeVar("T", bound="CreateFilesystemResponse200")


@_attrs_define
class CreateFilesystemResponse200:
    """
    Attributes:
        data (Filesystem): Information about a shared filesystem.
    """

    data: Filesystem

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
        from ..models.filesystem import Filesystem

        d = dict(src_dict)
        data = Filesystem.from_dict(d.pop("data"))

        create_filesystem_response_200 = cls(
            data=data,
        )

        return create_filesystem_response_200
