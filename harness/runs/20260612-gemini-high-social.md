# Gemini CLI (Antigravity) — 실환경 테스트 기록

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-12 |
| 플랫폼 | Gemini CLI v0.10.0 (gemini-2.5-pro) |
| 스킬 설치 경로 | `gemini extensions link skill/make-learn` + `~/.gemini/antigravity/global_workflows/make-learn.md` |
| 샘플 | high-social (고1 사회 — 인권 보장과 헌법) |
| 결과 | **BLOCKED — API 할당량 초과** |

## 테스트 결과

두 차례 시도(2026-06-12 04:03 KST, 14:46 KST) 모두 첫 번째 API 호출에서 즉시 차단됨:

```
status: 429 RESOURCE_EXHAUSTED
reason: RATE_LIMIT_EXCEEDED
model: gemini-2.5-pro
"You have exhausted your capacity on this model."
```

T1~T5 검증 불가. HTML 출력 없음.

## 인프라 검증 내용 (API 독립)

테스트 실패와 무관하게 다음 설정은 완료 및 동작 확인:

| 구성 요소 | 경로 | 상태 |
|-----------|------|------|
| Gemini 확장 설정 파일 | `skill/make-learn/gemini-extension.json` | ✓ 생성 |
| Gemini CLI 확장 등록 | `gemini extensions link skill/make-learn` | ✓ 등록 확인 |
| Antigravity 전역 워크플로우 | `~/.gemini/antigravity/global_workflows/make-learn.md` | ✓ 복사 |
| install.sh 자동화 | 섹션 4 — `gemini extensions link` + Antigravity WF 복사 | ✓ 반영 |

## 다음 단계

API 할당량 초기화 후 동일 high-social 샘플로 재시도 필요 (T1~T5 전체 미검증 상태).
