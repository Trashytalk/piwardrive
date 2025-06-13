
import json
import os
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


@dataclass
class Config:
    """Persistent application configuration."""

    theme: str = "Dark"
    map_poll_gps: int = 10
    map_poll_aps: int = 60
    map_show_gps: bool = True
    map_show_aps: bool = True
    map_cluster_aps: bool = False
    map_use_offline: bool = False
    kismet_logdir: str = "/mnt/ssd/kismet_logs"
    bettercap_caplet: str = "/usr/local/etc/bettercap/alfa.cap"
    dashboard_layout: List[Any] = field(default_factory=list)
    debug_mode: bool = False


DEFAULT_CONFIG = Config()

def _apply_env_overrides(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``cfg`` with PW_<KEY> environment overrides."""
    result = dict(cfg)
    for key, default in DEFAULT_CONFIG.items():
        env_key = f"PW_{key.upper()}"
        if env_key in os.environ:
            raw = os.environ[env_key]
            if isinstance(default, bool):
                result[key] = raw.lower() in {"1", "true", "yes", "on"}
            elif isinstance(default, int):
                try:
                    result[key] = int(raw)
                except ValueError:
                    pass
            elif isinstance(default, list):
                try:
                    result[key] = json.loads(raw)
                except json.JSONDecodeError:
                    result[key] = raw
            else:
                result[key] = raw
    return result


def load_config() -> Config:
    """Load configuration from ``CONFIG_PATH`` and return a :class:`Config`."""

    data: Dict[str, Any] = {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    merged = {**asdict(DEFAULT_CONFIG), **data}
    return Config(**merged)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(config), f, indent=2)

def save_config(config: Dict[str, Any]) -> None:
    """Persist ``config`` dictionary to ``CONFIG_PATH``."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

@dataclass
class AppConfig:
    """Typed configuration container."""

    theme: str = DEFAULT_CONFIG["theme"]
    map_poll_gps: int = DEFAULT_CONFIG["map_poll_gps"]
    map_poll_aps: int = DEFAULT_CONFIG["map_poll_aps"]
    map_show_gps: bool = DEFAULT_CONFIG["map_show_gps"]
    map_show_aps: bool = DEFAULT_CONFIG["map_show_aps"]
    map_cluster_aps: bool = DEFAULT_CONFIG["map_cluster_aps"]
    map_use_offline: bool = DEFAULT_CONFIG["map_use_offline"]
    offline_tile_path: str = DEFAULT_CONFIG["offline_tile_path"]
    kismet_logdir: str = DEFAULT_CONFIG["kismet_logdir"]
    bettercap_caplet: str = DEFAULT_CONFIG["bettercap_caplet"]
    dashboard_layout: List[Any] = field(default_factory=list)
    debug_mode: bool = DEFAULT_CONFIG["debug_mode"]

    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration with environment overrides."""
        return cls(**load_config())

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a plain dictionary."""
        return {field: getattr(self, field) for field in DEFAULT_CONFIG.keys()}
