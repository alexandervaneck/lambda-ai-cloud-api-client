from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiErrorFileSystemInWrongRegion")


@_attrs_define
class ApiErrorFileSystemInWrongRegion:
    """
    Attributes:
        code (Literal['instance-operations/launch/file-system-in-wrong-region']): The unique identifier for the type of
            error.
        message (str): A description of the error.
        suggestion (str | Unset): One or more suggestions of possible ways to fix the error.
    """

    code: Literal["instance-operations/launch/file-system-in-wrong-region"]
    message: str
    suggestion: str | Unset = UNSET
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
            }
        )
        if suggestion is not UNSET:
            field_dict["suggestion"] = suggestion

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = cast(Literal["instance-operations/launch/file-system-in-wrong-region"], d.pop("code"))
        if code != "instance-operations/launch/file-system-in-wrong-region":
            raise ValueError(
                f"code must match const 'instance-operations/launch/file-system-in-wrong-region', got '{code}'"
            )

        message = d.pop("message")

        suggestion = d.pop("suggestion", UNSET)

        api_error_file_system_in_wrong_region = cls(
            code=code,
            message=message,
            suggestion=suggestion,
        )

        api_error_file_system_in_wrong_region.additional_properties = d
        return api_error_file_system_in_wrong_region

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
