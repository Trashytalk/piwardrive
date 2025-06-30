"""Application configuration helpers with env overrides and validation."""

import json
import os
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

from ..errors import ConfigError


class Theme(str, Enum):
    """Available UI themes."""

    Dark = "Dark"  # noqa: V107
    Light = "Light"  # noqa: V107
    Green = "Green"  # noqa: V107
    Red = "Red"  # noqa: V107


CONFIG_DIR = str(Path.home() / ".config" / "piwardrive")
CONFIG_PATH = str(Path(CONFIG_DIR) / "config.json")
PROFILES_DIR = str(Path(CONFIG_DIR) / "profiles")
ACTIVE_PROFILE_FILE = str(Path(CONFIG_DIR) / "active_profile")
REPORTS_DIR = str(Path(CONFIG_DIR) / "reports")  # noqa: V107
HEALTH_EXPORT_DIR = str(Path(CONFIG_DIR) / "health_exports")
HEALTH_EXPORT_INTERVAL = 6  # hours
COMPRESS_HEALTH_EXPORTS = True
HEALTH_EXPORT_RETENTION = 7
TILE_MAINTENANCE_INTERVAL = 604800  # seconds
TILE_MAX_AGE_DAYS = 30
TILE_CACHE_LIMIT_MB = 512
COMPRESS_OFFLINE_TILES = True
ROUTE_PREFETCH_INTERVAL = 3600  # seconds
ROUTE_PREFETCH_LOOKAHEAD = 5
REMOTE_SYNC_INTERVAL = 60  # minutes
HANDSHAKE_CACHE_SECONDS_DEFAULT = 10.0
LOG_TAIL_CACHE_SECONDS_DEFAULT = 1.0

# Cloud upload defaults
CLOUD_BUCKET = ""
CLOUD_PREFIX = ""
CLOUD_PROFILE = ""


def get_config_path(profile: Optional[str] = None) -> str:
    """Return path to ``profile`` or the main ``config.json``."""
    if profile is None:
        profile = get_active_profile()
    return _profile_path(profile) if profile else CONFIG_PATH


def config_mtime(profile: Optional[str] = None) -> Optional[float]:  # noqa: V103
    """Return modification time for the active config file if it exists."""
    path = get_config_path(profile)
    try:
        return Path(path).stat().st_mtime
    except FileNotFoundError:
        return None


