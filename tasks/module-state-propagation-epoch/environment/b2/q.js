function q_b(a, b, c) {
  const label = `slot-${b}`;
  c[label] = (c[label] || []).concat(a);
  const next = `slot-${b + 1}`;
  const visible = c[next] || [];
  c[next] = [];
  return visible.slice().sort((left, right) => left - right);
}

function scan_b(a) {
  return Object.keys(a).sort();
}

module.exports = { q_b, scan_b };
