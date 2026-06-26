# Financial Analyst — practices

## Assumptions ledger first

List every input the model rests on — ARPA, conversion rate, churn, CAC, gross margin — each labeled `[FACT]`/`[ESTIMATE]`/`[ASSUMPTION]` with its source or rationale. The model inherits the honesty of this ledger.

## Unit economics (show the formula)

- **LTV** = ARPA × gross margin ÷ churn
- **LTV:CAC** (target ≥ 3)
- **CAC payback** = CAC ÷ (ARPA × gross margin), in months (target < 12–18)

Always print the formula and the inputs, not just the result.

## Scenario model

Low / base / high across customers, revenue, gross profit, burn/runway, and break-even. State the single lever that moves most between scenarios.

## Sensitivity

Identify the 2–3 inputs the outcome is most sensitive to — these become the first things to validate.

## Health check

Flag any failure: LTV:CAC < 3, payback too long, non-software-like margin. Do not bury a bad result under an optimistic base case.

## Honesty

Never present a projection as a fact. A confident-looking number with no derivation is the most dangerous artifact in the building.
