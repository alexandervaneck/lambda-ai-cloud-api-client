"""Contains some shared types for properties"""

from collections.abc import Mapping, MutableMapping
from http import HTTPStatus
from typing import IO, BinaryIO, Generic, Literal, TypeVar

from attrs import define

from lambda_ai_cloud_api_client.errors import HttpError


class Unset:
    def __bool__(self) -> Literal[False]:
        return False

    def __str__(self):
        return "-"

    def __repr__(self):
        return "-"

    def __rich__(self) -> str:
        return "-"


UNSET: Unset = Unset()

# The types that `httpx.Client(files=)` can accept, copied from that library.
FileContent = IO[bytes] | bytes | str
FileTypes = (
    # (filename, file (or bytes), content_type)
    tuple[str | None, FileContent, str | None]
    # (filename, file (or bytes), content_type, headers)
    | tuple[str | None, FileContent, str | None, Mapping[str, str]]
)
RequestFiles = list[tuple[str, FileTypes]]


@define
class File:
    """Contains information for file uploads"""

    payload: BinaryIO
    file_name: str | None = None
    mime_type: str | None = None

    def to_tuple(self) -> FileTypes:
        """Return a tuple representation that httpx will accept for multipart/form-data"""
        return self.file_name, self.payload, self.mime_type


T = TypeVar("T")


@define
class Response(Generic[T]):
    """A response from an endpoint"""

    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: T | None

    def raise_for_status(self):
        if self.status_code.is_client_error or self.status_code.is_server_error:
            raise HttpError(status_code=self.status_code, content=self.content.decode(errors="ignore"))


__all__ = ["UNSET", "File", "FileTypes", "RequestFiles", "Response", "Unset"]
