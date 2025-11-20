from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GeneratedSSHKey")


@_attrs_define
class GeneratedSSHKey:
    """Information about a server-generated SSH key, which can be used to access instances over
    SSH.

        Attributes:
            id (str): The unique identifier (ID) of the SSH key.
            name (str): The name of the SSH key.
            public_key (str): The public key for the SSH key.
            private_key (str): The private key generated in the SSH key pair. Make sure to store a
                copy of this key locally, as Lambda does not store the key server-side.
    """

    id: str
    name: str
    public_key: str
    private_key: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        public_key = self.public_key

        private_key = self.private_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "public_key": public_key,
                "private_key": private_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        public_key = d.pop("public_key")

        private_key = d.pop("private_key")

        generated_ssh_key = cls(
            id=id,
            name=name,
            public_key=public_key,
            private_key=private_key,
        )

        generated_ssh_key.additional_properties = d
        return generated_ssh_key

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
