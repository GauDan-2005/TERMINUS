import json
import subprocess
from pathlib import Path

import pytest


APP = Path("/app")
REPORT = APP / "output" / "index-report.json"


@pytest.fixture(scope="session")
def report_data():
    """Run the matrix once and return the parsed report."""
    subprocess.run(["bash", "/app/scripts/run-matrix.sh"], cwd=APP, check=True, timeout=180)
    return json.loads(REPORT.read_text(encoding="utf-8"))


def token(*parts):
    return "_".join(parts)


def case_by_name(data, *parts):
    target = token(*parts)
    cases = {item["name"]: item for item in data["cases"]}
    assert target in cases, (target, sorted(cases))
    return cases[target]


def obs_by_label(case, *parts):
    target = token(*parts)
    rows = {item["label"]: item for item in case["observations"]}
    assert target in rows, (target, sorted(rows))
    return rows[target]


def p(*parts):
    return "/".join(("/app", *parts))


def expect_value(actual, expected):
    assert actual == expected, (actual, expected)


def expect_field(obj, key, expected):
    actual = obj[key]
    assert actual == expected, (key, actual, expected, obj)


def expect_path(row, *parts):
    expect_field(row, "path", p(*parts))


def expect_source(row, *parts):
    expect_field(row, "source", p(*parts))


def expect_prefix(obj, key, prefix):
    assert obj[key].startswith(prefix), (key, obj)


def expect_not_prefix(obj, key, prefix):
    assert not obj[key].startswith(prefix), (key, prefix, obj)


def expect_positive(obj, key):
    assert obj[key] > 0, (key, obj)


def expect_sorted(values):
    assert values == sorted(values), values


def test_t01_flow(report_data):
    """Alpha follows the current workspace location after the switch."""
    alpha = case_by_name(report_data, "alpha")
    before = obs_by_label(alpha, "alpha", "before")
    after = obs_by_label(alpha, "alpha", "after")

    expect_field(before, "symbol", "Widget")
    expect_path(before, "fixtures", "alpha", "ws-old", "src", "widget.ts")
    expect_field(after, "found", True)
    expect_field(after, "symbol", "Widget")
    expect_field(after, "fresh", True)
    expect_path(after, "fixtures", "alpha", "ws-new", "src", "widget.ts")
    expect_source(after, "fixtures", "alpha", "ws-new", "src", "widget.ts")
    expect_field(after, "reused", False)


def test_t02_flow(report_data):
    """Beta generated rows carry the refreshed file and source."""
    beta = case_by_name(report_data, "beta")
    after = obs_by_label(beta, "beta", "after")

    expect_field(after, "found", True)
    expect_field(after, "symbol", "Client")
    expect_path(after, "fixtures", "beta", "gen-v2", "generated", "api.ts")
    expect_source(after, "fixtures", "beta", "schemas", "v2", "api.schema")
    expect_field(after, "line", 2)
    expect_field(after, "fresh", True)


def test_t03_flow(report_data):
    """Gamma package rows follow the active target."""
    gamma = case_by_name(report_data, "gamma")
    before = obs_by_label(gamma, "gamma", "before")
    after = obs_by_label(gamma, "gamma", "after")

    expect_field(before, "symbol", "Bridge")
    expect_path(before, "fixtures", "gamma", "pkg-a", "src", "bridge.ts")
    expect_field(after, "found", True)
    expect_field(after, "symbol", "Bridge")
    expect_path(after, "fixtures", "gamma", "pkg-b", "src", "bridge.ts")
    expect_source(after, "fixtures", "gamma", "pkg-b", "src", "bridge.ts")
    expect_field(after, "fresh", True)
    expect_field(after, "reused", False)


def test_t04_flow(report_data):
    """Delta keeps generated handles through an unrelated workspace change."""
    delta = case_by_name(report_data, "delta")
    before = obs_by_label(delta, "delta", "client", "before")
    after_app = obs_by_label(delta, "delta", "client", "after", "app")
    after_gen = obs_by_label(delta, "delta", "client", "after", "gen")

    expect_field(before, "symbol", "DeltaClient")
    expect_path(before, "fixtures", "delta", "gen-v1", "generated", "client.ts")
    expect_field(after_app, "symbol", "DeltaClient")
    expect_path(after_app, "fixtures", "delta", "gen-v1", "generated", "client.ts")
    expect_field(after_gen, "symbol", "DeltaClient")
    expect_source(after_app, "fixtures", "delta", "schemas", "v1", "client.schema")
    expect_field(after_app, "reused", True)
    expect_path(after_gen, "fixtures", "delta", "gen-v2", "generated", "client.ts")
    expect_source(after_gen, "fixtures", "delta", "schemas", "v2", "client.schema")
    expect_field(after_gen, "reused", False)


