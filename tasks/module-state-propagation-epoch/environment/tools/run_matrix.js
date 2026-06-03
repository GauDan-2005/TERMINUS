#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { f_a } = require('../a1/p');
const { m_e } = require('../d4/s');

const base = process.cwd();
const dataPath = path.join(base, 'fixtures', 'scenarios.json');
const outDir = path.join(base, 'outcome');
const outPath = path.join(outDir, 'report.json');

function main() {
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  const records = data.scenarios.map((entry) => f_a(entry, base, {}));
  const aggregate = m_e(records, { source: 'local' });
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify({ records, aggregate }, null, 2) + '\n');
}

main();
