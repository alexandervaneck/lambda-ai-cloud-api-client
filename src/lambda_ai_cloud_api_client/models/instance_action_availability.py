from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_action_availability_details import InstanceActionAvailabilityDetails


T = TypeVar("T", bound="InstanceActionAvailability")


@_attrs_define
class InstanceActionAvailability:
    """
    Attributes:
        migrate (InstanceActionAvailabilityDetails):
        rebuild (InstanceActionAvailabilityDetails):
        restart (InstanceActionAvailabilityDetails):
        cold_reboot (InstanceActionAvailabilityDetails):
        terminate (InstanceActionAvailabilityDetails):
    """

    migrate: InstanceActionAvailabilityDetails
    rebuild: InstanceActionAvailabilityDetails
    restart: InstanceActionAvailabilityDetails
    cold_reboot: InstanceActionAvailabilityDetails
    terminate: InstanceActionAvailabilityDetails
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        migrate = self.migrate.to_dict()

        rebuild = self.rebuild.to_dict()

        restart = self.restart.to_dict()

        cold_reboot = self.cold_reboot.to_dict()

        terminate = self.terminate.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "migrate": migrate,
                "rebuild": rebuild,
                "restart": restart,
                "cold_reboot": cold_reboot,
                "terminate": terminate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_action_availability_details import InstanceActionAvailabilityDetails

        d = dict(src_dict)
        migrate = InstanceActionAvailabilityDetails.from_dict(d.pop("migrate"))

        rebuild = InstanceActionAvailabilityDetails.from_dict(d.pop("rebuild"))

        restart = InstanceActionAvailabilityDetails.from_dict(d.pop("restart"))

        cold_reboot = InstanceActionAvailabilityDetails.from_dict(d.pop("cold_reboot"))

        terminate = InstanceActionAvailabilityDetails.from_dict(d.pop("terminate"))

        instance_action_availability = cls(
            migrate=migrate,
            rebuild=rebuild,
            restart=restart,
            cold_reboot=cold_reboot,
            terminate=terminate,
        )

        instance_action_availability.additional_properties = d
        return instance_action_availability

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
