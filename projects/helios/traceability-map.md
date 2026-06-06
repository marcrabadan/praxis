<!-- Generated for the Helios example project. Source: projects/helios/ artifacts. -->

# Helios — Traceability map

Bidirectional map of the Helios product's artifacts: the `live-tracking` feature
chain (`IDEA → DISC → RES → SPEC → REQ → TASK → VER → REL`) plus the corrective
(`BUG-`) and quality-only (`REF-`) lifecycles and how they link back to the
requirements. Colours show **status**. Requirements are defined **once** in
`specs/live-tracking/spec.md`; tasks reference them by id, never copy them.

```mermaid
flowchart LR
    %% Helios — traceability map

    IDEA["IDEA-HELIOS-42"]:::done
    DISC["DISC-live-tracking"]:::done
    RES["RES-live-tracking"]:::done
    SPEC["SPEC-live-tracking (accepted)"]:::done

    IDEA --> DISC --> RES --> SPEC

    subgraph REQS["Requirements — defined once in spec.md"]
        R1["REQ-001 live location"]:::req
        R2["REQ-002 live ETA"]:::req
        R3["REQ-003 ops monitoring"]:::req
        R4["REQ-004 SSE transport"]:::req
        R5["REQ-005 latency NFR"]:::req
        R6["REQ-006 authz"]:::req
    end
    SPEC --> R1 & R2 & R3 & R4 & R5 & R6

    ADR1["ADR-001 SSE"]:::done
    ADR2["ADR-002 ETA in workers"]:::done
    ADR1 -->|decides| R4
    ADR2 -->|decides| R2

    subgraph API["helios-api · Team Tracking"]
        T1["TASK-001 contract"]:::done
        T2["TASK-002 SSE endpoint"]:::prog
        T3["TASK-003 authz"]:::todo
    end
    subgraph WK["helios-workers · Team Tracking"]
        T4["TASK-004 ingest pings"]:::prog
        T5["TASK-005 publish ETA"]:::todo
        T6["TASK-006 load test"]:::todo
    end
    subgraph WEB["helios-web · Team Tracking"]
        T7["TASK-007 tracking page"]:::todo
    end
    subgraph CON["helios-console · Team Ops"]
        T8["TASK-008 ops dashboard"]:::todo
    end

    R4 --> T1
    R1 --> T2
    R2 --> T2
    R6 --> T3
    R1 --> T4
    R2 --> T5
    R5 --> T6
    R1 --> T7
    R2 --> T7
    R4 --> T7
    R3 --> T8

    VER["VER-live-tracking (in progress)"]:::prog
    REL["REL-live-tracking (not released)"]:::todo
    API --> VER
    WK --> VER
    WEB --> VER
    CON --> VER
    VER --> REL
    REL -. closes .-> IDEA

    %% Corrective (BUG) and quality-only (REF) lifecycles
    PRICING["helios-api / helios-workers pricing (code)"]:::code
    BUG1["BUG-coupon-total-mismatch (fixed)"]:::done
    REF1["REF-extract-pricing-calculator (done)"]:::done
    BUG2["BUG-sse-reconnect-stale-marker (in progress)"]:::prog
    REF2["REF-web-map-perf (in progress)"]:::prog

    BUG1 --> PRICING
    REF1 --> PRICING
    REF1 -. addresses class of .-> BUG1
    BUG2 -. found in .-> R1
    REF2 -. speeds up .-> R1

    classDef done fill:#1b5e20,stroke:#0b3d12,color:#fff
    classDef prog fill:#e65100,stroke:#8f3a00,color:#fff
    classDef todo fill:#37474f,stroke:#1c272d,color:#fff
    classDef req fill:#00695c,stroke:#003f37,color:#fff
    classDef code fill:#455a64,stroke:#26333a,color:#fff
```

**Legend (status):** 🟢 green = accepted / done / fixed · 🟠 amber = in progress ·
⚫ grey = todo / pending / not released · 🟦 teal = requirement (defined once).

**How to read it**

- The spine `IDEA → DISC → RES → SPEC` is the feature being understood, researched,
  then specified — research precedes the spec.
- `ADR-001` / `ADR-002` *decide* requirements (transport, where ETA is computed).
- Each `TASK-` traces up to the `REQ-` it implements; tasks are grouped by repo and
  team. The same `REQ-001` is implemented across `helios-api`, `helios-workers`,
  and `helios-web` by **reference**, never duplicated.
- All four repos' work feeds `VER-live-tracking`; `REL-` closes the originating idea.
- `BUG-` and `REF-` are lighter lifecycles: the SSE bug and the map refinement link
  back to `REQ-001`; the pricing bug and the pricing-extraction refinement share a
  code area, and the refinement removes the duplication that bred the bug.
