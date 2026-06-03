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
    if (cycle.native === 'old' && nativeValue < carry + cycle.base) {
      accepted = false;
    }
    rows.push({ index, value: rowValue, factor, nativeValue, deferred: owned });
    carry = cycle.base;
  }
  return {
    name: a.name,
    rows,
    finalCounter: carry,
    dependencyTotal: rows.reduce((acc, row) => acc + row.factor, 0),
    acceptedOlder: accepted,
    healthy: false
  };
}

module.exports = { f_a };
