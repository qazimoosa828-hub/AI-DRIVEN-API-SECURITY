# Vulnerable Demo API

**⚠️ DEMONSTRATION ONLY — Contains intentional security vulnerabilities**

This API is designed to demonstrate OWASP API Security Top 10 vulnerabilities for the security assessment platform.

## Test Accounts (DEMONSTRATION DATA)

| Username | Password    | Role  | User ID |
|----------|------------|-------|---------|
| user1    | password123 | user  | 1       |
| user2    | password456 | user  | 2       |
| admin    | adminpass   | admin | 3       |

## Intentional Vulnerabilities

| OWASP Category | Endpoint | Vulnerability |
|---------------|----------|--------------|
| API1 - BOLA | GET /api/items/{id} | No ownership check |
| API2 - Broken Auth | GET /api/users/{id} | No auth required |
| API3 - Property Auth | GET /api/users/me | Returns SSN, address |
| API4 - Resource Consumption | GET /api/search | No page_size limit |
| API5 - Function Auth | GET /api/admin/users | No role check |
| API6 - Business Flows | POST /api/orders | No rate/quantity limit |
| API7 - SSRF | POST /api/fetch-url | No URL validation |
| API8 - Misconfiguration | All responses | CORS *, debug info, stack traces |
| API9 - Inventory | /api/admin/config | Exposes internal config |
| API10 - Unsafe Consumption | POST /api/fetch-url | No input validation |

## Secure Comparison Endpoints

- GET /api/secure/items/{id} — With ownership check
- GET /api/secure/users/me — Returns safe properties only
- GET /api/secure/admin/users — With role enforcement

## Running

```bash
cd demo-api
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --host 127.0.0.1
```

## Reset Demo Data

```bash
curl -X POST http://localhost:8001/api/reset
```

## OpenAPI Documentation

Available at http://localhost:8001/docs when running.
