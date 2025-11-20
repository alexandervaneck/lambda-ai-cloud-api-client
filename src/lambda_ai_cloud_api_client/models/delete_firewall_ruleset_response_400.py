from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_firewall_ruleset_in_use import ApiErrorFirewallRulesetInUse


T = TypeVar("T", bound="DeleteFirewallRulesetResponse400")


@_attrs_define
class DeleteFirewallRulesetResponse400:
    """
    Attributes:
        error (ApiErrorFirewallRulesetInUse):
    """

    error: ApiErrorFirewallRulesetInUse

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
        from ..models.api_error_firewall_ruleset_in_use import ApiErrorFirewallRulesetInUse

        d = dict(src_dict)
        error = ApiErrorFirewallRulesetInUse.from_dict(d.pop("error"))

        delete_firewall_ruleset_response_400 = cls(
            error=error,
        )

        return delete_firewall_ruleset_response_400
