import os
import sys

from piwardrive.sigint_suite.cellular.parsers import (parse_band_output,
                                                      parse_imsi_output)


def test_parse_imsi_output():
    output = "12345,310,260,-50\n67890,311,480,-60"
    recs = parse_imsi_output(output)
    assert [r.model_dump() for r in recs] == [
        {"imsi": "12345", "mcc": "310", "mnc": "260", "rssi": "-50", "lat": None, "lon": None},
        {"imsi": "67890", "mcc": "311", "mnc": "480", "rssi": "-60", "lat": None, "lon": None},
    ]


def test_parse_band_output():
    output = "LTE,100,-60\n5G,200,-70"
    recs = parse_band_output(output)
    assert [r.model_dump() for r in recs] == [
        {"band": "LTE", "channel": "100", "rssi": "-60"},
        {"band": "5G", "channel": "200", "rssi": "-70"},
    ]
