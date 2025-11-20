from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_filesystem_not_found import ApiErrorFilesystemNotFound


T = TypeVar("T", bound="FilesystemDeleteResponse404")


@_attrs_define
class FilesystemDeleteResponse404:
    """
    Attributes:
        error (ApiErrorFilesystemNotFound):
    """

    error: ApiErrorFilesystemNotFound

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_filesystem_not_found import ApiErrorFilesystemNotFound

        d = dict(src_dict)
        error = ApiErrorFilesystemNotFound.from_dict(d.pop("error"))

        filesystem_delete_response_404 = cls(
            error=error,
        )

        return filesystem_delete_response_404
