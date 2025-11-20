from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ApiErrorQuotaExceeded")


@_attrs_define
class ApiErrorQuotaExceeded:
    """
    Attributes:
        code (Literal['global/quota-exceeded']): The unique identifier for the type of error.
        message (str): A description of the error. Default: 'Quota exceeded.'.
        suggestion (str): One or more suggestions of possible ways to fix the error. Default: 'Contact Support to
            increase your quota.'.
    """

    code: Literal["global/quota-exceeded"]
    message: str = "Quota exceeded."
    suggestion: str = "Contact Support to increase your quota."
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
        code = cast(Literal["global/quota-exceeded"], d.pop("code"))
        if code != "global/quota-exceeded":
            raise ValueError(f"code must match const 'global/quota-exceeded', got '{code}'")

        message = d.pop("message")

        suggestion = d.pop("suggestion")

        api_error_quota_exceeded = cls(
            code=code,
            message=message,
            suggestion=suggestion,
        )

        api_error_quota_exceeded.additional_properties = d
        return api_error_quota_exceeded

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
