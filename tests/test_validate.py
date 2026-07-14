import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

from etl.validate import validate

def _make_mock_connection(total, uniq, met, breached, open_count, critical_count, bad_rows):
    connection = MagicMock()

    row_counts_result = MagicMock()
    row_counts_result.one.return_value = SimpleNamespace(total=total, uniq=uniq)

    status_counts_result = MagicMock()
    status_counts_result.all.return_value = [("Met", met), ("Breached", breached)]

    open_result = MagicMock()
    open_result.scalar.return_value = open_count

    critical_result = MagicMock()
    critical_result.scalar.return_value = critical_count

    bad_rows_result = MagicMock()
    bad_rows_result.scalar.return_value = bad_rows

    connection.execute.side_effect = [
        row_counts_result,
        status_counts_result,
        open_result,
        critical_result,
        bad_rows_result,
    ]
    return connection


def _silent_logger():
    logger = logging.getLogger("test_validate")
    logger.addHandler(logging.NullHandler())
    return logger


def test_validate_all_pass(monkeypatch):
    expected = {
        "total_rows": 180,
        "unique_incident_ids": 180,
        "met_target": 38,
        "breached_target": 142,
        "open_incidents": 63,
        "critical_incidents": 12,
    }
    monkeypatch.setattr("etl.validate.EXPECTED", expected)

    conn = _make_mock_connection(
        total=180, uniq=180, met=38, breached=142,
        open_count=63, critical_count=12, bad_rows=0,
    )
    assert validate(conn, _silent_logger()) is True


def test_validate_fails_on_mismatch(monkeypatch):
    expected = {
        "total_rows": 180,
        "unique_incident_ids": 180,
        "met_target": 38,
        "breached_target": 142,
        "open_incidents": 63,
        "critical_incidents": 12,
    }
    monkeypatch.setattr("etl.validate.EXPECTED", expected)

    # open_incidents is wrong (60 instead of 63)
    conn = _make_mock_connection(
        total=180, uniq=180, met=38, breached=142,
        open_count=60, critical_count=12, bad_rows=0,
    )
    assert validate(conn, _silent_logger()) is False


def test_validate_fails_on_negative_delay(monkeypatch):
    expected = {
        "total_rows": 180,
        "unique_incident_ids": 180,
        "met_target": 38,
        "breached_target": 142,
        "open_incidents": 63,
        "critical_incidents": 12,
    }
    monkeypatch.setattr("etl.validate.EXPECTED", expected)

    conn = _make_mock_connection(
        total=180, uniq=180, met=38, breached=142,
        open_count=63, critical_count=12, bad_rows=2,
    )
    assert validate(conn, _silent_logger()) is False