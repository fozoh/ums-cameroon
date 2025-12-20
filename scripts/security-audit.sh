#!/bin/bash

# Security audit script - runs npm audit and checks for hardcoded secrets

set -e

echo "🔒 Running Security Audit..."
echo ""

# npm audit
echo "1️⃣  Checking npm dependencies (frontend)..."
cd frontend
npm audit --audit-level=moderate || exit 1
cd ..

# Secrets detection
echo ""
echo "2️⃣  Scanning for hardcoded secrets..."

# Check for common patterns
patterns=(
  "password.*="
  "api.key.*="
  "secret.*="
  "token.*="
  "aws.secret"
  "private.key"
)

found=0
for pattern in "${patterns[@]}"; do
  if grep -r --include="*.py" --include="*.js" --include="*.jsx" \
           --exclude-dir=node_modules --exclude-dir=.venv \
           -i "$pattern" . 2>/dev/null | grep -v "\.env.example"; then
    found=$((found + 1))
  fi
done

if [ $found -gt 0 ]; then
  echo "⚠️  WARNING: Found ${found} potential hardcoded secrets. Please review!"
  exit 1
else
  echo "✓ No hardcoded secrets detected"
fi

echo ""
echo "✓ Security audit passed!"
