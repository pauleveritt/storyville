#!/bin/bash
# Benchmark script for comparing sequential vs parallel pytest execution
set -e

echo "═══════════════════════════════════════════════════════════"
echo "   Pytest Parallel Execution Benchmark"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if pytest-xdist is available
echo "Checking dependencies..."
if ! uv run python -c "import xdist" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  pytest-xdist not installed.${NC}"
    echo "Install with: uv add --dev pytest-xdist"
    echo ""
    echo "Skipping parallel tests..."
    SKIP_PARALLEL=1
else
    echo -e "${GREEN}✓ pytest-xdist is installed${NC}"
    SKIP_PARALLEL=0
fi
echo ""

# Test files to benchmark
TEST_FILES="tests/test_watchers.py tests/test_hotreload_integration.py"

echo -e "${BLUE}Test files:${NC} $TEST_FILES"
echo ""

# Function to extract timing from pytest output
extract_time() {
    # Try to extract from "X passed in Y.YYs" format
    echo "$1" | grep -oE '[0-9]+\.[0-9]+s' | head -1 | tr -d 's'
}

# Sequential baseline
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔄 Running SEQUENTIAL (baseline)...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SEQUENTIAL_OUTPUT=$(uv run pytest $TEST_FILES -q --tb=no 2>&1)
SEQUENTIAL_TIME=$(extract_time "$SEQUENTIAL_OUTPUT")

if [ -n "$SEQUENTIAL_TIME" ]; then
    echo -e "${GREEN}✓ Sequential:${NC} ${SEQUENTIAL_TIME}s"
    echo "$SEQUENTIAL_OUTPUT" | grep -E "passed|failed" | head -1
else
    echo -e "${RED}✗ Failed to extract timing${NC}"
    echo "$SEQUENTIAL_OUTPUT"
    exit 1
fi
echo ""

# Exit if parallel is not available
if [ "$SKIP_PARALLEL" -eq 1 ]; then
    echo "Benchmark complete (sequential only)"
    exit 0
fi

# Parallel with different worker counts
declare -a WORKERS=("2" "4" "8" "auto")
declare -a PARALLEL_TIMES=()

for workers in "${WORKERS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}⚡ Running PARALLEL with -n $workers...${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    PARALLEL_OUTPUT=$(uv run pytest $TEST_FILES -n $workers -q --tb=no 2>&1)
    PARALLEL_TIME=$(extract_time "$PARALLEL_OUTPUT")

    if [ -n "$PARALLEL_TIME" ]; then
        PARALLEL_TIMES+=("$PARALLEL_TIME")

        # Calculate speedup and reduction
        SPEEDUP=$(echo "scale=2; $SEQUENTIAL_TIME / $PARALLEL_TIME" | bc)
        REDUCTION=$(echo "scale=1; 100 - ($PARALLEL_TIME / $SEQUENTIAL_TIME * 100)" | bc)

        echo -e "${GREEN}✓ Parallel (n=$workers):${NC} ${PARALLEL_TIME}s"
        echo "$PARALLEL_OUTPUT" | grep -E "passed|failed" | head -1
        echo -e "${YELLOW}  → Speedup: ${SPEEDUP}x (${REDUCTION}% faster)${NC}"
    else
        echo -e "${RED}✗ Failed to extract timing${NC}"
        echo "$PARALLEL_OUTPUT"
    fi
    echo ""
done

# Summary table
echo "═══════════════════════════════════════════════════════════"
echo "   Summary"
echo "═══════════════════════════════════════════════════════════"
echo ""
printf "%-25s %-12s %-12s %-12s\n" "Configuration" "Time" "Speedup" "Improvement"
echo "───────────────────────────────────────────────────────────"
printf "%-25s %-12s %-12s %-12s\n" "Sequential (baseline)" "${SEQUENTIAL_TIME}s" "1.00x" "-"

idx=0
for workers in "${WORKERS[@]}"; do
    if [ -n "${PARALLEL_TIMES[$idx]}" ]; then
        PARALLEL_TIME="${PARALLEL_TIMES[$idx]}"
        SPEEDUP=$(echo "scale=2; $SEQUENTIAL_TIME / $PARALLEL_TIME" | bc)
        REDUCTION=$(echo "scale=1; 100 - ($PARALLEL_TIME / $SEQUENTIAL_TIME * 100)" | bc)
        printf "%-25s %-12s %-12s %-12s\n" "Parallel (n=$workers)" "${PARALLEL_TIME}s" "${SPEEDUP}x" "${REDUCTION}%"
    fi
    idx=$((idx + 1))
done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Benchmark complete!${NC}"
echo "═══════════════════════════════════════════════════════════"
