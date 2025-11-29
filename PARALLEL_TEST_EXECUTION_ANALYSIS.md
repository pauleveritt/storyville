# Parallel Test Execution: Performance Analysis

## Overview

This document analyzes the performance impact of running tests in parallel using pytest-xdist, comparing sequential vs parallel execution for the optimized test suite.

---

## Setup Requirements

To run tests in parallel, install pytest-xdist:

```bash
uv add --dev pytest-xdist
# or
pip install pytest-xdist
```

---

## Test Categories for Parallel Execution

### Independent Test Suites (Can Run in Parallel)

These test suites are independent and benefit from parallelization:

1. **test_watchers.py** (7 tests, ~22.4s)
   - File watcher tests with isolated tmp_path
   - No shared state between tests
   - Each test creates its own directories

2. **test_hotreload_integration.py** (8 tests, ~28.4s)
   - Hot reload integration tests
   - 5 async watcher tests (use tmp_path)
   - 3 WebSocket/app tests (may share some state)

3. **Static asset tests** (~15 tests, estimated ~5s)
   - Discovery, copying, validation, rewriting
   - Isolated file operations

4. **Story/Section/Subject tests** (~30 tests, estimated ~10s)
   - Model tests, view tests
   - Mostly unit tests with no I/O

5. **Subinterpreter tests** (14 slow tests, estimated ~45s)
   - Pool creation/shutdown per test
   - Independent builds
   - High parallelization benefit

### Tests That May Conflict (Careful Parallelization)

These tests may have shared state or resource conflicts:

1. **WebSocket broadcast tests**
   - Global WebSocket connection manager
   - May need test isolation improvements

2. **Site building tests** (examples.huge)
   - Heavy I/O and CPU usage
   - May benefit from limiting workers

---

## Expected Performance Results

### Current Performance (Sequential, Optimized)

Based on our optimizations:

| Test Suite | Tests | Duration | Notes |
|------------|-------|----------|-------|
| test_watchers.py | 7 | ~22.4s | Event-based waiting |
| test_hotreload_integration.py | 8 | ~28.4s | Watcher + WebSocket |
| Subinterpreter tests | 14 | ~45s | Pool operations |
| Static asset tests | 15 | ~5s | Fast unit tests |
| Model/view tests | 30 | ~10s | Fast unit tests |
| **TOTAL (estimated)** | **74** | **~110s** | Sequential |

---

## Parallel Execution Analysis

### Theoretical Maximum Speedup

**Amdahl's Law:** Speedup = 1 / (S + P/N)
- S = Serial fraction (fixtures, imports, teardown) ≈ 0.1 (10%)
- P = Parallel fraction ≈ 0.9 (90%)
- N = Number of workers

| Workers | Theoretical Speedup | Expected Time | Notes |
|---------|-------------------|---------------|-------|
| 1 (sequential) | 1.0x | 110s | Baseline |
| 2 | 1.82x | 60s | ~45% reduction |
| 4 | 3.08x | 36s | ~67% reduction |
| 8 | 4.71x | 23s | ~79% reduction |
| auto (CPU cores) | 3-5x | 22-37s | Depends on hardware |

### Real-World Adjustments

**Overhead factors:**
- pytest-xdist coordination: ~2-5s
- Fixture duplication per worker: ~1-2s per worker
- I/O contention (tmp files): minimal (each test uses tmp_path)
- Memory overhead: ~50MB per worker

**Adjusted estimates:**

| Workers | Real Speedup | Expected Time | Efficiency |
|---------|--------------|---------------|------------|
| 1 | 1.0x | 110s | 100% |
| 2 | 1.7x | 65s | 85% |
| 4 | 2.5x | 44s | 63% |
| 8 | 3.5x | 31s | 44% |
| **auto** | **2.5-3x** | **37-44s** | **~60%** |

---

## Benchmark Commands

### Sequential (Baseline)

```bash
# Run all optimized async tests sequentially
pytest tests/test_watchers.py tests/test_hotreload_integration.py -v --durations=10

# Expected: ~51 seconds
```

### Parallel Execution

```bash
# Auto-detect CPU cores (recommended)
pytest tests/test_watchers.py tests/test_hotreload_integration.py -n auto -v

# Expected: ~17-22 seconds (60-65% reduction)

# Explicit worker counts
pytest tests/test_watchers.py tests/test_hotreload_integration.py -n 2 -v
pytest tests/test_watchers.py tests/test_hotreload_integration.py -n 4 -v
pytest tests/test_watchers.py tests/test_hotreload_integration.py -n 8 -v

# All slow tests (subinterpreter + watchers + hotreload)
pytest -m slow -n auto -v
```

### Measuring Performance

```bash
# Sequential timing
time pytest tests/test_watchers.py tests/test_hotreload_integration.py -v

# Parallel timing
time pytest tests/test_watchers.py tests/test_hotreload_integration.py -n auto -v

# Compare
echo "Sequential: $(time pytest tests/test_watchers.py tests/test_hotreload_integration.py -q 2>&1 | grep real)"
echo "Parallel:   $(time pytest tests/test_watchers.py tests/test_hotreload_integration.py -n auto -q 2>&1 | grep real)"
```