@dataclass
class Config:
    """Persistent application configuration."""

    theme: str = "Dark"  # noqa: V107
    map_poll_gps: int = 10  # noqa: V107
    map_poll_gps_max: int = 30  # noqa: V107
    map_poll_aps: int = 60  # noqa: V107
    map_poll_bt: int = 60  # noqa: V107
    map_poll_wigle: int = 0  # noqa: V107
    map_show_gps: bool = True  # noqa: V107
    map_follow_gps: bool = True  # noqa: V107
    map_show_aps: bool = True  # noqa: V107
    map_show_bt: bool = False  # noqa: V107
    map_show_wigle: bool = False  # noqa: V107
    map_show_heatmap: bool = False  # noqa: V107
    map_cluster_aps: bool = False  # noqa: V107
    map_cluster_capacity: int = 8  # noqa: V107
    map_use_offline: bool = False  # noqa: V107
    map_auto_prefetch: bool = False  # noqa: V107
    disable_scanning: bool = False  # noqa: V107
    kismet_logdir: str = "/mnt/ssd/kismet_logs"  # noqa: V107
    bettercap_caplet: str = "/usr/local/etc/bettercap/alfa.cap"  # noqa: V107
    dashboard_layout: List[Any] = field(default_factory=list)  # noqa: V107
    debug_mode: bool = False  # noqa: V107
    offline_tile_path: str = "/mnt/ssd/tiles/offline.mbtiles"  # noqa: V107
    log_paths: List[str] = field(
        default_factory=lambda: [
            "/var/log/syslog",
            "/var/log/kismet.log",
            "/var/log/bettercap.log",
        ]
    )
    health_poll_interval: int = 10  # noqa: V107
    log_rotate_interval: int = 3600  # noqa: V107
    log_rotate_archives: int = 3  # noqa: V107
    cleanup_rotated_logs: bool = True  # noqa: V107
    reports_dir: str = REPORTS_DIR  # noqa: V107
    health_export_interval: int = HEALTH_EXPORT_INTERVAL  # noqa: V107
    health_export_dir: str = HEALTH_EXPORT_DIR  # noqa: V107
    compress_health_exports: bool = COMPRESS_HEALTH_EXPORTS  # noqa: V107
    health_export_retention: int = HEALTH_EXPORT_RETENTION  # noqa: V107
    tile_maintenance_interval: int = TILE_MAINTENANCE_INTERVAL  # noqa: V107
    tile_max_age_days: int = TILE_MAX_AGE_DAYS  # noqa: V107
    tile_cache_limit_mb: int = TILE_CACHE_LIMIT_MB  # noqa: V107
    compress_offline_tiles: bool = COMPRESS_OFFLINE_TILES  # noqa: V107
    route_prefetch_interval: int = ROUTE_PREFETCH_INTERVAL  # noqa: V107
    route_prefetch_lookahead: int = ROUTE_PREFETCH_LOOKAHEAD  # noqa: V107
    widget_battery_status: bool = False  # noqa: V107
    ui_font_size: int = 16  # noqa: V107
    admin_password_hash: str = ""  # noqa: V107
    remote_sync_url: str = ""  # noqa: V107
    remote_sync_token: str = ""  # noqa: V107
    remote_sync_timeout: int = 5  # noqa: V107
    remote_sync_retries: int = 3  # noqa: V107
    remote_sync_interval: int = REMOTE_SYNC_INTERVAL  # noqa: V107
    handshake_cache_seconds: float = HANDSHAKE_CACHE_SECONDS_DEFAULT  # noqa: V107
    log_tail_cache_seconds: float = LOG_TAIL_CACHE_SECONDS_DEFAULT  # noqa: V107
    wigle_api_name: str = ""  # noqa: V107
    wigle_api_key: str = ""  # noqa: V107
    gps_movement_threshold: float = 1.0  # noqa: V107
    cloud_bucket: str = CLOUD_BUCKET  # noqa: V107
    cloud_prefix: str = CLOUD_PREFIX  # noqa: V107
    cloud_profile: str = CLOUD_PROFILE  # noqa: V107
    mysql_host: str = "localhost"  # noqa: V107
    mysql_port: int = 3306  # noqa: V107
    mysql_user: str = "piwardrive"  # noqa: V107
    mysql_password: str = ""  # noqa: V107
    mysql_db: str = "piwardrive"  # noqa: V107
    scan_rules: Dict[str, Any] = field(default_factory=dict)  # noqa: V107


DEFAULT_CONFIG = Config()
DEFAULTS = asdict(DEFAULT_CONFIG)

# Mapping of environment variable names to configuration keys
ENV_OVERRIDE_MAP: Dict[str, str] = {
    f"PW_{name.upper()}": name for name in DEFAULTS.keys()
}


def list_env_overrides() -> Dict[str, str]:
    """Return available ``PW_`` environment variable overrides."""
    return dict(ENV_OVERRIDE_MAP)


