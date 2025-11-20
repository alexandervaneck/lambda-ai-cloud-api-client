from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_unauthorized import ApiErrorUnauthorized


T = TypeVar("T", bound="UpdateGlobalFirewallRulesetResponse401")


@_attrs_define
class UpdateGlobalFirewallRulesetResponse401:
    """
    Attributes:
        error (ApiErrorUnauthorized):
    """

    error: ApiErrorUnauthorized

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
        from ..models.api_error_unauthorized import ApiErrorUnauthorized

        d = dict(src_dict)
        error = ApiErrorUnauthorized.from_dict(d.pop("error"))

        update_global_firewall_ruleset_response_401 = cls(
            error=error,
        )

        return update_global_firewall_ruleset_response_401
