# Comprehensive Code Quality Analysis Report

## Summary
- Files with issues: 524
- Total issues found: 4582

## Undefined Names

No issues found.

## Unused Variables

No issues found.

## Import Issues

### comprehensive_qa_fix.py
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.Set'
- Line 11: Unused import 'typing.Tuple'

### comprehensive_code_analyzer.py
- Line 10: Unused import 'sys'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.List'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Set'
- Line 12: Unused import 'typing.Tuple'
- Line 14: Unused import 'json'

### fix_remaining_syntax.py
- Line 6: Unused import 'os'
- Line 8: Unused import 'ast'
- Line 9: Unused import 'pathlib.Path'

### main.py
- Line 16: Unused import '__future__.annotations'

### fix_issues.py
- Line 6: Unused import 'pathlib.Path'

### test_imports.py
- Line 6: Unused import 'time'

### fix_undefined.py
- Line 6: Unused import 'pathlib.Path'

### service.py
- Line 10: Unused import '__future__.annotations'

### quality_summary.py
- Line 6: Unused import 'pathlib.Path'

### fix_syntax_errors.py
- Line 8: Unused import 'sys'
- Line 9: Unused import 'pathlib.Path'

### tools/performance_demo.py
- Line 14: Unused import 'pathlib.Path'

### tools/sync.py
- Line 1: Unused import 'piwardrive.sync.*'

### tools/setup_performance_dashboard.py
- Line 12: Unused import 'pathlib.Path'

### tools/setup.py
- Line 3: Unused import 'pathlib.Path'
- Line 10: Unused import 'tomli'

### tools/sync_receiver.py
- Line 4: Unused import 'fastapi.FastAPI'
- Line 4: Unused import 'fastapi.HTTPException'
- Line 4: Unused import 'fastapi.UploadFile'

### tools/exception_handler.py
- Line 3: Unused import '__future__.annotations'

### tests/test_load_kismet_data.py
- Line 3: Unused import 'pathlib.Path'
- Line 5: Unused import 'piwardrive.advanced_localization.load_kismet_data'

### tests/test_cli_tools.py
- Line 4: Unused import 'types.SimpleNamespace'

### tests/test_route_optimizer.py
- Line 3: Unused import 'piwardrive.route_optimizer'

### tests/test_config_watcher.py
- Line 3: Unused import 'piwardrive.config_watcher.watch_config'

### tests/test_integration_comprehensive.py
- Line 18: Unused import 'contextlib.contextmanager'
- Line 19: Unused import 'pathlib.Path'
- Line 20: Unused import 'unittest.mock.patch'
- Line 498: Duplicate import 'os'

### tests/test_rf_utils.py
- Line 1: Unused import 'numpy'

### tests/test_webui_server_main.py
- Line 3: Unused import 'types.ModuleType'
- Line 4: Unused import 'unittest.mock.Mock'

### tests/test_service_main.py
- Line 4: Unused import 'types.ModuleType'
- Line 5: Unused import 'unittest.mock.AsyncMock'

### tests/test_diagnostics.py
- Line 7: Unused import 'types.ModuleType'
- Line 7: Unused import 'types.SimpleNamespace'
- Line 8: Unused import 'unittest.mock'
- Line 15: Unused import 'typing.Any'
- Line 19: Unused import 'piwardrive.diagnostics'

### tests/test_interfaces.py
- Line 9: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock'

### tests/test_orientation_sensors_pkg.py
- Line 3: Unused import 'importlib.reload'
- Line 5: Unused import 'piwardrive.orientation_sensors'

### tests/test_db_stats_widget.py
- Line 3: Unused import 'typing.Any'

### tests/test_kiosk_cli.py
- Line 4: Unused import 'pathlib.Path'

### tests/test_security.py
- Line 5: Unused import 'piwardrive.security'

### tests/test_core_application.py
- Line 8: Unused import 'tempfile'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.call'
- Line 12: Unused import 'dataclasses.asdict'

### tests/test_security_system.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.mock_open'

### tests/test_main_simple.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 58: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 82: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 85: Duplicate import 'piwardrive.di.Container'
- Line 177: Duplicate import 'piwardrive.config.Config'
- Line 195: Duplicate import 'piwardrive.persistence.AppState'
- Line 297: Duplicate import 'pathlib.Path'
- Line 18: Duplicate import 'piwardrive.main'
- Line 272: Duplicate import 'piwardrive.main'

### tests/test_widget_cache.py
- Line 3: Unused import 'pathlib.Path'
- Line 4: Unused import 'types.ModuleType'

### tests/test_config_env_webhooks.py
- Line 1: Unused import 'pathlib.Path'
- Line 21: Duplicate import 'piwardrive.config'

### tests/test_iot_analytics.py
- Line 4: Unused import 'piwardrive.analytics.iot.correlate_city_services'
- Line 4: Unused import 'piwardrive.analytics.iot.fingerprint_iot_devices'

### tests/test_aggregation_service_main_new.py
- Line 3: Unused import 'unittest.mock.AsyncMock'

### tests/test_config_runtime.py
- Line 1: Unused import 'pathlib.Path'
- Line 3: Unused import 'piwardrive.config'

### tests/test_direction_finding.py
- Line 1: Unused import 'logging'
- Line 10: Unused import 'unittest.mock.MagicMock'
- Line 10: Unused import 'unittest.mock.Mock'
- Line 10: Unused import 'unittest.mock.patch'
- Line 189: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 208: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 218: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 243: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 243: Duplicate import 'piwardrive.direction_finding.config.SignalMappingConfig'
- Line 243: Duplicate import 'piwardrive.direction_finding.config.TriangulationConfig'
- Line 262: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 262: Duplicate import 'piwardrive.direction_finding.config.SignalMappingConfig'
- Line 262: Duplicate import 'piwardrive.direction_finding.config.TriangulationConfig'
- Line 282: Duplicate import 'piwardrive.direction_finding.config.PathLossConfig'
- Line 282: Duplicate import 'piwardrive.direction_finding.config.SignalMappingConfig'
- Line 282: Duplicate import 'piwardrive.direction_finding.config.TriangulationConfig'

### tests/test_utils.py
- Line 10: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Any'
- Line 13: Unused import 'unittest.mock'
- Line 18: Unused import 'cachetools.TTLCache'
- Line 35: Unused import 'collections.namedtuple'
- Line 580: Duplicate import 'piwardrive.core.utils'
- Line 802: Duplicate import 'sys'

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 2: Unused import 'pathlib.Path'
- Line 3: Unused import 'types.ModuleType'

### tests/test_logconfig.py
- Line 5: Unused import 'typing.Any'
- Line 7: Unused import 'piwardrive.logconfig.setup_logging'

### tests/test_main_application.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.MagicMock'
- Line 9: Unused import 'pathlib.Path'

### tests/test_tower_tracking.py
- Line 2: Unused import 'logging'

### tests/test_jwt_utils_fixed.py
- Line 18: Unused import 'pytest'
- Line 24: Unused import 'piwardrive.jwt_utils'
- Line 41: Duplicate import 'importlib'
- Line 48: Duplicate import 'importlib'
- Line 55: Duplicate import 'importlib'
- Line 62: Duplicate import 'importlib'
- Line 69: Duplicate import 'importlib'
- Line 76: Duplicate import 'importlib'
- Line 83: Duplicate import 'importlib'

### tests/test_web_server_main.py
- Line 3: Unused import 'types.ModuleType'
- Line 4: Unused import 'unittest.mock.Mock'

### tests/test_vehicle_sensors.py
- Line 3: Unused import 'piwardrive.vehicle_sensors'

### tests/test_core_config.py
- Line 9: Unused import 'tempfile'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 12: Unused import 'dataclasses.asdict'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.Any'

### tests/test_service_direct_import.py
- Line 12: Unused import 'pathlib.Path'

### tests/test_advanced_localization.py
- Line 1: Unused import 'numpy'
- Line 2: Unused import 'pandas'
- Line 4: Unused import 'piwardrive.advanced_localization.Config'
- Line 4: Unused import 'piwardrive.advanced_localization._kalman_1d'
- Line 4: Unused import 'piwardrive.advanced_localization.apply_kalman_filter'
- Line 4: Unused import 'piwardrive.advanced_localization.estimate_ap_location_centroid'
- Line 4: Unused import 'piwardrive.advanced_localization.localize_aps'
- Line 4: Unused import 'piwardrive.advanced_localization.remove_outliers'
- Line 4: Unused import 'piwardrive.advanced_localization.rssi_to_distance'

### tests/test_kalman.py
- Line 1: Unused import 'numpy'
- Line 3: Unused import 'piwardrive.advanced_localization._kalman_1d'

### tests/test_fingerprint_persistence.py
- Line 3: Unused import 'pathlib.Path'
- Line 5: Unused import 'piwardrive.persistence'

### tests/test_service_simple.py
- Line 12: Unused import 'pathlib.Path'
- Line 174: Duplicate import 'os'
- Line 187: Duplicate import 'fastapi.FastAPI'
- Line 188: Duplicate import 'fastapi.middleware.cors.CORSMiddleware'
- Line 189: Duplicate import 'os'
- Line 39: Duplicate import 'fastapi.FastAPI'
- Line 40: Duplicate import 'fastapi.middleware.cors.CORSMiddleware'
- Line 41: Duplicate import 'os'

### tests/test_export.py
- Line 3: Unused import 'types.ModuleType'
- Line 3: Unused import 'types.SimpleNamespace'
- Line 7: Unused import 'piwardrive.export'

### tests/test_database_counts.py
- Line 4: Unused import 'types.SimpleNamespace'
- Line 28: Duplicate import 'pytest'

### tests/test_band_scanner.py
- Line 3: Unused import 'piwardrive.sigint_suite.cellular.band_scanner.scanner.async_scan_bands'
- Line 3: Unused import 'piwardrive.sigint_suite.cellular.band_scanner.scanner.scan_bands'

### tests/test_cpu_pool.py
- Line 3: Unused import 'piwardrive.cpu_pool.run_cpu_bound'

### tests/test_analysis_queries_service.py
- Line 3: Unused import 'dataclasses.dataclass'

### tests/test_remote_sync.py
- Line 5: Unused import 'types.ModuleType'
- Line 21: Unused import 'piwardrive.remote_sync'
- Line 159: Duplicate import 'sqlite3'
- Line 176: Duplicate import 'sqlite3'
- Line 226: Duplicate import 'sqlite3'
- Line 260: Duplicate import 'os'

### tests/test_analysis_queries_cache.py
- Line 3: Unused import 'types.ModuleType'
- Line 7: Unused import 'piwardrive.services.analysis_queries'

### tests/test_network_analytics.py
- Line 3: Unused import 'piwardrive.network_analytics'

### tests/test_critical_paths.py
- Line 9: Unused import 'unittest.mock.Mock'
- Line 9: Unused import 'unittest.mock.patch'
- Line 9: Unused import 'unittest.mock.MagicMock'
- Line 40: Duplicate import 'piwardrive.core.utils.safe_json_load'
- Line 212: Duplicate import 'piwardrive.task_queue.Task'
- Line 212: Duplicate import 'piwardrive.task_queue.TaskPriority'
- Line 285: Duplicate import 'piwardrive.widget_manager.WidgetManager'
- Line 286: Duplicate import 'piwardrive.widgets.base.BaseWidget'
- Line 485: Duplicate import 'piwardrive.task_queue.TaskPriority'

### tests/test_cache_security_comprehensive.py
- Line 10: Unused import 'pytest'

### tests/test_cloud_export.py
- Line 2: Unused import 'typing.Any'
- Line 6: Unused import 'piwardrive.cloud_export'

### tests/test_utils_comprehensive.py
- Line 16: Unused import 'dataclasses.dataclass'
- Line 246: Duplicate import 'piwardrive.utils'

### tests/test_persistence_comprehensive.py
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.AsyncMock'
- Line 360: Duplicate import 'piwardrive.persistence.FingerprintInfo'
- Line 360: Duplicate import 'piwardrive.persistence.save_fingerprint_info'
- Line 360: Duplicate import 'piwardrive.persistence.load_fingerprint_info'
- Line 360: Duplicate import 'piwardrive.persistence.create_user'
- Line 360: Duplicate import 'piwardrive.persistence.get_user'

### tests/test_scheduler_system.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.MagicMock'
- Line 616: Duplicate import 'os'

### tests/test_vacuum_script.py
- Line 2: Unused import 'types.SimpleNamespace'

### tests/test_health_export.py
- Line 2: Unused import 'dataclasses.asdict'

### tests/test_service_sync.py
- Line 4: Unused import 'dataclasses.asdict'
- Line 4: Unused import 'dataclasses.dataclass'
- Line 5: Unused import 'pathlib.Path'
- Line 6: Unused import 'types.ModuleType'
- Line 8: Unused import 'fastapi.testclient.TestClient'

### tests/test_battery_widget.py
- Line 2: Unused import 'typing.Any'

### tests/test_parsers.py
- Line 1: Unused import 'piwardrive.sigint_suite.cellular.parsers.parse_band_output'
- Line 1: Unused import 'piwardrive.sigint_suite.cellular.parsers.parse_imsi_output'

### tests/test_migrations_fixed.py
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.AsyncMock'

### tests/test_service_async_endpoints.py
- Line 4: Unused import 'dataclasses.dataclass'
- Line 5: Unused import 'types.ModuleType'
- Line 5: Unused import 'types.SimpleNamespace'
- Line 7: Unused import 'httpx.ASGITransport'
- Line 7: Unused import 'httpx.AsyncClient'

### tests/test_status_service.py
- Line 3: Unused import 'dataclasses.asdict'
- Line 5: Unused import 'httpx.ASGITransport'
- Line 5: Unused import 'httpx.AsyncClient'
- Line 7: Unused import 'piwardrive.persistence.HealthRecord'

### tests/test_persistence.py
- Line 3: Unused import 'pathlib.Path'
- Line 4: Unused import 'typing.Any'
- Line 6: Unused import 'piwardrive.config'
- Line 6: Unused import 'piwardrive.persistence'

### tests/test_core_persistence.py
- Line 6: Unused import 'os'
- Line 10: Unused import 'tempfile'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'unittest.mock.Mock'
- Line 12: Unused import 'unittest.mock.patch'
- Line 12: Unused import 'unittest.mock.AsyncMock'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.Any'

### tests/test_priority_queue.py
- Line 5: Unused import 'piwardrive.task_queue.PriorityTaskQueue'

### tests/test_fastjson.py
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 38: Duplicate import 'piwardrive.fastjson'
- Line 58: Duplicate import 'piwardrive.fastjson'
- Line 66: Duplicate import 'piwardrive.fastjson'
- Line 76: Duplicate import 'piwardrive.fastjson'
- Line 87: Duplicate import 'piwardrive.fastjson'
- Line 107: Duplicate import 'piwardrive.fastjson'
- Line 117: Duplicate import 'piwardrive.fastjson'
- Line 132: Duplicate import 'piwardrive.fastjson'
- Line 155: Duplicate import 'piwardrive.fastjson'
- Line 164: Duplicate import 'piwardrive.fastjson'
- Line 198: Duplicate import 'piwardrive.fastjson'
- Line 217: Duplicate import 'piwardrive.fastjson'
- Line 236: Duplicate import 'piwardrive.fastjson'
- Line 188: Duplicate import 'piwardrive.fastjson'

### tests/test_lora_scanner.py
- Line 4: Unused import 'types.ModuleType'
- Line 8: Unused import 'piwardrive.lora_scanner'

### tests/test_analysis_extra.py
- Line 2: Unused import 'pathlib.Path'
- Line 3: Unused import 'types.ModuleType'

### tests/test_main_application_comprehensive.py
- Line 6: Unused import 'asyncio'
- Line 9: Unused import 'tempfile'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.AsyncMock'
- Line 11: Unused import 'unittest.mock.call'
- Line 12: Unused import 'dataclasses.asdict'

### tests/test_network_fingerprinting_integration.py
- Line 2: Unused import 'types.SimpleNamespace'
- Line 4: Unused import 'piwardrive.services.network_fingerprinting'

### tests/test_core_config_extra.py
- Line 6: Unused import 'piwardrive.core.config'

### tests/test_model_trainer.py
- Line 2: Unused import 'types.SimpleNamespace'

### tests/test_di.py
- Line 2: Unused import 'unittest.mock'
- Line 6: Unused import 'piwardrive.di.Container'

### tests/test_widget_system.py
- Line 6: Unused import 'json'
- Line 7: Unused import 'unittest.mock.Mock'
- Line 7: Unused import 'unittest.mock.patch'
- Line 7: Unused import 'unittest.mock.MagicMock'
- Line 8: Unused import 'pathlib.Path'
- Line 474: Duplicate import 'os'
- Line 501: Duplicate import 'time'

### tests/test_sigint_export_json.py
- Line 3: Unused import 'piwardrive.sigint_suite.exports.export_json'

### tests/test_webui_server.py
- Line 2: Unused import 'types.ModuleType'
- Line 2: Unused import 'types.SimpleNamespace'
- Line 5: Unused import 'fastapi.testclient.TestClient'

### tests/test_export_logs_script.py
- Line 2: Unused import 'types.SimpleNamespace'

### tests/test_main_application_fixed.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.MagicMock'
- Line 8: Unused import 'unittest.mock.AsyncMock'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'tempfile'
- Line 12: Unused import 'shutil'
- Line 37: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 106: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 107: Duplicate import 'piwardrive.config.Config'
- Line 108: Duplicate import 'piwardrive.persistence.AppState'
- Line 162: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 163: Duplicate import 'piwardrive.config.Config'
- Line 164: Duplicate import 'piwardrive.persistence.AppState'
- Line 207: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 271: Duplicate import 'piwardrive.main'
- Line 289: Duplicate import 'piwardrive.config.Config'
- Line 290: Duplicate import 'piwardrive.persistence.AppState'
- Line 340: Duplicate import 'piwardrive.config.Config'
- Line 341: Duplicate import 'piwardrive.persistence.AppState'
- Line 379: Duplicate import 'piwardrive.main'
- Line 406: Duplicate import 'piwardrive.config.Config'
- Line 407: Duplicate import 'piwardrive.persistence.AppState'
- Line 445: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 446: Duplicate import 'piwardrive.config.Config'
- Line 447: Duplicate import 'piwardrive.persistence.AppState'
- Line 253: Duplicate import 'piwardrive.main'
- Line 324: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 370: Duplicate import 'piwardrive.main.PiWardriveApp'
- Line 433: Duplicate import 'piwardrive.main.PiWardriveApp'

### tests/test_aggregation_service.py
- Line 5: Unused import 'fastapi.testclient.TestClient'

### tests/test_web_server_missing.py
- Line 3: Unused import 'types.ModuleType'

### tests/test_compute_health_stats_empty.py
- Line 2: Unused import 'types.ModuleType'
- Line 16: Unused import 'piwardrive.analysis'

### tests/test_service_api.py
- Line 6: Unused import 'json'
- Line 9: Unused import 'unittest.mock.Mock'
- Line 9: Unused import 'unittest.mock.patch'
- Line 9: Unused import 'unittest.mock.MagicMock'
- Line 9: Unused import 'unittest.mock.AsyncMock'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 188: Duplicate import 'fastapi.FastAPI'
- Line 198: Duplicate import 'fastapi.FastAPI'
- Line 198: Duplicate import 'fastapi.HTTPException'
- Line 199: Duplicate import 'fastapi.testclient.TestClient'
- Line 216: Duplicate import 'fastapi.FastAPI'
- Line 217: Duplicate import 'fastapi.testclient.TestClient'
- Line 361: Duplicate import 'piwardrive.api.auth.AUTH_DEP'
- Line 366: Duplicate import 'piwardrive.api.auth.AuthMiddleware'
- Line 371: Duplicate import 'fastapi.FastAPI'
- Line 371: Duplicate import 'fastapi.HTTPException'
- Line 372: Duplicate import 'fastapi.testclient.TestClient'
- Line 420: Duplicate import 'fastapi.FastAPI'
- Line 436: Duplicate import 'fastapi.FastAPI'
- Line 438: Duplicate import 'piwardrive.api.auth.AuthMiddleware'
- Line 439: Duplicate import 'piwardrive.error_middleware.add_error_middleware'
- Line 51: Duplicate import 'fastapi.FastAPI'
- Line 52: Duplicate import 'fastapi.middleware.cors.CORSMiddleware'
- Line 258: Duplicate import 'piwardrive.api.auth.AUTH_DEP'
- Line 259: Duplicate import 'piwardrive.api.common.get_cpu_temp'
- Line 259: Duplicate import 'piwardrive.api.common.get_mem_usage'
- Line 260: Duplicate import 'piwardrive.error_middleware.add_error_middleware'
- Line 39: Duplicate import 'fastapi.FastAPI'
- Line 245: Duplicate import 'fastapi.FastAPI'
- Line 403: Duplicate import 'fastapi.FastAPI'
- Line 408: Duplicate import 'piwardrive.api.auth.AuthMiddleware'
- Line 409: Duplicate import 'piwardrive.error_middleware.add_error_middleware'

### tests/test_unit_enhanced.py
- Line 17: Unused import 'contextlib.contextmanager'
- Line 18: Unused import 'pathlib.Path'
- Line 19: Unused import 'unittest.mock.Mock'
- Line 19: Unused import 'unittest.mock.patch'

### tests/test_analysis.py
- Line 2: Unused import 'pathlib.Path'
- Line 3: Unused import 'types.ModuleType'

### tests/test_sync_receiver.py
- Line 3: Unused import 'pathlib.Path'
- Line 5: Unused import 'fastapi.testclient.TestClient'

### tests/test_imports_src.py
- Line 3: Unused import 'pathlib.Path'
- Line 6: Unused import 'test_imports._setup_dummy_modules'

### tests/test_sigint_paths.py
- Line 6: Unused import 'piwardrive.sigint_suite.paths'

### tests/test_vector_tile_customizer.py
- Line 2: Unused import 'pathlib.Path'
- Line 4: Unused import 'piwardrive.vector_tile_customizer'

### tests/test_exceptions_comprehensive.py
- Line 10: Unused import 'http.HTTPStatus'
- Line 11: Unused import 'pathlib.Path'

### tests/test_plugins.py
- Line 2: Unused import 'pathlib.Path'
- Line 24: Duplicate import 'sys'

### tests/test_exception_handler.py
- Line 5: Unused import 'types.ModuleType'
- Line 6: Unused import 'typing.Any'
- Line 7: Unused import 'unittest.mock'

### tests/test_performance_comprehensive.py
- Line 18: Unused import 'contextlib.contextmanager'
- Line 19: Unused import 'dataclasses.dataclass'
- Line 20: Unused import 'pathlib.Path'
- Line 21: Unused import 'typing.Any'
- Line 21: Unused import 'typing.Dict'
- Line 21: Unused import 'typing.List'
- Line 21: Unused import 'typing.Optional'
- Line 22: Unused import 'unittest.mock.Mock'
- Line 22: Unused import 'unittest.mock.patch'

### tests/test_cache.py
- Line 10: Unused import 'pathlib.Path'

### tests/test_resource_manager.py
- Line 2: Unused import 'pathlib.Path'
- Line 4: Unused import 'piwardrive.resource_manager.ResourceManager'

### tests/test_cache_security_fixed.py
- Line 8: Unused import 'pytest'
- Line 9: Unused import 'cryptography.fernet.Fernet'
- Line 62: Duplicate import 'asyncio'
- Line 75: Duplicate import 'asyncio'
- Line 89: Duplicate import 'asyncio'

### tests/test_widget_system_comprehensive.py
- Line 8: Unused import 'tempfile'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.AsyncMock'

### tests/test_config.py
- Line 6: Unused import 'dataclasses.asdict'
- Line 7: Unused import 'pathlib.Path'
- Line 8: Unused import 'typing.Any'
- Line 11: Unused import 'pydantic.ValidationError'
- Line 108: Duplicate import 'piwardrive.core.config'
- Line 237: Duplicate import 'piwardrive.core.config'
- Line 256: Duplicate import 'piwardrive.core.config'

### tests/test_route_prefetch.py
- Line 2: Unused import 'types.SimpleNamespace'
- Line 84: Duplicate import 'importlib'
- Line 107: Duplicate import 'importlib'
- Line 132: Duplicate import 'importlib'

### tests/test_service_comprehensive.py
- Line 9: Unused import 'asyncio'
- Line 13: Unused import 'pathlib.Path'
- Line 14: Unused import 'tempfile'
- Line 226: Duplicate import 'src.piwardrive.service'

### tests/test_web_server.py
- Line 3: Unused import 'types.ModuleType'
- Line 5: Unused import 'fastapi.testclient.TestClient'

### tests/test_jwt_utils_comprehensive.py
- Line 14: Unused import 'pathlib.Path'
- Line 22: Unused import 'piwardrive.jwt_utils'
- Line 40: Duplicate import 'importlib'
- Line 47: Duplicate import 'importlib'
- Line 55: Duplicate import 'importlib'
- Line 62: Duplicate import 'importlib'
- Line 70: Duplicate import 'importlib'
- Line 77: Duplicate import 'importlib'
- Line 85: Duplicate import 'importlib'
- Line 401: Duplicate import 'importlib'

### tests/test_imports.py
- Line 3: Unused import 'pathlib.Path'
- Line 4: Unused import 'types.ModuleType'

### tests/test_gpsd_client.py
- Line 5: Unused import 'piwardrive.gpsd_client'

### tests/test_ckml.py
- Line 1: Unused import 'piwardrive.ckml'

### tests/test_service_direct.py
- Line 5: Unused import 'unittest.mock.patch'
- Line 5: Unused import 'unittest.mock.MagicMock'
- Line 22: Unused import 'fastapi.FastAPI'
- Line 19: Duplicate import 'piwardrive.service'
- Line 37: Duplicate import 'piwardrive.service'
- Line 54: Duplicate import 'importlib'
- Line 55: Duplicate import 'piwardrive.service'
- Line 64: Duplicate import 'piwardrive.service'
- Line 91: Duplicate import 'piwardrive.service'
- Line 106: Duplicate import 'piwardrive.service'
- Line 143: Duplicate import 'importlib'
- Line 144: Duplicate import 'piwardrive.service'
- Line 153: Duplicate import 'piwardrive.service'
- Line 126: Duplicate import 'piwardrive.service'

### tests/test_clustering.py
- Line 1: Unused import 'piwardrive.analytics.clustering.cluster_positions'

### tests/test_extra_widgets.py
- Line 2: Unused import 'typing.Any'

### tests/test_gpsd_client_async_more.py
- Line 3: Unused import 'piwardrive.gpsd_client_async.AsyncGPSDClient'

### tests/test_sync.py
- Line 3: Unused import 'types.ModuleType'
- Line 3: Unused import 'types.SimpleNamespace'
- Line 11: Unused import 'piwardrive.sync'

### tests/test_r_integration.py
- Line 3: Unused import 'pathlib.Path'
- Line 4: Unused import 'types.SimpleNamespace'
- Line 5: Unused import 'unittest.mock'
- Line 9: Unused import 'piwardrive.r_integration'

### tests/test_bt_scanner.py
- Line 2: Unused import 'types.SimpleNamespace'

### tests/test_migrations_comprehensive.py
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.AsyncMock'
- Line 14: Unused import 'importlib'

### tests/test_remote_sync_pkg.py
- Line 5: Unused import 'types.ModuleType'
- Line 19: Unused import 'piwardrive.remote_sync'
- Line 144: Duplicate import 'sqlite3'

### tests/test_scheduler_tasks.py
- Line 6: Unused import 'os'
- Line 9: Unused import 'threading'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.AsyncMock'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 11: Unused import 'unittest.mock.call'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Callable'

### tests/test_async_scheduler.py
- Line 4: Unused import 'types.ModuleType'
- Line 4: Unused import 'types.SimpleNamespace'
- Line 5: Unused import 'typing.Any'

### tests/test_analysis_hooks.py
- Line 2: Unused import 'types.ModuleType'

### tests/test_orientation_sensors.py
- Line 3: Unused import '__future__.annotations'

### tests/test_service_api_fixed_v2.py
- Line 9: Unused import 'unittest.mock.Mock'
- Line 9: Unused import 'unittest.mock.patch'
- Line 9: Unused import 'unittest.mock.MagicMock'
- Line 9: Unused import 'unittest.mock.AsyncMock'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 508: Unused import 'pydantic.BaseModel'
- Line 120: Duplicate import 'psutil'
- Line 133: Duplicate import 'psutil'

### tests/test_performance.py
- Line 1: Unused import 'piwardrive.performance'

### tests/test_service_layer.py
- Line 8: Unused import 'unittest.mock.Mock'
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.AsyncMock'
- Line 9: Unused import 'fastapi.testclient.TestClient'

### tests/test_error_reporting.py
- Line 5: Unused import 'types.SimpleNamespace'
- Line 6: Unused import 'typing.Any'

### tests/test_config_validation.py
- Line 1: Unused import 'pathlib.Path'
- Line 4: Unused import 'pydantic.ValidationError'
- Line 6: Unused import 'piwardrive.config'

### tests/test_scan_report.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Any'
- Line 7: Unused import 'piwardrive.scan_report'

### tests/test_service.py
- Line 6: Unused import 'dataclasses.asdict'
- Line 6: Unused import 'dataclasses.dataclass'
- Line 7: Unused import 'types.ModuleType'
- Line 7: Unused import 'types.SimpleNamespace'
- Line 8: Unused import 'typing.Any'
- Line 9: Unused import 'unittest.mock'

### tests/test_service_api_fixed.py
- Line 9: Unused import 'unittest.mock.Mock'
- Line 9: Unused import 'unittest.mock.patch'
- Line 9: Unused import 'unittest.mock.MagicMock'
- Line 9: Unused import 'unittest.mock.AsyncMock'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 529: Unused import 'pydantic.BaseModel'
- Line 124: Duplicate import 'psutil'
- Line 138: Duplicate import 'psutil'

### tests/test_heatmap.py
- Line 3: Unused import 'piwardrive.heatmap'

### tests/test_circuit_breaker.py
- Line 5: Unused import 'piwardrive.circuit_breaker.CircuitBreaker'

### tests/test_memory_monitor.py
- Line 3: Unused import 'piwardrive.memory_monitor.MemoryMonitor'

### tests/test_localization.py
- Line 11: Unused import 'tempfile'
- Line 12: Unused import 'pathlib.Path'
- Line 13: Unused import 'unittest.mock'
- Line 39: Duplicate import 'importlib'

### tests/test_calibrate_orientation.py
- Line 2: Unused import 'logging'
- Line 4: Unused import 'types.SimpleNamespace'
- Line 16: Unused import 'piwardrive.scripts.calibrate_orientation'

### tests/test_integration_core.py
- Line 4: Unused import 'aiohttp.web'
- Line 6: Unused import 'remote_sync'

### tests/test_tile_maintenance.py
- Line 4: Unused import 'pathlib.Path'
- Line 5: Unused import 'types.SimpleNamespace'
- Line 40: Unused import 'typing.Any'

### tests/test_start_kiosk_script.py
- Line 3: Unused import 'pathlib.Path'

### tests/test_logging_filters.py
- Line 4: Unused import 'piwardrive.logging.filters.ContentFilter'
- Line 4: Unused import 'piwardrive.logging.filters.RateLimiter'
- Line 4: Unused import 'piwardrive.logging.filters.SensitiveDataFilter'

### tests/test_health_monitor.py
- Line 5: Unused import 'pathlib.Path'
- Line 6: Unused import 'types.ModuleType'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.cast'
- Line 8: Unused import 'unittest.mock'

### tests/test_api_service.py
- Line 6: Unused import 'os'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'unittest.mock.Mock'
- Line 11: Unused import 'unittest.mock.patch'
- Line 11: Unused import 'unittest.mock.AsyncMock'
- Line 11: Unused import 'unittest.mock.MagicMock'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.List'

