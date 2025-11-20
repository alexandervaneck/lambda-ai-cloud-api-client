from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.instance_action_unavailable_code import InstanceActionUnavailableCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="InstanceActionAvailabilityDetails")


@_attrs_define
class InstanceActionAvailabilityDetails:
    """
    Attributes:
        available (bool): If set, indicates that the relevant operation can be performed on the instance in its current
            state.
        reason_code (InstanceActionUnavailableCode | str | Unset): A code representing the instance state that is
            blocking the operation. Only provided if the operation is blocked.
        reason_description (str | Unset): A longer description of why this operation is currently blocked. Only provided
            if the operation is blocked.
    """

    available: bool
    reason_code: InstanceActionUnavailableCode | str | Unset = UNSET
    reason_description: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        reason_code: str | Unset
        if isinstance(self.reason_code, Unset):
            reason_code = UNSET
        elif isinstance(self.reason_code, InstanceActionUnavailableCode):
            reason_code = self.reason_code.value
        else:
            reason_code = self.reason_code

        reason_description = self.reason_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
            }
        )
        if reason_code is not UNSET:
            field_dict["reason_code"] = reason_code
        if reason_description is not UNSET:
            field_dict["reason_description"] = reason_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        available = d.pop("available")

        def _parse_reason_code(data: object) -> InstanceActionUnavailableCode | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_code_type_0 = InstanceActionUnavailableCode(data)

                return reason_code_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(InstanceActionUnavailableCode | str | Unset, data)

        reason_code = _parse_reason_code(d.pop("reason_code", UNSET))

        reason_description = d.pop("reason_description", UNSET)

        instance_action_availability_details = cls(
            available=available,
            reason_code=reason_code,
            reason_description=reason_description,
        )

        instance_action_availability_details.additional_properties = d
        return instance_action_availability_details

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
