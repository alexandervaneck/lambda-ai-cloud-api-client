from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.generated_ssh_key import GeneratedSSHKey
    from ..models.ssh_key import SSHKey


T = TypeVar("T", bound="AddSSHKeyResponse200")


@_attrs_define
class AddSSHKeyResponse200:
    """
    Attributes:
        data (GeneratedSSHKey | SSHKey):
    """

    data: GeneratedSSHKey | SSHKey

    def to_dict(self) -> dict[str, Any]:
        from ..models.generated_ssh_key import GeneratedSSHKey

        data: dict[str, Any]
        data = self.data.to_dict() if isinstance(self.data, GeneratedSSHKey) else self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.generated_ssh_key import GeneratedSSHKey
        from ..models.ssh_key import SSHKey

        d = dict(src_dict)

        def _parse_data(data: object) -> GeneratedSSHKey | SSHKey:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = GeneratedSSHKey.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_1 = SSHKey.from_dict(data)

            return data_type_1

        data = _parse_data(d.pop("data"))

        add_ssh_key_response_200 = cls(
            data=data,
        )

        return add_ssh_key_response_200
