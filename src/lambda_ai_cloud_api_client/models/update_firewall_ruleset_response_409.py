from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_internal import ApiErrorInternal


T = TypeVar("T", bound="UpdateFirewallRulesetResponse409")


@_attrs_define
class UpdateFirewallRulesetResponse409:
    """
    Attributes:
        error (ApiErrorInternal):
    """

    error: ApiErrorInternal

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
        from ..models.api_error_internal import ApiErrorInternal

        d = dict(src_dict)
        error = ApiErrorInternal.from_dict(d.pop("error"))

        update_firewall_ruleset_response_409 = cls(
            error=error,
        )

        return update_firewall_ruleset_response_409
