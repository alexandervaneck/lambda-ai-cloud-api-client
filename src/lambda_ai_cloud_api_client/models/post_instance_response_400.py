from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters


T = TypeVar("T", bound="PostInstanceResponse400")


@_attrs_define
class PostInstanceResponse400:
    """
    Attributes:
        error (ApiErrorInvalidParameters):
    """

    error: ApiErrorInvalidParameters

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
        from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters

        d = dict(src_dict)
        error = ApiErrorInvalidParameters.from_dict(d.pop("error"))

        post_instance_response_400 = cls(
            error=error,
        )

        return post_instance_response_400
