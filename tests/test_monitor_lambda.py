import pytest

from src.ec2_uptime_monitor.deepracer_ec2_uptime_report import lambda_handler


def test_default():
    res = lambda_handler
    assert 1 == 1