### tests/test_security_analyzer_integration.py
- Line 1: Unused import 'piwardrive.services.security_analyzer'

### tests/test_data_sink.py
- Line 3: Unused import 'types.ModuleType'
- Line 5: Unused import 'piwardrive.data_sink'

### tests/conftest.py
- Line 5: Unused import 'types.ModuleType'

### tests/test_aggregation_service_main.py
- Line 3: Unused import 'unittest.mock.AsyncMock'

### tests/test_performance_dashboard_integration.py
- Line 5: Unused import 'unittest.mock.MagicMock'
- Line 5: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'fastapi.testclient.TestClient'

### tests/test_service_plugins.py
- Line 3: Unused import 'fastapi.testclient.TestClient'

### tests/test_gpsd_client_async.py
- Line 3: Unused import 'piwardrive.gpsd_client_async'

### tests/test_forecasting.py
- Line 1: Unused import 'numpy'

### tests/test_vector_tile_customizer_cli.py
- Line 22: Duplicate import 'piwardrive.scripts.vector_tile_customizer_cli'

### tests/test_sigint_integration.py
- Line 4: Unused import 'piwardrive.sigint_integration.load_sigint_data'

### tests/test_service_status_script.py
- Line 3: Unused import 'piwardrive.scripts.service_status'

### tests/test_robust_request.py
- Line 1: Unused import 'typing.Any'

### tests/test_export_log_bundle_script.py
- Line 2: Unused import 'types.SimpleNamespace'

### tests/test_log_viewer.py
- Line 1: Unused import 'types.SimpleNamespace'
- Line 2: Unused import 'typing.Any'

### benchmarks/status_benchmark.py
- Line 7: Unused import 'httpx.ASGITransport'
- Line 7: Unused import 'httpx.AsyncClient'
- Line 9: Unused import 'service.app'

### benchmarks/packet_parse_benchmark.py
- Line 7: Unused import 'piwardrive.lora_scanner'

### benchmarks/plot_benchmark.py
- Line 4: Unused import 'pathlib.Path'
- Line 6: Unused import 'pandas'

### benchmarks/analysis_queries_benchmark.py
- Line 6: Unused import 'piwardrive.services.analysis_queries'

### benchmarks/scheduler_benchmark.py
- Line 7: Unused import 'httpx.ASGITransport'
- Line 7: Unused import 'httpx.AsyncClient'
- Line 9: Unused import 'piwardrive.scheduler.PollScheduler'

### examples/direction_finding_example.py
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Dict'
- Line 12: Unused import 'numpy'
- Line 19: Unused import 'piwardrive.direction_finding.DFAlgorithm'
- Line 19: Unused import 'piwardrive.direction_finding.PathLossModel'
- Line 19: Unused import 'piwardrive.direction_finding.add_df_measurement'
- Line 19: Unused import 'piwardrive.direction_finding.configure_df'
- Line 19: Unused import 'piwardrive.direction_finding.get_df_hardware_capabilities'
- Line 19: Unused import 'piwardrive.direction_finding.get_df_status'
- Line 19: Unused import 'piwardrive.direction_finding.initialize_df_integration'
- Line 19: Unused import 'piwardrive.direction_finding.start_df_integration'
- Line 19: Unused import 'piwardrive.direction_finding.stop_df_integration'

### examples/security_analysis_example.py
- Line 5: Unused import 'piwardrive.services.network_fingerprinting'
- Line 5: Unused import 'piwardrive.services.security_analyzer'

### scripts/watch_service.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'typing.Iterable'
- Line 11: Unused import 'watchgod.awatch'

### scripts/df_integration_demo.py
- Line 10: Unused import 'pathlib.Path'

### scripts/validate_migration.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'

### scripts/monitoring_service.py
- Line 12: Unused import 'pathlib.Path'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Optional'

### scripts/generate_config_schema.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'pathlib.Path'

### scripts/test_db_improvements.py
- Line 9: Unused import 'pathlib.Path'

### scripts/dependency_audit.py
- Line 23: Unused import 'pathlib.Path'
- Line 24: Unused import 'typing.Any'
- Line 24: Unused import 'typing.Dict'
- Line 24: Unused import 'typing.List'

### scripts/health_export.py
- Line 7: Unused import 'dataclasses.asdict'
- Line 8: Unused import 'typing.Iterable'
- Line 13: Unused import 'piwardrive.persistence.HealthRecord'
- Line 13: Unused import 'piwardrive.persistence.load_recent_health'

### scripts/migrate_db.py
- Line 5: Unused import 'piwardrive.persistence'

### scripts/export_db.py
- Line 7: Unused import 'piwardrive.logconfig.setup_logging'
- Line 8: Unused import 'pwutils.database'

### scripts/prefetch_batch.py
- Line 6: Unused import 'screens.map_utils.tile_cache'
- Line 8: Unused import 'piwardrive.logconfig.setup_logging'

### scripts/simple_db_check.py
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.List'

### scripts/export_orientation_map.py
- Line 4: Unused import 'pathlib.Path'

### scripts/vacuum_db.py
- Line 8: Unused import 'piwardrive.persistence'

### scripts/kiosk.py
- Line 3: Unused import '__future__.annotations'
- Line 13: Unused import 'piwardrive.cli.kiosk.main'

### scripts/test_database_functions.py
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 18: Unused import 'piwardrive.core.persistence.analyze_network_behavior'
- Line 18: Unused import 'piwardrive.core.persistence.compute_network_analytics'
- Line 18: Unused import 'piwardrive.core.persistence.count_suspicious_activities'
- Line 18: Unused import 'piwardrive.core.persistence.get_table_counts'
- Line 18: Unused import 'piwardrive.core.persistence.load_recent_suspicious'
- Line 18: Unused import 'piwardrive.core.persistence.refresh_daily_detection_stats'
- Line 18: Unused import 'piwardrive.core.persistence.refresh_network_coverage_grid'
- Line 18: Unused import 'piwardrive.core.persistence.run_suspicious_activity_detection'
- Line 18: Unused import 'piwardrive.core.persistence.save_bluetooth_detections'
- Line 18: Unused import 'piwardrive.core.persistence.save_cellular_detections'
- Line 18: Unused import 'piwardrive.core.persistence.save_gps_tracks'
- Line 18: Unused import 'piwardrive.core.persistence.save_network_fingerprints'
- Line 18: Unused import 'piwardrive.core.persistence.save_scan_session'
- Line 18: Unused import 'piwardrive.core.persistence.save_suspicious_activities'
- Line 18: Unused import 'piwardrive.core.persistence.save_wifi_detections'

### scripts/localize_aps.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'pathlib.Path'

### scripts/service_status.py
- Line 6: Unused import 'types.SimpleNamespace'

### scripts/vector_tile_customizer_cli.py
- Line 3: Unused import 'piwardrive.vector_tile_customizer'

### scripts/prune_db.py
- Line 9: Unused import 'piwardrive.persistence'

### scripts/export_grafana.py
- Line 4: Unused import 'typing.Any'
- Line 53: Unused import 'piwardrive.persistence.load_ap_cache'
- Line 53: Unused import 'piwardrive.persistence.load_recent_health'

### scripts/check_orientation_sensors.py
- Line 3: Unused import '__future__.annotations'

### scripts/migrate_sqlite_to_postgres.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'

### scripts/performance_cli.py
- Line 14: Unused import 'pathlib.Path'
- Line 15: Unused import 'typing.Any'
- Line 15: Unused import 'typing.Dict'

### scripts/bench_geom.py
- Line 6: Unused import 'piwardrive.utils'

### scripts/calibrate_orientation.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'pathlib.Path'
- Line 9: Unused import 'typing.Dict'

### scripts/mobile_diagnostics.py
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Optional'
- Line 47: Duplicate import 'socket'

### scripts/export_mysql.py
- Line 6: Unused import 'typing.Any'

### scripts/uav_track_playback.py
- Line 3: Unused import '__future__.annotations'

### scripts/compare_performance.py
- Line 13: Unused import 'pathlib.Path'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Tuple'

### scripts/rotate_logs.py
- Line 3: Unused import '__future__.annotations'

### scripts/validate_config.py
- Line 4: Unused import '__future__.annotations'
- Line 9: Unused import 'pathlib.Path'
- Line 11: Unused import 'piwardrive.config'

### scripts/cleanup_cache.py
- Line 5: Unused import 'piwardrive.map.tile_maintenance'

### scripts/generate_openapi.py
- Line 4: Unused import '__future__.annotations'
- Line 15: Unused import 'piwardrive.service'

### scripts/performance_monitor.py
- Line 15: Unused import 'dataclasses.asdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 19: Unused import 'pathlib.Path'
- Line 20: Unused import 'typing.Any'
- Line 20: Unused import 'typing.Dict'
- Line 20: Unused import 'typing.List'
- Line 20: Unused import 'typing.Optional'
- Line 20: Unused import 'typing.Tuple'

### scripts/tile_maintenance_cli.py
- Line 4: Unused import 'types.SimpleNamespace'
- Line 16: Duplicate import 'piwardrive.map.tile_maintenance'
- Line 23: Duplicate import 'piwardrive.map.tile_maintenance'

### scripts/uav_record.py
- Line 3: Unused import '__future__.annotations'
- Line 14: Unused import 'piwardrive.logconfig.setup_logging'

### scripts/log_follow.py
- Line 9: Unused import 'utils.tail_file'
- Line 11: Unused import 'piwardrive.logconfig.setup_logging'

### scripts/health_import.py
- Line 7: Unused import 'typing.Iterable'
- Line 7: Unused import 'typing.cast'
- Line 12: Unused import 'piwardrive.persistence.HealthRecord'
- Line 12: Unused import 'piwardrive.persistence.flush_health_records'
- Line 12: Unused import 'piwardrive.persistence.save_health_record'

### scripts/db_summary.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'typing.Dict'

### scripts/check_locales_sync.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'pathlib.Path'

### scripts/export_gpx.py
- Line 4: Unused import 'pathlib.Path'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.Mapping'
- Line 7: Unused import 'piwardrive.export'

### widgets/__init__.py
- Line 1: Unused import 'importlib.import_module'
- Line 1: Unused import 'importlib.sys'

### src/gps_handler.py
- Line 11: Unused import '__future__.annotations'
- Line 15: Unused import 'typing.Any'

### src/sync.py
- Line 3: Unused import 'piwardrive.sync.*'

### src/service.py
- Line 10: Unused import '__future__.annotations'
- Line 15: Unused import 'types.ModuleType'
- Line 16: Unused import 'typing.Any'
- Line 16: Unused import 'typing.Callable'

### tests/models/test_api_models.py
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 15: Unused import 'pydantic.ValidationError'
- Line 20: Unused import 'piwardrive.models.api_models.WiFiScanRequest'
- Line 20: Unused import 'piwardrive.models.api_models.AccessPoint'
- Line 20: Unused import 'piwardrive.models.api_models.WiFiScanResponse'
- Line 20: Unused import 'piwardrive.models.api_models.BluetoothScanRequest'
- Line 20: Unused import 'piwardrive.models.api_models.BluetoothDevice'
- Line 20: Unused import 'piwardrive.models.api_models.BluetoothScanResponse'
- Line 20: Unused import 'piwardrive.models.api_models.SystemStats'
- Line 20: Unused import 'piwardrive.models.api_models.ErrorResponse'
- Line 20: Unused import 'piwardrive.models.api_models.CellularScanRequest'
- Line 20: Unused import 'piwardrive.models.api_models.CellTower'
- Line 20: Unused import 'piwardrive.models.api_models.CellularScanResponse'
- Line 20: Unused import 'piwardrive.models.api_models.BluetoothDetection'
- Line 20: Unused import 'piwardrive.models.api_models.CellularDetection'
- Line 20: Unused import 'piwardrive.models.api_models.NetworkFingerprint'
- Line 20: Unused import 'piwardrive.models.api_models.SuspiciousActivity'
- Line 20: Unused import 'piwardrive.models.api_models.NetworkAnalyticsRecord'

### tests/performance/test_performance_infrastructure.py
- Line 15: Unused import 'dataclasses.asdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 16: Unused import 'pathlib.Path'
- Line 17: Unused import 'typing.Any'
- Line 17: Unused import 'typing.Dict'
- Line 17: Unused import 'typing.List'
- Line 17: Unused import 'typing.Optional'
- Line 17: Unused import 'typing.Tuple'

### tests/staging/test_staging_environment.py
- Line 13: Unused import 'dataclasses.dataclass'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Optional'

### tests/logging/test_structured_logger.py
- Line 8: Unused import 'unittest.mock.patch'
- Line 8: Unused import 'unittest.mock.MagicMock'
- Line 8: Unused import 'unittest.mock.mock_open'
- Line 9: Unused import 'io.StringIO'
- Line 27: Unused import 'importlib.metadata.PackageNotFoundError'
- Line 580: Duplicate import 'tempfile'
- Line 581: Duplicate import 'os'
- Line 689: Duplicate import 'tempfile'
- Line 690: Duplicate import 'os'
- Line 756: Duplicate import 'tempfile'

### webui/tests/run_agg_server.py
- Line 9: Unused import 'dataclasses.dataclass'

### webui/tests/run_tile_maintenance_cli.py
- Line 9: Unused import 'piwardrive.scripts.tile_maintenance_cli'

### docs/examples/python_examples.py
- Line 3: Unused import '__future__.annotations'

### examples/plugins/weather_widget.py
- Line 3: Unused import '__future__.annotations'
- Line 10: Unused import 'widgets.base.DashboardWidget'

### examples/localization_improvement/main_localization.py
- Line 8: Unused import 'numpy'
- Line 9: Unused import 'pandas'
- Line 10: Unused import 'folium.Map'
- Line 10: Unused import 'folium.Marker'
- Line 12: Unused import 'sklearn.cluster.DBSCAN'

### src/pwutils/database.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Sequence'
- Line 7: Unused import 'piwardrive.export'
- Line 7: Unused import 'piwardrive.persistence'

### src/remote_sync/__init__.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/mysql_export.py
- Line 6: Unused import '__future__.annotations'
- Line 8: Unused import 'dataclasses.dataclass'
- Line 9: Unused import 'typing.Any'
- Line 9: Unused import 'typing.Iterable'
- Line 9: Unused import 'typing.List'
- Line 9: Unused import 'typing.Sequence'
- Line 13: Unused import 'persistence.HealthRecord'

### src/piwardrive/diagnostics.py
- Line 7: Unused import '__future__.annotations'
- Line 20: Unused import 'typing.Any'
- Line 20: Unused import 'typing.Dict'
- Line 21: Unused import 'uuid.uuid4'
- Line 359: Unused import 'dataclasses.asdict'

### src/piwardrive/cache.py
- Line 7: Unused import '__future__.annotations'
- Line 10: Unused import 'typing.Any'
- Line 12: Unused import 'core.utils._get_redis_client'

### src/piwardrive/db_browser.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'pathlib.Path'

### src/piwardrive/analysis.py
- Line 6: Unused import 'dataclasses.asdict'
- Line 8: Unused import 'typing.Callable'
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.List'
- Line 99: Unused import 'analytics.anomaly.HealthAnomalyDetector'

### src/piwardrive/remote_sync.py
- Line 6: Unused import '__future__.annotations'
- Line 10: Unused import 'typing.Tuple'

### src/piwardrive/circuit_breaker.py
- Line 7: Unused import '__future__.annotations'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Awaitable'
- Line 10: Unused import 'typing.Callable'

### src/piwardrive/heatmap.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Sequence'
- Line 5: Unused import 'typing.Tuple'
- Line 7: Unused import 'numpy'
- Line 8: Unused import 'scipy.ndimage.convolve'

### src/piwardrive/lora_scanner.py
- Line 18: Unused import '__future__.annotations'
- Line 26: Unused import 'dataclasses.dataclass'
- Line 27: Unused import 'typing.Callable'
- Line 27: Unused import 'typing.List'
- Line 27: Unused import 'typing.ParamSpec'
- Line 27: Unused import 'typing.Sequence'
- Line 27: Unused import 'typing.TypeVar'
- Line 29: Unused import 'core.config'

### src/piwardrive/route_prefetch.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'

### src/piwardrive/gpsd_client.py
- Line 17: Unused import 'typing.Any'
- Line 17: Unused import 'typing.cast'

### src/piwardrive/aggregation_service.py
- Line 7: Unused import '__future__.annotations'
- Line 14: Unused import 'contextlib.asynccontextmanager'
- Line 15: Unused import 'typing.AsyncIterator'
- Line 15: Unused import 'typing.Dict'
- Line 15: Unused import 'typing.Iterable'
- Line 15: Unused import 'typing.List'
- Line 15: Unused import 'typing.Tuple'
- Line 18: Unused import 'fastapi.FastAPI'
- Line 18: Unused import 'fastapi.HTTPException'
- Line 18: Unused import 'fastapi.UploadFile'
- Line 21: Unused import 'persistence.HealthRecord'
- Line 22: Unused import 'security.validate_filename'

### src/piwardrive/route_optimizer.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.List'
- Line 6: Unused import 'typing.Tuple'

### src/piwardrive/kiosk.py
- Line 3: Unused import 'cli.kiosk.*'

### src/piwardrive/memory_monitor.py
- Line 9: Unused import 'collections.deque'
- Line 11: Unused import 'typing.Deque'
- Line 11: Unused import 'typing.Tuple'

### src/piwardrive/cpu_pool.py
- Line 7: Unused import '__future__.annotations'
- Line 11: Unused import 'concurrent.futures.ProcessPoolExecutor'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Callable'

### src/piwardrive/di.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'threading.Lock'
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Callable'
- Line 6: Unused import 'typing.Dict'

### src/piwardrive/localization.py
- Line 5: Unused import 'functools.lru_cache'

### src/piwardrive/scan_report.py
- Line 9: Unused import 'collections.Counter'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.Iterable'
- Line 14: Unused import 'persistence.load_ap_cache'

### src/piwardrive/gps_track_playback.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Awaitable'
- Line 6: Unused import 'typing.Callable'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.Tuple'

### src/piwardrive/widget_manager.py
- Line 11: Unused import '__future__.annotations'
- Line 14: Unused import 'importlib.util'
- Line 18: Unused import 'pathlib.Path'
- Line 19: Unused import 'typing.Dict'
- Line 19: Unused import 'typing.Optional'

### src/piwardrive/database_service.py
- Line 7: Unused import '__future__.annotations'
- Line 9: Unused import 'typing.Any'
- Line 9: Unused import 'typing.List'
- Line 12: Unused import 'db.DatabaseAdapter'
- Line 12: Unused import 'db.DatabaseManager'
- Line 12: Unused import 'db.MySQLAdapter'
- Line 12: Unused import 'db.PostgresAdapter'
- Line 12: Unused import 'db.SQLiteAdapter'

### src/piwardrive/gpsd_client_async.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'types.TracebackType'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Type'

### src/piwardrive/network_analytics.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'collections.defaultdict'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Dict'
- Line 7: Unused import 'typing.Iterable'
- Line 7: Unused import 'typing.List'
- Line 7: Unused import 'typing.Mapping'
- Line 7: Unused import 'typing.Tuple'
- Line 9: Unused import 'numpy'
- Line 10: Unused import 'sklearn.cluster.DBSCAN'
- Line 12: Unused import 'piwardrive.sigint_suite.enrichment.cached_lookup_vendor'

### src/piwardrive/export.py
- Line 8: Unused import 'xml.etree.ElementTree'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Callable'
- Line 10: Unused import 'typing.Iterable'
- Line 10: Unused import 'typing.Mapping'
- Line 10: Unused import 'typing.Sequence'

### src/piwardrive/main.py
- Line 3: Unused import '__future__.annotations'
- Line 10: Unused import 'dataclasses.asdict'
- Line 10: Unused import 'dataclasses.fields'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Callable'
- Line 14: Unused import 'watchdog.observers.Observer'
- Line 194: Duplicate import 'logconfig.DEFAULT_LOG_PATH'

### src/piwardrive/web_server.py
- Line 8: Unused import '__future__.annotations'
- Line 16: Unused import 'piwardrive.service.app'

### src/piwardrive/config_watcher.py
- Line 8: Unused import '__future__.annotations'
- Line 11: Unused import 'typing.Callable'

### src/piwardrive/graphql_api.py
- Line 8: Unused import '__future__.annotations'
- Line 11: Unused import 'dataclasses.asdict'
- Line 19: Unused import 'core.config'
- Line 19: Unused import 'core.persistence'

### src/piwardrive/sync.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.Sequence'
- Line 12: Unused import 'piwardrive.config'

### src/piwardrive/utils.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'dataclasses.dataclass'
- Line 8: Unused import 'typing.TYPE_CHECKING'
- Line 12: Unused import 'error_reporting.format_error'
- Line 12: Unused import 'error_reporting.report_error'

### src/piwardrive/advanced_localization.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'dataclasses.dataclass'
- Line 7: Unused import 'pathlib.Path'
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.Iterable'
- Line 8: Unused import 'typing.Tuple'
- Line 11: Unused import 'numpy'
- Line 12: Unused import 'pandas'
- Line 13: Unused import 'scipy.signal'
- Line 14: Unused import 'sklearn.cluster.DBSCAN'

### src/piwardrive/vehicle_sensors.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Optional'

### src/piwardrive/__init__.py
- Line 3: Unused import 'logging'
- Line 5: Unused import 'importlib.import_module'
- Line 6: Unused import 'types.ModuleType'
- Line 8: Unused import 'widget_manager.LazyWidgetManager'

### src/piwardrive/exceptions.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'http.HTTPStatus'

### src/piwardrive/task_queue.py
- Line 7: Unused import '__future__.annotations'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Awaitable'
- Line 11: Unused import 'typing.Callable'

### src/piwardrive/fastjson.py
- Line 11: Unused import '__future__.annotations'
- Line 14: Unused import 'typing.Any'

### src/piwardrive/r_integration.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'pathlib.Path'
- Line 6: Unused import 'typing.Dict'
- Line 6: Unused import 'typing.Optional'
- Line 8: Unused import 'errors.PiWardriveError'

### src/piwardrive/logconfig.py
- Line 8: Unused import 'typing.Iterable'
- Line 8: Unused import 'typing.Optional'
- Line 10: Unused import 'piwardrive.config.CONFIG_DIR'

### src/piwardrive/service.py
- Line 9: Unused import '__future__.annotations'

### src/piwardrive/resource_manager.py
- Line 12: Unused import 'contextlib.contextmanager'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Callable'
- Line 13: Unused import 'typing.Iterable'

### src/piwardrive/orientation_sensors.py
- Line 15: Unused import 'typing.Any'
- Line 15: Unused import 'typing.Dict'
- Line 15: Unused import 'typing.Optional'
- Line 17: Unused import 'piwardrive.security.sanitize_path'

### src/piwardrive/persistence.py
- Line 10: Unused import 'dataclasses.asdict'
- Line 10: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'pathlib.Path'

### src/piwardrive/jwt_utils.py
- Line 10: Unused import 'typing.Optional'

### src/piwardrive/error_middleware.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Awaitable'
- Line 8: Unused import 'typing.Callable'
- Line 15: Unused import 'exceptions.PiWardriveError'

### src/piwardrive/cloud_export.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Optional'

### src/piwardrive/performance.py
- Line 9: Unused import '__future__.annotations'
- Line 12: Unused import 'collections.defaultdict'
- Line 13: Unused import 'contextlib.contextmanager'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'

### src/piwardrive/errors.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'exceptions.ConfigurationError'
- Line 5: Unused import 'exceptions.DatabaseError'
- Line 5: Unused import 'exceptions.PiWardriveError'
- Line 5: Unused import 'exceptions.ServiceError'

### src/piwardrive/scheduler.py
- Line 3: Unused import '__future__.annotations'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Awaitable'
- Line 13: Unused import 'typing.Callable'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.Mapping'
- Line 13: Unused import 'typing.Protocol'
- Line 13: Unused import 'typing.Sequence'
- Line 16: Unused import 'core.config'
- Line 17: Unused import 'gpsd_client.client'

### src/piwardrive/setup_wizard.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'pathlib.Path'
- Line 8: Unused import 'typing.Any'

### src/piwardrive/notifications.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.List'
- Line 10: Unused import 'core.config'
- Line 12: Unused import 'utils.get_cpu_temp'
- Line 12: Unused import 'utils.get_disk_usage'
- Line 12: Unused import 'utils.run_async_task'

### src/piwardrive/exception_handler.py
- Line 9: Unused import '__future__.annotations'
- Line 14: Unused import 'typing.Any'

### src/piwardrive/interfaces.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Protocol'

### src/piwardrive/data_sink.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Iterable'
- Line 7: Unused import 'typing.Mapping'

### src/piwardrive/simpleui.py
- Line 8: Unused import '__future__.annotations'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Callable'
- Line 10: Unused import 'typing.Iterable'

### src/piwardrive/security.py
- Line 11: Unused import 'cryptography.fernet.Fernet'

### src/piwardrive/unified_platform.py
- Line 26: Unused import 'collections.defaultdict'
- Line 27: Unused import 'dataclasses.dataclass'
- Line 27: Unused import 'dataclasses.field'
- Line 29: Unused import 'enum.Enum'
- Line 30: Unused import 'pathlib.Path'
- Line 31: Unused import 'typing.Any'
- Line 31: Unused import 'typing.Callable'
- Line 31: Unused import 'typing.Dict'
- Line 31: Unused import 'typing.List'
- Line 31: Unused import 'typing.Optional'
- Line 34: Unused import 'flask.Flask'
- Line 34: Unused import 'flask.jsonify'
- Line 34: Unused import 'flask.render_template_string'
- Line 34: Unused import 'flask.request'
- Line 35: Unused import 'flask_cors.CORS'
- Line 37: Unused import 'analysis.packet_engine.PacketAnalysisEngine'
- Line 42: Unused import 'mining.advanced_data_mining.AdvancedDataMining'
- Line 45: Unused import 'ml.threat_detection.OfflineThreatDetector'
- Line 49: Unused import 'protocols.multi_protocol.MultiProtocolManager'
- Line 51: Unused import 'signal.rf_spectrum.RFSpectrumIntelligence'

### src/piwardrive/services/alerting.py
- Line 7: Unused import '__future__.annotations'
- Line 10: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Iterable'
- Line 11: Unused import 'typing.Mapping'

### src/piwardrive/services/maintenance.py
- Line 7: Unused import '__future__.annotations'
- Line 15: Unused import 'dataclasses.asdict'

### src/piwardrive/services/db_monitor.py
- Line 6: Unused import '__future__.annotations'
- Line 9: Unused import 'collections.defaultdict'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.List'
- Line 12: Unused import 'piwardrive.persistence'

### src/piwardrive/services/report_generator.py
- Line 9: Unused import '__future__.annotations'
- Line 13: Unused import 'importlib.resources'

### src/piwardrive/services/integration_service.py
- Line 8: Unused import '__future__.annotations'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Iterable'
- Line 13: Unused import 'typing.Mapping'
- Line 17: Unused import 'piwardrive.logging.filters.RateLimiter'

### src/piwardrive/services/analysis_queries.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Sequence'
- Line 9: Unused import 'cachetools.TTLCache'

### src/piwardrive/services/view_refresher.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/services/network_analytics.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.List'
- Line 9: Unused import 'numpy'

### src/piwardrive/services/cellular_scanner.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.List'

### src/piwardrive/services/bluetooth_scanner.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.List'

### src/piwardrive/services/export_service.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 9: Unused import 'piwardrive.export'
- Line 9: Unused import 'piwardrive.persistence'

### src/piwardrive/services/security_analyzer.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Iterable'
- Line 7: Unused import 'typing.List'
- Line 7: Unused import 'typing.Mapping'
- Line 9: Unused import 'piwardrive.persistence'

### src/piwardrive/services/demographic_analytics.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'functools.lru_cache'
- Line 7: Unused import 'pathlib.Path'
- Line 9: Unused import 'typing.Any'
- Line 9: Unused import 'typing.Dict'
- Line 9: Unused import 'typing.List'

### src/piwardrive/services/coordinator.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Dict'
- Line 7: Unused import 'typing.Iterable'
- Line 7: Unused import 'typing.List'
- Line 7: Unused import 'typing.Mapping'
- Line 11: Unused import 'piwardrive.core.config'

### src/piwardrive/services/data_export.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'importlib.resources'
- Line 6: Unused import 'typing.Sequence'
- Line 8: Unused import 'piwardrive.export'
- Line 8: Unused import 'piwardrive.persistence'

### src/piwardrive/services/stream_processor.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.Iterable'
- Line 8: Unused import 'typing.Mapping'
- Line 10: Unused import 'piwardrive.services.network_fingerprinting'
- Line 10: Unused import 'piwardrive.services.security_analyzer'

### src/piwardrive/services/analytics_processor.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 9: Unused import 'numpy'

### src/piwardrive/services/cluster_manager.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'dataclasses.dataclass'
- Line 8: Unused import 'dataclasses.field'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.Iterable'
- Line 10: Unused import 'typing.List'
- Line 10: Unused import 'typing.Optional'

### src/piwardrive/services/network_fingerprinting.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Iterable'
- Line 9: Unused import 'piwardrive.persistence'

### src/piwardrive/services/model_trainer.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/services/monitoring.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'collections.defaultdict'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.Iterable'
- Line 8: Unused import 'typing.List'
- Line 8: Unused import 'typing.Mapping'

### src/piwardrive/models/api_models.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'pydantic.BaseModel'
- Line 5: Unused import 'pydantic.ConfigDict'
- Line 5: Unused import 'pydantic.Field'

### src/piwardrive/models/__init__.py
- Line 3: Unused import 'api_models.AccessPoint'
- Line 3: Unused import 'api_models.BluetoothDevice'
- Line 3: Unused import 'api_models.BluetoothDetection'
- Line 3: Unused import 'api_models.BluetoothScanRequest'
- Line 3: Unused import 'api_models.BluetoothScanResponse'
- Line 3: Unused import 'api_models.CellTower'
- Line 3: Unused import 'api_models.CellularDetection'
- Line 3: Unused import 'api_models.CellularScanRequest'
- Line 3: Unused import 'api_models.CellularScanResponse'
- Line 3: Unused import 'api_models.ErrorResponse'
- Line 3: Unused import 'api_models.NetworkAnalyticsRecord'
- Line 3: Unused import 'api_models.NetworkFingerprint'
- Line 3: Unused import 'api_models.SuspiciousActivity'
- Line 3: Unused import 'api_models.SystemStats'
- Line 3: Unused import 'api_models.WiFiScanRequest'
- Line 3: Unused import 'api_models.WiFiScanResponse'

### src/piwardrive/mqtt/__init__.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Any'
- Line 8: Unused import 'paho.mqtt.client'

### src/piwardrive/analysis/packet_engine.py
- Line 12: Unused import 'collections.defaultdict'
- Line 12: Unused import 'collections.deque'
- Line 13: Unused import 'dataclasses.dataclass'
- Line 13: Unused import 'dataclasses.field'
- Line 15: Unused import 'enum.Enum'
- Line 16: Unused import 'typing.Any'
- Line 16: Unused import 'typing.Dict'
- Line 16: Unused import 'typing.List'
- Line 16: Unused import 'typing.Optional'
- Line 16: Unused import 'typing.Set'

### src/piwardrive/performance/realtime_optimizer.py
- Line 13: Unused import 'collections.defaultdict'
- Line 13: Unused import 'collections.deque'
- Line 14: Unused import 'contextlib.asynccontextmanager'
- Line 15: Unused import 'dataclasses.asdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 16: Unused import 'typing.Any'
- Line 16: Unused import 'typing.Callable'
- Line 16: Unused import 'typing.Dict'
- Line 16: Unused import 'typing.List'
- Line 16: Unused import 'typing.Optional'
- Line 16: Unused import 'typing.Set'
- Line 17: Unused import 'weakref.WeakSet'
- Line 21: Unused import 'starlette.websockets.WebSocketDisconnect'

