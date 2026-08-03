# CLAUDE.md — 인스타 맛집 릴스 콘텐츠
## 계정 정보
- 맛집/노포/바 리뷰 릴스 계정. 목표: 게시물당 조회수 극대화. 협찬 진행함

## 검증된 스타일 공식 v1.0 (/log 실데이터 기반)
[통념 깨는 가격·룰] × [숨은 아지트 발견 서사] × [반말 혼잣말 톤] × [같이 갈 사람 소환]
- 커버 훅: 지역 + 가격파괴/특이한 룰을 반드시 커버에 명시
  (검증: "만원 안주 오마카세" → 14.2만 조회, 평균 7초)
- 캡션 첫 줄: 정보격차 FOMO ("직장인들 다 알고 있었던", "나만 알고 싶었는데")
- 가게의 특이한 룰/시스템이 최우선 소재 (만원 오마카세, 6시반 전 1+1, 외부음식 허용)
- 공간 반전 + 노포 디테일 구체 묘사 ("여기 서울 맞나", "전구색 불빛에 바랜 간판")
- 마무리: 희소성/재방문 보증 ("한번만 가본 사람은 없을걸...?")
- 톤: 반말 혼잣말, ",,," "•••" 사용. 광고 문체 금지
- 정보 블록: 📍상호 ⏰영업시간 🚨휴무 (저장 유도)
- 지표 우선순위: 공유 > 저장 > 좋아요 (소환형 콘텐츠가 계정의 무기)

## 안티패턴 (하지 말 것 — /log/002에서 검증)
- "추천 OO바" 같은 일반 워딩 커버 금지 → 건너뛰기 58.9% 유발
- 킬러 소재(특이 룰·가격)를 캡션에만 두고 커버에서 빼는 실수 금지
- 첫 3초에 반전 없으면 평균 조회시간 반토막 (7초 vs 4초 실측)

## 협찬 규칙
- 가이드라인 필수 요소 100% 반영하되 훅에는 광고 냄새 금지
- 훅은 시청자 이득/호기심, 필수 요소는 중후반 배치
- 산출 마지막에 가이드라인 반영 체크리스트 첨부

## 산출물 규칙 (기획 요청 시 항상 이 순서)
1. 훅 3안 → 추천 1개와 이유 (킬러 소재가 커버에 있는지 자가검증)
2. 타임코드 대본 (15~30초, 컷 2~4초, 자막 문안)
3. 캡션 (첫줄 후킹 → 서사 → 정보블록)
4. 해시태그 (지역3 + 음식3 + 광역2)
5. /log 상위 게시물의 훅 유형·문장 호흡 우선 참고

---

# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
