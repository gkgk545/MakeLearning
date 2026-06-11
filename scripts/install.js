#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'make-learn';
const PLUGIN_NAME = 'make-learn-plugin';
const sourceDir = path.join(__dirname, '..', 'skill', SKILL_NAME);

// 단순 스킬 복사 대상 (Claude Code / Codex / 공용 본체)
const skillTargets = [
  { label: '공용 본체  ', dir: path.join(os.homedir(), '.make-learn') },
  { label: 'Claude Code', dir: path.join(os.homedir(), '.claude', 'skills', SKILL_NAME) },
  { label: 'Codex      ', dir: path.join(os.homedir(), '.codex', 'skills', SKILL_NAME) },
];

// Antigravity(Gemini)는 ~/.gemini/config/plugins/<플러그인>/ 아래에서 로드한다.
// 스킬은 plugins/<플러그인>/skills/<스킬>/ 에 두고, plugin.json 으로 등록한다.
const pluginRoot = path.join(os.homedir(), '.gemini', 'config', 'plugins', PLUGIN_NAME);
const pluginSkillDir = path.join(pluginRoot, 'skills', SKILL_NAME);

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// plugin.json 은 반드시 BOM 없는 표준 UTF-8 로 기록한다.
// (BOM 이 붙으면 Antigravity 의 JSON 파서가 메타데이터를 읽지 못해 플러그인을 통째로 무시한다.)
function writePluginManifest(dir) {
  const manifest = {
    name: PLUGIN_NAME,
    version: '1.0.0',
    description: '학습자료로 수업용 웹앱 게임을 만들어 주는 make-learn 스킬',
    author: 'gkgk545',
  };
  fs.mkdirSync(dir, { recursive: true });
  // JSON.stringify 결과는 BOM 이 없는 순수 ASCII/UTF-8 문자열이다.
  fs.writeFileSync(path.join(dir, 'plugin.json'), JSON.stringify(manifest, null, 2), {
    encoding: 'utf8',
  });
}

if (!fs.existsSync(path.join(sourceDir, 'SKILL.md'))) {
  console.error(`skill/${SKILL_NAME}/SKILL.md 를 찾을 수 없습니다.`);
  process.exit(1);
}

for (const { label, dir } of skillTargets) {
  copyDir(sourceDir, dir);
  console.log(`${label} → ${dir}`);
}

// Antigravity 플러그인 등록
copyDir(sourceDir, pluginSkillDir);
writePluginManifest(pluginRoot);
console.log(`Antigravity → ${pluginRoot} (plugin.json + skills/${SKILL_NAME})`);

console.log('\nmake-learn 설치 완료. 사용 중인 프로그램을 재시작한 뒤 /make-learn 을 입력하세요.');
