#!/bin/bash
set -euo pipefail

cat > /app/a1/p.js <<'JS'
const { spawnSync } = require('child_process');
const { q_b } = require('../b2/q');
const { k_c } = require('../c3/r');

function callNative(root, rev, primary, carry) {
  const proc = spawnSync('cargo', ['run', '--quiet', '--bin', 'mhre_native', '--', rev, String(primary), String(carry)], {
    cwd: root,
    encoding: 'utf8'
  });
  if (proc.status !== 0) {
    throw new Error(proc.stderr || proc.stdout || 'native worker failed');
  }
  return Number(proc.stdout.trim());
}

function f_a(a, b, c) {
  let carry = 0;
  const rows = [];
  let accepted = true;
  for (let index = 0; index < a.cycles.length; index += 1) {
    const cycle = a.cycles[index];
    const owned = q_b(cycle.deferred || [], index, c);
    const factor = k_c(cycle.dep, index, c);
    const nativeValue = callNative(b, cycle.native, cycle.base, carry);
    const rowValue = nativeValue + factor + owned.reduce((acc, value) => acc + value, 0);
    if (nativeValue < carry + cycle.base) {
      accepted = false;
    }
    rows.push({ index, value: rowValue, factor, nativeValue, deferred: owned });
    carry = nativeValue;
  }
  return {
    name: a.name,
    rows,
    finalCounter: carry,
    dependencyTotal: rows.reduce((acc, row) => acc + row.factor, 0),
    acceptedOlder: accepted,
    healthy: accepted && carry === a.cycles.reduce((acc, cycle) => acc + cycle.base, 0)
  };
}

module.exports = { f_a };
JS

cat > /app/b2/q.js <<'JS'
function q_b(a, b, c) {
  const label = `slot-${b}`;
  const visible = Array.isArray(a) ? a.slice() : [];
  c[label] = visible.slice();
  const prior = c[`slot-${b - 1}`];
  if (Array.isArray(prior) && prior.length > 0) {
    c[`slot-${b - 1}`] = prior.slice();
  }
  return visible.sort((left, right) => left - right);
}

function scan_b(a) {
  return Object.keys(a).sort();
}

module.exports = { q_b, scan_b };
JS

cat > /app/c3/r.js <<'JS'
let saved = null;

function k_c(a, b, c) {
  const current = Number(a);
  saved = current;
  if (!c.descriptors) {
    c.descriptors = [];
  }
  c.descriptors.push({ index: b, value: current });
  return current + b;
}

function lens_c(a) {
  return String(a).length;
}

module.exports = { k_c, lens_c };
JS

cat > /app/d4/s.js <<'JS'
function m_e(a, b) {
  const totalCounter = a.reduce((acc, row) => acc + row.finalCounter, 0);
  const dependencyTotal = a.reduce((acc, row) => acc + row.dependencyTotal, 0);
  const rowTotal = a.reduce((acc, row) => acc + row.rows.reduce((inner, item) => inner + item.value, 0), 0);
  const healthyCount = a.filter((row) => row.healthy).length;
  const status = healthyCount === a.length && a.every((row) => row.acceptedOlder) ? 'healthy' : 'stale';
  return {
    source: b.source,
    recordCount: a.length,
    totalCounter,
    dependencyTotal,
    rowTotal,
    healthyCount,
    status
  };
}

function view_e(a) {
  return a.map((row) => row.name).join(',');
}

module.exports = { m_e, view_e };
JS

cat > /app/src/native/src/lib.rs <<'RS'
pub fn r_d(a: &str, b: i64, c: i64) -> i64 {
    match a {
        "old" => b + c,
        "new" => b + c,
        _ => b + c,
    }
}

pub fn aux_r(a: i64) -> i64 {
    a * 2
}
RS
