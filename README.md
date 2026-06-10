# 🎮 make-learn — 학습자료로 수업용 웹앱 게임 만들기

초·중·고 선생님이 **학습자료(텍스트·PDF·사진)를 주면, 수업에서 바로 쓸 수 있는 복습 게임(단일 HTML)을 만들어주는** AI 에이전트 스킬입니다.

- **전 교과 지원**: 국어, 수학, 사회, 과학, 영어, 실과(기술·가정), 도덕, 음악, 미술, 체육 등
- **3가지 수업 방식**: ① TV 화면 수업(교사 조작) ② 학생 개별 접속(스마트기기) ③ 전자칠판(직접 터치)
- **3개 플랫폼**: Claude Code · ChatGPT Codex · Google Antigravity — 한 번 설치로 모두 사용
- **어디서나 동작**: 생성된 게임은 인터넷 없이 파일 더블클릭만으로 실행 (외부 의존성 없음, 서버 불필요)
- **학습 효과 우선**: 모든 게임은 오답 시 정답+해설을 보여주고, 결과 화면에서 틀린 문항을 복습

## 빠른 시작

```bash
# macOS / Linux
bash install.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File install.ps1
```

설치 후 사용 중인 프로그램을 재시작하고 `/make-learn` + 학습자료를 입력하세요. 자세한 안내(비개발자용): [docs/INSTALL.md](docs/INSTALL.md)

## 동작 방식 (7단계)

1. 학습자료 입력 → 2. 자료 분석(학교급·교과·핵심 개념) → 3. 짧은 인터뷰(질문 5개 이내, "추천대로 해줘" 가능) → 4. 게임 명세서 승인 → 5. 제작 → 6. 완성도 검증(정답 전수 대조·동작·기기 대응) → 7. 게임 파일 + 사용법·공유 안내 반환

## 지원 게임 유형 (7종 + 자유 설계)

| 유형 | 어울리는 내용 |
|---|---|
| 골든벨 퀴즈 | 개념 확인 전반 (가장 범용) |
| 카드 짝맞추기 | 용어-뜻, 단어-의미, 기호-이름 |
| 분류·정렬 | 범주 나누기, 순서·과정 |
| 스피드 챌린지 | 연산·어휘 숙달 훈련 |
| 팀 대항 점수판 | 단원 마무리 모둠 대항전 (TV·전자칠판) |
| 낱말·빈칸 채우기 | 핵심 용어·표현 암기 |
| 말판 보드게임 | 놀이성 있는 모둠 복습 |

## 저장소 구조

```
skill/make-learn/     스킬 본체 (SKILL.md + core 지침·게임 패턴 7종)
adapters/antigravity/ Antigravity 전역 워크플로우
harness/              품질 검증 하네스 (교과별 샘플 자료 6종, 합격 기준, 테스트 절차)
docs/INSTALL.md       선생님용 설치 가이드
install.sh / .ps1     설치 스크립트 (Claude·Codex·Antigravity 동시 설치)
PLAN.md               설계 결정 기록
```

## 개발·기여

- 스킬 지침 수정 시: `skill/make-learn/core/`가 단일 진실 공급원입니다. 수정 후 `harness/test-protocol.md` 절차로 회귀 확인을 해주세요.
- 게임 품질 기준: `skill/make-learn/core/verify-rubric.md` + `harness/acceptance.md`
- `reference/kingmath`는 설계 패턴 참고용입니다 (CC BY-NC 4.0 — 코드 직접 복사 금지, 본 스킬은 패턴만 학습해 자체 템플릿 사용).
