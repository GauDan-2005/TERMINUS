let saved = null;

function k_c(a, b, c) {
  if (saved === null) {
    saved = Number(a);
  }
  return saved + b;
}

function lens_c(a) {
  return String(a).length;
}

module.exports = { k_c, lens_c };
