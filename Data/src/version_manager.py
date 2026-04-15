# src/version_manager.py
import copy

class VersionManager:
    def __init__(self):
        self.history: dict[str, list] = {}   # doc_id -> list of versions

    def save_version(self, document):
        doc_id = document.doc_id
        if doc_id not in self.history:
            self.history[doc_id] = []
        snapshot = copy.deepcopy(document)
        self.history[doc_id].append(snapshot)

    def new_version(self, document, updated_metadata: dict):
        self.save_version(document)           # archive current
        document.metadata.update(updated_metadata)
        document.version += 1
        return document

    def get_history(self, doc_id: str) -> list:
        return self.history.get(doc_id, [])