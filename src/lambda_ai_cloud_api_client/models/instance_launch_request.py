from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_region_code import PublicRegionCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.firewall_ruleset_entry import FirewallRulesetEntry
    from ..models.image_specification_family import ImageSpecificationFamily
    from ..models.image_specification_id import ImageSpecificationID
    from ..models.requested_filesystem_mount_entry import RequestedFilesystemMountEntry
    from ..models.requested_tag_entry import RequestedTagEntry


T = TypeVar("T", bound="InstanceLaunchRequest")


@_attrs_define
class InstanceLaunchRequest:
    """
    Attributes:
        region_name (PublicRegionCode):
        instance_type_name (str): The type of instance you want to launch. To retrieve a list of available instance
            types, see
            [List available instance types](#listInstanceTypes).
        ssh_key_names (list[str]): The names of the SSH keys you want to use to provide access to the instance.
            Currently, exactly one SSH key must be specified.
        file_system_names (list[str] | Unset): The names of the filesystems you want to mount to the instance. When
            specified
            alongside `file_system_mounts`, any filesystems referred to in both lists will use the
            mount path specified in `file_system_mounts`, rather than the default.
        file_system_mounts (list[RequestedFilesystemMountEntry] | Unset): The filesystem mounts to mount to the
            instance. When specified alongside
            `file_system_names`, any filesystems referred to in both lists will use the
            mount path specified in `file_system_mounts`, rather than the default.
        hostname (str | Unset): The hostname to assign to the instance. If not specified, a default, IP-address-based
            hostname is assigned. This hostname is driven into /etc/hostname on the instance.
        name (str | Unset): The name you want to assign to your instance. Must be 64 characters or fewer.
        image (ImageSpecificationFamily | ImageSpecificationID | Unset): The machine image you want to use. Defaults to
            the latest Lambda Stack image.
        user_data (str | Unset): An instance configuration string specified in a valid
            [cloud-init user-data](https://cloudinit.readthedocs.io/en/latest/explanation/format.html)
            format. You can use this field to configure your instance on launch. The
            user data string must be plain text and cannot exceed 1MB in size.
        tags (list[RequestedTagEntry] | Unset): Key/value pairs representing the instance's tags.
        firewall_rulesets (list[FirewallRulesetEntry] | Unset): The firewall rulesets to associate with the instance.
            The firewall rulesets must exist in the same region as the instance.
    """

    region_name: PublicRegionCode
    instance_type_name: str
    ssh_key_names: list[str]
    file_system_names: list[str] | Unset = UNSET
    file_system_mounts: list[RequestedFilesystemMountEntry] | Unset = UNSET
    hostname: str | Unset = UNSET
    name: str | Unset = UNSET
    image: ImageSpecificationFamily | ImageSpecificationID | Unset = UNSET
    user_data: str | Unset = UNSET
    tags: list[RequestedTagEntry] | Unset = UNSET
    firewall_rulesets: list[FirewallRulesetEntry] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.image_specification_id import ImageSpecificationID

        region_name = self.region_name.value

        instance_type_name = self.instance_type_name

        ssh_key_names = self.ssh_key_names

        file_system_names: list[str] | Unset = UNSET
        if not isinstance(self.file_system_names, Unset):
            file_system_names = self.file_system_names

        file_system_mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.file_system_mounts, Unset):
            file_system_mounts = []
            for file_system_mounts_item_data in self.file_system_mounts:
                file_system_mounts_item = file_system_mounts_item_data.to_dict()
                file_system_mounts.append(file_system_mounts_item)

        hostname = self.hostname

        name = self.name

        image: dict[str, Any] | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, ImageSpecificationID):
            image = self.image.to_dict()
        else:
            image = self.image.to_dict()

        user_data = self.user_data

        tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        firewall_rulesets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.firewall_rulesets, Unset):
            firewall_rulesets = []
            for firewall_rulesets_item_data in self.firewall_rulesets:
                firewall_rulesets_item = firewall_rulesets_item_data.to_dict()
                firewall_rulesets.append(firewall_rulesets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "region_name": region_name,
                "instance_type_name": instance_type_name,
                "ssh_key_names": ssh_key_names,
            }
        )
        if file_system_names is not UNSET:
            field_dict["file_system_names"] = file_system_names
        if file_system_mounts is not UNSET:
            field_dict["file_system_mounts"] = file_system_mounts
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if name is not UNSET:
            field_dict["name"] = name
        if image is not UNSET:
            field_dict["image"] = image
        if user_data is not UNSET:
            field_dict["user_data"] = user_data
        if tags is not UNSET:
            field_dict["tags"] = tags
        if firewall_rulesets is not UNSET:
            field_dict["firewall_rulesets"] = firewall_rulesets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.firewall_ruleset_entry import FirewallRulesetEntry
        from ..models.image_specification_family import ImageSpecificationFamily
        from ..models.image_specification_id import ImageSpecificationID
        from ..models.requested_filesystem_mount_entry import RequestedFilesystemMountEntry
        from ..models.requested_tag_entry import RequestedTagEntry

        d = dict(src_dict)
        region_name = PublicRegionCode(d.pop("region_name"))

        instance_type_name = d.pop("instance_type_name")

        ssh_key_names = cast(list[str], d.pop("ssh_key_names"))

        file_system_names = cast(list[str], d.pop("file_system_names", UNSET))

        _file_system_mounts = d.pop("file_system_mounts", UNSET)
        file_system_mounts: list[RequestedFilesystemMountEntry] | Unset = UNSET
        if _file_system_mounts is not UNSET:
            file_system_mounts = []
            for file_system_mounts_item_data in _file_system_mounts:
                file_system_mounts_item = RequestedFilesystemMountEntry.from_dict(file_system_mounts_item_data)

                file_system_mounts.append(file_system_mounts_item)

        hostname = d.pop("hostname", UNSET)

        name = d.pop("name", UNSET)

        def _parse_image(data: object) -> ImageSpecificationFamily | ImageSpecificationID | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                image_type_0 = ImageSpecificationID.from_dict(data)

                return image_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            image_type_1 = ImageSpecificationFamily.from_dict(data)

            return image_type_1

        image = _parse_image(d.pop("image", UNSET))

        user_data = d.pop("user_data", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: list[RequestedTagEntry] | Unset = UNSET
        if _tags is not UNSET:
            tags = []
            for tags_item_data in _tags:
                tags_item = RequestedTagEntry.from_dict(tags_item_data)

                tags.append(tags_item)

        _firewall_rulesets = d.pop("firewall_rulesets", UNSET)
        firewall_rulesets: list[FirewallRulesetEntry] | Unset = UNSET
        if _firewall_rulesets is not UNSET:
            firewall_rulesets = []
            for firewall_rulesets_item_data in _firewall_rulesets:
                firewall_rulesets_item = FirewallRulesetEntry.from_dict(firewall_rulesets_item_data)

                firewall_rulesets.append(firewall_rulesets_item)

        instance_launch_request = cls(
            region_name=region_name,
            instance_type_name=instance_type_name,
            ssh_key_names=ssh_key_names,
            file_system_names=file_system_names,
            file_system_mounts=file_system_mounts,
            hostname=hostname,
            name=name,
            image=image,
            user_data=user_data,
            tags=tags,
            firewall_rulesets=firewall_rulesets,
        )

        instance_launch_request.additional_properties = d
        return instance_launch_request

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
