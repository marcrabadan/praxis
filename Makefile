PYTHON ?= python
GENERATOR := .claude/skills/skill-creator/scripts/create_skill.py
VALIDATOR := .claude/factory/validators/validate_skill.py
CATALOG := .claude/factory/scripts/build_catalog.py
INTEGRATIONS := integrations/scripts/build_integrations.py
HARNESS_VALIDATOR := tools/validate_harness.py
TRACEABILITY_VALIDATOR := tools/validate_traceability.py
SKILLS_DIR := .claude/skills

.PHONY: help validate validate-all validate-harness validate-traceability check-tasks create catalog catalog-check integrations integrations-check export smoke-test clean-dist test

help:
	@echo "praxis — common tasks"
	@echo ""
	@echo "  make test                      Run ledger unit tests"
	@echo "  make validate SKILL=<path>     Validate one skill folder"
	@echo "  make validate-all              Validate every skill in .claude/skills/ and dist/"
	@echo "  make validate-harness          Validate harness state (projects, schemas, config)"
	@echo "  make validate-traceability     Check artifact source:/traces: links resolve (advisory)"
	@echo "  make check-tasks FILE=<path>   Lint a tasks.md for per-task anti-drift fields (advisory)"
	@echo "  make create NAME=<slug> TIER=<1-5> [BRIEF=<path>] [DESC=<text>] [OUT=<path>]"
	@echo "                                 Run the generator (default OUT=dist/<name>)"
	@echo "  make catalog                   Regenerate SKILLS.md (the skill + command index)"
	@echo "  make integrations              Regenerate the Cursor / IntelliJ / Codex integrations"
	@echo "  make export SKILL=<name> TO=<dir>   Copy a skill into <dir>/.claude/skills/<name>"
	@echo "  make smoke-test                Build a throwaway skill and validate it"
	@echo "  make clean-dist                Remove everything under dist/ except .gitkeep"
	@echo ""
	@echo "Examples:"
	@echo "  make validate SKILL=.claude/skills/skill-creator"
	@echo "  make create NAME=branch-namer TIER=1 DESC=\"...\""
	@echo "  make export SKILL=software-architect TO=../my-product-repo"

test:
	$(PYTHON) -m unittest discover -s .claude/skills/memory/scripts -p 'test_*.py' -v
	$(PYTHON) -m unittest discover -s tools -p 'test_*.py' -v

validate:
	@if [ -z "$(SKILL)" ]; then echo "error: SKILL=<path> is required"; exit 2; fi
	$(PYTHON) $(VALIDATOR) $(SKILL)

validate-all:
	@for d in $(SKILLS_DIR)/*/; do \
		echo "--- $$d"; \
		$(PYTHON) $(VALIDATOR) $$d || exit 1; \
	done
	@for d in $$(find dist -mindepth 1 -maxdepth 1 -type d 2>/dev/null); do \
		echo "--- $$d"; \
		$(PYTHON) $(VALIDATOR) $$d || exit 1; \
	done
	@echo "All skills validated."

validate-harness:
	$(PYTHON) $(HARNESS_VALIDATOR)

validate-traceability:
	$(PYTHON) $(TRACEABILITY_VALIDATOR)

check-tasks:
	@if [ -z "$(FILE)" ]; then echo "error: FILE=<path to tasks.md> is required"; exit 2; fi
	$(PYTHON) tools/check_tasks.py $(FILE)

create:
	@if [ -z "$(NAME)" ] || [ -z "$(TIER)" ]; then echo "error: NAME and TIER are required"; exit 2; fi
	$(PYTHON) $(GENERATOR) \
		--name $(NAME) \
		--tier $(TIER) \
		$(if $(BRIEF),--brief $(BRIEF),) \
		$(if $(DESC),--description "$(DESC)",) \
		--out $(if $(OUT),$(OUT),dist/$(NAME))

catalog:
	$(PYTHON) $(CATALOG)

catalog-check:
	$(PYTHON) $(CATALOG) --check

integrations:
	$(PYTHON) $(INTEGRATIONS)

integrations-check:
	$(PYTHON) $(INTEGRATIONS) --check

export:
	@if [ -z "$(SKILL)" ] || [ -z "$(TO)" ]; then echo "error: SKILL=<name> and TO=<dir> are required"; exit 2; fi
	@if [ ! -d "$(SKILLS_DIR)/$(SKILL)" ]; then echo "error: no such skill: $(SKILLS_DIR)/$(SKILL)"; exit 2; fi
	@mkdir -p "$(TO)/.claude/skills"
	@rm -rf "$(TO)/.claude/skills/$(SKILL)"
	@cp -R "$(SKILLS_DIR)/$(SKILL)" "$(TO)/.claude/skills/$(SKILL)"
	@echo "Exported $(SKILL) -> $(TO)/.claude/skills/$(SKILL)"

smoke-test:
	@echo "Generating throwaway tier-1 skill..."
	$(PYTHON) $(GENERATOR) \
		--name smoke-test-skill \
		--tier 1 \
		--description "Throwaway skill used by 'make smoke-test'. Use when validating the factory toolchain." \
		--purpose "Verify the generator + validator are working." \
		--out dist/_smoke-test --force
	$(PYTHON) $(VALIDATOR) dist/_smoke-test
	@echo "Smoke test passed. Cleaning up..."
	@rm -rf dist/_smoke-test

clean-dist:
	@find dist -mindepth 1 ! -name .gitkeep -exec rm -rf {} +
	@echo "Cleaned dist/."
