function clone_h(a) {
  return JSON.parse(JSON.stringify(a));
}

function stamp_h(a, b) {
  const copy = clone_h(a);
  copy.marker = b;
  return copy;
}

module.exports = { clone_h, stamp_h };
