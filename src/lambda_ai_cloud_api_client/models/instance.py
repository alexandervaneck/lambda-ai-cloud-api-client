from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.instance_status import InstanceStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filesystem_mount_entry import FilesystemMountEntry
    from ..models.firewall_ruleset_entry import FirewallRulesetEntry
    from ..models.instance_action_availability import InstanceActionAvailability
    from ..models.instance_type import InstanceType
    from ..models.region import Region
    from ..models.tag_entry import TagEntry


T = TypeVar("T", bound="Instance")


@_attrs_define
class Instance:
    """Detailed information about the instance.

    Attributes:
        id (str): The unique identifier of the instance.
        status (InstanceStatus): The current status of the instance.
        ssh_key_names (list[str]): The names of the SSH keys that are allowed to access the instance.
        file_system_names (list[str]): The names of the filesystems mounted to the instance. If no filesystems are
            mounted, this array is empty.
        region (Region):
        instance_type (InstanceType):
        actions (InstanceActionAvailability):
        name (str | Unset): If set, the user-provided name of the instance.
        ip (str | Unset): The public IPv4 address of the instance.
        private_ip (str | Unset): The private IPv4 address of the instance.
        file_system_mounts (list[FilesystemMountEntry] | Unset): The filesystems, along with the mount paths, mounted to
            the instances. If no filesystems are mounted, this parameter
            will be missing from the response.
        hostname (str | Unset): The hostname assigned to this instance, which resolves to the instance's IP.
        jupyter_token (str | Unset): The secret token used to log into the JupyterLab server hosted on the instance.
        jupyter_url (str | Unset): The URL that opens the JupyterLab environment on the instance.
        tags (list[TagEntry] | Unset): Key/value pairs representing the instance's tags.
        firewall_rulesets (list[FirewallRulesetEntry] | Unset): The firewall rulesets associated with this instance.
    """

    id: str
    status: InstanceStatus
    ssh_key_names: list[str]
    file_system_names: list[str]
    region: Region
    instance_type: InstanceType
    actions: InstanceActionAvailability
    name: str | Unset = UNSET
    ip: str | Unset = UNSET
    private_ip: str | Unset = UNSET
    file_system_mounts: list[FilesystemMountEntry] | Unset = UNSET
    hostname: str | Unset = UNSET
    jupyter_token: str | Unset = UNSET
    jupyter_url: str | Unset = UNSET
    tags: list[TagEntry] | Unset = UNSET
    firewall_rulesets: list[FirewallRulesetEntry] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        status = self.status.value

        ssh_key_names = self.ssh_key_names

        file_system_names = self.file_system_names

        region = self.region.to_dict()

        instance_type = self.instance_type.to_dict()

        actions = self.actions.to_dict()

        name = self.name

        ip = self.ip

        private_ip = self.private_ip

        file_system_mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.file_system_mounts, Unset):
            file_system_mounts = []
            for file_system_mounts_item_data in self.file_system_mounts:
                file_system_mounts_item = file_system_mounts_item_data.to_dict()
                file_system_mounts.append(file_system_mounts_item)

        hostname = self.hostname

        jupyter_token = self.jupyter_token

        jupyter_url = self.jupyter_url

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
                "id": id,
                "status": status,
                "ssh_key_names": ssh_key_names,
                "file_system_names": file_system_names,
                "region": region,
                "instance_type": instance_type,
                "actions": actions,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if ip is not UNSET:
            field_dict["ip"] = ip
        if private_ip is not UNSET:
            field_dict["private_ip"] = private_ip
        if file_system_mounts is not UNSET:
            field_dict["file_system_mounts"] = file_system_mounts
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if jupyter_token is not UNSET:
            field_dict["jupyter_token"] = jupyter_token
        if jupyter_url is not UNSET:
            field_dict["jupyter_url"] = jupyter_url
        if tags is not UNSET:
            field_dict["tags"] = tags
        if firewall_rulesets is not UNSET:
            field_dict["firewall_rulesets"] = firewall_rulesets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filesystem_mount_entry import FilesystemMountEntry
        from ..models.firewall_ruleset_entry import FirewallRulesetEntry
        from ..models.instance_action_availability import InstanceActionAvailability
        from ..models.instance_type import InstanceType
        from ..models.region import Region
        from ..models.tag_entry import TagEntry

        d = dict(src_dict)
        id = d.pop("id")

        status = InstanceStatus(d.pop("status"))

        ssh_key_names = cast(list[str], d.pop("ssh_key_names"))

        file_system_names = cast(list[str], d.pop("file_system_names"))

        region = Region.from_dict(d.pop("region"))

        instance_type = InstanceType.from_dict(d.pop("instance_type"))

        actions = InstanceActionAvailability.from_dict(d.pop("actions"))

        name = d.pop("name", UNSET)

        ip = d.pop("ip", UNSET)

        private_ip = d.pop("private_ip", UNSET)

        _file_system_mounts = d.pop("file_system_mounts", UNSET)
        file_system_mounts: list[FilesystemMountEntry] | Unset = UNSET
        if _file_system_mounts is not UNSET:
            file_system_mounts = []
            for file_system_mounts_item_data in _file_system_mounts:
                file_system_mounts_item = FilesystemMountEntry.from_dict(file_system_mounts_item_data)

                file_system_mounts.append(file_system_mounts_item)

        hostname = d.pop("hostname", UNSET)

        jupyter_token = d.pop("jupyter_token", UNSET)

        jupyter_url = d.pop("jupyter_url", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: list[TagEntry] | Unset = UNSET
        if _tags is not UNSET:
            tags = []
            for tags_item_data in _tags:
                tags_item = TagEntry.from_dict(tags_item_data)

                tags.append(tags_item)

        _firewall_rulesets = d.pop("firewall_rulesets", UNSET)
        firewall_rulesets: list[FirewallRulesetEntry] | Unset = UNSET
        if _firewall_rulesets is not UNSET:
            firewall_rulesets = []
            for firewall_rulesets_item_data in _firewall_rulesets:
                firewall_rulesets_item = FirewallRulesetEntry.from_dict(firewall_rulesets_item_data)

                firewall_rulesets.append(firewall_rulesets_item)

        instance = cls(
            id=id,
            status=status,
            ssh_key_names=ssh_key_names,
            file_system_names=file_system_names,
            region=region,
            instance_type=instance_type,
            actions=actions,
            name=name,
            ip=ip,
            private_ip=private_ip,
            file_system_mounts=file_system_mounts,
            hostname=hostname,
            jupyter_token=jupyter_token,
            jupyter_url=jupyter_url,
            tags=tags,
            firewall_rulesets=firewall_rulesets,
        )

        instance.additional_properties = d
        return instance

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
