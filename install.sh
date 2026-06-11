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

# 4) Antigravity (Gemini) 플러그인
#    ~/.gemini/config/plugins/<플러그인>/ 아래에서 로드되므로, plugin.json 으로 등록하고
#    스킬은 skills/<스킬>/ 하위에 둔다. plugin.json 은 반드시 BOM 없는 표준 UTF-8 로 기록한다.
PLUGIN_ROOT="$HOME/.gemini/config/plugins/make-learn-plugin"
mkdir -p "$PLUGIN_ROOT/skills/make-learn"
cp -R "$SKILL_SRC/." "$PLUGIN_ROOT/skills/make-learn/"
# heredoc 으로 직접 기록 → BOM 없음
cat > "$PLUGIN_ROOT/plugin.json" <<'JSON'
{
  "name": "make-learn-plugin",
  "version": "1.0.0",
  "description": "학습자료로 수업용 웹앱 게임을 만들어 주는 make-learn 스킬",
  "author": "gkgk545"
}
JSON
installed+=("Antigravity      → $PLUGIN_ROOT/  (plugin.json + skills/make-learn, 호출: /make-learn)")

echo ""
echo "✅ 설치 완료!"
for line in "${installed[@]}"; do echo "   $line"; done
echo ""
echo "사용 중인 프로그램(Claude Code / Codex / Antigravity)을 다시 시작한 뒤,"
echo "채팅창에 /make-learn 을 입력하고 학습자료를 함께 올려보세요."
