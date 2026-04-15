# src/folder_router.py

ROUTING_RULES = {
    "Finance":    "/Enterprise/Finance/Invoices",
    "Legal":      "/Enterprise/Legal/Contracts",
    "Operations": "/Enterprise/Operations/Reports",
    "HR":         "/Enterprise/HR/Forms",
    "Unknown":    "/Enterprise/Unclassified",
}

class FolderRouter:
    def route(self, document) -> str:
        from content_model import DOCUMENT_TYPES
        doc_info = DOCUMENT_TYPES.get(document.doc_type, {})
        category = doc_info.get("category", "Unknown")
        path = ROUTING_RULES.get(category, ROUTING_RULES["Unknown"])
        document.folder_path = path
        return path