### src/piwardrive/performance/async_optimizer.py
- Line 12: Unused import 'collections.defaultdict'
- Line 12: Unused import 'collections.deque'
- Line 13: Unused import 'contextlib.asynccontextmanager'
- Line 14: Unused import 'dataclasses.dataclass'
- Line 15: Unused import 'typing.Any'
- Line 15: Unused import 'typing.Callable'
- Line 15: Unused import 'typing.Dict'
- Line 15: Unused import 'typing.List'
- Line 15: Unused import 'typing.Optional'
- Line 15: Unused import 'typing.TypeVar'
- Line 15: Unused import 'typing.Union'
- Line 16: Unused import 'weakref.WeakSet'

### src/piwardrive/performance/__init__.py
- Line 3: Unused import 'async_optimizer.AsyncOptimizer'
- Line 4: Unused import 'db_optimizer.DatabaseOptimizer'
- Line 5: Unused import 'realtime_optimizer.RealtimeOptimizer'

### src/piwardrive/performance/db_optimizer.py
- Line 11: Unused import 'contextlib.asynccontextmanager'
- Line 12: Unused import 'dataclasses.dataclass'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Optional'
- Line 13: Unused import 'typing.Tuple'

### src/piwardrive/performance/optimization.py
- Line 30: Unused import 'concurrent.futures.ProcessPoolExecutor'
- Line 30: Unused import 'concurrent.futures.ThreadPoolExecutor'
- Line 31: Unused import 'dataclasses.dataclass'
- Line 31: Unused import 'dataclasses.field'
- Line 33: Unused import 'enum.Enum'
- Line 34: Unused import 'pathlib.Path'
- Line 35: Unused import 'typing.Any'
- Line 35: Unused import 'typing.Callable'
- Line 35: Unused import 'typing.Dict'
- Line 35: Unused import 'typing.List'
- Line 35: Unused import 'typing.Optional'
- Line 35: Unused import 'typing.Set'
- Line 35: Unused import 'typing.Tuple'
- Line 35: Unused import 'typing.Union'
- Line 38: Unused import 'numpy'

### src/piwardrive/ui/user_experience.py
- Line 13: Unused import 'abc.ABC'
- Line 13: Unused import 'abc.abstractmethod'
- Line 14: Unused import 'dataclasses.asdict'
- Line 14: Unused import 'dataclasses.dataclass'
- Line 16: Unused import 'pathlib.Path'
- Line 17: Unused import 'typing.Any'
- Line 17: Unused import 'typing.Callable'
- Line 17: Unused import 'typing.Dict'
- Line 17: Unused import 'typing.List'
- Line 17: Unused import 'typing.Optional'
- Line 17: Unused import 'typing.Tuple'
- Line 21: Unused import 'flask.Flask'
- Line 21: Unused import 'flask.jsonify'
- Line 21: Unused import 'flask.redirect'
- Line 21: Unused import 'flask.render_template'
- Line 21: Unused import 'flask.request'
- Line 21: Unused import 'flask.session'
- Line 21: Unused import 'flask.url_for'
- Line 30: Unused import 'flask_socketio.SocketIO'
- Line 30: Unused import 'flask_socketio.emit'
- Line 30: Unused import 'flask_socketio.join_room'
- Line 30: Unused import 'flask_socketio.leave_room'
- Line 38: Unused import 'tkinter.filedialog'
- Line 38: Unused import 'tkinter.messagebox'
- Line 38: Unused import 'tkinter.ttk'

### src/piwardrive/cli/kiosk.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'typing.Sequence'

### src/piwardrive/cli/config_cli.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'dataclasses.asdict'
- Line 9: Unused import 'typing.Any'

### src/piwardrive/testing/automated_framework.py
- Line 14: Unused import 'collections.defaultdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 15: Unused import 'dataclasses.field'
- Line 17: Unused import 'enum.Enum'
- Line 18: Unused import 'typing.Any'
- Line 18: Unused import 'typing.Callable'
- Line 18: Unused import 'typing.Dict'
- Line 18: Unused import 'typing.List'
- Line 18: Unused import 'typing.Optional'
- Line 18: Unused import 'typing.Tuple'

### src/piwardrive/integrations/sigint.py
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Mapping'
- Line 7: Unused import 'piwardrive.sigint_suite.paths'

### src/piwardrive/integrations/wigle.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'types.SimpleNamespace'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.List'
- Line 10: Unused import 'piwardrive.core.utils.WIGLE_CACHE_SECONDS'
- Line 10: Unused import 'piwardrive.core.utils.async_ttl_cache'

### src/piwardrive/integrations/r_integration.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'pathlib.Path'
- Line 6: Unused import 'typing.Dict'
- Line 6: Unused import 'typing.Optional'
- Line 8: Unused import 'errors.PiWardriveError'

### src/piwardrive/sigint_suite/__init__.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.cast'
- Line 54: Duplicate import 'sys'

### src/piwardrive/migrations/005_create_cellular_detections.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/004_create_gps_tracks.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/006_create_network_fingerprints.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/base.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'abc.ABC'
- Line 5: Unused import 'abc.abstractmethod'

### src/piwardrive/migrations/001_create_scan_sessions.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/009_create_materialized_views.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/003_create_bluetooth_detections.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/010_performance_indexes.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/__init__.py
- Line 3: Unused import 'importlib.import_module'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/008_create_network_analytics.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/runner.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Sequence'
- Line 7: Unused import 'base.BaseMigration'
- Line 71: Duplicate import '.MIGRATIONS'

### src/piwardrive/migrations/007_create_suspicious_activities.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'base.BaseMigration'

### src/piwardrive/migrations/002_enhance_wifi_detections.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'base.BaseMigration'

### src/piwardrive/core/config.py
- Line 8: Unused import 'pathlib.Path'
- Line 9: Unused import 'typing.Any'
- Line 9: Unused import 'typing.Dict'
- Line 9: Unused import 'typing.List'
- Line 9: Unused import 'typing.Optional'
- Line 11: Unused import 'pydantic.BaseModel'
- Line 11: Unused import 'pydantic.Field'
- Line 11: Unused import 'pydantic.ValidationError'
- Line 13: Unused import 'errors.ConfigError'
- Line 449: Duplicate import 'yaml'

### src/piwardrive/core/utils.py
- Line 15: Unused import 'contextlib.asynccontextmanager'
- Line 16: Unused import 'dataclasses.dataclass'
- Line 18: Unused import 'pathlib.Path'
- Line 40: Unused import 'concurrent.futures.Future'
- Line 41: Unused import 'enum.IntEnum'
- Line 1184: Unused import 'ckml.parse_coords'
- Line 1206: Unused import 'defusedxml.ElementTree'
- Line 677: Duplicate import 'piwardrive.security.validate_service_name'
- Line 733: Duplicate import 'piwardrive.security.validate_service_name'
- Line 827: Duplicate import 'piwardrive.security.validate_service_name'
- Line 1129: Duplicate import 'math'
- Line 850: Duplicate import 'dbus'

### src/piwardrive/core/fastjson.py
- Line 6: Unused import 'fastjson.dumps'
- Line 6: Unused import 'fastjson.loads'

### src/piwardrive/core/persistence.py
- Line 3: Unused import '__future__.annotations'
- Line 11: Unused import 'dataclasses.asdict'
- Line 11: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'dataclasses.field'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.AsyncIterator'
- Line 13: Unused import 'typing.Awaitable'
- Line 13: Unused import 'typing.Callable'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Optional'
- Line 13: Unused import 'typing.Sequence'
- Line 33: Unused import 'piwardrive.config'
- Line 1451: Duplicate import 'tempfile'
- Line 1638: Duplicate import 'os'

### src/piwardrive/web/webui_server.py
- Line 1: Unused import '__future__.annotations'

### src/piwardrive/direction_finding/core.py
- Line 9: Unused import 'dataclasses.dataclass'
- Line 9: Unused import 'dataclasses.field'
- Line 10: Unused import 'enum.Enum'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.Optional'
- Line 11: Unused import 'typing.Tuple'
- Line 11: Unused import 'typing.Union'
- Line 13: Unused import 'numpy'

### src/piwardrive/direction_finding/hardware.py
- Line 12: Unused import 'pathlib.Path'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Optional'
- Line 13: Unused import 'typing.Tuple'
- Line 15: Unused import 'numpy'

### src/piwardrive/direction_finding/config.py
- Line 7: Unused import '__future__.annotations'
- Line 11: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'dataclasses.field'
- Line 13: Unused import 'pathlib.Path'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Optional'
- Line 14: Unused import 'typing.Union'

### src/piwardrive/direction_finding/__init__.py
- Line 7: Unused import 'algorithms.BeamformingProcessor'
- Line 7: Unused import 'algorithms.MUSICProcessor'
- Line 7: Unused import 'algorithms.PathLossCalculator'
- Line 7: Unused import 'algorithms.RSSTriangulation'
- Line 7: Unused import 'algorithms.SignalMapper'
- Line 14: Unused import 'config.DFAlgorithm'
- Line 14: Unused import 'config.DFConfigManager'
- Line 14: Unused import 'config.DFConfiguration'
- Line 14: Unused import 'config.PathLossModel'
- Line 14: Unused import 'config.config_manager'
- Line 14: Unused import 'config.get_algorithm_config'
- Line 14: Unused import 'config.get_df_config'
- Line 14: Unused import 'config.set_df_algorithm'
- Line 14: Unused import 'config.update_df_config'
- Line 25: Unused import 'core.AngleEstimate'
- Line 25: Unused import 'core.DFEngine'
- Line 25: Unused import 'core.DFMeasurement'
- Line 25: Unused import 'core.DFQuality'
- Line 25: Unused import 'core.DFResult'
- Line 25: Unused import 'core.PositionEstimate'
- Line 33: Unused import 'hardware.AntennaArrayManager'
- Line 33: Unused import 'hardware.HardwareDetector'
- Line 33: Unused import 'hardware.WiFiAdapterManager'
- Line 34: Unused import 'integration.DFIntegrationManager'
- Line 34: Unused import 'integration.add_df_measurement'
- Line 34: Unused import 'integration.configure_df'
- Line 34: Unused import 'integration.get_df_hardware_capabilities'
- Line 34: Unused import 'integration.get_df_integration_manager'
- Line 34: Unused import 'integration.get_df_status'
- Line 34: Unused import 'integration.initialize_df_integration'
- Line 34: Unused import 'integration.start_df_integration'
- Line 34: Unused import 'integration.stop_df_integration'

### src/piwardrive/direction_finding/algorithms.py
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.Optional'
- Line 11: Unused import 'typing.Tuple'
- Line 27: Unused import 'core.AngleEstimate'
- Line 27: Unused import 'core.DFMeasurement'
- Line 27: Unused import 'core.DFQuality'
- Line 27: Unused import 'core.DFResult'
- Line 27: Unused import 'core.PositionEstimate'

### src/piwardrive/direction_finding/integration.py
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Callable'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.Optional'
- Line 14: Unused import 'core.DFEngine'
- Line 14: Unused import 'core.DFMeasurement'
- Line 14: Unused import 'core.DFResult'

### src/piwardrive/integration/system_orchestration.py
- Line 24: Unused import 'collections.defaultdict'
- Line 24: Unused import 'collections.deque'
- Line 25: Unused import 'dataclasses.dataclass'
- Line 25: Unused import 'dataclasses.field'
- Line 27: Unused import 'enum.Enum'
- Line 28: Unused import 'pathlib.Path'
- Line 29: Unused import 'typing.Any'
- Line 29: Unused import 'typing.AsyncGenerator'
- Line 29: Unused import 'typing.Callable'
- Line 29: Unused import 'typing.Dict'
- Line 29: Unused import 'typing.List'
- Line 29: Unused import 'typing.Optional'
- Line 29: Unused import 'typing.Set'
- Line 29: Unused import 'typing.Tuple'
- Line 29: Unused import 'typing.Union'
- Line 44: Unused import 'celery.Celery'
- Line 45: Unused import 'flask.Flask'
- Line 45: Unused import 'flask.jsonify'
- Line 45: Unused import 'flask.request'
- Line 46: Unused import 'flask_restx.Api'
- Line 46: Unused import 'flask_restx.Resource'
- Line 46: Unused import 'flask_restx.fields'
- Line 328: Duplicate import 'random'

### src/piwardrive/db/mysql.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'contextlib.asynccontextmanager'
- Line 4: Unused import 'typing.Any'
- Line 4: Unused import 'typing.AsyncIterator'
- Line 4: Unused import 'typing.Iterable'
- Line 8: Unused import 'adapter.DatabaseAdapter'

### src/piwardrive/db/__init__.py
- Line 3: Unused import 'adapter.DatabaseAdapter'
- Line 4: Unused import 'manager.DatabaseManager'
- Line 5: Unused import 'mysql.MySQLAdapter'
- Line 6: Unused import 'postgres.PostgresAdapter'
- Line 7: Unused import 'sqlite.SQLiteAdapter'

### src/piwardrive/db/adapter.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Any'
- Line 3: Unused import 'typing.AsyncIterator'
- Line 3: Unused import 'typing.Iterable'

### src/piwardrive/db/manager.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'contextlib.asynccontextmanager'
- Line 6: Unused import 'typing.AsyncIterator'
- Line 6: Unused import 'typing.Callable'
- Line 6: Unused import 'typing.Dict'
- Line 9: Unused import 'services.db_monitor'

### src/piwardrive/db/postgres.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'contextlib.asynccontextmanager'
- Line 4: Unused import 'typing.Any'
- Line 4: Unused import 'typing.AsyncIterator'
- Line 4: Unused import 'typing.Iterable'
- Line 8: Unused import 'adapter.DatabaseAdapter'

### src/piwardrive/db/sqlite.py
- Line 1: Unused import '__future__.annotations'
- Line 4: Unused import 'typing.Any'
- Line 4: Unused import 'typing.AsyncIterator'
- Line 4: Unused import 'typing.Iterable'
- Line 8: Unused import 'adapter.DatabaseAdapter'

### src/piwardrive/reporting/professional.py
- Line 8: Unused import 'dataclasses.asdict'
- Line 8: Unused import 'dataclasses.dataclass'
- Line 10: Unused import 'enum.Enum'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 12: Unused import 'typing.Optional'
- Line 12: Unused import 'typing.Tuple'

### src/piwardrive/map/tile_maintenance.py
- Line 9: Unused import 'concurrent.futures.Future'
- Line 12: Unused import 'piwardrive.scheduler.PollScheduler'
- Line 49: Duplicate import 'typing.Any'
- Line 42: Duplicate import 'watchdog.events.FileSystemEventHandler'
- Line 43: Duplicate import 'watchdog.observers.Observer'
- Line 45: Duplicate import 'typing.Any'

### src/piwardrive/map/vector_tiles.py
- Line 3: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Iterable'
- Line 8: Unused import 'typing.Tuple'

### src/piwardrive/map/vector_tile_customizer.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/ml/threat_detection.py
- Line 14: Unused import 'collections.Counter'
- Line 14: Unused import 'collections.defaultdict'
- Line 15: Unused import 'dataclasses.asdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 17: Unused import 'pathlib.Path'
- Line 18: Unused import 'typing.Any'
- Line 18: Unused import 'typing.Dict'
- Line 18: Unused import 'typing.List'
- Line 18: Unused import 'typing.Optional'
- Line 18: Unused import 'typing.Tuple'
- Line 20: Unused import 'numpy'

### src/piwardrive/hardware/enhanced_hardware.py
- Line 14: Unused import 'abc.ABC'
- Line 14: Unused import 'abc.abstractmethod'
- Line 15: Unused import 'dataclasses.asdict'
- Line 15: Unused import 'dataclasses.dataclass'
- Line 17: Unused import 'pathlib.Path'
- Line 18: Unused import 'typing.Any'
- Line 18: Unused import 'typing.Dict'
- Line 18: Unused import 'typing.List'
- Line 18: Unused import 'typing.Optional'
- Line 18: Unused import 'typing.Tuple'
- Line 18: Unused import 'typing.Union'
- Line 31: Unused import 'usb.core'

### src/piwardrive/analytics/explain.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Iterable'
- Line 7: Unused import 'numpy'
- Line 8: Unused import 'sklearn.inspection.permutation_importance'

### src/piwardrive/analytics/forecasting.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.List'
- Line 7: Unused import 'numpy'
- Line 9: Unused import 'persistence.HealthRecord'
- Line 15: Unused import 'statsmodels.tsa.arima.model.ARIMA'
- Line 25: Unused import 'pandas'
- Line 26: Unused import 'prophet.Prophet'

### src/piwardrive/analytics/predictive.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Mapping'
- Line 5: Unused import 'typing.Tuple'
- Line 7: Unused import 'numpy'
- Line 8: Unused import 'sklearn.linear_model.LinearRegression'

### src/piwardrive/analytics/iot.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Dict'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Mapping'
- Line 5: Unused import 'typing.Tuple'

### src/piwardrive/analytics/baseline.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Dict'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.List'
- Line 8: Unused import 'analysis.compute_health_stats'
- Line 9: Unused import 'persistence.HealthRecord'
- Line 9: Unused import 'persistence._get_conn'
- Line 9: Unused import 'persistence.flush_health_records'
- Line 50: Duplicate import 'cpu_pool.run_cpu_bound'

### src/piwardrive/analytics/__init__.py
- Line 3: Unused import 'clustering.cluster_positions'
- Line 4: Unused import 'forecasting.forecast_cpu_temp'
- Line 5: Unused import 'iot.correlate_city_services'
- Line 5: Unused import 'iot.fingerprint_iot_devices'
- Line 6: Unused import 'predictive.capacity_planning_forecast'
- Line 6: Unused import 'predictive.failure_prediction'
- Line 6: Unused import 'predictive.identify_expansion_opportunities'
- Line 6: Unused import 'predictive.linear_forecast'
- Line 6: Unused import 'predictive.predict_network_lifecycle'

### src/piwardrive/analytics/anomaly.py
- Line 1: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Iterable'
- Line 8: Unused import 'sklearn.ensemble.IsolationForest'
- Line 10: Unused import 'persistence.HealthRecord'

### src/piwardrive/analytics/clustering.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Iterable'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Mapping'
- Line 5: Unused import 'typing.Tuple'
- Line 7: Unused import 'numpy'
- Line 8: Unused import 'sklearn.cluster.DBSCAN'

### src/piwardrive/navigation/offline_navigation.py
- Line 21: Unused import 'collections.deque'
- Line 22: Unused import 'dataclasses.dataclass'
- Line 22: Unused import 'dataclasses.field'
- Line 24: Unused import 'enum.Enum'
- Line 25: Unused import 'pathlib.Path'
- Line 26: Unused import 'typing.Any'
- Line 26: Unused import 'typing.Callable'
- Line 26: Unused import 'typing.Dict'
- Line 26: Unused import 'typing.List'
- Line 26: Unused import 'typing.Optional'
- Line 26: Unused import 'typing.Set'
- Line 26: Unused import 'typing.Tuple'

### src/piwardrive/geospatial/intelligence.py
- Line 8: Unused import 'dataclasses.dataclass'
- Line 10: Unused import 'enum.Enum'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.NamedTuple'
- Line 11: Unused import 'typing.Optional'
- Line 11: Unused import 'typing.Tuple'
- Line 13: Unused import 'numpy'

### src/piwardrive/jobs/maintenance_jobs.py
- Line 1: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'
- Line 8: Unused import 'typing.Awaitable'
- Line 8: Unused import 'typing.Callable'
- Line 8: Unused import 'typing.Dict'

### src/piwardrive/jobs/analytics_jobs.py
- Line 1: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Awaitable'
- Line 7: Unused import 'typing.Callable'
- Line 7: Unused import 'typing.Dict'

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 26: Unused import 'collections.defaultdict'
- Line 26: Unused import 'collections.deque'
- Line 27: Unused import 'concurrent.futures.ThreadPoolExecutor'
- Line 28: Unused import 'dataclasses.dataclass'
- Line 28: Unused import 'dataclasses.field'
- Line 30: Unused import 'enum.Enum'
- Line 31: Unused import 'pathlib.Path'
- Line 32: Unused import 'typing.Any'
- Line 32: Unused import 'typing.AsyncGenerator'
- Line 32: Unused import 'typing.Callable'
- Line 32: Unused import 'typing.Dict'
- Line 32: Unused import 'typing.List'
- Line 32: Unused import 'typing.Optional'
- Line 32: Unused import 'typing.Set'
- Line 32: Unused import 'typing.Tuple'
- Line 32: Unused import 'typing.Union'
- Line 44: Unused import 'networkx'
- Line 45: Unused import 'numpy'
- Line 46: Unused import 'pandas'

### src/piwardrive/enhanced/critical_additions.py
- Line 20: Unused import 'collections.defaultdict'
- Line 20: Unused import 'collections.deque'
- Line 21: Unused import 'concurrent.futures.ThreadPoolExecutor'
- Line 22: Unused import 'dataclasses.dataclass'
- Line 22: Unused import 'dataclasses.field'
- Line 24: Unused import 'enum.Enum'
- Line 25: Unused import 'pathlib.Path'
- Line 26: Unused import 'typing.Any'
- Line 26: Unused import 'typing.AsyncGenerator'
- Line 26: Unused import 'typing.Callable'
- Line 26: Unused import 'typing.Dict'
- Line 26: Unused import 'typing.List'
- Line 26: Unused import 'typing.Optional'
- Line 26: Unused import 'typing.Set'
- Line 26: Unused import 'typing.Tuple'
- Line 26: Unused import 'typing.Union'
- Line 38: Unused import 'numpy'

### src/piwardrive/routes/websocket.py
- Line 1: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Any'

### src/piwardrive/routes/analytics.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'fastapi.APIRouter'
- Line 5: Unused import 'fastapi.Depends'
- Line 5: Unused import 'fastapi.HTTPException'

### src/piwardrive/routes/bluetooth.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'fastapi.APIRouter'
- Line 5: Unused import 'fastapi.Depends'

### src/piwardrive/routes/wifi.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'fastapi.APIRouter'
- Line 7: Unused import 'fastapi.Depends'

### src/piwardrive/routes/security.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'fastapi.APIRouter'
- Line 5: Unused import 'fastapi.Depends'

### src/piwardrive/routes/cellular.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'fastapi.APIRouter'
- Line 5: Unused import 'fastapi.Depends'

### src/piwardrive/plugins/plugin_architecture.py
- Line 24: Unused import 'dataclasses.dataclass'
- Line 24: Unused import 'dataclasses.field'
- Line 26: Unused import 'enum.Enum'
- Line 28: Unused import 'typing.Any'
- Line 28: Unused import 'typing.Callable'
- Line 28: Unused import 'typing.Dict'
- Line 28: Unused import 'typing.List'
- Line 28: Unused import 'typing.Optional'
- Line 28: Unused import 'typing.Set'
- Line 28: Unused import 'typing.Type'
- Line 28: Unused import 'typing.Union'

### src/piwardrive/protocols/multi_protocol.py
- Line 10: Unused import 'collections.defaultdict'
- Line 11: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'dataclasses.field'
- Line 13: Unused import 'enum.Enum'
- Line 14: Unused import 'typing.Any'
- Line 14: Unused import 'typing.Callable'
- Line 14: Unused import 'typing.Dict'
- Line 14: Unused import 'typing.List'
- Line 14: Unused import 'typing.Optional'
- Line 14: Unused import 'typing.Set'
- Line 14: Unused import 'typing.Tuple'
- Line 805: Duplicate import 'numpy'
- Line 1009: Duplicate import 'numpy'

### src/piwardrive/scripts/service_status.py
- Line 6: Unused import 'types.SimpleNamespace'

### src/piwardrive/scripts/scan_report.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/scripts/cleanup_cache.py
- Line 5: Unused import 'piwardrive.map.tile_maintenance'

### src/piwardrive/api/widget_marketplace.py
- Line 1: Unused import '__future__.annotations'
- Line 6: Unused import 'pathlib.Path'
- Line 7: Unused import 'typing.Any'
- Line 9: Unused import 'fastapi.APIRouter'
- Line 11: Unused import 'piwardrive.api.auth.AUTH_DEP'

### src/piwardrive/api/maintenance_jobs.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Dict'
- Line 7: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/analytics_jobs.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Any'
- Line 3: Unused import 'typing.Dict'
- Line 5: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/logging_control.py
- Line 3: Unused import 'flask.Blueprint'
- Line 3: Unused import 'flask.jsonify'
- Line 3: Unused import 'flask.request'

### src/piwardrive/api/performance_dashboard.py
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.List'
- Line 11: Unused import 'typing.Optional'
- Line 120: Duplicate import 'piwardrive.core.persistence._db_path'
- Line 172: Duplicate import 'piwardrive.core.persistence._db_path'
- Line 283: Duplicate import 'piwardrive.core.persistence._db_path'
- Line 327: Duplicate import 'piwardrive.core.persistence._db_path'

### src/piwardrive/api/common.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'http.HTTPStatus'

### src/piwardrive/visualization/advanced_viz.py
- Line 10: Unused import 'dataclasses.dataclass'
- Line 12: Unused import 'io.BytesIO'
- Line 13: Unused import 'typing.Any'
- Line 13: Unused import 'typing.Dict'
- Line 13: Unused import 'typing.List'
- Line 13: Unused import 'typing.Optional'
- Line 13: Unused import 'typing.Tuple'
- Line 15: Unused import 'numpy'
- Line 16: Unused import 'pandas'
- Line 505: Unused import 'geopy.distance.geodesic'

### src/piwardrive/visualization/advanced_visualization.py
- Line 23: Unused import 'dataclasses.dataclass'
- Line 23: Unused import 'dataclasses.field'
- Line 25: Unused import 'enum.Enum'
- Line 26: Unused import 'pathlib.Path'
- Line 27: Unused import 'typing.Any'
- Line 27: Unused import 'typing.Callable'
- Line 27: Unused import 'typing.Dict'
- Line 27: Unused import 'typing.List'
- Line 27: Unused import 'typing.Optional'
- Line 27: Unused import 'typing.Set'
- Line 27: Unused import 'typing.Tuple'
- Line 27: Unused import 'typing.Union'
- Line 32: Unused import 'pandas'

### src/piwardrive/widgets/disk_trend.py
- Line 3: Unused import 'typing.Any'
- Line 8: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/security_score.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/health_analysis.py
- Line 5: Unused import 'typing.Any'
- Line 16: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/alert_summary.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/signal_strength.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/heatmap.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.Any'
- Line 18: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/lora_scan_widget.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/system_resource.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/db_stats.py
- Line 13: Unused import 'base.DashboardWidget'
- Line 30: Unused import 'concurrent.futures.Future'
- Line 31: Duplicate import 'typing.Any'

### src/piwardrive/widgets/base.py
- Line 3: Unused import 'typing.Any'
- Line 5: Unused import 'piwardrive.simpleui.BoxLayout'

### src/piwardrive/widgets/service_status.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/network_density.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/net_throughput.py
- Line 3: Unused import 'typing.Any'
- Line 7: Unused import 'piwardrive.localization._'
- Line 9: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/scanner_status.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/storage_usage.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/suspicious_activity.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/database_health.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/vehicle_speed.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/__init__.py
- Line 9: Unused import 'importlib.import_module'
- Line 9: Unused import 'importlib.machinery'
- Line 9: Unused import 'importlib.util'
- Line 10: Unused import 'pathlib.Path'
- Line 11: Unused import 'typing.Any'
- Line 11: Unused import 'typing.Callable'
- Line 11: Unused import 'typing.Dict'
- Line 11: Unused import 'typing.Iterable'
- Line 11: Unused import 'typing.Optional'

### src/piwardrive/widgets/threat_map.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/health_status.py
- Line 4: Unused import 'typing.Any'
- Line 11: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/gps_status.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/handshake_counter.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/log_viewer.py
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.List'
- Line 16: Duplicate import 'piwardrive.utils.tail_file'

### src/piwardrive/widgets/detection_rate.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/battery_status.py
- Line 4: Unused import 'typing.Any'
- Line 13: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/threat_level.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/cpu_temp_graph.py
- Line 3: Unused import 'typing.Any'
- Line 8: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/device_classification.py
- Line 4: Unused import 'typing.Any'
- Line 10: Unused import 'base.DashboardWidget'

### src/piwardrive/widgets/orientation_widget.py
- Line 4: Unused import 'typing.Any'
- Line 12: Unused import 'base.DashboardWidget'

### src/piwardrive/data_processing/enhanced_processing.py
- Line 14: Unused import 'collections.defaultdict'
- Line 14: Unused import 'collections.deque'
- Line 15: Unused import 'concurrent.futures.ThreadPoolExecutor'
- Line 16: Unused import 'dataclasses.asdict'
- Line 16: Unused import 'dataclasses.dataclass'
- Line 18: Unused import 'pathlib.Path'
- Line 19: Unused import 'typing.Any'
- Line 19: Unused import 'typing.Callable'
- Line 19: Unused import 'typing.Dict'
- Line 19: Unused import 'typing.List'
- Line 19: Unused import 'typing.Optional'
- Line 19: Unused import 'typing.Tuple'
- Line 19: Unused import 'typing.Union'
- Line 22: Unused import 'numpy'
- Line 23: Unused import 'pandas'
- Line 24: Unused import 'scipy.stats'

### src/piwardrive/mining/advanced_data_mining.py
- Line 8: Unused import 'collections.Counter'
- Line 8: Unused import 'collections.defaultdict'
- Line 9: Unused import 'dataclasses.dataclass'
- Line 9: Unused import 'dataclasses.field'
- Line 11: Unused import 'enum.Enum'
- Line 12: Unused import 'typing.Any'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 12: Unused import 'typing.Optional'
- Line 12: Unused import 'typing.Set'
- Line 12: Unused import 'typing.Tuple'
- Line 14: Unused import 'numpy'
- Line 757: Unused import 'itertools.combinations'

### src/piwardrive/logging/storage.py
- Line 4: Unused import 'concurrent.futures.ThreadPoolExecutor'
- Line 6: Unused import 'pathlib.Path'
- Line 7: Unused import 'typing.Dict'

### src/piwardrive/logging/structured_logger.py
- Line 19: Unused import 'contextvars.ContextVar'
- Line 20: Unused import 'dataclasses.asdict'
- Line 20: Unused import 'dataclasses.dataclass'
- Line 22: Unused import 'importlib.metadata.PackageNotFoundError'
- Line 22: Unused import 'importlib.metadata.version'
- Line 23: Unused import 'typing.Any'
- Line 23: Unused import 'typing.Dict'
- Line 23: Unused import 'typing.Optional'
- Line 23: Unused import 'typing.Union'
- Line 25: Unused import 'fastjson.dumps'
- Line 160: Duplicate import 'os'

### src/piwardrive/logging/config.py
- Line 1: Unused import '__future__.annotations'
- Line 6: Unused import 'pathlib.Path'
- Line 7: Unused import 'typing.Any'
- Line 7: Unused import 'typing.Dict'
- Line 7: Unused import 'typing.Optional'

### src/piwardrive/logging/levels.py
- Line 2: Unused import 'enum.IntEnum'
- Line 3: Unused import 'typing.Any'
- Line 3: Unused import 'typing.Callable'
- Line 3: Unused import 'typing.Dict'
- Line 3: Unused import 'typing.Optional'
- Line 3: Unused import 'typing.Set'

### src/piwardrive/logging/__init__.py
- Line 3: Unused import 'config.LoggingConfig'
- Line 4: Unused import 'structured_logger.LogContext'
- Line 4: Unused import 'structured_logger.PiWardriveLogger'
- Line 4: Unused import 'structured_logger.StructuredFormatter'
- Line 4: Unused import 'structured_logger.get_logger'
- Line 4: Unused import 'structured_logger.set_log_context'

