# make-learn 스킬 설치 스크립트 (Windows PowerShell)
# 사용법: 폴더에서 마우스 오른쪽 클릭 → 'PowerShell에서 실행'
#        또는 PowerShell에서  powershell -ExecutionPolicy Bypass -File install.ps1
$ErrorActionPreference = "Stop"

$SrcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillSrc = Join-Path $SrcDir "skill\make-learn"
$Home_ = $env:USERPROFILE

if (-not (Test-Path (Join-Path $SkillSrc "SKILL.md"))) {
    Write-Host "❌ skill\make-learn\SKILL.md 를 찾을 수 없어요. 압축을 푼 폴더 안에서 실행해 주세요."
    exit 1
}

Write-Host "📦 make-learn 스킬을 설치합니다..."

# 1) 공용 본체
$dest = Join-Path $Home_ ".make-learn"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "$SkillSrc\*" $dest

# 2) Claude Code
$dest = Join-Path $Home_ ".claude\skills\make-learn"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "$SkillSrc\*" $dest

# 3) Codex
$dest = Join-Path $Home_ ".codex\skills\make-learn"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "$SkillSrc\*" $dest

# 4) Antigravity (Gemini) 플러그인
#    ~/.gemini/config/plugins/<플러그인>/ 아래에서 로드되므로, plugin.json 으로 등록하고
#    스킬은 skills/<스킬>/ 하위에 둔다.
$PluginRoot = Join-Path $Home_ ".gemini\config\plugins\make-learn-plugin"
$dest = Join-Path $PluginRoot "skills\make-learn"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "$SkillSrc\*" $dest

# plugin.json 은 반드시 BOM 없는 표준 UTF-8 로 기록한다.
# (Set-Content/Out-File 은 BOM 을 붙이므로 .NET API 로 직접 기록한다.)
$pluginJson = @"
{
  "name": "make-learn-plugin",
  "version": "1.0.0",
  "description": "학습자료로 수업용 웹앱 게임을 만들어 주는 make-learn 스킬",
  "author": "gkgk545"
}
"@
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $PluginRoot "plugin.json"), $pluginJson, $utf8NoBom)

Write-Host ""
Write-Host "✅ 설치 완료!"
Write-Host "   공용 본체        → $Home_\.make-learn\"
Write-Host "   Claude Code      → $Home_\.claude\skills\make-learn\  (호출: /make-learn)"
Write-Host "   Codex            → $Home_\.codex\skills\make-learn\"
Write-Host "   Antigravity      → $PluginRoot\  (plugin.json + skills\make-learn, 호출: /make-learn)"
Write-Host ""
Write-Host "사용 중인 프로그램(Claude Code / Codex / Antigravity)을 다시 시작한 뒤,"
Write-Host "채팅창에 /make-learn 을 입력하고 학습자료를 함께 올려보세요."