def test_t05_flow(report_data):
    """Epsilon reports a removed generated symbol as missing."""
    epsilon = case_by_name(report_data, "epsilon")
    before = obs_by_label(epsilon, "epsilon", "legacy", "before")
    after = obs_by_label(epsilon, "epsilon", "legacy", "after")
    client = obs_by_label(epsilon, "epsilon", "client", "after")

    expect_field(before, "found", True)
    expect_field(before, "symbol", "Legacy")
    expect_path(before, "fixtures", "epsilon", "gen-v1", "generated", "legacy.ts")
    expect_field(after, "found", False)
    expect_field(after, "symbol", "Legacy")
    expect_field(after, "path", "")
    expect_field(after, "source", "")
    expect_field(after, "fresh", True)
    expect_field(client, "symbol", "Client")
    expect_path(client, "fixtures", "epsilon", "gen-v2", "generated", "client.ts")


def test_t06_flow(report_data):
    """Zeta handles package and workspace changes in one timeline."""
    zeta = case_by_name(report_data, "zeta")
    bridge_pkg = obs_by_label(zeta, "zeta", "bridge", "after", "pkg")
    widget_pkg = obs_by_label(zeta, "zeta", "widget", "after", "pkg")
    widget_app = obs_by_label(zeta, "zeta", "widget", "after", "app")
    bridge_app = obs_by_label(zeta, "zeta", "bridge", "after", "app")

    expect_field(bridge_pkg, "symbol", "Bridge")
    expect_path(bridge_pkg, "fixtures", "zeta", "pkg-b", "src", "bridge.ts")
    expect_field(widget_pkg, "symbol", "Widget")
    expect_path(widget_pkg, "fixtures", "zeta", "app-old", "src", "widget.ts")
    expect_field(widget_pkg, "reused", True)
    expect_field(widget_app, "symbol", "Widget")
    expect_path(widget_app, "fixtures", "zeta", "app-new", "src", "widget.ts")
    expect_field(widget_app, "reused", False)
    expect_field(bridge_app, "symbol", "Bridge")
    expect_path(bridge_app, "fixtures", "zeta", "pkg-b", "src", "bridge.ts")
    expect_field(bridge_app, "reused", True)


def test_t07_flow(report_data):
    """Every case marks the audit clean."""
    names = [case["name"] for case in report_data["cases"]]
    expect_value(names, ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"])
    for item in report_data["cases"]:
        expect_field(item, "ok", True)
        expect_field(item, "stale", [])


def test_t08_flow(report_data):
    """After-state rows do not point into previous workspace roots."""
    disallowed = {
        token("alpha", "after"): p("fixtures", "alpha", "ws-old") + "/",
        token("delta", "widget", "after", "app"): p("fixtures", "delta", "app-old") + "/",
        token("zeta", "widget", "after", "app"): p("fixtures", "zeta", "app-old") + "/",
    }
    for case in report_data["cases"]:
        for item in case["observations"]:
            prefix = disallowed.get(item["label"])
            if prefix is not None:
                expect_not_prefix(item, "path", prefix)


def test_t09_flow(report_data):
    """Epochs advance while changed rows avoid reuse claims."""
    for case in report_data["cases"]:
        epochs = [item["epoch"] for item in case["observations"]]
        expect_sorted(epochs)
    delta = case_by_name(report_data, "delta")
    widget_after_app = obs_by_label(delta, "delta", "widget", "after", "app")
    client_after_gen = obs_by_label(delta, "delta", "client", "after", "gen")
    expect_field(widget_after_app, "symbol", "DeltaWidget")
    expect_field(widget_after_app, "reused", False)
    expect_field(client_after_gen, "symbol", "DeltaClient")
    expect_field(client_after_gen, "reused", False)


def test_t10_flow(report_data):
    """Stable definitions keep reuse when another slot changes."""
    delta = case_by_name(report_data, "delta")
    zeta = case_by_name(report_data, "zeta")

    client_after_app = obs_by_label(delta, "delta", "client", "after", "app")
    widget_after_gen = obs_by_label(delta, "delta", "widget", "after", "gen")
    widget_after_pkg = obs_by_label(zeta, "zeta", "widget", "after", "pkg")
    bridge_after_app = obs_by_label(zeta, "zeta", "bridge", "after", "app")
    expect_field(client_after_app, "symbol", "DeltaClient")
    expect_field(client_after_app, "reused", True)
    expect_field(widget_after_gen, "symbol", "DeltaWidget")
    expect_field(widget_after_gen, "reused", True)
    expect_field(widget_after_pkg, "symbol", "Widget")
    expect_field(widget_after_pkg, "reused", True)
    expect_field(bridge_after_app, "symbol", "Bridge")
    expect_field(bridge_after_app, "reused", True)


def test_t11_flow(report_data):
    """Path and source fields use the documented found/missing convention."""
    for case in report_data["cases"]:
        for item in case["observations"]:
            assert item["symbol"], (case["name"], item["label"], item)
            if item["found"]:
                expect_prefix(item, "path", "/app/")
                expect_prefix(item, "source", "/app/")
                expect_positive(item, "line")
            else:
                expect_field(item, "path", "")
                expect_field(item, "source", "")
                expect_field(item, "line", 0)


def test_t12_flow(report_data):
    """Two consecutive matrix runs produce the same report."""
    first = json.dumps(report_data, sort_keys=True)
    subprocess.run(["bash", "/app/scripts/run-matrix.sh"], cwd=APP, check=True, timeout=180)
    second = json.dumps(json.loads(REPORT.read_text(encoding="utf-8")), sort_keys=True)
    expect_value(second, first)