### src/piwardrive/logging/scheduler.py
- Line 3: Unused import 'typing.TYPE_CHECKING'
- Line 3: Unused import 'typing.Callable'
- Line 3: Unused import 'typing.List'
- Line 7: Unused import 'storage.LogRetentionManager'

### src/piwardrive/logging/rotation.py
- Line 9: Unused import 'dataclasses.dataclass'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Callable'
- Line 12: Unused import 'typing.Dict'
- Line 12: Unused import 'typing.List'
- Line 12: Unused import 'typing.Optional'
- Line 14: Unused import 'prometheus_client.Counter'
- Line 14: Unused import 'prometheus_client.Gauge'
- Line 14: Unused import 'prometheus_client.Histogram'
- Line 17: Unused import 'storage.LogArchiveManager'
- Line 17: Unused import 'storage.LogRetentionManager'

### src/piwardrive/logging/dynamic_config.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'pathlib.Path'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Callable'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.List'
- Line 15: Unused import 'exceptions.ConfigurationError'
- Line 15: Unused import 'exceptions.ServiceError'

### src/piwardrive/logging/filters.py
- Line 4: Unused import 'collections.defaultdict'
- Line 4: Unused import 'collections.deque'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Dict'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Optional'
- Line 5: Unused import 'typing.Pattern'

### src/piwardrive/signal/rf_spectrum.py
- Line 8: Unused import 'dataclasses.dataclass'
- Line 9: Unused import 'enum.Enum'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.List'
- Line 10: Unused import 'typing.NamedTuple'
- Line 10: Unused import 'typing.Optional'
- Line 10: Unused import 'typing.Tuple'
- Line 12: Unused import 'numpy'

### src/piwardrive/integrations/sigint_suite/plugins.py
- Line 9: Unused import '__future__.annotations'
- Line 13: Unused import 'importlib.util'
- Line 14: Unused import 'pathlib.Path'
- Line 15: Unused import 'types.ModuleType'
- Line 16: Unused import 'typing.Dict'
- Line 18: Unused import 'paths.CONFIG_DIR'

### src/piwardrive/integrations/sigint_suite/hooks.py
- Line 3: Unused import 'collections.defaultdict'
- Line 4: Unused import 'typing.Any'
- Line 4: Unused import 'typing.Callable'
- Line 4: Unused import 'typing.Dict'
- Line 4: Unused import 'typing.List'

### src/piwardrive/integrations/sigint_suite/continuous_scan.py
- Line 3: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Callable'
- Line 6: Unused import 'typing.Dict'
- Line 6: Unused import 'typing.List'
- Line 8: Unused import 'piwardrive.task_queue.BackgroundTaskQueue'

### src/piwardrive/integrations/sigint_suite/models.py
- Line 3: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Optional'
- Line 7: Unused import 'pydantic.BaseModel'
- Line 7: Unused import 'pydantic.ConfigDict'

### src/piwardrive/integrations/sigint_suite/__init__.py
- Line 5: Unused import 'typing.Any'
- Line 7: Unused import 'piwardrive.logging.init_logging'

### src/piwardrive/integrations/sigint_suite/enrichment/__init__.py
- Line 3: Unused import 'oui.cached_lookup_vendor'
- Line 3: Unused import 'oui.load_oui_map'
- Line 3: Unused import 'oui.lookup_vendor'

### src/piwardrive/integrations/sigint_suite/enrichment/oui.py
- Line 3: Unused import '__future__.annotations'
- Line 9: Unused import 'functools.lru_cache'
- Line 10: Unused import 'typing.TYPE_CHECKING'
- Line 10: Unused import 'typing.Any'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.NoReturn'
- Line 10: Unused import 'typing.Optional'
- Line 10: Unused import 'typing.cast'

### src/piwardrive/integrations/sigint_suite/rf/spectrum.py
- Line 3: Unused import 'typing.List'
- Line 3: Unused import 'typing.Tuple'
- Line 3: Unused import 'typing.cast'
- Line 5: Unused import 'numpy'
- Line 8: Unused import 'rtlsdr.RtlSdr'

### src/piwardrive/integrations/sigint_suite/rf/utils.py
- Line 3: Unused import '__future__.annotations'

### src/piwardrive/integrations/sigint_suite/rf/__init__.py
- Line 3: Unused import 'demod.demodulate_fm'
- Line 4: Unused import 'spectrum.spectrum_scan'
- Line 5: Unused import 'utils.ghz_to_hz'
- Line 5: Unused import 'utils.hz_to_ghz'
- Line 5: Unused import 'utils.hz_to_khz'
- Line 5: Unused import 'utils.hz_to_mhz'
- Line 5: Unused import 'utils.khz_to_hz'
- Line 5: Unused import 'utils.mhz_to_hz'
- Line 5: Unused import 'utils.parse_frequency'

### src/piwardrive/integrations/sigint_suite/rf/demod.py
- Line 3: Unused import 'typing.List'
- Line 3: Unused import 'typing.cast'
- Line 5: Unused import 'numpy'
- Line 8: Unused import 'rtlsdr.RtlSdr'

### src/piwardrive/integrations/sigint_suite/bluetooth/__init__.py
- Line 3: Unused import 'scanner.scan_bluetooth'
- Line 3: Unused import 'scanner.start_scanner'
- Line 3: Unused import 'scanner.stop_scanner'

### src/piwardrive/integrations/sigint_suite/bluetooth/scanner.py
- Line 8: Unused import 'typing.Dict'
- Line 8: Unused import 'typing.List'

### src/piwardrive/integrations/sigint_suite/wifi/__init__.py
- Line 3: Unused import 'scanner.scan_wifi'

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 3: Unused import '__future__.annotations'
- Line 10: Unused import 'typing.Dict'
- Line 10: Unused import 'typing.Iterable'
- Line 10: Unused import 'typing.List'
- Line 10: Unused import 'typing.Optional'
- Line 10: Unused import 'typing.Union'

### src/piwardrive/integrations/sigint_suite/cellular/utils.py
- Line 3: Unused import '__future__.annotations'
- Line 7: Unused import 'typing.List'
- Line 7: Unused import 'typing.Optional'
- Line 7: Unused import 'typing.Tuple'

### src/piwardrive/integrations/sigint_suite/cellular/__init__.py
- Line 3: Unused import 'band_scanner.async_scan_bands'
- Line 3: Unused import 'band_scanner.scan_bands'
- Line 4: Unused import 'imsi_catcher.async_scan_imsis'
- Line 4: Unused import 'imsi_catcher.scan_imsis'
- Line 5: Unused import 'tower_scanner.async_scan_towers'
- Line 5: Unused import 'tower_scanner.scan_towers'

### src/piwardrive/integrations/sigint_suite/exports/__init__.py
- Line 3: Unused import 'exporter.EXPORT_FORMATS'
- Line 3: Unused import 'exporter.export_csv'
- Line 3: Unused import 'exporter.export_json'
- Line 3: Unused import 'exporter.export_records'
- Line 3: Unused import 'exporter.export_yaml'

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 5: Unused import 'dataclasses.asdict'
- Line 5: Unused import 'dataclasses.is_dataclass'
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Iterable'
- Line 6: Unused import 'typing.Mapping'
- Line 6: Unused import 'typing.Sequence'

### src/piwardrive/integrations/sigint_suite/gps/__init__.py
- Line 3: Unused import 'typing.Optional'
- Line 3: Unused import 'typing.Tuple'
- Line 5: Unused import 'piwardrive.gpsd_client.client'

### src/piwardrive/integrations/sigint_suite/dashboard/__init__.py
- Line 13: Unused import '__future__.annotations'
- Line 18: Unused import 'typing.Any'
- Line 18: Unused import 'typing.Dict'
- Line 18: Unused import 'typing.List'
- Line 18: Unused import 'typing.Mapping'

### src/piwardrive/integrations/sigint_suite/cellular/parsers/__init__.py
- Line 3: Unused import 'typing.List'
- Line 5: Unused import 'piwardrive.sigint_suite.models.BandRecord'
- Line 5: Unused import 'piwardrive.sigint_suite.models.ImsiRecord'
- Line 5: Unused import 'piwardrive.sigint_suite.models.TowerRecord'

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/__init__.py
- Line 3: Unused import 'scanner.async_scan_bands'
- Line 3: Unused import 'scanner.scan_bands'

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 8: Unused import 'typing.List'
- Line 8: Unused import 'typing.Optional'
- Line 8: Unused import 'typing.cast'

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/__init__.py
- Line 3: Unused import 'scanner.async_scan_imsis'
- Line 3: Unused import 'scanner.scan_imsis'

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Callable'
- Line 6: Unused import 'typing.List'
- Line 6: Unused import 'typing.Optional'
- Line 6: Unused import 'typing.cast'
- Line 15: Unused import 'utils.build_cmd_args'

### src/piwardrive/integrations/sigint_suite/cellular/tower_tracker/__init__.py
- Line 3: Unused import 'tracker.TowerTracker'

### src/piwardrive/integrations/sigint_suite/cellular/tower_tracker/tracker.py
- Line 4: Unused import 'types.TracebackType'
- Line 5: Unused import 'typing.Dict'
- Line 5: Unused import 'typing.List'
- Line 5: Unused import 'typing.Optional'

### src/piwardrive/integrations/sigint_suite/cellular/tower_scanner/__init__.py
- Line 3: Unused import 'scanner.async_scan_towers'
- Line 3: Unused import 'scanner.scan_towers'

### src/piwardrive/integrations/sigint_suite/cellular/tower_scanner/scanner.py
- Line 6: Unused import 'typing.List'
- Line 6: Unused import 'typing.Optional'
- Line 15: Unused import 'utils.build_cmd_args'

### src/piwardrive/sigint_suite/cellular/imsi_catcher/__init__.py
- Line 1: Unused import 'integrations.sigint_suite.cellular.imsi_catcher.*'

### src/piwardrive/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 3: Unused import 'piwardrive.integrations.sigint_suite.cellular.imsi_catcher.scanner.*'

### src/piwardrive/sigint_suite/cellular/tower_tracker/__init__.py
- Line 1: Unused import 'integrations.sigint_suite.cellular.tower_tracker.*'

### src/piwardrive/api/monitoring/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 7: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/monitoring/__init__.py
- Line 1: Unused import 'endpoints.router'

### src/piwardrive/api/websockets/handlers.py
- Line 1: Unused import '__future__.annotations'
- Line 8: Unused import 'typing.Any'

### src/piwardrive/api/websockets/__init__.py
- Line 1: Unused import 'events.broadcast_events'
- Line 2: Unused import 'handlers.router'

### src/piwardrive/api/websockets/events.py
- Line 1: Unused import '__future__.annotations'
- Line 4: Unused import 'typing.AsyncGenerator'

### src/piwardrive/api/health/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 7: Unused import 'dataclasses.asdict'
- Line 8: Unused import 'typing.Any'
- Line 19: Unused import 'models.BaselineAnalysisResult'
- Line 19: Unused import 'models.HealthRecordDict'
- Line 19: Unused import 'models.SyncResponse'

### src/piwardrive/api/health/models.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.TypedDict'

### src/piwardrive/api/health/__init__.py
- Line 1: Unused import 'endpoints.router'
- Line 2: Unused import 'models.BaselineAnalysisResult'
- Line 2: Unused import 'models.HealthRecordDict'

### src/piwardrive/api/auth/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 14: Unused import 'health.models.AuthLoginResponse'
- Line 14: Unused import 'health.models.LogoutResponse'
- Line 14: Unused import 'health.models.TokenResponse'
- Line 19: Unused import 'dependencies.AUTH_DEP'
- Line 19: Unused import 'dependencies.SECURITY_DEP'
- Line 19: Unused import 'dependencies.ensure_default_user'

### src/piwardrive/api/auth/dependencies.py
- Line 1: Unused import '__future__.annotations'

### src/piwardrive/api/auth/__init__.py
- Line 1: Unused import 'dependencies.AUTH_DEP'
- Line 1: Unused import 'dependencies.check_auth'
- Line 2: Unused import 'endpoints.router'
- Line 3: Unused import 'middleware.AuthMiddleware'

### src/piwardrive/api/auth/middleware.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'fastapi.FastAPI'
- Line 3: Unused import 'fastapi.Request'
- Line 7: Unused import 'dependencies.check_auth'

### src/piwardrive/api/demographics/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 5: Unused import 'typing.Any'
- Line 5: Unused import 'typing.Dict'
- Line 7: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/demographics/__init__.py
- Line 1: Unused import 'endpoints.router'

### src/piwardrive/api/analytics/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Any'
- Line 5: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/analytics/__init__.py
- Line 1: Unused import 'endpoints.router'

### src/piwardrive/api/system/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 9: Unused import 'dataclasses.asdict'
- Line 11: Unused import 'pathlib.Path'
- Line 12: Unused import 'typing.Any'
- Line 345: Duplicate import 'sigint_integration.load_sigint_data'

### src/piwardrive/api/system/__init__.py
- Line 1: Unused import 'endpoints_simple.router'
- Line 2: Unused import 'monitoring.collect_widget_metrics'

### src/piwardrive/api/system/endpoints_simple.py
- Line 3: Unused import 'typing.Any'
- Line 3: Unused import 'typing.Dict'
- Line 4: Unused import 'fastapi.APIRouter'
- Line 5: Unused import 'piwardrive.api.auth.AUTH_DEP'

### src/piwardrive/api/system/monitoring.py
- Line 1: Unused import '__future__.annotations'

### src/piwardrive/api/widgets/__init__.py
- Line 1: Unused import '__future__.annotations'
- Line 6: Unused import 'typing.Any'
- Line 6: Unused import 'typing.Dict'
- Line 6: Unused import 'typing.List'
- Line 6: Unused import 'typing.TypedDict'
- Line 8: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/analysis_queries/endpoints.py
- Line 1: Unused import '__future__.annotations'
- Line 3: Unused import 'typing.Any'
- Line 5: Unused import 'fastapi.APIRouter'

### src/piwardrive/api/analysis_queries/__init__.py
- Line 1: Unused import 'endpoints.router'

## Missing Docstrings

### comprehensive_code_analyzer.py
- Line 16: Missing docstring for class 'ComprehensiveCodeAnalyzer'

### test_imports.py
- Line 9: Missing docstring for function 'timeout_handler'

### quality_summary.py
- Line 20: Missing docstring for function 'main'

### tools/sync_receiver.py
- Line 14: Missing docstring for function 'receive'

### tests/test_load_kismet_data.py
- Line 28: Missing docstring for function 'test_load_kismet_data_filters_and_returns_dataframe'

### tests/test_gps_handler.py
- Line 14: Missing docstring for class '_DummyBase'
- Line 25: Missing docstring for function 'test_position_none_on_connect_failure'
- Line 34: Missing docstring for function 'test_timeout_returns_none'
- Line 46: Missing docstring for function 'test_reconnect_after_error'
- Line 26: Missing docstring for class 'Dummy'
- Line 35: Missing docstring for class 'Dummy'
- Line 52: Missing docstring for class 'Dummy'
- Line 56: Missing docstring for function 'next'

### tests/test_cli_tools.py
- Line 28: Missing docstring for function 'test_config_cli_get_local'
- Line 35: Missing docstring for function 'test_config_cli_set_local'
- Line 50: Missing docstring for function 'test_config_cli_get_api'
- Line 62: Missing docstring for function 'test_config_cli_set_api'
- Line 80: Missing docstring for function 'test_config_cli_get_unknown_local'
- Line 87: Missing docstring for function 'test_config_cli_set_unknown_local'
- Line 94: Missing docstring for function 'test_config_cli_get_unknown_api'
- Line 106: Missing docstring for function 'test_config_cli_set_unknown_api'
- Line 53: Missing docstring for function 'fake_get'
- Line 65: Missing docstring for function 'fake_get'
- Line 69: Missing docstring for function 'fake_update'
- Line 97: Missing docstring for function 'fake_get'
- Line 109: Missing docstring for function 'fake_get'

### tests/test_route_optimizer.py
- Line 10: Missing docstring for function 'test_suggest_route_unvisited_cells'

### tests/test_config_watcher.py
- Line 6: Missing docstring for function 'test_watch_config_triggers'

### tests/test_integration_comprehensive.py
- Line 371: Missing docstring for function 'data_processor'
- Line 375: Missing docstring for function 'data_sink'

### tests/test_rf_utils.py
- Line 15: Missing docstring for class 'DummySdr'
- Line 29: Missing docstring for function 'test_spectrum_scan_returns_power'
- Line 41: Missing docstring for class 'SignalSdr'
- Line 47: Missing docstring for function 'test_demodulate_fm'
- Line 59: Missing docstring for function 'test_missing_rtlsdr'
- Line 68: Missing docstring for function 'test_fm_demodulate_basic'
- Line 74: Missing docstring for function 'test_frequency_conversions'
- Line 80: Missing docstring for function 'test_parse_frequency'
- Line 42: Missing docstring for function 'read_samples'

### tests/test_webui_server_main.py
- Line 7: Missing docstring for function 'test_main_runs_uvicorn'
- Line 19: Missing docstring for function 'test_main_env_port'

### tests/test_service_main.py
- Line 8: Missing docstring for function 'test_main_starts_uvicorn'

### tests/test_diagnostics.py
- Line 22: Missing docstring for function 'test_generate_system_report_includes_temp'
- Line 35: Missing docstring for function 'test_self_test_returns_extra_info'
- Line 52: Missing docstring for function 'test_self_test_restarts_failed_services'
- Line 74: Missing docstring for function 'test_stop_profiling_writes_callgrind'
- Line 85: Missing docstring for function 'test_rotate_log_gz'
- Line 105: Missing docstring for function 'test_rotate_log_upload'
- Line 124: Missing docstring for function 'test_rotate_log_max_files_check'
- Line 131: Missing docstring for function 'test_rotate_log_async_max_files_check'
- Line 138: Missing docstring for function 'test_run_network_test_caches_success'
- Line 158: Missing docstring for function 'test_run_network_test_cache_expires'
- Line 177: Missing docstring for function 'test_run_network_test_handles_failure'
- Line 188: Missing docstring for function 'test_list_usb_devices_handles_failure'
- Line 145: Missing docstring for function 'fake_run'
- Line 165: Missing docstring for function 'fake_run'

### tests/test_interfaces.py
- Line 42: Missing docstring for class 'TestMapService'
- Line 174: Missing docstring for function 'mock_generator'
- Line 211: Missing docstring for class 'TestDataCollector'
- Line 354: Missing docstring for class 'MockMapService'
- Line 361: Missing docstring for class 'MockDataCollector'

### tests/test_orientation_sensors_pkg.py
- Line 8: Missing docstring for function 'test_orientation_to_angle_pkg'
- Line 14: Missing docstring for function 'test_orientation_to_angle_custom_map_pkg'
- Line 19: Missing docstring for function 'test_update_orientation_map_pkg'
- Line 27: Missing docstring for function 'test_get_orientation_dbus_missing_pkg'
- Line 32: Missing docstring for function 'test_get_orientation_dbus_success_pkg'
- Line 60: Missing docstring for function 'test_read_mpu6050_missing_pkg'
- Line 65: Missing docstring for function 'test_read_mpu6050_success_pkg'
- Line 81: Missing docstring for function 'test_read_mpu6050_env_pkg'
- Line 99: Missing docstring for function 'test_reset_orientation_map_unsafe_pkg'
- Line 33: Missing docstring for class 'DummyIface'
- Line 46: Missing docstring for class 'DummyBus'
- Line 66: Missing docstring for class 'DummySensor'
- Line 82: Missing docstring for class 'DummySensor'

### tests/test_db_stats_widget.py
- Line 10: Missing docstring for function 'test_widget_update'

### tests/test_kiosk_cli.py
- Line 7: Missing docstring for function 'test_kiosk_cli_launches_browser'

### tests/test_security.py
- Line 8: Missing docstring for function 'test_hash_and_verify_password'
- Line 14: Missing docstring for function 'test_validate_service_name'
- Line 20: Missing docstring for function 'test_sanitize_path_valid'
- Line 31: Missing docstring for function 'test_validate_filename'
- Line 37: Missing docstring for function 'test_sanitize_filename'

### tests/test_sigint_scanners_basic.py
- Line 30: Missing docstring for function 'test_parse_iwlist_output'
- Line 45: Missing docstring for function 'test_scan_wifi'
- Line 60: Missing docstring for function 'test_scan_bluetoothctl'
- Line 69: Missing docstring for function 'test_async_scan_bluetoothctl'
- Line 70: Missing docstring for function 'fake_proc'
- Line 71: Missing docstring for class 'P'

### tests/test_vendor_lookup.py
- Line 18: Missing docstring for function 'test_update_oui_file_downloads'
- Line 46: Missing docstring for function 'test_update_oui_file_logs_error'
- Line 22: Missing docstring for class 'Resp'
- Line 36: Missing docstring for function 'fail'

### tests/test_imsi_catcher.py
- Line 11: Missing docstring for function 'test_scan_imsis_parses_output_and_tags_location'
- Line 39: Missing docstring for function 'test_scan_imsis_custom_hook'
- Line 50: Missing docstring for function 'add_op'

### tests/test_widget_cache.py
- Line 7: Missing docstring for function 'test_widget_plugin_cache'
- Line 24: Missing docstring for function 'wrapped'

### tests/test_config_env_webhooks.py
- Line 6: Missing docstring for function 'setup_tmp'
- Line 17: Missing docstring for function 'test_env_override_list'

### tests/test_iot_analytics.py
- Line 7: Missing docstring for function 'test_fingerprint_iot_devices_basic'
- Line 30: Missing docstring for function 'test_correlate_city_services_window'

### tests/test_aggregation_service_main_new.py
- Line 6: Missing docstring for function 'test_main_starts_uvicorn'

### tests/test_config_runtime.py
- Line 6: Missing docstring for function 'setup_tmp'
- Line 14: Missing docstring for function 'test_config_mtime_updates'
- Line 26: Missing docstring for function 'test_config_mtime_returns_timestamp'

### tests/test_direction_finding.py
- Line 469: Missing docstring for function 'test_callback'

### tests/test_utils.py
- Line 40: Missing docstring for function 'test_format_error_with_enum'
- Line 64: Missing docstring for function 'test_tail_file_returns_last_lines'
- Line 76: Missing docstring for function 'test_tail_file_missing_returns_empty_list'
- Line 81: Missing docstring for function 'test_tail_file_nonpositive_lines'
- Line 92: Missing docstring for function 'test_tail_file_handles_large_file'
- Line 102: Missing docstring for function 'test_tail_file_cache'
- Line 175: Missing docstring for function 'test_run_service_cmd_success'
- Line 185: Missing docstring for function 'test_run_service_cmd_failure'
- Line 195: Missing docstring for function 'test_run_service_cmd_retries_until_success'
- Line 212: Missing docstring for function 'test_message_bus_disconnect_called'
- Line 251: Missing docstring for function 'test_service_status_passes_retry_params'
- Line 260: Missing docstring for function 'test_point_in_polygon_basic'
- Line 266: Missing docstring for function 'test_load_kml_parses_features'
- Line 281: Missing docstring for function 'test_load_kmz_parses_features'
- Line 295: Missing docstring for function 'test_fetch_kismet_devices_request_exception'
- Line 314: Missing docstring for function 'test_fetch_kismet_devices_json_error'
- Line 345: Missing docstring for function 'test_get_smart_status_ok'
- Line 358: Missing docstring for function 'test_get_smart_status_failure'
- Line 372: Missing docstring for function 'test_fetch_kismet_devices_async'
- Line 401: Missing docstring for function 'test_fetch_kismet_devices_async_logs_cache_error'
- Line 436: Missing docstring for function 'test_fetch_kismet_devices_cache'
- Line 471: Missing docstring for function 'test_fetch_kismet_devices_async_cache'
- Line 509: Missing docstring for function 'test_safe_request_retries'
- Line 535: Missing docstring for function 'test_safe_request_cache'
- Line 564: Missing docstring for function 'test_safe_request_cache_pruning'
- Line 602: Missing docstring for function 'test_ensure_service_running_attempts_restart'
- Line 619: Missing docstring for function 'test_scan_bt_devices_parses_output'
- Line 659: Missing docstring for function 'test_scan_bt_devices_handles_error'
- Line 669: Missing docstring for function 'test_gpsd_cache'
- Line 697: Missing docstring for function 'test_count_bettercap_handshakes'
- Line 712: Missing docstring for function 'test_count_bettercap_handshakes_missing'
- Line 717: Missing docstring for function 'test_count_bettercap_handshakes_cache'
- Line 735: Missing docstring for function 'test_network_scanning_disabled'
- Line 741: Missing docstring for function 'test_get_network_throughput_interface'
- Line 764: Missing docstring for function 'test_network_scanning_disabled_logs'
- Line 772: Missing docstring for function 'test_get_network_throughput_calculates_kbps'
- Line 786: Missing docstring for function 'test_get_network_throughput_resets_when_cache_missing'
- Line 821: Missing docstring for function 'test_get_mem_usage_cache'
- Line 840: Missing docstring for function 'test_get_disk_usage_cache'
- Line 110: Missing docstring for function 'fail'
- Line 122: Missing docstring for class 'Bus'
- Line 153: Missing docstring for class 'Bus'
- Line 157: Missing docstring for class 'Manager'
- Line 198: Missing docstring for function 'start_side'
- Line 215: Missing docstring for class 'Bus'
- Line 296: Missing docstring for class 'FakeSession'
- Line 315: Missing docstring for class 'FakeResp'
- Line 327: Missing docstring for class 'FakeSession'
- Line 373: Missing docstring for class 'FakeResp'
- Line 385: Missing docstring for class 'FakeSession'
- Line 402: Missing docstring for class 'FakeResp'
- Line 414: Missing docstring for class 'FakeSession'
- Line 454: Missing docstring for class 'FakeSession'
- Line 474: Missing docstring for class 'FakeResp'
- Line 486: Missing docstring for class 'FakeSession'
- Line 512: Missing docstring for class 'Resp'
- Line 519: Missing docstring for function 'get'
- Line 538: Missing docstring for class 'Resp'
- Line 546: Missing docstring for function 'request'
- Line 565: Missing docstring for class 'Resp'
- Line 586: Missing docstring for function 'timer'
- Line 624: Missing docstring for class 'Props'
- Line 629: Missing docstring for class 'Bus'
- Line 742: Missing docstring for class 'C'
- Line 749: Missing docstring for function 'fake_counters'
- Line 132: Missing docstring for function 'get_proxy_object'
- Line 158: Missing docstring for function 'GetManagedObjects'
- Line 227: Missing docstring for function 'get_proxy_object'
- Line 234: Missing docstring for function 'disconnect'
- Line 493: Missing docstring for function 'get'
- Line 625: Missing docstring for function 'Get'
- Line 903: Missing docstring for function 'mock_request'
- Line 933: Missing docstring for function 'mock_request'
- Line 986: Missing docstring for function 'mock_request'
- Line 133: Missing docstring for class 'Obj'
- Line 228: Missing docstring for class 'Obj'
- Line 969: Missing docstring for function 'mock_request'

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 9: Missing docstring for function 'test_plot_cpu_temp_plotly_backend'
- Line 10: Missing docstring for class 'FakeSeries'
- Line 31: Missing docstring for class 'FakeDataFrame'
- Line 11: Missing docstring for function 'rolling'
- Line 44: Missing docstring for function 'sort_values'
- Line 12: Missing docstring for class 'Roll'
- Line 16: Missing docstring for function 'mean'

### tests/test_logconfig.py
- Line 10: Missing docstring for function 'test_setup_logging_writes_json'
- Line 20: Missing docstring for function 'test_setup_logging_respects_env'
- Line 32: Missing docstring for function 'test_setup_logging_stdout'

### tests/test_hooks.py
- Line 5: Missing docstring for function 'test_custom_post_processor'
- Line 19: Missing docstring for function 'add_custom'

### tests/test_sigint_plugins.py
- Line 5: Missing docstring for function 'test_sigint_plugin_loaded'
- Line 20: Missing docstring for function 'test_sigint_plugin_error'

### tests/test_new_widgets.py
- Line 14: Missing docstring for function 'test_gps_status_widget'
- Line 23: Missing docstring for function 'test_service_status_widget'
- Line 32: Missing docstring for function 'test_handshake_counter_widget'
- Line 41: Missing docstring for function 'test_storage_usage_widget'
- Line 50: Missing docstring for function 'test_signal_strength_widget'

### tests/test_tower_tracking.py
- Line 25: Missing docstring for function 'test_tracker_update_and_query'
- Line 37: Missing docstring for function 'test_wifi_and_bluetooth_logging'
- Line 54: Missing docstring for function 'test_async_logging_and_retrieval'
- Line 67: Missing docstring for function 'test_tower_history'

### tests/test_web_server_main.py
- Line 7: Missing docstring for function 'test_main_runs_uvicorn'

### tests/test_vehicle_sensors.py
- Line 6: Missing docstring for function 'test_read_rpm_obd_missing'
- Line 11: Missing docstring for function 'test_read_engine_load_obd_success'
- Line 12: Missing docstring for class 'DummyVal'
- Line 19: Missing docstring for class 'DummyConn'

### tests/test_prune_db_script.py
- Line 4: Missing docstring for function 'test_prune_db_script'

### tests/test_core_config.py
- Line 560: Missing docstring for function 'save_config_worker'

### tests/test_service_direct_import.py
- Line 82: Missing docstring for function 'mock_create_app'

### tests/test_advanced_localization.py
- Line 15: Missing docstring for function 'test_kalman_1d_empty'
- Line 21: Missing docstring for function 'test_kalman_1d_sample_values'
- Line 28: Missing docstring for function 'test_kalman_1d_constant_series'
- Line 34: Missing docstring for function 'test_apply_kalman_filter_changes_values'
- Line 45: Missing docstring for function 'test_apply_kalman_filter_noop_when_disabled'
- Line 52: Missing docstring for function 'test_remove_outliers_drops_points'
- Line 68: Missing docstring for function 'test_rssi_to_distance'
- Line 73: Missing docstring for function 'test_estimate_ap_location_centroid_weighted'
- Line 87: Missing docstring for function 'test_localize_aps_returns_dict'

### tests/test_kalman.py
- Line 6: Missing docstring for function 'test_kalman_filter_reduces_variance'

### tests/test_export_db_script.py
- Line 16: Missing docstring for function 'test_export_db_script'

### tests/test_fingerprint_persistence.py
- Line 12: Missing docstring for function 'test_save_and_load_fingerprint_info'

### tests/test_service_simple.py
- Line 43: Missing docstring for function 'create_app'

### tests/test_export.py
- Line 10: Missing docstring for function 'test_filter_records'
- Line 38: Missing docstring for function 'test_export_records_formats'
- Line 70: Missing docstring for function 'test_estimate_location_from_rssi'
- Line 83: Missing docstring for function 'test_export_map_kml'
- Line 101: Missing docstring for function 'test_export_map_kml_compute_position'

### tests/test_database_counts.py
- Line 20: Missing docstring for function 'setup_tmp'
- Line 27: Missing docstring for function 'test_get_table_counts'

### tests/test_band_scanner.py
- Line 9: Missing docstring for function 'test_scan_bands_parses_output'
- Line 19: Missing docstring for function 'test_scan_bands_passes_timeout'
- Line 33: Missing docstring for function 'test_async_scan_bands'
- Line 22: Missing docstring for function 'fake_check_output'
- Line 36: Missing docstring for class 'DummyProc'

### tests/test_cpu_pool.py
- Line 11: Missing docstring for function 'test_run_cpu_bound'

### tests/test_analysis_queries_service.py
- Line 53: Missing docstring for function 'test_analysis_endpoints'
- Line 17: Missing docstring for class 'MetricsResult'
- Line 71: Missing docstring for function 'run_tests'

