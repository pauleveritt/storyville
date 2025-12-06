# Task Breakdown: Repository Development Infrastructure Improvements

## Overview

Total Task Groups: 4
Estimated Tasks: ~15-20 individual tasks

This specification focuses on improving developer experience through better CI caching, clearer task organization, and
comprehensive documentation of development workflows. The work is primarily configuration and documentation - no
database, API, or frontend components involved.

## Task List

### Task Group 1: Justfile Recipe Reorganization

**Dependencies:** None
**Owner Role:** DevOps/Build Engineer

- [x] 1.0 Complete Justfile recipe reorganization
    - [x] 1.1 Rename `fmt` recipe to `lint`
        - Current behavior: `uv run ruff check .`
        - Keep exact same behavior, just change recipe name
        - Update any internal references if present
    - [x] 1.2 Create new `fmt` recipe for formatting
        - Command: `uv run ruff format .`
        - This actually formats code (not just checks)
        - Follow existing pattern with `*ARGS` support
    - [x] 1.3 Add `setup` recipe as alias to `install`
        - Simple alias for better discoverability
        - Pattern: `setup: install`
    - [x] 1.4 Create `ci-checks` recipe with fail-fast chaining
        - Chain: `install && lint && typecheck && test-parallel`
        - Use `&&` for fail-fast behavior (not `;`)
        - This runs all quality checks in order
    - [x] 1.5 Update `ci` recipe to use new naming
        - Replace old `fmt` call with `lint`
        - Consider calling `ci-checks` or consolidating logic
    - [x] 1.6 Verify all recipes maintain `uv run` prefix pattern
        - Ensure consistency across all commands
        - Keep `*ARGS` pattern for argument passing
    - [x] 1.7 Test locally with `just ci-checks`
        - Verify fail-fast behavior (stop on first failure)
        - Ensure all steps execute in correct order
        - Confirm proper exit codes

**Acceptance Criteria:**

- `just lint` runs ruff check (renamed from fmt)
- `just fmt` runs ruff format (new behavior)
- `just setup` works as alias for install
- `just ci-checks` chains all quality checks with fail-fast
- All recipes maintain consistent `uv run` pattern
- Local testing confirms proper behavior

---

### Task Group 2: Composite Action Enhancement with Caching

**Dependencies:** None (can run parallel with Task Group 1)
**Owner Role:** DevOps/CI Engineer

- [x] 2.0 Complete composite action caching enhancement
    - [x] 2.1 Add cache step for `.venv` directory
        - Use `actions/cache@v4` (before uv setup)
        - Action: restore cache if available
        - Path: `.venv` directory
    - [x] 2.2 Generate cache key from `uv.lock` hash
        - Key format: `venv-${{ runner.os }}-${{ hashFiles('uv.lock') }}`
        - Ensures cache invalidates when dependencies change
        - Restore keys for fallback behavior
    - [x] 2.3 Keep existing setup-uv@v7 with enable-cache
        - This caches uv's own package cache
        - Don't remove existing cache configuration
        - Two-layer caching: .venv + uv cache
    - [x] 2.4 Add cache save step (post-install)
        - Runs after successful dependency installation
        - Saves `.venv` directory for next run
        - Should only save on cache miss
    - [x] 2.5 Verify composite action structure
        - File: `.github/actions/setup-python-uv/action.yml`
        - Maintain existing step order where possible
        - Ensure shell: bash for all run steps
    - [x] 2.6 Test caching behavior locally with `act`
        - Install act: `brew install act` (if not installed)
        - Run: `act -j ci_tests --rm`
        - Verify cache restore/save steps execute
        - Note: act caching may have limitations
    - [x] 2.7 Verify workflows still reference composite action correctly
        - Check: `.github/workflows/ci.yml`
        - Check: `.github/workflows/pages.yml`
        - Check: `.github/workflows/pypi.yml`
        - All use: `./.github/actions/setup-python-uv`

**Acceptance Criteria:**

- Composite action includes cache restoration before setup
- Cache key uses hash of `uv.lock` file
- Cache saves `.venv` directory after installation
- Existing setup-uv caching remains intact
- All three workflows continue to work
- Cache significantly speeds up CI runs (verify in actual CI)

