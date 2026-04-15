# src/audit_logger.py
import logging
from datetime import datetime

logging.basicConfig(
    filename="audit.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

class AuditLogger:
    def log(self, action: str, doc_id: str, user: str, detail: str = ""):
        entry = f"ACTION={action} | DOC={doc_id} | USER={user} | {detail}"
        logging.info(entry)
        print(f"[AUDIT] {entry}")

    def log_error(self, action: str, doc_id: str, error: str):
        entry = f"ACTION={action} | DOC={doc_id} | ERROR={error}"
        logging.error(entry)
        print(f"[ERROR] {entry}")