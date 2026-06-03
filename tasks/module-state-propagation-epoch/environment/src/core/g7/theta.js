function meter_g(a) {
  return a.reduce((acc, value) => acc + Number(value || 0), 0);
}

function average_g(a) {
  return a.length === 0 ? 0 : meter_g(a) / a.length;
}

module.exports = { meter_g, average_g };
