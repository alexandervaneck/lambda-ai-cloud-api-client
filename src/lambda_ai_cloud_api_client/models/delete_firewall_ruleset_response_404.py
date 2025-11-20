from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_firewall_ruleset_not_found import ApiErrorFirewallRulesetNotFound


T = TypeVar("T", bound="DeleteFirewallRulesetResponse404")


@_attrs_define
class DeleteFirewallRulesetResponse404:
    """
    Attributes:
        error (ApiErrorFirewallRulesetNotFound):
    """

    error: ApiErrorFirewallRulesetNotFound

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
        from ..models.api_error_firewall_ruleset_not_found import ApiErrorFirewallRulesetNotFound

        d = dict(src_dict)
        error = ApiErrorFirewallRulesetNotFound.from_dict(d.pop("error"))

        delete_firewall_ruleset_response_404 = cls(
            error=error,
        )

        return delete_firewall_ruleset_response_404
