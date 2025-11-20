from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.audit_events_page import AuditEventsPage


T = TypeVar("T", bound="GetAuditEventsResponse200")


@_attrs_define
class GetAuditEventsResponse200:
    """
    Attributes:
        data (AuditEventsPage): A paginated response containing audit events.
    """

    data: AuditEventsPage

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_events_page import AuditEventsPage

        d = dict(src_dict)
        data = AuditEventsPage.from_dict(d.pop("data"))

        get_audit_events_response_200 = cls(
            data=data,
        )

        return get_audit_events_response_200
