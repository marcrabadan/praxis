# Discovery Report — Live delivery tracking

> Step 1 of `feature-development`. **Example** artifact for the Helios multi-repo
> project. Routed to the business-analyst. No solutions yet.

## Problem statement

Customers don't know where their delivery is or when it will arrive, so they call
support and rate deliveries poorly. Ops can't see which in-flight deliveries are
at risk of being late.

## Business goals

- Cut "where is my order?" support contacts.
- Improve on-time delivery rate by letting ops intervene early.

## Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| Customer | Sees live location + ETA for their own delivery |
| Ops team | Monitors all in-flight deliveries, spots lateness |
| Driver | Already sends location from the driver app (out of scope here) |
| Product owner | Gate approver for spec & release |
| Tech lead | Gate approver for architecture |

## Constraints

- The API contract (`helios-api/openapi.yaml`) is canonical — any new endpoint is
  defined there first.
- ETAs are computed in `helios-workers` (project authority note), not the API.
- Customers may only see their own delivery; ops see all (authz).

## Assumptions

- Driver apps already emit location pings to an ingestion endpoint.
- Map rendering can reuse the existing map component in `helios-web`.

## Risks

- Real-time fan-out at peak load could overwhelm the API.
- Leaking another customer's location is a serious privacy incident.

## Open questions

- Which real-time transport: WebSocket or SSE? (tracked as project open-question #2)
- Do `helios-web` and `helios-console` share one component library? (open-question #1)

## Traceability

- Idea / request id: `IDEA-HELIOS-42`
- This artifact id: `DISC-live-tracking`
- Feeds: research (`RES-live-tracking`) → spec (`SPEC-live-tracking`)
