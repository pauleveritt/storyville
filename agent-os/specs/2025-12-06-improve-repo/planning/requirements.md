# Spec Requirements: Improve Repo - Create Composite Action

## Initial Description

Number 14 Improve Repo - Create composite action.

We've just created a composite action at `.github/actions/setup-python-uv/action.yml` that centralizes Python and uv setup across three GitHub Actions workflows (ci.yml, pages.yml, pypi.yml). This improves maintainability by avoiding duplication.

## Requirements Discussion

### First Round Questions

**Q1:** For the Justfile improvements, I'm thinking we should rename the current `fmt` to `lint` (since it runs ruff check), create a new `fmt` recipe that runs `ruff format`, add a `setup` recipe as an alias for `install`, and add a `ci-checks` recipe that chains the quality checks. Should we use `&&` to chain them (fails fast) or `;` (runs all even if one fails)?
**Answer:** `just setup` should be an alias for `install`, and `just ci-checks` should use `&&` to chain individual recipes

**Q2:** For documenting non-Just alternatives, where should we put this? I'm thinking either a "Development without Just" section in the README, or in a CONTRIBUTING.md file. Which makes more sense for your project?
**Answer:** Add a section to document non-Just alternatives (likely in README or CONTRIBUTING)

**Q3:** For the composite action improvements, should we:
- Cache the `.venv` directory itself (not just uv's cache) for faster subsequent runs?
- Include a dependency hash in the cache key so cache invalidates when dependencies change?
**Answer:** YES to composite action improvements:
- Cache the `.venv` directory (not just uv cache)
- Include dependency hash in cache key
- Note: Python version parameter removed - project is Python 3.14-only

**Q4:** For workflow modernization, should we:
- Implement concurrency controls to cancel outdated workflow runs?
- Add automated dependency updates (like Dependabot or Renovate)?
- Add workflow artifacts to preserve test reports?
**Answer:** NO/NO/NO:
- NO: Implementing concurrency controls
- NO: Dependency update automation
- NO: Workflow artifacts for test reports
- Note: Matrix testing removed - project is Python 3.14-only

**Q5:** For updating the standards files (tech-stack.md, conventions.md), should we:
- Document Just recipes as the "preferred" way but show direct uv/pytest commands as alternatives?
- Specify exact versions or version ranges for tools (uv, ruff, pytest, mypy)?
- Document the composite action pattern as a standard for future GitHub Actions?
**Answer:** YES/YES/YES:
- Just recipes as "preferred" with alternatives documented
- Specific versions/version ranges for tools
- Composite action pattern as standard

**Q6:** Are there any features or improvements we should explicitly exclude from this spec? For example:
- Pre-commit hooks setup
- Docker development environment
- Additional CI providers (CircleCI, Travis, etc.)
- Code coverage reporting setup
**Answer:** (Context indicates focus on Just, composite action, workflows, and documentation - excluding other tooling)

### Existing Code to Reference

**Similar Features Identified:**
- Composite action: `.github/actions/setup-python-uv/action.yml` (already created, needs enhancement)
- Workflows to update: `.github/workflows/ci.yml`, `.github/workflows/pages.yml`, `.github/workflows/pypi.yml`
- Justfile: Root directory (needs recipe updates)
- Standards files: `agent-os/standards/global/tech-stack.md`, `agent-os/standards/global/conventions.md`

**Testing Approach:**
- Local testing with `act` tool (brew install act)

### Follow-up Questions

None required - user provided comprehensive answers to all clarifying questions.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A - No visual files present.

## Requirements Summary

### Functional Requirements

**Justfile Updates:**
- Rename current `fmt` recipe to `lint` (runs `ruff check`)
- Create new `fmt` recipe that runs `ruff format`
- Add `setup` recipe as an alias for `install`
- Add `ci-checks` recipe that chains quality checks using `&&` (fail-fast behavior)

**Composite Action Enhancements:**
- Cache the `.venv` directory in addition to uv's cache
- Include dependency hash in cache key for proper cache invalidation

**Workflow Modernization:**
- Update all three workflows (ci.yml, pages.yml, pypi.yml) to use enhanced composite action
- Note: Project is Python 3.14-only, no matrix testing needed

**Documentation Updates:**
- Add section documenting non-Just alternatives (README or CONTRIBUTING)
- Document direct uv/pytest/ruff commands as alternatives to Just recipes
- Show both preferred (Just) and alternative approaches

**Standards Files Updates:**
- Update `tech-stack.md` with:
  - Just recipes as preferred approach
  - Direct command alternatives
  - Specific versions/version ranges for tools (uv, ruff, pytest, mypy)
  - Composite action pattern documentation
- Update `conventions.md` with:
  - Development workflow standards
  - Testing approach standards
  - CI/CD patterns

### Reusability Opportunities

**Existing Files to Modify:**
- `.github/actions/setup-python-uv/action.yml` - enhance with caching and version parameter
- `.github/workflows/ci.yml` - add matrix testing, use enhanced composite action
- `.github/workflows/pages.yml` - use enhanced composite action
- `.github/workflows/pypi.yml` - use enhanced composite action
- `Justfile` - restructure recipes as specified
- `agent-os/standards/global/tech-stack.md` - document tooling standards
- `agent-os/standards/global/conventions.md` - document development patterns

**Testing Tools:**
- Use `act` for local workflow testing before pushing

### Scope Boundaries

**In Scope:**
- Justfile recipe reorganization (fmt/lint/setup/ci-checks)
- Composite action enhancement (venv caching, version parameter, dependency hash)
- Workflow updates for matrix testing
- Documentation of Just alternatives in README or CONTRIBUTING
- Standards file updates for tech-stack.md and conventions.md

**Out of Scope:**
- Implementing concurrency controls in workflows
- Dependency update automation (Dependabot/Renovate)
- Workflow artifacts for test reports
- Pre-commit hooks setup
- Docker development environment
- Additional CI providers (CircleCI, Travis, etc.)
- Code coverage reporting setup

### Technical Considerations

**Technology Stack:**
- Python 3.14 (project standard per CLAUDE.md, 3.14-only)
- uv (package manager)
- Just (task runner)
- ruff (linting and formatting)
- pytest (testing)
- ty/basedpyright (type checking)
- GitHub Actions (CI/CD)

**Testing Approach:**
- Local workflow testing with `act` tool
- Quality checks must pass: `just test`, `just typecheck`, `just fmt`

**Caching Strategy:**
- Cache `.venv` directory for faster workflow runs
- Use dependency hash in cache key for proper invalidation
- Maintain existing uv cache behavior

**Documentation Philosophy:**
- Just recipes as "preferred" method
- Always show direct command alternatives
- Make project accessible to developers without Just installed
- Clear, actionable documentation in README or CONTRIBUTING
