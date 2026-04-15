# OpenText Document Workflow System

A Python-based simulation of an **OpenText Content Server (OTCS)** document management workflow, built to demonstrate Application Analyst competencies in enterprise content management, document classification, metadata validation, folder routing, versioning, and audit logging.

> This project was built to mirror the real-world responsibilities of an Application Support/Analyst role supporting OpenText — including incident triage, validation failures, routing errors, version conflicts, and audit trail investigation.

---

## Table of Contents

- [Project Overview](#project-overview)
- [What This Simulates](#what-this-simulates)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run Locally](#how-to-run-locally)
- [API Reference](#api-reference)
- [Running the Tests](#running-the-tests)
- [Troubleshooting Use Cases](#troubleshooting-use-cases)
- [Audit Log Example](#audit-log-example)
- [Key Concepts Demonstrated](#key-concepts-demonstrated)
- [Author](#author)

---

## Project Overview

OpenText Content Server is an enterprise content management (ECM) platform widely used in regulated industries such as financial services, healthcare, and government. It manages the full lifecycle of documents — from upload and classification through to versioning, access control, and archiving.

This project simulates the core document workflow layer using a REST API built in Python and Flask. It replicates the concepts an Application Analyst would work with daily when supporting an OpenText environment — including content templates, folder routing rules, metadata validation, versioning, and audit trails.

---

## What This Simulates

| OpenText Concept | Simulated In This Project |
|---|---|
| Content templates with mandatory fields | `Document` dataclass with required metadata per type |
| Document classification and workspace routing | `FolderRouter` — routes by document type to folder path |
| Major/minor versioning | `VersionManager` — tracks version history with snapshots |
| Audit trail | `AuditLogger` — timestamped log of every create, update, and error |
| REST API (OTCS REST v2) | Flask API with POST, GET, PUT endpoints |
| Metadata validation errors | Returns missing fields with HTTP 400 |
| Unclassified document handling | Falls back to `/Enterprise/Unclassified` for unknown types |

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core language |
| Flask | 3.0.3 | REST API layer |
| PyYAML | 6.0.1 | Configuration loading |
| pytest | 8.2.0 | Unit testing |
| pytest-cov | latest | Test coverage reporting |

---

## Project Structure

```
opentext-document-workflow/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── settings.yaml               # App configuration
├── data/
│   └── sample_documents/
│       ├── invoice_001.pdf         # Sample test files
│       └── contract_abc.docx
├── src/
│   ├── __init__.py
│   ├── content_model.py            # Document types, metadata schema, validation
│   ├── folder_router.py            # Routing rules by document category
│   ├── version_manager.py          # Version history and snapshot management
│   ├── audit_logger.py             # Timestamped audit trail logging
│   └── api.py                      # Flask REST endpoints
├── tests/
│   └── test_workflow.py            # Full pytest test suite
└── docs/
    └── troubleshooting-use-cases.md
```

---

## How to Run Locally

### Prerequisites

- Python 3.11 or higher
- Git
- A terminal (VS Code terminal, Command Prompt, or bash)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/opentext-document-workflow.git
cd opentext-document-workflow
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Flask API

```bash
python src/api.py
```

You should see:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

The API is now running locally. Open a second terminal to make requests.

---

## API Reference

### POST `/documents` — Upload a document

Validates metadata, routes to the correct folder, and logs the action.

**Request:**

```bash
curl -X POST http://localhost:5000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "invoice_001.pdf",
    "doc_type": "Invoice",
    "user": "analyst.user",
    "metadata": {
      "vendor": "Acme Corp",
      "amount": "4500.00",
      "date": "2025-04-15"
    }
  }'
```

**Success response (201):**

```json
{
  "doc_id": "a3f9c2d1-7b84-4e21-bc93-d1f20a4c8e91",
  "folder": "/Enterprise/Finance/Invoices",
  "version": 1
}
```

**Validation failure response (400):**

```json
{
  "error": "Validation failed",
  "missing_fields": ["amount", "date"]
}
```

---

### GET `/documents/<doc_id>` — Retrieve a document

```bash
curl http://localhost:5000/documents/a3f9c2d1-7b84-4e21-bc93-d1f20a4c8e91
```

**Response:**

```json
{
  "name": "invoice_001.pdf",
  "type": "Invoice",
  "folder": "/Enterprise/Finance/Invoices",
  "version": 1,
  "status": "Pending",
  "metadata": {
    "vendor": "Acme Corp",
    "amount": "4500.00",
    "date": "2025-04-15"
  }
}
```

---

### PUT `/documents/<doc_id>/version` — Update document version

```bash
curl -X PUT http://localhost:5000/documents/a3f9c2d1-.../version \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"amount": "4750.00"}, "user": "analyst.user"}'
```

**Response:**

```json
{
  "doc_id": "a3f9c2d1-...",
  "new_version": 2
}
```

---

### GET `/documents/search` — Search documents

```bash
# All documents
curl "http://localhost:5000/documents/search"

# Filter by type
curl "http://localhost:5000/documents/search?doc_type=Invoice"

# Filter by status
curl "http://localhost:5000/documents/search?status=Pending"
```

---

### Supported Document Types

| Document Type | Required Metadata Fields | Routes To |
|---|---|---|
| `Invoice` | `vendor`, `amount`, `date` | `/Enterprise/Finance/Invoices` |
| `Contract` | `party_a`, `party_b`, `expiry` | `/Enterprise/Legal/Contracts` |
| `Report` | `author`, `department` | `/Enterprise/Operations/Reports` |
| `HR_Form` | `employee_id`, `form_type` | `/Enterprise/HR/Forms` |
| Any unknown type | — | `/Enterprise/Unclassified` |

---

## Running the Tests

### Run all tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_workflow.py::TestValidDocuments::test_invoice_validates_successfully PASSED
tests/test_workflow.py::TestValidDocuments::test_invoice_routes_to_finance_folder PASSED
tests/test_workflow.py::TestValidDocuments::test_contract_routes_to_legal_folder PASSED
tests/test_workflow.py::TestValidDocuments::test_document_gets_unique_id PASSED
tests/test_workflow.py::TestValidDocuments::test_new_document_starts_at_version_1 PASSED
tests/test_workflow.py::TestValidationFailures::test_invoice_missing_vendor_fails PASSED
tests/test_workflow.py::TestValidationFailures::test_invoice_missing_all_fields_returns_all_missing PASSED
tests/test_workflow.py::TestValidationFailures::test_unknown_doc_type_routes_to_unclassified PASSED
tests/test_workflow.py::TestVersionManager::test_version_increments_on_update PASSED
tests/test_workflow.py::TestVersionManager::test_version_history_is_preserved PASSED
...
20 passed in 0.41s
```

### Run with coverage report

```bash
pip install pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Troubleshooting Use Cases

The following use cases simulate real L2 Application Support scenarios that occur in OpenText environments. Each follows the same investigation structure used in production: **trigger → symptom → root cause → fix → verify → document.**

---

### Use Case 1 — Missing metadata causes document rejection

**Scenario:** A Finance team member calls saying "the system won't accept my invoice."

**Trigger:**

```bash
curl -X POST http://localhost:5000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "invoice_broken.pdf",
    "doc_type": "Invoice",
    "user": "finance.user",
    "metadata": {"vendor": "Acme Corp"}
  }'
```

**Symptom:**

```json
{"error": "Validation failed", "missing_fields": ["amount", "date"]}
```

**Root cause:** The `Invoice` content template requires `vendor`, `amount`, and `date`. Only `vendor` was provided.

**Fix:** Identify the missing fields from the error response and audit log. Contact the user with the exact fields required. Resubmit with complete metadata. In production OpenText, enforce mandatory fields in the upload form/content template to prevent this at source.

**Audit log entry:**

```
ERROR | ACTION=UPLOAD | DOC=xxx | ERROR=Missing fields: ['amount', 'date']
```

---

### Use Case 2 — Document routed to Unclassified folder

**Scenario:** A document ends up in `/Enterprise/Unclassified` and is not being processed by any team.

**Trigger:**

```bash
curl -X POST http://localhost:5000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "procurement_form.pdf",
    "doc_type": "Procurement",
    "user": "ops.user",
    "metadata": {"department": "IT"}
  }'
```

**Symptom:**

```json
{"folder": "/Enterprise/Unclassified", "version": 1}
```

**Root cause:** `Procurement` is not a registered document type in the content model. The routing engine falls back to `Unclassified`. In production OpenText, this occurs when a document class has not been created in the workspace classification scheme, or when a user selects the wrong document class during upload.

**Fix:** Either register `Procurement` as a new document type with its routing rule, or work with the user to identify the correct existing document type. In production, check the OpenText Admin workspace configuration.

---

### Use Case 3 — Version conflict from concurrent edits

**Scenario:** Two users update the same document simultaneously and one person's changes are overwritten.

**Trigger:**

```bash
# User 1 updates the contract expiry
curl -X PUT http://localhost:5000/documents/DOC_ID/version \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"expiry": "2027-01-01"}, "user": "legal.user1"}'

# User 2 (working from the old version) also updates
curl -X PUT http://localhost:5000/documents/DOC_ID/version \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"expiry": "2028-06-30"}, "user": "legal.user2"}'
```

**Root cause:** No checkout/reservation mechanism in place. Both users edited simultaneously and the last write wins.

**Fix:** In production OpenText, enforce the document reservation (check-out) workflow so only one user can edit at a time. The version history in this project demonstrates how to reconstruct which user made which change and when — critical for compliance investigations.

---

### Use Case 4 — Document not found (404)

**Scenario:** A user says "I uploaded the document yesterday but now I can't find it."

**Trigger:**

```bash
curl http://localhost:5000/documents/non-existent-id-99999
```

**Symptom:**

```json
{"error": "Not found"}
```

**Investigation steps:**

```bash
# 1. Search all documents to confirm it's not registered
curl "http://localhost:5000/documents/search"

# 2. Search by document type to narrow down
curl "http://localhost:5000/documents/search?doc_type=Invoice"

# 3. Check audit.log for any record of that doc_id
cat audit.log | grep "non-existent-id-99999"
```

**Root cause (in this project):** The in-memory store resets on restart — no database persistence. In production OpenText, a 404 typically means: the document is in a different workspace, the user lacks view permissions on the node, the document was archived or deleted, or the node ID changed after a migration.

**Fix:** Check the OpenText recycle bin, verify the user's access permissions on the workspace, and review the audit trail for the last known action on the document.

---

### Use Case 5 — Audit trail investigation

**Scenario:** Compliance team requests a record of all actions taken on a document as part of a regulatory review.

**How to demonstrate:**

```bash
# After uploading and updating a document, view the full audit trail
cat audit.log
```

**Example output:**

```
2025-04-15 09:12:01 | INFO  | ACTION=UPLOAD         | DOC=abc123 | USER=analyst.user   | Routed to /Enterprise/Finance/Invoices
2025-04-15 09:14:33 | INFO  | ACTION=VERSION_UPDATE | DOC=abc123 | USER=analyst.user   | Now at v2
2025-04-15 09:15:02 | ERROR | ACTION=UPLOAD         | DOC=def456 | ERROR=Missing fields: ['amount', 'date']
2025-04-15 09:18:45 | INFO  | ACTION=UPLOAD         | DOC=def456 | USER=finance.user   | Routed to /Enterprise/Finance/Invoices
```

**What this demonstrates:** In regulated environments such as superannuation, healthcare, or financial services, every document action must be traceable. The audit log provides the full chain of custody — who uploaded, who modified, when, and any errors that occurred. This is directly relevant to compliance requirements such as those in APRA-regulated entities.

---

## Key Concepts Demonstrated

**End-to-end ownership** — each feature traces a complete lifecycle from ingestion through validation, routing, versioning, and audit — not just a single layer.

**Metadata-driven classification** — document types drive both validation rules and routing decisions, mirroring how OpenText content templates and workspace classification schemes work in production.

**Structured error handling** — every failure returns a specific, actionable error message and writes a corresponding audit log entry, matching the investigation workflow used in L2/L3 support.

**Version history with snapshots** — prior versions are preserved as immutable snapshots, enabling rollback and audit reconstruction — consistent with OpenText major/minor versioning behaviour.

**Separation of concerns** — each module has a single responsibility (`content_model`, `folder_router`, `version_manager`, `audit_logger`, `api`), making the codebase easy to extend and test independently.

---

## Author

**Ibtisam**
Application Support Analyst | Melbourne, Australia
[GitHub Profile](https://github.com/YOUR_USERNAME)

> Built as part of an interview preparation portfolio demonstrating OpenText ECM concepts, Python application development, REST API design, and structured troubleshooting methodology.
