# Sample: `/review-changes` — didactic, severity-tagged review

> Illustrative transcript. See [README](README.md) for what that means.

---

**Prompt**

```text
/review-changes
```

*(Reviewing the working diff that adds the "pay with a saved card" endpoint.)*

---

**Response**

Diff touches an authenticated payment endpoint and its handler. Routing to **developer**
(baseline) + **security-engineer** (authz on a money path) + **qa-engineer** (untested branch).
The relevant hunk:

```python
@app.post("/checkout/pay")
def pay(req):
    method = db.get_payment_method(req.json["method_id"])   # saved Stripe token
    charge = stripe.charge(method.token, req.json["amount"])
    return {"status": charge.status}
```

### 🔴 Blocker

- **🔴 server.py:3 — Missing ownership check on saved payment method (IDOR)**
  - **What:** `get_payment_method(method_id)` is fetched by ID with no check that it belongs to
    the authenticated user.
  - **Why it matters:** Any logged-in user can pass another user's `method_id` and charge *their*
    saved card — a textbook IDOR / broken object-level authorization (Security checklist: authorization;
    OWASP A01). This is account takeover of payment.
  - **Fix:** Scope the lookup to the caller: `db.get_payment_method(method_id, owner=req.user.id)`
    and return 404 (not 403) when it doesn't match, so you don't leak which IDs exist.

### 🟠 Should-fix

- **🟠 server.py:4 — Amount taken from the client**
  - **What:** `amount` comes straight from the request body.
  - **Why it matters:** A client-supplied price lets the caller pay $0.01 for a $100 order
    (Developer checklist: never trust client input for authoritative values).
  - **Fix:** Derive the amount from the server-side order/cart total keyed to the order ID; ignore any client amount.

- **🟠 server.py:4 — Unhandled processor failure**
  - **What:** `stripe.charge(...)` can raise (network, declined card, rate limit); nothing catches it.
  - **Why it matters:** An unhandled exception 500s the checkout and leaks a stack trace
    (Developer checklist: error handling at I/O boundaries).
  - **Fix:** Wrap the call; map declines to a clean 402 with a user-safe message, log the rest.

### 🟡 Nit

- **🟡 server.py:2 — Direct `req.json[...]` indexing**
  - **What:** Missing keys raise `KeyError` → 500 instead of a 400.
  - **Why it matters:** Validate inputs at the edge; return actionable 4xx errors.
  - **Fix:** Parse/validate the body with a schema (e.g. pydantic) and reject malformed requests with 400.

**Verdict: Changes requested.** One blocker (payment IDOR) must be fixed before merge; two
should-fix issues on the same money path. No tests cover this handler — add the ownership-denied
and declined-card cases. *Experts consulted: developer, security-engineer, qa-engineer.*
