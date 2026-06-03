function m_e(a, b) {
  const totalCounter = a.reduce((acc, row) => acc + row.finalCounter, 0);
  const dependencyTotal = a.reduce((acc, row) => acc + row.dependencyTotal, 0);
  const rowTotal = a.reduce((acc, row) => acc + row.rows.reduce((inner, item) => inner + item.value, 0), 0);
  const healthyCount = a.filter((row) => row.acceptedOlder).length;
  return {
    source: b.source,
    recordCount: a.length,
    totalCounter,
    dependencyTotal,
    rowTotal,
    healthyCount,
    status: 'stale'
  };
}

function view_e(a) {
  return a.map((row) => row.name).join(',');
}

module.exports = { m_e, view_e };
