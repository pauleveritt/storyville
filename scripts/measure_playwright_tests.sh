#!/bin/bash
# Script to measure Playwright test performance
set -e

echo "═══════════════════════════════════════════════════════════"
echo "   Playwright Tests Performance Measurement"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test file
TEST_FILE="tests/test_playwright_integration.py"

echo -e "${BLUE}Test file:${NC} $TEST_FILE"
echo ""

# Count tests
TEST_COUNT=$(grep -c "^def test_" "$TEST_FILE" || echo "0")
echo -e "${BLUE}Total tests:${NC} $TEST_COUNT"
echo ""

# Run tests and measure time
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Running Playwright tests...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Capture start time
START_TIME=$(date +%s.%N)

# Run tests with pytest
OUTPUT=$(uv run just test "$TEST_FILE" -v --tb=short 2>&1)
EXIT_CODE=$?

# Capture end time
END_TIME=$(date +%s.%N)

# Calculate duration
DURATION=$(echo "$END_TIME - $START_TIME" | bc)

# Display output
echo "$OUTPUT"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Extract test results
PASSED=$(echo "$OUTPUT" | grep -oE "[0-9]+ passed" | grep -oE "[0-9]+" || echo "0")
FAILED=$(echo "$OUTPUT" | grep -oE "[0-9]+ failed" | grep -oE "[0-9]+" || echo "0")

echo -e "${GREEN}Tests passed:${NC} $PASSED"
if [ "$FAILED" != "0" ]; then
    echo -e "${YELLOW}Tests failed:${NC} $FAILED"
fi
echo -e "${BLUE}Duration:${NC} ${DURATION}s"
echo ""

# Extract slowest tests
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Slowest Tests (from --durations)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run again with durations to get detailed timing
uv run just test "$TEST_FILE" -q --durations=0 2>&1 | tail -20

echo ""
echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Measurement complete!${NC}"
echo "═══════════════════════════════════════════════════════════"

exit $EXIT_CODE
