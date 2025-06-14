"""Application configuration helpers with env overrides and validation."""

import json
import os
from dataclasses import dataclass, asdict, field

from pathlib import Path
from typing import Any, Dict, List, Optional


from pydantic import BaseModel, Field, ValidationError, field_validator

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")
ACTIVE_PROFILE_FILE = os.path.join(CONFIG_DIR, "active_profile")

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "theme": {"type": "string"},
        "map_poll_gps": {"type": "integer"},
        "map_poll_gps_max": {"type": "integer"},
        "map_poll_aps": {"type": "integer"},
        "map_poll_bt": {"type": "integer"},
        "map_show_gps": {"type": "boolean"},
        "map_show_aps": {"type": "boolean"},
        "map_show_bt": {"type": "boolean"},
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
    map_poll_gps_max: int = 30
    map_poll_aps: int = 60
    map_poll_bt: int = 60
    map_show_gps: bool = True
    map_show_aps: bool = True
    map_show_bt: bool = False
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


def _parse_env_value(raw: str, default: Any) -> Any:
    """Convert environment string ``raw`` to the type of ``default``."""
    if isinstance(default, bool):
        low = raw.lower()
        if low in {"1", "true", "yes", "on"}:
            return True
        if low in {"0", "false", "no", "off"}:
            return False
        raise ValueError(f"Invalid boolean value: {raw}")
    if isinstance(default, int):
        val = int(raw)
        if val < 1:
            raise ValueError("Value must be positive")
        return val

class FileConfigModel(BaseModel):
    """Validation model for configuration files."""

    theme: Optional[str] = None
    map_poll_gps: Optional[int] = None
    map_poll_gps_max: Optional[int] = None
    map_poll_aps: Optional[int] = None
    map_show_gps: Optional[bool] = None
    map_show_aps: Optional[bool] = None
    map_cluster_aps: Optional[bool] = None
    map_use_offline: Optional[bool] = None
    kismet_logdir: Optional[str] = Field(default=None, min_length=1)
    bettercap_caplet: Optional[str] = Field(default=None, min_length=1)
    dashboard_layout: List[Any] = Field(default_factory=list)
    debug_mode: Optional[bool] = None
    offline_tile_path: Optional[str] = Field(default=None, min_length=1)
    health_poll_interval: Optional[int] = Field(default=None, ge=1)
    log_rotate_interval: Optional[int] = Field(default=None, ge=1)
    log_rotate_archives: Optional[int] = Field(default=None, ge=1)
    widget_battery_status: Optional[bool] = None
    admin_password_hash: Optional[str] = ""


class ConfigModel(FileConfigModel):
    """Extended validation used by :func:`validate_config_data`."""

    map_poll_gps: int = Field(..., gt=0)

    @field_validator("theme")
    def check_theme(cls, value: str) -> str:
        if value not in {"Dark", "Light", "Green", "Red"}:
            raise ValueError(f"Invalid theme: {value}")
        return value


def _parse_env_value(raw: str, default: Any) -> Any:
    """Return ``raw`` converted to the type of ``default``."""
    if isinstance(default, bool):
        return raw.lower() in {"1", "true", "yes", "on"}
    if isinstance(default, int):
        try:
            return int(raw)
        except ValueError:
            return default
    if isinstance(default, float):
        try:
            return float(raw)
        except ValueError:
            return default
    if isinstance(default, list):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return default
    return raw


def validate_config_data(data: Dict[str, Any]) -> None:
    """Validate configuration values using :class:`ConfigModel`."""
    ConfigModel(**data)



def _apply_env_overrides(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``cfg`` with PW_<KEY> environment overrides."""
    result = dict(cfg)
    for key, default in DEFAULTS.items():
        raw = os.getenv(f"PW_{key.upper()}")
        if raw is not None:
            result[key] = _parse_env_value(raw, default)
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
        FileConfigModel(**loaded)
        data = loaded
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, ValidationError):
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


def export_config(config: Config, path: str) -> None:
    """Export ``config`` to ``path`` in JSON or YAML format."""
    ext = Path(path).suffix.lower()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = asdict(config)
    if ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    elif ext in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dep
            raise RuntimeError("PyYAML required for YAML export") from exc
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)
    else:
        raise ValueError(f"Unsupported export format: {ext}")


def import_config(path: str) -> Config:
    """Load configuration from ``path`` (JSON or YAML)."""
    ext = Path(path).suffix.lower()
    with open(path, "r", encoding="utf-8") as f:
        if ext == ".json":
            data = json.load(f)
        elif ext in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except Exception as exc:  # pragma: no cover - optional dep
                raise RuntimeError("PyYAML required for YAML import") from exc
            data = yaml.safe_load(f) or {}
        else:
            raise ValueError(f"Unsupported config format: {ext}")
    FileConfigModel(**data)
    merged = {**DEFAULTS, **data}
    return Config(**merged)


@dataclass
class AppConfig:
    """Typed configuration container."""

    theme: str = DEFAULTS["theme"]
    map_poll_gps: int = DEFAULTS["map_poll_gps"]
    map_poll_gps_max: int = DEFAULTS["map_poll_gps_max"]
    map_poll_aps: int = DEFAULTS["map_poll_aps"]
    map_poll_bt: int = DEFAULTS["map_poll_bt"]
    map_show_gps: bool = DEFAULTS["map_show_gps"]
    map_show_aps: bool = DEFAULTS["map_show_aps"]
    map_show_bt: bool = DEFAULTS["map_show_bt"]
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
    FileConfigModel(**data)
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
