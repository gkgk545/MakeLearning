#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'make-learn';
const sourceDir = path.join(__dirname, '..', 'skill', SKILL_NAME);

// install.sh / install.ps1 과 동일한 설치 대상
const targets = [
  { label: '공용 본체  ', dir: path.join(os.homedir(), '.make-learn') },
  { label: 'Claude Code', dir: path.join(os.homedir(), '.claude', 'skills', SKILL_NAME) },
  { label: 'Codex      ', dir: path.join(os.homedir(), '.codex', 'skills', SKILL_NAME) },
  { label: 'Antigravity', dir: path.join(os.homedir(), '.gemini', 'antigravity', 'skills', SKILL_NAME) },
];

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

if (!fs.existsSync(path.join(sourceDir, 'SKILL.md'))) {
  console.error(`skill/${SKILL_NAME}/SKILL.md 를 찾을 수 없습니다.`);
  process.exit(1);
}

for (const { label, dir } of targets) {
  copyDir(sourceDir, dir);
  console.log(`${label} → ${dir}`);
}

console.log('\nmake-learn 설치 완료. 사용 중인 프로그램을 재시작한 뒤 /make-learn 을 입력하세요.');
