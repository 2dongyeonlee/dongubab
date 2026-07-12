# 🔌 MCP 연동 설정 (dongubab)

용피디의 [클로드에 무조건 설치해야 하는 24가지](https://yongk.notion.site/24-13247642a71383e1b48e8169263e114a)
가이드를 기준으로, 이 프로젝트에 필요한 MCP 서버들을 `.mcp.json`에 정리했습니다.

Claude Code는 프로젝트 루트의 `.mcp.json`을 자동으로 읽습니다. 이 저장소를 열면
아래 서버들이 함께 로드됩니다. (`claude mcp list` 로 상태 확인)

---

## ✅ 이미 연결되어 있어서 여기 안 넣은 것

계정(claude.ai 커넥터) 레벨에서 이미 연결되어 있어 `.mcp.json`에 중복으로 넣지 않았습니다.

| 도구 | 상태 |
| --- | --- |
| **Notion** | 커넥터로 연결됨 (14번) |
| **Google Drive** | 커넥터로 설치됨 — 채팅에서 토글만 켜면 됨 (12번) |
| **GitHub** | 세션에 이미 연결됨 (17번) |

---

## 🔑 API 키 없이 바로 되는 것 (설치만 하면 동작)

`npx` / `uvx` 로 자동 설치됩니다. 사전에 **Node.js** 와 **uv** 만 깔려 있으면 됩니다.

| 서버 | 버킷 | 하는 일 |
| --- | --- | --- |
| `filesystem` | ① 기본 엔진 | 작업 폴더(`.`)의 파일 읽기·정리 |
| `memory` | ① 기본 엔진 | 취향·맥락·결정사항 장기 기억 |
| `sequential-thinking` | ① 기본 엔진 | 복잡한 문제를 단계별로 사고 |
| `fetch` | ② 웹·리서치 | URL 하나를 정확히 읽어오기 |
| `playwright` | ② 웹·리서치 | 진짜 브라우저로 웹 조작·QA·스크린샷 |
| `git` | ④ 개발 자동화 | 로컬 diff·커밋 기록 읽기 |
| `context7` | ④ 개발 자동화 | 최신 라이브러리 문서 실시간 공급 |
| `sqlite` | ⑤ 데이터 | 로컬 `./data.db` 분석 |

> ⚠️ `filesystem`은 **컴퓨터 전체가 아니라 이 프로젝트 폴더(`.`)만** 열도록 설정했습니다.

---

## 🔐 API 키가 필요한 것 (환경변수로 관리)

키를 **채팅창·문서에 붙여넣지 말고** 환경변수로 넣으세요. `.mcp.json`은 `${VAR}` 로
값을 읽습니다. 키가 없으면 해당 서버만 인증 실패할 뿐, 나머지는 정상 동작합니다.

| 서버 | 필요한 환경변수 | 키 발급처 |
| --- | --- | --- |
| `brave-search` | `BRAVE_API_KEY` | brave.com/search/api |
| `firecrawl` | `FIRECRAWL_API_KEY` | firecrawl.dev |
| `exa` | `EXA_API_KEY` | exa.ai |
| `perplexity` | `PERPLEXITY_API_KEY` | perplexity.ai (API) |
| `postgres` | `POSTGRES_CONNECTION_STRING` | 본인 DB 접속 문자열 |

### 환경변수 넣는 법 (예시)

```bash
# ~/.zshrc 또는 ~/.bashrc 에 추가
export BRAVE_API_KEY="..."
export FIRECRAWL_API_KEY="..."
export EXA_API_KEY="..."
export PERPLEXITY_API_KEY="..."
export POSTGRES_CONNECTION_STRING="postgresql://readonly_user:...@host:5432/db"
```

> ⚠️ `postgres`는 가이드 권고대로 **읽기 전용 계정**부터 연결하세요.

---

## 🧰 사전 준비물

1. **Node.js** — `npx` 기반 서버용
2. **uv** — `uvx` 기반 서버용 (`fetch`, `git`, `sqlite`)
3. **API 키** — 위 표의 키 필요한 서버를 쓸 경우만

설치 확인:

```bash
node -v && npx -v
uv --version
claude mcp list
```

---

## 🛡️ 보안 수칙 (가이드 요약)

1. 파일 권한은 **폴더 단위** — 프로젝트 폴더만 열기 (이미 `.` 로 제한)
2. API 키는 **환경변수로** — 채팅·문서에 그대로 붙여넣지 않기
3. GitHub 토큰은 **최소 권한**부터
4. 처음 보는 MCP는 **검증 후 설치**
5. 쓰기 권한은 **마지막에** — DB·파일시스템은 읽기 전용으로 먼저 테스트

---

*본 설정은 위 공개 가이드를 바탕으로 이 저장소에 맞게 구성한 것입니다. 패키지명·구성은
업데이트로 바뀔 수 있으니 각 GitHub 저장소에서 최신 상태를 확인하세요.*
