#!/usr/bin/env bash
# make-learn 스킬 설치 스크립트 (macOS / Linux)
# 사용법: 터미널에서  bash install.sh
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SRC_DIR/skill/make-learn"

if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
  echo "❌ skill/make-learn/SKILL.md 를 찾을 수 없어요. 압축을 풀거나 클론한 폴더 안에서 실행해 주세요."
  exit 1
fi

echo "📦 make-learn 스킬을 설치합니다..."
installed=()

# 1) 공용 본체
mkdir -p "$HOME/.make-learn"
cp -R "$SKILL_SRC/." "$HOME/.make-learn/"
installed+=("공용 본체        → ~/.make-learn/")

# 2) Claude Code
mkdir -p "$HOME/.claude/skills/make-learn"
cp -R "$SKILL_SRC/." "$HOME/.claude/skills/make-learn/"
installed+=("Claude Code      → ~/.claude/skills/make-learn/  (호출: /make-learn)")

# 3) Codex (있을 때만 안내가 달라질 뿐, 폴더는 항상 생성해도 무해)
mkdir -p "$HOME/.codex/skills/make-learn"
cp -R "$SKILL_SRC/." "$HOME/.codex/skills/make-learn/"
installed+=("Codex            → ~/.codex/skills/make-learn/   (호출: /make-learn 또는 \$make-learn)")

# 4) Gemini CLI 확장 (Antigravity 포함)
#    gemini-extension.json 이 있는 폴더를 `gemini extensions link` 로 등록한다.
#    Antigravity 전역 워크플로우는 ~/.gemini/antigravity/global_workflows/ 에 복사한다.
AGYW_DIR="$HOME/.gemini/antigravity/global_workflows"
mkdir -p "$AGYW_DIR"
cp "$SRC_DIR/adapters/antigravity/make-learn.md" "$AGYW_DIR/make-learn.md"
# Gemini CLI 확장 등록 (gemini CLI 가 있을 때만)
if command -v gemini &>/dev/null; then
  echo "Y" | gemini extensions link "$SKILL_SRC" 2>/dev/null && \
    installed+=("Gemini CLI 확장  → $(gemini extensions list 2>/dev/null | grep make-learn | head -1 | awk '{print $3}')  (호출: /make-learn)") || \
    installed+=("Gemini CLI 확장  → 수동 등록 필요: gemini extensions link $(pwd)/skill/make-learn")
else
  installed+=("Gemini CLI 확장  → gemini CLI 없음 — 설치 후 gemini extensions link skill/make-learn 실행")
fi
installed+=("Antigravity WF   → $AGYW_DIR/make-learn.md  (호출: /make-learn)")

echo ""
echo "✅ 설치 완료!"
for line in "${installed[@]}"; do echo "   $line"; done
echo ""
echo "사용 중인 프로그램(Claude Code / Codex / Antigravity)을 다시 시작한 뒤,"
echo "채팅창에 /make-learn 을 입력하고 학습자료를 함께 올려보세요."
