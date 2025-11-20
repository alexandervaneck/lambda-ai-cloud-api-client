from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_duplicate import ApiErrorDuplicate
    from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
    from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded


T = TypeVar("T", bound="CreateFilesystemResponse400")


@_attrs_define
class CreateFilesystemResponse400:
    """
    Attributes:
        error (ApiErrorDuplicate | ApiErrorInvalidParameters | ApiErrorQuotaExceeded):
    """

    error: ApiErrorDuplicate | ApiErrorInvalidParameters | ApiErrorQuotaExceeded

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_duplicate import ApiErrorDuplicate
        from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded

        error: dict[str, Any]
        if isinstance(self.error, (ApiErrorDuplicate, ApiErrorQuotaExceeded)):
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
        from ..models.api_error_duplicate import ApiErrorDuplicate
        from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
        from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded

        d = dict(src_dict)

        def _parse_error(data: object) -> ApiErrorDuplicate | ApiErrorInvalidParameters | ApiErrorQuotaExceeded:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = ApiErrorDuplicate.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_1 = ApiErrorQuotaExceeded.from_dict(data)

                return error_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_2 = ApiErrorInvalidParameters.from_dict(data)

            return error_type_2

        error = _parse_error(d.pop("error"))

        create_filesystem_response_400 = cls(
            error=error,
        )

        return create_filesystem_response_400
