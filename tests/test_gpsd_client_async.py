import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gpsd_client_async


class DummyReader:
    def __init__(self, lines):
        self.lines = lines

    async def readline(self):
        if self.lines:
            return (self.lines.pop(0) + "\n").encode()
        return b""


class DummyWriter:
    def __init__(self):
        self.sent = []

    def write(self, data):
        self.sent.append(data.decode())

    async def drain(self):
        pass

    def close(self):
        pass

    async def wait_closed(self):
        pass


def test_async_methods_return_values(monkeypatch):
    lines = [
        '{"class":"VERSION"}',
        '{"class":"DEVICES"}',
        '{"class":"WATCH"}',
        '{"class":"POLL","tpv":[{"mode":3,"lat":1.0,"lon":2.0,"epx":1.0,"epy":2.0}]}',
        '{"class":"POLL","tpv":[{"mode":3,"lat":1.0,"lon":2.0,"epx":1.0,"epy":2.0}]}',
        '{"class":"POLL","tpv":[{"mode":3,"lat":1.0,"lon":2.0,"epx":1.0,"epy":2.0}]}',
        '{"class":"POLL","tpv":[{"mode":3,"lat":1.0,"lon":2.0,"epx":1.0,"epy":2.0}]}',
    ]
    writer = DummyWriter()

    async def fake_open_connection(host, port):
        return DummyReader(lines), writer

    monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)

    client = gpsd_client_async.AsyncGPSDClient()

    async def run():
        pos = await client.get_position_async()
        acc = await client.get_accuracy_async()
        fix = await client.get_fix_quality_async()
        return pos, acc, fix

    pos, acc, fix = asyncio.run(run())

    assert pos == (1.0, 2.0)
    assert acc == 2.0
    assert fix == "3D"
    assert writer.sent[0].startswith("?WATCH")
    assert writer.sent.count("?POLL;\n") == 3


def test_async_methods_failures(monkeypatch):
    async def fake_open_connection(host, port):
        raise OSError("fail")

    monkeypatch.setattr(asyncio, "open_connection", fake_open_connection)

    client = gpsd_client_async.AsyncGPSDClient()

    async def run():
        pos = await client.get_position_async()
        acc = await client.get_accuracy_async()
        fix = await client.get_fix_quality_async()
        return pos, acc, fix

    pos, acc, fix = asyncio.run(run())

    assert pos is None
    assert acc is None
    assert fix == "Unknown"
