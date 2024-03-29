"""Integration tests for the Agresso API service.

Set `AGRESSO_API_KEY` temporarily in `tox.ini` to run these tests against a
real Agresso instance.

Running these may take some time depending on how fast Agresso feels like
responding.
"""

import os

import pytest

from agresso.service import (
    account_name,
    get_budget,
    get_budget_descriptions,
    get_general_ledger,
    get_user_log_contractor_invoices,
    get_workflow_comment_parked,
    get_workflow_contrator_invoices,
)


def _is_csv_serializable(data):
    """Return true if `data` is CSV serializable by our JSON->CSV pipeline.

    In particular, check that all the dicts in `data` contain the same keys.
    """
    if len(data) == 0:
        return True

    keys = data[0].keys()
    return all([keys == d.keys() for d in data[1:]])


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_general_ledger():
    data = get_general_ledger(2024)
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_workflow_contrator_invoices():
    data = get_workflow_contrator_invoices()
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_user_log_contrator_invoices():
    data = get_user_log_contractor_invoices()
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_workflow_comment_parked():
    data = get_workflow_comment_parked()
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_budget():
    data = get_budget(2024)
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_budget_descriptions():
    data = get_budget_descriptions(2024)
    assert isinstance(data, list)
    assert _is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_account_name():
    assert account_name("00100") == "Lønn faste stillinger (HR)"
