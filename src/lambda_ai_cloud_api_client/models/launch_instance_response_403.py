from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_account_inactive import ApiErrorAccountInactive
    from ..models.api_error_invalid_billing_address import ApiErrorInvalidBillingAddress


T = TypeVar("T", bound="LaunchInstanceResponse403")


@_attrs_define
class LaunchInstanceResponse403:
    """
    Attributes:
        error (ApiErrorAccountInactive | ApiErrorInvalidBillingAddress):
    """

    error: ApiErrorAccountInactive | ApiErrorInvalidBillingAddress

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_account_inactive import ApiErrorAccountInactive

        error: dict[str, Any]
        error = self.error.to_dict() if isinstance(self.error, ApiErrorAccountInactive) else self.error.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_error_account_inactive import ApiErrorAccountInactive
        from ..models.api_error_invalid_billing_address import ApiErrorInvalidBillingAddress

        d = dict(src_dict)

        def _parse_error(data: object) -> ApiErrorAccountInactive | ApiErrorInvalidBillingAddress:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = ApiErrorAccountInactive.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_1 = ApiErrorInvalidBillingAddress.from_dict(data)

            return error_type_1

        error = _parse_error(d.pop("error"))

        launch_instance_response_403 = cls(
            error=error,
        )

        return launch_instance_response_403
