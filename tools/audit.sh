#!/usr/bin/env bash
# Audit connectors/ for anything that looks like an embedded secret.
# Run from the repo root: tools/audit.sh
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

# 1. Suspicious assignments: key/secret/token/password with a literal value.
if grep -rEni '(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*["'\''][^"'\'' ]+["'\'']' connectors/ ; then
  echo "FAIL: possible embedded secret above"
  fail=1
fi

# 2. Common token prefixes accidentally committed.
if grep -rEn 'xox[baprs]-|ghp_|gho_|sk-live-|rk-live-|AKIA[0-9A-Z]{16}' connectors/ ; then
  echo "FAIL: possible real credential above"
  fail=1
fi

# 3. Private key material.
if grep -rEl 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY' connectors/ ; then
  echo "FAIL: private key material above"
  fail=1
fi

# 4. Every SKILL.md must have a Files manifest (the install audit boundary).
while IFS= read -r f; do
  if ! grep -q '^## Files' "$f"; then
    echo "FAIL: $f has no ## Files manifest"
    fail=1
  fi
done < <(find connectors -name SKILL.md)

if [ "$fail" -eq 0 ]; then
  echo "audit clean"
fi
exit "$fail"
