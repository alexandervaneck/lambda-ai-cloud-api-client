from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_instance_not_found import ApiErrorInstanceNotFound


T = TypeVar("T", bound="RestartInstanceResponse404")


@_attrs_define
class RestartInstanceResponse404:
    """
    Attributes:
        error (ApiErrorInstanceNotFound):
    """

    error: ApiErrorInstanceNotFound

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
        from ..models.api_error_instance_not_found import ApiErrorInstanceNotFound

        d = dict(src_dict)
        error = ApiErrorInstanceNotFound.from_dict(d.pop("error"))

        restart_instance_response_404 = cls(
            error=error,
        )

        return restart_instance_response_404
