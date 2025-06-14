"""Tests for various utility helpers."""
import os
import sys
import tempfile
import zipfile

from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.modules.setdefault('psutil', mock.Mock())
sys.modules.setdefault('requests', mock.Mock())
import utils


def test_find_latest_file_returns_latest():
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


def test_find_latest_file_none_when_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert utils.find_latest_file(tmpdir, '*.txt') is None


def test_tail_file_returns_last_lines():
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        for i in range(5):
            tmp.write(f"line{i}\n")
        tmp_path = tmp.name
    try:
        result = utils.tail_file(tmp_path, lines=3)
        assert result == ['line2', 'line3', 'line4']
    finally:
        os.unlink(tmp_path)


def test_tail_file_missing_returns_empty_list():
    result = utils.tail_file('/does/not/exist', lines=3)
    assert result == []


def test_run_service_cmd_success():
    mock_proc = mock.Mock(returncode=0, stdout='ok', stderr='')
    with mock.patch('utils.subprocess.run', return_value=mock_proc) as run_mock:
        success, out, err = utils.run_service_cmd('kismet', 'start')
        run_mock.assert_called_once_with(
            ['sudo', 'systemctl', 'start', 'kismet'], capture_output=True, text=True
        )
        assert success is True
        assert out == 'ok'
        assert err == ''


def test_run_service_cmd_failure():
    mock_proc = mock.Mock(returncode=1, stdout='', stderr='error')
    with mock.patch('utils.subprocess.run', return_value=mock_proc) as run_mock:
        success, out, err = utils.run_service_cmd('kismet', 'start')
        run_mock.assert_called_once()
        assert success is False
        assert out == ''
        assert err == 'error'


def test_run_service_cmd_retries_until_success():
    results = [
        OSError('boom'),
        mock.Mock(returncode=0, stdout='ok', stderr=''),
    ]

    def side_effect(*_args, **_kwargs):
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


def test_service_status_passes_retry_params():
    with mock.patch(
        'utils.run_service_cmd',
        return_value=(True, 'active', '')
    ) as run_mock:
        assert utils.service_status('kismet', attempts=2, delay=0.5) is True
        run_mock.assert_called_once_with('kismet', 'is-active', attempts=2, delay=0.5)


def test_point_in_polygon_basic():
    square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert utils.point_in_polygon((0.5, 0.5), square) is True
    assert utils.point_in_polygon((1.5, 0.5), square) is False


def test_load_kml_parses_features(tmp_path):
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


def test_load_kmz_parses_features(tmp_path):
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
