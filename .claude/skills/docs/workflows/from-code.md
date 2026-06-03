# Workflow — Docs from Code

Generate documentation by reading the codebase directly — API reference, module guides, component docs, data dictionaries.

## When you reach here

The user wants documentation derived from code, not from prior decisions. Typical triggers: "document the API", "write a component guide for X", "generate a data dictionary", "document this module".

## Steps

### 1. Identify the scope

From the user's request, determine what to document:

| Request | What to explore |
|---------|----------------|
| "document the API" | Routes, controllers, handlers, OpenAPI/GraphQL schemas |
| "document this module / package" | Exports, public functions, types, README |
| "document the data model" | ORM models, schema files, migrations, type defs |
| "component guide for X" | Component file, props, tests, usage examples |
| "document everything" | Top-level directory structure, then recurse by module |

If the scope is ambiguous, ask one clarifying question (e.g. "Which module or path should I start from?").

### 2. Explore the codebase

Use `find`, `grep`, and `Read` to gather raw material. Never invent details — read the actual source.

```bash
# Find entry points
find . -name "*.ts" -o -name "*.py" -o -name "*.go" | head -50

# Find route/handler definitions
grep -r "router\.\|app\.\|@Get\|@Post\|@route" --include="*.ts" -l

# Find model/schema definitions
grep -r "class.*Model\|Schema\|@Entity\|table(" --include="*.ts" -l

# Find component exports
grep -r "export.*function\|export default" --include="*.tsx" -l
```

Read the relevant files in full before writing anything.

### 3. Select the format

Use [references/formats.md](../references/formats.md) to pick the right document shape. Run the [references/checklist.md](../references/checklist.md) before writing.

### 4. Write the documents

For each document:

- Open with the file path or module name and a one-line purpose statement.
- Cover only the public/exported surface — internals are implementation detail.
- Include a working usage example for every exported function or component.
- For APIs: document every parameter (name, type, required, description) and the response shape.
- For data models: produce a table per entity (field, type, nullable, description).
- Use actual names from the code — do not rename or idealise them.

### 5. Record to the ledger

For each file written:

```bash
python .claude/skills/memory/scripts/ledger.py log \
  --type artifact \
  --title "<doc type>: <name>" \
  --source /docs \
  --tags docs,generated \
  --body "Generated <type> from <source path(s)>. Path: <output path>."
```

Leave the entry `pending`.

### 6. Report

List each file written with its path and the source files it was derived from. Note anything that was skipped (e.g. private internals, generated files, test fixtures) and why.
