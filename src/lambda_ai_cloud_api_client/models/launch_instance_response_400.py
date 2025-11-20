from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_file_system_in_wrong_region import ApiErrorFileSystemInWrongRegion
    from ..models.api_error_insufficient_capacity import ApiErrorInsufficientCapacity
    from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
    from ..models.api_error_launch_resource_not_found import ApiErrorLaunchResourceNotFound
    from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded


T = TypeVar("T", bound="LaunchInstanceResponse400")


@_attrs_define
class LaunchInstanceResponse400:
    """
    Attributes:
        error (ApiErrorFileSystemInWrongRegion | ApiErrorInsufficientCapacity | ApiErrorInvalidParameters |
            ApiErrorLaunchResourceNotFound | ApiErrorQuotaExceeded):
    """

    error: (
        ApiErrorFileSystemInWrongRegion
        | ApiErrorInsufficientCapacity
        | ApiErrorInvalidParameters
        | ApiErrorLaunchResourceNotFound
        | ApiErrorQuotaExceeded
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_file_system_in_wrong_region import ApiErrorFileSystemInWrongRegion
        from ..models.api_error_insufficient_capacity import ApiErrorInsufficientCapacity
        from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
        from ..models.api_error_launch_resource_not_found import ApiErrorLaunchResourceNotFound

        error: dict[str, Any]
        if isinstance(
            self.error,
            (
                ApiErrorFileSystemInWrongRegion,
                ApiErrorInsufficientCapacity,
                ApiErrorInvalidParameters,
                ApiErrorLaunchResourceNotFound,
            ),
        ):
            error = self.error.to_dict()
        else:
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
        from ..models.api_error_file_system_in_wrong_region import ApiErrorFileSystemInWrongRegion
        from ..models.api_error_insufficient_capacity import ApiErrorInsufficientCapacity
        from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
        from ..models.api_error_launch_resource_not_found import ApiErrorLaunchResourceNotFound
        from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded

        d = dict(src_dict)

        def _parse_error(
            data: object,
        ) -> (
            ApiErrorFileSystemInWrongRegion
            | ApiErrorInsufficientCapacity
            | ApiErrorInvalidParameters
            | ApiErrorLaunchResourceNotFound
            | ApiErrorQuotaExceeded
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = ApiErrorFileSystemInWrongRegion.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_1 = ApiErrorInsufficientCapacity.from_dict(data)

                return error_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_2 = ApiErrorInvalidParameters.from_dict(data)

                return error_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_3 = ApiErrorLaunchResourceNotFound.from_dict(data)

                return error_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_4 = ApiErrorQuotaExceeded.from_dict(data)

            return error_type_4

        error = _parse_error(d.pop("error"))

        launch_instance_response_400 = cls(
            error=error,
        )

        return launch_instance_response_400
