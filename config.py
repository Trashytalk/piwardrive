"""Application configuration helpers with env overrides."""

import json
import os
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List

import jsonschema

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "theme": {"type": "string"},
        "map_poll_gps": {"type": "integer"},
        "map_poll_aps": {"type": "integer"},
        "map_show_gps": {"type": "boolean"},
        "map_show_aps": {"type": "boolean"},
        "map_cluster_aps": {"type": "boolean"},
        "map_use_offline": {"type": "boolean"},
        "kismet_logdir": {"type": "string"},
        "bettercap_caplet": {"type": "string"},
        "dashboard_layout": {"type": "array"},
        "debug_mode": {"type": "boolean"},
        "offline_tile_path": {"type": "string"},
        "health_poll_interval": {"type": "integer"},
        "log_rotate_interval": {"type": "integer"},
        "log_rotate_archives": {"type": "integer"},
        "widget_battery_status": {"type": "boolean"},
        "admin_password_hash": {"type": "string"},
    },
    "additionalProperties": False,
}


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
    offline_tile_path: str = "/mnt/ssd/tiles/offline.mbtiles"
    health_poll_interval: int = 10
    log_rotate_interval: int = 3600
    log_rotate_archives: int = 3
    widget_battery_status: bool = False
    admin_password_hash: str = ""


DEFAULT_CONFIG = Config()
DEFAULTS = asdict(DEFAULT_CONFIG)


def _apply_env_overrides(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``cfg`` with PW_<KEY> environment overrides."""
    result = dict(cfg)
    for key, default in DEFAULTS.items():
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
            loaded = json.load(f)
        jsonschema.validate(loaded, CONFIG_SCHEMA)
        data = loaded
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, jsonschema.ValidationError):
        pass
    merged = {**DEFAULTS, **data}
    return Config(**merged)


def save_config(config: Config) -> None:
    """Persist ``config`` dataclass to ``CONFIG_PATH``."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(config), f, indent=2)


@dataclass
class AppConfig:
    """Typed configuration container."""

    theme: str = DEFAULTS["theme"]
    map_poll_gps: int = DEFAULTS["map_poll_gps"]
    map_poll_aps: int = DEFAULTS["map_poll_aps"]
    map_show_gps: bool = DEFAULTS["map_show_gps"]
    map_show_aps: bool = DEFAULTS["map_show_aps"]
    map_cluster_aps: bool = DEFAULTS["map_cluster_aps"]
    map_use_offline: bool = DEFAULTS["map_use_offline"]
    offline_tile_path: str = DEFAULTS["offline_tile_path"]
    kismet_logdir: str = DEFAULTS["kismet_logdir"]
    bettercap_caplet: str = DEFAULTS["bettercap_caplet"]
    dashboard_layout: List[Any] = field(default_factory=list)
    debug_mode: bool = DEFAULTS["debug_mode"]
    health_poll_interval: int = DEFAULTS["health_poll_interval"]
    log_rotate_interval: int = DEFAULTS["log_rotate_interval"]
    log_rotate_archives: int = DEFAULTS["log_rotate_archives"]
    widget_battery_status: bool = DEFAULTS["widget_battery_status"]
    admin_password_hash: str = DEFAULTS.get("admin_password_hash", "")

    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration with environment overrides."""
        file_cfg = asdict(load_config())
        merged = _apply_env_overrides(file_cfg)
        return cls(**merged)

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a plain dictionary."""
        return {field: getattr(self, field) for field in DEFAULTS.keys()}
