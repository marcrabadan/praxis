# Choosing the Right Diagram Type

Use this guide when the user's request is ambiguous. Pick one type and stick to it — mixed-type diagrams are hard to read.

---

## Decision tree

```
What does the user want to see?
│
├─ Structure (what exists, how parts relate spatially)
│  ├─ System-level: services, datastores, external actors → Architecture (C4 flowchart)
│  ├─ Code-level: classes, modules, packages              → Class diagram (Mermaid classDiagram)
│  └─ Data entities and their relationships               → ER diagram
│
├─ Behaviour over time (who does what, in what order)
│  ├─ API calls, user journeys, event flows               → Sequence diagram
│  └─ State transitions (e.g. order status lifecycle)     → State diagram (Mermaid stateDiagram-v2)
│
└─ Data movement / process steps
   ├─ Pipeline, ETL, data flow                            → Flow diagram (flowchart LR)
   └─ Decision logic, branching                           → Flow diagram (flowchart TD with diamonds)
```

---

## Type comparison

| Type | Best for | Avoid when |
|------|----------|------------|
| Architecture (C4 flowchart) | Showing the overall system at a glance; onboarding new engineers | Showing timing or sequence of calls |
| Sequence | Debugging interaction bugs; documenting an API contract; auth/data flows | Showing how components are structured |
| ER | Documenting the data model; schema design reviews | Showing runtime behaviour |
| Flow | Data pipeline steps; CI/CD workflow; decision logic | Complex multi-actor interactions (use sequence instead) |
| Class | Module/package API surface; OO inheritance hierarchies | Runtime or deployment topology |

---

## C4 levels (for architecture diagrams)

Use the right level for the audience:

| Level | Shows | Audience |
|-------|-------|----------|
| **L1 System context** | Your system + external actors and systems that interact with it | Non-technical stakeholders |
| **L2 Container** | Services, databases, frontends inside your system boundary | Engineers onboarding |
| **L3 Component** | Modules/classes inside one container | The team working on that service |
| **L4 Code** | Class diagrams — rarely useful in Mermaid; use IDE tooling instead | Code reviewers |

When in doubt, draw L2 (containers). It gives the best ratio of insight to complexity.

---

## Combine types only when necessary

If a complete picture needs more than one diagram type, produce separate diagrams and link them. For example:

- An architecture diagram (L2) showing the containers.
- A sequence diagram showing the auth flow between those containers.
- An ER diagram showing the data model used by the database container.

Produce them in the order above — structure first, then behaviour, then data.
