import json
import subprocess

import pytest
from pathlib import Path


APP = Path('/app')
OUT = APP / 'outcome' / 'report.json'

SCENARIOS = [
    {'name':'alpha','cycles':[{'base':4,'dep':2,'deferred':[3],'native':'old'},{'base':5,'dep':3,'deferred':[],'native':'new'}]},
    {'name':'beta','cycles':[{'base':2,'dep':4,'deferred':[5,1],'native':'old'},{'base':3,'dep':4,'deferred':[2],'native':'old'},{'base':1,'dep':5,'deferred':[],'native':'new'}]},
    {'name':'gamma','cycles':[{'base':6,'dep':1,'deferred':[],'native':'new'},{'base':2,'dep':6,'deferred':[4],'native':'old'}]},
    {'name':'delta','cycles':[{'base':1,'dep':7,'deferred':[2,2],'native':'old'},{'base':8,'dep':2,'deferred':[1],'native':'new'}]},
    {'name':'epsilon','cycles':[{'base':3,'dep':3,'deferred':[3],'native':'old'},{'base':3,'dep':8,'deferred':[2],'native':'old'},{'base':3,'dep':2,'deferred':[],'native':'new'}]},
    {'name':'zeta','cycles':[{'base':9,'dep':2,'deferred':[],'native':'old'},{'base':1,'dep':9,'deferred':[3],'native':'new'}]},
]


def expected_record(scenario):
    carry = 0
    rows = []
    accepted = True
    for index, cycle in enumerate(scenario['cycles']):
        native = cycle['base'] + carry
        factor = cycle['dep'] + index
        deferred = sorted(cycle.get('deferred', []))
        value = native + factor + sum(deferred)
        accepted = accepted and native >= carry + cycle['base']
        rows.append({'index': index, 'value': value, 'factor': factor, 'nativeValue': native, 'deferred': deferred})
        carry = native
    return {
        'name': scenario['name'],
        'rows': rows,
        'finalCounter': carry,
        'dependencyTotal': sum(row['factor'] for row in rows),
        'acceptedOlder': accepted,
        'healthy': accepted and carry == sum(cycle['base'] for cycle in scenario['cycles']),
    }


def expected_report():
    records = [expected_record(s) for s in SCENARIOS]
    aggregate = {
        'source': 'local',
        'recordCount': len(records),
        'totalCounter': sum(r['finalCounter'] for r in records),
        'dependencyTotal': sum(r['dependencyTotal'] for r in records),
        'rowTotal': sum(sum(row['value'] for row in r['rows']) for r in records),
        'healthyCount': sum(1 for r in records if r['healthy']),
        'status': 'healthy' if all(r['healthy'] for r in records) else 'stale',
    }
    return {'records': records, 'aggregate': aggregate}


def run_matrix():
    if OUT.exists():
        OUT.unlink()
    subprocess.run(['npm', 'run', 'matrix'], cwd=APP, check=True, text=True, capture_output=True)


def run_report():
    run_matrix()
    return json.loads(OUT.read_text())


def by_name(report, name):
    return {row['name']: row for row in report['records']}[name]


@pytest.fixture(scope='module')
def shared_report():
    return run_report()


def test_case_one(shared_report):
    """The first scenario keeps carried numeric values across the second row."""
    assert by_name(shared_report, 'alpha') == expected_record(SCENARIOS[0])


def test_case_two(shared_report):
    """Aggregate counters are folded from the scenario records."""
    expected = expected_report()
    assert shared_report['aggregate']['totalCounter'] == expected['aggregate']['totalCounter']
    assert shared_report['aggregate']['recordCount'] == len(SCENARIOS)


def test_case_three(shared_report):
    """Scenario names and row counts remain aligned after repeated runs."""
    got = [(r['name'], len(r['rows'])) for r in shared_report['records']]
    want = [(s['name'], len(s['cycles'])) for s in SCENARIOS]
    assert got == want


def test_case_four(shared_report):
    """Deferred row values are credited to their owning row."""
    assert by_name(shared_report, 'delta')['rows'] == expected_record(SCENARIOS[3])['rows']


def test_case_five(shared_report):
    """Late deferred values survive descriptor changes in a longer run."""
    assert [r['deferred'] for r in by_name(shared_report, 'epsilon')['rows']] == [[3], [2], []]
    assert by_name(shared_report, 'epsilon')['finalCounter'] == expected_record(SCENARIOS[4])['finalCounter']


def test_case_six(shared_report):
    """Descriptor factors are computed from each row rather than a prior row."""
    assert [r['factor'] for r in by_name(shared_report, 'zeta')['rows']] == [2, 10]


def test_case_seven(shared_report):
    """Independent scenarios do not share descriptor values."""
    assert by_name(shared_report, 'gamma')['dependencyTotal'] == expected_record(SCENARIOS[2])['dependencyTotal']
    assert by_name(shared_report, 'zeta')['dependencyTotal'] == expected_record(SCENARIOS[5])['dependencyTotal']


def test_case_eight(shared_report):
    """Older native records are accepted after normalization."""
    assert all(record['acceptedOlder'] for record in shared_report['records'])


def test_case_nine(shared_report):
    """Mixed native revisions produce stable row totals."""
    expected = expected_report()
    assert shared_report['aggregate']['rowTotal'] == expected['aggregate']['rowTotal']
    assert by_name(shared_report, 'beta')['rows'][1]['nativeValue'] == expected_record(SCENARIOS[1])['rows'][1]['nativeValue']


def test_case_ten(shared_report):
    """The final status comes from all scenario health checks."""
    expected = expected_report()
    assert shared_report['aggregate'] == expected['aggregate']
    assert all(row['healthy'] for row in shared_report['records'])


def test_rust_build_artifact_present(shared_report):
    """The Rust component is compiled and present after matrix execution."""
    target = APP / 'target'
    assert target.exists(), 'Rust target/ directory missing after matrix run'
    binaries = list(target.rglob('mhre_native'))
    assert binaries, 'Rust binary mhre_native was never built'


def test_report_stable_across_consecutive_runs():
    """Running matrix twice in one session produces identical reports."""
    r1 = run_report()
    subprocess.run(['npm', 'run', 'matrix'], cwd=APP, check=True, text=True, capture_output=True)
    r2 = json.loads(OUT.read_text())
    assert r1 == r2, 'Report drifted between consecutive matrix runs'
