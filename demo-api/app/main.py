"""
DEMONSTRATION API — Deliberately Vulnerable API for Testing
============================================================
THIS API IS FOR LOCAL TESTING ONLY. It contains INTENTIONAL security
weaknesses for demonstrating the security assessment platform.

DO NOT deploy this to any public-facing server.
DO NOT use this with real user data.

Test accounts (DEMONSTRATION DATA):
- user1 / password123 (regular user, id=1)
- user2 / password456 (regular user, id=2)
- admin / adminpass (admin user, id=3)
"""

from fastapi import FastAPI, HTTPException, Header, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import hashlib
import json
import time
import uuid

app = FastAPI(
    title="Vulnerable Demo API",
    description="DEMONSTRATION ONLY — Intentionally vulnerable API for security testing",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Intentionally misconfigured CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── DEMO DATA (DEMONSTRATION DATA — NOT REAL) ─────────────────────

DEMO_USERS = {
    1: {"id": 1, "username": "user1", "email": "user1@demo.local", "role": "user",
        "password": "password123", "full_name": "Demo User One", "ssn": "123-45-6789",
        "phone": "555-0101", "address": "123 Demo St"},
    2: {"id": 2, "username": "user2", "email": "user2@demo.local", "role": "user",
        "password": "password456", "full_name": "Demo User Two", "ssn": "987-65-4321",
        "phone": "555-0102", "address": "456 Test Ave"},
    3: {"id": 3, "username": "admin", "email": "admin@demo.local", "role": "admin",
        "password": "adminpass", "full_name": "Demo Admin", "ssn": "000-00-0000",
        "phone": "555-0100", "address": "789 Admin Blvd"},
}

DEMO_ITEMS = {
    1: {"id": 1, "owner_id": 1, "name": "User1 Item A", "value": 100, "secret_notes": "Confidential A"},
    2: {"id": 2, "owner_id": 1, "name": "User1 Item B", "value": 200, "secret_notes": "Confidential B"},
    3: {"id": 3, "owner_id": 2, "name": "User2 Item C", "value": 300, "secret_notes": "Confidential C"},
    4: {"id": 4, "owner_id": 2, "name": "User2 Item D", "value": 400, "secret_notes": "Confidential D"},
    5: {"id": 5, "owner_id": 3, "name": "Admin Item E", "value": 500, "secret_notes": "Admin Secret"},
}

DEMO_ORDERS = {
    1: {"id": 1, "user_id": 1, "product": "Widget", "quantity": 2, "total": 50.0, "status": "completed"},
    2: {"id": 2, "user_id": 2, "product": "Gadget", "quantity": 1, "total": 75.0, "status": "pending"},
}

PROMO_CODES = {"DEMO2024": {"discount": 50, "used": False, "max_uses": 1, "current_uses": 0}}

# Simple token store — INTENTIONALLY WEAK (demo only)
TOKENS = {}

# ─── MODELS ─────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class ItemCreate(BaseModel):
    name: str
    value: float = 0
    secret_notes: str = ""

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    secret_notes: Optional[str] = None
    owner_id: Optional[int] = None  # VULNERABLE: allows owner reassignment

class OrderCreate(BaseModel):
    product: str
    quantity: int = 1

class URLRequest(BaseModel):
    url: str

class PromoRequest(BaseModel):
    code: str

# ─── AUTH HELPERS ───────────────────────────────────────────────────

def simple_token(user_id: int) -> str:
    """Generate a simple demo token — INTENTIONALLY WEAK"""
    token = hashlib.md5(f"{user_id}-{time.time()}".encode()).hexdigest()
    TOKENS[token] = user_id
    return token

def get_current_user_id(authorization: Optional[str] = Header(None)) -> Optional[int]:
    """Extract user from token — does NOT enforce auth (vulnerability)"""
    if not authorization:
        return None
    token = authorization.replace("Bearer ", "")
    return TOKENS.get(token)

def require_auth(authorization: str = Header(...)) -> int:
    """Require authentication"""
    token = authorization.replace("Bearer ", "")
    user_id = TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

# ─── HEALTH & INFO ─────────────────────────────────────────────────

@app.get("/", tags=["info"])
def root():
    return {
        "name": "Vulnerable Demo API",
        "version": "1.0.0",
        "status": "running",
        "note": "DEMONSTRATION ONLY — Contains intentional vulnerabilities",
        "server": "DemoServer/1.0",  # VULNERABLE: Server info disclosure
        "debug_mode": True,  # VULNERABLE: Debug info exposure
    }

@app.get("/health", tags=["info"])
def health():
    return {"status": "ok", "uptime": time.time()}

# ─── AUTH ENDPOINTS ─────────────────────────────────────────────────

@app.post("/api/auth/register", tags=["auth"])
def register(req: RegisterRequest):
    """Register a new user — VULNERABLE: No rate limiting, no password policy"""
    for u in DEMO_USERS.values():
        if u["username"] == req.username:
            raise HTTPException(400, "Username taken")
    new_id = max(DEMO_USERS.keys()) + 1
    DEMO_USERS[new_id] = {
        "id": new_id, "username": req.username, "email": req.email,
        "role": "user", "password": req.password,  # VULNERABLE: plaintext storage
        "full_name": "", "ssn": "", "phone": "", "address": "",
    }
    token = simple_token(new_id)
    return {"token": token, "user_id": new_id, "message": "Registered"}

@app.post("/api/auth/login", tags=["auth"])
def login(req: LoginRequest):
    """Login — VULNERABLE: No brute force protection, verbose errors"""
    for u in DEMO_USERS.values():
        if u["username"] == req.username:
            if u["password"] == req.password:
                token = simple_token(u["id"])
                return {"token": token, "user_id": u["id"], "role": u["role"]}
            else:
                raise HTTPException(401, f"Wrong password for user '{req.username}'")  # VULNERABLE: user enumeration
    raise HTTPException(401, f"User '{req.username}' not found")  # VULNERABLE: user enumeration

# ─── USERS (API3 — Broken Object Property Level Authorization) ─────

@app.get("/api/users/me", tags=["users"])
def get_me(user_id: int = Depends(require_auth)):
    """Get current user profile — VULNERABLE: Returns excessive data including SSN"""
    user = DEMO_USERS.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    # VULNERABLE: Returns ALL properties including sensitive ones
    return {k: v for k, v in user.items() if k != "password"}

@app.get("/api/users/{target_id}", tags=["users"])
def get_user(target_id: int, user_id: Optional[int] = Depends(get_current_user_id)):
    """Get user profile — VULNERABLE: No auth required, excessive data"""
    # VULNERABLE: Endpoint accessible without authentication
    user = DEMO_USERS.get(target_id)
    if not user:
        raise HTTPException(404, "User not found")
    # VULNERABLE: Returns sensitive properties to any caller
    return {k: v for k, v in user.items() if k != "password"}

# ─── ITEMS (API1 — BOLA) ───────────────────────────────────────────

@app.get("/api/items", tags=["items"])
def list_items(user_id: int = Depends(require_auth)):
    """List items for current user"""
    return [item for item in DEMO_ITEMS.values() if item["owner_id"] == user_id]

@app.get("/api/items/{item_id}", tags=["items"])
def get_item(item_id: int, user_id: int = Depends(require_auth)):
    """Get item by ID — VULNERABLE: No ownership check (BOLA)"""
    item = DEMO_ITEMS.get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    # VULNERABLE: Returns ANY item regardless of ownership
    return item

@app.put("/api/items/{item_id}", tags=["items"])
def update_item(item_id: int, update: ItemUpdate, user_id: int = Depends(require_auth)):
    """Update item — VULNERABLE: No ownership check + mass assignment"""
    item = DEMO_ITEMS.get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    # VULNERABLE: No ownership check
    # VULNERABLE: Allows owner_id reassignment (mass assignment)
    update_data = update.model_dump(exclude_unset=True)
    DEMO_ITEMS[item_id].update(update_data)
    return DEMO_ITEMS[item_id]

@app.post("/api/items", tags=["items"])
def create_item(item: ItemCreate, user_id: int = Depends(require_auth)):
    """Create a new item"""
    new_id = max(DEMO_ITEMS.keys()) + 1
    DEMO_ITEMS[new_id] = {
        "id": new_id, "owner_id": user_id,
        "name": item.name, "value": item.value,
        "secret_notes": item.secret_notes,
    }
    return DEMO_ITEMS[new_id]

@app.delete("/api/items/{item_id}", tags=["items"])
def delete_item(item_id: int, user_id: int = Depends(require_auth)):
    """Delete item — VULNERABLE: No ownership check"""
    if item_id not in DEMO_ITEMS:
        raise HTTPException(404, "Item not found")
    # VULNERABLE: Any authenticated user can delete any item
    if item_id > 5:
        del DEMO_ITEMS[item_id]
    return {"message": "Deleted"}

# ─── ADMIN (API5 — Broken Function Level Authorization) ────────────

@app.get("/api/admin/users", tags=["admin"])
def admin_list_users(user_id: int = Depends(require_auth)):
    """List all users — VULNERABLE: No role check"""
    # VULNERABLE: Any authenticated user can access admin endpoint
    return [{k: v for k, v in u.items() if k != "password"} for u in DEMO_USERS.values()]

@app.delete("/api/admin/users/{target_id}", tags=["admin"])
def admin_delete_user(target_id: int, user_id: int = Depends(require_auth)):
    """Delete user — VULNERABLE: No role check"""
    # VULNERABLE: No admin role verification
    if target_id not in DEMO_USERS:
        raise HTTPException(404, "User not found")
    return {"message": f"User {target_id} would be deleted", "warning": "Demo mode — not actually deleted"}

@app.get("/api/admin/config", tags=["admin"])
def admin_config(user_id: int = Depends(require_auth)):
    """System config — VULNERABLE: No role check, exposes sensitive config"""
    return {
        "database": "demo.db",
        "debug": True,
        "secret_key": "demo-secret-key-12345",  # VULNERABLE: Secret exposure
        "api_keys": {"service_a": "key-aaa-111"},  # VULNERABLE: Key exposure
    }

# ─── ORDERS (API6 — Unrestricted Access to Sensitive Business Flows) ─

@app.post("/api/orders", tags=["orders"])
def create_order(order: OrderCreate, user_id: int = Depends(require_auth)):
    """Create order — VULNERABLE: No rate limiting, no quantity limits"""
    # VULNERABLE: No abuse prevention — can create unlimited orders
    new_id = max(DEMO_ORDERS.keys()) + 1 if DEMO_ORDERS else 1
    DEMO_ORDERS[new_id] = {
        "id": new_id, "user_id": user_id,
        "product": order.product, "quantity": order.quantity,
        "total": order.quantity * 25.0, "status": "completed",
    }
    return DEMO_ORDERS[new_id]

@app.post("/api/promo/redeem", tags=["orders"])
def redeem_promo(req: PromoRequest, user_id: int = Depends(require_auth)):
    """Redeem promo code — VULNERABLE: No rate limit, reusable codes"""
    code = PROMO_CODES.get(req.code)
    if not code:
        raise HTTPException(404, "Invalid promo code")
    # VULNERABLE: No per-user limit, can be redeemed multiple times
    return {"discount": code["discount"], "message": "Promo applied"}

# ─── URL FETCH (API7 — SSRF) ───────────────────────────────────────

@app.post("/api/fetch-url", tags=["utility"])
def fetch_url(req: URLRequest, user_id: int = Depends(require_auth)):
    """Fetch URL content — VULNERABLE: No URL validation (SSRF risk)"""
    # VULNERABLE: Accepts any URL without validation
    # In a real vulnerable app this would actually fetch the URL
    # For demo safety, we simulate the vulnerability indicator
    import urllib.parse
    parsed = urllib.parse.urlparse(req.url)
    return {
        "url": req.url,
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "status": "URL accepted for processing",
        "note": "Demo mode — URL not actually fetched for safety",
        # VULNERABLE: Returns internal URL parsing details
    }

# ─── PAGINATED ENDPOINT (API4 — Unrestricted Resource Consumption) ─

@app.get("/api/search", tags=["search"])
def search_items(
    q: str = "",
    page: int = 1,
    page_size: int = Query(default=10, le=10000),  # VULNERABLE: Allows very large page sizes
    user_id: int = Depends(require_auth),
):
    """Search items — VULNERABLE: No max page size enforcement, no rate limit"""
    # VULNERABLE: Accepts extremely large page_size
    all_items = list(DEMO_ITEMS.values())
    if q:
        all_items = [i for i in all_items if q.lower() in i["name"].lower()]
    start = (page - 1) * page_size
    return {
        "results": all_items[start:start + page_size],
        "total": len(all_items),
        "page": page,
        "page_size": page_size,  # VULNERABLE: Reflects back large page_size
    }

# ─── INPUT VALIDATION ENDPOINT ─────────────────────────────────────

@app.get("/api/query", tags=["search"])
def query_data(
    filter: str = "",
    sort: str = "id",
    user_id: int = Depends(require_auth),
):
    """Query with filter — VULNERABLE: Reflects input without sanitization"""
    # VULNERABLE: Reflects user input directly
    return {
        "filter_applied": filter,  # VULNERABLE: Input reflection
        "sort_by": sort,
        "results": list(DEMO_ITEMS.values())[:5],
        "query_info": f"Filtered by: {filter}, sorted by: {sort}",  # VULNERABLE: Input in response
    }

# ─── SECURE COMPARISON ENDPOINTS ───────────────────────────────────
# These demonstrate FIXED versions of the vulnerable endpoints

@app.get("/api/secure/items/{item_id}", tags=["secure"])
def secure_get_item(item_id: int, user_id: int = Depends(require_auth)):
    """SECURE version: Enforces ownership check"""
    item = DEMO_ITEMS.get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    if item["owner_id"] != user_id:
        raise HTTPException(403, "Access denied")
    # Only return non-sensitive properties
    return {"id": item["id"], "name": item["name"], "value": item["value"]}

@app.get("/api/secure/users/me", tags=["secure"])
def secure_get_me(user_id: int = Depends(require_auth)):
    """SECURE version: Returns only safe properties"""
    user = DEMO_USERS.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {"id": user["id"], "username": user["username"], "email": user["email"]}

@app.get("/api/secure/admin/users", tags=["secure"])
def secure_admin_list(user_id: int = Depends(require_auth)):
    """SECURE version: Enforces admin role"""
    user = DEMO_USERS.get(user_id)
    if not user or user["role"] != "admin":
        raise HTTPException(403, "Admin access required")
    return [{"id": u["id"], "username": u["username"]} for u in DEMO_USERS.values()]

# ─── RESET ENDPOINT ────────────────────────────────────────────────

@app.post("/api/reset", tags=["admin"])
def reset_demo():
    """Reset demo data to initial state — FOR DEMONSTRATION ONLY"""
    global DEMO_USERS, DEMO_ITEMS, DEMO_ORDERS, PROMO_CODES, TOKENS
    DEMO_USERS = {
        1: {"id": 1, "username": "user1", "email": "user1@demo.local", "role": "user",
            "password": "password123", "full_name": "Demo User One", "ssn": "123-45-6789",
            "phone": "555-0101", "address": "123 Demo St"},
        2: {"id": 2, "username": "user2", "email": "user2@demo.local", "role": "user",
            "password": "password456", "full_name": "Demo User Two", "ssn": "987-65-4321",
            "phone": "555-0102", "address": "456 Test Ave"},
        3: {"id": 3, "username": "admin", "email": "admin@demo.local", "role": "admin",
            "password": "adminpass", "full_name": "Demo Admin", "ssn": "000-00-0000",
            "phone": "555-0100", "address": "789 Admin Blvd"},
    }
    DEMO_ITEMS = {
        1: {"id": 1, "owner_id": 1, "name": "User1 Item A", "value": 100, "secret_notes": "Confidential A"},
        2: {"id": 2, "owner_id": 1, "name": "User1 Item B", "value": 200, "secret_notes": "Confidential B"},
        3: {"id": 3, "owner_id": 2, "name": "User2 Item C", "value": 300, "secret_notes": "Confidential C"},
        4: {"id": 4, "owner_id": 2, "name": "User2 Item D", "value": 400, "secret_notes": "Confidential D"},
        5: {"id": 5, "owner_id": 3, "name": "Admin Item E", "value": 500, "secret_notes": "Admin Secret"},
    }
    DEMO_ORDERS = {
        1: {"id": 1, "user_id": 1, "product": "Widget", "quantity": 2, "total": 50.0, "status": "completed"},
        2: {"id": 2, "user_id": 2, "product": "Gadget", "quantity": 1, "total": 75.0, "status": "pending"},
    }
    PROMO_CODES = {"DEMO2024": {"discount": 50, "used": False, "max_uses": 1, "current_uses": 0}}
    TOKENS = {}
    return {"message": "Demo data reset to initial state"}

# ─── ERROR HANDLING (API8 — Security Misconfiguration) ─────────────

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """VULNERABLE: Returns detailed error info including stack traces"""
    import traceback
    return {
        "error": str(exc),
        "type": type(exc).__name__,
        "path": str(request.url),
        "method": request.method,
        # VULNERABLE: Stack trace exposure
        "traceback": traceback.format_exc() if True else None,
    }
