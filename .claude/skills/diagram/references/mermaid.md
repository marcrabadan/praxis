# Mermaid Syntax Reference

Quick reference for the four diagram types this skill uses. Validate your output mentally against these patterns before emitting.

---

## Flowchart / Graph (architecture, flow)

```mermaid
flowchart TD
    %% TD = top-down; LR = left-right; TB = top-bottom; BT = bottom-top

    A[User Browser] -->|HTTPS| B[API Gateway]
    B --> C{Auth Service}
    C -->|valid| D[Order Service]
    C -->|invalid| E[401 Response]
    D -->|publishes| F[(Event Bus)]
    F --> G[Notification Service]

    subgraph Backend
        C
        D
        G
    end
```

**Node shapes:**
- `[Text]` — rectangle (process, service)
- `(Text)` — rounded rectangle (start/end)
- `{Text}` — diamond (decision)
- `[(Text)]` — cylinder (database)
- `[[Text]]` — subroutine
- `((Text))` — circle (event)
- `>Text]` — flag/asymmetric

**Edge labels:** `A -->|label| B`  
**Subgraphs:** `subgraph Name ... end`  
**Styling:** `style A fill:#f9f,stroke:#333`  
**Click links:** `click A href "url"`

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant API
    participant DB

    User->>Browser: Submit login form
    Browser->>+API: POST /auth/login
    API->>DB: SELECT user WHERE email=?
    DB-->>API: User record
    API-->>-Browser: 200 { token }
    Browser-->>User: Redirect to dashboard

    Note over API,DB: Token is JWT, expires in 1h

    loop Token refresh
        Browser->>API: GET /auth/refresh
        API-->>Browser: 200 { new_token }
    end
```

**Arrow types:**
- `->>` solid arrow (synchronous call)
- `-->>` dashed arrow (response)
- `-x` arrow with cross (async/fire-and-forget)
- `-)` open arrow (async)

**Activations:** `+Participant` / `-Participant`  
**Notes:** `Note over A,B: text` or `Note right of A: text`  
**Loops/alt:** `loop`, `alt`/`else`, `opt`, `par`, `critical`

---

## Entity-Relationship Diagram

```mermaid
erDiagram
    USER {
        uuid id PK
        string email
        string name
        timestamp created_at
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        decimal total
        string status
        timestamp placed_at
    }
    ORDER_ITEM {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCT {
        uuid id PK
        string sku
        string name
        decimal price
    }

    USER ||--o{ ORDER : "places"
    ORDER ||--|{ ORDER_ITEM : "contains"
    PRODUCT ||--o{ ORDER_ITEM : "appears in"
```

**Cardinality:**
- `||` exactly one
- `o|` zero or one
- `||` one (exact)
- `}|` one or more
- `}o` zero or more
- `{` (left side mirror)

**Relationship label:** always a verb phrase in quotes.  
**Attributes:** `type name [PK|FK|UK]`

---

## Class Diagram (component/module structure)

```mermaid
classDiagram
    class OrderService {
        +createOrder(userId, items) Order
        +cancelOrder(orderId) void
        -validateItems(items) bool
    }
    class PaymentService {
        +charge(orderId, amount) Receipt
        +refund(orderId) void
    }
    class Order {
        +id UUID
        +status OrderStatus
        +total Decimal
    }

    OrderService --> PaymentService : uses
    OrderService ..> Order : creates
```

**Relationships:**
- `-->` association
- `..>` dependency
- `--|>` inheritance
- `..|>` realisation (interface)
- `--*` composition
- `--o` aggregation

---

## Common mistakes to avoid

- Spaces in node IDs without quotes: use `A["My Node"]` not `A[My Node]`.
- Arrow label spaces: `A -->|label| B` works; `A --> |label| B` does not.
- ER cardinality direction: the left entity is the "one" side in `||--o{`.
- `sequenceDiagram` must have at least one `participant` or `actor` before using it.
- Nested subgraphs work in flowchart; avoid them in sequence diagrams.
- Mermaid does not support multi-line node labels — keep labels short.