---

## Expected Results for Watcher + Hotreload Tests

### Before Optimization (Sequential)
- **test_watchers.py:** 27.5s
- **test_hotreload_integration.py:** 31.0s
- **Total:** 58.5s

### After Event-Based Optimization (Sequential)
- **test_watchers.py:** 22.4s
- **test_hotreload_integration.py:** 28.4s
- **Total:** 50.8s
- **Improvement:** -7.7s (13% faster)

### After Event-Based Optimization + Parallel (n=4)
- **Expected total:** ~17-20s
- **Improvement over original:** -38.5s to -41.5s (66-71% faster)
- **Improvement over sequential optimized:** -30.8s to -33.8s (61-67% faster)

### After Event-Based Optimization + Parallel (n=auto, ~8 cores)
- **Expected total:** ~15-18s
- **Improvement over original:** -40.5s to -43.5s (69-74% faster)
- **Improvement over sequential optimized:** -32.8s to -35.8s (65-70% faster)

---

## Breakdown by Test Type

### Independent Tests (Highest Parallelization Benefit)

**test_watchers.py** (7 tests, 22.4s sequential):
```
Test 1: 3.0s  |████████████|
Test 2: 3.0s  |████████████|
Test 3: 0.5s  |██|
Test 4: 0.01s |.|
Test 5: 6.4s  |█████████████████████|
Test 6: 6.0s  |████████████████████|
Test 7: 3.5s  |██████████████|
```

**With n=4 workers:**
```
Worker 1: Test 1 (3.0s) + Test 4 (0.01s) = 3.01s
Worker 2: Test 2 (3.0s) + Test 3 (0.5s)  = 3.5s
Worker 3: Test 5 (6.4s)                  = 6.4s  ← Critical path
Worker 4: Test 6 (6.0s)                  = 6.0s
Worker 5: Test 7 (3.5s)                  = 3.5s

Total: ~6.4s + overhead (~1s) = ~7.4s
Speedup: 22.4s / 7.4s = 3.0x
```

**test_hotreload_integration.py** (8 tests, 28.4s sequential):
```
5 async tests: ~19.4s total (can parallelize well)
3 sync tests: ~9.0s total (WebSocket, app lifecycle)

With n=4: ~19.4/4 + 9.0/3 = ~4.9 + 3.0 = ~7.9s
Speedup: 28.4s / 7.9s = 3.6x
```

---

## Optimal Worker Count Recommendations

### Based on Test Suite Characteristics

1. **For watcher + hotreload tests (15 tests):**
   - **Optimal:** `-n 4` (best balance of speed and resource usage)
   - Expected time: ~14-17s (vs 51s sequential)
   - Speedup: ~3.0-3.6x

2. **For all slow tests (~30 tests):**
   - **Optimal:** `-n auto` or `-n 8`
   - Expected time: ~25-30s (vs 90-100s sequential)
   - Speedup: ~3.0-4.0x

3. **For full test suite (~100 tests):**
   - **Optimal:** `-n auto`
   - Expected time: ~40-50s (vs 120-150s sequential)
   - Speedup: ~2.5-3.5x

### Hardware Considerations

| CPU Cores | Recommended `-n` | Rationale |
|-----------|------------------|-----------|
| 4 cores | `-n 4` | Use all cores |
| 8 cores | `-n 8` or `-n auto` | Good parallelism |
| 16+ cores | `-n auto` | Let pytest decide |
| CI/CD | `-n 4` | Balance speed & resource limits |

---

## Implementation: Add to pyproject.toml

```toml
[dependency-groups]
dev = [
    # ... existing deps ...
    "pytest-xdist>=3.5.0",  # Add this
]
```

Or add to justfile:

```justfile
# Run tests in parallel
test-parallel:
    uv run pytest -n auto -v

# Run slow tests in parallel
test-slow-parallel:
    uv run pytest -m slow -n auto -v

# Compare sequential vs parallel
test-compare:
    @echo "Sequential:"
    @time uv run pytest tests/test_watchers.py tests/test_hotreload_integration.py -q
    @echo "\nParallel:"
    @time uv run pytest tests/test_watchers.py tests/test_hotreload_integration.py -n auto -q
```

---

## Potential Issues & Solutions

### Issue 1: WebSocket Broadcast Global State

**Problem:** `broadcast_reload()` uses global WebSocket manager
**Solution:** Use test fixtures to isolate WebSocket state per test

```python
@pytest.fixture
def isolated_websocket_manager():
    """Provide isolated WebSocket manager for each test."""
    from storytime.websocket import _connections
    old_connections = _connections.copy()
    _connections.clear()
    yield
    _connections.clear()
    _connections.update(old_connections)
```

### Issue 2: Port Conflicts (If Tests Use Servers)

**Problem:** Multiple tests trying to bind to same port
**Solution:** Use dynamic port allocation

```python
@pytest.fixture
def free_port():
    """Get a free port for test server."""
    import socket
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port
```