class FileConfigModel(BaseModel):
    """Validation model for configuration files."""

    theme: Optional[str] = None
    map_poll_gps: Optional[int] = None
    map_poll_gps_max: Optional[int] = None
    map_poll_aps: Optional[int] = None
    map_poll_wigle: Optional[int] = None
    map_show_gps: Optional[bool] = None
    map_follow_gps: Optional[bool] = None
    map_show_aps: Optional[bool] = None
    map_cluster_aps: Optional[bool] = None
    map_show_heatmap: Optional[bool] = None
    map_show_wigle: Optional[bool] = None
    map_cluster_capacity: Optional[int] = Field(default=None, ge=1)
    map_use_offline: Optional[bool] = None
    map_auto_prefetch: Optional[bool] = None
    disable_scanning: Optional[bool] = None
    kismet_logdir: Optional[str] = Field(default=None, min_length=1)
    bettercap_caplet: Optional[str] = Field(default=None, min_length=1)
    dashboard_layout: List[Any] = Field(default_factory=list)
    debug_mode: Optional[bool] = None
    offline_tile_path: Optional[str] = Field(default=None, min_length=1)
    health_poll_interval: Optional[int] = Field(default=None, ge=1)
    log_rotate_interval: Optional[int] = Field(default=None, ge=1)
    log_rotate_archives: Optional[int] = Field(default=None, ge=1)
    cleanup_rotated_logs: Optional[bool] = None
    reports_dir: Optional[str] = Field(default=None, min_length=1)
    health_export_interval: Optional[int] = Field(default=None, ge=1)
    health_export_dir: Optional[str] = Field(default=None, min_length=1)
    compress_health_exports: Optional[bool] = None
    health_export_retention: Optional[int] = Field(default=None, ge=1)
    tile_maintenance_interval: Optional[int] = Field(default=None, ge=1)
    tile_max_age_days: Optional[int] = Field(default=None, ge=1)
    tile_cache_limit_mb: Optional[int] = Field(default=None, ge=1)
    compress_offline_tiles: Optional[bool] = None
    route_prefetch_interval: Optional[int] = Field(default=None, ge=1)
    route_prefetch_lookahead: Optional[int] = Field(default=None, ge=1)
    widget_battery_status: Optional[bool] = None
    log_paths: List[str] = Field(default_factory=list)
    ui_font_size: Optional[int] = Field(default=None, ge=1)
    admin_password_hash: Optional[str] = ""
    remote_sync_url: Optional[str] = Field(default=None, min_length=1)
    remote_sync_token: Optional[str] = None
    remote_sync_timeout: Optional[int] = Field(default=None, ge=1)
    remote_sync_retries: Optional[int] = Field(default=None, ge=1)
    remote_sync_interval: Optional[int] = Field(default=None, ge=1)
    handshake_cache_seconds: Optional[float] = Field(default=None, ge=0)
    log_tail_cache_seconds: Optional[float] = Field(default=None, ge=0)
    wigle_api_name: Optional[str] = None
    wigle_api_key: Optional[str] = None
    gps_movement_threshold: Optional[float] = Field(default=None, gt=0)
    cloud_bucket: Optional[str] = None
    cloud_prefix: Optional[str] = None
    cloud_profile: Optional[str] = None
    mysql_host: Optional[str] = None
    mysql_port: Optional[int] = Field(default=None, ge=1)
    mysql_user: Optional[str] = None
    mysql_password: Optional[str] = None
    mysql_db: Optional[str] = None
    scan_rules: Dict[str, Any] = Field(default_factory=dict)


class ConfigModel(FileConfigModel):
    """Extended validation used by :func:`validate_config_data`."""

    map_poll_gps: int = Field(..., gt=0)
    map_poll_wigle: int = Field(default=0, ge=0)
    map_cluster_capacity: int = Field(default=8, ge=1)
    ui_font_size: int = Field(default=16, ge=1)
    log_paths: List[str] = Field(default_factory=list)
    health_export_interval: int = Field(default=6, ge=1)
    health_export_dir: str = DEFAULTS["health_export_dir"]
    reports_dir: str = DEFAULTS["reports_dir"]
    compress_health_exports: bool = DEFAULTS["compress_health_exports"]
    health_export_retention: int = Field(default=7, ge=1)
    map_auto_prefetch: bool = DEFAULTS["map_auto_prefetch"]
    map_follow_gps: bool = DEFAULTS["map_follow_gps"]
    map_show_wigle: bool = DEFAULTS["map_show_wigle"]
    handshake_cache_seconds: float = Field(
        default=DEFAULTS["handshake_cache_seconds"], ge=0
    )
    log_tail_cache_seconds: float = Field(
        default=DEFAULTS["log_tail_cache_seconds"], ge=0
    )
    mysql_host: str = DEFAULTS["mysql_host"]
    mysql_port: int = Field(default=DEFAULTS["mysql_port"], ge=1)
    mysql_user: str = DEFAULTS["mysql_user"]
    mysql_password: str = DEFAULTS["mysql_password"]
    mysql_db: str = DEFAULTS["mysql_db"]
    scan_rules: Dict[str, Any] = field(default_factory=dict)
    scan_rules: Dict[str, Any] = Field(default_factory=dict)

    theme: Theme

    @field_validator("theme", mode="before")
    def check_theme(cls, value: Any) -> Theme:
        """Validate that ``value`` is a known :class:`Theme`."""
        try:
            return Theme(value)
        except Exception as exc:  # pragma: no cover - should raise
            raise ConfigError(f"Invalid theme: {value}") from exc


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
    if data.get("remote_sync_url") == "":
        data["remote_sync_url"] = None
    ConfigModel(**data)


