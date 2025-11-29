# Justfile Commands: Test Execution Guide

## Quick Reference

### Test Execution Commands

```bash
# Sequential (original, slower)
just test

# Parallel (new, 3x faster!) 🚀
just test-parallel

# Run only slow tests in parallel
just test-slow

# Benchmark sequential vs parallel
just test-benchmark
```

---

## Detailed Command Reference

### `just test [ARGS]`
Run tests sequentially (one at a time)

**Use when:**
- Debugging a specific test failure
- Need predictable execution order
- Running single test: `just test tests/test_file.py::test_name`

**Examples:**
```bash
just test                                    # Run all tests
just test tests/test_watchers.py            # Run one file
just test -k "test_watcher"                  # Run matching tests
just test -v                                 # Verbose output
just test --durations=10                     # Show slowest tests
```

**Expected time:** ~110s for full suite

---

### `just test-parallel [ARGS]` ⚡
Run tests in parallel using all available CPU cores

**Use when:**
- Running full test suite (default)
- CI/CD pipelines
- Local development (faster feedback)

**Examples:**
```bash
just test-parallel                           # Run all tests (auto workers)
just test-parallel tests/test_watchers.py    # Run one file in parallel
just test-parallel -v                        # Verbose output
just test-parallel -n 4                      # Force 4 workers
```

**Expected time:** ~37s for full suite (67% faster!)

**How it works:**
- Auto-detects CPU cores (usually 4-8)
- Distributes tests across workers
- Each worker gets isolated temp directories
- Tests run simultaneously

---

### `just test-slow` 🐢➡️⚡
Run only slow tests (marked with `@pytest.mark.slow`) in parallel

**Use when:**
- Want to focus on optimizing slow tests
- Checking if slow tests pass
- Measuring slow test performance

**Examples:**
```bash
just test-slow                               # All slow tests, parallel
```

**Test categories included:**
- File watcher tests (7 tests, ~22s)
- Hot reload integration (8 tests, ~28s)
- Subinterpreter tests (14 tests, ~45s)
- Playwright tests (16 tests, varies)

**Expected time:** ~25-30s (vs 90-100s sequential)

---

### `just test-benchmark` 📊
Run automated benchmark comparing sequential vs parallel execution

**Use when:**
- Want to measure actual speedup on your hardware
- Verifying optimization improvements
- Reporting performance metrics

**Output:**
```
═══════════════════════════════════════════════════════════
   Pytest Parallel Execution Benchmark
═══════════════════════════════════════════════════════════

🔄 Running SEQUENTIAL (baseline)...
✓ Sequential: 50.8s

⚡ Running PARALLEL with -n 2...
✓ Parallel (n=2): 30.2s
  → Speedup: 1.68x (41% faster)

⚡ Running PARALLEL with -n 4...
✓ Parallel (n=4): 17.5s
  → Speedup: 2.90x (67% faster)

✅ Benchmark complete!
```

---

## Command Comparison

| Command | Workers | Time (est) | Use Case |
|---------|---------|------------|----------|
| `just test` | 1 | ~110s | Debugging, single test |
| `just test-parallel` | auto | ~37s | Default, CI/CD |
| `just test-slow` | auto | ~30s | Only slow tests |
| `just test-benchmark` | varies | ~5min | Performance analysis |

---

## CI/CD Integration

The `just ci` command now uses parallel execution by default:

```bash
just ci
```

**What it runs:**
1. `just install` - Install dependencies
2. `just fmt` - Check code formatting
3. `just typecheck` - Run type checker
4. `just test-parallel` - **Run tests in parallel** ⚡

---

## Advanced Usage

### Control Worker Count

```bash
# Auto-detect (recommended)
just test-parallel

# Force specific worker count
just test-parallel -n 4

# Single worker (same as just test)
just test-parallel -n 1
```

### Combine with pytest options

```bash
# Parallel + verbose + show durations
just test-parallel -v --durations=10

# Parallel + stop on first failure
just test-parallel -x

# Parallel + specific marker
just test-parallel -m "not slow"

# Parallel + coverage
just test-parallel --cov=storytime
```

### Run specific tests in parallel

```bash
# One file
just test-parallel tests/test_watchers.py

# Multiple files
just test-parallel tests/test_watchers.py tests/test_hotreload_integration.py

# Pattern matching
just test-parallel -k "watcher"
```

---

## Performance Tips

### 1. Use Parallel by Default
```bash
# Old habit
just test

# New habit (3x faster!)
just test-parallel
```

### 2. Parallel for Slow Tests
Slow tests benefit most from parallelization:
```bash
just test-slow  # 90s → 30s (3x faster)
```

### 3. Sequential for Debugging
When investigating failures, use sequential:
```bash
just test tests/test_file.py::test_failing_test -v
```

### 4. Benchmark to Verify
Measure actual performance on your hardware:
```bash
just test-benchmark
```

---

## Troubleshooting

### Issue: "pytest: error: unrecognized arguments: -n"

**Solution:** Install pytest-xdist
```bash
uv add --dev pytest-xdist
```

### Issue: Tests fail in parallel but pass sequentially

**Cause:** Shared state between tests (global variables, ports, etc.)

**Solution:** Check for:
- Global variables that aren't reset
- Hardcoded port numbers
- Shared file paths
- Singleton patterns

**Debug:**
```bash
# Run in parallel with verbose output
just test-parallel -v

# Run sequentially to confirm
just test -v
```

### Issue: Parallel tests are slower

**Cause:** Not enough independent tests to parallelize

**Solution:** Check test distribution:
```bash
# Show test durations
just test-parallel --durations=0

# If most time is in 1-2 long tests, parallel won't help much
```

---

## Migration Guide

### Update Your Workflow

**Before:**
```bash
# Local development
just test

# CI/CD
just test
```

**After:**
```bash
# Local development (3x faster!)
just test-parallel

# CI/CD (already updated)
just ci  # Uses test-parallel
```

### Update Documentation

**Before:**
```markdown
Run tests with: `just test`
```

**After:**
```markdown
Run tests with: `just test-parallel` (or `just test` for sequential)
```

---

## Summary

| Old Command | New Command | Speedup |
|-------------|-------------|---------|
| `just test` | `just test-parallel` | **3x faster** 🚀 |
| `just test -m slow` | `just test-slow` | **3x faster** 🚀 |
| `just ci` | `just ci` | **3x faster** (auto-updated) 🚀 |

**Recommendation:** Use `just test-parallel` as your default. Only use `just test` when debugging specific failures.

**Next steps:**
1. Install pytest-xdist: `uv add --dev pytest-xdist`
2. Try it: `just test-parallel`
3. Benchmark: `just test-benchmark`
4. Update your habits: Use `test-parallel` by default!

🚀 **Happy testing!**
