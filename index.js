#!/usr/bin/env node

/**
 * Paper Mentor Skill for Claude Code
 *
 * This is a Claude Code skill that helps users deeply understand academic papers.
 *
 * Installation:
 *   npx @your-username/paper-mentor-skill
 *
 * Or install to Claude Code skills directory:
 *   npx @your-username/paper-mentor-skill install
 */

const path = require('path');
const fs = require('fs');
const os = require('os');

const SKILL_NAME = 'paper-mentor';
const SKILL_DIR = path.join(os.homedir(), '.claude', 'skills', SKILL_NAME);

function install() {
  const sourceDir = __dirname;

  console.log(`📦 Installing ${SKILL_NAME} skill...`);

  // Create destination directory
  if (!fs.existsSync(SKILL_DIR)) {
    fs.mkdirSync(SKILL_DIR, { recursive: true });
  }

  // Copy files
  const files = fs.readdirSync(sourceDir);
  for (const file of files) {
    if (['node_modules', 'package.json', 'index.js', '.git'].includes(file)) {
      continue;
    }

    const sourcePath = path.join(sourceDir, file);
    const destPath = path.join(SKILL_DIR, file);

    if (fs.statSync(sourcePath).isDirectory()) {
      // Skip directories
      continue;
    }

    fs.copyFileSync(sourcePath, destPath);
    console.log(`  ✓ Copied ${file}`);
  }

  console.log(`\n✅ ${SKILL_NAME} skill installed successfully!`);
  console.log(`   Location: ${SKILL_DIR}`);
  console.log(`\nUsage in Claude Code:`);
  console.log(`   /${SKILL_NAME} https://arxiv.org/abs/XXXX.XXXXX`);
}

// Main entry point
const args = process.argv.slice(2);

if (args[0] === 'install') {
  install();
} else if (args[0] === 'help' || args[0] === '--help' || args[0] === '-h') {
  console.log(`
Paper Mentor Skill for Claude Code

Usage:
  npx paper-mentor-skill install    Install the skill to Claude Code
  npx paper-mentor-skill help       Show this help message

After installation, use in Claude Code:
  /paper-mentor https://arxiv.org/abs/XXXX.XXXXX
`);
} else {
  console.log(`
Paper Mentor Skill for Claude Code

To install:
  npx paper-mentor-skill install

Or directly:
  npx paper-mentor-skill install
`);
}
