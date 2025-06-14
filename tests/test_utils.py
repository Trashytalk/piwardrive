"""Tests for various utility helpers."""
import os
import sys
import tempfile
import zipfile
import json

from typing import Any

from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.modules.setdefault('psutil', mock.Mock())
import psutil
if 'requests' not in sys.modules:
    dummy_requests = mock.Mock()
    dummy_requests.RequestException = Exception
    sys.modules['requests'] = dummy_requests
import utils
import asyncio
from collections import namedtuple


def test_find_latest_file_returns_latest() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, 'a.txt')
        file2 = os.path.join(tmpdir, 'b.txt')
        with open(file1, 'w') as f:
            f.write('1')
        with open(file2, 'w') as f:
            f.write('2')
        os.utime(file1, (1, 1))
        os.utime(file2, (2, 2))
        result = utils.find_latest_file(tmpdir, '*.txt')
        assert result == file2


def test_find_latest_file_none_when_empty() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        assert utils.find_latest_file(tmpdir, '*.txt') is None


def test_tail_file_returns_last_lines() -> None:
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        for i in range(5):
            tmp.write(f"line{i}\n")
        tmp_path = tmp.name
    try:
        result = utils.tail_file(tmp_path, lines=3)
        assert result == ['line2', 'line3', 'line4']
    finally:
        os.unlink(tmp_path)


def test_tail_file_missing_returns_empty_list() -> None:
    result = utils.tail_file('/does/not/exist', lines=3)
    assert result == []


def test_run_service_cmd_success() -> None:
    mock_proc = mock.Mock(returncode=0, stdout='ok', stderr='')
    with mock.patch('utils.subprocess.run', return_value=mock_proc) as run_mock:
        success, out, err = utils.run_service_cmd('kismet', 'start')
        run_mock.assert_called_once_with(
            ['sudo', 'systemctl', 'start', 'kismet'], capture_output=True, text=True
        )
        assert success is True
        assert out == 'ok'
        assert err == ''


def test_run_service_cmd_failure() -> None:
    mock_proc = mock.Mock(returncode=1, stdout='', stderr='error')
    with mock.patch('utils.subprocess.run', return_value=mock_proc) as run_mock:
        success, out, err = utils.run_service_cmd('kismet', 'start')
        run_mock.assert_called_once()
        assert success is False
        assert out == ''
        assert err == 'error'


def test_run_service_cmd_retries_until_success() -> None:
    results = [
        OSError('boom'),
        mock.Mock(returncode=0, stdout='ok', stderr=''),
    ]

    def side_effect(*_args: Any, **_kwargs: Any) -> Any:
        res = results.pop(0)
        if isinstance(res, Exception):
            raise res
        return res

    with mock.patch('utils.subprocess.run', side_effect=side_effect) as run_mock:
        success, out, err = utils.run_service_cmd('kismet', 'start', attempts=2, delay=0)
        assert run_mock.call_count == 2
        assert success is True
        assert out == 'ok'
        assert err == ''


def test_service_status_passes_retry_params() -> None:
    with mock.patch(
        'utils.run_service_cmd',
        return_value=(True, 'active', '')
    ) as run_mock:
        assert utils.service_status('kismet', attempts=2, delay=0.5) is True
        run_mock.assert_called_once_with('kismet', 'is-active', attempts=2, delay=0.5)


def test_point_in_polygon_basic() -> None:
    square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert utils.point_in_polygon((0.5, 0.5), square) is True
    assert utils.point_in_polygon((1.5, 0.5), square) is False


def test_load_kml_parses_features(tmp_path: Any) -> None:
    kml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<kml xmlns='http://www.opengis.net/kml/2.2'>"
        "<Placemark><name>Line</name><LineString><coordinates>0,0 1,1</coordinates></LineString></Placemark>"
        "<Placemark><name>Pt</name><Point><coordinates>2,2</coordinates></Point></Placemark>"
        "</kml>"
    )
    kml_path = tmp_path / 'test.kml'
    kml_path.write_text(kml_content)
    feats = utils.load_kml(str(kml_path))
    types = sorted(f['type'] for f in feats)
    assert types == ['LineString', 'Point']


def test_load_kmz_parses_features(tmp_path: Any) -> None:
    kml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<kml xmlns='http://www.opengis.net/kml/2.2'>"
        "<Placemark><name>Pt</name><Point><coordinates>3,3</coordinates></Point></Placemark>"
        "</kml>"
    )
    kmz_path = tmp_path / 'test.kmz'
    with zipfile.ZipFile(kmz_path, 'w') as zf:
        zf.writestr('doc.kml', kml_content)
    feats = utils.load_kml(str(kmz_path))
    assert feats and feats[0]['type'] == 'Point'


def test_fetch_kismet_devices_request_exception(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        utils.requests,
        'get',
        mock.Mock(side_effect=utils.requests.RequestException('boom')),
    )
    with mock.patch('utils.report_error') as err:
        aps, clients = utils.fetch_kismet_devices()
        assert aps == [] and clients == []
        assert err.call_count == 2


def test_fetch_kismet_devices_json_error(monkeypatch: Any) -> None:
    resp = mock.Mock(status_code=200)
    resp.json.side_effect = json.JSONDecodeError('bad', 'doc', 0)
    monkeypatch.setattr(utils.requests, 'get', mock.Mock(return_value=resp))
    with mock.patch('utils.report_error') as err:
        aps, clients = utils.fetch_kismet_devices()
        assert aps == [] and clients == []
        assert err.call_count == 2


def test_get_smart_status_ok(monkeypatch: Any) -> None:
    Part = namedtuple('Part', 'device mountpoint fstype opts')
    part = Part('/dev/sda', '/mnt/ssd', 'ext4', '')
    monkeypatch.setattr(psutil, 'disk_partitions', lambda all=False: [part])
    proc = mock.Mock(returncode=0, stdout='SMART overall-health self-assessment test result: PASSED\n', stderr='')
    monkeypatch.setattr(utils.subprocess, 'run', lambda *a, **k: proc)
    assert utils.get_smart_status('/mnt/ssd') == 'OK'


def test_fetch_kismet_devices_async(monkeypatch: Any) -> None:
    resp = mock.Mock(status_code=200, content=b'{"access_points": [1], "clients": [2]}')
    monkeypatch.setattr(utils.requests, 'get', lambda *a, **k: resp)
    aps, clients = asyncio.run(utils.fetch_kismet_devices_async())
    assert aps == [1] and clients == [2]


def test_polygon_area_triangle() -> None:
    pts = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
    area = utils.polygon_area(pts)
    expected = 111320.0 ** 2 / 2
    assert abs(area - expected) < expected * 0.05