def _apply_env_overrides(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``cfg`` with ``PW_`` environment overrides."""
    result = dict(cfg)
    for env_var, key in ENV_OVERRIDE_MAP.items():
        default = DEFAULTS[key]
        raw = os.getenv(env_var)
        if raw is not None:
            if key == "theme":
                try:
                    result[key] = Theme(raw)
                except ValueError:
                    result[key] = raw
            else:
                result[key] = _parse_env_value(raw, default)
        elif key == "remote_sync_url" and result.get(key, default) == "":
            # Allow missing remote sync URL
            result[key] = None
    return result


def _profile_path(name: str) -> str:
    return str(Path(PROFILES_DIR) / f"{Path(name).stem}.json")


def list_profiles() -> List[str]:
    """Return available profile names under ``PROFILES_DIR``."""
    profiles_dir = Path(PROFILES_DIR)
    if not profiles_dir.is_dir():
        return []
    return [p.stem for p in profiles_dir.iterdir() if p.suffix == ".json"]


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
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    with open(ACTIVE_PROFILE_FILE, "w", encoding="utf-8") as f:
        f.write(name)


def load_config(profile: Optional[str] = None) -> Config:
    """Load configuration from ``profile`` or ``CONFIG_PATH``."""
    if profile is None:
        profile = get_active_profile()
    path = get_config_path(profile)

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
    path = get_config_path(profile)
    data = asdict(config)
    validate_config_data(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def export_config(config: Config, path: str) -> None:
    """Export ``config`` to ``path`` in JSON or YAML format."""
    ext = Path(path).suffix.lower()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    data = asdict(config)
    if ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    elif ext in {".yaml", ".yml"}:
        try:
            import yaml
        except Exception as exc:  # pragma: no cover - optional dep
            raise ConfigError("PyYAML required for YAML export") from exc
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)
    else:
        raise ConfigError(f"Unsupported export format: {ext}")


def import_config(path: str) -> Config:
    """Load configuration from ``path`` (JSON or YAML)."""
    ext = Path(path).suffix.lower()
    with open(path, "r", encoding="utf-8") as f:
        if ext == ".json":
            data = json.load(f)
        elif ext in {".yaml", ".yml"}:
            try:
                import yaml
            except Exception as exc:  # pragma: no cover - optional dep
                raise ConfigError("PyYAML required for YAML import") from exc
            data = yaml.safe_load(f) or {}
        else:
            raise ConfigError(f"Unsupported config format: {ext}")
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
    map_poll_wigle: int = DEFAULTS["map_poll_wigle"]
    map_show_gps: bool = DEFAULTS["map_show_gps"]
    map_follow_gps: bool = DEFAULTS["map_follow_gps"]
    map_show_aps: bool = DEFAULTS["map_show_aps"]
    map_show_bt: bool = DEFAULTS["map_show_bt"]
    map_show_heatmap: bool = DEFAULTS["map_show_heatmap"]
    map_show_wigle: bool = DEFAULTS["map_show_wigle"]
    map_cluster_aps: bool = DEFAULTS["map_cluster_aps"]
    map_cluster_capacity: int = DEFAULTS["map_cluster_capacity"]
    map_use_offline: bool = DEFAULTS["map_use_offline"]
    map_auto_prefetch: bool = DEFAULTS["map_auto_prefetch"]
    disable_scanning: bool = DEFAULTS["disable_scanning"]
    offline_tile_path: str = DEFAULTS["offline_tile_path"]
    kismet_logdir: str = DEFAULTS["kismet_logdir"]
    bettercap_caplet: str = DEFAULTS["bettercap_caplet"]
    dashboard_layout: List[Any] = field(default_factory=list)
    debug_mode: bool = DEFAULTS["debug_mode"]
    health_poll_interval: int = DEFAULTS["health_poll_interval"]
    log_paths: List[str] = field(default_factory=lambda: DEFAULTS["log_paths"])
    log_rotate_interval: int = DEFAULTS["log_rotate_interval"]
    log_rotate_archives: int = DEFAULTS["log_rotate_archives"]
    cleanup_rotated_logs: bool = DEFAULTS["cleanup_rotated_logs"]
    reports_dir: str = DEFAULTS["reports_dir"]
    health_export_interval: int = DEFAULTS["health_export_interval"]
    health_export_dir: str = DEFAULTS["health_export_dir"]
    compress_health_exports: bool = DEFAULTS["compress_health_exports"]
    health_export_retention: int = DEFAULTS["health_export_retention"]
    tile_maintenance_interval: int = DEFAULTS["tile_maintenance_interval"]
    tile_max_age_days: int = DEFAULTS["tile_max_age_days"]
    tile_cache_limit_mb: int = DEFAULTS["tile_cache_limit_mb"]
    compress_offline_tiles: bool = DEFAULTS["compress_offline_tiles"]
    route_prefetch_interval: int = DEFAULTS["route_prefetch_interval"]
    route_prefetch_lookahead: int = DEFAULTS["route_prefetch_lookahead"]
    widget_battery_status: bool = DEFAULTS["widget_battery_status"]
    ui_font_size: int = DEFAULTS["ui_font_size"]
    admin_password_hash: str = DEFAULTS.get("admin_password_hash", "")
    remote_sync_url: str = DEFAULTS["remote_sync_url"]
    remote_sync_token: str = DEFAULTS["remote_sync_token"]
    remote_sync_timeout: int = DEFAULTS["remote_sync_timeout"]
    remote_sync_retries: int = DEFAULTS["remote_sync_retries"]
    remote_sync_interval: int = DEFAULTS["remote_sync_interval"]
    handshake_cache_seconds: float = DEFAULTS["handshake_cache_seconds"]
    log_tail_cache_seconds: float = DEFAULTS["log_tail_cache_seconds"]
    wigle_api_name: str = DEFAULTS["wigle_api_name"]
    wigle_api_key: str = DEFAULTS["wigle_api_key"]
    gps_movement_threshold: float = DEFAULTS["gps_movement_threshold"]
    cloud_bucket: str = DEFAULTS["cloud_bucket"]
    cloud_prefix: str = DEFAULTS["cloud_prefix"]
    cloud_profile: str = DEFAULTS["cloud_profile"]
    mysql_host: str = DEFAULTS["mysql_host"]
    mysql_port: int = DEFAULTS["mysql_port"]
    mysql_user: str = DEFAULTS["mysql_user"]
    mysql_password: str = DEFAULTS["mysql_password"]
    mysql_db: str = DEFAULTS["mysql_db"]

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
    with (
        open(src, "r", encoding="utf-8") as fsrc,
        open(dest, "w", encoding="utf-8") as fdst,
    ):
        fdst.write(fsrc.read())


def import_profile(path: str, name: Optional[str] = None) -> str:
    """Import a profile from ``path`` and save as ``name``."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    FileConfigModel(**data)
    cfg = Config(**{**DEFAULTS, **data})
    if name is None:
        name = Path(path).stem
    save_config(cfg, profile=name)
    return name


def delete_profile(name: str) -> None:
    """Remove the specified profile file."""
    try:
        os.remove(_profile_path(name))
    except FileNotFoundError:
        pass
