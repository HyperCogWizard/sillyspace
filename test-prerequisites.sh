#!/bin/bash
#
# Test script to verify prerequisite installation
#

set -e

echo "Testing AtomSpace Prerequisites Installation"
echo "============================================="

# Test cmake
echo -n "Testing cmake... "
if cmake --version >/dev/null 2>&1; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test guile
echo -n "Testing guile... "
if guile --version >/dev/null 2>&1; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test cxxtest
echo -n "Testing cxxtest... "
if cxxtestgen --version >/dev/null 2>&1; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test cogutil
echo -n "Testing cogutil... "
if pkg-config --exists cogutil 2>/dev/null || [ -f "/usr/local/lib/cmake/CogUtil/CogUtilConfig.cmake" ]; then
    echo "✓ PASSED"
else
    echo "✗ FAILED"
    exit 1
fi

# Test cmake configuration
echo -n "Testing AtomSpace cmake configuration... "
cd "$(dirname "$0")"
rm -rf test_build
mkdir test_build
cd test_build
if cmake .. >/dev/null 2>&1; then
    echo "✓ PASSED"
    cd ..
    rm -rf test_build
else
    echo "✗ FAILED"
    cd ..
    rm -rf test_build
    exit 1
fi

echo ""
echo "All prerequisite tests passed! ✓"
echo "The AtomSpace prerequisites are correctly installed."
echo ""
echo "Note: Full build may still have issues due to atom type generation"
echo "bugs unrelated to prerequisites."