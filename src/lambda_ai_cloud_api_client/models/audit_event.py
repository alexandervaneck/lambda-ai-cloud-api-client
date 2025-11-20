from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.audit_event_additional_details import AuditEventAdditionalDetails


T = TypeVar("T", bound="AuditEvent")


@_attrs_define
class AuditEvent:
    """Audit event in the account's audit log. To view the full catalog of
    possible audit events, visit
    [Access and security > Audit logs](https://docs.lambda.ai/public-cloud/access-security#audit-logs)
    in the Lambda Cloud documentation.

        Attributes:
            service_name (str): The service in which the action was performed.
            resource_name (str): The type of resource that was affected.
            action (str): The action that was performed.
            catalog_version (str): The version of the event catalog schema.
            event_id (str): The unique identifier (ID) for this audit event.
            event_time (str): The UTC timestamp for when the event occurred (ISO 8601 format).
            actor_lrn (None | str): The Lambda Resource Name (LRN) of the actor who performed the action.
            resource_lrns (list[str]): The Lambda Resource Names (LRNs) of the resources affected by this action.
            resource_owner_lrn (None | str): The Lambda Resource Name (LRN) of the account that owns the affected resources.
            request_api_key_lrn (None | str): The Lambda Resource Name (LRN) of the API key used to authenticate the
                request, if applicable.
            additional_details (AuditEventAdditionalDetails): Additional event-specific details. The exact keys returned
                vary by event type.
    """

    service_name: str
    resource_name: str
    action: str
    catalog_version: str
    event_id: str
    event_time: str
    actor_lrn: None | str
    resource_lrns: list[str]
    resource_owner_lrn: None | str
    request_api_key_lrn: None | str
    additional_details: AuditEventAdditionalDetails
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_name = self.service_name

        resource_name = self.resource_name

        action = self.action

        catalog_version = self.catalog_version

        event_id = self.event_id

        event_time = self.event_time

        actor_lrn: None | str
        actor_lrn = self.actor_lrn

        resource_lrns = self.resource_lrns

        resource_owner_lrn: None | str
        resource_owner_lrn = self.resource_owner_lrn

        request_api_key_lrn: None | str
        request_api_key_lrn = self.request_api_key_lrn

        additional_details = self.additional_details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_name": service_name,
                "resource_name": resource_name,
                "action": action,
                "catalog_version": catalog_version,
                "event_id": event_id,
                "event_time": event_time,
                "actor_lrn": actor_lrn,
                "resource_lrns": resource_lrns,
                "resource_owner_lrn": resource_owner_lrn,
                "request_api_key_lrn": request_api_key_lrn,
                "additional_details": additional_details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.audit_event_additional_details import AuditEventAdditionalDetails

        d = dict(src_dict)
        service_name = d.pop("service_name")

        resource_name = d.pop("resource_name")

        action = d.pop("action")

        catalog_version = d.pop("catalog_version")

        event_id = d.pop("event_id")

        event_time = d.pop("event_time")

        def _parse_actor_lrn(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_lrn = _parse_actor_lrn(d.pop("actor_lrn"))

        resource_lrns = cast(list[str], d.pop("resource_lrns"))

        def _parse_resource_owner_lrn(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        resource_owner_lrn = _parse_resource_owner_lrn(d.pop("resource_owner_lrn"))

        def _parse_request_api_key_lrn(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        request_api_key_lrn = _parse_request_api_key_lrn(d.pop("request_api_key_lrn"))

        additional_details = AuditEventAdditionalDetails.from_dict(d.pop("additional_details"))

        audit_event = cls(
            service_name=service_name,
            resource_name=resource_name,
            action=action,
            catalog_version=catalog_version,
            event_id=event_id,
            event_time=event_time,
            actor_lrn=actor_lrn,
            resource_lrns=resource_lrns,
            resource_owner_lrn=resource_owner_lrn,
            request_api_key_lrn=request_api_key_lrn,
            additional_details=additional_details,
        )

        audit_event.additional_properties = d
        return audit_event

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