### tests/test_remote_sync.py
- Line 24: Missing docstring for class 'DummyResp'
- Line 35: Missing docstring for class 'DummySession'
- Line 53: Missing docstring for function 'prepare'
- Line 62: Missing docstring for function 'run_sync'
- Line 76: Missing docstring for function 'test_load_sync_state_missing'
- Line 81: Missing docstring for function 'test_save_and_load_sync_state'
- Line 87: Missing docstring for function 'test_sync_database_file_missing'
- Line 93: Missing docstring for function 'test_sync_database_retry'
- Line 99: Missing docstring for function 'test_sync_database_failure'
- Line 139: Missing docstring for function 'test_sync_new_records'
- Line 174: Missing docstring for function 'test_make_range_db'
- Line 224: Missing docstring for function 'test_make_range_db_empty_range'
- Line 272: Missing docstring for function 'test_sync_database_timeout'
- Line 295: Missing docstring for function 'test_sync_database_exponential_backoff'
- Line 323: Missing docstring for function 'test_sync_metrics_success'
- Line 335: Missing docstring for function 'test_sync_metrics_failure'
- Line 46: Missing docstring for function 'post'
- Line 104: Missing docstring for class 'FailSession'
- Line 277: Missing docstring for function 'fake_timeout'
- Line 299: Missing docstring for class 'FailTwiceSession'
- Line 340: Missing docstring for class 'FailSess'
- Line 300: Missing docstring for function 'post'

### tests/test_analysis_queries_cache.py
- Line 10: Missing docstring for class 'CallCounter'
- Line 19: Missing docstring for function 'test_cached_fetch'

### tests/test_lazy_widget_loading.py
- Line 5: Missing docstring for function 'test_lazy_loading'

### tests/test_task_queue.py
- Line 6: Missing docstring for function 'test_background_task_queue_runs_tasks'
- Line 20: Missing docstring for function 'test_run_continuous_scan_with_queue'
- Line 10: Missing docstring for function 'job'

### tests/test_widget_manager.py
- Line 26: Missing docstring for function 'test_lazy_manager_load'
- Line 38: Missing docstring for function 'test_release_widget'
- Line 54: Missing docstring for function 'test_memory_pressure_unloads'
- Line 58: Missing docstring for class 'DummyMonitor'
- Line 63: Missing docstring for function 'sample'

### tests/test_network_analytics.py
- Line 30: Missing docstring for function 'test_open_network_flagged'
- Line 35: Missing docstring for function 'test_duplicate_bssid_multiple_ssids_flagged_second_only'
- Line 42: Missing docstring for function 'test_missing_fields_handled'
- Line 49: Missing docstring for function 'test_open_and_duplicate_combined'
- Line 57: Missing docstring for function 'test_duplicate_bssid_same_ssid_not_flagged'
- Line 64: Missing docstring for function 'test_wep_network_flagged'
- Line 69: Missing docstring for function 'test_unknown_vendor_flagged'
- Line 75: Missing docstring for function 'test_duplicate_bssid_three_ssids_flagged_second_third_only'
- Line 83: Missing docstring for function 'test_open_network_case_insensitive'
- Line 88: Missing docstring for function 'test_duplicate_and_unknown_vendor_flagged'
- Line 96: Missing docstring for function 'test_cluster_by_signal_returns_centroids'
- Line 139: Missing docstring for function 'test_detect_rogue_devices_combines_checks'

### tests/test_tile_maintenance_cli.py
- Line 32: Missing docstring for function 'test_tile_maintenance_cli'

### tests/test_critical_paths.py
- Line 218: Missing docstring for function 'test_func'

### tests/test_cloud_export.py
- Line 9: Missing docstring for function 'test_upload_to_s3_logs_errors'
- Line 12: Missing docstring for class 'DummyClient'
- Line 16: Missing docstring for class 'DummySession'
- Line 20: Missing docstring for function 'client'

### tests/test_scheduler_system.py
- Line 340: Missing docstring for function 'flaky_task'
- Line 372: Missing docstring for function 'long_running_task'
- Line 464: Missing docstring for function 'concurrent_task'
- Line 570: Missing docstring for function 'high_freq_task'
- Line 592: Missing docstring for function 'create_task_func'

### tests/test_mysql_export.py
- Line 7: Missing docstring for class 'DummyCursor'
- Line 24: Missing docstring for class 'DummyConn'
- Line 41: Missing docstring for function 'test_init_schema'
- Line 55: Missing docstring for function 'test_insert_records'

### tests/test_vacuum_script.py
- Line 5: Missing docstring for function 'test_vacuum_script'

### tests/test_health_export.py
- Line 8: Missing docstring for function 'test_export_json'
- Line 20: Missing docstring for function 'test_export_csv'

### tests/test_service_sync.py
- Line 50: Missing docstring for function 'test_sync_endpoint_success'
- Line 72: Missing docstring for function 'test_sync_endpoint_failure'
- Line 23: Missing docstring for class 'MetricsResult'
- Line 57: Missing docstring for function 'fake_upload'

### tests/test_continuous_scan.py
- Line 8: Missing docstring for function 'test_scan_once_returns_data'
- Line 16: Missing docstring for function 'test_run_continuous_scan_iterations'
- Line 45: Missing docstring for function 'test_run_once_writes_json'
- Line 58: Missing docstring for function 'test_main_runs_iterations'

### tests/test_battery_widget.py
- Line 5: Missing docstring for class 'DummyBattery'
- Line 15: Missing docstring for function 'test_widget_updates'

### tests/test_parsers.py
- Line 7: Missing docstring for function 'test_parse_imsi_output'
- Line 30: Missing docstring for function 'test_parse_band_output'

### tests/test_health_stats_script.py
- Line 7: Missing docstring for function 'test_health_stats_script_output'
- Line 10: Missing docstring for function 'fake_load'

### tests/test_migrations_fixed.py
- Line 20: Missing docstring for class 'BaseMigration'
- Line 41: Missing docstring for class 'TestMigration'
- Line 392: Missing docstring for class 'MigrationRunner'

### tests/test_service_async_endpoints.py
- Line 60: Missing docstring for function 'test_widgets_endpoint_async'
- Line 74: Missing docstring for function 'test_logs_endpoint_async'
- Line 91: Missing docstring for function 'test_service_status_endpoint_async'
- Line 30: Missing docstring for class 'MetricsResult'
- Line 66: Missing docstring for function 'call'
- Line 83: Missing docstring for function 'call'
- Line 94: Missing docstring for function 'fake_status'
- Line 101: Missing docstring for function 'call'

### tests/test_status_service.py
- Line 10: Missing docstring for function 'test_get_status_async'

### tests/test_persistence.py
- Line 13: Missing docstring for function 'test_save_and_load_health_record'
- Line 27: Missing docstring for function 'test_save_and_load_app_state'
- Line 36: Missing docstring for function 'test_save_and_load_dashboard_settings'
- Line 48: Missing docstring for function 'test_custom_db_path'
- Line 65: Missing docstring for function 'test_purge_old_health'
- Line 80: Missing docstring for function 'test_vacuum'
- Line 91: Missing docstring for function 'test_conn_closed_on_loop_switch'
- Line 111: Missing docstring for function 'test_schema_version'

### tests/test_priority_queue.py
- Line 9: Missing docstring for function 'test_priority_order'

### tests/test_db_summary_script.py
- Line 6: Missing docstring for function 'test_db_summary_script'

### tests/test_lora_scanner.py
- Line 11: Missing docstring for function 'test_parse_packets'
- Line 23: Missing docstring for function 'test_parse_packets_pandas'
- Line 37: Missing docstring for function 'test_plot_signal_trend'
- Line 62: Missing docstring for function 'test_async_scan_lora'
- Line 75: Missing docstring for function 'test_async_parse_packets'
- Line 84: Missing docstring for function 'test_main'
- Line 63: Missing docstring for function 'fake_exec'
- Line 64: Missing docstring for class 'P'

### tests/test_analysis_extra.py
- Line 25: Missing docstring for function 'test_plot_cpu_temp_matplotlib_backend'
- Line 90: Missing docstring for function 'test_plot_cpu_temp_no_pandas'
- Line 110: Missing docstring for function 'test_plot_cpu_temp_plotly'
- Line 26: Missing docstring for class 'FakeSeries'
- Line 47: Missing docstring for class 'FakeDataFrame'
- Line 111: Missing docstring for class 'FakeSeries'
- Line 132: Missing docstring for class 'FakeDataFrame'
- Line 27: Missing docstring for function 'rolling'
- Line 60: Missing docstring for function 'sort_values'
- Line 112: Missing docstring for function 'rolling'
- Line 145: Missing docstring for function 'sort_values'
- Line 28: Missing docstring for class 'Roll'
- Line 113: Missing docstring for class 'Roll'
- Line 32: Missing docstring for function 'mean'
- Line 117: Missing docstring for function 'mean'

### tests/test_baseline_analysis.py
- Line 8: Missing docstring for function 'test_analyze_health_baseline'
- Line 16: Missing docstring for function 'test_load_baseline_health'

### tests/test_network_fingerprinting_integration.py
- Line 7: Missing docstring for class 'Dummy'
- Line 15: Missing docstring for function 'test_fingerprint_wifi_records'

### tests/test_core_config_extra.py
- Line 9: Missing docstring for function 'test_env_override'
- Line 16: Missing docstring for function 'test_export_import_roundtrip'
- Line 25: Missing docstring for function 'test_export_invalid_extension'
- Line 32: Missing docstring for function 'test_yaml_export_import'
- Line 41: Missing docstring for function 'test_apply_env_overrides_remote_sync_url'
- Line 48: Missing docstring for function 'test_apply_env_overrides_mysql'
- Line 72: Missing docstring for function 'test_list_profiles'
- Line 83: Missing docstring for function 'test_switch_profile'
- Line 134: Missing docstring for function 'test_env_override_webhooks'
- Line 104: Missing docstring for function 'fake_import'
- Line 123: Missing docstring for function 'fake_import'

### tests/test_model_trainer.py
- Line 8: Missing docstring for class 'DummyScheduler'
- Line 24: Missing docstring for function 'test_model_trainer_runs'
- Line 12: Missing docstring for function 'schedule'

### tests/test_di.py
- Line 9: Missing docstring for function 'test_register_instance_and_resolve'
- Line 17: Missing docstring for function 'test_register_factory_and_single_instance'
- Line 28: Missing docstring for function 'test_resolve_missing_key_raises'
- Line 34: Missing docstring for function 'test_concurrent_resolve_creates_single_instance'
- Line 39: Missing docstring for function 'factory'

### tests/test_widget_system.py
- Line 36: Missing docstring for class 'TestWidget'
- Line 51: Missing docstring for class 'TestWidget'
- Line 68: Missing docstring for class 'TestWidget'
- Line 88: Missing docstring for class 'TestWidget1'
- Line 95: Missing docstring for class 'TestWidget2'
- Line 115: Missing docstring for class 'TestWidget'
- Line 134: Missing docstring for class 'TestWidget'
- Line 149: Missing docstring for class 'TestWidget1'
- Line 156: Missing docstring for class 'TestWidget2'
- Line 177: Missing docstring for class 'FailingWidget'
- Line 193: Missing docstring for class 'CountingWidget'
- Line 216: Missing docstring for class 'ConfigurableWidget'
- Line 253: Missing docstring for class 'TestWidget'
- Line 267: Missing docstring for class 'TestWidget'
- Line 281: Missing docstring for class 'TestWidget1'
- Line 288: Missing docstring for class 'TestWidget2'
- Line 374: Missing docstring for class 'DatabaseWidget'
- Line 395: Missing docstring for class 'SchedulerWidget'
- Line 419: Missing docstring for class 'ConfigWidget'
- Line 446: Missing docstring for class 'SlowWidget'
- Line 479: Missing docstring for class 'MemoryWidget'
- Line 503: Missing docstring for class 'ConcurrentWidget'
- Line 518: Missing docstring for function 'access_widget'
- Line 546: Missing docstring for class 'ValidatingWidget'
- Line 582: Missing docstring for class 'SanitizingWidget'
- Line 198: Missing docstring for function 'get_data'
- Line 451: Missing docstring for function 'get_data'
- Line 508: Missing docstring for function 'get_data'
- Line 553: Missing docstring for function 'set_config'

### tests/test_sigint_export_json.py
- Line 6: Missing docstring for function 'test_export_json'

### tests/test_webui_server.py
- Line 17: Missing docstring for function 'test_webui_serves_static_and_api'

### tests/test_export_logs_script.py
- Line 5: Missing docstring for function 'test_export_logs_script'
- Line 8: Missing docstring for function 'fake_export'
- Line 13: Missing docstring for class 'DummyApp'

### tests/test_main_application_fixed.py
- Line 67: Missing docstring for function 'side_effect'

### tests/test_aggregation_service.py
- Line 36: Missing docstring for function 'test_upload_and_stats'
- Line 58: Missing docstring for function 'test_upload_appends'
- Line 76: Missing docstring for function 'test_upload_rejects_traversal'
- Line 89: Missing docstring for function 'test_upload_rejects_nested_traversal'
- Line 102: Missing docstring for function 'test_upload_rejects_evil_db'

### tests/test_web_server_missing.py
- Line 8: Missing docstring for function 'test_create_app_missing_dist'
- Line 17: Missing docstring for function 'fake_join'

### tests/test_analysis.py
- Line 9: Missing docstring for function 'test_compute_health_stats'
- Line 19: Missing docstring for function 'test_plot_cpu_temp_creates_file'
- Line 42: Missing docstring for function 'test_plot_cpu_temp_plotly_backend'

### tests/test_sync_receiver.py
- Line 23: Missing docstring for function 'test_rejects_traversal'
- Line 30: Missing docstring for function 'test_rejects_nested_traversal'
- Line 37: Missing docstring for function 'test_rejects_evil_db'

### tests/test_imports_src.py
- Line 17: Missing docstring for function 'test_import_package_modules'

### tests/test_geometry_utils.py
- Line 11: Missing docstring for function 'test_haversine_distance_known'
- Line 16: Missing docstring for function 'test_polygon_area_triangle'
- Line 27: Missing docstring for function 'test_parse_coord_text'
- Line 32: Missing docstring for function 'test_get_avg_rssi'

### tests/test_sigint_paths.py
- Line 4: Missing docstring for function 'test_export_dir_env_override'

### tests/test_vector_tile_customizer.py
- Line 7: Missing docstring for function 'test_apply_style'
- Line 24: Missing docstring for function 'test_build_mbtiles'

### tests/test_plugins.py
- Line 12: Missing docstring for function 'test_load_hello_plugin'

### tests/test_exception_handler.py
- Line 10: Missing docstring for function 'load_handler'
- Line 17: Missing docstring for class 'DummyLoop'
- Line 25: Missing docstring for function 'test_install_sets_hooks'
- Line 45: Missing docstring for function 'test_install_only_once'

### tests/test_performance_comprehensive.py
- Line 274: Missing docstring for class 'MockHighVolumeScanner'
- Line 305: Missing docstring for class 'MockContinuousScanner'
- Line 725: Missing docstring for function 'collect_memory_sample'
- Line 279: Missing docstring for function 'scan_networks'
- Line 310: Missing docstring for function 'scan_networks'

### tests/test_resource_manager.py
- Line 7: Missing docstring for function 'test_file_and_db_cleanup'
- Line 21: Missing docstring for function 'test_task_cancel'

### tests/test_wigle_integration.py
- Line 6: Missing docstring for class 'FakeResp'
- Line 23: Missing docstring for class 'FakeSession'
- Line 37: Missing docstring for function 'test_fetch_wigle_networks'
- Line 67: Missing docstring for function 'test_fetch_wigle_networks_cache'
- Line 73: Missing docstring for class 'Session'
- Line 74: Missing docstring for function 'get'

### tests/test_cache_security_fixed.py
- Line 50: Missing docstring for function 'run_test'
- Line 63: Missing docstring for function 'run_test'
- Line 76: Missing docstring for function 'run_test'
- Line 90: Missing docstring for function 'run_test'

### tests/test_widget_system_comprehensive.py
- Line 46: Missing docstring for class 'TestWidget'
- Line 253: Missing docstring for class 'MockWidget'
- Line 279: Missing docstring for class 'AsyncWidget'
- Line 294: Missing docstring for function 'test_async_update'
- Line 303: Missing docstring for class 'ErrorWidget'
- Line 366: Missing docstring for class 'TestWidget'
- Line 392: Missing docstring for class 'MockWidgetRegistry'
- Line 407: Missing docstring for class 'MockWidgetRegistry'
- Line 420: Missing docstring for class 'TestWidget'
- Line 481: Missing docstring for class 'TestWidget'
- Line 286: Missing docstring for function 'update_async'

### tests/test_config.py
- Line 16: Missing docstring for function 'setup_temp_config'
- Line 31: Missing docstring for function 'test_load_config_defaults_when_missing'
- Line 47: Missing docstring for function 'test_save_and_load_roundtrip'
- Line 73: Missing docstring for function 'test_save_config_dataclass_roundtrip'
- Line 82: Missing docstring for function 'test_save_config_no_temp_files'
- Line 90: Missing docstring for function 'test_load_config_bad_json'
- Line 97: Missing docstring for function 'test_load_config_schema_violation'
- Line 104: Missing docstring for function 'test_load_config_invalid_json_monkeypatch'
- Line 115: Missing docstring for function 'test_save_config_validation_error'
- Line 122: Missing docstring for function 'test_env_override_integer'
- Line 137: Missing docstring for function 'test_env_override_boolean'
- Line 148: Missing docstring for function 'test_env_override_health_poll'
- Line 155: Missing docstring for function 'test_env_override_route_prefetch'
- Line 164: Missing docstring for function 'test_env_override_battery_widget'
- Line 171: Missing docstring for function 'test_list_env_overrides'
- Line 176: Missing docstring for function 'test_export_import_json'
- Line 185: Missing docstring for function 'test_export_import_yaml'
- Line 195: Missing docstring for function 'test_profile_roundtrip'
- Line 207: Missing docstring for function 'test_import_export_profile'
- Line 218: Missing docstring for function 'test_import_export_delete_profile'
- Line 309: Missing docstring for function 'test_save_load_webhooks'
- Line 319: Missing docstring for function 'test_profile_inheritance'
- Line 280: Missing docstring for function 'fake_import'
- Line 298: Missing docstring for function 'fake_import'

### tests/test_tower_scanner.py
- Line 9: Missing docstring for function 'test_scan_towers'
- Line 24: Missing docstring for function 'test_async_scan_towers'
- Line 27: Missing docstring for class 'DummyProc'

### tests/test_route_prefetch.py
- Line 26: Missing docstring for class 'DummyScheduler'
- Line 38: Missing docstring for class 'DummyMap'
- Line 51: Missing docstring for function 'test_route_prefetcher_runs'
- Line 75: Missing docstring for function 'test_route_prefetcher_no_points'
- Line 99: Missing docstring for function 'test_predict_points'
- Line 124: Missing docstring for function 'test_zero_lookahead'
- Line 30: Missing docstring for function 'schedule'
- Line 44: Missing docstring for function 'prefetch_tiles'

### tests/test_web_server.py
- Line 20: Missing docstring for function 'test_web_server_serves_static_and_api'
- Line 30: Missing docstring for function 'fake_join'
- Line 40: Missing docstring for function 'fake_isdir'

### tests/test_imports.py
- Line 172: Missing docstring for function 'test_import_top_level_modules'
- Line 22: Missing docstring for class '_FastAPI'
- Line 23: Missing docstring for function 'get'
- Line 29: Missing docstring for function 'post'
- Line 35: Missing docstring for function 'put'
- Line 41: Missing docstring for function 'delete'
- Line 47: Missing docstring for function 'websocket'

### tests/test_gpsd_client.py
- Line 26: Missing docstring for function 'test_get_position_none_on_failure'
- Line 31: Missing docstring for function 'test_reconnect_after_error'
- Line 49: Missing docstring for function 'test_env_overrides'
- Line 15: Missing docstring for function 'get_current'
- Line 35: Missing docstring for function 'get_current'

### tests/test_ckml.py
- Line 4: Missing docstring for function 'test_parse_coords_simple'
- Line 9: Missing docstring for function 'test_parse_coords_with_altitude'
- Line 14: Missing docstring for function 'test_parse_coords_negative'
- Line 19: Missing docstring for function 'test_parse_coords_malformed_single_token'
- Line 24: Missing docstring for function 'test_parse_coords_mixed_valid_invalid'

### tests/test_clustering.py
- Line 4: Missing docstring for function 'test_cluster_positions_basic'

### tests/test_extra_widgets.py
- Line 12: Missing docstring for function 'test_orientation_widget'
- Line 24: Missing docstring for function 'test_vehicle_speed_widget'
- Line 33: Missing docstring for function 'test_lora_scan_widget'

### tests/test_gpsd_client_async_more.py
- Line 10: Missing docstring for function 'test_get_position_async'
- Line 20: Missing docstring for function 'test_get_accuracy_async'
- Line 30: Missing docstring for function 'test_get_fix_quality_async'
- Line 40: Missing docstring for function 'test_async_methods_none'

### tests/test_sync.py
- Line 14: Missing docstring for class 'DummyConfig'
- Line 21: Missing docstring for function 'test_upload_data_retries'
- Line 67: Missing docstring for function 'test_upload_data_failure'
- Line 24: Missing docstring for class 'Resp'
- Line 33: Missing docstring for class 'Session'
- Line 68: Missing docstring for class 'Resp'
- Line 77: Missing docstring for class 'Session'
- Line 43: Missing docstring for function 'post'

### tests/test_r_integration.py
- Line 12: Missing docstring for class 'DummyResult'
- Line 18: Missing docstring for function 'test_health_summary_missing_rpy2'
- Line 32: Missing docstring for function 'test_health_summary_no_plot'
- Line 53: Missing docstring for function 'test_health_summary_with_plot'
- Line 21: Missing docstring for function 'fake_import'

### tests/test_bt_scanner.py
- Line 8: Missing docstring for class 'DummyDevice'
- Line 12: Missing docstring for function 'test_scan_bluetooth_bleak'
- Line 28: Missing docstring for function 'test_scan_bluetooth_fallback'
- Line 40: Missing docstring for function 'fake_import'

### tests/test_remote_sync_pkg.py
- Line 22: Missing docstring for class 'DummyResp'
- Line 33: Missing docstring for class 'DummySession'
- Line 51: Missing docstring for function 'prepare'
- Line 60: Missing docstring for function 'run_sync'
- Line 74: Missing docstring for function 'test_sync_database_file_missing'
- Line 80: Missing docstring for function 'test_sync_database_retry'
- Line 86: Missing docstring for function 'test_sync_database_failure'
- Line 124: Missing docstring for function 'test_sync_new_records'
- Line 44: Missing docstring for function 'post'
- Line 91: Missing docstring for class 'FailSession'

### tests/test_scheduler_tasks.py
- Line 259: Missing docstring for function 'counting_task'
- Line 288: Missing docstring for function 'success_task'
- Line 316: Missing docstring for function 'task1'
- Line 320: Missing docstring for function 'task2'
- Line 380: Missing docstring for function 'test_task'
- Line 410: Missing docstring for function 'priority_task'
- Line 441: Missing docstring for function 'success_task'
- Line 649: Missing docstring for function 'cpu_task'
- Line 680: Missing docstring for function 'concurrent_task'
- Line 714: Missing docstring for function 'throughput_task'
- Line 752: Missing docstring for function 'failing_task'
- Line 757: Missing docstring for function 'success_task'
- Line 783: Missing docstring for function 'failing_task'
- Line 788: Missing docstring for function 'success_task'
- Line 816: Missing docstring for function 'sometimes_failing_task'

### tests/test_health_import.py
- Line 13: Missing docstring for function 'test_import_json'
- Line 31: Missing docstring for function 'test_import_csv'

### tests/test_async_scheduler.py
- Line 10: Missing docstring for function 'load_scheduler'
- Line 17: Missing docstring for function 'test_poll_scheduler_accepts_async_widget'
- Line 41: Missing docstring for function 'test_poll_scheduler_handles_async_callback'
- Line 61: Missing docstring for function 'test_async_scheduler_runs_tasks'
- Line 87: Missing docstring for function 'test_async_scheduler_sleep_remaining_time'
- Line 120: Missing docstring for function 'test_async_scheduler_cancel_all_waits'
- Line 151: Missing docstring for function 'test_async_scheduler_cancel_all_gathers_exceptions'
- Line 185: Missing docstring for function 'test_poll_scheduler_metrics'
- Line 205: Missing docstring for function 'test_async_scheduler_metrics'
- Line 232: Missing docstring for function 'test_scheduler_rejects_invalid_interval'
- Line 20: Missing docstring for class 'Widget'
- Line 29: Missing docstring for function 'fake_run_async'
- Line 49: Missing docstring for function 'fake_run_async'
- Line 76: Missing docstring for function 'runner'
- Line 94: Missing docstring for function 'fake_sleep'
- Line 103: Missing docstring for function 'job'
- Line 107: Missing docstring for function 'runner'
- Line 140: Missing docstring for function 'runner'
- Line 171: Missing docstring for function 'runner'
- Line 219: Missing docstring for function 'runner'

### tests/test_analysis_hooks.py
- Line 21: Missing docstring for function 'test_ml_hook_invoked'

### tests/test_orientation_sensors.py
- Line 17: Missing docstring for function 'test_orientation_to_angle'
- Line 23: Missing docstring for function 'test_orientation_to_angle_custom_map'
- Line 28: Missing docstring for function 'test_update_orientation_map'
- Line 36: Missing docstring for function 'test_update_orientation_map_clone'
- Line 44: Missing docstring for function 'test_get_orientation_dbus_missing'
- Line 53: Missing docstring for function 'test_get_orientation_dbus_success'
- Line 86: Missing docstring for function 'test_get_heading'
- Line 92: Missing docstring for function 'test_get_heading_none'
- Line 97: Missing docstring for function 'test_read_mpu6050_missing'
- Line 106: Missing docstring for function 'test_read_mpu6050_success'
- Line 128: Missing docstring for function 'test_read_mpu6050_env'
- Line 152: Missing docstring for function 'test_reset_orientation_map_env'
- Line 166: Missing docstring for function 'test_reset_orientation_map_invalid'
- Line 178: Missing docstring for function 'test_reset_orientation_map_unsafe'
- Line 54: Missing docstring for class 'DummyIface'
- Line 67: Missing docstring for class 'DummyBus'
- Line 107: Missing docstring for class 'DummySensor'
- Line 129: Missing docstring for class 'DummySensor'

### tests/test_service_api_fixed_v2.py
- Line 193: Missing docstring for function 'protected_endpoint'
- Line 209: Missing docstring for function 'auth_middleware'
- Line 225: Missing docstring for function 'process_auth_header'
- Line 377: Missing docstring for function 'get_database_info'
- Line 465: Missing docstring for function 'check_service_health'
- Line 485: Missing docstring for function 'add_security_headers'
- Line 510: Missing docstring for class 'UserInput'
- Line 575: Missing docstring for function 'add_security_headers'
- Line 107: Missing docstring for function 'get_mem_usage'
- Line 119: Missing docstring for function 'get_disk_usage'
- Line 132: Missing docstring for function 'get_network_throughput'
- Line 152: Missing docstring for function 'service_status_async'
- Line 171: Missing docstring for function 'run_service_cmd'

### tests/test_performance.py
- Line 4: Missing docstring for function 'test_record_metrics'

### tests/test_sigint_exports.py
- Line 7: Missing docstring for function 'test_export_csv'
- Line 15: Missing docstring for function 'test_export_yaml'
- Line 25: Missing docstring for function 'test_all_contains_export_yaml'
- Line 31: Missing docstring for function 'test_export_json'

### tests/test_config_validation.py
- Line 9: Missing docstring for function 'setup'
- Line 14: Missing docstring for function 'test_invalid_env_value'

### tests/test_scan_report.py
- Line 11: Missing docstring for function 'test_generate_scan_report'

### tests/test_service.py
- Line 23: Missing docstring for class 'MetricsResult'
- Line 52: Missing docstring for function 'test_status_endpoint_returns_recent_records'
- Line 84: Missing docstring for function 'test_status_auth_missing_credentials'
- Line 97: Missing docstring for function 'test_widget_metrics_endpoint'
- Line 149: Missing docstring for function 'test_logs_endpoint_returns_lines_async'
- Line 163: Missing docstring for function 'test_logs_endpoint_handles_sync_function'
- Line 177: Missing docstring for function 'test_logs_endpoint_allows_whitelisted_path'
- Line 192: Missing docstring for function 'test_logs_endpoint_rejects_unknown_path'
- Line 210: Missing docstring for function 'test_websocket_status_stream'
- Line 263: Missing docstring for function 'test_sse_status_stream'
- Line 319: Missing docstring for function 'test_ws_aps_stream'
- Line 344: Missing docstring for function 'test_sse_aps_stream'
- Line 372: Missing docstring for function 'test_websocket_timeout_closes_connection'
- Line 420: Missing docstring for function 'test_update_config_endpoint_success'
- Line 434: Missing docstring for function 'test_update_config_endpoint_invalid_key'
- Line 442: Missing docstring for function 'test_dashboard_settings_endpoints'
- Line 473: Missing docstring for function 'test_widget_metrics_auth_missing_credentials'
- Line 501: Missing docstring for function 'test_widget_metrics_auth_bad_password'
- Line 548: Missing docstring for function 'test_baseline_analysis_endpoint'
- Line 640: Missing docstring for function 'test_service_control_endpoint_invalid_action'
- Line 668: Missing docstring for function 'test_db_stats_endpoint'
- Line 686: Missing docstring for function 'test_lora_scan_endpoint'
- Line 701: Missing docstring for function 'test_auth_login_valid'
- Line 195: Missing docstring for function 'fake_tail'
- Line 451: Missing docstring for function 'fake_save'
- Line 687: Missing docstring for function 'fake_scan'

### tests/test_anomaly_detector.py
- Line 7: Missing docstring for function 'test_anomaly_warning_triggered'

### tests/test_service_api_fixed.py
- Line 217: Missing docstring for class 'AuthMiddleware'
- Line 238: Missing docstring for class 'MockAuthMiddleware'
- Line 508: Missing docstring for function 'add_security_headers'
- Line 533: Missing docstring for class 'UserInput'
- Line 602: Missing docstring for function 'add_security_headers'
- Line 110: Missing docstring for function 'get_mem_usage'
- Line 123: Missing docstring for function 'get_disk_usage'
- Line 137: Missing docstring for function 'get_network_throughput'
- Line 161: Missing docstring for function 'service_status_async'
- Line 182: Missing docstring for function 'run_service_cmd'
- Line 242: Missing docstring for function 'dispatch'

### tests/test_heatmap.py
- Line 6: Missing docstring for function 'test_histogram_counts'
- Line 19: Missing docstring for function 'test_histogram_points'
- Line 26: Missing docstring for function 'test_density_map_expands_counts'
- Line 36: Missing docstring for function 'test_coverage_map_binary'
- Line 44: Missing docstring for function 'test_histogram_invalid_bins'

### tests/test_circuit_breaker.py
- Line 9: Missing docstring for function 'test_circuit_breaker'

### tests/test_memory_monitor.py
- Line 6: Missing docstring for function 'test_memory_monitor_detects_growth'

### tests/test_localization.py
- Line 149: Missing docstring for function 'mock_open_side_effect'
- Line 184: Missing docstring for function 'mock_open_side_effect'
- Line 323: Missing docstring for function 'mock_open_side_effect'

### tests/test_calibrate_orientation.py
- Line 7: Missing docstring for function 'test_calibrate_orientation'

### tests/test_integration_core.py
- Line 11: Missing docstring for function 'setup_tmp'
- Line 16: Missing docstring for function 'test_health_record_flow'
- Line 26: Missing docstring for function 'test_dashboard_settings_config'
- Line 35: Missing docstring for function 'test_sync_new_records_real_server'
- Line 46: Missing docstring for function 'handler'
- Line 55: Missing docstring for function 'run_test'

