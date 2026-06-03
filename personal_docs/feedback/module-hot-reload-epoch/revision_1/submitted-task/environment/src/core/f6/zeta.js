function order_f(a) {
  return a.slice().sort((left, right) => String(left).localeCompare(String(right)));
}

function merge_f(a, b) {
  return order_f([].concat(a || [], b || []));
}

module.exports = { order_f, merge_f };
