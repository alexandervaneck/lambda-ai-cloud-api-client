import json
from typing import Any


def _to_serializable(value: Any) -> Any:
    """Convert API models into JSON serializable structures."""
    if hasattr(value, "to_dict"):
        return _to_serializable(value.to_dict())
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_serializable(v) for v in value]
    return value


def print_response(response) -> None:
    """Pretty-print responses and exit non-zero on errors."""
    status = int(response.status_code)
    parsed = response.parsed
    if 200 <= status < 300:
        payload = _to_serializable(parsed) if parsed is not None else {"status": status}
        print(json.dumps(payload, indent=2))
        return

    payload = parsed if parsed is not None else response.content.decode("utf-8", errors="replace")
    print(json.dumps({"status_code": status, "error": _to_serializable(payload)}, indent=2))
