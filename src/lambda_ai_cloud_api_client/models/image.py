from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.image_architecture import ImageArchitecture

if TYPE_CHECKING:
    from ..models.region import Region


T = TypeVar("T", bound="Image")


@_attrs_define
class Image:
    """An available machine image in Lambda Cloud.

    Attributes:
        id (str): The unique identifier (ID) for an image.
        created_time (datetime.datetime): The date and time that the image was created.
        updated_time (datetime.datetime): The date and time that the image was last updated.
        name (str): The human-readable identifier for an image.
        description (str): Additional information about the image.
        family (str): The family the image belongs to.
        version (str): The image version.
        architecture (ImageArchitecture):
        region (Region):
    """

    id: str
    created_time: datetime.datetime
    updated_time: datetime.datetime
    name: str
    description: str
    family: str
    version: str
    architecture: ImageArchitecture
    region: Region
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        created_time = self.created_time.isoformat()

        updated_time = self.updated_time.isoformat()

        name = self.name

        description = self.description

        family = self.family

        version = self.version

        architecture = self.architecture.value

        region = self.region.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_time": created_time,
                "updated_time": updated_time,
                "name": name,
                "description": description,
                "family": family,
                "version": version,
                "architecture": architecture,
                "region": region,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.region import Region

        d = dict(src_dict)
        id = d.pop("id")

        created_time = isoparse(d.pop("created_time"))

        updated_time = isoparse(d.pop("updated_time"))

        name = d.pop("name")

        description = d.pop("description")

        family = d.pop("family")

        version = d.pop("version")

        architecture = ImageArchitecture(d.pop("architecture"))

        region = Region.from_dict(d.pop("region"))

        image = cls(
            id=id,
            created_time=created_time,
            updated_time=updated_time,
            name=name,
            description=description,
            family=family,
            version=version,
            architecture=architecture,
            region=region,
        )

        image.additional_properties = d
        return image

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
