# make-learn 설치 가이드 (선생님용)

**make-learn**은 학습자료를 주면 수업용 게임(인터넷 없이 동작하는 웹페이지 파일)을 만들어주는 AI 도우미 기능입니다. Claude Code, ChatGPT Codex, Google Antigravity 중 **하나라도** 쓰고 계시면 설치할 수 있어요.

## 1. 파일 내려받기

1. 이 저장소(GitHub) 페이지에서 초록색 **Code** 버튼 → **Download ZIP** 클릭.
2. 내려받은 ZIP 파일의 압축을 풀어주세요. (예: 바탕화면)

## 2. 설치하기

### Windows

1. 압축 푼 폴더를 엽니다.
2. `install.ps1` 파일에 **마우스 오른쪽 클릭 → "PowerShell에서 실행"**.
   - "실행 정책" 경고가 나오면: 시작 메뉴에서 PowerShell을 열고 아래 한 줄을 붙여넣어 실행하세요.
     ```
     powershell -ExecutionPolicy Bypass -File "압축푼폴더경로\install.ps1"
     ```
3. "✅ 설치 완료!"가 나오면 끝.

### Mac

1. **터미널**을 엽니다 (Spotlight에서 "터미널" 검색).
2. `bash ` (bash와 한 칸 공백)를 입력한 뒤, 압축 푼 폴더 안의 `install.sh` 파일을 터미널 창으로 **끌어다 놓고** Enter.
3. "✅ 설치 완료!"가 나오면 끝.

## 3. 사용하기

쓰고 있는 프로그램을 **완전히 종료했다가 다시 실행**한 뒤:

| 프로그램 | 사용 방법 |
|---|---|
| **Claude Code** | 채팅창에 `/make-learn` 입력 + 학습자료(PDF·사진·텍스트) 첨부 |
| **ChatGPT Codex** | 채팅창에 `/make-learn` 입력 (스킬 목록에서 선택) + 학습자료 |
| **Google Antigravity** | Agent Manager 채팅창에 `/make-learn` 입력 + 학습자료 |

그 다음은 AI가 한국어로 몇 가지를 물어봅니다 (수업 방식, 게임 종류 등 — 4~5개 이내). 잘 모르겠으면 **"추천대로 해줘"**라고만 답하셔도 됩니다.

### 학습자료는 이런 걸 주시면 돼요
- 수업 정리 텍스트 (복사해서 붙여넣기)
- PDF 학습지·교과서 발췌
- 교과서나 학습지를 찍은 **사진**
- ⚠️ 한글(HWP)·PPT 파일은 직접 못 읽어요 → PDF로 저장하거나 내용을 복사해 붙여넣어 주세요.

## 4. 자주 묻는 질문

**Q. 게임 파일은 어떻게 학생들에게 주나요?**
완성되면 AI가 공유 방법(파일 전달, 무료 링크 만들기 등)을 함께 안내해 드려요. 게임은 인터넷 없이도 동작해서 파일만 보내도 됩니다.

**Q. 문항을 나중에 바꿀 수 있나요?**
네. 게임 파일을 메모장으로 열면 위쪽에 `✏️ 문항 수정 구역`이 있어요. 또는 AI에게 "3번 문제 바꿔줘"라고 하면 됩니다.

**Q. 업데이트는 어떻게 하나요?**
새 버전 ZIP을 받아 압축을 풀고 설치를 한 번 더 실행하면 덮어쓰기됩니다.

**Q. 삭제하려면?**
다음 폴더를 지우면 됩니다: `~/.make-learn`, `~/.claude/skills/make-learn`, `~/.codex/skills/make-learn`, `~/.gemini/antigravity/skills/make-learn` (예전 버전을 쓰셨다면 `~/.gemini/antigravity/global_workflows/make-learn.md`도 함께 삭제)