### tests/test_tile_maintenance.py
- Line 36: Missing docstring for class 'DummyScheduler'
- Line 50: Missing docstring for function 'test_tile_maintenance_runs'
- Line 42: Missing docstring for function 'schedule'
- Line 61: Missing docstring for class 'DummyConn'

### tests/test_start_kiosk_script.py
- Line 6: Missing docstring for function 'test_start_kiosk_launches_browser'

### tests/test_logging_filters.py
- Line 7: Missing docstring for function 'test_content_filter_include_exclude'
- Line 25: Missing docstring for function 'test_rate_limiter'
- Line 35: Missing docstring for function 'test_sensitive_data_redaction'

### tests/test_health_monitor.py
- Line 19: Missing docstring for class 'DummyScheduler'
- Line 33: Missing docstring for function 'test_health_monitor_polls_self_test'
- Line 56: Missing docstring for function 'test_health_monitor_daily_summary'
- Line 78: Missing docstring for function 'test_health_monitor_exports'
- Line 102: Missing docstring for function 'test_health_monitor_export_cleanup'
- Line 128: Missing docstring for function 'test_health_monitor_upload_to_cloud'
- Line 24: Missing docstring for function 'schedule'
- Line 86: Missing docstring for function 'fake_export'
- Line 138: Missing docstring for class 'DummyCollector'
- Line 145: Missing docstring for function 'fake_export'

### tests/test_api_service.py
- Line 855: Missing docstring for function 'websocket_handler'
- Line 533: Missing docstring for function 'websocket_handler'
- Line 565: Missing docstring for function 'websocket_handler'

### tests/test_security_analyzer_integration.py
- Line 4: Missing docstring for function 'test_detect_hidden_ssids'
- Line 17: Missing docstring for function 'test_detect_evil_twins'

### tests/test_data_sink.py
- Line 12: Missing docstring for function 'test_upload_to_s3'
- Line 21: Missing docstring for function 'test_write_influxdb'
- Line 53: Missing docstring for function 'test_write_postgres'
- Line 24: Missing docstring for class 'Sess'
- Line 56: Missing docstring for class 'Conn'
- Line 68: Missing docstring for function 'fake_connect'
- Line 31: Missing docstring for function 'post'
- Line 34: Missing docstring for class 'Resp'

### tests/conftest.py
- Line 15: Missing docstring for function 'add_dummy_module'

### tests/test_aggregation_service_main.py
- Line 6: Missing docstring for function 'test_main_starts_uvicorn'

### tests/test_service_plugins.py
- Line 8: Missing docstring for function 'test_plugins_endpoint'

### tests/test_gpsd_client_async.py
- Line 6: Missing docstring for class 'DummyReader'
- Line 16: Missing docstring for class 'DummyWriter'
- Line 33: Missing docstring for function 'test_async_methods_return_values'
- Line 67: Missing docstring for function 'test_async_methods_failures'
- Line 10: Missing docstring for function 'readline'
- Line 52: Missing docstring for function 'run'
- Line 75: Missing docstring for function 'run'

### tests/test_wifi_scanner.py
- Line 14: Missing docstring for function 'test_scan_wifi_enriches_vendor'
- Line 47: Missing docstring for function 'test_scan_wifi_no_vendor'
- Line 71: Missing docstring for function 'test_async_scan_wifi'
- Line 86: Missing docstring for function 'dummy_proc'
- Line 87: Missing docstring for class 'P'

### tests/test_forecasting.py
- Line 7: Missing docstring for function 'test_forecast_cpu_temp_deterministic'

### tests/test_vector_tile_customizer_cli.py
- Line 4: Missing docstring for function 'test_vector_tile_customizer_cli_build'
- Line 18: Missing docstring for function 'test_vector_tile_customizer_cli_style'

### tests/test_sigint_integration.py
- Line 7: Missing docstring for function 'test_load_sigint_data'
- Line 20: Missing docstring for function 'test_load_sigint_data_missing'

### tests/test_service_status_script.py
- Line 6: Missing docstring for function 'test_service_status_script_output'

### tests/test_robust_request.py
- Line 6: Missing docstring for function 'test_robust_request_retries'
- Line 37: Missing docstring for function 'test_orientation_widget_update'
- Line 9: Missing docstring for function 'fake_request'

### tests/test_export_log_bundle_script.py
- Line 5: Missing docstring for function 'test_export_log_bundle_script'
- Line 8: Missing docstring for function 'fake_bundle'
- Line 13: Missing docstring for class 'DummyApp'

### tests/test_log_viewer.py
- Line 7: Missing docstring for function 'test_log_viewer_filter_regex'
- Line 15: Missing docstring for function 'test_log_viewer_no_filter'
- Line 23: Missing docstring for function 'test_log_viewer_path_menu'

### web/app.py
- Line 45: Missing docstring for function 'create_app'
- Line 73: Missing docstring for function 'main'
- Line 28: Missing docstring for function 'dispatch'
- Line 53: Missing docstring for function 'ws_updates'

### examples/security_analysis_example.py
- Line 8: Missing docstring for function 'main'

### scripts/watch_service.py
- Line 32: Missing docstring for function 'main'

### scripts/validate_migration.py
- Line 12: Missing docstring for function 'count_rows_sqlite'
- Line 18: Missing docstring for function 'count_rows_pg'
- Line 23: Missing docstring for function 'validate'

### scripts/dependency_audit.py
- Line 439: Missing docstring for function 'main'

### scripts/health_export.py
- Line 51: Missing docstring for function 'main'

### scripts/localize_aps.py
- Line 34: Missing docstring for function 'main'

### scripts/export_grafana.py
- Line 60: Missing docstring for function 'main'

### scripts/migrate_sqlite_to_postgres.py
- Line 12: Missing docstring for function 'copy_table'
- Line 36: Missing docstring for function 'main'

### scripts/export_mysql.py
- Line 28: Missing docstring for function 'main'

### scripts/uav_track_playback.py
- Line 24: Missing docstring for function 'main'

### scripts/validate_config.py
- Line 14: Missing docstring for function 'main'

### scripts/generate_openapi.py
- Line 18: Missing docstring for function 'main'

### scripts/uav_record.py
- Line 22: Missing docstring for function 'main'

### scripts/health_import.py
- Line 69: Missing docstring for function 'main'

### tests/models/test_api_models.py
- Line 431: Missing docstring for class 'SimpleObject'

### tests/logging/test_structured_logger.py
- Line 649: Missing docstring for class 'ComplexObject'

### src/piwardrive/db_browser.py
- Line 12: Missing docstring for class '_DBHandler'
- Line 15: Missing docstring for function 'do_GET'

### src/piwardrive/graphql_api.py
- Line 76: Missing docstring for function 'handle'

### src/piwardrive/performance/async_optimizer.py
- Line 132: Missing docstring for function 'decorator'
- Line 134: Missing docstring for function 'wrapper'
- Line 633: Missing docstring for function 'test_operation'

### src/piwardrive/performance/db_optimizer.py
- Line 458: Missing docstring for function 'main'

### src/piwardrive/ui/user_experience.py
- Line 1231: Missing docstring for function 'index'
- Line 1237: Missing docstring for function 'setup_wizard'
- Line 1250: Missing docstring for function 'complete_setup_step'
- Line 1269: Missing docstring for function 'tutorials'
- Line 1274: Missing docstring for function 'start_tutorial'
- Line 1288: Missing docstring for function 'dashboard'
- Line 1293: Missing docstring for function 'get_widget_data'
- Line 1298: Missing docstring for function 'themes'
- Line 1303: Missing docstring for function 'get_theme_css'

### src/piwardrive/testing/automated_framework.py
- Line 377: Missing docstring for function 'is_prime'
- Line 574: Missing docstring for function 'cpu_stress_worker'

### src/piwardrive/migrations/005_create_cellular_detections.py
- Line 13: Missing docstring for function 'apply'
- Line 62: Missing docstring for function 'rollback'

### src/piwardrive/migrations/004_create_gps_tracks.py
- Line 13: Missing docstring for function 'apply'
- Line 45: Missing docstring for function 'rollback'

### src/piwardrive/migrations/006_create_network_fingerprints.py
- Line 13: Missing docstring for function 'apply'
- Line 43: Missing docstring for function 'rollback'

### src/piwardrive/migrations/001_create_scan_sessions.py
- Line 13: Missing docstring for function 'apply'
- Line 44: Missing docstring for function 'rollback'

### src/piwardrive/migrations/009_create_materialized_views.py
- Line 13: Missing docstring for function 'apply'
- Line 58: Missing docstring for function 'rollback'

### src/piwardrive/migrations/003_create_bluetooth_detections.py
- Line 13: Missing docstring for function 'apply'
- Line 61: Missing docstring for function 'rollback'

### src/piwardrive/migrations/010_performance_indexes.py
- Line 11: Missing docstring for function 'apply'
- Line 37: Missing docstring for function 'rollback'

### src/piwardrive/migrations/008_create_network_analytics.py
- Line 11: Missing docstring for function 'apply'
- Line 45: Missing docstring for function 'rollback'

### src/piwardrive/migrations/007_create_suspicious_activities.py
- Line 11: Missing docstring for function 'apply'
- Line 45: Missing docstring for function 'rollback'

### src/piwardrive/migrations/002_enhance_wifi_detections.py
- Line 13: Missing docstring for function 'apply'
- Line 181: Missing docstring for function 'rollback'

### src/piwardrive/core/utils.py
- Line 73: Missing docstring for class '_GPSDEntry'
- Line 94: Missing docstring for class '_NetIOEntry'
- Line 111: Missing docstring for class '_MemUsageEntry'
- Line 121: Missing docstring for class '_DiskUsageEntry'
- Line 191: Missing docstring for class '_DummySession'
- Line 213: Missing docstring for function 'decorator'
- Line 218: Missing docstring for function 'wrapper'

### src/piwardrive/core/persistence.py
- Line 299: Missing docstring for class '_ConnCtx'

### src/piwardrive/web/webui_server.py
- Line 33: Missing docstring for function 'main'

### src/piwardrive/direction_finding/algorithms.py
- Line 331: Missing docstring for function 'objective'

### src/piwardrive/integration/system_orchestration.py
- Line 154: Missing docstring for function 'before_request'
- Line 159: Missing docstring for function 'after_request'

### src/piwardrive/db/mysql.py
- Line 62: Missing docstring for function 'execute'
- Line 68: Missing docstring for function 'executemany'
- Line 74: Missing docstring for function 'fetchall'
- Line 83: Missing docstring for function 'transaction'

### src/piwardrive/db/manager.py
- Line 56: Missing docstring for function 'execute'
- Line 63: Missing docstring for function 'executemany'
- Line 70: Missing docstring for function 'fetchall'

### src/piwardrive/db/postgres.py
- Line 33: Missing docstring for function 'connect'
- Line 49: Missing docstring for function 'close'
- Line 84: Missing docstring for function 'execute'
- Line 89: Missing docstring for function 'executemany'
- Line 94: Missing docstring for function 'fetchall'
- Line 101: Missing docstring for function 'transaction'

### src/piwardrive/db/sqlite.py
- Line 47: Missing docstring for function 'connect'
- Line 64: Missing docstring for function 'close'
- Line 96: Missing docstring for function 'execute'
- Line 102: Missing docstring for function 'executemany'
- Line 108: Missing docstring for function 'fetchall'
- Line 115: Missing docstring for function 'transaction'

### src/piwardrive/geospatial/intelligence.py
- Line 154: Missing docstring for function 'objective'

### src/piwardrive/jobs/maintenance_jobs.py
- Line 59: Missing docstring for function 'enqueue'

### src/piwardrive/jobs/analytics_jobs.py
- Line 51: Missing docstring for function 'enqueue'

### src/piwardrive/routes/websocket.py
- Line 18: Missing docstring for function 'ws_detections'
- Line 36: Missing docstring for function 'sse_detections'

### src/piwardrive/protocols/multi_protocol.py
- Line 1094: Missing docstring for function 'device_discovered'

### src/piwardrive/api/common.py
- Line 38: Missing docstring for function 'error_json'

### src/piwardrive/data_processing/enhanced_processing.py
- Line 719: Missing docstring for function 'strong_signal_filter'
- Line 142: Missing docstring for function 'simple_rule'
- Line 179: Missing docstring for function 'composite_rule'
- Line 196: Missing docstring for function 'geospatial_rule'

### src/piwardrive/logging/storage.py
- Line 26: Missing docstring for function 'upload'
- Line 42: Missing docstring for function 'upload'
- Line 104: Missing docstring for function 'archive_log'
- Line 174: Missing docstring for function 'cleanup_expired_logs'

### src/piwardrive/logging/structured_logger.py
- Line 230: Missing docstring for function 'dataclass_replace'

### src/piwardrive/logging/scheduler.py
- Line 21: Missing docstring for function 'schedule_rotation_check'
- Line 36: Missing docstring for function 'start'
- Line 40: Missing docstring for function 'stop'

### src/piwardrive/integrations/sigint_suite/scan_all.py
- Line 16: Missing docstring for function 'run_once'
- Line 30: Missing docstring for function 'main'

### src/piwardrive/integrations/sigint_suite/enrichment/oui.py
- Line 30: Missing docstring for function 'robust_request'
- Line 55: Missing docstring for class '_DummySession'

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 51: Missing docstring for function 'finalize'

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 16: Missing docstring for function 'normalise'

### src/piwardrive/integrations/sigint_suite/scripts/continuous_scan.py
- Line 21: Missing docstring for function 'main'

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 82: Missing docstring for function 'main'

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 121: Missing docstring for function 'main'

### src/piwardrive/sigint_suite/cellular/tower_tracker/tracker.py
- Line 9: Missing docstring for class 'TowerTracker'

### src/piwardrive/api/websockets/handlers.py
- Line 20: Missing docstring for function 'ws_aps'
- Line 58: Missing docstring for function 'sse_aps'
- Line 95: Missing docstring for function 'ws_status'
- Line 123: Missing docstring for function 'sse_status'

### src/piwardrive/api/health/endpoints.py
- Line 25: Missing docstring for function 'get_status'
- Line 35: Missing docstring for function 'baseline_analysis_endpoint'
- Line 51: Missing docstring for function 'sync_records'
- Line 62: Missing docstring for function 'sse_history'

### src/piwardrive/api/health/models.py
- Line 6: Missing docstring for class 'TokenResponse'
- Line 11: Missing docstring for class 'AuthLoginResponse'
- Line 15: Missing docstring for class 'LogoutResponse'
- Line 19: Missing docstring for class 'HealthRecordDict'
- Line 27: Missing docstring for class 'BaselineAnalysisResult'
- Line 34: Missing docstring for class 'SyncResponse'

### src/piwardrive/api/auth/middleware.py
- Line 17: Missing docstring for function 'dispatch'

### src/piwardrive/api/analytics/endpoints.py
- Line 55: Missing docstring for function 'get_lifecycle_forecast'
- Line 66: Missing docstring for function 'get_capacity_forecast'
- Line 76: Missing docstring for function 'get_predictive_summary'

### src/piwardrive/api/system/endpoints.py
- Line 52: Missing docstring for function 'get_orientation_endpoint'
- Line 89: Missing docstring for function 'get_gps_endpoint'
- Line 123: Missing docstring for function 'get_logs'
- Line 140: Missing docstring for function 'get_db_stats_endpoint'
- Line 152: Missing docstring for function 'db_health_endpoint'
- Line 169: Missing docstring for function 'lora_scan_endpoint'
- Line 177: Missing docstring for function 'control_service_endpoint'
- Line 191: Missing docstring for function 'get_service_status_endpoint'
- Line 204: Missing docstring for function 'update_config_endpoint'
- Line 224: Missing docstring for function 'get_webhooks_endpoint'
- Line 232: Missing docstring for function 'update_webhooks_endpoint'
- Line 242: Missing docstring for function 'list_fingerprints_endpoint'
- Line 250: Missing docstring for function 'add_fingerprint_endpoint'
- Line 270: Missing docstring for function 'add_geofence_endpoint'
- Line 287: Missing docstring for function 'update_geofence_endpoint'
- Line 307: Missing docstring for function 'remove_geofence_endpoint'
- Line 325: Missing docstring for function 'export_access_points'
- Line 341: Missing docstring for function 'export_bluetooth'

### src/piwardrive/api/widgets/__init__.py
- Line 15: Missing docstring for class 'WidgetsListResponse'
- Line 19: Missing docstring for class 'WidgetMetrics'
- Line 25: Missing docstring for class 'DashboardSettingsResponse'
- Line 39: Missing docstring for function 'list_widgets'
- Line 50: Missing docstring for function 'get_plugins'
- Line 57: Missing docstring for function 'get_dashboard_settings_endpoint'
- Line 65: Missing docstring for function 'update_dashboard_settings_endpoint'

## Complexity Issues

### comprehensive_qa_fix.py
- Line 68: High complexity in function 'fix_unused_imports' (score: 16)
- Line 184: High complexity in function 'fix_long_lines' (score: 16)
- Line 242: High complexity in function 'main' (score: 11)

### fix_remaining_syntax.py
- Line 77: High complexity in function 'fix_unexpected_indentation' (score: 14)

### fix_issues.py
- Line 10: High complexity in function 'fix_unused_imports' (score: 12)
- Line 111: High complexity in function 'fix_unterminated_fstrings' (score: 18)

### fix_undefined.py
- Line 9: High complexity in function 'fix_undefined_variables' (score: 14)

### fix_syntax_errors.py
- Line 45: High complexity in function 'fix_unexpected_indents' (score: 11)

### comprehensive_fix.py
- Line 21: High complexity in function 'fix_line_too_long' (score: 14)
- Line 70: High complexity in function 'fix_undefined_variables' (score: 39)

### tests/test_imports.py
- Line 15: Long function '_setup_dummy_modules' (100 statements)

### scripts/dependency_audit.py
- Line 379: High complexity in function 'run_enhanced_security_scan' (score: 11)
- Line 439: High complexity in function 'main' (score: 20)

### scripts/mobile_diagnostics.py
- Line 404: High complexity in function 'main' (score: 13)
- Line 204: High complexity in function '_generate_mobile_recommendations' (score: 11)

### scripts/compare_performance.py
- Line 272: High complexity in function '_compare_performance_metrics' (score: 12)

### scripts/check_locales_sync.py
- Line 10: High complexity in function 'main' (score: 11)

### src/piwardrive/widget_manager.py
- Line 97: High complexity in function '_discover_plugins' (score: 12)

### src/piwardrive/network_analytics.py
- Line 15: High complexity in function 'find_suspicious_aps' (score: 14)

### src/piwardrive/export.py
- Line 36: High complexity in function 'filter_records' (score: 14)
- Line 260: High complexity in function 'export_map_kml' (score: 13)
- Line 47: High complexity in function '_matches' (score: 14)

### src/piwardrive/main.py
- Line 41: High complexity in function '__init__' (score: 15)

### src/piwardrive/unified_platform.py
- Line 342: High complexity in function '_setup_apis' (score: 11)

### src/piwardrive/performance/optimization.py
- Line 956: Long function 'demo_performance_optimization' (87 statements)

### src/piwardrive/core/utils.py
- Line 208: High complexity in function 'async_ttl_cache' (score: 12)
- Line 411: High complexity in function 'safe_request' (score: 11)
- Line 611: High complexity in function 'tail_file' (score: 11)
- Line 729: High complexity in function '_run_service_cmd_async' (score: 11)
- Line 896: High complexity in function 'fetch_kismet_devices_async' (score: 11)
- Line 213: High complexity in function 'decorator' (score: 12)
- Line 218: High complexity in function 'wrapper' (score: 12)

### src/piwardrive/direction_finding/hardware.py
- Line 50: High complexity in function '_parse_iwconfig_output' (score: 16)

### src/piwardrive/map/tile_maintenance.py
- Line 70: High complexity in function 'enforce_cache_limit' (score: 14)

### src/piwardrive/ml/threat_detection.py
- Line 386: High complexity in function 'create_baseline_profile' (score: 14)

### src/piwardrive/hardware/enhanced_hardware.py
- Line 267: High complexity in function '_get_supported_bands' (score: 13)

### src/piwardrive/navigation/offline_navigation.py
- Line 595: High complexity in function 'update_position' (score: 14)
- Line 702: High complexity in function 'navigate_to_waypoint' (score: 11)

### src/piwardrive/plugins/plugin_architecture.py
- Line 204: High complexity in function 'validate_plugin' (score: 11)

### src/piwardrive/api/performance_dashboard.py
- Line 318: High complexity in function 'get_performance_recommendations' (score: 11)

### src/piwardrive/visualization/advanced_visualization.py
- Line 968: Long function 'demo_advanced_visualization' (52 statements)

### src/piwardrive/widgets/__init__.py
- Line 161: High complexity in function '_load_plugins' (score: 16)

### src/piwardrive/data_processing/enhanced_processing.py
- Line 133: High complexity in function 'compile_rule' (score: 20)
- Line 142: High complexity in function 'simple_rule' (score: 11)

### src/piwardrive/integrations/sigint_suite/plugins.py
- Line 28: High complexity in function '_load_plugins' (score: 12)

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 46: High complexity in function '_parse_iwlist_output' (score: 16)

## Security Issues

### comprehensive_code_analyzer.py
- Line 158: Use of eval() is dangerous
- Line 159: Use of exec() is dangerous
- Line 162: Use of os.system() is dangerous
- Line 163: Use of input() can be dangerous in some contexts

### tests/test_security_system.py
- Line 223: Use of input() can be dangerous in some contexts
- Line 236: Use of input() can be dangerous in some contexts
- Line 248: Use of input() can be dangerous in some contexts
- Line 260: Use of input() can be dangerous in some contexts
- Line 273: Use of input() can be dangerous in some contexts
- Line 279: Use of input() can be dangerous in some contexts
- Line 283: Use of input() can be dangerous in some contexts
- Line 469: Use of input() can be dangerous in some contexts

### tests/test_direction_finding.py
- Line 74: Use of eval() is dangerous

### tests/test_tower_tracking.py
- Line 54: Use of eval() is dangerous

### tests/test_critical_paths.py
- Line 334: Use of input() can be dangerous in some contexts
- Line 337: Use of input() can be dangerous in some contexts
- Line 460: Dynamic import with __import__ can be dangerous

### tests/test_cache_security_comprehensive.py
- Line 259: Use of input() can be dangerous in some contexts
- Line 266: Use of input() can be dangerous in some contexts
- Line 274: Use of input() can be dangerous in some contexts
- Line 406: Use of input() can be dangerous in some contexts

### tests/test_fastjson.py
- Line 56: Use of input() can be dangerous in some contexts

### tests/test_lora_scanner.py
- Line 63: Use of exec() is dangerous

### tests/test_main_application_fixed.py
- Line 72: Dynamic import with __import__ can be dangerous

### tests/test_jwt_utils_comprehensive.py
- Line 429: Use of input() can be dangerous in some contexts

### tests/test_scheduler_tasks.py
- Line 485: Use of eval() is dangerous

### tests/test_service_api_fixed_v2.py
- Line 153: Use of exec() is dangerous
- Line 173: subprocess with shell=True is dangerous

### tests/test_service_api_fixed.py
- Line 162: Use of exec() is dangerous
- Line 549: Use of input() can be dangerous in some contexts

### server/parse_widgets.py
- Line 21: Use of eval() is dangerous

### scripts/calibrate_orientation.py
- Line 16: Use of input() can be dangerous in some contexts

### src/piwardrive/lora_scanner.py
- Line 118: Use of exec() is dangerous

### src/piwardrive/main.py
- Line 140: Use of exec() is dangerous

### src/piwardrive/core/utils.py
- Line 238: Pickle deserialization can be dangerous

### src/piwardrive/direction_finding/hardware.py
- Line 580: Use of exec() is dangerous
- Line 634: Use of exec() is dangerous

### src/piwardrive/ml/threat_detection.py
- Line 1115: Pickle deserialization can be dangerous

### src/piwardrive/plugins/plugin_architecture.py
- Line 278: Use of exec() is dangerous

### src/piwardrive/visualization/advanced_visualization.py
- Line 398: Use of exec() is dangerous

### src/piwardrive/integrations/sigint_suite/bluetooth/scanner.py
- Line 54: Use of exec() is dangerous
- Line 157: Use of exec() is dangerous

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 166: Use of exec() is dangerous

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 68: Use of exec() is dangerous

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 89: Use of exec() is dangerous

### src/piwardrive/integrations/sigint_suite/cellular/tower_scanner/scanner.py
- Line 35: Use of exec() is dangerous

## Performance Issues

### comprehensive_code_analyzer.py
- Line 183: for i in range(len(...)) - consider enumerate()

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 18: for i in range(len(...)) - consider enumerate()

### tests/test_analysis_extra.py
- Line 34: for i in range(len(...)) - consider enumerate()
- Line 119: for i in range(len(...)) - consider enumerate()

### src/piwardrive/analysis.py
- Line 65: for i in range(len(...)) - consider enumerate()

### src/piwardrive/network_analytics.py
- Line 93: for i in range(len(...)) - consider enumerate()

### src/piwardrive/navigation/offline_navigation.py
- Line 121: for i in range(len(...)) - consider enumerate()

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 796: for i in range(len(...)) - consider enumerate()

### src/piwardrive/visualization/advanced_visualization.py
- Line 166: for i in range(len(...)) - consider enumerate()

### src/piwardrive/widgets/log_viewer.py
- Line 74: for i in range(len(...)) - consider enumerate()

### src/piwardrive/mining/advanced_data_mining.py
- Line 188: for i in range(len(...)) - consider enumerate()
- Line 311: for i in range(len(...)) - consider enumerate()

## Maintainability Issues

### comprehensive_qa_fix.py
- Line 22: Magic number found - consider using constants
- Line 159: TODO/FIXME comment found

### comprehensive_code_analyzer.py
- Line 144: Line too long (127 > 120 characters)
- Line 202: Magic number found - consider using constants
- Line 203: Magic number found - consider using constants
- Line 205: TODO/FIXME comment found
- Line 206: TODO/FIXME comment found

### main.py
- Line 54: Magic number found - consider using constants
- Line 55: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants
- Line 79: Magic number found - consider using constants
- Line 119: Magic number found - consider using constants
- Line 120: Magic number found - consider using constants
- Line 129: Magic number found - consider using constants
- Line 133: Magic number found - consider using constants
- Line 149: Magic number found - consider using constants
- Line 150: Magic number found - consider using constants

### fix_syntax_errors.py
- Line 94: Line too long (129 > 120 characters)
- Line 95: Line too long (125 > 120 characters)

### tools/setup_performance_dashboard.py
- Line 145: Magic number found - consider using constants
- Line 155: Magic number found - consider using constants
- Line 156: Magic number found - consider using constants
- Line 165: Magic number found - consider using constants
- Line 169: Magic number found - consider using constants

### tools/sync_receiver.py
- Line 18: Magic number found - consider using constants
- Line 23: Magic number found - consider using constants
- Line 36: Magic number found - consider using constants

### tests/test_load_kismet_data.py
- Line 23: Magic number found - consider using constants
- Line 24: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants

### tests/test_integration_comprehensive.py
- Line 62: Magic number found - consider using constants
- Line 225: Magic number found - consider using constants
- Line 232: Magic number found - consider using constants
- Line 262: Magic number found - consider using constants
- Line 263: Magic number found - consider using constants
- Line 266: Magic number found - consider using constants
- Line 267: Magic number found - consider using constants
- Line 286: Magic number found - consider using constants
- Line 326: Magic number found - consider using constants
- Line 447: Magic number found - consider using constants
- Line 480: Magic number found - consider using constants
- Line 483: Magic number found - consider using constants
- Line 485: Magic number found - consider using constants
- Line 494: Magic number found - consider using constants
- Line 536: Magic number found - consider using constants
- Line 537: Magic number found - consider using constants
- Line 554: Magic number found - consider using constants
- Line 555: Magic number found - consider using constants
- Line 564: Magic number found - consider using constants
- Line 566: Magic number found - consider using constants

### tests/test_rf_utils.py
- Line 84: Magic number found - consider using constants

### tests/test_webui_server_main.py
- Line 28: Magic number found - consider using constants
- Line 30: Magic number found - consider using constants

### tests/test_interfaces.py
- Line 75: Magic number found - consider using constants
- Line 79: Magic number found - consider using constants
- Line 112: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants
- Line 388: Magic number found - consider using constants
- Line 398: Magic number found - consider using constants

### tests/test_orientation_sensors_pkg.py
- Line 10: Magic number found - consider using constants
- Line 93: Magic number found - consider using constants
- Line 96: Magic number found - consider using constants

### tests/test_db_stats_widget.py
- Line 16: Magic number found - consider using constants

### tests/test_core_application.py
- Line 162: Magic number found - consider using constants
- Line 173: Magic number found - consider using constants
- Line 199: Magic number found - consider using constants
- Line 211: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants

### tests/test_security_system.py
- Line 63: Magic number found - consider using constants
- Line 136: Magic number found - consider using constants
- Line 141: Magic number found - consider using constants
- Line 217: Magic number found - consider using constants
- Line 278: Magic number found - consider using constants
- Line 279: Magic number found - consider using constants
- Line 283: Magic number found - consider using constants
- Line 389: Magic number found - consider using constants
- Line 392: Magic number found - consider using constants
- Line 395: Magic number found - consider using constants
- Line 404: Magic number found - consider using constants
- Line 412: Magic number found - consider using constants
- Line 418: Magic number found - consider using constants
- Line 426: Magic number found - consider using constants
- Line 433: Magic number found - consider using constants
- Line 435: Magic number found - consider using constants
- Line 511: Magic number found - consider using constants
- Line 547: Magic number found - consider using constants

### tests/test_sigint_scanners_basic.py
- Line 13: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants

### tests/test_imsi_catcher.py
- Line 12: Magic number found - consider using constants
- Line 21: Magic number found - consider using constants
- Line 22: Magic number found - consider using constants
- Line 23: Magic number found - consider using constants
- Line 29: Magic number found - consider using constants
- Line 30: Magic number found - consider using constants
- Line 31: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants

### tests/test_main_simple.py
- Line 105: Line too long (121 > 120 characters)

### tests/test_direction_finding.py
- Line 117: Magic number found - consider using constants
- Line 125: Magic number found - consider using constants
- Line 162: Magic number found - consider using constants
- Line 197: Magic number found - consider using constants
- Line 273: Magic number found - consider using constants
- Line 274: Magic number found - consider using constants
- Line 293: Magic number found - consider using constants
- Line 294: Magic number found - consider using constants
- Line 295: Magic number found - consider using constants
- Line 324: Magic number found - consider using constants
- Line 573: Magic number found - consider using constants
- Line 579: Magic number found - consider using constants
- Line 585: Magic number found - consider using constants
- Line 591: Magic number found - consider using constants

### tests/test_utils.py
- Line 95: Magic number found - consider using constants
- Line 99: Magic number found - consider using constants
- Line 316: Magic number found - consider using constants
- Line 374: Magic number found - consider using constants
- Line 403: Magic number found - consider using constants
- Line 475: Magic number found - consider using constants
- Line 513: Magic number found - consider using constants
- Line 539: Magic number found - consider using constants
- Line 555: Magic number found - consider using constants
- Line 566: Magic number found - consider using constants
- Line 699: Magic number found - consider using constants
- Line 700: Magic number found - consider using constants
- Line 719: Magic number found - consider using constants
- Line 747: Magic number found - consider using constants
- Line 760: Magic number found - consider using constants
- Line 761: Magic number found - consider using constants
- Line 774: Magic number found - consider using constants
- Line 776: Magic number found - consider using constants
- Line 780: Magic number found - consider using constants
- Line 781: Magic number found - consider using constants
- Line 782: Magic number found - consider using constants
- Line 789: Magic number found - consider using constants
- Line 795: Magic number found - consider using constants
- Line 865: Magic number found - consider using constants

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 71: Magic number found - consider using constants