---

### Task Group 3: Documentation Updates

**Dependencies:** Task Groups 1, 2 (reference new recipes and workflows)
**Owner Role:** Technical Writer/Documentation Engineer

- [x] 3.0 Complete documentation updates
    - [x] 3.1 Add "Development" section to README.md
        - Location: After "Contributing" section (around line 384)
        - Follow existing README formatting style
        - Include section header with emoji (e.g., "### 🛠️ Development Commands")
    - [x] 3.2 Create command mapping table in README
        - Column 1: Just Recipe (preferred approach)
        - Column 2: Direct Command (alternative)
        - Include: install/setup, lint, fmt, typecheck, test, test-parallel, ci-checks
        - Example: `just install` → `uv sync --all-groups`
    - [x] 3.3 Document act tool for local workflow testing
        - Installation: `brew install act` (macOS)
        - Basic usage: `act -j ci_tests --rm`
        - Note limitations: caching behavior, secrets handling
        - Link to act documentation: https://github.com/nektos/act
    - [x] 3.4 Add note about Just recipes as preferred method
        - Clearly state Just is the recommended approach
        - Explain alternatives are for contributors without Just
        - Maintain consistency with existing Contributing section
    - [x] 3.5 Update tech-stack.md with actual project stack
        - File: `agent-os/standards/global/tech-stack.md`
        - Replace placeholder content with real tools
        - Section: Framework & Runtime
            - Python 3.14+ (3.14-only, no matrix testing)
            - uv 1.x (package manager)
            - Just 1.x (task runner, preferred)
        - Section: Testing & Quality
            - ruff 0.14.4+ (linting and formatting)
            - pytest 9.0+ (testing framework)
            - ty/basedpyright (type checking)
        - Section: Deployment & Infrastructure
            - GitHub Actions (CI/CD)
            - Composite action pattern for reusability
        - Add version requirements/ranges for each tool
        - Document Just as preferred with uv alternatives
    - [x] 3.6 Update conventions.md with development workflows
        - File: `agent-os/standards/global/conventions.md`
        - Add section: "Quality Check Sequence"
            - Order: lint → format → type check → test
            - Command: `just ci-checks` or individual steps
            - All must pass before committing
        - Add section: "Caching Strategy"
            - `.venv` directory cached with dependency hash
            - uv cache via setup-uv action
            - Speeds up CI by avoiding reinstalls
        - Add section: "Composite Action Pattern"
            - Centralized setup steps in `.github/actions/`
            - Reusable across all workflows
            - Maintains consistency and reduces duplication
        - Add section: "Local CI Testing"
            - Use `act` tool for workflow validation
            - Test before pushing to avoid CI failures
            - Note: some features may not work identically

**Acceptance Criteria:**

- README includes new "Development" section with command table
- Command mapping shows Just recipes and direct alternatives
- act tool installation and usage documented
- tech-stack.md reflects actual project tooling with versions
- conventions.md includes quality check workflow and caching strategy
- Documentation is clear, consistent, and actionable

---

### Task Group 4: Verification and Testing

**Dependencies:** Task Groups 1, 2, 3
**Owner Role:** QA/Integration Engineer

- [ ] 4.0 Complete end-to-end verification
    - [ ] 4.1 Test all Justfile recipes locally
        - Run: `just --list` (verify all recipes visible)
        - Test: `just setup` (alias works)
        - Test: `just lint` (ruff check)
        - Test: `just fmt` (ruff format)
        - Test: `just typecheck` (ty check)
        - Test: `just test` (pytest)
        - Test: `just ci-checks` (full chain with fail-fast)
    - [ ] 4.2 Test direct command alternatives
        - Verify each command in documentation table works
        - Test: `uv sync --all-groups`
        - Test: `uv run ruff check .`
        - Test: `uv run ruff format .`
        - Test: `uv run ty check`
        - Test: `uv run pytest`
        - Ensure documentation is accurate
    - [ ] 4.3 Test composite action locally with act
        - Run: `act -j ci_tests --rm`
        - Verify setup steps execute correctly
        - Check cache restore/save steps (may have limitations)
        - Verify all quality checks run
    - [ ] 4.4 Push to branch and verify CI workflows
        - Push to feature branch (e.g., `improve-repo`)
        - Watch: `.github/workflows/ci.yml` execution
        - Verify: Cache restoration works (check logs)
        - Verify: All quality checks pass
        - Check: Build time improvement from caching
    - [ ] 4.5 Test pages workflow (if applicable)
        - Trigger: Push to main or manual workflow dispatch
        - Verify: Composite action works in pages context
        - Check: Documentation site builds successfully
    - [ ] 4.6 Review documentation clarity
        - Read through new README "Development" section
        - Verify command table is accurate
        - Check tech-stack.md for completeness
        - Check conventions.md for clarity
        - Ensure no broken links or typos
    - [ ] 4.7 Run final quality checks
        - Execute: `just ci-checks`
        - Ensure: All checks pass (lint, format, typecheck, test)
        - Verify: Code formatting consistent (run `just fmt`)
        - Confirm: No regressions introduced

