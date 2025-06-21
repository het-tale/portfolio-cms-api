#!/usr/bin/env bash

# Paths to check
MODEL_FILES=$(git diff --cached --name-only | grep -E 'app/models/.*\.py$|.*sqlmodel.*\.py$')

# Alembic migration folder
MIGRATION_FILES=$(git diff --cached --name-only | grep -E 'alembic/versions/.*\.py$')

if [ -n "$MODEL_FILES" ] && [ -z "$MIGRATION_FILES" ]; then
  echo "❌ Model files changed but no Alembic migration staged."
  echo "💡 Run: alembic revision --autogenerate -m 'your message'"
  exit 1
fi

echo "✅ Alembic check passed"
exit 0
