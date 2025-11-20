from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.region import Region
    from ..models.user import User


T = TypeVar("T", bound="Filesystem")


@_attrs_define
class Filesystem:
    """Information about a shared filesystem.

    Attributes:
        id (str): The unique identifier (ID) of the filesystem.
        name (str): The name of the filesystem.
        mount_point (str): The DEFAULT absolute path indicating where on instances the filesystem will be mounted.
            If `file_system_mounts` were used at launch time, the actual mount point is in the
            instance response.
        created (datetime.datetime): The date and time at which the filesystem was created. Formatted as an ISO 8601
            timestamp.
        created_by (User): Information about a user in your Team.
        is_in_use (bool): Whether the filesystem is currently mounted to an instance. Filesystems that
            are mounted cannot be deleted.
        region (Region):
        bytes_used (int | Unset): The approximate amount of storage used by the filesystem in bytes. This estimate is
            updated every few hours.
    """

    id: str
    name: str
    mount_point: str
    created: datetime.datetime
    created_by: User
    is_in_use: bool
    region: Region
    bytes_used: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        mount_point = self.mount_point

        created = self.created.isoformat()

        created_by = self.created_by.to_dict()

        is_in_use = self.is_in_use

        region = self.region.to_dict()

        bytes_used = self.bytes_used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "mount_point": mount_point,
                "created": created,
                "created_by": created_by,
                "is_in_use": is_in_use,
                "region": region,
            }
        )
        if bytes_used is not UNSET:
            field_dict["bytes_used"] = bytes_used

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.region import Region
        from ..models.user import User

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        mount_point = d.pop("mount_point")

        created = isoparse(d.pop("created"))

        created_by = User.from_dict(d.pop("created_by"))

        is_in_use = d.pop("is_in_use")

        region = Region.from_dict(d.pop("region"))

        bytes_used = d.pop("bytes_used", UNSET)

        filesystem = cls(
            id=id,
            name=name,
            mount_point=mount_point,
            created=created,
            created_by=created_by,
            is_in_use=is_in_use,
            region=region,
            bytes_used=bytes_used,
        )

        filesystem.additional_properties = d
        return filesystem

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
