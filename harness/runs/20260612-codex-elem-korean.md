# Codex CLI — 실환경 테스트 기록

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-12 |
| 플랫폼 | Codex CLI v0.139.0 (gpt-5.5) |
| 스킬 설치 경로 | `~/.codex/skills/make-learn/` |
| 샘플 | elem-korean (초등 3학년 국어 — 맞춤법) |
| 생성 패턴 | 11 표적 사냥 |
| 결과 | **합격** |

## T1 — 스킬 인식

- `/make-learn` 호출 → `SKILL.md` 즉시 로드 ✓
- 7단계 파이프라인 진입 확인 ✓

## T2 — 핵심 문서 접근

- `make-learn-core.md` 읽음 ✓
- `interview-guide.md` 읽음 ✓
- `design-guide.md` 읽음 ✓
- `game-patterns/11-target.md` 읽음 ✓

## T3 — 파이프라인 준수

- 자료 분석 → 패턴 선택(표적 사냥) → 설계 가이드 적용 순서 확인 ✓
- 인터뷰 추천 방식 자동 적용 ✓

## T4 — HTML 출력

- 파일: `/tmp/codex-test2/game-output.html`
- 제목: **맞춤법 표적 사냥** (초등 3학년 국어)
- 줄 수: 791줄
- `const GAME_DATA`: ✓
- `window.onerror`: ✓
- `<script>` 블록 3개 (3-스크립트 패턴): ✓

## T5 — 인수 기준 (P1~P5)

| 기준 | 결과 | 비고 |
|------|------|------|
| P1 JS 문법 | **PASS** | `node --check` 오류 0건 |
| P2 외부 URL | **PASS** | `www.w3.org/2000/svg` 는 SVG 네임스페이스 속성값(HTTP 요청 아님) |
| P3 브라우저 실행 | **PASS** | 콘솔 오류 0건; 시작 버튼→게임 진입(1/5 라운드, 28초 타이머) 확인; result_reached=True |
| P4 레이아웃 | **PASS** | 390px 카드 레이아웃 정상; 1280px 중앙 배치 이상 없음 |
| P5 줄 수 | **PASS** | 791줄 (허용 범위 600~1200) |

## 실행 조건 메모

- `codex exec` 는 신뢰된 git 저장소 안에서 실행해야 함 (외부 실행 시 "Not inside a trusted directory" 오류)
- 180초 타임아웃은 HTML 전체 생성에 부족 — **360초 이상 권장**
- `--sandbox-permissions disk-full-read-access,disk-full-write-access,network-full-access` 필요
