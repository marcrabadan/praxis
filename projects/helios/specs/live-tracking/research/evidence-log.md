# Evidence Log — Live delivery tracking

> One row per source backing a finding. **Example** content.

| Id | Claim it supports | Source | Date | Confidence | Notes |
|----|-------------------|--------|------|------------|-------|
| EV-001 | SSE suffices for server→client updates | MDN: Server-Sent Events | 2026-06-06 | high | Auto-reconnect built in |
| EV-002 | WebSocket adds ops cost without benefit here | internal infra review notes | 2026-06-06 | medium | No client→server stream needed |
| EV-003 | ETA logic already lives in helios-workers | `helios-workers/routing/eta.py` | 2026-06-06 | high | Currently internal metrics only |
| EV-004 | Map component reusable in helios-web | `helios-web/src/components/Map` | 2026-06-06 | high | Used today for address picker |
