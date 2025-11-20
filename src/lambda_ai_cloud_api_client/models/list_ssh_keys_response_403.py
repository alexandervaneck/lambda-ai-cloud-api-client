from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.api_error_account_inactive import ApiErrorAccountInactive


T = TypeVar("T", bound="ListSSHKeysResponse403")


@_attrs_define
class ListSSHKeysResponse403:
    """
    Attributes:
        error (ApiErrorAccountInactive):
    """

    error: ApiErrorAccountInactive

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
        from ..models.api_error_account_inactive import ApiErrorAccountInactive

        d = dict(src_dict)
        error = ApiErrorAccountInactive.from_dict(d.pop("error"))

        list_ssh_keys_response_403 = cls(
            error=error,
        )

        return list_ssh_keys_response_403
