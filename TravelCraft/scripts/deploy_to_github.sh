#!/usr/bin/env bash
# TravelCraft v2.3 — Deploy trip directory to GitHub + GitHub Pages
# Usage: deploy_to_github.sh <trip-dir> <slug> <github-user> <github-repo>
# Env:   GH_TOKEN (Personal Access Token with `repo` scope)
# Output: GitHub Pages URL on stdout
#
# Strategy:
#   - Clone existing repo to a temp workspace
#   - Copy trip-dir to trips/<slug>/
#   - Commit + push
#   - Auto-enable GitHub Pages (source = main branch, root) if not already
#   - Return https://<user>.github.io/<repo>/trips/<slug>/

set -euo pipefail

TRIP_DIR="${1:?missing trip directory}"
SLUG="${2:?missing slug}"
GH_USER="${3:?missing GitHub user}"
GH_REPO="${4:?missing GitHub repo}"

if [[ -z "${GH_TOKEN:-}" ]]; then
  cat >&2 <<EOF
[deploy_to_github] ERROR: GH_TOKEN environment variable not set.
Create one at: https://github.com/settings/tokens/new
  - Note: TravelCraft Deploy
  - Scopes: [x] repo
Then export it:
  export GH_TOKEN=ghp_xxxxxxxxxxxx
EOF
  exit 1
fi

WORK_DIR="/tmp/tc-gh-deploy-$$"
mkdir -p "$WORK_DIR"
trap "rm -rf '$WORK_DIR'" EXIT

REPO_URL="https://${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git"

echo "[deploy_to_github] cloning $GH_USER/$GH_REPO..." >&2
if ! git clone "$REPO_URL" "$WORK_DIR" 2>&1 >&2; then
  cat >&2 <<EOF
[deploy_to_github] clone failed. Common causes:
  1. Repo doesn't exist — create it at https://github.com/new
  2. Token doesn't have 'repo' scope
  3. Repo is owned by another org (use org/repo format)
EOF
  exit 2
fi

# Copy trip contents to trips/<slug>/
DEST="$WORK_DIR/trips/$SLUG"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$TRIP_DIR"/. "$DEST/"

# Don't commit intermediate / large files
find "$DEST" -name "_*" -delete 2>/dev/null || true
find "$DEST" -name ".env" -delete 2>/dev/null || true
find "$DEST" -name "vercel.json" -delete 2>/dev/null || true

cd "$WORK_DIR"
git config user.email "travelcraft@localhost"
git config user.name "TravelCraft"
git add -A

if git diff --cached --quiet; then
  echo "[deploy_to_github] no changes to commit" >&2
else
  git commit -m "Deploy $SLUG ($(date +%Y-%m-%d))" >&2
  echo "[deploy_to_github] pushing..." >&2
  git push origin main 2>&1 >&2
fi

# Enable GitHub Pages (idempotent; returns 201 on create, 409 if already enabled)
echo "[deploy_to_github] ensuring GitHub Pages is enabled..." >&2
HTTP_CODE=$(curl -sX POST \
  -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$GH_USER/$GH_REPO/pages" \
  -d '{"source":{"branch":"main","path":"/"}}')
case "$HTTP_CODE" in
  201) echo "[deploy_to_github] ✓ Pages enabled" >&2 ;;
  409) echo "[deploy_to_github] ✓ Pages already enabled" >&2 ;;
  *)   echo "[deploy_to_github] WARN: Pages API returned $HTTP_CODE (continuing anyway)" >&2 ;;
esac

URL="https://${GH_USER}.github.io/${GH_REPO}/trips/${SLUG}/"
echo "[deploy_to_github] ✓ done. URL will be live in 1-2 min:" >&2
echo "$URL"
