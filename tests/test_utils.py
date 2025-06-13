import os
import sys
import tempfile
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
        run_mock.assert_called_once_with(['sudo', 'systemctl', 'start', 'kismet'], capture_output=True, text=True)
        assert success is True
        assert out == 'ok'
        assert err == ''


def test_run_service_cmd_failure():
    mock_proc = mock.Mock(returncode=1, stdout='', stderr='error')
    with mock.patch('utils.subprocess.run', return_value=mock_proc):
        success, out, err = utils.run_service_cmd('kismet', 'start')
        assert success is False
        assert out == ''
        assert err == 'error'
