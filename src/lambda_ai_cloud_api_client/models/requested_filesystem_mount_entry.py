from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RequestedFilesystemMountEntry")


@_attrs_define
class RequestedFilesystemMountEntry:
    """The mount point for a filesystem mounted to an instance.

    Attributes:
        mount_point (str): The absolute path indicating where on the instance the filesystem will be mounted.
        file_system_id (str): The id of the filesystem to mount to the instance.
    """

    mount_point: str
    file_system_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mount_point = self.mount_point

        file_system_id = self.file_system_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mount_point": mount_point,
                "file_system_id": file_system_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mount_point = d.pop("mount_point")

        file_system_id = d.pop("file_system_id")

        requested_filesystem_mount_entry = cls(
            mount_point=mount_point,
            file_system_id=file_system_id,
        )

        requested_filesystem_mount_entry.additional_properties = d
        return requested_filesystem_mount_entry

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
