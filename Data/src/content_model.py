# src/content_model.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

DOCUMENT_TYPES = {
    "Invoice":    {"required_fields": ["vendor", "amount", "date"], "category": "Finance"},
    "Contract":   {"required_fields": ["party_a", "party_b", "expiry"], "category": "Legal"},
    "Report":     {"required_fields": ["author", "department"], "category": "Operations"},
    "HR_Form":    {"required_fields": ["employee_id", "form_type"], "category": "HR"},
}

@dataclass
class Document:
    name: str
    doc_type: str
    metadata: dict
    content: bytes = b""
    doc_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    status: str = "Pending"          # Pending | Active | Archived
    folder_path: str = ""

    def validate(self) -> tuple[bool, list]:
        """Check all required metadata fields are present."""
        required = DOCUMENT_TYPES.get(self.doc_type, {}).get("required_fields", [])
        missing = [f for f in required if f not in self.metadata]
        return (len(missing) == 0), missing