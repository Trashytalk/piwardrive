import sys


def test_vector_tile_customizer_cli_build(monkeypatch):
    called = {}
    if 'piwardrive.scripts.vector_tile_customizer_cli' in sys.modules:
        del sys.modules['piwardrive.scripts.vector_tile_customizer_cli']
    import piwardrive.scripts.vector_tile_customizer_cli as cli

    def fake_build(folder, output):
        called['build'] = (folder, output)

    monkeypatch.setattr(cli.vtc, 'build_mbtiles', fake_build)
    cli.main(['build', 'tiles', 'out.mbtiles'])
    assert called['build'] == ('tiles', 'out.mbtiles')


def test_vector_tile_customizer_cli_style(monkeypatch):
    called = {}
    if 'piwardrive.scripts.vector_tile_customizer_cli' in sys.modules:
        del sys.modules['piwardrive.scripts.vector_tile_customizer_cli']
    import piwardrive.scripts.vector_tile_customizer_cli as cli

    def fake_style(mbtiles, *, style_path=None, name=None, description=None):
        called['style'] = (mbtiles, style_path, name, description)

    monkeypatch.setattr(cli.vtc, 'apply_style', fake_style)
    cli.main([
        'style',
        'db.mbtiles',
        '--style', 'style.json',
        '--name', 'N',
        '--description', 'D',
    ])
    assert called['style'] == ('db.mbtiles', 'style.json', 'N', 'D')

