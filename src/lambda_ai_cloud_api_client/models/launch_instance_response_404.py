from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_launch_resource_not_found import ApiErrorLaunchResourceNotFound


T = TypeVar("T", bound="LaunchInstanceResponse404")


@_attrs_define
class LaunchInstanceResponse404:
    """
    Attributes:
        error (ApiErrorLaunchResourceNotFound):
    """

    error: ApiErrorLaunchResourceNotFound

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
        from ..models.api_error_launch_resource_not_found import ApiErrorLaunchResourceNotFound

        d = dict(src_dict)
        error = ApiErrorLaunchResourceNotFound.from_dict(d.pop("error"))

        launch_instance_response_404 = cls(
            error=error,
        )

        return launch_instance_response_404
