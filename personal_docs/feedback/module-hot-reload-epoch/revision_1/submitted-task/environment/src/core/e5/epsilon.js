function shape_e(a, b, c) {
  return { title: String(a), width: Number(b || 0), tags: Array.isArray(c) ? c.slice() : [] };
}

function print_e(a) {
  return `${a.title}:${a.width}`;
}

module.exports = { shape_e, print_e };
