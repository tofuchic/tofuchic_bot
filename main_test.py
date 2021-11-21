import base64
from datetime import datetime
import main
import pytest

key = pytest.importorskip('key')


def test_init_logfile(capsys):
    # Call tested function
    main.init_logfile(force=True)
    out, err = capsys.readouterr()
    log_path = './trigger.log'
    with open(log_path, mode='r') as log_file:
        assert log_file.readlines() == []


def test_get_latest_triggered_datetime(capsys):
    # Call tested function
    _datetime = '2021-11-21 05:37:32\n'
    expect = datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S\n')
    log_path = './trigger.log'
    with open(log_path, mode='w') as log_file:
        log_file.write(_datetime)
    actual = main.get_latest_triggered_datetime()
    out, err = capsys.readouterr()
    assert actual == expect
