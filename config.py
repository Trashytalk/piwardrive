"""Application configuration helpers with env overrides."""

import json
import os
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

import jsonschema

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")
ACTIVE_PROFILE_FILE = os.path.join(CONFIG_DIR, "active_profile")

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


def _profile_path(name: str) -> str:
    return os.path.join(PROFILES_DIR, f"{os.path.basename(name)}.json")


def list_profiles() -> List[str]:
    """Return available profile names under ``PROFILES_DIR``."""
    if not os.path.isdir(PROFILES_DIR):
        return []
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(PROFILES_DIR)
        if f.endswith(".json")
    ]


def get_active_profile() -> Optional[str]:
    """Return the active profile name if set."""
    env = os.getenv("PW_PROFILE_NAME")
    if env:
        return env
    try:
        with open(ACTIVE_PROFILE_FILE, "r", encoding="utf-8") as f:
            name = f.read().strip()
            return name or None
    except FileNotFoundError:
        return None


def set_active_profile(name: str) -> None:
    """Persist ``name`` as the active profile."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(ACTIVE_PROFILE_FILE, "w", encoding="utf-8") as f:
        f.write(name)


def load_config(profile: Optional[str] = None) -> Config:
    """Load configuration from ``profile`` or ``CONFIG_PATH``."""

    if profile is None:
        profile = get_active_profile()
    path = _profile_path(profile) if profile else CONFIG_PATH

    data: Dict[str, Any] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        jsonschema.validate(loaded, CONFIG_SCHEMA)
        data = loaded
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, jsonschema.ValidationError):
        pass
    merged = {**DEFAULTS, **data}
    return Config(**merged)


def save_config(config: Config, profile: Optional[str] = None) -> None:
    """Persist ``config`` dataclass to ``profile`` or ``CONFIG_PATH``."""
    if profile is None:
        profile = get_active_profile()
    path = _profile_path(profile) if profile else CONFIG_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
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

    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration with environment overrides."""
        file_cfg = asdict(load_config())
        merged = _apply_env_overrides(file_cfg)
        return cls(**merged)

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as a plain dictionary."""
        return {field: getattr(self, field) for field in DEFAULTS.keys()}


def switch_profile(name: str) -> Config:
    """Set ``name`` as active and load its configuration."""
    set_active_profile(name)
    return load_config(profile=name)


def export_profile(name: str, dest: str) -> None:
    """Write ``name`` profile to ``dest`` path."""
    src = _profile_path(name)
    with open(src, "r", encoding="utf-8") as fsrc, open(
        dest, "w", encoding="utf-8"
    ) as fdst:
        fdst.write(fsrc.read())


def import_profile(path: str, name: Optional[str] = None) -> str:
    """Import a profile from ``path`` and save as ``name``."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    jsonschema.validate(data, CONFIG_SCHEMA)
    cfg = Config(**{**DEFAULTS, **data})
    if name is None:
        name = os.path.splitext(os.path.basename(path))[0]
    save_config(cfg, profile=name)
    return name


def delete_profile(name: str) -> None:
    """Remove the specified profile file."""
    try:
        os.remove(_profile_path(name))
    except FileNotFoundError:
        pass
