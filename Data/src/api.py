# src/api.py
import flask # type: ignore
from content_model import Document
from folder_router import FolderRouter
from version_manager import VersionManager
from audit_logger import AuditLogger

app = flask.Flask(__name__)
router = FolderRouter()
version_mgr = VersionManager()
logger = AuditLogger()
documents: dict[str, Document] = {}

@app.route("/documents", methods=["POST"])
def upload_document():
    data = flask.request.json
    doc = Document(
        name=data["name"],
        doc_type=data["doc_type"],
        metadata=data.get("metadata", {}),
    )
    valid, missing = doc.validate()
    if not valid:
        logger.log_error("UPLOAD", doc.doc_id, f"Missing fields: {missing}")
        return flask.jsonify({"error": "Validation failed", "missing_fields": missing}), 400

    folder = router.route(doc)
    documents[doc.doc_id] = doc
    logger.log("UPLOAD", doc.doc_id, data.get("user", "system"), f"Routed to {folder}")
    return flask.jsonify({"doc_id": doc.doc_id, "folder": folder, "version": doc.version}), 201

@app.route("/documents/<doc_id>", methods=["GET"])
def get_document(doc_id):
    doc = documents.get(doc_id)
    if not doc:
        return flask.jsonify({"error": "Not found"}), 404
    return flask.jsonify({"name": doc.name, "type": doc.doc_type,
                    "folder": doc.folder_path, "version": doc.version,
                    "metadata": doc.metadata, "status": doc.status})

@app.route("/documents/<doc_id>/version", methods=["PUT"])
def update_version(doc_id):
    doc = documents.get(doc_id)
    if not doc:
        return flask.jsonify({"error": "Not found"}), 404
    updated = version_mgr.new_version(doc, flask.request.json.get("metadata", {}))
    logger.log("VERSION_UPDATE", doc_id, flask.request.json.get("user", "system"),
               f"Now at v{updated.version}")
    return flask.jsonify({"doc_id": doc_id, "new_version": updated.version})

if __name__ == "__main__":
    app.run(debug=True)