**Acceptance Criteria:**

- All Justfile recipes work as documented
- Direct command alternatives execute successfully
- Local act testing works (within known limitations)
- CI workflows pass with improved caching
- Documentation is accurate and complete
- All quality checks pass without errors

---

## Execution Order

**Recommended implementation sequence:**

1. **Start with Task Group 1 and 2 in parallel** (independent work)
    - Task Group 1: Justfile reorganization (local changes)
    - Task Group 2: Composite action enhancement (CI changes)

2. **Then Task Group 3** (depends on knowing new recipes and workflow)
    - Document the changes made in Groups 1 and 2
    - Update standards files with actual project details

3. **Finally Task Group 4** (verification of all changes)
    - Test everything locally and in CI
    - Ensure documentation accuracy

**Estimated Timeline:**

- Task Group 1: 30-45 minutes
- Task Group 2: 45-60 minutes (includes testing with act)
- Task Group 3: 60-90 minutes (documentation writing)
- Task Group 4: 30-45 minutes (verification)
- **Total: 2.5-4 hours**

---

## Important Notes

### No Testing Code Required

- This is purely configuration and documentation work
- No unit tests or integration tests to write
- Verification is done through manual testing and CI runs
- Use act tool for local workflow validation

### Python 3.14-Only Project

- No matrix testing needed
- No version parameters in workflows
- Single Python version simplifies CI configuration

### Fail-Fast Philosophy

- Use `&&` in ci-checks recipe for immediate failure
- `continue-on-error: false` in all workflow steps
- Stops at first failure to save time and provide clear feedback

### Caching Strategy

- Two-layer caching: `.venv` directory + uv's package cache
- Cache key tied to `uv.lock` hash for proper invalidation
- Significantly speeds up CI runs (30-60 second improvement expected)

### Documentation Philosophy

- Just recipes are "preferred" but not required
- Always show direct command alternatives
- Make project accessible to contributors without Just installed
- Clear, actionable instructions with examples

### Files to Modify

- `Justfile` (Task Group 1)
- `.github/actions/setup-python-uv/action.yml` (Task Group 2)
- `README.md` (Task Group 3)
- `agent-os/standards/global/tech-stack.md` (Task Group 3)
- `agent-os/standards/global/conventions.md` (Task Group 3)

### Files to Reference (no changes)

- `.github/workflows/ci.yml` (verify it still works)
- `.github/workflows/pages.yml` (verify it still works)
- `.github/workflows/pypi.yml` (verify it still works)

---

## Alignment with Standards

This tasks list is designed to align with:

- **Python 3.14+ standards** (modern syntax, type hints)
- **Minimal testing philosophy** (no test code for infrastructure changes)
- **Quality check workflow** (lint, format, typecheck, test sequence)
- **Clear documentation** (Just preferred, alternatives documented)
- **Composite action pattern** (reusable CI/CD components)

---

## Success Criteria

✅ All Justfile recipes work as documented and expected
✅ Composite action successfully caches `.venv` and speeds up CI
✅ Documentation clearly shows Just recipes and direct alternatives
✅ Standards files reflect actual project tech stack and conventions
✅ All three GitHub workflows (ci, pages, pypi) continue to work
✅ Local testing with act validates workflow behavior
✅ Quality checks pass: lint, format, typecheck, test
