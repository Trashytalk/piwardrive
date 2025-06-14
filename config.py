"""Application configuration helpers with env overrides and validation."""

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
        "theme": {"type": "string", "enum": ["Dark", "Light"]},
        "map_poll_gps": {"type": "integer", "minimum": 1},
        "map_poll_aps": {"type": "integer", "minimum": 1},
        "map_show_gps": {"type": "boolean"},
        "map_show_aps": {"type": "boolean"},
        "map_cluster_aps": {"type": "boolean"},
        "map_use_offline": {"type": "boolean"},
        "kismet_logdir": {"type": "string", "minLength": 1},
        "bettercap_caplet": {"type": "string", "minLength": 1},
        "dashboard_layout": {"type": "array"},
        "debug_mode": {"type": "boolean"},
        "offline_tile_path": {"type": "string", "minLength": 1},
        "health_poll_interval": {"type": "integer", "minimum": 1},
        "log_rotate_interval": {"type": "integer", "minimum": 1},
        "log_rotate_archives": {"type": "integer", "minimum": 1},
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
        raw = os.getenv(f"PW_{key.upper()}")
        if raw is not None:
            result[key] = _parse_env_value(raw, default)
    return result



def _parse_env_value(raw: str, default: Any) -> Any:
    """Convert ``raw`` environment value to the type of ``default``."""
    if isinstance(default, bool):
        return raw.lower() in {"1", "true", "yes", "on"}
    if isinstance(default, int):
        try:
            return int(raw)
        except ValueError:
            return default
    if isinstance(default, list):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return raw


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
        validate_config_data(merged)
        return cls(**merged)

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a plain dictionary."""
        return {field: getattr(self, field) for field in DEFAULTS.keys()}
