"""
Small shared helpers used across services/routes.
"""
from typing import Any, Dict


def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a MongoDB document into a JSON-safe dict with `id` instead of `_id`."""
    if doc is None:
        return None
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


def serialize_list(docs) -> list:
    return [serialize_doc(doc) for doc in docs]