### tests/test_hooks.py
- Line 9: Magic number found - consider using constants

### tests/test_tower_tracking.py
- Line 28: Magic number found - consider using constants
- Line 42: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants

### tests/test_jwt_utils_fixed.py
- Line 64: Magic number found - consider using constants
- Line 68: Magic number found - consider using constants
- Line 71: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants
- Line 82: Magic number found - consider using constants
- Line 85: Magic number found - consider using constants
- Line 109: Magic number found - consider using constants
- Line 122: Magic number found - consider using constants
- Line 154: Magic number found - consider using constants
- Line 188: Magic number found - consider using constants
- Line 201: Magic number found - consider using constants
- Line 220: Magic number found - consider using constants
- Line 247: Magic number found - consider using constants
- Line 248: Magic number found - consider using constants
- Line 260: Magic number found - consider using constants
- Line 261: Magic number found - consider using constants
- Line 287: Magic number found - consider using constants
- Line 336: Magic number found - consider using constants
- Line 352: Magic number found - consider using constants
- Line 413: Magic number found - consider using constants
- Line 441: Magic number found - consider using constants
- Line 452: Magic number found - consider using constants
- Line 454: Magic number found - consider using constants
- Line 457: Magic number found - consider using constants

### tests/test_core_config.py
- Line 135: Magic number found - consider using constants
- Line 149: Magic number found - consider using constants
- Line 205: Magic number found - consider using constants
- Line 254: Magic number found - consider using constants
- Line 398: Magic number found - consider using constants
- Line 404: Magic number found - consider using constants
- Line 505: Magic number found - consider using constants
- Line 518: Magic number found - consider using constants
- Line 542: Magic number found - consider using constants
- Line 543: Magic number found - consider using constants
- Line 549: Magic number found - consider using constants
- Line 550: Magic number found - consider using constants

### tests/test_service_direct_import.py
- Line 75: Magic number found - consider using constants

### tests/test_advanced_localization.py
- Line 24: Magic number found - consider using constants

### tests/test_service_simple.py
- Line 67: Magic number found - consider using constants
- Line 75: Magic number found - consider using constants
- Line 76: Magic number found - consider using constants
- Line 177: Magic number found - consider using constants

### tests/test_export.py
- Line 114: Magic number found - consider using constants

### tests/test_band_scanner.py
- Line 10: Magic number found - consider using constants
- Line 15: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants
- Line 52: Magic number found - consider using constants

### tests/test_analysis_queries_service.py
- Line 81: Magic number found - consider using constants

### tests/test_widget_manager.py
- Line 65: Magic number found - consider using constants

### tests/test_critical_paths.py
- Line 63: Magic number found - consider using constants
- Line 64: Magic number found - consider using constants
- Line 65: Magic number found - consider using constants
- Line 372: Magic number found - consider using constants
- Line 373: Magic number found - consider using constants
- Line 374: Magic number found - consider using constants

### tests/test_cache_security_comprehensive.py
- Line 42: Magic number found - consider using constants
- Line 54: Magic number found - consider using constants
- Line 166: Magic number found - consider using constants
- Line 167: Magic number found - consider using constants
- Line 306: Magic number found - consider using constants

### tests/test_persistence_comprehensive.py
- Line 36: Magic number found - consider using constants
- Line 42: Magic number found - consider using constants
- Line 62: Magic number found - consider using constants
- Line 63: Magic number found - consider using constants
- Line 70: Magic number found - consider using constants
- Line 71: Magic number found - consider using constants
- Line 113: Magic number found - consider using constants
- Line 180: Magic number found - consider using constants
- Line 185: Magic number found - consider using constants
- Line 262: Magic number found - consider using constants
- Line 304: Magic number found - consider using constants
- Line 321: Magic number found - consider using constants
- Line 322: Magic number found - consider using constants
- Line 327: Magic number found - consider using constants
- Line 333: Magic number found - consider using constants
- Line 353: Magic number found - consider using constants
- Line 473: Magic number found - consider using constants
- Line 478: Magic number found - consider using constants

### tests/test_scheduler_system.py
- Line 638: Magic number found - consider using constants

### tests/test_service_sync.py
- Line 68: Magic number found - consider using constants
- Line 88: Magic number found - consider using constants

### tests/test_parsers.py
- Line 8: Magic number found - consider using constants
- Line 12: Magic number found - consider using constants
- Line 13: Magic number found - consider using constants
- Line 14: Magic number found - consider using constants
- Line 20: Magic number found - consider using constants
- Line 21: Magic number found - consider using constants
- Line 22: Magic number found - consider using constants
- Line 31: Magic number found - consider using constants
- Line 35: Magic number found - consider using constants

### tests/test_migrations_fixed.py
- Line 167: Magic number found - consider using constants
- Line 172: Magic number found - consider using constants
- Line 177: Magic number found - consider using constants
- Line 178: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 292: Magic number found - consider using constants
- Line 297: Magic number found - consider using constants
- Line 302: Magic number found - consider using constants
- Line 367: Magic number found - consider using constants

### tests/test_service_async_endpoints.py
- Line 68: Magic number found - consider using constants
- Line 85: Magic number found - consider using constants
- Line 103: Magic number found - consider using constants

### tests/test_status_service.py
- Line 35: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants

### tests/test_core_persistence.py
- Line 134: Magic number found - consider using constants
- Line 136: Magic number found - consider using constants
- Line 137: Magic number found - consider using constants
- Line 145: Magic number found - consider using constants
- Line 146: Magic number found - consider using constants
- Line 160: Magic number found - consider using constants
- Line 188: Magic number found - consider using constants
- Line 215: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 280: Magic number found - consider using constants
- Line 287: Magic number found - consider using constants
- Line 319: Magic number found - consider using constants
- Line 331: Magic number found - consider using constants
- Line 357: Magic number found - consider using constants
- Line 365: Magic number found - consider using constants
- Line 375: Magic number found - consider using constants
- Line 434: Magic number found - consider using constants
- Line 470: Magic number found - consider using constants
- Line 486: Magic number found - consider using constants
- Line 515: Magic number found - consider using constants
- Line 518: Magic number found - consider using constants
- Line 577: Magic number found - consider using constants
- Line 581: Magic number found - consider using constants
- Line 608: Magic number found - consider using constants
- Line 690: Magic number found - consider using constants

### tests/test_fastjson.py
- Line 224: Magic number found - consider using constants

### tests/test_lora_scanner.py
- Line 13: Magic number found - consider using constants
- Line 14: Magic number found - consider using constants
- Line 25: Magic number found - consider using constants
- Line 26: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants
- Line 77: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants

### tests/test_analysis_extra.py
- Line 85: Magic number found - consider using constants
- Line 105: Magic number found - consider using constants
- Line 172: Magic number found - consider using constants

### tests/test_main_application_comprehensive.py
- Line 493: Magic number found - consider using constants
- Line 507: Magic number found - consider using constants

### tests/test_model_trainer.py
- Line 20: Magic number found - consider using constants

### tests/test_widget_system.py
- Line 482: Magic number found - consider using constants

### tests/test_webui_server.py
- Line 30: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants
- Line 61: Magic number found - consider using constants
- Line 64: Magic number found - consider using constants
- Line 67: Magic number found - consider using constants

### tests/test_export_logs_script.py
- Line 8: Magic number found - consider using constants

### tests/test_aggregation_service.py
- Line 46: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants
- Line 86: Magic number found - consider using constants
- Line 99: Magic number found - consider using constants
- Line 112: Magic number found - consider using constants

### tests/test_service_api.py
- Line 50: Magic number found - consider using constants
- Line 57: Magic number found - consider using constants
- Line 100: Magic number found - consider using constants
- Line 115: Magic number found - consider using constants
- Line 148: Magic number found - consider using constants
- Line 149: Magic number found - consider using constants
- Line 206: Magic number found - consider using constants
- Line 211: Magic number found - consider using constants
- Line 230: Magic number found - consider using constants
- Line 277: Magic number found - consider using constants
- Line 285: Magic number found - consider using constants
- Line 286: Magic number found - consider using constants
- Line 301: Magic number found - consider using constants
- Line 308: Magic number found - consider using constants
- Line 339: Magic number found - consider using constants
- Line 386: Magic number found - consider using constants

### tests/test_unit_enhanced.py
- Line 114: Magic number found - consider using constants
- Line 115: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants
- Line 159: Magic number found - consider using constants
- Line 160: Magic number found - consider using constants
- Line 291: Magic number found - consider using constants
- Line 325: Magic number found - consider using constants
- Line 392: Magic number found - consider using constants
- Line 428: Magic number found - consider using constants
- Line 453: Magic number found - consider using constants
- Line 454: Magic number found - consider using constants
- Line 455: Magic number found - consider using constants
- Line 456: Magic number found - consider using constants
- Line 457: Magic number found - consider using constants
- Line 522: Magic number found - consider using constants
- Line 620: Magic number found - consider using constants
- Line 627: Magic number found - consider using constants
- Line 634: Magic number found - consider using constants
- Line 690: Magic number found - consider using constants
- Line 712: Magic number found - consider using constants
- Line 721: Magic number found - consider using constants
- Line 722: Magic number found - consider using constants
- Line 723: Magic number found - consider using constants
- Line 736: Magic number found - consider using constants
- Line 744: Magic number found - consider using constants
- Line 756: Magic number found - consider using constants
- Line 872: Magic number found - consider using constants
- Line 873: Magic number found - consider using constants
- Line 874: Magic number found - consider using constants
- Line 875: Magic number found - consider using constants
- Line 884: Magic number found - consider using constants
- Line 894: Magic number found - consider using constants
- Line 895: Magic number found - consider using constants
- Line 899: Magic number found - consider using constants
- Line 916: Magic number found - consider using constants
- Line 917: Magic number found - consider using constants
- Line 933: Magic number found - consider using constants
- Line 1007: Magic number found - consider using constants

### tests/test_analysis.py
- Line 22: Magic number found - consider using constants
- Line 23: Magic number found - consider using constants
- Line 45: Magic number found - consider using constants
- Line 46: Magic number found - consider using constants

### tests/test_sync_receiver.py
- Line 27: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants

### tests/test_geometry_utils.py
- Line 13: Magic number found - consider using constants
- Line 20: Magic number found - consider using constants

### tests/test_performance_comprehensive.py
- Line 72: Line too long (125 > 120 characters)
- Line 77: Magic number found - consider using constants
- Line 154: Magic number found - consider using constants
- Line 164: Magic number found - consider using constants
- Line 166: Magic number found - consider using constants
- Line 180: Magic number found - consider using constants
- Line 190: Magic number found - consider using constants
- Line 193: Magic number found - consider using constants
- Line 195: Magic number found - consider using constants
- Line 202: Line too long (256 > 120 characters)
- Line 202: Magic number found - consider using constants
- Line 230: Magic number found - consider using constants
- Line 232: Magic number found - consider using constants
- Line 282: Magic number found - consider using constants
- Line 285: Magic number found - consider using constants
- Line 287: Magic number found - consider using constants
- Line 293: Magic number found - consider using constants
- Line 298: Magic number found - consider using constants
- Line 299: Magic number found - consider using constants
- Line 318: Magic number found - consider using constants
- Line 357: Magic number found - consider using constants
- Line 358: Magic number found - consider using constants
- Line 389: Magic number found - consider using constants
- Line 390: Magic number found - consider using constants
- Line 450: Magic number found - consider using constants
- Line 456: Magic number found - consider using constants
- Line 458: Magic number found - consider using constants
- Line 467: Line too long (170 > 120 characters)
- Line 468: Line too long (148 > 120 characters)
- Line 489: Magic number found - consider using constants
- Line 492: Magic number found - consider using constants
- Line 494: Magic number found - consider using constants
- Line 497: Magic number found - consider using constants
- Line 516: Line too long (232 > 120 characters)
- Line 527: Magic number found - consider using constants
- Line 530: Magic number found - consider using constants
- Line 543: Magic number found - consider using constants
- Line 554: Magic number found - consider using constants
- Line 557: Magic number found - consider using constants
- Line 559: Magic number found - consider using constants
- Line 576: Magic number found - consider using constants
- Line 579: Magic number found - consider using constants
- Line 581: Magic number found - consider using constants
- Line 620: Magic number found - consider using constants
- Line 679: Magic number found - consider using constants
- Line 687: Magic number found - consider using constants
- Line 689: Magic number found - consider using constants
- Line 732: Magic number found - consider using constants
- Line 743: Magic number found - consider using constants
- Line 745: Magic number found - consider using constants
- Line 762: Magic number found - consider using constants
- Line 786: Magic number found - consider using constants

### tests/test_cache.py
- Line 208: Magic number found - consider using constants
- Line 213: Magic number found - consider using constants
- Line 218: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 233: Magic number found - consider using constants
- Line 365: Magic number found - consider using constants
- Line 374: Magic number found - consider using constants
- Line 377: Magic number found - consider using constants
- Line 379: Magic number found - consider using constants
- Line 385: Magic number found - consider using constants
- Line 387: Magic number found - consider using constants
- Line 391: Magic number found - consider using constants
- Line 392: Magic number found - consider using constants
- Line 404: Magic number found - consider using constants
- Line 405: Magic number found - consider using constants
- Line 412: Magic number found - consider using constants
- Line 497: Magic number found - consider using constants

### tests/test_widget_system_comprehensive.py
- Line 295: Magic number found - consider using constants
- Line 537: Magic number found - consider using constants

### tests/test_config.py
- Line 57: Magic number found - consider using constants
- Line 69: Magic number found - consider using constants
- Line 157: Magic number found - consider using constants
- Line 160: Magic number found - consider using constants

### tests/test_tower_scanner.py
- Line 10: Magic number found - consider using constants
- Line 19: Magic number found - consider using constants
- Line 20: Magic number found - consider using constants
- Line 25: Magic number found - consider using constants
- Line 46: Magic number found - consider using constants

### tests/test_route_prefetch.py
- Line 19: Magic number found - consider using constants

### tests/test_service_comprehensive.py
- Line 63: Magic number found - consider using constants
- Line 133: Magic number found - consider using constants
- Line 148: Magic number found - consider using constants
- Line 270: Magic number found - consider using constants

### tests/test_web_server.py
- Line 54: Magic number found - consider using constants
- Line 58: Magic number found - consider using constants

### tests/test_jwt_utils_comprehensive.py
- Line 38: Magic number found - consider using constants
- Line 64: Magic number found - consider using constants
- Line 68: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants
- Line 79: Magic number found - consider using constants
- Line 83: Magic number found - consider using constants
- Line 87: Magic number found - consider using constants
- Line 111: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants
- Line 122: Magic number found - consider using constants
- Line 126: Magic number found - consider using constants
- Line 177: Magic number found - consider using constants
- Line 183: Magic number found - consider using constants
- Line 189: Magic number found - consider using constants
- Line 193: Magic number found - consider using constants
- Line 255: Magic number found - consider using constants
- Line 313: Magic number found - consider using constants
- Line 394: Magic number found - consider using constants
- Line 396: Magic number found - consider using constants
- Line 397: Magic number found - consider using constants
- Line 412: Magic number found - consider using constants
- Line 414: Magic number found - consider using constants
- Line 415: Magic number found - consider using constants
- Line 431: Magic number found - consider using constants

### tests/test_gpsd_client.py
- Line 11: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants
- Line 51: Magic number found - consider using constants
- Line 54: Magic number found - consider using constants

### tests/test_service_direct.py
- Line 32: Magic number found - consider using constants
- Line 140: Magic number found - consider using constants

### tests/test_sync.py
- Line 25: Magic number found - consider using constants
- Line 69: Magic number found - consider using constants

### tests/test_migrations_comprehensive.py
- Line 580: Magic number found - consider using constants
- Line 604: Magic number found - consider using constants

### tests/test_scheduler_tasks.py
- Line 653: Magic number found - consider using constants

### tests/test_service_api_fixed_v2.py
- Line 38: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants
- Line 59: Magic number found - consider using constants
- Line 60: Magic number found - consider using constants
- Line 80: Magic number found - consider using constants
- Line 84: Magic number found - consider using constants
- Line 87: Magic number found - consider using constants
- Line 95: Magic number found - consider using constants
- Line 129: Magic number found - consider using constants
- Line 130: Magic number found - consider using constants
- Line 141: Magic number found - consider using constants
- Line 142: Magic number found - consider using constants
- Line 264: Magic number found - consider using constants
- Line 284: Magic number found - consider using constants
- Line 289: Magic number found - consider using constants
- Line 298: Magic number found - consider using constants
- Line 299: Magic number found - consider using constants
- Line 310: Magic number found - consider using constants
- Line 333: Magic number found - consider using constants
- Line 338: Magic number found - consider using constants
- Line 362: Magic number found - consider using constants
- Line 366: Magic number found - consider using constants
- Line 383: Magic number found - consider using constants
- Line 394: Magic number found - consider using constants
- Line 399: Magic number found - consider using constants
- Line 400: Magic number found - consider using constants
- Line 404: Magic number found - consider using constants
- Line 427: Magic number found - consider using constants
- Line 432: Magic number found - consider using constants
- Line 453: Magic number found - consider using constants
- Line 499: Magic number found - consider using constants
- Line 524: Magic number found - consider using constants
- Line 529: Magic number found - consider using constants
- Line 539: Magic number found - consider using constants
- Line 540: Magic number found - consider using constants
- Line 552: Magic number found - consider using constants
- Line 584: Magic number found - consider using constants
- Line 605: Magic number found - consider using constants
- Line 610: Magic number found - consider using constants

### tests/test_service_layer.py
- Line 30: Magic number found - consider using constants
- Line 39: Magic number found - consider using constants
- Line 61: Magic number found - consider using constants
- Line 80: Magic number found - consider using constants
- Line 86: Magic number found - consider using constants
- Line 102: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants
- Line 123: Magic number found - consider using constants
- Line 131: Magic number found - consider using constants
- Line 143: Magic number found - consider using constants
- Line 148: Magic number found - consider using constants
- Line 156: Magic number found - consider using constants
- Line 269: Magic number found - consider using constants
- Line 275: Magic number found - consider using constants
- Line 283: Magic number found - consider using constants
- Line 338: Magic number found - consider using constants
- Line 348: Magic number found - consider using constants
- Line 358: Magic number found - consider using constants
- Line 368: Magic number found - consider using constants
- Line 387: Magic number found - consider using constants
- Line 393: Magic number found - consider using constants
- Line 400: Magic number found - consider using constants

### tests/test_error_reporting.py
- Line 14: Magic number found - consider using constants

### tests/test_service.py
- Line 77: Magic number found - consider using constants
- Line 80: Magic number found - consider using constants
- Line 94: Magic number found - consider using constants
- Line 121: Magic number found - consider using constants
- Line 130: Magic number found - consider using constants
- Line 136: Magic number found - consider using constants
- Line 145: Magic number found - consider using constants
- Line 159: Magic number found - consider using constants
- Line 173: Magic number found - consider using constants
- Line 188: Magic number found - consider using constants
- Line 206: Magic number found - consider using constants
- Line 244: Magic number found - consider using constants
- Line 256: Magic number found - consider using constants
- Line 297: Magic number found - consider using constants
- Line 312: Magic number found - consider using constants
- Line 402: Magic number found - consider using constants
- Line 416: Magic number found - consider using constants
- Line 428: Magic number found - consider using constants
- Line 439: Magic number found - consider using constants
- Line 463: Magic number found - consider using constants
- Line 469: Magic number found - consider using constants
- Line 498: Magic number found - consider using constants
- Line 530: Magic number found - consider using constants
- Line 532: Magic number found - consider using constants
- Line 544: Magic number found - consider using constants
- Line 570: Magic number found - consider using constants
- Line 581: Magic number found - consider using constants
- Line 592: Magic number found - consider using constants
- Line 609: Magic number found - consider using constants
- Line 624: Magic number found - consider using constants
- Line 637: Magic number found - consider using constants
- Line 643: Magic number found - consider using constants
- Line 653: Magic number found - consider using constants
- Line 664: Magic number found - consider using constants
- Line 677: Magic number found - consider using constants
- Line 678: Magic number found - consider using constants
- Line 682: Magic number found - consider using constants
- Line 697: Magic number found - consider using constants
- Line 717: Magic number found - consider using constants

### tests/test_service_api_fixed.py
- Line 38: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants
- Line 58: Magic number found - consider using constants
- Line 59: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants
- Line 84: Magic number found - consider using constants
- Line 90: Magic number found - consider using constants
- Line 97: Magic number found - consider using constants
- Line 134: Magic number found - consider using constants
- Line 135: Magic number found - consider using constants
- Line 149: Magic number found - consider using constants
- Line 150: Magic number found - consider using constants
- Line 257: Magic number found - consider using constants
- Line 264: Magic number found - consider using constants
- Line 280: Magic number found - consider using constants
- Line 301: Magic number found - consider using constants
- Line 306: Magic number found - consider using constants
- Line 315: Magic number found - consider using constants
- Line 316: Magic number found - consider using constants
- Line 327: Magic number found - consider using constants
- Line 340: Magic number found - consider using constants
- Line 345: Magic number found - consider using constants
- Line 366: Magic number found - consider using constants
- Line 387: Magic number found - consider using constants
- Line 399: Magic number found - consider using constants
- Line 406: Magic number found - consider using constants
- Line 439: Magic number found - consider using constants
- Line 446: Magic number found - consider using constants
- Line 473: Magic number found - consider using constants
- Line 522: Magic number found - consider using constants
- Line 547: Magic number found - consider using constants
- Line 552: Magic number found - consider using constants
- Line 562: Magic number found - consider using constants
- Line 563: Magic number found - consider using constants
- Line 575: Magic number found - consider using constants
- Line 578: Magic number found - consider using constants
- Line 611: Magic number found - consider using constants
- Line 632: Magic number found - consider using constants
- Line 637: Magic number found - consider using constants

### tests/test_localization.py
- Line 267: Magic number found - consider using constants
- Line 279: Magic number found - consider using constants
- Line 298: Magic number found - consider using constants
- Line 311: Magic number found - consider using constants

### tests/test_integration_core.py
- Line 58: Magic number found - consider using constants
- Line 61: Magic number found - consider using constants

### tests/test_tile_maintenance.py
- Line 57: Magic number found - consider using constants

### tests/test_health_monitor.py
- Line 73: Magic number found - consider using constants
- Line 110: Magic number found - consider using constants

### tests/test_api_service.py
- Line 90: Magic number found - consider using constants
- Line 100: Magic number found - consider using constants
- Line 105: Magic number found - consider using constants
- Line 114: Magic number found - consider using constants
- Line 118: Magic number found - consider using constants
- Line 123: Magic number found - consider using constants
- Line 129: Magic number found - consider using constants
- Line 133: Magic number found - consider using constants
- Line 137: Magic number found - consider using constants
- Line 138: Magic number found - consider using constants
- Line 146: Magic number found - consider using constants
- Line 147: Magic number found - consider using constants
- Line 148: Magic number found - consider using constants
- Line 149: Magic number found - consider using constants
- Line 154: Magic number found - consider using constants
- Line 159: Magic number found - consider using constants
- Line 162: Magic number found - consider using constants
- Line 185: Magic number found - consider using constants
- Line 186: Magic number found - consider using constants
- Line 187: Magic number found - consider using constants
- Line 197: Magic number found - consider using constants
- Line 198: Magic number found - consider using constants
- Line 199: Magic number found - consider using constants
- Line 205: Magic number found - consider using constants
- Line 209: Magic number found - consider using constants
- Line 214: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 234: Magic number found - consider using constants
- Line 244: Magic number found - consider using constants
- Line 249: Magic number found - consider using constants
- Line 254: Magic number found - consider using constants
- Line 264: Magic number found - consider using constants
- Line 272: Magic number found - consider using constants
- Line 277: Magic number found - consider using constants
- Line 298: Magic number found - consider using constants
- Line 304: Magic number found - consider using constants
- Line 308: Magic number found - consider using constants
- Line 313: Magic number found - consider using constants
- Line 324: Magic number found - consider using constants
- Line 325: Magic number found - consider using constants
- Line 332: Magic number found - consider using constants
- Line 333: Magic number found - consider using constants
- Line 347: Magic number found - consider using constants
- Line 352: Magic number found - consider using constants
- Line 380: Magic number found - consider using constants
- Line 385: Magic number found - consider using constants
- Line 408: Magic number found - consider using constants
- Line 413: Magic number found - consider using constants
- Line 430: Magic number found - consider using constants
- Line 435: Magic number found - consider using constants
- Line 455: Magic number found - consider using constants
- Line 460: Magic number found - consider using constants
- Line 466: Magic number found - consider using constants
- Line 476: Magic number found - consider using constants
- Line 477: Magic number found - consider using constants
- Line 488: Magic number found - consider using constants
- Line 493: Magic number found - consider using constants
- Line 503: Magic number found - consider using constants
- Line 508: Magic number found - consider using constants
- Line 597: Magic number found - consider using constants
- Line 603: Magic number found - consider using constants
- Line 608: Magic number found - consider using constants
- Line 620: Magic number found - consider using constants
- Line 625: Magic number found - consider using constants
- Line 629: Magic number found - consider using constants
- Line 634: Magic number found - consider using constants
- Line 644: Magic number found - consider using constants
- Line 649: Magic number found - consider using constants
- Line 666: Magic number found - consider using constants
- Line 673: Magic number found - consider using constants
- Line 677: Magic number found - consider using constants
- Line 684: Magic number found - consider using constants
- Line 693: Magic number found - consider using constants
- Line 706: Magic number found - consider using constants
- Line 713: Magic number found - consider using constants
- Line 720: Magic number found - consider using constants
- Line 738: Magic number found - consider using constants
- Line 748: Magic number found - consider using constants
- Line 749: Magic number found - consider using constants
- Line 763: Magic number found - consider using constants
- Line 768: Magic number found - consider using constants
- Line 778: Magic number found - consider using constants
- Line 784: Magic number found - consider using constants
- Line 790: Magic number found - consider using constants
- Line 807: Magic number found - consider using constants
- Line 811: Magic number found - consider using constants
- Line 815: Magic number found - consider using constants
- Line 819: Magic number found - consider using constants
- Line 827: Magic number found - consider using constants
- Line 835: Magic number found - consider using constants
- Line 852: Magic number found - consider using constants

### tests/test_security_analyzer_integration.py
- Line 8: Magic number found - consider using constants
- Line 21: Magic number found - consider using constants
- Line 29: Magic number found - consider using constants

### tests/test_performance_dashboard_integration.py
- Line 30: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants
- Line 38: Magic number found - consider using constants
- Line 43: Magic number found - consider using constants
- Line 52: Magic number found - consider using constants
- Line 57: Magic number found - consider using constants
- Line 74: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants
- Line 82: Magic number found - consider using constants
- Line 87: Magic number found - consider using constants
- Line 119: Magic number found - consider using constants
- Line 124: Magic number found - consider using constants
- Line 153: Magic number found - consider using constants
- Line 160: Magic number found - consider using constants
- Line 167: Magic number found - consider using constants

### tests/test_service_plugins.py
- Line 28: Magic number found - consider using constants

### tests/test_wifi_scanner.py
- Line 18: Magic number found - consider using constants
- Line 24: Magic number found - consider using constants
- Line 51: Magic number found - consider using constants
- Line 75: Magic number found - consider using constants
- Line 81: Magic number found - consider using constants

### tests/test_export_log_bundle_script.py
- Line 8: Magic number found - consider using constants

### web/app.py
- Line 32: Magic number found - consider using constants
- Line 37: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants
- Line 76: Magic number found - consider using constants
- Line 77: Magic number found - consider using constants

### benchmarks/packet_parse_benchmark.py
- Line 12: Magic number found - consider using constants
- Line 16: Magic number found - consider using constants
- Line 29: Magic number found - consider using constants

### benchmarks/plot_benchmark.py
- Line 12: Magic number found - consider using constants
- Line 14: Magic number found - consider using constants

### benchmarks/persistence_benchmark.py
- Line 11: Magic number found - consider using constants
- Line 37: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants

### examples/direction_finding_example.py
- Line 114: Magic number found - consider using constants
- Line 115: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants
- Line 117: Magic number found - consider using constants
- Line 159: Magic number found - consider using constants
- Line 262: Magic number found - consider using constants
- Line 267: Magic number found - consider using constants
- Line 272: Magic number found - consider using constants

### examples/security_analysis_example.py
- Line 12: Magic number found - consider using constants

### scripts/df_integration_demo.py
- Line 156: Magic number found - consider using constants
- Line 157: Magic number found - consider using constants
- Line 163: Magic number found - consider using constants
- Line 164: Magic number found - consider using constants
- Line 170: Magic number found - consider using constants
- Line 171: Magic number found - consider using constants

### scripts/monitoring_service.py
- Line 58: Magic number found - consider using constants
- Line 134: Magic number found - consider using constants
- Line 140: Line too long (132 > 120 characters)
- Line 164: Magic number found - consider using constants
- Line 171: Line too long (151 > 120 characters)
- Line 226: Line too long (138 > 120 characters)
- Line 328: Line too long (137 > 120 characters)
- Line 331: Magic number found - consider using constants
- Line 332: Magic number found - consider using constants
- Line 378: Magic number found - consider using constants
- Line 384: Magic number found - consider using constants
- Line 387: Magic number found - consider using constants
- Line 478: Magic number found - consider using constants

### scripts/export_logs.py
- Line 23: Magic number found - consider using constants

### scripts/dependency_audit.py
- Line 270: Magic number found - consider using constants
- Line 312: Line too long (122 > 120 characters)

### scripts/export_log_bundle.py
- Line 23: Magic number found - consider using constants

### scripts/simple_db_check.py
- Line 18: Line too long (217 > 120 characters)
- Line 71: Line too long (175 > 120 characters)
- Line 82: Line too long (181 > 120 characters)
- Line 105: Line too long (137 > 120 characters)

### scripts/test_database_functions.py
- Line 48: Line too long (449 > 120 characters)
- Line 48: Magic number found - consider using constants
- Line 61: Line too long (618 > 120 characters)
- Line 61: Magic number found - consider using constants
- Line 66: Line too long (186 > 120 characters)
- Line 67: Line too long (121 > 120 characters)
- Line 67: Magic number found - consider using constants
- Line 68: Line too long (193 > 120 characters)
- Line 68: Magic number found - consider using constants
- Line 73: Line too long (164 > 120 characters)
- Line 74: Line too long (285 > 120 characters)
- Line 74: Magic number found - consider using constants
- Line 83: Line too long (443 > 120 characters)
- Line 83: Magic number found - consider using constants
- Line 94: Line too long (264 > 120 characters)
- Line 94: Magic number found - consider using constants
- Line 103: Line too long (203 > 120 characters)
- Line 133: Line too long (132 > 120 characters)

### scripts/export_grafana.py
- Line 64: Magic number found - consider using constants

### scripts/performance_cli.py
- Line 59: Magic number found - consider using constants
- Line 127: Magic number found - consider using constants
- Line 184: Magic number found - consider using constants
- Line 185: Magic number found - consider using constants
- Line 289: Magic number found - consider using constants

### scripts/bench_geom.py
- Line 13: Magic number found - consider using constants
- Line 14: Magic number found - consider using constants
- Line 17: Magic number found - consider using constants

### scripts/calibrate_orientation.py
- Line 40: Magic number found - consider using constants

