from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_invalid_parameters import ApiErrorInvalidParameters
    from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded


T = TypeVar("T", bound="CreateFirewallRulesetResponse400")


@_attrs_define
class CreateFirewallRulesetResponse400:
    """
    Attributes:
        error (ApiErrorInvalidParameters | ApiErrorQuotaExceeded):
    """

    error: ApiErrorInvalidParameters | ApiErrorQuotaExceeded

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded

        error: dict[str, Any]
        error = self.error.to_dict() if isinstance(self.error, ApiErrorQuotaExceeded) else self.error.to_dict()

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
        from ..models.api_error_quota_exceeded import ApiErrorQuotaExceeded

        d = dict(src_dict)

        def _parse_error(data: object) -> ApiErrorInvalidParameters | ApiErrorQuotaExceeded:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = ApiErrorQuotaExceeded.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            error_type_1 = ApiErrorInvalidParameters.from_dict(data)

            return error_type_1

        error = _parse_error(d.pop("error"))

        create_firewall_ruleset_response_400 = cls(
            error=error,
        )

        return create_firewall_ruleset_response_400
