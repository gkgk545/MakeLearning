#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_NAME = 'make-learn';
const SKILL_FILES = ['SKILL.md'];
const SKILL_DIRS = ['core'];

const sourceDir = path.join(__dirname, '..', 'skill', 'make-learn');
const targetDir = path.join(os.homedir(), '.claude', 'skills', SKILL_NAME);

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

fs.mkdirSync(targetDir, { recursive: true });

for (const file of SKILL_FILES) {
  const src = path.join(sourceDir, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(targetDir, file));
  }
}

for (const dir of SKILL_DIRS) {
  copyDir(path.join(sourceDir, dir), path.join(targetDir, dir));
}

console.log(`make-learn skill installed → ${targetDir}`);
