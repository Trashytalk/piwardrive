import os
import subprocess
from pathlib import Path


def test_start_kiosk_launches_browser(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "log.txt"

    server_script = bin_dir / "piwardrive-webui"
    server_script.write_text(
        (
            "#!/bin/sh\n"
            'echo server_started >> "%s"\n'
            "trap 'exit 0' TERM\n"
            "while true; do sleep 0.1; done\n"
        )
        % log
    )
    browser_script = bin_dir / "chromium-browser"
    browser_script.write_text('#!/bin/sh\necho browser_called >> "%s"\n' % log)
    sleep_script = bin_dir / "sleep"
    sleep_script.write_text("#!/bin/sh\n:")
    for p in (server_script, browser_script, sleep_script):
        p.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"

    script = Path("scripts/start_kiosk.sh")
    subprocess.run(["bash", str(script)], env=env, check=True)

    assert "server_started" in log.read_text()
    assert "browser_called" in log.read_text()
