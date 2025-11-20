from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApiErrorAccountInactive")


@_attrs_define
class ApiErrorAccountInactive:
    """
    Attributes:
        code (Literal['global/account-inactive']): The unique identifier for the type of error.
        message (str): A description of the error. Default: 'Your account is inactive.'.
        suggestion (str): One or more suggestions of possible ways to fix the error. Default: 'Make sure you have
            verified your email address and have a valid payment method. Contact Support if problems continue.'.
    """

    code: Literal["global/account-inactive"]
    message: str = "Your account is inactive."
    suggestion: str = "Make sure you have verified your email address and have a valid payment method. Contact Support if problems continue."
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        suggestion = self.suggestion

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "suggestion": suggestion,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = cast(Literal["global/account-inactive"], d.pop("code"))
        if code != "global/account-inactive":
            raise ValueError(f"code must match const 'global/account-inactive', got '{code}'")

        message = d.pop("message")

        suggestion = d.pop("suggestion")

        api_error_account_inactive = cls(
            code=code,
            message=message,
            suggestion=suggestion,
        )

        api_error_account_inactive.additional_properties = d
        return api_error_account_inactive

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
