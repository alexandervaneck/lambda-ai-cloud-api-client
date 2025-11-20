from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.ssh_key import SSHKey


T = TypeVar("T", bound="ListSSHKeysResponse200")


@_attrs_define
class ListSSHKeysResponse200:
    """
    Attributes:
        data (list[SSHKey]):
    """

    data: list[SSHKey]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ssh_key import SSHKey

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = SSHKey.from_dict(data_item_data)

            data.append(data_item)

        list_ssh_keys_response_200 = cls(
            data=data,
        )

        return list_ssh_keys_response_200
