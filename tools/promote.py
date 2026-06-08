"""Praxis promotion executor — close the learning loop, under human gate.

A validated assumption (never-assume), or a gap surfaced by skill-learner, can
generalise: it is not a one-off but knowledge the team should *always* apply.
This tool turns that into a **pending governance proposal** — a proposed new
rule, workflow gate, eval, or guardrail — and routes who authors it.

Two hard rules, inherited from the harness doctrine, are enforced here:

  * **Promote on evidence, never on anticipation.** A promotion from an
    assumption requires that the assumption is *resolved* (confirmed or
    corrected); a direct proposal requires explicit evidence. An open guess
    cannot become a rule.
  * **Propose, never mutate.** This tool does **not** create the rule/gate/eval.
    It records the proposal as a `pending` entry in the memory ledger and prints
    the routing. A human accepts it (`/memory accept <id>`) and authors it
    (rules → rules/, gates → workflows/, evals/skills → skill-creator). Pending
    is not approval.

The proposal is a normal memory-ledger `decision` entry (status `pending`),
tagged `promotion`, `promote:<target>`, and — when it came from an assumption —
`source:<ASSUME-id>`. It is not a parallel store: it lives and dies in the
ledger's existing accept / reject / supersede lifecycle.

Deterministic, stdlib-only. It reuses tools/assumptions.py and the memory
ledger; it adds no new state of its own.

Usage:
    python promote.py from-assumption ASSUME-… [--target rule] [--draft "…"] \
        [--dest rules/api-timestamps.md] [--note "…"]
    python promote.py propose --target gate --title "verify needs perf budget" \
        --evidence "3 incidents traced to unbudgeted latency" \
        --rationale "make it a release gate" [--dest workflows/…] [--draft "…"]
    python promote.py list [--target rule]
    python promote.py routing rule

Exit codes:
    0: success
    1: not found / nothing to do / evidence rule not satisfied
    2: arguments wrong
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import assumptions as A

# The memory ledger lives in a skill, not in tools/; import it the same way
# validate_harness imports the factory's frontmatter parser.
_LEDGER_DIR = (
    Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "memory" / "scripts"
)
sys.path.insert(0, str(_LEDGER_DIR))
import ledger  # noqa: E402

# Targets a promotion can have — aligned with assumptions.py PROMOTE_TARGETS
# minus "none" (which means "not promotable").
TARGETS = ("rule", "guardrail", "eval", "gate")
# Resolved assumption statuses — only these carry the evidence to promote.
_RESOLVED = ("confirmed", "corrected")

# Deterministic authoring guidance per target: where the accepted proposal is
# turned into real governance, and by whom. This is the bridge to skill-learner.
ROUTING = {
    "rule": (
        "Author a new `rules/<name>.md` (a short, behaviour-changing harness "
        "rule), add it to the rules list in AGENTS.md, and add a deterministic "
        "check + test if the rule is mechanically checkable."
    ),
    "gate": (
        "Add the condition to the relevant `workflows/<id>.workflow.json` `gates` "
        "(or `loops`/`stopConditions`), then `make validate-harness`. Document it "
        "in the matching `systems/` doc."
    ),
    "eval": (
        "Add positive/negative cases to the owning skill's `evals/*.json`. Route "
        "through skill-learner → skill-creator's evaluate flow; run the validator."
    ),
    "guardrail": (
        "Add a deterministic check under `tools/` (a validator) or a workflow "
        "gate, and wire it into `make`/CI so it actually blocks. Never a check the "
        "model is merely asked to remember."
    ),
}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _ledger_log(*, title: str, body: str, tags: list[str]) -> str:
    """Append a pending 'decision' entry to the memory ledger; return its id."""
    ledger._ensure_structure()
    entry_id = ledger._new_id()
    now = ledger._now()
    meta = {
        "id": entry_id,
        "created": now,
        "updated": now,
        "source": "/promote",
        "type": "decision",
        "status": "pending",
        "title": title,
        "tags": tags,
        "supersedes": None,
    }
    ledger._add_entry(meta, body)
    return entry_id


def _proposal_body(*, target: str, headline: str, evidence_lines: list[str],
                   draft: str | None, dest: str | None) -> str:
    draft_block = draft.strip() if draft and draft.strip() else \
        "_TBD — author on acceptance (see routing below)._"
    dest_block = dest.strip() if dest and dest.strip() else \
        "_TBD — pick the smallest home that fits (see routing below)._"
    evidence = "\n".join(f"- {line}" for line in evidence_lines) or "- _(none recorded)_"
    return (
        f"# Promotion proposal — {target}: {headline}\n\n"
        f"**Status: pending. Recording is not authorization.** Accept with "
        f"`/memory accept <id>` before any {target} is authored. *Promote on "
        f"evidence, never on anticipation; propose, never mutate.*\n\n"
        f"## Evidence\n\n{evidence}\n\n"
        f"## Proposed governance ({target})\n\n{draft_block}\n\n"
        f"## Destination\n\n{dest_block}\n\n"
        f"## Routing (author only after acceptance)\n\n{ROUTING[target]}\n"
    )


def _link_assumption(assume_id: str, ledger_id: str, target: str) -> None:
    """Point the assumption at its proposal (decision_ref) without changing status."""
    rows = A._read_index()
    row = A._find(rows, assume_id)
    if not row:
        return
    row["decision_ref"] = ledger_id
    row["promote"] = target
    row["updated"] = A._now()
    A._write_index(rows)
    body = A._read_entry_body(row["id"]).rstrip()
    footer = (f"_promotion proposed {A._now()} → {target} "
              f"(memory ledger {ledger_id}, pending)_")
    A._write_entry_md(dict(row), body + f"\n\n---\n\n{footer}\n")


# --------------------------------------------------------------------------- #
# from-assumption
# --------------------------------------------------------------------------- #
def cmd_from_assumption(args) -> int:
    row = A._find(A._read_index(), args.id)
    if not row:
        print(f"error: no assumption matching {args.id!r}", file=sys.stderr)
        return 1
    if row.get("status") not in _RESOLVED:
        print(f"error: assumption {row['id']} is '{row.get('status')}', not resolved. "
              f"Promote on evidence: confirm or correct it first "
              f"(`assumptions.py confirm|correct`).", file=sys.stderr)
        return 1

    target = args.target or (row.get("promote") if row.get("promote") in TARGETS else None)
    if target not in TARGETS:
        print(f"error: no promotion target. Pass --target ({'|'.join(TARGETS)}) or set "
              f"one when resolving the assumption (`--promote`).", file=sys.stderr)
        return 2

    resolution = row.get("resolution") or "confirmed as originally stated"
    evidence = [
        f"Source assumption: `{row['id']}` ({row.get('status')}, "
        f"confidence {row.get('confidence')})",
        f"What was assumed: {row.get('statement', '')}",
        f"Validated resolution: {resolution}",
        f"Originally recorded by: {row.get('source', '')}",
    ]
    body = _proposal_body(
        target=target, headline=row.get("statement", ""),
        evidence_lines=evidence, draft=args.draft, dest=args.dest,
    )
    tags = ["promotion", f"promote:{target}", f"source:{row['id']}"]
    ledger_id = _ledger_log(
        title=f"Promote to {target}: {row.get('statement', '')}",
        body=body, tags=tags,
    )
    _link_assumption(row["id"], ledger_id, target)

    print(f"{ledger_id}")
    print(f"  pending promotion proposal ({target}) recorded in the memory ledger, "
          f"linked from {row['id']}.")
    print(f"  Accept with `/memory accept {ledger_id}`, then author it:")
    print(f"    {ROUTING[target]}")
    return 0


# --------------------------------------------------------------------------- #
# propose — direct, evidence-required (e.g. from skill-learner)
# --------------------------------------------------------------------------- #
def cmd_propose(args) -> int:
    if args.target not in TARGETS:
        print(f"error: --target must be one of {'|'.join(TARGETS)}", file=sys.stderr)
        return 2
    if not (args.evidence and args.evidence.strip()):
        print("error: --evidence is required. Promote on evidence, never on "
              "anticipation.", file=sys.stderr)
        return 2
    evidence = [args.evidence.strip()]
    if args.rationale and args.rationale.strip():
        evidence.append(f"Rationale: {args.rationale.strip()}")
    body = _proposal_body(
        target=args.target, headline=args.title,
        evidence_lines=evidence, draft=args.draft, dest=args.dest,
    )
    tags = ["promotion", f"promote:{args.target}"]
    ledger_id = _ledger_log(
        title=f"Promote to {args.target}: {args.title}", body=body, tags=tags,
    )
    print(f"{ledger_id}")
    print(f"  pending promotion proposal ({args.target}) recorded in the memory ledger.")
    print(f"  Accept with `/memory accept {ledger_id}`, then author it:")
    print(f"    {ROUTING[args.target]}")
    return 0


# --------------------------------------------------------------------------- #
# list / routing
# --------------------------------------------------------------------------- #
def cmd_list(args) -> int:
    rows = [r for r in ledger._read_index()
            if "promotion" in (r.get("tags") or [])]
    if args.target:
        want = f"promote:{args.target}"
        rows = [r for r in rows if want in (r.get("tags") or [])]
    if getattr(args, "pending", False):
        rows = [r for r in rows if r.get("status") == "pending"]
    if not rows:
        print("(no matching promotion proposals)")
        return 0
    rows.sort(key=lambda r: r.get("created", ""), reverse=True)
    for r in rows:
        target = next((t.split(":", 1)[1] for t in (r.get("tags") or [])
                       if t.startswith("promote:")), "?")
        print(f"{r.get('id')}  [{r.get('status')}]  {target}\n    {r.get('title', '')}")
    return 0


def cmd_routing(args) -> int:
    if args.target not in TARGETS:
        print(f"error: target must be one of {'|'.join(TARGETS)}", file=sys.stderr)
        return 2
    print(ROUTING[args.target])
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Praxis promotion executor.")
    sub = p.add_subparsers(dest="cmd", required=True)

    fa = sub.add_parser("from-assumption",
                        help="Propose a promotion from a resolved assumption.")
    fa.add_argument("id", help="the ASSUME- id to promote")
    fa.add_argument("--target", help=f"one of: {'|'.join(TARGETS)} "
                    "(defaults to the assumption's recorded promote target)")
    fa.add_argument("--draft", help="a first draft of the rule/gate/eval text")
    fa.add_argument("--dest", help="proposed destination path")
    fa.add_argument("--note")
    fa.set_defaults(func=cmd_from_assumption)

    pr = sub.add_parser("propose", help="Propose a promotion directly (evidence required).")
    pr.add_argument("--target", required=True, help=f"one of: {'|'.join(TARGETS)}")
    pr.add_argument("--title", required=True)
    pr.add_argument("--evidence", required=True,
                    help="the evidence this should be durable governance")
    pr.add_argument("--rationale")
    pr.add_argument("--draft")
    pr.add_argument("--dest")
    pr.set_defaults(func=cmd_propose)

    ls = sub.add_parser("list", help="List promotion proposals in the ledger.")
    ls.add_argument("--target", help=f"filter by target ({'|'.join(TARGETS)})")
    ls.add_argument("--pending", action="store_true", help="only those awaiting acceptance")
    ls.set_defaults(func=cmd_list)

    rt = sub.add_parser("routing", help="Print the authoring routing for a target.")
    rt.add_argument("target", help=f"one of: {'|'.join(TARGETS)}")
    rt.set_defaults(func=cmd_routing)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