### scripts/mobile_diagnostics.py
- Line 24: Magic number found - consider using constants
- Line 39: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants
- Line 73: Magic number found - consider using constants
- Line 134: Magic number found - consider using constants
- Line 136: Magic number found - consider using constants
- Line 143: Magic number found - consider using constants
- Line 165: Magic number found - consider using constants
- Line 168: Magic number found - consider using constants
- Line 184: Magic number found - consider using constants
- Line 197: Magic number found - consider using constants
- Line 299: Magic number found - consider using constants
- Line 309: Magic number found - consider using constants
- Line 319: Magic number found - consider using constants
- Line 331: Magic number found - consider using constants
- Line 421: TODO/FIXME comment found

### scripts/export_mysql.py
- Line 31: Magic number found - consider using constants
- Line 36: Magic number found - consider using constants

### scripts/compare_performance.py
- Line 235: Line too long (137 > 120 characters)
- Line 239: Line too long (143 > 120 characters)
- Line 259: Line too long (131 > 120 characters)
- Line 263: Line too long (137 > 120 characters)
- Line 291: Line too long (136 > 120 characters)
- Line 295: Line too long (142 > 120 characters)
- Line 313: Line too long (133 > 120 characters)
- Line 317: Line too long (139 > 120 characters)
- Line 335: Line too long (133 > 120 characters)
- Line 339: Line too long (139 > 120 characters)
- Line 376: Line too long (154 > 120 characters)
- Line 380: Line too long (160 > 120 characters)
- Line 384: Line too long (123 > 120 characters)

### scripts/performance_monitor.py
- Line 73: Magic number found - consider using constants
- Line 74: Magic number found - consider using constants
- Line 86: Magic number found - consider using constants
- Line 206: Magic number found - consider using constants
- Line 338: Magic number found - consider using constants
- Line 639: Magic number found - consider using constants

### scripts/tile_maintenance_cli.py
- Line 59: Magic number found - consider using constants

### scripts/uav_record.py
- Line 28: Magic number found - consider using constants

### src/gps_handler.py
- Line 40: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants
- Line 44: Magic number found - consider using constants
- Line 45: Magic number found - consider using constants

### tests/models/test_api_models.py
- Line 70: Magic number found - consider using constants
- Line 75: Magic number found - consider using constants
- Line 81: Magic number found - consider using constants
- Line 86: Magic number found - consider using constants
- Line 185: Magic number found - consider using constants
- Line 186: Magic number found - consider using constants
- Line 194: Magic number found - consider using constants
- Line 199: Magic number found - consider using constants
- Line 216: Magic number found - consider using constants
- Line 217: Magic number found - consider using constants
- Line 221: Magic number found - consider using constants
- Line 222: Magic number found - consider using constants
- Line 260: Magic number found - consider using constants
- Line 261: Magic number found - consider using constants
- Line 270: Magic number found - consider using constants
- Line 280: Magic number found - consider using constants
- Line 284: Magic number found - consider using constants
- Line 294: Magic number found - consider using constants
- Line 311: Magic number found - consider using constants
- Line 314: Magic number found - consider using constants
- Line 323: Magic number found - consider using constants
- Line 324: Magic number found - consider using constants
- Line 326: Magic number found - consider using constants
- Line 333: Magic number found - consider using constants
- Line 335: Magic number found - consider using constants
- Line 356: Magic number found - consider using constants
- Line 361: Magic number found - consider using constants
- Line 367: Magic number found - consider using constants
- Line 370: Magic number found - consider using constants
- Line 418: Magic number found - consider using constants
- Line 421: Magic number found - consider using constants
- Line 470: Line too long (130 > 120 characters)

### tests/performance/test_performance_infrastructure.py
- Line 56: Magic number found - consider using constants
- Line 79: Magic number found - consider using constants
- Line 102: Magic number found - consider using constants
- Line 174: Magic number found - consider using constants
- Line 196: Magic number found - consider using constants
- Line 281: Magic number found - consider using constants
- Line 304: Magic number found - consider using constants
- Line 322: Magic number found - consider using constants
- Line 356: Magic number found - consider using constants
- Line 429: Magic number found - consider using constants
- Line 436: Magic number found - consider using constants
- Line 493: Magic number found - consider using constants

### tests/staging/test_staging_environment.py
- Line 26: Magic number found - consider using constants
- Line 51: Magic number found - consider using constants
- Line 61: Magic number found - consider using constants
- Line 71: Magic number found - consider using constants
- Line 72: Magic number found - consider using constants
- Line 73: Magic number found - consider using constants
- Line 74: Magic number found - consider using constants
- Line 75: Magic number found - consider using constants
- Line 76: Magic number found - consider using constants
- Line 77: Magic number found - consider using constants
- Line 78: Magic number found - consider using constants
- Line 109: Magic number found - consider using constants
- Line 117: Magic number found - consider using constants
- Line 118: Magic number found - consider using constants
- Line 124: Magic number found - consider using constants
- Line 125: Magic number found - consider using constants
- Line 134: Magic number found - consider using constants
- Line 193: Magic number found - consider using constants
- Line 201: Magic number found - consider using constants
- Line 220: Magic number found - consider using constants
- Line 235: Magic number found - consider using constants
- Line 246: Magic number found - consider using constants
- Line 281: Magic number found - consider using constants
- Line 292: Magic number found - consider using constants
- Line 303: Magic number found - consider using constants
- Line 313: Magic number found - consider using constants
- Line 324: Magic number found - consider using constants
- Line 335: Magic number found - consider using constants
- Line 347: Magic number found - consider using constants
- Line 348: Magic number found - consider using constants
- Line 359: Magic number found - consider using constants
- Line 363: Magic number found - consider using constants
- Line 370: Magic number found - consider using constants
- Line 381: Magic number found - consider using constants

### tests/logging/test_structured_logger.py
- Line 50: Magic number found - consider using constants
- Line 51: Magic number found - consider using constants
- Line 55: Magic number found - consider using constants
- Line 56: Magic number found - consider using constants
- Line 66: Magic number found - consider using constants
- Line 67: Magic number found - consider using constants
- Line 68: Magic number found - consider using constants
- Line 75: Magic number found - consider using constants
- Line 76: Magic number found - consider using constants
- Line 77: Magic number found - consider using constants
- Line 90: Magic number found - consider using constants
- Line 94: Magic number found - consider using constants
- Line 97: Magic number found - consider using constants
- Line 119: Magic number found - consider using constants
- Line 123: Magic number found - consider using constants
- Line 124: Magic number found - consider using constants
- Line 181: Magic number found - consider using constants
- Line 204: Magic number found - consider using constants
- Line 216: Magic number found - consider using constants
- Line 384: Magic number found - consider using constants
- Line 401: Magic number found - consider using constants
- Line 446: Magic number found - consider using constants
- Line 449: Magic number found - consider using constants
- Line 456: Magic number found - consider using constants
- Line 457: Magic number found - consider using constants
- Line 460: Magic number found - consider using constants
- Line 461: Magic number found - consider using constants
- Line 483: Magic number found - consider using constants
- Line 508: Magic number found - consider using constants
- Line 509: Magic number found - consider using constants
- Line 587: Magic number found - consider using constants
- Line 597: Magic number found - consider using constants
- Line 817: Magic number found - consider using constants
- Line 821: Magic number found - consider using constants
- Line 822: Magic number found - consider using constants
- Line 827: Magic number found - consider using constants
- Line 831: Magic number found - consider using constants
- Line 839: Magic number found - consider using constants
- Line 847: Magic number found - consider using constants
- Line 848: Magic number found - consider using constants

### webui/tests/run_agg_server.py
- Line 40: Magic number found - consider using constants

### docs/examples/python_examples.py
- Line 7: Magic number found - consider using constants

### examples/plugins/weather_widget.py
- Line 33: Magic number found - consider using constants
- Line 34: Magic number found - consider using constants

### src/piwardrive/mysql_export.py
- Line 21: Magic number found - consider using constants
- Line 59: Magic number found - consider using constants
- Line 80: Magic number found - consider using constants
- Line 155: Magic number found - consider using constants
- Line 166: Magic number found - consider using constants
- Line 214: Magic number found - consider using constants
- Line 218: Magic number found - consider using constants
- Line 260: Magic number found - consider using constants
- Line 329: Magic number found - consider using constants
- Line 332: Magic number found - consider using constants
- Line 360: Magic number found - consider using constants

### src/piwardrive/diagnostics.py
- Line 298: Magic number found - consider using constants
- Line 305: Magic number found - consider using constants
- Line 363: Magic number found - consider using constants
- Line 436: Magic number found - consider using constants
- Line 463: Magic number found - consider using constants

### src/piwardrive/db_browser.py
- Line 30: Magic number found - consider using constants
- Line 33: Magic number found - consider using constants
- Line 39: Magic number found - consider using constants

### src/piwardrive/lora_scanner.py
- Line 167: Magic number found - consider using constants

### src/piwardrive/route_prefetch.py
- Line 35: Magic number found - consider using constants
- Line 42: Magic number found - consider using constants
- Line 54: Magic number found - consider using constants
- Line 65: Magic number found - consider using constants

### src/piwardrive/gpsd_client.py
- Line 46: Magic number found - consider using constants
- Line 48: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants
- Line 51: Magic number found - consider using constants

### src/piwardrive/aggregation_service.py
- Line 27: Magic number found - consider using constants
- Line 128: Magic number found - consider using constants
- Line 133: Magic number found - consider using constants

### src/piwardrive/memory_monitor.py
- Line 36: Magic number found - consider using constants
- Line 47: Magic number found - consider using constants

### src/piwardrive/widget_manager.py
- Line 35: Magic number found - consider using constants

### src/piwardrive/gpsd_client_async.py
- Line 21: Magic number found - consider using constants
- Line 23: Magic number found - consider using constants
- Line 25: Magic number found - consider using constants
- Line 26: Magic number found - consider using constants

### src/piwardrive/network_analytics.py
- Line 41: Magic number found - consider using constants

### src/piwardrive/main.py
- Line 87: Magic number found - consider using constants
- Line 89: Magic number found - consider using constants
- Line 130: Magic number found - consider using constants
- Line 150: Magic number found - consider using constants
- Line 167: Magic number found - consider using constants
- Line 190: Magic number found - consider using constants

### src/piwardrive/web_server.py
- Line 38: Magic number found - consider using constants

### src/piwardrive/graphql_api.py
- Line 85: Magic number found - consider using constants
- Line 87: Magic number found - consider using constants

### src/piwardrive/sync.py
- Line 34: Magic number found - consider using constants

### src/piwardrive/orientation_sensors.py
- Line 7: Magic number found - consider using constants
- Line 39: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants
- Line 44: Magic number found - consider using constants
- Line 46: Magic number found - consider using constants
- Line 47: Magic number found - consider using constants

### src/piwardrive/jwt_utils.py
- Line 16: Magic number found - consider using constants
- Line 17: Magic number found - consider using constants

### src/piwardrive/error_middleware.py
- Line 55: Magic number found - consider using constants

### src/piwardrive/setup_wizard.py
- Line 23: Magic number found - consider using constants
- Line 28: Magic number found - consider using constants

### src/piwardrive/exception_handler.py
- Line 5: Magic number found - consider using constants
- Line 47: Magic number found - consider using constants
- Line 69: Magic number found - consider using constants

### src/piwardrive/unified_platform.py
- Line 105: Magic number found - consider using constants
- Line 106: Magic number found - consider using constants
- Line 371: Magic number found - consider using constants
- Line 389: Magic number found - consider using constants
- Line 393: Magic number found - consider using constants
- Line 413: Magic number found - consider using constants
- Line 417: Magic number found - consider using constants
- Line 427: Magic number found - consider using constants
- Line 436: Magic number found - consider using constants
- Line 446: Magic number found - consider using constants
- Line 448: Magic number found - consider using constants
- Line 682: Line too long (134 > 120 characters)
- Line 692: Line too long (124 > 120 characters)
- Line 694: Line too long (149 > 120 characters)
- Line 695: Line too long (144 > 120 characters)
- Line 768: Magic number found - consider using constants
- Line 836: Magic number found - consider using constants
- Line 837: Magic number found - consider using constants
- Line 844: Magic number found - consider using constants
- Line 848: Magic number found - consider using constants

### src/piwardrive/services/maintenance.py
- Line 68: Magic number found - consider using constants

### src/piwardrive/services/db_monitor.py
- Line 51: Line too long (161 > 120 characters)

### src/piwardrive/services/report_generator.py
- Line 72: Magic number found - consider using constants

### src/piwardrive/services/analysis_queries.py
- Line 14: Magic number found - consider using constants
- Line 15: Magic number found - consider using constants

### src/piwardrive/services/view_refresher.py
- Line 13: Magic number found - consider using constants
- Line 18: Magic number found - consider using constants

### src/piwardrive/services/network_analytics.py
- Line 18: Magic number found - consider using constants
- Line 116: Magic number found - consider using constants

### src/piwardrive/services/stream_processor.py
- Line 19: Magic number found - consider using constants

### src/piwardrive/services/model_trainer.py
- Line 13: Magic number found - consider using constants
- Line 18: Magic number found - consider using constants
- Line 32: Magic number found - consider using constants

### src/piwardrive/models/api_models.py
- Line 43: Magic number found - consider using constants
- Line 48: Magic number found - consider using constants
- Line 147: Magic number found - consider using constants
- Line 152: Magic number found - consider using constants
- Line 180: Magic number found - consider using constants

### src/piwardrive/mqtt/__init__.py
- Line 17: Magic number found - consider using constants

### src/piwardrive/analysis/packet_engine.py
- Line 24: Magic number found - consider using constants
- Line 73: Magic number found - consider using constants
- Line 222: Magic number found - consider using constants
- Line 261: Magic number found - consider using constants
- Line 459: Magic number found - consider using constants
- Line 490: Magic number found - consider using constants
- Line 799: Magic number found - consider using constants
- Line 806: Magic number found - consider using constants
- Line 807: Magic number found - consider using constants
- Line 808: Magic number found - consider using constants
- Line 809: Magic number found - consider using constants
- Line 819: Magic number found - consider using constants
- Line 821: Magic number found - consider using constants
- Line 829: Magic number found - consider using constants
- Line 840: Magic number found - consider using constants
- Line 847: Magic number found - consider using constants
- Line 918: Magic number found - consider using constants
- Line 919: Magic number found - consider using constants
- Line 924: Magic number found - consider using constants
- Line 1186: Line too long (122 > 120 characters)

### src/piwardrive/performance/realtime_optimizer.py
- Line 59: Magic number found - consider using constants
- Line 147: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 248: Magic number found - consider using constants
- Line 375: Magic number found - consider using constants
- Line 383: Magic number found - consider using constants
- Line 427: Magic number found - consider using constants
- Line 428: Magic number found - consider using constants
- Line 581: Magic number found - consider using constants
- Line 584: Magic number found - consider using constants

### src/piwardrive/performance/async_optimizer.py
- Line 38: Magic number found - consider using constants
- Line 72: TODO/FIXME comment found
- Line 531: Magic number found - consider using constants

### src/piwardrive/performance/db_optimizer.py
- Line 61: Magic number found - consider using constants
- Line 111: Magic number found - consider using constants
- Line 234: Magic number found - consider using constants
- Line 348: Magic number found - consider using constants
- Line 367: Magic number found - consider using constants
- Line 369: Magic number found - consider using constants

### src/piwardrive/performance/optimization.py
- Line 125: Magic number found - consider using constants
- Line 240: Magic number found - consider using constants
- Line 495: Magic number found - consider using constants
- Line 501: Magic number found - consider using constants
- Line 742: Magic number found - consider using constants
- Line 857: Magic number found - consider using constants
- Line 922: Magic number found - consider using constants
- Line 924: Magic number found - consider using constants
- Line 926: Magic number found - consider using constants
- Line 930: Magic number found - consider using constants
- Line 934: Magic number found - consider using constants
- Line 973: Magic number found - consider using constants
- Line 1039: Magic number found - consider using constants
- Line 1056: Magic number found - consider using constants
- Line 1091: Magic number found - consider using constants

### src/piwardrive/ui/user_experience.py
- Line 130: Line too long (125 > 120 characters)
- Line 641: Magic number found - consider using constants
- Line 647: Magic number found - consider using constants
- Line 653: Magic number found - consider using constants
- Line 659: Magic number found - consider using constants
- Line 665: Magic number found - consider using constants
- Line 671: Magic number found - consider using constants
- Line 677: Magic number found - consider using constants
- Line 683: Magic number found - consider using constants
- Line 715: Magic number found - consider using constants
- Line 716: Magic number found - consider using constants
- Line 717: Magic number found - consider using constants
- Line 718: Magic number found - consider using constants
- Line 883: Magic number found - consider using constants
- Line 1305: Magic number found - consider using constants
- Line 1307: Magic number found - consider using constants
- Line 1412: Magic number found - consider using constants

### src/piwardrive/cli/kiosk.py
- Line 11: Magic number found - consider using constants

### src/piwardrive/testing/automated_framework.py
- Line 385: Magic number found - consider using constants
- Line 453: Magic number found - consider using constants
- Line 454: Magic number found - consider using constants
- Line 457: Magic number found - consider using constants
- Line 532: Magic number found - consider using constants
- Line 579: Magic number found - consider using constants
- Line 656: Magic number found - consider using constants
- Line 672: Magic number found - consider using constants
- Line 673: Magic number found - consider using constants
- Line 697: Magic number found - consider using constants
- Line 1021: Magic number found - consider using constants

### src/piwardrive/migrations/001_create_scan_sessions.py
- Line 41: Line too long (124 > 120 characters)

### src/piwardrive/migrations/010_performance_indexes.py
- Line 13: Line too long (124 > 120 characters)

### src/piwardrive/core/config.py
- Line 24: Magic number found - consider using constants
- Line 26: Magic number found - consider using constants
- Line 28: Magic number found - consider using constants

### src/piwardrive/core/utils.py
- Line 132: Magic number found - consider using constants
- Line 265: Magic number found - consider using constants
- Line 266: Magic number found - consider using constants
- Line 267: Magic number found - consider using constants
- Line 268: Magic number found - consider using constants
- Line 269: Magic number found - consider using constants
- Line 270: Magic number found - consider using constants
- Line 271: Magic number found - consider using constants
- Line 272: Magic number found - consider using constants
- Line 273: Magic number found - consider using constants
- Line 274: Magic number found - consider using constants
- Line 276: Magic number found - consider using constants
- Line 277: Magic number found - consider using constants
- Line 278: Magic number found - consider using constants
- Line 497: Magic number found - consider using constants
- Line 561: Magic number found - consider using constants
- Line 562: Magic number found - consider using constants
- Line 902: Magic number found - consider using constants
- Line 903: Magic number found - consider using constants
- Line 912: Magic number found - consider using constants
- Line 1110: Magic number found - consider using constants
- Line 1147: Magic number found - consider using constants

### src/piwardrive/core/persistence.py
- Line 245: Magic number found - consider using constants
- Line 1137: Magic number found - consider using constants
- Line 1138: Magic number found - consider using constants
- Line 1463: Magic number found - consider using constants
- Line 1502: Magic number found - consider using constants
- Line 1515: Magic number found - consider using constants
- Line 1608: Magic number found - consider using constants
- Line 1611: Magic number found - consider using constants
- Line 1622: Magic number found - consider using constants
- Line 1739: Magic number found - consider using constants

### src/piwardrive/web/webui_server.py
- Line 38: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants

### src/piwardrive/direction_finding/hardware.py
- Line 79: Magic number found - consider using constants
- Line 80: Magic number found - consider using constants
- Line 130: Magic number found - consider using constants
- Line 614: Magic number found - consider using constants
- Line 715: Magic number found - consider using constants
- Line 775: Magic number found - consider using constants

### src/piwardrive/direction_finding/config.py
- Line 154: Magic number found - consider using constants
- Line 166: Magic number found - consider using constants
- Line 178: Magic number found - consider using constants
- Line 207: Magic number found - consider using constants

### src/piwardrive/direction_finding/algorithms.py
- Line 72: Magic number found - consider using constants
- Line 94: Magic number found - consider using constants
- Line 128: Magic number found - consider using constants
- Line 145: Magic number found - consider using constants
- Line 157: Magic number found - consider using constants
- Line 174: Magic number found - consider using constants
- Line 406: Magic number found - consider using constants
- Line 438: Magic number found - consider using constants
- Line 607: Magic number found - consider using constants

### src/piwardrive/direction_finding/integration.py
- Line 33: Magic number found - consider using constants

### src/piwardrive/integration/system_orchestration.py
- Line 133: Magic number found - consider using constants
- Line 258: Magic number found - consider using constants
- Line 270: Magic number found - consider using constants
- Line 797: Magic number found - consider using constants
- Line 886: Magic number found - consider using constants

### src/piwardrive/db/sqlite.py
- Line 40: Magic number found - consider using constants

### src/piwardrive/reporting/professional.py
- Line 407: Magic number found - consider using constants
- Line 813: Magic number found - consider using constants
- Line 1029: Magic number found - consider using constants
- Line 1032: Magic number found - consider using constants

### src/piwardrive/map/tile_maintenance.py
- Line 57: Magic number found - consider using constants
- Line 76: Magic number found - consider using constants
- Line 168: Magic number found - consider using constants
- Line 170: Magic number found - consider using constants
- Line 172: Magic number found - consider using constants
- Line 217: Magic number found - consider using constants

### src/piwardrive/ml/threat_detection.py
- Line 1229: Line too long (122 > 120 characters)

### src/piwardrive/hardware/enhanced_hardware.py
- Line 161: Magic number found - consider using constants
- Line 384: Magic number found - consider using constants
- Line 524: Magic number found - consider using constants
- Line 761: Magic number found - consider using constants
- Line 833: Magic number found - consider using constants
- Line 834: Magic number found - consider using constants
- Line 835: Magic number found - consider using constants
- Line 871: Magic number found - consider using constants
- Line 931: Magic number found - consider using constants
- Line 943: Magic number found - consider using constants
- Line 1004: Magic number found - consider using constants
- Line 1064: Magic number found - consider using constants

### src/piwardrive/analytics/iot.py
- Line 60: Magic number found - consider using constants

### src/piwardrive/navigation/offline_navigation.py
- Line 245: Magic number found - consider using constants
- Line 331: Magic number found - consider using constants
- Line 346: Magic number found - consider using constants
- Line 356: Magic number found - consider using constants

### src/piwardrive/geospatial/intelligence.py
- Line 567: Magic number found - consider using constants

### src/piwardrive/jobs/maintenance_jobs.py
- Line 28: Magic number found - consider using constants
- Line 35: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants
- Line 45: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants
- Line 55: Magic number found - consider using constants

### src/piwardrive/jobs/analytics_jobs.py
- Line 32: Magic number found - consider using constants
- Line 37: Magic number found - consider using constants
- Line 42: Magic number found - consider using constants
- Line 47: Magic number found - consider using constants

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 115: Magic number found - consider using constants
- Line 646: Magic number found - consider using constants
- Line 666: Magic number found - consider using constants
- Line 863: Magic number found - consider using constants
- Line 1255: Magic number found - consider using constants
- Line 1299: Magic number found - consider using constants
- Line 1353: Magic number found - consider using constants
- Line 1365: Magic number found - consider using constants
- Line 1366: Magic number found - consider using constants
- Line 1367: Magic number found - consider using constants
- Line 1368: Magic number found - consider using constants
- Line 1445: Magic number found - consider using constants

### src/piwardrive/enhanced/critical_additions.py
- Line 123: Magic number found - consider using constants
- Line 229: Magic number found - consider using constants
- Line 232: Magic number found - consider using constants
- Line 428: Magic number found - consider using constants
- Line 429: Magic number found - consider using constants
- Line 433: Magic number found - consider using constants
- Line 441: Magic number found - consider using constants
- Line 459: Magic number found - consider using constants
- Line 462: Magic number found - consider using constants
- Line 474: Magic number found - consider using constants
- Line 485: Magic number found - consider using constants
- Line 491: Magic number found - consider using constants
- Line 498: Magic number found - consider using constants
- Line 542: Magic number found - consider using constants
- Line 547: Magic number found - consider using constants
- Line 686: Magic number found - consider using constants
- Line 688: Magic number found - consider using constants
- Line 689: Magic number found - consider using constants
- Line 713: Magic number found - consider using constants
- Line 809: Magic number found - consider using constants
- Line 811: Magic number found - consider using constants
- Line 826: Magic number found - consider using constants
- Line 884: Magic number found - consider using constants
- Line 885: Magic number found - consider using constants
- Line 886: Magic number found - consider using constants
- Line 888: Magic number found - consider using constants
- Line 908: Magic number found - consider using constants
- Line 927: Magic number found - consider using constants
- Line 928: Magic number found - consider using constants
- Line 929: Magic number found - consider using constants
- Line 930: Magic number found - consider using constants
- Line 931: Magic number found - consider using constants
- Line 960: Magic number found - consider using constants
- Line 965: Magic number found - consider using constants
- Line 966: Magic number found - consider using constants
- Line 971: Magic number found - consider using constants
- Line 972: Magic number found - consider using constants
- Line 990: Magic number found - consider using constants
- Line 996: Magic number found - consider using constants
- Line 997: Magic number found - consider using constants

### src/piwardrive/routes/analytics.py
- Line 18: Magic number found - consider using constants
- Line 44: Magic number found - consider using constants
- Line 57: Magic number found - consider using constants

### src/piwardrive/routes/bluetooth.py
- Line 24: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants
- Line 56: Magic number found - consider using constants

### src/piwardrive/routes/wifi.py
- Line 26: Magic number found - consider using constants
- Line 69: Magic number found - consider using constants
- Line 113: Magic number found - consider using constants
- Line 155: Magic number found - consider using constants

### src/piwardrive/routes/security.py
- Line 17: Magic number found - consider using constants
- Line 50: Magic number found - consider using constants

### src/piwardrive/routes/cellular.py
- Line 24: Magic number found - consider using constants
- Line 40: Magic number found - consider using constants
- Line 56: Magic number found - consider using constants

### src/piwardrive/protocols/multi_protocol.py
- Line 123: Magic number found - consider using constants
- Line 124: Magic number found - consider using constants
- Line 327: Magic number found - consider using constants
- Line 335: Magic number found - consider using constants
- Line 536: Magic number found - consider using constants
- Line 538: Magic number found - consider using constants
- Line 539: Magic number found - consider using constants
- Line 545: Magic number found - consider using constants
- Line 547: Magic number found - consider using constants
- Line 548: Magic number found - consider using constants
- Line 566: Magic number found - consider using constants
- Line 567: Magic number found - consider using constants
- Line 653: Magic number found - consider using constants
- Line 654: Magic number found - consider using constants
- Line 657: Magic number found - consider using constants
- Line 662: Magic number found - consider using constants
- Line 663: Magic number found - consider using constants
- Line 666: Magic number found - consider using constants
- Line 673: Magic number found - consider using constants
- Line 674: Magic number found - consider using constants
- Line 680: Magic number found - consider using constants
- Line 681: Magic number found - consider using constants
- Line 803: Magic number found - consider using constants

### src/piwardrive/api/logging_control.py
- Line 28: Magic number found - consider using constants

### src/piwardrive/api/performance_dashboard.py
- Line 51: Magic number found - consider using constants
- Line 87: Magic number found - consider using constants
- Line 99: Magic number found - consider using constants
- Line 111: Magic number found - consider using constants
- Line 177: Magic number found - consider using constants
- Line 192: Magic number found - consider using constants
- Line 232: Magic number found - consider using constants
- Line 345: Line too long (124 > 120 characters)
- Line 410: Magic number found - consider using constants

### src/piwardrive/visualization/advanced_viz.py
- Line 217: Magic number found - consider using constants
- Line 218: Magic number found - consider using constants
- Line 279: Magic number found - consider using constants
- Line 1107: Magic number found - consider using constants

### src/piwardrive/visualization/advanced_visualization.py
- Line 89: Magic number found - consider using constants
- Line 90: Magic number found - consider using constants
- Line 444: Magic number found - consider using constants
- Line 814: Magic number found - consider using constants
- Line 816: Magic number found - consider using constants
- Line 919: Magic number found - consider using constants

### src/piwardrive/widgets/health_analysis.py
- Line 35: Magic number found - consider using constants

### src/piwardrive/widgets/heatmap.py
- Line 31: Magic number found - consider using constants

### src/piwardrive/widgets/db_stats.py
- Line 70: Magic number found - consider using constants

### src/piwardrive/widgets/net_throughput.py
- Line 43: Magic number found - consider using constants
- Line 44: Magic number found - consider using constants

### src/piwardrive/widgets/__init__.py
- Line 153: Magic number found - consider using constants
- Line 208: Magic number found - consider using constants

### src/piwardrive/widgets/log_viewer.py
- Line 27: Magic number found - consider using constants

### src/piwardrive/data_processing/enhanced_processing.py
- Line 54: Magic number found - consider using constants
- Line 205: Magic number found - consider using constants
- Line 335: Magic number found - consider using constants
- Line 747: Magic number found - consider using constants
- Line 748: Magic number found - consider using constants
- Line 757: Magic number found - consider using constants
- Line 758: Magic number found - consider using constants

### src/piwardrive/mining/advanced_data_mining.py
- Line 106: Magic number found - consider using constants
- Line 108: Magic number found - consider using constants
- Line 486: Magic number found - consider using constants
- Line 807: Line too long (145 > 120 characters)
- Line 824: Magic number found - consider using constants
- Line 857: Line too long (123 > 120 characters)

### src/piwardrive/logging/storage.py
- Line 121: Magic number found - consider using constants
- Line 160: Magic number found - consider using constants
- Line 164: Magic number found - consider using constants
- Line 165: Magic number found - consider using constants
- Line 170: Magic number found - consider using constants
- Line 207: Magic number found - consider using constants

### src/piwardrive/signal/rf_spectrum.py
- Line 86: Magic number found - consider using constants
- Line 271: Magic number found - consider using constants
- Line 272: Magic number found - consider using constants
- Line 273: Magic number found - consider using constants
- Line 274: Magic number found - consider using constants
- Line 275: Magic number found - consider using constants
- Line 276: Magic number found - consider using constants
- Line 277: Magic number found - consider using constants
- Line 278: Magic number found - consider using constants
- Line 279: Magic number found - consider using constants
- Line 280: Magic number found - consider using constants
- Line 281: Magic number found - consider using constants
- Line 282: Magic number found - consider using constants
- Line 283: Magic number found - consider using constants
- Line 284: Magic number found - consider using constants
- Line 285: Magic number found - consider using constants
- Line 286: Magic number found - consider using constants

### src/piwardrive/integrations/sigint_suite/enrichment/oui.py
- Line 85: Magic number found - consider using constants
- Line 164: Magic number found - consider using constants

### src/piwardrive/integrations/sigint_suite/rf/spectrum.py
- Line 16: Magic number found - consider using constants

### src/piwardrive/sigint_suite/cellular/tower_tracker/tracker.py
- Line 6: Line too long (127 > 120 characters)

### src/piwardrive/api/health/endpoints.py
- Line 57: Magic number found - consider using constants

### src/piwardrive/api/auth/endpoints.py
- Line 30: Magic number found - consider using constants
- Line 41: Magic number found - consider using constants

### src/piwardrive/api/auth/dependencies.py
- Line 30: Magic number found - consider using constants
- Line 33: Magic number found - consider using constants

### src/piwardrive/api/auth/middleware.py
- Line 24: Magic number found - consider using constants

### src/piwardrive/api/system/endpoints.py
- Line 124: Magic number found - consider using constants
- Line 130: Magic number found - consider using constants
- Line 145: Magic number found - consider using constants
- Line 181: Magic number found - consider using constants
- Line 186: Magic number found - consider using constants
- Line 211: Magic number found - consider using constants
- Line 218: Magic number found - consider using constants
- Line 303: Magic number found - consider using constants
- Line 316: Magic number found - consider using constants

### src/piwardrive/api/system/endpoints_simple.py
- Line 32: Magic number found - consider using constants
