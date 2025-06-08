#!/bin/bash
#
# validate-gu-integration.sh
# 
# Simple validation script to check that Geometric Unity atom types
# have been properly added to the atom_types.script file.
#

echo "Validating Geometric Unity integration in AtomSpace..."
echo "======================================================="

ATOM_TYPES_FILE="opencog/atoms/atom_types/atom_types.script"

if [ ! -f "$ATOM_TYPES_FILE" ]; then
    echo "ERROR: atom_types.script file not found!"
    exit 1
fi

echo "Checking for Geometric Unity atom types..."

# Check for geometric objects
echo -n "  Geometric objects: "
if grep -q "SPACETIME_MANIFOLD\|GAUGE_BUNDLE\|SPINOR_BUNDLE" "$ATOM_TYPES_FILE"; then
    echo "✓ Found"
else
    echo "✗ Missing"
    exit 1
fi

# Check for physical fields  
echo -n "  Physical fields: "
if grep -q "EINSTEIN_TENSOR_FIELD\|YANG_MILLS_FIELD\|DIRAC_SPINOR_FIELD" "$ATOM_TYPES_FILE"; then
    echo "✓ Found"
else
    echo "✗ Missing"
    exit 1
fi

# Check for mathematical operations
echo -n "  Mathematical operations: "
if grep -q "COVARIANT_DERIVATIVE\|FIELD_STRENGTH\|EINSTEIN_HILBERT_ACTION" "$ATOM_TYPES_FILE"; then
    echo "✓ Found"
else
    echo "✗ Missing"
    exit 1
fi

# Check for unification links
echo -n "  Unification links: "
if grep -q "GEOMETRIC_UNITY_LINK\|UNIFIED_FIELD_LINK" "$ATOM_TYPES_FILE"; then
    echo "✓ Found"
else
    echo "✗ Missing"
    exit 1
fi

echo ""
echo "Checking example file..."
if [ -f "examples/atomspace/geometric-unity.scm" ]; then
    echo "  ✓ geometric-unity.scm example found"
    lines=$(wc -l < "examples/atomspace/geometric-unity.scm")
    echo "    ($lines lines of Scheme code)"
else
    echo "  ✗ geometric-unity.scm example missing"
    exit 1
fi

echo ""
echo "Checking test file..."
if [ -f "tests/query/GeometricUnityUTest.cxxtest" ]; then
    echo "  ✓ GeometricUnityUTest.cxxtest found"
    lines=$(wc -l < "tests/query/GeometricUnityUTest.cxxtest")
    echo "    ($lines lines of C++ test code)"
else
    echo "  ✗ GeometricUnityUTest.cxxtest missing"
    exit 1
fi

echo ""
echo "Checking documentation..."
if [ -f "doc/geometric-unity.md" ]; then
    echo "  ✓ geometric-unity.md documentation found"
    lines=$(wc -l < "doc/geometric-unity.md")
    echo "    ($lines lines of documentation)"
else
    echo "  ✗ geometric-unity.md documentation missing"
    exit 1
fi

echo ""
echo "Validating inheritance hierarchy..."
echo -n "  Checking geometric object inheritance: "
if grep -A 5 -B 5 "GEOMETRIC_OBJECT.*<-.*LINK" "$ATOM_TYPES_FILE" | grep -q "MANIFOLD.*<-.*GEOMETRIC_OBJECT"; then
    echo "✓ Valid"
else
    echo "✗ Invalid"
    exit 1
fi

echo -n "  Checking field node inheritance: "
if grep -A 5 -B 5 "FIELD_NODE.*<-.*NODE" "$ATOM_TYPES_FILE" | grep -q "EINSTEIN_TENSOR_FIELD.*<-.*FIELD_NODE"; then
    echo "✓ Valid"
else
    echo "✗ Invalid"
    exit 1
fi

echo -n "  Checking operation inheritance: "
if grep -A 5 -B 5 "GU_OPERATION.*<-.*FUNCTION_LINK" "$ATOM_TYPES_FILE" | grep -q "COVARIANT_DERIVATIVE.*<-.*GU_OPERATION"; then
    echo "✓ Valid"
else
    echo "✗ Invalid"
    exit 1
fi

echo ""
echo "Counting new atom types..."
gu_types=$(grep -c "SPACETIME_MANIFOLD\|GAUGE_BUNDLE\|SPINOR_BUNDLE\|EINSTEIN_TENSOR_FIELD\|YANG_MILLS_FIELD\|DIRAC_SPINOR_FIELD\|METRIC_FIELD\|CURVATURE_FIELD\|COVARIANT_DERIVATIVE\|FIELD_STRENGTH\|EINSTEIN_HILBERT_ACTION\|YANG_MILLS_ACTION\|DIRAC_ACTION\|GEOMETRIC_UNITY_LINK\|UNIFIED_FIELD_LINK" "$ATOM_TYPES_FILE")
echo "  Total GU atom types added: $gu_types"

if [ "$gu_types" -ge 15 ]; then
    echo "  ✓ Sufficient atom types for complete GU representation"
else
    echo "  ✗ Insufficient atom types (need at least 15)"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Geometric Unity integration validated!"
echo "=========================================="
echo ""
echo "The AtomSpace now supports representation of:"
echo "  • Spacetime manifolds and fiber bundles"
echo "  • Einstein, Yang-Mills, and Dirac fields"  
echo "  • Geometric operations and action functionals"
echo "  • Unified field theory structures"
echo ""
echo "See examples/atomspace/geometric-unity.scm for usage examples."
echo "Run tests with: make GeometricUnityUTest (after building)"