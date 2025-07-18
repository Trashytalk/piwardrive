from flask import Blueprint, jsonify, request

from piwardrive.logging.dynamic_config import DynamicLogConfig
from piwardrive.logging.levels import LogLevelManager

logging_api = Blueprint("logging", __name__, url_prefix="/api/logging")

# Assume log_config and log_manager are created elsewhere and imported
log_config = DynamicLogConfig("log_config.json")
log_manager = LogLevelManager(log_config.get_level_config())


@logging_api.route("/levels", methods=["GET"])
def get_log_levels():
    """Get current log levels for all components."""
    return jsonify(log_config.get_level_config())


@logging_api.route("/levels/<component>", methods=["PUT"])
def set_component_level(component: str):
    """Set log level for specific component."""
    _data = request.get_json()
    level = _data.get("level")

    if level not in ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        return jsonify({"error": "Invalid log level"}), 400

    log_config.update_component_level(component, level)
    return jsonify({"status": "updated", "component": component, "level": level})


@logging_api.route("/filters", methods=["GET"])
def get_filters():
    """Get current filter configuration."""
    return jsonify(log_config.get_filter_config())


@logging_api.route("/filters", methods=["PUT"])
def update_filters():
    """Update filter configuration."""
    request.get_json()
    # Implementation for updating filters
    return jsonify({"status": "updated"})
