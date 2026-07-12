#!/usr/bin/env bash
#
# 모든 프로젝트에서 쓸 수 있게 MCP 서버를 유저 스코프(전역)로 설치합니다.
# 내 컴퓨터에서 한 번만 실행하면 됩니다:  bash install-mcp.sh
#
# 요구사항: Claude Code CLI, Node.js(npx), uv(uvx)
# 확인:  claude --version && node -v && uv --version
#
# 설치 후 확인:  claude mcp list
# 삭제:         claude mcp remove <이름> --scope user

set -euo pipefail

SCOPE="--scope user"

echo "▶ 유저 스코프(전역)로 MCP 서버 설치 중..."

add() {
  local name="$1"; local json="$2"
  echo "  • $name"
  # 이미 있으면 지우고 다시 추가 (idempotent)
  claude mcp remove "$name" --scope user >/dev/null 2>&1 || true
  claude mcp add-json "$name" "$json" $SCOPE
}

# ── 🔑 키 없이 바로 동작 ─────────────────────────────
add filesystem          '{"command":"npx","args":["-y","@modelcontextprotocol/server-filesystem","'"$HOME"'"]}'
add memory              '{"command":"npx","args":["-y","@modelcontextprotocol/server-memory"]}'
add sequential-thinking '{"command":"npx","args":["-y","@modelcontextprotocol/server-sequential-thinking"]}'
add fetch               '{"command":"uvx","args":["mcp-server-fetch"]}'
add git                 '{"command":"uvx","args":["mcp-server-git"]}'
add playwright          '{"command":"npx","args":["-y","@playwright/mcp@latest"]}'
add context7            '{"command":"npx","args":["-y","@upstash/context7-mcp"]}'

# ── 🔐 API 키 필요 (환경변수에서 읽음) ────────────────
# 키가 없으면 해당 서버만 인증 실패할 뿐, 나머지는 정상 동작합니다.
add brave-search '{"command":"npx","args":["-y","@brave/brave-search-mcp-server"],"env":{"BRAVE_API_KEY":"'"${BRAVE_API_KEY:-}"'"}}'
add firecrawl    '{"command":"npx","args":["-y","firecrawl-mcp"],"env":{"FIRECRAWL_API_KEY":"'"${FIRECRAWL_API_KEY:-}"'"}}'
add exa          '{"command":"npx","args":["-y","exa-mcp-server"],"env":{"EXA_API_KEY":"'"${EXA_API_KEY:-}"'"}}'
add perplexity   '{"command":"npx","args":["-y","server-perplexity-ask"],"env":{"PERPLEXITY_API_KEY":"'"${PERPLEXITY_API_KEY:-}"'"}}'

if [ -n "${POSTGRES_CONNECTION_STRING:-}" ]; then
  add postgres "{\"command\":\"npx\",\"args\":[\"-y\",\"@modelcontextprotocol/server-postgres\",\"${POSTGRES_CONNECTION_STRING}\"]}"
else
  echo "  • postgres  (건너뜀 — POSTGRES_CONNECTION_STRING 미설정)"
fi

echo ""
echo "✅ 완료. 확인:  claude mcp list"
echo "   Notion / Google Drive / GitHub 은 계정 커넥터로 이미 연결되어 있어 제외했습니다."
