import json
import sys
from types import SimpleNamespace


def test_calibrate_orientation(tmp_path, monkeypatch):
    module = SimpleNamespace(
        BaseModel=object,
        Field=lambda *a, **k: None,
        ValidationError=Exception,
    )
    module.field_validator = lambda *a, **k: (lambda f: f)
    monkeypatch.setitem(sys.modules, "pydantic", module)

    import piwardrive.scripts.calibrate_orientation as co

    out = tmp_path / "omap.json"
    monkeypatch.setattr(co, "setup_logging", lambda stdout=True: None)

    def fake_prompt(angle: float) -> None:
        co.osens.update_orientation_map({f"orient_{int(angle)}": angle})

    monkeypatch.setattr(co, "_prompt", fake_prompt)

    try:
        co.main(["--output", str(out)])
    finally:
        co.osens.reset_orientation_map()

    data = json.loads(out.read_text())
    for key in ("orient_0", "orient_90", "orient_180", "orient_270"):
        assert key in data
