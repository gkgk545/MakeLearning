# 🎮 make-learn — 학습자료로 수업용 웹앱 게임 만들기

학습자료(텍스트·PDF·사진)를 분석해 **수업용 웹앱 게임**을 만들어 주는 AI 에이전트 스킬입니다. 산출물은 인터넷 없이 파일 더블클릭만으로 동작하는 **단일 HTML 파일**이라, 교사가 별도 설치나 개발 지식 없이 바로 수업에 쓸 수 있습니다.

> 초·중·고 교사가 학습자료와 함께 "복습 게임 만들어줘", "수업용 퀴즈 게임 만들어줘"라고 요청하면 동작합니다.

## 특징

- **단일 HTML, 제로 의존** — 외부 서버·인터넷 없이 파일 더블클릭만으로 실행 (구글 폰트만 예외).
- **학습 효과 우선** — 재미는 수단, 목적은 학습. 오답 시 반드시 정답과 해설을 보여주고, 결과 화면에서 틀린 문항을 복습합니다.
- **교사 부담 최소화** — 기술 용어 없이 한국어로만 대화하고, 질문은 5개 이내(최대 7개)·모든 질문에 추천안 동봉. "추천대로 해줘" 한마디로 완성까지 진행됩니다.
- **자료 기반 출제** — 문항은 교사가 준 학습자료 안에서만 출제 (연산처럼 규칙 기반 생성이 가능한 경우는 명세서에 명시 후 승인).
- **전 교과 지원** — 국어, 수학, 사회, 과학, 영어, 실과(기술·가정), 도덕, 음악, 미술, 체육 등.
- **3가지 수업 방식** — ① TV 화면 수업(교사 조작) ② 학생 개별 접속(스마트기기) ③ 전자칠판(직접 터치).
- **3개 플랫폼** — Claude Code · ChatGPT Codex · Google Antigravity. 한 번 설치로 모두 사용.

## 설치

어떤 방법을 쓰든 Claude Code · Codex · Antigravity **세 곳에 모두** 설치됩니다.

### 방법 1 — npm (Node.js 16 이상)

```bash
npm install -g github:gkgk545/MakeLearning
```

`postinstall` 스크립트가 스킬을 각 플랫폼의 skills 폴더에 자동으로 복사합니다. 업데이트할 때도 같은 명령을 실행하면 됩니다.

### 방법 2 — 설치 스크립트

먼저 저장소를 내려받습니다. 둘 중 편한 방법으로:

```bash
# git이 있는 경우
git clone https://github.com/gkgk545/MakeLearning.git
cd MakeLearning
```

또는 GitHub 페이지에서 초록색 **Code** 버튼 → **Download ZIP**으로 받아 압축을 풀고, 그 폴더로 이동합니다.

이어서 설치 스크립트를 실행합니다:

```bash
# macOS / Linux
bash install.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File install.ps1
```

### 설치 위치

| 플랫폼 | 경로 | 호출 |
|---|---|---|
| Claude Code | `~/.claude/skills/make-learn/` | `/make-learn` |
| ChatGPT Codex | `~/.codex/skills/make-learn/` | `/make-learn` 또는 `$make-learn` |
| Google Antigravity | `~/.gemini/config/plugins/make-learn-plugin/` (plugin.json + `skills/make-learn/`) | `/make-learn` |

설치 후 사용 중인 프로그램을 **완전히 종료했다가 다시 실행**한 뒤 `/make-learn` + 학습자료를 입력하세요. 자세한 안내(비개발자용): [docs/INSTALL.md](docs/INSTALL.md)

## 사용 예시

```
/make-learn 초등 5학년 과학 "식물의 구조와 기능" 학습지를 첨부합니다.
이걸로 복습 게임 만들어줘.
```

→ 자료 분석 → 추천안 기반 인터뷰 → 명세서 승인 → 단일 HTML 게임 파일 생성·검증 후 전달.

## 7단계 제작 파이프라인

| 단계 | 내용 |
|------|------|
| 1. 입력 수집 | 학습자료 받기 (HWP·PPT는 PDF 변환 또는 붙여넣기 안내) |
| 2. 자료 분석 | 학교급·교과·핵심 개념·문항화 요소 추출 후 교사 확인 |
| 3. 순차 인터뷰 | 추천안을 붙인 질문 흐름 (5개 이내·최대 7개) |
| 4. 설계 계획 | 게임 명세서 작성 → 교사 승인 |
| 5. 제작 | 디자인 가이드 + 선택 패턴 준수, 단일 HTML 생성 |
| 6. 검증 | 검증 루브릭 전 항목 점검, 불합격 시 수정 후 재검증 |
| 7. 반환 | 파일 + 사용법 + 공유 방법 안내 |

## 지원 게임 유형 (7종 + 자유 설계)

`skill/make-learn/core/game-patterns/`에 7가지 게임 유형이 정의되어 있으며, 자료 성격에 맞는 패턴을 선택하거나 자유 설계합니다.

| 유형 | 패턴 파일 | 어울리는 내용 |
|---|---|---|
| 골든벨 퀴즈 | `01-quiz.md` | 개념 확인 전반 (가장 범용) |
| 카드 짝맞추기 | `02-matching.md` | 용어-뜻, 단어-의미, 기호-이름 |
| 분류·정렬 | `03-sorting.md` | 범주 나누기, 순서·과정 |
| 스피드 챌린지 | `04-speed.md` | 연산·어휘 숙달 훈련 |
| 팀 대항 점수판 | `05-team-battle.md` | 단원 마무리 모둠 대항전 (TV·전자칠판) |
| 낱말·빈칸 채우기 | `06-word.md` | 핵심 용어·표현 암기 |
| 말판 보드게임 | `07-board.md` | 놀이성 있는 모둠 복습 |

## 저장소 구조

```
make-learn/
├── skill/make-learn/             # 스킬 본체 — 단일 진실 공급원
│   ├── SKILL.md                  #   스킬 진입점 (7단계 요약 + 절대 규칙)
│   └── core/
│       ├── make-learn-core.md    #   7단계 파이프라인 본체 지침
│       ├── interview-guide.md    #   3단계 인터뷰 질문 흐름
│       ├── design-guide.md       #   5단계 제작 규칙(단일 파일·학교급별 톤 등)
│       ├── verify-rubric.md      #   6단계 검증 루브릭
│       ├── share-guide.md        #   7단계 공유·문항 수정 안내
│       └── game-patterns/        #   게임 유형별 화면 흐름·데이터 스키마 (7종)
├── harness/                      # 품질 검증 하네스 (교과별 샘플 6종, 합격 기준, 테스트 절차)
├── docs/INSTALL.md               # 선생님용 설치 가이드
├── install.sh / install.ps1      # 설치 스크립트 (macOS·Linux / Windows)
└── scripts/install.js            # npm postinstall 스크립트
```

## 절대 규칙

- 모든 대화는 한국어, 교사에게 기술 용어를 쓰지 않습니다.
- 문항은 학습자료 안에서만 출제합니다.
- 오답 피드백에는 반드시 정답과 해설을 포함합니다.
- 산출물은 외부 의존 없는 단일 HTML — 더블클릭만으로 동작해야 합니다.
- 검증(6단계)을 통과하기 전에는 완성을 선언하지 않습니다.

## 개발·기여

- 스킬 지침 수정 시: `skill/make-learn/core/`가 단일 진실 공급원입니다. 수정 후 `harness/test-protocol.md` 절차로 회귀 확인을 해주세요.
- 게임 품질 기준: `skill/make-learn/core/verify-rubric.md` + `harness/acceptance.md`