### Issue 3: Pytest-xdist Not Installed

**Problem:** `pytest: error: unrecognized arguments: -n`
**Solution:** Add to dev dependencies as shown above

---

## Expected Cumulative Performance Gains

### Journey of Optimizations

| Stage | Duration | Improvement | Cumulative Gain |
|-------|----------|-------------|-----------------|
| **Original (Sequential)** | 58.5s | - | - |
| + Event-based waiting | 50.8s | -7.7s (13%) | 13% faster |
| + Parallel (n=4) | 17s | -33.8s (67%) | **71% faster** 🚀 |
| + Parallel (n=8) | 15s | -35.8s (71%) | **74% faster** 🚀 |

### Test Reduction + Speed Optimizations

If we include the test reduction work:

| Metric | Before | After All Optimizations | Improvement |
|--------|--------|------------------------|-------------|
| **Test count** | ~130 tests | ~80 tests | -38% tests |
| **Test lines** | ~2,400 lines | ~1,200 lines | -50% code |
| **Slow tests (sequential)** | 58.5s | 50.8s | -13% time |
| **Slow tests (parallel)** | 58.5s | 15-17s | **71-74% faster** 🚀 |
| **Full suite (estimated)** | ~150s | ~45-50s | **67-70% faster** 🎯 |

---

## Verification Script

Create `scripts/benchmark_parallel.sh`:

```bash
#!/bin/bash
set -e

echo "=== Pytest Parallel Execution Benchmark ==="
echo ""

# Check if pytest-xdist is available
if ! uv run python -c "import xdist" 2>/dev/null; then
    echo "⚠️  pytest-xdist not installed. Installing..."
    uv add --dev pytest-xdist
fi

# Test files to benchmark
TEST_FILES="tests/test_watchers.py tests/test_hotreload_integration.py"

echo "Test files: $TEST_FILES"
echo ""

# Sequential baseline
echo "🔄 Running sequential (baseline)..."
SEQUENTIAL_TIME=$(uv run pytest $TEST_FILES -q --tb=no 2>&1 | grep -E "passed|failed" | head -1)
SEQUENTIAL_SECONDS=$(uv run pytest $TEST_FILES -q --tb=no --durations=0 2>&1 | tail -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)

echo "Sequential: $SEQUENTIAL_TIME (${SEQUENTIAL_SECONDS}s)"
echo ""

# Parallel with different worker counts
for workers in 2 4 8 auto; do
    echo "⚡ Running with -n $workers..."
    PARALLEL_TIME=$(uv run pytest $TEST_FILES -n $workers -q --tb=no 2>&1 | grep -E "passed|failed" | head -1)
    PARALLEL_SECONDS=$(uv run pytest $TEST_FILES -n $workers -q --tb=no --durations=0 2>&1 | tail -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)

    # Calculate speedup
    if [ -n "$SEQUENTIAL_SECONDS" ] && [ -n "$PARALLEL_SECONDS" ]; then
        SPEEDUP=$(echo "scale=2; $SEQUENTIAL_SECONDS / $PARALLEL_SECONDS" | bc)
        REDUCTION=$(echo "scale=1; 100 - ($PARALLEL_SECONDS / $SEQUENTIAL_SECONDS * 100)" | bc)
        echo "  Parallel (n=$workers): $PARALLEL_TIME (${PARALLEL_SECONDS}s)"
        echo "  Speedup: ${SPEEDUP}x (${REDUCTION}% faster)"
    else
        echo "  Parallel (n=$workers): $PARALLEL_TIME"
    fi
    echo ""
done

echo "✅ Benchmark complete!"
```

Make executable:
```bash
chmod +x scripts/benchmark_parallel.sh
./scripts/benchmark_parallel.sh
```

---

## Conclusion

Parallel test execution with pytest-xdist provides significant performance improvements:

### Expected Results Summary

| Configuration | Time | vs Sequential | vs Original |
|---------------|------|---------------|-------------|
| **Original sequential** | 58.5s | - | - |
| **Optimized sequential** | 50.8s | +15% | +13% |
| **Optimized + parallel (n=4)** | ~17s | **+67%** | **+71%** |
| **Optimized + parallel (n=8)** | ~15s | **+71%** | **+74%** |

### Recommendations

1. ✅ **Install pytest-xdist:** Add to dev dependencies
2. ✅ **Use `-n auto`:** Let pytest detect optimal worker count
3. ✅ **Run parallel in CI/CD:** Use `-n 4` for consistent CI performance
4. ✅ **Combine with event-based optimization:** Best results when both applied
5. ⚠️ **Watch for state conflicts:** Isolate global state in fixtures if needed

### Next Steps

1. Install pytest-xdist: `uv add --dev pytest-xdist`
2. Run benchmark script to measure actual performance
3. Update CI/CD pipeline to use parallel execution
4. Add parallel commands to justfile/Makefile
5. Monitor for test isolation issues

**Combined with our previous optimizations, parallel execution can make the test suite 70-75% faster!** 🚀
