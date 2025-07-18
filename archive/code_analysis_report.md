# Code Analysis Report for PiWardrive

## Summary
- Files with issues: 477
- Total issues found: 12904

## Syntax Errors

### scripts/field_status_indicators.py
- Line 22: unexpected indent

### scripts/migrate_enhanced_schema.py
- Line 204: unterminated string literal (detected at line 204)

### scripts/optimize_database.py
- Line 17: unexpected indent

### scripts/check_migration_status.py
- Line 15: expected 'except' or 'finally' block

### scripts/create_performance_baseline.py
- Line 160: unmatched '}'

### scripts/critical_db_improvements.py
- Line 25: unexpected indent

### scripts/init_database.py
- Line 297: unterminated triple-quoted string literal (detected at line 311)

### scripts/problem_reporter.py
- Line 34: invalid syntax

### tests/test_vector_tiles_module.py
- Line 11: unterminated string literal (detected at line 11)

### scripts/enhance_schema.py
- Line 15: unexpected indent

### scripts/field_diagnostics.py
- Line 28: invalid syntax

### scripts/check_api_compatibility.py
- Line 134: unmatched ')'

### scripts/run_migrations.py
- Line 12: invalid syntax

### scripts/database_optimizer.py
- Line 65: unterminated string literal (detected at line 65)

### tests/utils/metrics.py
- Line 26: invalid decimal literal

### scripts/advanced_analytics_service.py
- Line 371: unterminated triple-quoted string literal (detected at line 383)

### tests/test_plot_cpu_temp_no_pandas.py
- Line 6: invalid syntax

### tests/test_widget_plugins.py
- Line 12: invalid syntax

## Undefined Names

### src/piwardrive/hardware/enhanced_hardware.py
- Line 1003: F821 undefined name 'picamera'

### src/piwardrive/reporting/professional.py
- Line 348: F821 undefined name 'report_data'
- Line 763: F821 undefined name 'result'

### src/piwardrive/cli/config_cli.py
- Line 64: F821 undefined name 'data'
- Line 66: F821 undefined name 'data'
- Line 69: F821 undefined name 'data'
- Line 71: F821 undefined name 'data'
- Line 75: F821 undefined name 'data'
- Line 77: F821 undefined name 'data'

### src/piwardrive/direction_finding/algorithms.py
- Line 283: F821 undefined name 'result'
- Line 354: F821 undefined name 'result'
- Line 355: F821 undefined name 'result'
- Line 727: F821 undefined name 'iq_data'
- Line 727: F821 undefined name 'iq_data'
- Line 733: F821 undefined name 'iq_data'
- Line 742: F821 undefined name 'result'
- Line 965: F821 undefined name 'result'

### src/piwardrive/performance/async_optimizer.py
- Line 142: F821 undefined name 'result'
- Line 249: F821 undefined name 'stats'
- Line 250: F821 undefined name 'stats'
- Line 251: F821 undefined name 'stats'
- Line 252: F821 undefined name 'stats'
- Line 253: F821 undefined name 'stats'
- Line 253: F821 undefined name 'stats'
- Line 255: F821 undefined name 'stats'
- Line 334: F821 undefined name 'stats'
- Line 335: F821 undefined name 'stats'
- Line 336: F821 undefined name 'stats'
- Line 337: F821 undefined name 'stats'
- Line 420: F821 undefined name 'result'
- Line 512: F821 undefined name 'stats'
- Line 513: F821 undefined name 'stats'
- Line 514: F821 undefined name 'stats'
- Line 515: F821 undefined name 'stats'
- Line 516: F821 undefined name 'stats'
- Line 517: F821 undefined name 'stats'
- Line 517: F821 undefined name 'stats'
- Line 519: F821 undefined name 'stats'
- Line 520: F821 undefined name 'stats'
- Line 520: F821 undefined name 'stats'
- Line 522: F821 undefined name 'stats'

### src/piwardrive/data_sink.py
- Line 40: F821 undefined name 'data'

### src/piwardrive/map/tile_maintenance.py
- Line 26: F821 undefined name 'result'
- Line 28: F821 undefined name 'result'

### src/piwardrive/protocols/multi_protocol.py
- Line 797: F821 undefined name 'iq_data'
- Line 1071: F821 undefined name 'stats'
- Line 1072: F821 undefined name 'stats'
- Line 1076: F821 undefined name 'stats'
- Line 1077: F821 undefined name 'stats'
- Line 1078: F821 undefined name 'stats'
- Line 1079: F821 undefined name 'stats'
- Line 1080: F821 undefined name 'stats'
- Line 1081: F821 undefined name 'stats'
- Line 1083: F821 undefined name 'stats'
- Line 1138: F821 undefined name 'stats'
- Line 1139: F821 undefined name 'stats'
- Line 1140: F821 undefined name 'stats'
- Line 1141: F821 undefined name 'stats'
- Line 1142: F821 undefined name 'stats'
- Line 1143: F821 undefined name 'stats'
- Line 1144: F821 undefined name 'stats'
- Line 1145: F821 undefined name 'stats'

### src/piwardrive/ui/user_experience.py
- Line 193: F821 undefined name 'data'
- Line 194: F821 undefined name 'data'
- Line 197: F821 undefined name 'data'
- Line 218: F821 undefined name 'data'
- Line 696: F821 undefined name 'config'
- Line 700: F821 undefined name 'config'
- Line 701: F821 undefined name 'config'
- Line 757: F821 undefined name 'config'
- Line 781: F821 undefined name 'widget_config'
- Line 791: F821 undefined name 'widget_config'
- Line 1256: F821 undefined name 'data'
- Line 1261: F821 undefined name 'data'
- Line 1295: F821 undefined name 'data'

### src/piwardrive/data_processing/enhanced_processing.py
- Line 200: F821 undefined name 'lat'
- Line 200: F821 undefined name 'lon'
- Line 203: F821 undefined name 'lat'
- Line 205: F821 undefined name 'lon'
- Line 233: F821 undefined name 'filtered_data'
- Line 235: F821 undefined name 'filtered_data'
- Line 557: F821 undefined name 'enhanced_data'
- Line 559: F821 undefined name 'enhanced_data'
- Line 697: F821 undefined name 'description'

### src/piwardrive/routes/bluetooth.py
- Line 33: F821 undefined name 'result'
- Line 34: F821 undefined name 'result'
- Line 49: F821 undefined name 'result'
- Line 50: F821 undefined name 'result'

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 462: F821 undefined name 'AESGCM'
- Line 478: F821 undefined name 'AESGCM'
- Line 878: F821 undefined name 'stats'
- Line 891: F821 undefined name 'stats'
- Line 945: F821 undefined name 'result'
- Line 960: F821 undefined name 'result'
- Line 1373: F821 undefined name 'data'
- Line 1394: F821 undefined name 'result'
- Line 1417: F821 undefined name 'data'
- Line 1420: F821 undefined name 'data'

### src/piwardrive/logging/storage.py
- Line 204: F821 undefined name 'data'

### src/piwardrive/db_browser.py
- Line 36: F821 undefined name 'data'

### src/piwardrive/performance/realtime_optimizer.py
- Line 215: F821 undefined name 'stats'
- Line 218: F821 undefined name 'stats'
- Line 227: F821 undefined name 'stats'
- Line 357: F821 undefined name 'stats'
- Line 360: F821 undefined name 'stats'
- Line 369: F821 undefined name 'stats'
- Line 471: F821 undefined name 'optimized_data'
- Line 542: F821 undefined name 'optimized_data'
- Line 681: F821 undefined name 'stats'
- Line 682: F821 undefined name 'stats'
- Line 683: F821 undefined name 'stats'
- Line 685: F821 undefined name 'stats'

### src/piwardrive/main.py
- Line 182: F821 undefined name 'data'
- Line 228: F821 undefined name 'data'
- Line 229: F821 undefined name 'data'

### src/piwardrive/orientation_sensors.py
- Line 85: F821 undefined name 'data'
- Line 87: F821 undefined name 'data'

### src/piwardrive/geospatial/intelligence.py
- Line 174: F821 undefined name 'result'
- Line 176: F821 undefined name 'result'
- Line 187: F821 undefined name 'result'
- Line 188: F821 undefined name 'result'
- Line 189: F821 undefined name 'result'
- Line 230: F821 undefined name 'stats'
- Line 231: F821 undefined name 'stats'
- Line 234: F821 undefined name 'stats'
- Line 234: F821 undefined name 'stats'
- Line 235: F821 undefined name 'stats'
- Line 235: F821 undefined name 'stats'
- Line 815: F821 undefined name 'stats'
- Line 816: F821 undefined name 'stats'
- Line 817: F821 undefined name 'stats'

### src/piwardrive/visualization/advanced_viz.py
- Line 97: F821 undefined name 'data'
- Line 110: F821 undefined name 'data'
- Line 297: F821 undefined name 'ssid_data'
- Line 298: F821 undefined name 'ssid_data'
- Line 306: F821 undefined name 'ssid_data'
- Line 307: F821 undefined name 'ssid_data'
- Line 320: F821 undefined name 'ssid_data'
- Line 321: F821 undefined name 'ssid_data'
- Line 463: F821 undefined name 'analysis'
- Line 499: F821 undefined name 'stats'
- Line 501: F821 undefined name 'stats'
- Line 563: F821 undefined name 'total_aps'
- Line 566: F821 undefined name 'total_aps'
- Line 581: F821 undefined name 'analysis'
- Line 942: F821 undefined name 'data'
- Line 955: F821 undefined name 'data'

### src/piwardrive/api/common.py
- Line 47: F821 undefined name 'Any'
- Line 47: F821 undefined name 'Any'
- Line 47: F821 undefined name 'MetricsResult'
- Line 51: F821 undefined name 'Callable'
- Line 51: F821 undefined name 'Awaitable'
- Line 51: F821 undefined name 'MetricsResult'
- Line 67: F821 undefined name 'Any'
- Line 67: F821 undefined name 'Any'
- Line 71: F821 undefined name 'Callable'
- Line 71: F821 undefined name 'Awaitable'
- Line 76: F821 undefined name 'Any'
- Line 76: F821 undefined name 'Any'
- Line 80: F821 undefined name 'Callable'
- Line 80: F821 undefined name 'Awaitable'
- Line 83: F821 undefined name 'Callable'
- Line 88: F821 undefined name 'Any'
- Line 88: F821 undefined name 'Any'
- Line 92: F821 undefined name 'Callable'
- Line 92: F821 undefined name 'Awaitable'

### src/piwardrive/services/maintenance.py
- Line 93: F821 undefined name 'result'

### src/piwardrive/direction_finding/core.py
- Line 261: F821 undefined name 'result'
- Line 262: F821 undefined name 'result'
- Line 291: F821 undefined name 'result'
- Line 298: F821 undefined name 'result'
- Line 299: F821 undefined name 'result'
- Line 300: F821 undefined name 'result'
- Line 303: F821 undefined name 'result'
- Line 305: F821 undefined name 'result'

### src/piwardrive/navigation/offline_navigation.py
- Line 812: F821 undefined name 'data'
- Line 821: F821 undefined name 'data'
- Line 846: F821 undefined name 'data'
- Line 849: F821 undefined name 'data'

### src/piwardrive/mining/advanced_data_mining.py
- Line 119: F821 undefined name 'data'
- Line 125: F821 undefined name 'data'
- Line 126: F821 undefined name 'data'
- Line 159: F821 undefined name 'data'
- Line 159: F821 undefined name 'data'
- Line 159: F821 undefined name 'data'
- Line 163: F821 undefined name 'data'
- Line 178: F821 undefined name 'data'
- Line 182: F821 undefined name 'data'
- Line 206: F821 undefined name 'data'
- Line 220: F821 undefined name 'data'
- Line 224: F821 undefined name 'data'
- Line 258: F821 undefined name 'data'
- Line 1295: F821 undefined name 'stats'
- Line 1296: F821 undefined name 'stats'
- Line 1297: F821 undefined name 'stats'

### src/piwardrive/widgets/health_analysis.py
- Line 53: F821 undefined name 'stats'
- Line 54: F821 undefined name 'stats'
- Line 55: F821 undefined name 'stats'
- Line 56: F821 undefined name 'stats'

### tests/test_integration_comprehensive.py
- Line 126: F821 undefined name 'config'
- Line 140: F821 undefined name 'config'
- Line 160: F821 undefined name 'config'
- Line 177: F821 undefined name 'config'
- Line 195: F821 undefined name 'config'
- Line 198: F821 undefined name 'config'
- Line 216: F821 undefined name 'config'
- Line 241: F821 undefined name 'config'
- Line 256: F821 undefined name 'config'
- Line 276: F821 undefined name 'config'
- Line 293: F821 undefined name 'config'
- Line 424: F821 undefined name 'config'
- Line 437: F821 undefined name 'config'
- Line 474: F821 undefined name 'config'
- Line 509: F821 undefined name 'config'
- Line 528: F821 undefined name 'config'

### src/piwardrive/plugins/plugin_architecture.py
- Line 710: F821 undefined name 'viz_result'
- Line 716: F821 undefined name 'analysis_result'

### src/piwardrive/core/utils.py
- Line 237: F821 undefined name 'data'
- Line 238: F821 undefined name 'data'
- Line 245: F821 undefined name 'result'
- Line 250: F821 undefined name 'result'
- Line 255: F821 undefined name 'result'
- Line 389: F821 undefined name 'result'
- Line 463: F821 undefined name 'result'
- Line 464: F821 undefined name 'result'
- Line 644: F821 undefined name 'result'
- Line 645: F821 undefined name 'result'
- Line 1053: F821 undefined name 'data'
- Line 1055: F821 undefined name 'data'
- Line 1061: F821 undefined name 'data'
- Line 1063: F821 undefined name 'data'
- Line 1236: F821 undefined name 'data'

### src/piwardrive/widgets/health_status.py
- Line 44: F821 undefined name 'data'
- Line 47: F821 undefined name 'data'
- Line 48: F821 undefined name 'data'
- Line 51: F821 undefined name 'data'

### src/piwardrive/integrations/sigint_suite/dashboard/__init__.py
- Line 34: F821 undefined name 'data'
- Line 35: F821 undefined name 'data'
- Line 98: F821 undefined name 'data'
- Line 100: F821 undefined name 'data'

### src/piwardrive/widgets/orientation_widget.py
- Line 44: F821 undefined name 'data'
- Line 44: F821 undefined name 'data'
- Line 45: F821 undefined name 'data'

### src/sync.py
- Line 3: F403 'from piwardrive.sync import *' used; unable to detect undefined names

### src/piwardrive/scan_report.py
- Line 33: F821 undefined name 'data'
- Line 34: F821 undefined name 'data'
- Line 35: F821 undefined name 'data'

### tests/test_performance_comprehensive.py
- Line 150: F821 undefined name 'config'
- Line 185: F821 undefined name 'config'
- Line 219: F821 undefined name 'config'
- Line 291: F821 undefined name 'config'
- Line 322: F821 undefined name 'config'
- Line 344: F821 undefined name 'config'
- Line 374: F821 undefined name 'config'
- Line 446: F821 undefined name 'config'
- Line 464: F821 undefined name 'config'
- Line 485: F821 undefined name 'config'
- Line 516: F821 undefined name 'config'
- Line 516: F821 undefined name 'config'
- Line 516: F821 undefined name 'config'
- Line 673: F821 undefined name 'config'
- Line 734: F821 undefined name 'config'

### src/piwardrive/diagnostics.py
- Line 147: F821 undefined name 'data'
- Line 167: F821 undefined name 'stats'
- Line 176: F821 undefined name 'stats'
- Line 193: F821 undefined name 'stats'
- Line 194: F821 undefined name 'stats'
- Line 423: F821 undefined name 'result'

### tests/test_migrations_comprehensive.py
- Line 22: F821 undefined name 'BaseMigration'
- Line 29: F821 undefined name 'BaseMigration'
- Line 36: F821 undefined name 'BaseMigration'
- Line 44: F821 undefined name 'BaseMigration'
- Line 55: F821 undefined name 'ScanSessionsMigration'
- Line 61: F821 undefined name 'ScanSessionsMigration'
- Line 78: F821 undefined name 'ScanSessionsMigration'
- Line 105: F821 undefined name 'ScanSessionsMigration'
- Line 134: F821 undefined name 'BluetoothMigration'
- Line 140: F821 undefined name 'BluetoothMigration'
- Line 156: F821 undefined name 'BluetoothMigration'
- Line 184: F821 undefined name 'GPSTracksMigration'
- Line 190: F821 undefined name 'GPSTracksMigration'
- Line 206: F821 undefined name 'GPSTracksMigration'
- Line 235: F821 undefined name 'PerformanceIndexesMigration'
- Line 241: F821 undefined name 'PerformanceIndexesMigration'
- Line 278: F821 undefined name 'PerformanceIndexesMigration'
- Line 316: F821 undefined name 'MigrationRunner'
- Line 323: F821 undefined name 'MigrationRunner'
- Line 340: F821 undefined name 'MigrationRunner'
- Line 355: F821 undefined name 'MigrationRunner'
- Line 358: F821 undefined name 'ScanSessionsMigration'
- Line 376: F821 undefined name 'MigrationRunner'
- Line 379: F821 undefined name 'ScanSessionsMigration'
- Line 397: F821 undefined name 'MigrationRunner'
- Line 401: F821 undefined name 'ScanSessionsMigration'
- Line 402: F821 undefined name 'BluetoothMigration'
- Line 403: F821 undefined name 'GPSTracksMigration'
- Line 432: F821 undefined name 'MigrationRunner'
- Line 439: F821 undefined name 'ScanSessionsMigration'
- Line 461: F821 undefined name 'MigrationRunner'
- Line 464: F821 undefined name 'ScanSessionsMigration'
- Line 481: F821 undefined name 'MigrationRunner'
- Line 484: F821 undefined name 'ScanSessionsMigration'
- Line 516: F821 undefined name 'ScanSessionsMigration'
- Line 528: F821 undefined name 'ScanSessionsMigration'
- Line 540: F821 undefined name 'MigrationRunner'
- Line 548: F821 undefined name 'MigrationRunner'
- Line 565: F821 undefined name 'PerformanceIndexesMigration'
- Line 596: F821 undefined name 'ScanSessionsMigration'

### src/piwardrive/api/websockets/handlers.py
- Line 45: F821 undefined name 'data'
- Line 84: F821 undefined name 'data'
- Line 110: F821 undefined name 'data'
- Line 137: F821 undefined name 'data'

### tests/test_widget_manager.py
- Line 33: F821 undefined name 'widget'
- Line 43: F821 undefined name 'widget'
- Line 45: F821 undefined name 'widget'

### src/piwardrive/scheduler.py
- Line 53: F821 undefined name 'data'
- Line 53: F821 undefined name 'data'
- Line 130: F821 undefined name 'result'
- Line 131: F821 undefined name 'result'
- Line 159: F821 undefined name 'result'
- Line 160: F821 undefined name 'result'
- Line 213: F821 undefined name 'result'
- Line 214: F821 undefined name 'result'

### src/piwardrive/performance/db_optimizer.py
- Line 108: F821 undefined name 'stats'
- Line 115: F821 undefined name 'stats'
- Line 254: F821 undefined name 'result'
- Line 254: F821 undefined name 'result'
- Line 392: F821 undefined name 'result'
- Line 394: F821 undefined name 'result'

### src/piwardrive/analytics/predictive.py
- Line 90: F821 undefined name 'result'
- Line 91: F821 undefined name 'result'

### src/piwardrive/direction_finding/hardware.py
- Line 36: F821 undefined name 'result'
- Line 38: F821 undefined name 'result'
- Line 118: F821 undefined name 'result'
- Line 119: F821 undefined name 'result'
- Line 155: F821 undefined name 'result'
- Line 156: F821 undefined name 'result'
- Line 190: F821 undefined name 'result'
- Line 191: F821 undefined name 'result'
- Line 246: F821 undefined name 'result'
- Line 247: F821 undefined name 'result'
- Line 616: F821 undefined name 'data'

### src/piwardrive/routes/websocket.py
- Line 25: F821 undefined name 'data'
- Line 44: F821 undefined name 'data'

### src/piwardrive/jobs/maintenance_jobs.py
- Line 67: F821 undefined name 'result'
- Line 68: F821 undefined name 'result'

### src/piwardrive/widgets/db_stats.py
- Line 43: F821 undefined name 'result'
- Line 45: F821 undefined name 'result'
- Line 73: F821 undefined name 'stats'

### src/piwardrive/testing/automated_framework.py
- Line 232: F821 undefined name 'result'
- Line 421: F821 undefined name 'result'
- Line 454: F821 undefined name 'test_data'
- Line 457: F821 undefined name 'test_data'
- Line 473: F821 undefined name 'test_data'
- Line 630: F821 undefined name 'result'
- Line 793: F821 undefined name 'result'
- Line 828: F821 undefined name 'result'
- Line 855: F821 undefined name 'result'
- Line 856: F821 undefined name 'result'
- Line 861: F821 undefined name 'result'

### tests/test_cache_security_comprehensive.py
- Line 31: F821 undefined name 'CacheEntry'
- Line 40: F821 undefined name 'CacheEntry'
- Line 47: F821 undefined name 'CacheEntry'
- Line 54: F821 undefined name 'CacheEntry'
- Line 65: F821 undefined name 'LRUCache'
- Line 143: F821 undefined name 'LRUCache'
- Line 147: F821 undefined name 'save_cache'
- Line 154: F821 undefined name 'LRUCache'
- Line 158: F821 undefined name 'save_cache'
- Line 175: F821 undefined name 'load_cache'
- Line 177: F821 undefined name 'LRUCache'
- Line 182: F821 undefined name 'load_cache'
- Line 184: F821 undefined name 'LRUCache'
- Line 193: F821 undefined name 'load_cache'
- Line 195: F821 undefined name 'LRUCache'
- Line 230: F821 undefined name 'generate_api_key'
- Line 239: F821 undefined name 'validate_api_key'
- Line 246: F821 undefined name 'validate_api_key'
- Line 253: F821 undefined name 'validate_api_key'
- Line 259: F821 undefined name 'sanitize_input'
- Line 266: F821 undefined name 'sanitize_input'
- Line 274: F821 undefined name 'sanitize_input'
- Line 281: F821 undefined name 'get_csrf_token'
- Line 292: F821 undefined name 'validate_csrf_token'
- Line 298: F821 undefined name 'validate_csrf_token'
- Line 341: F821 undefined name 'LRUCache'
- Line 354: F821 undefined name 'LRUCache'
- Line 387: F821 undefined name 'generate_api_key'
- Line 390: F821 undefined name 'validate_api_key'
- Line 391: F821 undefined name 'validate_api_key'
- Line 406: F821 undefined name 'sanitize_input'

### src/piwardrive/routes/cellular.py
- Line 33: F821 undefined name 'result'
- Line 34: F821 undefined name 'result'
- Line 49: F821 undefined name 'result'
- Line 50: F821 undefined name 'result'

### src/piwardrive/map/vector_tile_customizer.py
- Line 94: F821 undefined name 'data'

### src/piwardrive/integrations/wigle.py
- Line 54: F821 undefined name 'data'

### src/piwardrive/api/system/endpoints.py
- Line 30: F821 undefined name 'service'
- Line 32: F821 undefined name 'service'
- Line 33: F821 undefined name 'service'
- Line 34: F821 undefined name 'service'
- Line 40: F821 undefined name 'service'
- Line 41: F821 undefined name 'service'
- Line 47: F821 undefined name 'service'
- Line 48: F821 undefined name 'service'
- Line 54: F821 undefined name 'service'
- Line 55: F821 undefined name 'service'
- Line 56: F821 undefined name 'service'
- Line 61: F821 undefined name 'service'
- Line 63: F821 undefined name 'service'
- Line 63: F821 undefined name 'service'
- Line 64: F821 undefined name 'data'
- Line 65: F821 undefined name 'data'
- Line 66: F821 undefined name 'data'
- Line 76: F821 undefined name 'service'
- Line 78: F821 undefined name 'service'
- Line 79: F821 undefined name 'service'
- Line 81: F821 undefined name 'service'
- Line 81: F821 undefined name 'service'
- Line 82: F821 undefined name 'service'
- Line 83: F821 undefined name 'service'
- Line 89: F821 undefined name 'service'
- Line 91: F821 undefined name 'service'
- Line 91: F821 undefined name 'service'
- Line 93: F821 undefined name 'service'
- Line 96: F821 undefined name 'service'
- Line 97: F821 undefined name 'service'
- Line 125: F821 undefined name 'service'
- Line 127: F821 undefined name 'service'
- Line 131: F821 undefined name 'service'
- Line 132: F821 undefined name 'data'
- Line 133: F821 undefined name 'data'
- Line 135: F821 undefined name 'data'
- Line 142: F821 undefined name 'service'
- Line 171: F821 undefined name 'service'
- Line 172: F821 undefined name 'service'
- Line 179: F821 undefined name 'service'
- Line 182: F821 undefined name 'service'
- Line 183: F821 undefined name 'result'
- Line 193: F821 undefined name 'service'
- Line 194: F821 undefined name 'service'
- Line 199: F821 undefined name 'service'
- Line 200: F821 undefined name 'service'
- Line 206: F821 undefined name 'service'
- Line 207: F821 undefined name 'service'
- Line 210: F821 undefined name 'data'
- Line 212: F821 undefined name 'data'
- Line 213: F821 undefined name 'data'
- Line 214: F821 undefined name 'data'
- Line 216: F821 undefined name 'service'
- Line 216: F821 undefined name 'data'
- Line 219: F821 undefined name 'service'
- Line 219: F821 undefined name 'service'
- Line 219: F821 undefined name 'data'
- Line 220: F821 undefined name 'data'
- Line 226: F821 undefined name 'service'
- Line 227: F821 undefined name 'service'
- Line 234: F821 undefined name 'service'
- Line 235: F821 undefined name 'service'
- Line 237: F821 undefined name 'service'
- Line 244: F821 undefined name 'service'
- Line 252: F821 undefined name 'service'
- Line 253: F821 undefined name 'service'
- Line 265: F821 undefined name 'service'
- Line 266: F821 undefined name 'service'
- Line 272: F821 undefined name 'service'
- Line 273: F821 undefined name 'service'
- Line 282: F821 undefined name 'service'
- Line 289: F821 undefined name 'service'
- Line 290: F821 undefined name 'service'
- Line 301: F821 undefined name 'service'
- Line 309: F821 undefined name 'service'
- Line 310: F821 undefined name 'service'
- Line 314: F821 undefined name 'service'
- Line 319: F821 undefined name 'service'
- Line 320: F821 undefined name 'service'
- Line 321: F821 undefined name 'service'
- Line 336: F821 undefined name 'service'

### src/piwardrive/direction_finding/integration.py
- Line 52: F821 undefined name 'config'

### src/piwardrive/integrations/sigint.py
- Line 17: F821 undefined name 'data'
- Line 18: F821 undefined name 'data'

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 66: F821 undefined name 'data'
- Line 68: F821 undefined name 'data'
- Line 70: F821 undefined name 'data'
- Line 72: F821 undefined name 'data'

### src/piwardrive/api/websockets/events.py
- Line 28: F821 undefined name 'data'

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 135: F821 undefined name 'data'
- Line 137: F821 undefined name 'data'

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 93: F821 undefined name 'data'
- Line 95: F821 undefined name 'data'

### src/piwardrive/api/performance_dashboard.py
- Line 108: F821 undefined name 'stats'
- Line 134: F821 undefined name 'stats'
- Line 135: F821 undefined name 'table_stats'
- Line 136: F821 undefined name 'table_stats'
- Line 138: F821 undefined name 'table_stats'
- Line 140: F821 undefined name 'table_stats'
- Line 143: F821 undefined name 'stats'
- Line 149: F821 undefined name 'stats'
- Line 151: F821 undefined name 'stats'
- Line 157: F821 undefined name 'stats'
- Line 157: F821 undefined name 'realtime_stats'
- Line 159: F821 undefined name 'stats'
- Line 161: F821 undefined name 'stats'
- Line 460: F821 undefined name 'stats'

### code_analysis.py
- Line 122: 'data' might be undefined
- Line 124: 'config' might be undefined

## Unused Variables/Imports

### src/piwardrive/hardware/enhanced_hardware.py
- Line 14: F401 'abc.ABC' imported but unused
- Line 14: F401 'abc.abstractmethod' imported but unused
- Line 16: F401 'datetime.timedelta' imported but unused
- Line 18: F401 'typing.Tuple' imported but unused
- Line 18: F401 'typing.Union' imported but unused
- Line 31: F401 'usb.core' imported but unused

### tests/test_direction_finding.py
- Line 1: F401 'logging' imported but unused
- Line 10: F401 'unittest.mock.MagicMock' imported but unused
- Line 15: F401 'piwardrive.direction_finding.AntennaArrayManager' imported but unused
- Line 15: F401 'piwardrive.direction_finding.WiFiAdapterManager' imported but unused
- Line 15: F401 'piwardrive.direction_finding.config_manager' imported but unused
- Line 15: F401 'piwardrive.direction_finding.get_df_config' imported but unused
- Line 15: F401 'piwardrive.direction_finding.set_df_algorithm' imported but unused

### tests/test_migrations_fixed.py
- Line 11: F401 'unittest.mock.patch' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused

### test_imports.py
- Line 6: F401 'time' imported but unused
- Line 21: F401 'piwardrive.core.config.Config' imported but unused
- Line 25: F401 'piwardrive.core.persistence.AppState' imported but unused
- Line 29: F401 'piwardrive.main.PiWardriveApp' imported but unused

### src/piwardrive/logging/filters.py
- Line 5: F401 'typing.Optional' imported but unused

### tests/test_sigint_scanners_basic.py
- Line 3: F401 'piwardrive.sigint_suite.bluetooth.scanner.BluetoothDevice' imported but unused

### tests/test_calibrate_orientation.py
- Line 2: F401 'logging' imported but unused

### fix_issues.py
- Line 7: F401 'typing.List' imported but unused
- Line 7: F401 'typing.Tuple' imported but unused

### tests/performance/test_performance_infrastructure.py
- Line 17: F401 'typing.Tuple' imported but unused

### tests/test_security_system.py
- Line 8: F401 'unittest.mock.mock_open' imported but unused

### src/piwardrive/reporting/professional.py
- Line 9: F401 'datetime.timedelta' imported but unused

### tests/test_service_api_fixed_v2.py
- Line 6: F401 'json' imported but unused
- Line 9: F401 'unittest.mock.MagicMock' imported but unused
- Line 9: F401 'unittest.mock.AsyncMock' imported but unused
- Line 14: F401 'typing.Any' imported but unused
- Line 14: F401 'typing.Dict' imported but unused
- Line 14: F401 'typing.List' imported but unused

### src/piwardrive/performance/async_optimizer.py
- Line 15: F401 'typing.Union' imported but unused

### tests/test_jwt_utils_fixed.py
- Line 15: F401 'unittest.mock.MagicMock' imported but unused
- Line 16: F401 'datetime.datetime' imported but unused
- Line 16: F401 'datetime.timedelta' imported but unused
- Line 18: F401 'pytest' imported but unused

### src/piwardrive/services/data_export.py
- Line 5: F401 'importlib.resources' imported but unused
- Line 6: F401 'typing.Sequence' imported but unused

### tests/test_critical_paths.py
- Line 9: F401 'unittest.mock.Mock' imported but unused
- Line 9: F401 'unittest.mock.MagicMock' imported but unused

### tests/test_async_scheduler.py
- Line 4: F401 'types.ModuleType' imported but unused
- Line 4: F401 'types.SimpleNamespace' imported but unused

### tests/test_service_simple.py
- Line 10: F401 'unittest.mock' imported but unused
- Line 187: F401 'fastapi.FastAPI' imported but unused
- Line 188: F401 'fastapi.middleware.cors.CORSMiddleware' imported but unused
- Line 189: F401 'os' imported but unused

### src/piwardrive/services/cluster_manager.py
- Line 10: F401 'typing.Iterable' imported but unused

### src/piwardrive/protocols/multi_protocol.py
- Line 10: F401 'collections.defaultdict' imported but unused
- Line 14: F401 'typing.Tuple' imported but unused

### tests/test_resource_manager.py
- Line 2: F401 'pathlib.Path' imported but unused

### tests/test_unit_enhanced.py
- Line 1: F401 'logging' imported but unused
- Line 17: F401 'contextlib.contextmanager' imported but unused
- Line 18: F401 'pathlib.Path' imported but unused
- Line 19: F401 'unittest.mock.Mock' imported but unused
- Line 19: F401 'unittest.mock.patch' imported but unused
- Line 29: F401 'src.logging.LoggingManager' imported but unused

### src/piwardrive/ui/user_experience.py
- Line 13: F401 'abc.ABC' imported but unused
- Line 13: F401 'abc.abstractmethod' imported but unused
- Line 17: F401 'typing.Tuple' imported but unused
- Line 21: F401 'flask.session' imported but unused
- Line 30: F401 'flask_socketio.emit' imported but unused
- Line 30: F401 'flask_socketio.join_room' imported but unused
- Line 30: F401 'flask_socketio.leave_room' imported but unused
- Line 38: F401 'tkinter.filedialog' imported but unused
- Line 38: F401 'tkinter.messagebox' imported but unused
- Line 38: F401 'tkinter.ttk' imported but unused
- Line 295: F401 '..hardware.enhanced_hardware.EnhancedGPSManager' imported but unused

### src/piwardrive/routes/analytics.py
- Line 5: F401 'fastapi.HTTPException' imported but unused

### src/piwardrive/data_processing/enhanced_processing.py
- Line 16: F401 'dataclasses.asdict' imported but unused
- Line 18: F401 'pathlib.Path' imported but unused
- Line 19: F401 'typing.Optional' imported but unused
- Line 19: F401 'typing.Tuple' imported but unused
- Line 25: F401 'sklearn.cluster.DBSCAN' imported but unused
- Line 26: F401 'sklearn.preprocessing.StandardScaler' imported but unused

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 26: F401 'collections.deque' imported but unused
- Line 29: F401 'datetime.timedelta' imported but unused
- Line 31: F401 'pathlib.Path' imported but unused
- Line 32: F401 'typing.AsyncGenerator' imported but unused
- Line 32: F401 'typing.Optional' imported but unused
- Line 32: F401 'typing.Set' imported but unused
- Line 32: F401 'typing.Union' imported but unused
- Line 49: F401 'sklearn.cluster.DBSCAN' imported but unused
- Line 51: F401 'sklearn.preprocessing.StandardScaler' imported but unused

### tests/test_vendor_lookup.py
- Line 6: F401 'piwardrive.sigint_suite.paths' imported but unused

### src/piwardrive/integration/system_orchestration.py
- Line 24: F401 'collections.deque' imported but unused
- Line 28: F401 'pathlib.Path' imported but unused
- Line 29: F401 'typing.AsyncGenerator' imported but unused
- Line 29: F401 'typing.Set' imported but unused
- Line 29: F401 'typing.Tuple' imported but unused
- Line 29: F401 'typing.Union' imported but unused
- Line 44: F401 'celery.Celery' imported but unused
- Line 45: F401 'flask.request' imported but unused
- Line 46: F401 'flask_restx.Resource' imported but unused
- Line 46: F401 'flask_restx.fields' imported but unused
- Line 48: F401 'sqlalchemy.Column' imported but unused
- Line 48: F401 'sqlalchemy.DateTime' imported but unused
- Line 48: F401 'sqlalchemy.Float' imported but unused
- Line 48: F401 'sqlalchemy.Integer' imported but unused
- Line 48: F401 'sqlalchemy.String' imported but unused
- Line 48: F401 'sqlalchemy.Text' imported but unused
- Line 48: F401 'sqlalchemy.create_engine' imported but unused
- Line 49: F401 'sqlalchemy.ext.declarative.declarative_base' imported but unused
- Line 50: F401 'sqlalchemy.orm.sessionmaker' imported but unused

### src/piwardrive/database_service.py
- Line 12: F401 '.db.MySQLAdapter' imported but unused
- Line 12: F401 '.db.PostgresAdapter' imported but unused

### src/piwardrive/ml/threat_detection.py
- Line 16: F401 'datetime.timedelta' imported but unused
- Line 18: F401 'typing.Tuple' imported but unused
- Line 21: F401 'sklearn.cluster.DBSCAN' imported but unused
- Line 22: F401 'sklearn.decomposition.PCA' imported but unused

### comprehensive_fix.py
- Line 9: F401 'typing.Dict' imported but unused
- Line 9: F401 'typing.List' imported but unused
- Line 9: F401 'typing.Tuple' imported but unused

### tests/test_cache.py
- Line 12: F401 'unittest.mock.MagicMock' imported but unused

### src/piwardrive/services/monitoring.py
- Line 8: F401 'typing.Iterable' imported but unused
- Line 8: F401 'typing.Mapping' imported but unused

### tests/test_main_simple.py
- Line 9: F401 'pathlib.Path' imported but unused
- Line 59: F401 'piwardrive.di.Container' imported but unused

### tests/test_core_persistence.py
- Line 6: F401 'os' imported but unused
- Line 10: F401 'tempfile' imported but unused
- Line 12: F401 'unittest.mock.Mock' imported but unused
- Line 12: F401 'unittest.mock.AsyncMock' imported but unused
- Line 14: F401 'typing.List' imported but unused
- Line 14: F401 'typing.Dict' imported but unused
- Line 14: F401 'typing.Any' imported but unused
- Line 16: F401 'piwardrive.core.persistence._db_path' imported but unused

### tests/test_localization.py
- Line 11: F401 'tempfile' imported but unused

### src/piwardrive/performance/realtime_optimizer.py
- Line 14: F401 'contextlib.asynccontextmanager' imported but unused
- Line 15: F401 'dataclasses.asdict' imported but unused
- Line 16: F401 'typing.List' imported but unused
- Line 17: F401 'weakref.WeakSet' imported but unused

### tests/test_cache_security_fixed.py
- Line 8: F401 'pytest' imported but unused

### tests/test_utils_comprehensive.py
- Line 15: F401 'unittest.mock.MagicMock' imported but unused
- Line 16: F401 'dataclasses.dataclass' imported but unused
- Line 24: F401 'piwardrive.utils.format_error' imported but unused
- Line 24: F401 'piwardrive.utils.report_error' imported but unused

### tests/test_service_direct.py
- Line 5: F401 'unittest.mock.MagicMock' imported but unused

### fix_remaining_syntax.py
- Line 6: F401 'os' imported but unused
- Line 8: F401 'ast' imported but unused

### src/piwardrive/api/system/monitoring.py
- Line 4: F401 'logging' imported but unused

### src/piwardrive/geospatial/intelligence.py
- Line 9: F401 'datetime.timedelta' imported but unused
- Line 11: F401 'typing.NamedTuple' imported but unused
- Line 15: F401 'scipy.spatial.distance.cdist' imported but unused

### src/piwardrive/logging/levels.py
- Line 3: F401 'typing.Optional' imported but unused
- Line 3: F401 'typing.Set' imported but unused

### tests/test_network_fingerprinting_integration.py
- Line 2: F401 'types.SimpleNamespace' imported but unused

### tests/test_service_comprehensive.py
- Line 9: F401 'asyncio' imported but unused
- Line 11: F401 'unittest.mock' imported but unused
- Line 12: F401 'unittest.mock.AsyncMock' imported but unused
- Line 12: F401 'unittest.mock.MagicMock' imported but unused
- Line 14: F401 'tempfile' imported but unused
- Line 15: F401 'os' imported but unused
- Line 226: F401 'src.piwardrive.service' imported but unused

### fix_quality_issues.py
- Line 8: F401 'typing.Dict' imported but unused

### tests/test_error_reporting.py
- Line 1: F401 'logging' imported but unused

### src/piwardrive/visualization/advanced_viz.py
- Line 11: F401 'datetime.timedelta' imported but unused
- Line 13: F401 'typing.Optional' imported but unused
- Line 13: F401 'typing.Tuple' imported but unused
- Line 21: F401 'reportlab.lib.pagesizes.letter' imported but unused
- Line 24: F401 'reportlab.platypus.Image' imported but unused
- Line 33: F401 'scipy.spatial.distance.cdist' imported but unused
- Line 35: F401 'sklearn.preprocessing.StandardScaler' imported but unused

### tests/test_persistence_comprehensive.py
- Line 9: F401 'asyncio' imported but unused
- Line 11: F401 'unittest.mock.Mock' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused

### tests/logging/test_structured_logger.py
- Line 8: F401 'unittest.mock.MagicMock' imported but unused
- Line 8: F401 'unittest.mock.mock_open' imported but unused
- Line 549: F401 'queue.SimpleQueue' imported but unused
- Line 550: F401 'logging.handlers.QueueListener' imported but unused

### tests/test_api_service.py
- Line 6: F401 'os' imported but unused
- Line 7: F401 'json' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'unittest.mock.Mock' imported but unused
- Line 13: F401 'fastapi.status' imported but unused
- Line 14: F401 'typing.Dict' imported but unused
- Line 14: F401 'typing.Any' imported but unused
- Line 14: F401 'typing.List' imported but unused

### tests/test_service_layer.py
- Line 6: F401 'asyncio' imported but unused
- Line 7: F401 'json' imported but unused
- Line 17: F401 'piwardrive.errors.ConfigError' imported but unused

### src/piwardrive/direction_finding/core.py
- Line 155: F401 '.algorithms.PathLossCalculator' imported but unused
- Line 155: F401 '.algorithms.SignalMapper' imported but unused

### tests/test_tile_maintenance.py
- Line 33: F401 'piwardrive.scheduler.PollScheduler' imported but unused

### scripts/test_database_functions.py
- Line 12: F401 'typing.Any' imported but unused
- Line 12: F401 'typing.Dict' imported but unused
- Line 12: F401 'typing.List' imported but unused
- Line 18: F401 'piwardrive.core.persistence.save_cellular_detections' imported but unused
- Line 18: F401 'piwardrive.core.persistence.save_suspicious_activities' imported but unused

### src/piwardrive/navigation/offline_navigation.py
- Line 23: F401 'datetime.timedelta' imported but unused
- Line 26: F401 'typing.Set' imported but unused
- Line 26: F401 'typing.Tuple' imported but unused

### scripts/df_integration_demo.py
- Line 15: F401 'piwardrive.direction_finding.DFEngine' imported but unused
- Line 15: F401 'piwardrive.direction_finding.DFIntegrationManager' imported but unused
- Line 15: F401 'piwardrive.direction_finding.RSSTriangulation' imported but unused
- Line 15: F401 'piwardrive.direction_finding.get_df_config' imported but unused

### src/piwardrive/logging/dynamic_config.py
- Line 5: F401 'logging' imported but unused

### tests/test_widget_cache.py
- Line 3: F401 'pathlib.Path' imported but unused
- Line 4: F401 'types.ModuleType' imported but unused

### src/piwardrive/mining/advanced_data_mining.py
- Line 16: F401 'sklearn.decomposition.PCA' imported but unused

### tests/test_vacuum_script.py
- Line 2: F401 'types.SimpleNamespace' imported but unused

### src/piwardrive/logging/structured_logger.py
- Line 23: F401 'typing.Union' imported but unused

### src/piwardrive/visualization/advanced_visualization.py
- Line 27: F401 'typing.Set' imported but unused
- Line 27: F401 'typing.Union' imported but unused
- Line 35: F401 'matplotlib.collections.LineCollection' imported but unused
- Line 36: F401 'matplotlib.patches.Circle' imported but unused
- Line 36: F401 'matplotlib.patches.Polygon' imported but unused
- Line 36: F401 'matplotlib.patches.Rectangle' imported but unused
- Line 37: F401 'plotly.subplots.make_subplots' imported but unused

### tests/test_integration_comprehensive.py
- Line 1: F401 'logging' imported but unused
- Line 19: F401 'pathlib.Path' imported but unused

### src/piwardrive/plugins/plugin_architecture.py
- Line 28: F401 'typing.Optional' imported but unused
- Line 28: F401 'typing.Set' imported but unused
- Line 28: F401 'typing.Type' imported but unused

### scripts/monitoring_service.py
- Line 10: F401 'email.mime.multipart.MIMEMultipart' imported but unused
- Line 11: F401 'email.mime.text.MIMEText' imported but unused
- Line 13: F401 'typing.Optional' imported but unused

### src/piwardrive/enhanced/critical_additions.py
- Line 21: F401 'concurrent.futures.ThreadPoolExecutor' imported but unused
- Line 23: F401 'datetime.timedelta' imported but unused
- Line 25: F401 'pathlib.Path' imported but unused
- Line 26: F401 'typing.AsyncGenerator' imported but unused
- Line 26: F401 'typing.Optional' imported but unused
- Line 26: F401 'typing.Tuple' imported but unused
- Line 26: F401 'typing.Union' imported but unused

### tests/test_jwt_utils_comprehensive.py
- Line 12: F401 'unittest.mock' imported but unused
- Line 13: F401 'unittest.mock.Mock' imported but unused

### tests/test_main_application_comprehensive.py
- Line 6: F401 'asyncio' imported but unused
- Line 9: F401 'tempfile' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused
- Line 11: F401 'unittest.mock.call' imported but unused
- Line 12: F401 'dataclasses.asdict' imported but unused
- Line 15: F401 'piwardrive.config.load_config' imported but unused
- Line 15: F401 'piwardrive.config.save_config' imported but unused
- Line 16: F401 'piwardrive.persistence.load_app_state' imported but unused
- Line 16: F401 'piwardrive.persistence.save_app_state' imported but unused
- Line 19: F401 'piwardrive.security.hash_password' imported but unused

### src/piwardrive/signal/rf_spectrum.py
- Line 10: F401 'typing.NamedTuple' imported but unused

### src/sync.py
- Line 3: F401 'piwardrive.sync.*' imported but unused

### tests/test_performance_comprehensive.py
- Line 1: F401 'logging' imported but unused
- Line 17: F401 'concurrent.futures.ProcessPoolExecutor' imported but unused
- Line 20: F401 'pathlib.Path' imported but unused
- Line 21: F401 'typing.Optional' imported but unused
- Line 22: F401 'unittest.mock.Mock' imported but unused
- Line 22: F401 'unittest.mock.patch' imported but unused
- Line 30: F401 'src.data.aggregation.AggregationService' imported but unused
- Line 35: F401 'src.service.PiWardriveService' imported but unused

### src/piwardrive/diagnostics.py
- Line 9: F401 'logging' imported but unused

### scripts/dependency_audit.py
- Line 23: F401 'pathlib.Path' imported but unused

### comprehensive_code_analyzer.py
- Line 8: F401 'os' imported but unused
- Line 10: F401 'sys' imported but unused
- Line 12: F401 'typing.Set' imported but unused
- Line 12: F401 'typing.Tuple' imported but unused
- Line 13: F401 'subprocess' imported but unused
- Line 14: F401 'json' imported but unused

### tests/test_migrations_comprehensive.py
- Line 7: F401 'asyncio' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused
- Line 14: F401 'importlib' imported but unused

### scripts/compare_performance.py
- Line 13: F401 'pathlib.Path' imported but unused
- Line 14: F401 'typing.Tuple' imported but unused

### src/piwardrive/api/websockets/handlers.py
- Line 8: F401 'typing.Any' imported but unused

### tests/models/test_api_models.py
- Line 10: F401 'datetime.datetime' imported but unused
- Line 12: F401 'typing.Any' imported but unused
- Line 12: F401 'typing.Dict' imported but unused

### fix_syntax_errors.py
- Line 8: F401 'sys' imported but unused

### tests/test_main_application_fixed.py
- Line 8: F401 'unittest.mock.MagicMock' imported but unused
- Line 8: F401 'unittest.mock.AsyncMock' imported but unused
- Line 9: F401 'asyncio' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'tempfile' imported but unused
- Line 12: F401 'shutil' imported but unused
- Line 271: F401 'piwardrive.main' imported but unused
- Line 379: F401 'piwardrive.main' imported but unused

### tests/test_service_api.py
- Line 6: F401 'json' imported but unused
- Line 9: F401 'unittest.mock.MagicMock' imported but unused
- Line 9: F401 'unittest.mock.AsyncMock' imported but unused
- Line 10: F401 'fastapi.testclient.TestClient' imported but unused
- Line 11: F401 'fastapi.HTTPException' imported but unused
- Line 12: F401 'typing.Any' imported but unused
- Line 12: F401 'typing.Dict' imported but unused
- Line 12: F401 'typing.List' imported but unused
- Line 371: F401 'fastapi.HTTPException' imported but unused

### src/piwardrive/performance/db_optimizer.py
- Line 11: F401 'contextlib.asynccontextmanager' imported but unused

### scripts/simple_db_check.py
- Line 10: F401 'typing.List' imported but unused

### tests/test_fastjson.py
- Line 12: F401 'typing.Any' imported but unused
- Line 12: F401 'typing.Dict' imported but unused
- Line 12: F401 'typing.List' imported but unused

### src/piwardrive/api/auth/endpoints.py
- Line 19: F401 '.dependencies.AUTH_DEP' imported but unused

### tests/test_service_api_fixed.py
- Line 6: F401 'json' imported but unused
- Line 9: F401 'unittest.mock.MagicMock' imported but unused
- Line 9: F401 'unittest.mock.AsyncMock' imported but unused
- Line 14: F401 'typing.Any' imported but unused
- Line 14: F401 'typing.Dict' imported but unused
- Line 14: F401 'typing.List' imported but unused

### tests/test_service_direct_import.py
- Line 10: F401 'unittest.mock' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused

### src/piwardrive/direction_finding/hardware.py
- Line 12: F401 'pathlib.Path' imported but unused

### src/piwardrive/logging/__init__.py
- Line 1: F401 'logging' imported but unused

### tests/test_exception_handler.py
- Line 3: F401 'logging' imported but unused

### src/piwardrive/api/logging_control.py
- Line 1: F401 'logging' imported but unused

### tests/test_export.py
- Line 3: F401 'types.ModuleType' imported but unused
- Line 3: F401 'types.SimpleNamespace' imported but unused

### scripts/performance_monitor.py
- Line 15: F401 'dataclasses.asdict' imported but unused
- Line 16: F401 'datetime.timedelta' imported but unused
- Line 19: F401 'pathlib.Path' imported but unused
- Line 20: F401 'typing.Tuple' imported but unused

### scripts/performance_cli.py
- Line 15: F401 'typing.Any' imported but unused
- Line 15: F401 'typing.Dict' imported but unused

### tests/test_performance_dashboard_integration.py
- Line 5: F401 'unittest.mock.MagicMock' imported but unused

### src/piwardrive/widgets/cpu_temp_graph.py
- Line 5: F401 'piwardrive.localization._' imported but unused

### tests/test_scheduler_tasks.py
- Line 6: F401 'os' imported but unused
- Line 9: F401 'threading' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.call' imported but unused
- Line 12: F401 'datetime.datetime' imported but unused
- Line 12: F401 'datetime.timedelta' imported but unused
- Line 13: F401 'typing.Dict' imported but unused
- Line 13: F401 'typing.Any' imported but unused
- Line 13: F401 'typing.List' imported but unused
- Line 13: F401 'typing.Callable' imported but unused
- Line 15: F401 'piwardrive.scheduler.ScheduledTask' imported but unused

### src/piwardrive/direction_finding/__init__.py
- Line 34: F401 '.integration.configure_df' imported but unused

### src/piwardrive/unified_platform.py
- Line 26: F401 'collections.defaultdict' imported but unused
- Line 28: F401 'datetime.timedelta' imported but unused
- Line 31: F401 'typing.Callable' imported but unused

### src/piwardrive/testing/automated_framework.py
- Line 14: F401 'collections.defaultdict' imported but unused
- Line 16: F401 'datetime.timedelta' imported but unused
- Line 18: F401 'typing.Tuple' imported but unused

### tests/test_cache_security_comprehensive.py
- Line 8: F401 'unittest.mock.MagicMock' imported but unused
- Line 8: F401 'unittest.mock.mock_open' imported but unused
- Line 8: F401 'unittest.mock.AsyncMock' imported but unused
- Line 10: F401 'pytest' imported but unused
- Line 12: F401 'src.piwardrive.cache.RedisCache' imported but unused
- Line 13: F401 'src.piwardrive.security.sanitize_path' imported but unused
- Line 13: F401 'src.piwardrive.security.validate_service_name' imported but unused
- Line 13: F401 'src.piwardrive.security.validate_filename' imported but unused
- Line 13: F401 'src.piwardrive.security.sanitize_filename' imported but unused
- Line 13: F401 'src.piwardrive.security.encrypt_data' imported but unused
- Line 13: F401 'src.piwardrive.security.decrypt_data' imported but unused
- Line 13: F401 'src.piwardrive.security.hash_secret' imported but unused

### src/piwardrive/integrations/sigint_suite/cellular/utils.py
- Line 7: F401 'typing.List' imported but unused
- Line 7: F401 'typing.Tuple' imported but unused

### tests/test_core_config.py
- Line 9: F401 'tempfile' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'unittest.mock.Mock' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 12: F401 'dataclasses.asdict' imported but unused
- Line 13: F401 'typing.Dict' imported but unused
- Line 13: F401 'typing.Any' imported but unused
- Line 15: F401 'piwardrive.core.config.get_config_path' imported but unused
- Line 15: F401 'piwardrive.core.config.CONFIG_DIR' imported but unused
- Line 15: F401 'piwardrive.core.config.CONFIG_PATH' imported but unused
- Line 15: F401 'piwardrive.core.config.PROFILES_DIR' imported but unused
- Line 15: F401 'piwardrive.core.config.ACTIVE_PROFILE_FILE' imported but unused

### tests/test_interfaces.py
- Line 10: F401 'typing.Dict' imported but unused

### tests/test_scheduler_system.py
- Line 8: F401 'unittest.mock.MagicMock' imported but unused
- Line 9: F401 'datetime.timedelta' imported but unused
- Line 18: F401 'piwardrive.errors.ConfigError' imported but unused

### tests/test_core_application.py
- Line 8: F401 'tempfile' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.call' imported but unused
- Line 12: F401 'dataclasses.asdict' imported but unused
- Line 15: F401 'piwardrive.config.CONFIG_DIR' imported but unused

### src/piwardrive/widgets/disk_trend.py
- Line 5: F401 'piwardrive.localization._' imported but unused

### tests/staging/test_staging_environment.py
- Line 14: F401 'typing.Any' imported but unused
- Line 14: F401 'typing.List' imported but unused

### tests/test_main_application.py
- Line 8: F401 'unittest.mock.MagicMock' imported but unused
- Line 9: F401 'pathlib.Path' imported but unused

### src/piwardrive/performance/optimization.py
- Line 29: F401 'collections.defaultdict' imported but unused
- Line 30: F401 'concurrent.futures.ProcessPoolExecutor' imported but unused
- Line 35: F401 'typing.Union' imported but unused

### src/piwardrive/api/system/endpoints.py
- Line 3: F401 'logging' imported but unused
- Line 11: F401 'pathlib.Path' imported but unused
- Line 14: F401 'fastapi.Request' imported but unused
- Line 15: F401 'fastapi.responses.StreamingResponse' imported but unused
- Line 20: F401 'piwardrive.security.verify_password' imported but unused

### comprehensive_qa_fix.py
- Line 11: F401 'typing.Dict' imported but unused
- Line 11: F401 'typing.List' imported but unused
- Line 11: F401 'typing.Set' imported but unused

### src/piwardrive/direction_finding/integration.py
- Line 13: F401 '.config.DFConfiguration' imported but unused

### tests/test_widget_system_comprehensive.py
- Line 8: F401 'tempfile' imported but unused
- Line 9: F401 'os' imported but unused
- Line 10: F401 'pathlib.Path' imported but unused
- Line 11: F401 'unittest.mock.MagicMock' imported but unused
- Line 11: F401 'unittest.mock.AsyncMock' imported but unused
- Line 16: F401 'piwardrive.memory_monitor.MemoryMonitor' imported but unused
- Line 17: F401 'piwardrive.resource_manager.ResourceManager' imported but unused

### src/piwardrive/api/demographics/__init__.py
- Line 1: F401 '.endpoints.router' imported but unused

### src/piwardrive/error_middleware.py
- Line 5: F401 'logging' imported but unused

### tests/test_route_prefetch.py
- Line 23: F401 'piwardrive.route_prefetch' imported but unused

### tests/test_tower_tracking.py
- Line 2: F401 'logging' imported but unused

### tests/test_service.py
- Line 8: F401 'typing.Any' imported but unused

### tests/test_widget_system.py
- Line 6: F401 'json' imported but unused
- Line 7: F401 'unittest.mock.MagicMock' imported but unused
- Line 8: F401 'pathlib.Path' imported but unused
- Line 15: F401 'piwardrive.widget_manager.Widget' imported but unused
- Line 17: F401 'piwardrive.errors.ConfigError' imported but unused

### src/piwardrive/api/performance_dashboard.py
- Line 11: F401 'typing.Dict' imported but unused
- Line 11: F401 'typing.List' imported but unused
- Line 19: F401 'piwardrive.performance.db_optimizer.run_performance_analysis' imported but unused

### code_analysis.py
- Line 8: F401 'os' imported but unused
- Line 10: F401 'sys' imported but unused
- Line 12: F401 'typing.Tuple' imported but unused

## Import Issues

### src/piwardrive/data_sink.py
- Line 9: Relative import without module

### src/piwardrive/database_service.py
- Line 11: Relative import without module

### src/piwardrive/aggregation_service.py
- Line 20: Relative import without module

### src/piwardrive/integrations/sigint_suite/__init__.py
- Line 9: Relative import without module

### src/piwardrive/persistence.py
- Line 13: Relative import without module

### src/piwardrive/core/utils.py
- Line 34: Relative import without module

### src/piwardrive/integrations/sigint_suite/dashboard/__init__.py
- Line 20: Relative import without module

### src/piwardrive/scan_report.py
- Line 13: Relative import without module

### src/piwardrive/scheduler.py
- Line 15: Relative import without module

### src/piwardrive/__init__.py
- Line 16: Relative import without module

### src/piwardrive/widget_manager.py
- Line 21: Relative import without module

### src/piwardrive/migrations/runner.py
- Line 50: Relative import without module
- Line 71: Relative import without module

## Missing Docstrings

### src/piwardrive/hardware/enhanced_hardware.py
- Line 61: Missing docstring for functiondef 'to_dict'
- Line 84: Missing docstring for functiondef 'to_dict'
- Line 115: Missing docstring for functiondef 'to_dict'
- Line 130: Missing docstring for functiondef '__init__'
- Line 384: Missing docstring for functiondef '__init__'
- Line 595: Missing docstring for functiondef '__init__'
- Line 829: Missing docstring for functiondef '__init__'
- Line 990: Missing docstring for functiondef '__init__'

### tests/test_route_optimizer.py
- Line 6: Missing docstring for functiondef 'test_suggest_route_empty_returns_empty'
- Line 10: Missing docstring for functiondef 'test_suggest_route_unvisited_cells'

### tests/test_compute_health_stats_empty.py
- Line 19: Missing docstring for functiondef 'test_compute_health_stats_empty'

### tests/test_gpsd_client_async_more.py
- Line 6: Missing docstring for functiondef 'run'
- Line 10: Missing docstring for functiondef 'test_get_position_async'
- Line 20: Missing docstring for functiondef 'test_get_accuracy_async'
- Line 30: Missing docstring for functiondef 'test_get_fix_quality_async'
- Line 40: Missing docstring for functiondef 'test_async_methods_none'
- Line 13: Missing docstring for asyncfunctiondef 'fake_poll'
- Line 23: Missing docstring for asyncfunctiondef 'fake_poll'
- Line 33: Missing docstring for asyncfunctiondef 'fake_poll'
- Line 43: Missing docstring for asyncfunctiondef 'fake_poll'

### tests/test_direction_finding.py
- Line 469: Missing docstring for functiondef 'test_callback'

### tests/test_migrations_fixed.py
- Line 20: Missing docstring for classdef 'BaseMigration'
- Line 33: Missing docstring for asyncfunctiondef 'test_apply'
- Line 41: Missing docstring for classdef 'TestMigration'
- Line 60: Missing docstring for asyncfunctiondef 'test_migration'
- Line 392: Missing docstring for classdef 'MigrationRunner'
- Line 23: Missing docstring for asyncfunctiondef 'apply'
- Line 26: Missing docstring for asyncfunctiondef 'rollback'
- Line 44: Missing docstring for asyncfunctiondef 'apply'
- Line 53: Missing docstring for asyncfunctiondef 'rollback'
- Line 393: Missing docstring for functiondef '__init__'
- Line 397: Missing docstring for functiondef 'add_migration'
- Line 400: Missing docstring for asyncfunctiondef 'get_current_version'
- Line 404: Missing docstring for asyncfunctiondef 'run_migrations'

### test_imports.py
- Line 9: Missing docstring for functiondef 'timeout_handler'

### src/piwardrive/logging/filters.py
- Line 11: Missing docstring for functiondef '__init__'
- Line 44: Missing docstring for functiondef '__init__'
- Line 73: Missing docstring for functiondef '__init__'

### tests/test_circuit_breaker.py
- Line 9: Missing docstring for asyncfunctiondef 'test_circuit_breaker'
- Line 12: Missing docstring for asyncfunctiondef 'fail'
- Line 15: Missing docstring for asyncfunctiondef 'ok'

### tests/test_status_service.py
- Line 10: Missing docstring for functiondef 'test_get_status_async'
- Line 20: Missing docstring for asyncfunctiondef 'fake_load'
- Line 27: Missing docstring for asyncfunctiondef '_call'

### quality_summary.py
- Line 20: Missing docstring for functiondef 'main'

### src/piwardrive/services/network_analytics.py
- Line 17: Missing docstring for functiondef '_haversine'

### tests/test_imports_src.py
- Line 17: Missing docstring for functiondef 'test_import_package_modules'

### tests/test_sigint_scanners_basic.py
- Line 30: Missing docstring for functiondef 'test_parse_iwlist_output'
- Line 45: Missing docstring for functiondef 'test_scan_wifi'
- Line 60: Missing docstring for functiondef 'test_scan_bluetoothctl'
- Line 69: Missing docstring for functiondef 'test_async_scan_bluetoothctl'
- Line 70: Missing docstring for asyncfunctiondef 'fake_proc'
- Line 71: Missing docstring for classdef 'P'
- Line 72: Missing docstring for asyncfunctiondef 'communicate'

### tests/test_calibrate_orientation.py
- Line 7: Missing docstring for functiondef 'test_calibrate_orientation'
- Line 21: Missing docstring for functiondef 'fake_prompt'

### tests/performance/test_performance_infrastructure.py
- Line 56: Missing docstring for functiondef '__init__'
- Line 67: Missing docstring for functiondef 'make_request'
- Line 160: Missing docstring for asyncfunctiondef 'make_async_request'

### src/piwardrive/exception_handler.py
- Line 66: Missing docstring for asyncfunctiondef '_fastapi_handler'

### tests/test_db_stats_widget.py
- Line 6: Missing docstring for functiondef '_load_widget'
- Line 10: Missing docstring for functiondef 'test_widget_update'

### src/piwardrive/reporting/professional.py
- Line 135: Missing docstring for functiondef '__init__'
- Line 744: Missing docstring for functiondef '__init__'
- Line 948: Missing docstring for functiondef '__init__'
- Line 1074: Missing docstring for functiondef '__init__'

### src/piwardrive/cli/config_cli.py
- Line 28: Missing docstring for asyncfunctiondef '_api_get'
- Line 37: Missing docstring for asyncfunctiondef '_api_update'

### tests/test_service_api_fixed_v2.py
- Line 189: Missing docstring for functiondef 'get_current_user'
- Line 193: Missing docstring for asyncfunctiondef 'protected_endpoint'
- Line 209: Missing docstring for asyncfunctiondef 'auth_middleware'
- Line 225: Missing docstring for functiondef 'process_auth_header'
- Line 255: Missing docstring for asyncfunctiondef 'http_exception_handler'
- Line 262: Missing docstring for asyncfunctiondef 'general_exception_handler'
- Line 276: Missing docstring for asyncfunctiondef 'http_exception_handler'
- Line 283: Missing docstring for asyncfunctiondef 'test_error'
- Line 296: Missing docstring for asyncfunctiondef 'value_error_handler'
- Line 303: Missing docstring for asyncfunctiondef 'test_exception'
- Line 322: Missing docstring for asyncfunctiondef 'root'
- Line 326: Missing docstring for asyncfunctiondef 'health'
- Line 349: Missing docstring for asyncfunctiondef 'get_status'
- Line 353: Missing docstring for asyncfunctiondef 'get_info'
- Line 373: Missing docstring for functiondef 'get_database'
- Line 377: Missing docstring for asyncfunctiondef 'get_database_info'
- Line 426: Missing docstring for asyncfunctiondef 'health_check'
- Line 441: Missing docstring for asyncfunctiondef 'detailed_health'
- Line 461: Missing docstring for asyncfunctiondef 'check_database_health'
- Line 465: Missing docstring for asyncfunctiondef 'check_service_health'
- Line 485: Missing docstring for asyncfunctiondef 'add_security_headers'
- Line 493: Missing docstring for asyncfunctiondef 'root'
- Line 510: Missing docstring for classdef 'UserInput'
- Line 516: Missing docstring for asyncfunctiondef 'create_user'
- Line 536: Missing docstring for asyncfunctiondef 'value_error_handler'
- Line 544: Missing docstring for asyncfunctiondef 'sensitive_error'
- Line 575: Missing docstring for asyncfunctiondef 'add_security_headers'
- Line 582: Missing docstring for asyncfunctiondef 'general_exception_handler'
- Line 590: Missing docstring for asyncfunctiondef 'root'
- Line 594: Missing docstring for asyncfunctiondef 'health'
- Line 54: Missing docstring for functiondef 'parse_cors_origins'
- Line 67: Missing docstring for functiondef 'parse_cors_origins'
- Line 82: Missing docstring for functiondef 'get_cpu_temp'
- Line 92: Missing docstring for functiondef 'get_cpu_temp'
- Line 107: Missing docstring for functiondef 'get_mem_usage'
- Line 119: Missing docstring for functiondef 'get_disk_usage'
- Line 132: Missing docstring for functiondef 'get_network_throughput'
- Line 152: Missing docstring for asyncfunctiondef 'service_status_async'
- Line 171: Missing docstring for functiondef 'run_service_cmd'

### scripts/health_import.py
- Line 21: Missing docstring for functiondef '_parse_json'
- Line 40: Missing docstring for functiondef '_parse_csv'
- Line 63: Missing docstring for asyncfunctiondef '_save_records'
- Line 69: Missing docstring for functiondef 'main'

### tests/test_config_validation.py
- Line 9: Missing docstring for functiondef 'setup'
- Line 14: Missing docstring for functiondef 'test_invalid_env_value'

### src/piwardrive/direction_finding/algorithms.py
- Line 35: Missing docstring for functiondef '__init__'
- Line 218: Missing docstring for functiondef '__init__'
- Line 520: Missing docstring for functiondef '__init__'
- Line 626: Missing docstring for functiondef '__init__'
- Line 906: Missing docstring for functiondef '__init__'
- Line 84: Missing docstring for functiondef 'hata_loss'
- Line 135: Missing docstring for functiondef 'dense_urban_loss'
- Line 164: Missing docstring for functiondef 'rural_loss'
- Line 331: Missing docstring for functiondef 'objective'

### tests/test_kalman.py
- Line 6: Missing docstring for functiondef 'test_kalman_filter_reduces_variance'

### src/piwardrive/performance/async_optimizer.py
- Line 132: Missing docstring for functiondef 'decorator'
- Line 155: Missing docstring for functiondef '__init__'
- Line 261: Missing docstring for functiondef '__init__'
- Line 343: Missing docstring for functiondef '__init__'
- Line 378: Missing docstring for functiondef '__init__'
- Line 449: Missing docstring for functiondef '__init__'
- Line 528: Missing docstring for functiondef '__init__'
- Line 134: Missing docstring for asyncfunctiondef 'wrapper'
- Line 585: Missing docstring for asyncfunctiondef '_execute_coro'
- Line 633: Missing docstring for asyncfunctiondef 'test_operation'

### scripts/health_export.py
- Line 18: Missing docstring for functiondef '_write_csv'
- Line 35: Missing docstring for functiondef '_write_json'
- Line 47: Missing docstring for asyncfunctiondef '_load_records'
- Line 51: Missing docstring for functiondef 'main'

### tests/test_export_db_script.py
- Line 16: Missing docstring for functiondef 'test_export_db_script'
- Line 19: Missing docstring for asyncfunctiondef 'fake_load_ap_cache'

### tests/test_rf_utils.py
- Line 15: Missing docstring for classdef 'DummySdr'
- Line 29: Missing docstring for functiondef 'test_spectrum_scan_returns_power'
- Line 41: Missing docstring for classdef 'SignalSdr'
- Line 47: Missing docstring for functiondef 'test_demodulate_fm'
- Line 59: Missing docstring for functiondef 'test_missing_rtlsdr'
- Line 68: Missing docstring for functiondef 'test_fm_demodulate_basic'
- Line 74: Missing docstring for functiondef 'test_frequency_conversions'
- Line 80: Missing docstring for functiondef 'test_parse_frequency'
- Line 16: Missing docstring for functiondef '__init__'
- Line 22: Missing docstring for functiondef 'read_samples'
- Line 25: Missing docstring for functiondef 'close'
- Line 42: Missing docstring for functiondef 'read_samples'

### src/piwardrive/sigint_suite/__init__.py
- Line 50: Missing docstring for functiondef '__getattr__'

### src/piwardrive/map/tile_maintenance.py
- Line 152: Missing docstring for functiondef '__init__'
- Line 155: Missing docstring for functiondef 'on_any_event'
- Line 162: Missing docstring for functiondef '__init__'
- Line 197: Missing docstring for asyncfunctiondef '_run'
- Line 221: Missing docstring for asyncfunctiondef '_runner'

### tests/test_analysis.py
- Line 9: Missing docstring for functiondef 'test_compute_health_stats'
- Line 19: Missing docstring for functiondef 'test_plot_cpu_temp_creates_file'
- Line 42: Missing docstring for functiondef 'test_plot_cpu_temp_plotly_backend'

### tests/test_forecasting.py
- Line 7: Missing docstring for functiondef 'test_forecast_cpu_temp_deterministic'

### src/piwardrive/services/data_export.py
- Line 11: Missing docstring for asyncfunctiondef '_fetch_all'

### tests/test_service_status_script.py
- Line 6: Missing docstring for functiondef 'test_service_status_script_output'

### tests/test_critical_paths.py
- Line 197: Missing docstring for functiondef 'test_func'
- Line 218: Missing docstring for functiondef 'test_func'
- Line 241: Missing docstring for functiondef 'test_func'

### src/piwardrive/widgets/security_score.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### scripts/validate_config.py
- Line 14: Missing docstring for functiondef 'main'

### src/piwardrive/migrations/010_performance_indexes.py
- Line 11: Missing docstring for asyncfunctiondef 'apply'
- Line 37: Missing docstring for asyncfunctiondef 'rollback'

### tests/test_vector_tile_customizer.py
- Line 7: Missing docstring for functiondef 'test_apply_style'
- Line 24: Missing docstring for functiondef 'test_build_mbtiles'

### tests/test_async_scheduler.py
- Line 10: Missing docstring for functiondef 'load_scheduler'
- Line 17: Missing docstring for functiondef 'test_poll_scheduler_accepts_async_widget'
- Line 41: Missing docstring for functiondef 'test_poll_scheduler_handles_async_callback'
- Line 61: Missing docstring for functiondef 'test_async_scheduler_runs_tasks'
- Line 87: Missing docstring for functiondef 'test_async_scheduler_sleep_remaining_time'
- Line 120: Missing docstring for functiondef 'test_async_scheduler_cancel_all_waits'
- Line 151: Missing docstring for functiondef 'test_async_scheduler_cancel_all_gathers_exceptions'
- Line 185: Missing docstring for functiondef 'test_poll_scheduler_metrics'
- Line 205: Missing docstring for functiondef 'test_async_scheduler_metrics'
- Line 232: Missing docstring for functiondef 'test_scheduler_rejects_invalid_interval'
- Line 20: Missing docstring for classdef 'Widget'
- Line 29: Missing docstring for functiondef 'fake_run_async'
- Line 46: Missing docstring for asyncfunctiondef 'job'
- Line 49: Missing docstring for functiondef 'fake_run_async'
- Line 65: Missing docstring for asyncfunctiondef 'update'
- Line 71: Missing docstring for asyncfunctiondef 'fast_sleep'
- Line 76: Missing docstring for asyncfunctiondef 'runner'
- Line 94: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 103: Missing docstring for asyncfunctiondef 'job'
- Line 107: Missing docstring for asyncfunctiondef 'runner'
- Line 126: Missing docstring for asyncfunctiondef 'job'
- Line 135: Missing docstring for asyncfunctiondef 'fast_sleep'
- Line 140: Missing docstring for asyncfunctiondef 'runner'
- Line 157: Missing docstring for asyncfunctiondef 'job'
- Line 166: Missing docstring for asyncfunctiondef 'fast_sleep'
- Line 171: Missing docstring for asyncfunctiondef 'runner'
- Line 190: Missing docstring for functiondef 'cb'
- Line 209: Missing docstring for asyncfunctiondef 'cb'
- Line 214: Missing docstring for asyncfunctiondef 'fast_sleep'
- Line 219: Missing docstring for asyncfunctiondef 'runner'
- Line 23: Missing docstring for asyncfunctiondef 'update'

### tests/test_database_counts.py
- Line 10: Missing docstring for functiondef '_stub_pydantic'
- Line 20: Missing docstring for functiondef 'setup_tmp'
- Line 27: Missing docstring for functiondef 'test_get_table_counts'

### tests/test_config.py
- Line 16: Missing docstring for functiondef 'setup_temp_config'
- Line 31: Missing docstring for functiondef 'test_load_config_defaults_when_missing'
- Line 47: Missing docstring for functiondef 'test_save_and_load_roundtrip'
- Line 73: Missing docstring for functiondef 'test_save_config_dataclass_roundtrip'
- Line 82: Missing docstring for functiondef 'test_save_config_no_temp_files'
- Line 90: Missing docstring for functiondef 'test_load_config_bad_json'
- Line 97: Missing docstring for functiondef 'test_load_config_schema_violation'
- Line 104: Missing docstring for functiondef 'test_load_config_invalid_json_monkeypatch'
- Line 115: Missing docstring for functiondef 'test_save_config_validation_error'
- Line 122: Missing docstring for functiondef 'test_env_override_integer'
- Line 137: Missing docstring for functiondef 'test_env_override_boolean'
- Line 148: Missing docstring for functiondef 'test_env_override_health_poll'
- Line 155: Missing docstring for functiondef 'test_env_override_route_prefetch'
- Line 164: Missing docstring for functiondef 'test_env_override_battery_widget'
- Line 171: Missing docstring for functiondef 'test_list_env_overrides'
- Line 176: Missing docstring for functiondef 'test_export_import_json'
- Line 185: Missing docstring for functiondef 'test_export_import_yaml'
- Line 195: Missing docstring for functiondef 'test_profile_roundtrip'
- Line 207: Missing docstring for functiondef 'test_import_export_profile'
- Line 218: Missing docstring for functiondef 'test_import_export_delete_profile'
- Line 309: Missing docstring for functiondef 'test_save_load_webhooks'
- Line 319: Missing docstring for functiondef 'test_profile_inheritance'
- Line 280: Missing docstring for functiondef 'fake_import'
- Line 298: Missing docstring for functiondef 'fake_import'

### tests/test_service_simple.py
- Line 131: Missing docstring for functiondef 'mock_check_auth'
- Line 141: Missing docstring for functiondef 'mock_auth'
- Line 43: Missing docstring for functiondef 'create_app'

### tests/test_analysis_hooks.py
- Line 21: Missing docstring for functiondef 'test_ml_hook_invoked'
- Line 24: Missing docstring for functiondef 'hook'

### src/piwardrive/widgets/scanner_status.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### tests/test_gpsd_client_async.py
- Line 6: Missing docstring for classdef 'DummyReader'
- Line 16: Missing docstring for classdef 'DummyWriter'
- Line 33: Missing docstring for functiondef 'test_async_methods_return_values'
- Line 67: Missing docstring for functiondef 'test_async_methods_failures'
- Line 7: Missing docstring for functiondef '__init__'
- Line 10: Missing docstring for asyncfunctiondef 'readline'
- Line 17: Missing docstring for functiondef '__init__'
- Line 20: Missing docstring for functiondef 'write'
- Line 23: Missing docstring for asyncfunctiondef 'drain'
- Line 26: Missing docstring for functiondef 'close'
- Line 29: Missing docstring for asyncfunctiondef 'wait_closed'
- Line 45: Missing docstring for asyncfunctiondef 'fake_open_connection'
- Line 52: Missing docstring for asyncfunctiondef 'run'
- Line 68: Missing docstring for asyncfunctiondef 'fake_open_connection'
- Line 75: Missing docstring for asyncfunctiondef 'run'

### tests/test_hooks.py
- Line 5: Missing docstring for functiondef 'test_custom_post_processor'
- Line 19: Missing docstring for functiondef 'add_custom'

### src/piwardrive/api/health/models.py
- Line 6: Missing docstring for classdef 'TokenResponse'
- Line 11: Missing docstring for classdef 'AuthLoginResponse'
- Line 15: Missing docstring for classdef 'LogoutResponse'
- Line 19: Missing docstring for classdef 'HealthRecordDict'
- Line 27: Missing docstring for classdef 'BaselineAnalysisResult'
- Line 34: Missing docstring for classdef 'SyncResponse'

### src/piwardrive/migrations/001_create_scan_sessions.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 44: Missing docstring for asyncfunctiondef 'rollback'

### scripts/prefetch_cli.py
- Line 28: Missing docstring for functiondef 'progress'

### tests/test_iot_analytics.py
- Line 7: Missing docstring for functiondef 'test_fingerprint_iot_devices_basic'
- Line 30: Missing docstring for functiondef 'test_correlate_city_services_window'

### src/piwardrive/migrations/002_enhance_wifi_detections.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 181: Missing docstring for asyncfunctiondef 'rollback'

### src/piwardrive/db/mysql.py
- Line 14: Missing docstring for functiondef '__init__'
- Line 29: Missing docstring for asyncfunctiondef 'connect'
- Line 38: Missing docstring for asyncfunctiondef 'close'
- Line 44: Missing docstring for asyncfunctiondef '_acquire'
- Line 57: Missing docstring for asyncfunctiondef '_release'
- Line 62: Missing docstring for asyncfunctiondef 'execute'
- Line 68: Missing docstring for asyncfunctiondef 'executemany'
- Line 74: Missing docstring for asyncfunctiondef 'fetchall'
- Line 83: Missing docstring for asyncfunctiondef 'transaction'
- Line 96: Missing docstring for functiondef 'get_metrics'

### src/piwardrive/protocols/multi_protocol.py
- Line 153: Missing docstring for functiondef '__init__'
- Line 297: Missing docstring for functiondef '__init__'
- Line 409: Missing docstring for functiondef '__init__'
- Line 509: Missing docstring for functiondef '__init__'
- Line 623: Missing docstring for functiondef '__init__'
- Line 751: Missing docstring for functiondef '__init__'
- Line 823: Missing docstring for functiondef '__init__'
- Line 1094: Missing docstring for functiondef 'device_discovered'

### scripts/prefetch_batch.py
- Line 11: Missing docstring for functiondef '_parse_bboxes'
- Line 58: Missing docstring for functiondef 'progress'

### tests/test_resource_manager.py
- Line 7: Missing docstring for functiondef 'test_file_and_db_cleanup'
- Line 21: Missing docstring for functiondef 'test_task_cancel'
- Line 24: Missing docstring for asyncfunctiondef 'worker'

### src/piwardrive/integrations/sigint_suite/scan_all.py
- Line 16: Missing docstring for functiondef 'run_once'
- Line 30: Missing docstring for functiondef 'main'

### src/piwardrive/widgets/suspicious_activity.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### tests/test_webui_server_main.py
- Line 7: Missing docstring for functiondef 'test_main_runs_uvicorn'
- Line 19: Missing docstring for functiondef 'test_main_env_port'

### src/piwardrive/widgets/lora_scan_widget.py
- Line 24: Missing docstring for functiondef '__init__'

### src/piwardrive/ui/user_experience.py
- Line 57: Missing docstring for functiondef '__post_init__'
- Line 61: Missing docstring for functiondef 'to_dict'
- Line 75: Missing docstring for functiondef 'to_dict'
- Line 90: Missing docstring for functiondef 'to_dict'
- Line 104: Missing docstring for functiondef 'to_dict'
- Line 112: Missing docstring for functiondef '__init__'
- Line 343: Missing docstring for functiondef '__init__'
- Line 623: Missing docstring for functiondef '__init__'
- Line 903: Missing docstring for functiondef '__init__'
- Line 1317: Missing docstring for functiondef 'hardware_callback'
- Line 1214: Missing docstring for functiondef '__init__'
- Line 1231: Missing docstring for functiondef 'index'
- Line 1237: Missing docstring for functiondef 'setup_wizard'
- Line 1250: Missing docstring for functiondef 'complete_setup_step'
- Line 1269: Missing docstring for functiondef 'tutorials'
- Line 1274: Missing docstring for functiondef 'start_tutorial'
- Line 1288: Missing docstring for functiondef 'dashboard'
- Line 1293: Missing docstring for functiondef 'get_widget_data'
- Line 1298: Missing docstring for functiondef 'themes'
- Line 1303: Missing docstring for functiondef 'get_theme_css'

### scripts/uav_record.py
- Line 22: Missing docstring for functiondef 'main'

### src/piwardrive/widgets/signal_strength.py
- Line 24: Missing docstring for functiondef '__init__'
- Line 35: Missing docstring for functiondef '_apply'

### src/piwardrive/analytics/anomaly.py
- Line 16: Missing docstring for functiondef '__init__'

### tests/test_cli_tools.py
- Line 21: Missing docstring for functiondef '_import_cli'
- Line 28: Missing docstring for functiondef 'test_config_cli_get_local'
- Line 35: Missing docstring for functiondef 'test_config_cli_set_local'
- Line 50: Missing docstring for functiondef 'test_config_cli_get_api'
- Line 62: Missing docstring for functiondef 'test_config_cli_set_api'
- Line 80: Missing docstring for functiondef 'test_config_cli_get_unknown_local'
- Line 87: Missing docstring for functiondef 'test_config_cli_set_unknown_local'
- Line 94: Missing docstring for functiondef 'test_config_cli_get_unknown_api'
- Line 106: Missing docstring for functiondef 'test_config_cli_set_unknown_api'
- Line 41: Missing docstring for functiondef 'fake_save'
- Line 53: Missing docstring for asyncfunctiondef 'fake_get'
- Line 65: Missing docstring for asyncfunctiondef 'fake_get'
- Line 69: Missing docstring for asyncfunctiondef 'fake_update'
- Line 97: Missing docstring for asyncfunctiondef 'fake_get'
- Line 109: Missing docstring for asyncfunctiondef 'fake_get'

### tests/test_sigint_export_json.py
- Line 6: Missing docstring for functiondef 'test_export_json'

### src/piwardrive/data_processing/enhanced_processing.py
- Line 41: Missing docstring for functiondef 'to_dict'
- Line 54: Missing docstring for functiondef '__init__'
- Line 120: Missing docstring for functiondef '__init__'
- Line 241: Missing docstring for functiondef '__init__'
- Line 354: Missing docstring for functiondef '__init__'
- Line 515: Missing docstring for functiondef '__init__'
- Line 710: Missing docstring for functiondef 'signal_processor'
- Line 719: Missing docstring for functiondef 'strong_signal_filter'
- Line 142: Missing docstring for functiondef 'simple_rule'
- Line 179: Missing docstring for functiondef 'composite_rule'
- Line 196: Missing docstring for functiondef 'geospatial_rule'

### tests/test_lora_scanner.py
- Line 11: Missing docstring for functiondef 'test_parse_packets'
- Line 23: Missing docstring for functiondef 'test_parse_packets_pandas'
- Line 37: Missing docstring for functiondef 'test_plot_signal_trend'
- Line 62: Missing docstring for functiondef 'test_async_scan_lora'
- Line 75: Missing docstring for functiondef 'test_async_parse_packets'
- Line 84: Missing docstring for functiondef 'test_main'
- Line 63: Missing docstring for asyncfunctiondef 'fake_exec'
- Line 64: Missing docstring for classdef 'P'
- Line 65: Missing docstring for asyncfunctiondef 'communicate'

### src/piwardrive/api/auth/middleware.py
- Line 13: Missing docstring for functiondef '__init__'
- Line 17: Missing docstring for asyncfunctiondef 'dispatch'

### tests/test_logconfig.py
- Line 10: Missing docstring for functiondef 'test_setup_logging_writes_json'
- Line 20: Missing docstring for functiondef 'test_setup_logging_respects_env'
- Line 32: Missing docstring for functiondef 'test_setup_logging_stdout'

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 340: Missing docstring for functiondef '__init__'
- Line 417: Missing docstring for functiondef '__init__'
- Line 487: Missing docstring for functiondef '__init__'
- Line 678: Missing docstring for functiondef '__init__'
- Line 722: Missing docstring for functiondef '__init__'
- Line 744: Missing docstring for functiondef '__init__'
- Line 920: Missing docstring for functiondef '__init__'
- Line 1006: Missing docstring for functiondef '__init__'
- Line 1199: Missing docstring for functiondef '__init__'

### tests/test_vendor_lookup.py
- Line 9: Missing docstring for functiondef '_reload_module'
- Line 18: Missing docstring for functiondef 'test_update_oui_file_downloads'
- Line 46: Missing docstring for functiondef 'test_update_oui_file_logs_error'
- Line 22: Missing docstring for classdef 'Resp'
- Line 36: Missing docstring for functiondef 'fail'
- Line 49: Missing docstring for functiondef 'fail'
- Line 25: Missing docstring for functiondef 'raise_for_status'

### src/piwardrive/integration/system_orchestration.py
- Line 133: Missing docstring for functiondef '__init__'
- Line 190: Missing docstring for functiondef '__init__'
- Line 243: Missing docstring for functiondef '__init__'
- Line 283: Missing docstring for functiondef '__init__'
- Line 343: Missing docstring for functiondef '__init__'
- Line 385: Missing docstring for functiondef '__init__'
- Line 411: Missing docstring for functiondef '__init__'
- Line 449: Missing docstring for functiondef '__init__'
- Line 469: Missing docstring for functiondef '__init__'
- Line 504: Missing docstring for functiondef '__init__'
- Line 534: Missing docstring for functiondef '__init__'
- Line 575: Missing docstring for functiondef '__init__'
- Line 597: Missing docstring for functiondef '__init__'
- Line 658: Missing docstring for functiondef '__init__'
- Line 719: Missing docstring for functiondef '__init__'
- Line 851: Missing docstring for functiondef 'handle_test_event'
- Line 154: Missing docstring for functiondef 'before_request'
- Line 159: Missing docstring for functiondef 'after_request'
- Line 164: Missing docstring for functiondef 'health_check'
- Line 170: Missing docstring for functiondef 'metrics'
- Line 764: Missing docstring for functiondef 'monitor_health'

### src/piwardrive/logging/storage.py
- Line 15: Missing docstring for asyncfunctiondef 'upload'
- Line 22: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for asyncfunctiondef 'upload'
- Line 39: Missing docstring for functiondef '__init__'
- Line 42: Missing docstring for asyncfunctiondef 'upload'
- Line 50: Missing docstring for functiondef '__init__'
- Line 61: Missing docstring for asyncfunctiondef 'upload'
- Line 88: Missing docstring for functiondef '__init__'
- Line 93: Missing docstring for functiondef '_initialize_backends'
- Line 104: Missing docstring for asyncfunctiondef 'archive_log'
- Line 114: Missing docstring for asyncfunctiondef '_calculate_file_hash'
- Line 131: Missing docstring for asyncfunctiondef '_record_archival'
- Line 151: Missing docstring for functiondef '__init__'
- Line 155: Missing docstring for functiondef '_load_retention_policies'
- Line 174: Missing docstring for asyncfunctiondef 'cleanup_expired_logs'
- Line 184: Missing docstring for asyncfunctiondef '_cleanup_local_logs'
- Line 194: Missing docstring for asyncfunctiondef '_cleanup_archived_logs'
- Line 117: Missing docstring for functiondef '_hash_file'

### src/piwardrive/ml/threat_detection.py
- Line 47: Missing docstring for functiondef 'to_dict'
- Line 69: Missing docstring for functiondef 'to_dict'
- Line 85: Missing docstring for functiondef 'to_dict'
- Line 92: Missing docstring for functiondef '__init__'
- Line 234: Missing docstring for functiondef '__init__'
- Line 381: Missing docstring for functiondef '__init__'
- Line 579: Missing docstring for functiondef '__init__'
- Line 806: Missing docstring for functiondef '__init__'

### src/piwardrive/aggregation_service.py
- Line 83: Missing docstring for asyncfunctiondef '_merge_records'
- Line 96: Missing docstring for asyncfunctiondef '_merge_points'
- Line 105: Missing docstring for asyncfunctiondef '_process_upload'

### tests/test_health_monitor.py
- Line 19: Missing docstring for classdef 'DummyScheduler'
- Line 33: Missing docstring for functiondef 'test_health_monitor_polls_self_test'
- Line 56: Missing docstring for functiondef 'test_health_monitor_daily_summary'
- Line 78: Missing docstring for functiondef 'test_health_monitor_exports'
- Line 102: Missing docstring for functiondef 'test_health_monitor_export_cleanup'
- Line 128: Missing docstring for functiondef 'test_health_monitor_upload_to_cloud'
- Line 20: Missing docstring for functiondef '__init__'
- Line 24: Missing docstring for functiondef 'schedule'
- Line 29: Missing docstring for functiondef 'cancel'
- Line 86: Missing docstring for functiondef 'fake_export'
- Line 112: Missing docstring for functiondef 'fake_export'
- Line 138: Missing docstring for classdef 'DummyCollector'
- Line 145: Missing docstring for functiondef 'fake_export'
- Line 149: Missing docstring for asyncfunctiondef 'direct'
- Line 139: Missing docstring for functiondef 'collect'

### tests/test_integration_core.py
- Line 11: Missing docstring for functiondef 'setup_tmp'
- Line 16: Missing docstring for functiondef 'test_health_record_flow'
- Line 26: Missing docstring for functiondef 'test_dashboard_settings_config'
- Line 35: Missing docstring for functiondef 'test_sync_new_records_real_server'
- Line 46: Missing docstring for asyncfunctiondef 'handler'
- Line 55: Missing docstring for asyncfunctiondef 'run_test'

### tests/test_diagnostics.py
- Line 22: Missing docstring for functiondef 'test_generate_system_report_includes_temp'
- Line 35: Missing docstring for functiondef 'test_self_test_returns_extra_info'
- Line 52: Missing docstring for functiondef 'test_self_test_restarts_failed_services'
- Line 74: Missing docstring for functiondef 'test_stop_profiling_writes_callgrind'
- Line 85: Missing docstring for functiondef 'test_rotate_log_gz'
- Line 105: Missing docstring for functiondef 'test_rotate_log_upload'
- Line 124: Missing docstring for functiondef 'test_rotate_log_max_files_check'
- Line 131: Missing docstring for functiondef 'test_rotate_log_async_max_files_check'
- Line 138: Missing docstring for functiondef 'test_run_network_test_caches_success'
- Line 158: Missing docstring for functiondef 'test_run_network_test_cache_expires'
- Line 177: Missing docstring for functiondef 'test_run_network_test_handles_failure'
- Line 188: Missing docstring for functiondef 'test_list_usb_devices_handles_failure'
- Line 145: Missing docstring for functiondef 'fake_run'
- Line 165: Missing docstring for functiondef 'fake_run'

### tests/test_priority_queue.py
- Line 9: Missing docstring for asyncfunctiondef 'test_priority_order'
- Line 13: Missing docstring for asyncfunctiondef 'make_task'

### src/piwardrive/notifications.py
- Line 60: Missing docstring for asyncfunctiondef '_post'
- Line 70: Missing docstring for asyncfunctiondef '_check'

### src/piwardrive/integrations/sigint_suite/scripts/continuous_scan.py
- Line 11: Missing docstring for functiondef '_save_results'
- Line 21: Missing docstring for functiondef 'main'

### src/piwardrive/db_browser.py
- Line 12: Missing docstring for classdef '_DBHandler'
- Line 15: Missing docstring for functiondef 'do_GET'

### tests/test_clustering.py
- Line 4: Missing docstring for functiondef 'test_cluster_positions_basic'
- Line 14: Missing docstring for functiondef 'test_cluster_positions_empty'

### tests/test_tile_maintenance_cli.py
- Line 8: Missing docstring for functiondef '_dummy_modules'
- Line 32: Missing docstring for functiondef 'test_tile_maintenance_cli'
- Line 35: Missing docstring for functiondef 'fake_purge'
- Line 38: Missing docstring for functiondef 'fake_limit'
- Line 41: Missing docstring for functiondef 'fake_vacuum'

### scripts/mobile_diagnostics.py
- Line 22: Missing docstring for functiondef '__init__'

### tests/test_main_simple.py
- Line 98: Missing docstring for functiondef 'custom_service_runner'

### tests/test_sigint_paths.py
- Line 4: Missing docstring for functiondef 'test_export_dir_env_override'

### tests/test_wifi_scanner.py
- Line 6: Missing docstring for functiondef '_mock_lookup_vendor'
- Line 14: Missing docstring for functiondef 'test_scan_wifi_enriches_vendor'
- Line 47: Missing docstring for functiondef 'test_scan_wifi_no_vendor'
- Line 71: Missing docstring for functiondef 'test_async_scan_wifi'
- Line 86: Missing docstring for asyncfunctiondef 'dummy_proc'
- Line 87: Missing docstring for classdef 'P'
- Line 88: Missing docstring for asyncfunctiondef 'communicate'

### tests/test_imports.py
- Line 15: Missing docstring for functiondef '_setup_dummy_modules'
- Line 172: Missing docstring for functiondef 'test_import_top_level_modules'
- Line 22: Missing docstring for classdef '_FastAPI'
- Line 23: Missing docstring for functiondef 'get'
- Line 29: Missing docstring for functiondef 'post'
- Line 35: Missing docstring for functiondef 'put'
- Line 41: Missing docstring for functiondef 'delete'
- Line 47: Missing docstring for functiondef 'websocket'
- Line 24: Missing docstring for functiondef 'decorator'
- Line 30: Missing docstring for functiondef 'decorator'
- Line 36: Missing docstring for functiondef 'decorator'
- Line 42: Missing docstring for functiondef 'decorator'
- Line 48: Missing docstring for functiondef 'decorator'

### tests/test_core_persistence.py
- Line 687: Missing docstring for asyncfunctiondef 'save_records'

### src/gps_handler.py
- Line 51: Missing docstring for functiondef '_connect'
- Line 63: Missing docstring for functiondef '_ensure_connection'

### tests/test_web_server_main.py
- Line 7: Missing docstring for functiondef 'test_main_runs_uvicorn'

### src/piwardrive/db/adapter.py
- Line 9: Missing docstring for asyncfunctiondef 'connect'
- Line 12: Missing docstring for asyncfunctiondef 'close'
- Line 15: Missing docstring for asyncfunctiondef 'execute'
- Line 18: Missing docstring for asyncfunctiondef 'executemany'
- Line 21: Missing docstring for asyncfunctiondef 'fetchall'

### tests/test_localization.py
- Line 149: Missing docstring for functiondef 'mock_open_side_effect'
- Line 184: Missing docstring for functiondef 'mock_open_side_effect'
- Line 323: Missing docstring for functiondef 'mock_open_side_effect'

### src/piwardrive/performance/realtime_optimizer.py
- Line 637: Missing docstring for asyncfunctiondef 'cleanup_task'

### tests/test_band_scanner.py
- Line 9: Missing docstring for functiondef 'test_scan_bands_parses_output'
- Line 19: Missing docstring for functiondef 'test_scan_bands_passes_timeout'
- Line 33: Missing docstring for functiondef 'test_async_scan_bands'
- Line 22: Missing docstring for functiondef 'fake_check_output'
- Line 36: Missing docstring for classdef 'DummyProc'
- Line 40: Missing docstring for asyncfunctiondef 'fake_create'
- Line 46: Missing docstring for asyncfunctiondef 'run'
- Line 37: Missing docstring for asyncfunctiondef 'communicate'

### tests/test_cache_security_fixed.py
- Line 50: Missing docstring for asyncfunctiondef 'run_test'
- Line 63: Missing docstring for asyncfunctiondef 'run_test'
- Line 76: Missing docstring for asyncfunctiondef 'run_test'
- Line 90: Missing docstring for asyncfunctiondef 'run_test'

### tests/test_utils_comprehensive.py
- Line 109: Missing docstring for asyncfunctiondef 'dummy_coro'

### tests/test_core_config_extra.py
- Line 9: Missing docstring for functiondef 'test_env_override'
- Line 16: Missing docstring for functiondef 'test_export_import_roundtrip'
- Line 25: Missing docstring for functiondef 'test_export_invalid_extension'
- Line 32: Missing docstring for functiondef 'test_yaml_export_import'
- Line 41: Missing docstring for functiondef 'test_apply_env_overrides_remote_sync_url'
- Line 48: Missing docstring for functiondef 'test_apply_env_overrides_mysql'
- Line 68: Missing docstring for functiondef 'test_parse_env_value'
- Line 72: Missing docstring for functiondef 'test_list_profiles'
- Line 83: Missing docstring for functiondef 'test_switch_profile'
- Line 134: Missing docstring for functiondef 'test_env_override_webhooks'
- Line 104: Missing docstring for functiondef 'fake_import'
- Line 123: Missing docstring for functiondef 'fake_import'

### src/piwardrive/main.py
- Line 99: Missing docstring for asyncfunctiondef '_start_jobs'
- Line 138: Missing docstring for asyncfunctiondef '_run_update'
- Line 178: Missing docstring for functiondef '_write'

### tests/test_remote_sync.py
- Line 24: Missing docstring for classdef 'DummyResp'
- Line 35: Missing docstring for classdef 'DummySession'
- Line 53: Missing docstring for functiondef 'prepare'
- Line 62: Missing docstring for asyncfunctiondef 'run_sync'
- Line 76: Missing docstring for functiondef 'test_load_sync_state_missing'
- Line 81: Missing docstring for functiondef 'test_save_and_load_sync_state'
- Line 87: Missing docstring for functiondef 'test_sync_database_file_missing'
- Line 93: Missing docstring for functiondef 'test_sync_database_retry'
- Line 99: Missing docstring for functiondef 'test_sync_database_failure'
- Line 121: Missing docstring for functiondef '_create_db'
- Line 139: Missing docstring for functiondef 'test_sync_new_records'
- Line 174: Missing docstring for functiondef 'test_make_range_db'
- Line 224: Missing docstring for functiondef 'test_make_range_db_empty_range'
- Line 272: Missing docstring for functiondef 'test_sync_database_timeout'
- Line 295: Missing docstring for functiondef 'test_sync_database_exponential_backoff'
- Line 323: Missing docstring for functiondef 'test_sync_metrics_success'
- Line 335: Missing docstring for functiondef 'test_sync_metrics_failure'
- Line 25: Missing docstring for asyncfunctiondef '__aenter__'
- Line 28: Missing docstring for asyncfunctiondef '__aexit__'
- Line 31: Missing docstring for functiondef 'raise_for_status'
- Line 36: Missing docstring for functiondef '__init__'
- Line 40: Missing docstring for asyncfunctiondef '__aenter__'
- Line 43: Missing docstring for asyncfunctiondef '__aexit__'
- Line 46: Missing docstring for functiondef 'post'
- Line 67: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 104: Missing docstring for classdef 'FailSession'
- Line 112: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 146: Missing docstring for asyncfunctiondef 'fake_sync'
- Line 277: Missing docstring for functiondef 'fake_timeout'
- Line 284: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 299: Missing docstring for classdef 'FailTwiceSession'
- Line 312: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 340: Missing docstring for classdef 'FailSess'
- Line 105: Missing docstring for functiondef 'post'
- Line 300: Missing docstring for functiondef 'post'
- Line 341: Missing docstring for functiondef 'post'

### tests/test_extra_widgets.py
- Line 5: Missing docstring for functiondef '_load_widgets'
- Line 12: Missing docstring for functiondef 'test_orientation_widget'
- Line 24: Missing docstring for functiondef 'test_vehicle_speed_widget'
- Line 33: Missing docstring for functiondef 'test_lora_scan_widget'

### tests/test_task_queue.py
- Line 6: Missing docstring for asyncfunctiondef 'test_background_task_queue_runs_tasks'
- Line 20: Missing docstring for asyncfunctiondef 'test_run_continuous_scan_with_queue'
- Line 10: Missing docstring for asyncfunctiondef 'job'
- Line 23: Missing docstring for asyncfunctiondef 'fake_wifi'
- Line 26: Missing docstring for asyncfunctiondef 'fake_bt'

### tests/test_aggregation_service.py
- Line 8: Missing docstring for functiondef '_create_src_db'
- Line 36: Missing docstring for functiondef 'test_upload_and_stats'
- Line 58: Missing docstring for functiondef 'test_upload_appends'
- Line 76: Missing docstring for functiondef 'test_upload_rejects_traversal'
- Line 89: Missing docstring for functiondef 'test_upload_rejects_nested_traversal'
- Line 102: Missing docstring for functiondef 'test_upload_rejects_evil_db'

### tests/test_load_kismet_data.py
- Line 28: Missing docstring for functiondef 'test_load_kismet_data_filters_and_returns_dataframe'

### src/piwardrive/migrations/008_create_network_analytics.py
- Line 11: Missing docstring for asyncfunctiondef 'apply'
- Line 45: Missing docstring for asyncfunctiondef 'rollback'

### src/piwardrive/services/export_service.py
- Line 12: Missing docstring for asyncfunctiondef '_fetch'

### src/piwardrive/geospatial/intelligence.py
- Line 116: Missing docstring for functiondef '__init__'
- Line 202: Missing docstring for functiondef '__init__'
- Line 301: Missing docstring for functiondef '__init__'
- Line 510: Missing docstring for functiondef '__init__'
- Line 591: Missing docstring for functiondef '__init__'
- Line 154: Missing docstring for functiondef 'objective'

### src/piwardrive/logging/levels.py
- Line 27: Missing docstring for functiondef '__init__'
- Line 70: Missing docstring for functiondef '_get_component_level'
- Line 76: Missing docstring for functiondef '_get_context_level'
- Line 83: Missing docstring for functiondef '_get_conditional_level'
- Line 103: Missing docstring for functiondef '__init__'
- Line 132: Missing docstring for functiondef '_load_content_filters'
- Line 135: Missing docstring for functiondef '_load_context_filters'
- Line 138: Missing docstring for functiondef '_setup_rate_limiters'
- Line 141: Missing docstring for functiondef '_load_sensitive_patterns'
- Line 144: Missing docstring for functiondef '_check_content_filters'
- Line 147: Missing docstring for functiondef '_check_context_filters'
- Line 150: Missing docstring for functiondef '_check_rate_limits'
- Line 153: Missing docstring for functiondef '_check_sensitive_data'

### tests/test_network_fingerprinting_integration.py
- Line 7: Missing docstring for classdef 'Dummy'
- Line 15: Missing docstring for functiondef 'test_fingerprint_wifi_records'
- Line 8: Missing docstring for functiondef '__init__'
- Line 11: Missing docstring for asyncfunctiondef '__call__'

### src/piwardrive/api/widgets/__init__.py
- Line 15: Missing docstring for classdef 'WidgetsListResponse'
- Line 19: Missing docstring for classdef 'WidgetMetrics'
- Line 25: Missing docstring for classdef 'DashboardSettingsResponse'
- Line 32: Missing docstring for asyncfunctiondef '_collect_widget_metrics'
- Line 39: Missing docstring for asyncfunctiondef 'list_widgets'
- Line 45: Missing docstring for asyncfunctiondef 'get_widget_metrics'
- Line 50: Missing docstring for asyncfunctiondef 'get_plugins'
- Line 57: Missing docstring for asyncfunctiondef 'get_dashboard_settings_endpoint'
- Line 65: Missing docstring for asyncfunctiondef 'update_dashboard_settings_endpoint'

### tests/test_error_reporting.py
- Line 25: Missing docstring for functiondef 'show_alert'

### tests/conftest.py
- Line 15: Missing docstring for functiondef 'add_dummy_module'
- Line 18: Missing docstring for functiondef '_add'

### src/piwardrive/analytics/forecasting.py
- Line 14: Missing docstring for functiondef '_arima_forecast'
- Line 24: Missing docstring for functiondef '_prophet_forecast'

### tests/test_plugins.py
- Line 5: Missing docstring for functiondef '_setup_env'
- Line 12: Missing docstring for functiondef 'test_load_hello_plugin'

### tests/test_bt_scanner.py
- Line 8: Missing docstring for classdef 'DummyDevice'
- Line 12: Missing docstring for functiondef 'test_scan_bluetooth_bleak'
- Line 28: Missing docstring for functiondef 'test_scan_bluetooth_fallback'
- Line 13: Missing docstring for asyncfunctiondef 'fake_discover'
- Line 29: Missing docstring for asyncfunctiondef 'fake_start'
- Line 35: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 40: Missing docstring for functiondef 'fake_import'

### tests/test_baseline_analysis.py
- Line 8: Missing docstring for functiondef 'test_analyze_health_baseline'
- Line 16: Missing docstring for functiondef 'test_load_baseline_health'

### tests/test_tower_scanner.py
- Line 9: Missing docstring for functiondef 'test_scan_towers'
- Line 24: Missing docstring for functiondef 'test_async_scan_towers'
- Line 27: Missing docstring for classdef 'DummyProc'
- Line 31: Missing docstring for asyncfunctiondef 'fake_create'
- Line 41: Missing docstring for asyncfunctiondef 'run'
- Line 28: Missing docstring for asyncfunctiondef 'communicate'

### tests/test_health_stats_script.py
- Line 7: Missing docstring for functiondef 'test_health_stats_script_output'
- Line 10: Missing docstring for asyncfunctiondef 'fake_load'

### src/piwardrive/visualization/advanced_viz.py
- Line 61: Missing docstring for functiondef '__init__'
- Line 226: Missing docstring for functiondef '__init__'
- Line 420: Missing docstring for functiondef '__init__'
- Line 587: Missing docstring for functiondef '__init__'
- Line 903: Missing docstring for functiondef '__init__'

### tests/test_fingerprint_persistence.py
- Line 8: Missing docstring for functiondef 'setup_tmp'
- Line 12: Missing docstring for functiondef 'test_save_and_load_fingerprint_info'

### src/piwardrive/api/common.py
- Line 38: Missing docstring for functiondef 'error_json'
- Line 47: Missing docstring for asyncfunctiondef '_default_fetch_metrics_async'
- Line 67: Missing docstring for asyncfunctiondef '_default_async_scan_lora'
- Line 76: Missing docstring for asyncfunctiondef '_default_service_status_async'
- Line 88: Missing docstring for asyncfunctiondef '_default_async_tail_file'

### tests/test_gpsd_client.py
- Line 8: Missing docstring for functiondef '_reload_with_dummy'
- Line 26: Missing docstring for functiondef 'test_get_position_none_on_failure'
- Line 31: Missing docstring for functiondef 'test_reconnect_after_error'
- Line 49: Missing docstring for functiondef 'test_env_overrides'
- Line 11: Missing docstring for functiondef 'connect'
- Line 15: Missing docstring for functiondef 'get_current'
- Line 35: Missing docstring for functiondef 'get_current'

### src/piwardrive/advanced_localization.py
- Line 169: Missing docstring for functiondef '_process'

### scripts/migrate_sqlite_to_postgres.py
- Line 12: Missing docstring for asyncfunctiondef 'copy_table'
- Line 26: Missing docstring for asyncfunctiondef 'migrate'
- Line 36: Missing docstring for asyncfunctiondef 'main'

### tests/test_service_async_endpoints.py
- Line 20: Missing docstring for functiondef '_get_service'
- Line 53: Missing docstring for asyncfunctiondef '_make_request'
- Line 60: Missing docstring for functiondef 'test_widgets_endpoint_async'
- Line 74: Missing docstring for functiondef 'test_logs_endpoint_async'
- Line 91: Missing docstring for functiondef 'test_service_status_endpoint_async'
- Line 30: Missing docstring for classdef 'MetricsResult'
- Line 37: Missing docstring for asyncfunctiondef '_dummy_async'
- Line 66: Missing docstring for asyncfunctiondef 'call'
- Line 77: Missing docstring for asyncfunctiondef 'fake_tail'
- Line 83: Missing docstring for asyncfunctiondef 'call'
- Line 94: Missing docstring for asyncfunctiondef 'fake_status'
- Line 101: Missing docstring for asyncfunctiondef 'call'

### src/piwardrive/web/webui_server.py
- Line 33: Missing docstring for functiondef 'main'

### src/piwardrive/integrations/sigint_suite/__init__.py
- Line 26: Missing docstring for functiondef '__getattr__'

### tests/logging/test_structured_logger.py
- Line 649: Missing docstring for classdef 'ComplexObject'
- Line 650: Missing docstring for functiondef '__str__'
- Line 653: Missing docstring for functiondef '__repr__'

### tests/test_cloud_export.py
- Line 9: Missing docstring for functiondef 'test_upload_to_s3_logs_errors'
- Line 12: Missing docstring for classdef 'DummyClient'
- Line 16: Missing docstring for classdef 'DummySession'
- Line 13: Missing docstring for functiondef 'upload_file'
- Line 17: Missing docstring for functiondef '__init__'
- Line 20: Missing docstring for functiondef 'client'

### src/piwardrive/services/network_fingerprinting.py
- Line 12: Missing docstring for functiondef '_extract_characteristics'
- Line 34: Missing docstring for functiondef '_classify'
- Line 51: Missing docstring for functiondef '_fingerprint_hash'
- Line 56: Missing docstring for functiondef '_make_row'

### tests/test_api_service.py
- Line 855: Missing docstring for asyncfunctiondef 'websocket_handler'
- Line 533: Missing docstring for asyncfunctiondef 'websocket_handler'
- Line 565: Missing docstring for asyncfunctiondef 'websocket_handler'

### src/piwardrive/error_reporting.py
- Line 39: Missing docstring for functiondef '__init__'

### src/piwardrive/logging/rotation.py
- Line 47: Missing docstring for functiondef '__init__'
- Line 57: Missing docstring for functiondef '_parse_timedelta'
- Line 107: Missing docstring for functiondef '__init__'
- Line 167: Missing docstring for functiondef '_check_size_limit'
- Line 175: Missing docstring for functiondef '_check_age_limit'
- Line 180: Missing docstring for functiondef '_check_free_space'
- Line 188: Missing docstring for functiondef '_get_rotated_filename'
- Line 210: Missing docstring for functiondef '_archive_log'
- Line 221: Missing docstring for functiondef '_compress_old_files'
- Line 238: Missing docstring for functiondef '_cleanup_old_files'

### src/piwardrive/direction_finding/core.py
- Line 135: Missing docstring for functiondef '__init__'

### tests/test_tile_maintenance.py
- Line 11: Missing docstring for functiondef '_dummy_modules'
- Line 36: Missing docstring for classdef 'DummyScheduler'
- Line 50: Missing docstring for functiondef 'test_tile_maintenance_runs'
- Line 37: Missing docstring for functiondef '__init__'
- Line 42: Missing docstring for functiondef 'schedule'
- Line 46: Missing docstring for functiondef 'cancel'
- Line 61: Missing docstring for classdef 'DummyConn'
- Line 62: Missing docstring for functiondef '__init__'
- Line 65: Missing docstring for functiondef '__enter__'
- Line 68: Missing docstring for functiondef '__exit__'
- Line 71: Missing docstring for functiondef 'execute'

### src/piwardrive/db/postgres.py
- Line 14: Missing docstring for functiondef '__init__'
- Line 33: Missing docstring for asyncfunctiondef 'connect'
- Line 49: Missing docstring for asyncfunctiondef 'close'
- Line 57: Missing docstring for asyncfunctiondef '_get_read_pool'
- Line 65: Missing docstring for asyncfunctiondef '_acquire'
- Line 80: Missing docstring for asyncfunctiondef '_release'
- Line 84: Missing docstring for asyncfunctiondef 'execute'
- Line 89: Missing docstring for asyncfunctiondef 'executemany'
- Line 94: Missing docstring for asyncfunctiondef 'fetchall'
- Line 101: Missing docstring for asyncfunctiondef 'transaction'
- Line 113: Missing docstring for functiondef 'get_metrics'

### tests/test_anomaly_detector.py
- Line 7: Missing docstring for functiondef 'test_anomaly_warning_triggered'

### tests/test_utils.py
- Line 40: Missing docstring for functiondef 'test_format_error_with_enum'
- Line 45: Missing docstring for functiondef 'test_find_latest_file_returns_latest'
- Line 59: Missing docstring for functiondef 'test_find_latest_file_none_when_empty'
- Line 64: Missing docstring for functiondef 'test_tail_file_returns_last_lines'
- Line 76: Missing docstring for functiondef 'test_tail_file_missing_returns_empty_list'
- Line 81: Missing docstring for functiondef 'test_tail_file_nonpositive_lines'
- Line 92: Missing docstring for functiondef 'test_tail_file_handles_large_file'
- Line 102: Missing docstring for functiondef 'test_tail_file_cache'
- Line 121: Missing docstring for functiondef '_patch_dbus'
- Line 150: Missing docstring for functiondef '_patch_bt_dbus'
- Line 175: Missing docstring for functiondef 'test_run_service_cmd_success'
- Line 185: Missing docstring for functiondef 'test_run_service_cmd_failure'
- Line 195: Missing docstring for functiondef 'test_run_service_cmd_retries_until_success'
- Line 212: Missing docstring for functiondef 'test_message_bus_disconnect_called'
- Line 251: Missing docstring for functiondef 'test_service_status_passes_retry_params'
- Line 260: Missing docstring for functiondef 'test_point_in_polygon_basic'
- Line 266: Missing docstring for functiondef 'test_load_kml_parses_features'
- Line 281: Missing docstring for functiondef 'test_load_kmz_parses_features'
- Line 295: Missing docstring for functiondef 'test_fetch_kismet_devices_request_exception'
- Line 314: Missing docstring for functiondef 'test_fetch_kismet_devices_json_error'
- Line 345: Missing docstring for functiondef 'test_get_smart_status_ok'
- Line 358: Missing docstring for functiondef 'test_get_smart_status_failure'
- Line 372: Missing docstring for functiondef 'test_fetch_kismet_devices_async'
- Line 401: Missing docstring for functiondef 'test_fetch_kismet_devices_async_logs_cache_error'
- Line 436: Missing docstring for functiondef 'test_fetch_kismet_devices_cache'
- Line 471: Missing docstring for functiondef 'test_fetch_kismet_devices_async_cache'
- Line 509: Missing docstring for functiondef 'test_safe_request_retries'
- Line 535: Missing docstring for functiondef 'test_safe_request_cache'
- Line 564: Missing docstring for functiondef 'test_safe_request_cache_pruning'
- Line 602: Missing docstring for functiondef 'test_ensure_service_running_attempts_restart'
- Line 619: Missing docstring for functiondef 'test_scan_bt_devices_parses_output'
- Line 659: Missing docstring for functiondef 'test_scan_bt_devices_handles_error'
- Line 669: Missing docstring for functiondef 'test_gpsd_cache'
- Line 697: Missing docstring for functiondef 'test_count_bettercap_handshakes'
- Line 712: Missing docstring for functiondef 'test_count_bettercap_handshakes_missing'
- Line 717: Missing docstring for functiondef 'test_count_bettercap_handshakes_cache'
- Line 735: Missing docstring for functiondef 'test_network_scanning_disabled'
- Line 741: Missing docstring for functiondef 'test_get_network_throughput_interface'
- Line 764: Missing docstring for functiondef 'test_network_scanning_disabled_logs'
- Line 772: Missing docstring for functiondef 'test_get_network_throughput_calculates_kbps'
- Line 786: Missing docstring for functiondef 'test_get_network_throughput_resets_when_cache_missing'
- Line 821: Missing docstring for functiondef 'test_get_mem_usage_cache'
- Line 840: Missing docstring for functiondef 'test_get_disk_usage_cache'
- Line 110: Missing docstring for functiondef 'fail'
- Line 122: Missing docstring for classdef 'Bus'
- Line 153: Missing docstring for classdef 'Bus'
- Line 157: Missing docstring for classdef 'Manager'
- Line 163: Missing docstring for functiondef 'system_bus'
- Line 166: Missing docstring for functiondef 'interface'
- Line 198: Missing docstring for functiondef 'start_side'
- Line 215: Missing docstring for classdef 'Bus'
- Line 252: Missing docstring for asyncfunctiondef '_svc'
- Line 296: Missing docstring for classdef 'FakeSession'
- Line 315: Missing docstring for classdef 'FakeResp'
- Line 327: Missing docstring for classdef 'FakeSession'
- Line 373: Missing docstring for classdef 'FakeResp'
- Line 385: Missing docstring for classdef 'FakeSession'
- Line 402: Missing docstring for classdef 'FakeResp'
- Line 414: Missing docstring for classdef 'FakeSession'
- Line 454: Missing docstring for classdef 'FakeSession'
- Line 474: Missing docstring for classdef 'FakeResp'
- Line 486: Missing docstring for classdef 'FakeSession'
- Line 512: Missing docstring for classdef 'Resp'
- Line 519: Missing docstring for functiondef 'get'
- Line 538: Missing docstring for classdef 'Resp'
- Line 546: Missing docstring for functiondef 'request'
- Line 565: Missing docstring for classdef 'Resp'
- Line 571: Missing docstring for functiondef 'get'
- Line 586: Missing docstring for functiondef 'timer'
- Line 605: Missing docstring for functiondef 'status'
- Line 624: Missing docstring for classdef 'Props'
- Line 629: Missing docstring for classdef 'Bus'
- Line 633: Missing docstring for functiondef 'interface'
- Line 742: Missing docstring for classdef 'C'
- Line 749: Missing docstring for functiondef 'fake_counters'
- Line 807: Missing docstring for asyncfunctiondef 'do_work'
- Line 812: Missing docstring for functiondef 'cb'
- Line 123: Missing docstring for functiondef '__init__'
- Line 126: Missing docstring for asyncfunctiondef 'connect'
- Line 129: Missing docstring for asyncfunctiondef 'introspect'
- Line 132: Missing docstring for functiondef 'get_proxy_object'
- Line 139: Missing docstring for functiondef 'disconnect'
- Line 154: Missing docstring for functiondef 'get_object'
- Line 158: Missing docstring for functiondef 'GetManagedObjects'
- Line 216: Missing docstring for functiondef '__init__'
- Line 219: Missing docstring for asyncfunctiondef 'connect'
- Line 222: Missing docstring for asyncfunctiondef 'introspect'
- Line 227: Missing docstring for functiondef 'get_proxy_object'
- Line 234: Missing docstring for functiondef 'disconnect'
- Line 297: Missing docstring for asyncfunctiondef '__aenter__'
- Line 300: Missing docstring for asyncfunctiondef '__aexit__'
- Line 303: Missing docstring for functiondef 'get'
- Line 318: Missing docstring for asyncfunctiondef 'text'
- Line 321: Missing docstring for asyncfunctiondef '__aenter__'
- Line 324: Missing docstring for asyncfunctiondef '__aexit__'
- Line 328: Missing docstring for asyncfunctiondef '__aenter__'
- Line 331: Missing docstring for asyncfunctiondef '__aexit__'
- Line 334: Missing docstring for functiondef 'get'
- Line 376: Missing docstring for asyncfunctiondef 'text'
- Line 379: Missing docstring for asyncfunctiondef '__aenter__'
- Line 382: Missing docstring for asyncfunctiondef '__aexit__'
- Line 386: Missing docstring for asyncfunctiondef '__aenter__'
- Line 389: Missing docstring for asyncfunctiondef '__aexit__'
- Line 392: Missing docstring for functiondef 'get'
- Line 405: Missing docstring for asyncfunctiondef 'text'
- Line 408: Missing docstring for asyncfunctiondef '__aenter__'
- Line 411: Missing docstring for asyncfunctiondef '__aexit__'
- Line 415: Missing docstring for asyncfunctiondef '__aenter__'
- Line 418: Missing docstring for asyncfunctiondef '__aexit__'
- Line 421: Missing docstring for functiondef 'get'
- Line 455: Missing docstring for asyncfunctiondef '__aenter__'
- Line 458: Missing docstring for asyncfunctiondef '__aexit__'
- Line 461: Missing docstring for functiondef 'get'
- Line 477: Missing docstring for asyncfunctiondef 'text'
- Line 480: Missing docstring for asyncfunctiondef '__aenter__'
- Line 483: Missing docstring for asyncfunctiondef '__aexit__'
- Line 487: Missing docstring for asyncfunctiondef '__aenter__'
- Line 490: Missing docstring for asyncfunctiondef '__aexit__'
- Line 493: Missing docstring for functiondef 'get'
- Line 516: Missing docstring for functiondef 'raise_for_status'
- Line 541: Missing docstring for functiondef 'raise_for_status'
- Line 568: Missing docstring for functiondef 'raise_for_status'
- Line 625: Missing docstring for functiondef 'Get'
- Line 630: Missing docstring for functiondef 'get_object'
- Line 743: Missing docstring for functiondef '__init__'
- Line 903: Missing docstring for functiondef 'mock_request'
- Line 920: Missing docstring for functiondef 'mock_request'
- Line 933: Missing docstring for functiondef 'mock_request'
- Line 940: Missing docstring for functiondef 'mock_sleep'
- Line 986: Missing docstring for functiondef 'mock_request'
- Line 133: Missing docstring for classdef 'Obj'
- Line 228: Missing docstring for classdef 'Obj'
- Line 969: Missing docstring for functiondef 'mock_request'
- Line 134: Missing docstring for functiondef 'get_interface'
- Line 229: Missing docstring for functiondef 'get_interface'

### src/piwardrive/task_queue.py
- Line 28: Missing docstring for asyncfunctiondef '_worker'
- Line 77: Missing docstring for asyncfunctiondef '_worker'

### src/piwardrive/migrations/005_create_cellular_detections.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 62: Missing docstring for asyncfunctiondef 'rollback'

### tests/test_sync.py
- Line 14: Missing docstring for classdef 'DummyConfig'
- Line 21: Missing docstring for functiondef 'test_upload_data_retries'
- Line 67: Missing docstring for functiondef 'test_upload_data_failure'
- Line 24: Missing docstring for classdef 'Resp'
- Line 33: Missing docstring for classdef 'Session'
- Line 56: Missing docstring for asyncfunctiondef '_noop'
- Line 68: Missing docstring for classdef 'Resp'
- Line 77: Missing docstring for classdef 'Session'
- Line 94: Missing docstring for asyncfunctiondef '_noop'
- Line 27: Missing docstring for asyncfunctiondef '__aenter__'
- Line 30: Missing docstring for asyncfunctiondef '__aexit__'
- Line 34: Missing docstring for functiondef '__init__'
- Line 37: Missing docstring for asyncfunctiondef '__aenter__'
- Line 40: Missing docstring for asyncfunctiondef '__aexit__'
- Line 43: Missing docstring for functiondef 'post'
- Line 71: Missing docstring for asyncfunctiondef '__aenter__'
- Line 74: Missing docstring for asyncfunctiondef '__aexit__'
- Line 78: Missing docstring for asyncfunctiondef '__aenter__'
- Line 81: Missing docstring for asyncfunctiondef '__aexit__'
- Line 84: Missing docstring for functiondef 'post'

### src/piwardrive/navigation/offline_navigation.py
- Line 151: Missing docstring for functiondef '__init__'
- Line 314: Missing docstring for functiondef '__init__'
- Line 362: Missing docstring for functiondef '__init__'
- Line 419: Missing docstring for functiondef '__init__'
- Line 567: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/battery_status.py
- Line 25: Missing docstring for functiondef '__init__'

### scripts/df_integration_demo.py
- Line 42: Missing docstring for functiondef '__init__'

### tests/test_gps_handler.py
- Line 8: Missing docstring for functiondef '_reload_with_dummy'
- Line 14: Missing docstring for classdef '_DummyBase'
- Line 25: Missing docstring for functiondef 'test_position_none_on_connect_failure'
- Line 34: Missing docstring for functiondef 'test_timeout_returns_none'
- Line 46: Missing docstring for functiondef 'test_reconnect_after_error'
- Line 15: Missing docstring for functiondef '__init__'
- Line 18: Missing docstring for functiondef 'stream'
- Line 21: Missing docstring for functiondef 'close'
- Line 26: Missing docstring for classdef 'Dummy'
- Line 35: Missing docstring for classdef 'Dummy'
- Line 52: Missing docstring for classdef 'Dummy'
- Line 27: Missing docstring for functiondef '__init__'
- Line 36: Missing docstring for functiondef 'waiting'
- Line 39: Missing docstring for functiondef 'next'
- Line 53: Missing docstring for functiondef 'waiting'
- Line 56: Missing docstring for functiondef 'next'

### src/piwardrive/analysis/packet_engine.py
- Line 557: Missing docstring for functiondef '__init__'
- Line 707: Missing docstring for functiondef '__init__'
- Line 915: Missing docstring for functiondef '__init__'
- Line 1094: Missing docstring for functiondef '__init__'

### scripts/export_mysql.py
- Line 16: Missing docstring for functiondef '_env_default'
- Line 28: Missing docstring for functiondef 'main'

### tests/test_geometry_utils.py
- Line 7: Missing docstring for functiondef 'test_haversine_distance_zero'
- Line 11: Missing docstring for functiondef 'test_haversine_distance_known'
- Line 16: Missing docstring for functiondef 'test_polygon_area_triangle'
- Line 23: Missing docstring for functiondef 'test_polygon_area_insufficient_points'
- Line 27: Missing docstring for functiondef 'test_parse_coord_text'
- Line 32: Missing docstring for functiondef 'test_get_avg_rssi'

### src/piwardrive/logging/dynamic_config.py
- Line 22: Missing docstring for functiondef '__init__'
- Line 37: Missing docstring for functiondef '__init__'

### tests/test_widget_cache.py
- Line 7: Missing docstring for functiondef 'test_widget_plugin_cache'
- Line 24: Missing docstring for functiondef 'wrapped'

### tests/test_service_sync.py
- Line 13: Missing docstring for functiondef '_load_service'
- Line 50: Missing docstring for functiondef 'test_sync_endpoint_success'
- Line 72: Missing docstring for functiondef 'test_sync_endpoint_failure'
- Line 23: Missing docstring for classdef 'MetricsResult'
- Line 30: Missing docstring for asyncfunctiondef '_dummy'
- Line 54: Missing docstring for asyncfunctiondef 'fake_load'
- Line 57: Missing docstring for asyncfunctiondef 'fake_upload'
- Line 75: Missing docstring for asyncfunctiondef 'fake_load'
- Line 78: Missing docstring for asyncfunctiondef 'fake_upload'

### tests/test_kiosk_cli.py
- Line 7: Missing docstring for functiondef 'test_kiosk_cli_launches_browser'

### src/piwardrive/mining/advanced_data_mining.py
- Line 93: Missing docstring for functiondef '__init__'
- Line 372: Missing docstring for functiondef '__init__'
- Line 581: Missing docstring for functiondef '__init__'
- Line 766: Missing docstring for functiondef '__init__'
- Line 1008: Missing docstring for functiondef '__init__'

### src/piwardrive/logging/config.py
- Line 13: Missing docstring for functiondef '__init__'
- Line 17: Missing docstring for functiondef '_get_default_config_path'
- Line 66: Missing docstring for functiondef '_get_environment_overrides'
- Line 72: Missing docstring for functiondef '_merge_configs'

### src/piwardrive/migrations/009_create_materialized_views.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 58: Missing docstring for asyncfunctiondef 'rollback'

### src/piwardrive/widgets/health_analysis.py
- Line 28: Missing docstring for functiondef '__init__'
- Line 46: Missing docstring for functiondef '_apply'

### src/piwardrive/analytics/iot.py
- Line 8: Missing docstring for functiondef '_extract_features'
- Line 21: Missing docstring for functiondef '_hash_features'
- Line 26: Missing docstring for functiondef '_classify'

### tests/test_vacuum_script.py
- Line 5: Missing docstring for functiondef 'test_vacuum_script'
- Line 8: Missing docstring for asyncfunctiondef 'fake_vacuum'

### src/piwardrive/logging/structured_logger.py
- Line 28: Missing docstring for functiondef '_get_version'
- Line 230: Missing docstring for functiondef 'dataclass_replace'
- Line 56: Missing docstring for functiondef '__init__'
- Line 116: Missing docstring for functiondef '__init__'
- Line 147: Missing docstring for functiondef '_create_handlers'
- Line 182: Missing docstring for functiondef '_log'

### src/piwardrive/visualization/advanced_visualization.py
- Line 123: Missing docstring for functiondef '__init__'
- Line 191: Missing docstring for functiondef '__init__'
- Line 295: Missing docstring for functiondef '__init__'
- Line 368: Missing docstring for functiondef '__init__'
- Line 478: Missing docstring for functiondef '__init__'
- Line 1150: Missing docstring for functiondef 'timeline_callback'
- Line 268: Missing docstring for functiondef 'playback_loop'

### src/piwardrive/logging/scheduler.py
- Line 16: Missing docstring for functiondef '__init__'
- Line 21: Missing docstring for functiondef 'schedule_rotation_check'
- Line 29: Missing docstring for functiondef 'schedule_retention_cleanup'
- Line 36: Missing docstring for asyncfunctiondef 'start'
- Line 40: Missing docstring for asyncfunctiondef 'stop'
- Line 45: Missing docstring for asyncfunctiondef '_run_scheduler'
- Line 54: Missing docstring for functiondef '_check_handler_rotation'
- Line 61: Missing docstring for functiondef '_daily_cleanup'
- Line 68: Missing docstring for functiondef '_run_retention_cleanup'

### src/piwardrive/migrations/003_create_bluetooth_detections.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 61: Missing docstring for asyncfunctiondef 'rollback'

### tests/test_integration_comprehensive.py
- Line 40: Missing docstring for functiondef '__init__'
- Line 322: Missing docstring for asyncfunctiondef 'mock_gps_service'
- Line 332: Missing docstring for asyncfunctiondef 'mock_network_scanner'
- Line 366: Missing docstring for asyncfunctiondef 'data_generator'
- Line 371: Missing docstring for asyncfunctiondef 'data_processor'
- Line 375: Missing docstring for asyncfunctiondef 'data_sink'
- Line 441: Missing docstring for functiondef 'write_worker'
- Line 533: Missing docstring for functiondef 'simulate_user'

### scripts/validate_migration.py
- Line 12: Missing docstring for asyncfunctiondef 'count_rows_sqlite'
- Line 18: Missing docstring for asyncfunctiondef 'count_rows_pg'
- Line 23: Missing docstring for asyncfunctiondef 'validate'

### src/piwardrive/direction_finding/config.py
- Line 284: Missing docstring for functiondef '__init__'
- Line 458: Missing docstring for functiondef 'enum_serializer'

### scripts/export_gpx.py
- Line 10: Missing docstring for functiondef '_load_json'
- Line 20: Missing docstring for functiondef '_load_csv'

### tests/test_mysql_export.py
- Line 7: Missing docstring for classdef 'DummyCursor'
- Line 24: Missing docstring for classdef 'DummyConn'
- Line 41: Missing docstring for functiondef 'test_init_schema'
- Line 55: Missing docstring for functiondef 'test_insert_records'
- Line 8: Missing docstring for functiondef '__init__'
- Line 11: Missing docstring for asyncfunctiondef 'execute'
- Line 14: Missing docstring for asyncfunctiondef 'executemany'
- Line 17: Missing docstring for asyncfunctiondef '__aenter__'
- Line 20: Missing docstring for asyncfunctiondef '__aexit__'
- Line 25: Missing docstring for functiondef '__init__'
- Line 28: Missing docstring for functiondef 'cursor'
- Line 31: Missing docstring for asyncfunctiondef 'commit'
- Line 34: Missing docstring for functiondef 'close'
- Line 37: Missing docstring for asyncfunctiondef 'wait_closed'
- Line 44: Missing docstring for asyncfunctiondef 'fake_connect'
- Line 58: Missing docstring for asyncfunctiondef 'fake_connect'

### src/piwardrive/plugins/plugin_architecture.py
- Line 172: Missing docstring for functiondef '__init__'
- Line 241: Missing docstring for functiondef '__init__'
- Line 288: Missing docstring for functiondef '__init__'
- Line 548: Missing docstring for functiondef '__init__'
- Line 581: Missing docstring for functiondef '__init__'
- Line 621: Missing docstring for functiondef '__init__'
- Line 749: Missing docstring for functiondef 'on_plugin_event'

### src/piwardrive/core/utils.py
- Line 73: Missing docstring for classdef '_GPSDEntry'
- Line 94: Missing docstring for classdef '_NetIOEntry'
- Line 111: Missing docstring for classdef '_MemUsageEntry'
- Line 121: Missing docstring for classdef '_DiskUsageEntry'
- Line 191: Missing docstring for classdef '_DummySession'
- Line 213: Missing docstring for functiondef 'decorator'
- Line 432: Missing docstring for functiondef '_get'
- Line 685: Missing docstring for functiondef '_call'
- Line 751: Missing docstring for asyncfunctiondef '_call'
- Line 778: Missing docstring for asyncfunctiondef '_retry'
- Line 1136: Missing docstring for functiondef 'project'
- Line 1208: Missing docstring for functiondef '_parse'
- Line 218: Missing docstring for asyncfunctiondef 'wrapper'
- Line 383: Missing docstring for functiondef '_done'
- Line 909: Missing docstring for asyncfunctiondef '_fetch'

### tests/test_data_sink.py
- Line 8: Missing docstring for asyncfunctiondef '_run'
- Line 12: Missing docstring for functiondef 'test_upload_to_s3'
- Line 21: Missing docstring for functiondef 'test_write_influxdb'
- Line 53: Missing docstring for functiondef 'test_write_postgres'
- Line 24: Missing docstring for classdef 'Sess'
- Line 56: Missing docstring for classdef 'Conn'
- Line 68: Missing docstring for asyncfunctiondef 'fake_connect'
- Line 25: Missing docstring for asyncfunctiondef '__aenter__'
- Line 28: Missing docstring for asyncfunctiondef '__aexit__'
- Line 31: Missing docstring for functiondef 'post'
- Line 57: Missing docstring for functiondef '__init__'
- Line 60: Missing docstring for asyncfunctiondef 'executemany'
- Line 63: Missing docstring for asyncfunctiondef 'close'
- Line 34: Missing docstring for classdef 'Resp'
- Line 35: Missing docstring for asyncfunctiondef '__aenter__'
- Line 38: Missing docstring for asyncfunctiondef '__aexit__'
- Line 41: Missing docstring for functiondef 'raise_for_status'

### tests/test_db_summary_script.py
- Line 6: Missing docstring for functiondef 'test_db_summary_script'

### scripts/export_grafana.py
- Line 7: Missing docstring for functiondef '_create_tables'
- Line 29: Missing docstring for functiondef '_insert_health'
- Line 39: Missing docstring for functiondef '_insert_wifi'
- Line 49: Missing docstring for asyncfunctiondef '_load_data'
- Line 60: Missing docstring for functiondef 'main'

### scripts/monitoring_service.py
- Line 37: Missing docstring for functiondef '__init__'

### tests/test_service_plugins.py
- Line 8: Missing docstring for functiondef 'test_plugins_endpoint'

### src/piwardrive/widgets/health_status.py
- Line 23: Missing docstring for functiondef '__init__'

### scripts/uav_track_playback.py
- Line 14: Missing docstring for asyncfunctiondef '_print_point'
- Line 18: Missing docstring for asyncfunctiondef '_run'
- Line 24: Missing docstring for functiondef 'main'

### tests/test_export_log_bundle_script.py
- Line 5: Missing docstring for functiondef 'test_export_log_bundle_script'
- Line 8: Missing docstring for asyncfunctiondef 'fake_bundle'
- Line 13: Missing docstring for classdef 'DummyApp'

### tests/test_ckml.py
- Line 4: Missing docstring for functiondef 'test_parse_coords_simple'
- Line 9: Missing docstring for functiondef 'test_parse_coords_with_altitude'
- Line 14: Missing docstring for functiondef 'test_parse_coords_negative'
- Line 19: Missing docstring for functiondef 'test_parse_coords_malformed_single_token'
- Line 24: Missing docstring for functiondef 'test_parse_coords_mixed_valid_invalid'

### src/piwardrive/enhanced/critical_additions.py
- Line 217: Missing docstring for functiondef '__init__'
- Line 327: Missing docstring for functiondef '__init__'
- Line 557: Missing docstring for functiondef '__init__'
- Line 782: Missing docstring for functiondef '__init__'

### src/piwardrive/services/stream_processor.py
- Line 79: Missing docstring for functiondef '_enqueue'
- Line 117: Missing docstring for asyncfunctiondef '_process_wifi'
- Line 121: Missing docstring for asyncfunctiondef '_run'

### tests/test_main_application_comprehensive.py
- Line 65: Missing docstring for functiondef 'mock_service_cmd'

### src/service.py
- Line 27: Missing docstring for functiondef '_proxy'
- Line 28: Missing docstring for functiondef 'wrapper'

### tests/test_aggregation_service_main_new.py
- Line 6: Missing docstring for functiondef 'test_main_starts_uvicorn'

### src/piwardrive/signal/rf_spectrum.py
- Line 86: Missing docstring for functiondef '__init__'
- Line 117: Missing docstring for functiondef '__init__'
- Line 247: Missing docstring for functiondef '__init__'
- Line 392: Missing docstring for functiondef '__init__'
- Line 449: Missing docstring for functiondef '__init__'
- Line 492: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/orientation_widget.py
- Line 24: Missing docstring for functiondef '__init__'

### scripts/watch_service.py
- Line 17: Missing docstring for asyncfunctiondef '_restart'
- Line 25: Missing docstring for asyncfunctiondef '_watch'
- Line 32: Missing docstring for functiondef 'main'

### src/piwardrive/scan_report.py
- Line 17: Missing docstring for functiondef '_sync_load'
- Line 23: Missing docstring for asyncfunctiondef '_load_records'

### src/piwardrive/widgets/storage_usage.py
- Line 24: Missing docstring for functiondef '__init__'

### tests/test_performance_comprehensive.py
- Line 56: Missing docstring for functiondef '__init__'
- Line 274: Missing docstring for classdef 'MockHighVolumeScanner'
- Line 305: Missing docstring for classdef 'MockContinuousScanner'
- Line 488: Missing docstring for functiondef 'data_stream'
- Line 725: Missing docstring for functiondef 'collect_memory_sample'
- Line 275: Missing docstring for functiondef '__init__'
- Line 279: Missing docstring for functiondef 'scan_networks'
- Line 306: Missing docstring for functiondef '__init__'
- Line 310: Missing docstring for functiondef 'scan_networks'
- Line 685: Missing docstring for functiondef 'make_connection'

### tests/test_sigint_exports.py
- Line 7: Missing docstring for functiondef 'test_export_csv'
- Line 15: Missing docstring for functiondef 'test_export_yaml'
- Line 25: Missing docstring for functiondef 'test_all_contains_export_yaml'
- Line 31: Missing docstring for functiondef 'test_export_json'

### src/piwardrive/core/persistence.py
- Line 278: Missing docstring for asyncfunctiondef '_acquire_conn'
- Line 291: Missing docstring for asyncfunctiondef '_release_conn'
- Line 299: Missing docstring for classdef '_ConnCtx'
- Line 300: Missing docstring for functiondef '__init__'
- Line 303: Missing docstring for asyncfunctiondef '__aenter__'
- Line 307: Missing docstring for asyncfunctiondef '__aexit__'

### src/piwardrive/diagnostics.py
- Line 309: Missing docstring for asyncfunctiondef '_poll'
- Line 356: Missing docstring for asyncfunctiondef '_run_summary'
- Line 425: Missing docstring for asyncfunctiondef '_run_export'
- Line 459: Missing docstring for functiondef '_cleanup_exports'

### scripts/dependency_audit.py
- Line 439: Missing docstring for functiondef 'main'

### comprehensive_code_analyzer.py
- Line 16: Missing docstring for classdef 'ComprehensiveCodeAnalyzer'
- Line 17: Missing docstring for functiondef '__init__'
- Line 300: Missing docstring for functiondef '__init__'

### tests/test_security.py
- Line 8: Missing docstring for functiondef 'test_hash_and_verify_password'
- Line 14: Missing docstring for functiondef 'test_validate_service_name'
- Line 20: Missing docstring for functiondef 'test_sanitize_path_valid'
- Line 26: Missing docstring for functiondef 'test_sanitize_path_invalid'
- Line 31: Missing docstring for functiondef 'test_validate_filename'
- Line 37: Missing docstring for functiondef 'test_sanitize_filename'

### tests/test_analysis_queries_cache.py
- Line 10: Missing docstring for classdef 'CallCounter'
- Line 19: Missing docstring for functiondef 'test_cached_fetch'
- Line 11: Missing docstring for functiondef '__init__'
- Line 14: Missing docstring for asyncfunctiondef '__call__'

### tests/test_start_kiosk_script.py
- Line 6: Missing docstring for functiondef 'test_start_kiosk_launches_browser'

### src/piwardrive/db/manager.py
- Line 16: Missing docstring for functiondef '__init__'
- Line 33: Missing docstring for asyncfunctiondef 'connect'
- Line 37: Missing docstring for asyncfunctiondef 'close'
- Line 48: Missing docstring for functiondef '_get_adapter'
- Line 56: Missing docstring for asyncfunctiondef 'execute'
- Line 63: Missing docstring for asyncfunctiondef 'executemany'
- Line 70: Missing docstring for asyncfunctiondef 'fetchall'
- Line 77: Missing docstring for functiondef 'get_metrics'

### scripts/compare_performance.py
- Line 20: Missing docstring for functiondef '__init__'

### src/piwardrive/map/vector_tiles.py
- Line 16: Missing docstring for functiondef '__init__'

### src/piwardrive/api/websockets/handlers.py
- Line 20: Missing docstring for asyncfunctiondef 'ws_aps'
- Line 58: Missing docstring for asyncfunctiondef 'sse_aps'
- Line 95: Missing docstring for asyncfunctiondef 'ws_status'
- Line 123: Missing docstring for asyncfunctiondef 'sse_status'
- Line 59: Missing docstring for asyncfunctiondef '_event_gen'
- Line 124: Missing docstring for asyncfunctiondef '_event_gen'

### src/piwardrive/widgets/net_throughput.py
- Line 19: Missing docstring for functiondef '__init__'

### tests/models/test_api_models.py
- Line 431: Missing docstring for classdef 'SimpleObject'
- Line 432: Missing docstring for functiondef '__init__'

### src/piwardrive/services/analysis_queries.py
- Line 24: Missing docstring for asyncfunctiondef '_cached_fetch'

### src/piwardrive/integrations/sigint_suite/cellular/tower_tracker/tracker.py
- Line 13: Missing docstring for functiondef '__init__'
- Line 31: Missing docstring for asyncfunctiondef '_get_conn'
- Line 38: Missing docstring for asyncfunctiondef '_init_db'

### tests/test_remote_sync_pkg.py
- Line 22: Missing docstring for classdef 'DummyResp'
- Line 33: Missing docstring for classdef 'DummySession'
- Line 51: Missing docstring for functiondef 'prepare'
- Line 60: Missing docstring for asyncfunctiondef 'run_sync'
- Line 74: Missing docstring for functiondef 'test_sync_database_file_missing'
- Line 80: Missing docstring for functiondef 'test_sync_database_retry'
- Line 86: Missing docstring for functiondef 'test_sync_database_failure'
- Line 106: Missing docstring for functiondef '_create_db'
- Line 124: Missing docstring for functiondef 'test_sync_new_records'
- Line 23: Missing docstring for asyncfunctiondef '__aenter__'
- Line 26: Missing docstring for asyncfunctiondef '__aexit__'
- Line 29: Missing docstring for functiondef 'raise_for_status'
- Line 34: Missing docstring for functiondef '__init__'
- Line 38: Missing docstring for asyncfunctiondef '__aenter__'
- Line 41: Missing docstring for asyncfunctiondef '__aexit__'
- Line 44: Missing docstring for functiondef 'post'
- Line 65: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 91: Missing docstring for classdef 'FailSession'
- Line 97: Missing docstring for asyncfunctiondef 'fake_sleep'
- Line 131: Missing docstring for asyncfunctiondef 'fake_sync'
- Line 92: Missing docstring for functiondef 'post'

### tests/test_main_application_fixed.py
- Line 67: Missing docstring for functiondef 'side_effect'
- Line 210: Missing docstring for functiondef 'mock_service_cmd_runner'

### tests/test_widget_manager.py
- Line 11: Missing docstring for functiondef '_setup_widget'
- Line 26: Missing docstring for functiondef 'test_lazy_manager_load'
- Line 38: Missing docstring for functiondef 'test_release_widget'
- Line 54: Missing docstring for functiondef 'test_memory_pressure_unloads'
- Line 58: Missing docstring for classdef 'DummyMonitor'
- Line 59: Missing docstring for functiondef '__init__'
- Line 63: Missing docstring for functiondef 'sample'

### tests/test_model_trainer.py
- Line 8: Missing docstring for classdef 'DummyScheduler'
- Line 20: Missing docstring for asyncfunctiondef '_fake_load'
- Line 24: Missing docstring for functiondef 'test_model_trainer_runs'
- Line 9: Missing docstring for functiondef '__init__'
- Line 12: Missing docstring for functiondef 'schedule'
- Line 16: Missing docstring for functiondef 'cancel'
- Line 27: Missing docstring for functiondef 'fit'

### tests/test_service_api.py
- Line 99: Missing docstring for asyncfunctiondef 'mock_call_next'
- Line 205: Missing docstring for asyncfunctiondef 'test_error'
- Line 223: Missing docstring for asyncfunctiondef 'test_exception'
- Line 378: Missing docstring for asyncfunctiondef 'test_sensitive_error'
- Line 426: Missing docstring for asyncfunctiondef 'test_endpoint'

### tests/test_wigle_integration.py
- Line 6: Missing docstring for classdef 'FakeResp'
- Line 23: Missing docstring for classdef 'FakeSession'
- Line 37: Missing docstring for functiondef 'test_fetch_wigle_networks'
- Line 67: Missing docstring for functiondef 'test_fetch_wigle_networks_cache'
- Line 7: Missing docstring for functiondef '__init__'
- Line 10: Missing docstring for asyncfunctiondef 'json'
- Line 13: Missing docstring for functiondef 'raise_for_status'
- Line 16: Missing docstring for asyncfunctiondef '__aenter__'
- Line 19: Missing docstring for asyncfunctiondef '__aexit__'
- Line 24: Missing docstring for functiondef '__init__'
- Line 27: Missing docstring for asyncfunctiondef '__aenter__'
- Line 30: Missing docstring for asyncfunctiondef '__aexit__'
- Line 33: Missing docstring for functiondef 'get'
- Line 73: Missing docstring for classdef 'Session'
- Line 74: Missing docstring for functiondef 'get'

### src/piwardrive/gpsd_client_async.py
- Line 46: Missing docstring for asyncfunctiondef '_connect'
- Line 63: Missing docstring for asyncfunctiondef '_ensure_connection'
- Line 80: Missing docstring for asyncfunctiondef '_poll'

### src/piwardrive/api/health/endpoints.py
- Line 25: Missing docstring for asyncfunctiondef 'get_status'
- Line 35: Missing docstring for asyncfunctiondef 'baseline_analysis_endpoint'
- Line 51: Missing docstring for asyncfunctiondef 'sync_records'
- Line 62: Missing docstring for asyncfunctiondef 'sse_history'
- Line 69: Missing docstring for asyncfunctiondef '_event_gen'

### src/piwardrive/api/analysis_queries/endpoints.py
- Line 14: Missing docstring for asyncfunctiondef 'get_evil_twins'
- Line 19: Missing docstring for asyncfunctiondef 'get_signal_strength'
- Line 24: Missing docstring for asyncfunctiondef 'get_network_security'
- Line 29: Missing docstring for asyncfunctiondef 'get_temporal_patterns'
- Line 34: Missing docstring for asyncfunctiondef 'get_mobile_devices'

### src/piwardrive/scheduler.py
- Line 45: Missing docstring for functiondef '_load_geofences'
- Line 61: Missing docstring for functiondef '_match_time'
- Line 119: Missing docstring for asyncfunctiondef '_runner'
- Line 156: Missing docstring for asyncfunctiondef '_call_update'
- Line 206: Missing docstring for asyncfunctiondef '_runner'
- Line 236: Missing docstring for functiondef '_call_update'

### src/piwardrive/performance/db_optimizer.py
- Line 54: Missing docstring for functiondef '__init__'
- Line 355: Missing docstring for functiondef '__init__'
- Line 360: Missing docstring for asyncfunctiondef '__aenter__'
- Line 377: Missing docstring for asyncfunctiondef '__aexit__'
- Line 458: Missing docstring for asyncfunctiondef 'main'

### src/piwardrive/jobs/analytics_jobs.py
- Line 24: Missing docstring for functiondef '__init__'
- Line 51: Missing docstring for functiondef 'enqueue'
- Line 52: Missing docstring for asyncfunctiondef '_run'

### src/piwardrive/widgets/network_density.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### src/piwardrive/widgets/device_classification.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### src/piwardrive/integrations/sigint_suite/enrichment/oui.py
- Line 118: Missing docstring for functiondef '_load_map'
- Line 148: Missing docstring for functiondef '_default_map'
- Line 30: Missing docstring for functiondef 'robust_request'
- Line 55: Missing docstring for classdef '_DummySession'
- Line 63: Missing docstring for functiondef 'robust_request'
- Line 56: Missing docstring for functiondef 'get'

### tests/test_new_widgets.py
- Line 5: Missing docstring for functiondef '_load'
- Line 14: Missing docstring for functiondef 'test_gps_status_widget'
- Line 23: Missing docstring for functiondef 'test_service_status_widget'
- Line 32: Missing docstring for functiondef 'test_handshake_counter_widget'
- Line 41: Missing docstring for functiondef 'test_storage_usage_widget'
- Line 50: Missing docstring for functiondef 'test_signal_strength_widget'
- Line 55: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 58: Missing docstring for functiondef 'fake_run'

### src/piwardrive/graphql_api.py
- Line 76: Missing docstring for asyncfunctiondef 'handle'

### src/piwardrive/migrations/004_create_gps_tracks.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 45: Missing docstring for asyncfunctiondef 'rollback'

### tests/test_cpu_pool.py
- Line 6: Missing docstring for functiondef '_square'
- Line 11: Missing docstring for asyncfunctiondef 'test_run_cpu_bound'

### src/piwardrive/migrations/006_create_network_fingerprints.py
- Line 13: Missing docstring for asyncfunctiondef 'apply'
- Line 43: Missing docstring for asyncfunctiondef 'rollback'

### src/piwardrive/services/report_generator.py
- Line 20: Missing docstring for functiondef '_load_template'
- Line 29: Missing docstring for functiondef '_render'

### src/piwardrive/widgets/gps_status.py
- Line 24: Missing docstring for functiondef '__init__'

### tests/test_service_api_fixed.py
- Line 94: Missing docstring for functiondef 'get_cpu_temp'
- Line 217: Missing docstring for classdef 'AuthMiddleware'
- Line 238: Missing docstring for classdef 'MockAuthMiddleware'
- Line 256: Missing docstring for asyncfunctiondef 'mock_call_next'
- Line 293: Missing docstring for asyncfunctiondef 'http_exception_handler'
- Line 300: Missing docstring for asyncfunctiondef 'test_error'
- Line 313: Missing docstring for asyncfunctiondef 'value_error_handler'
- Line 320: Missing docstring for asyncfunctiondef 'test_exception'
- Line 339: Missing docstring for asyncfunctiondef 'health_check'
- Line 358: Missing docstring for asyncfunctiondef 'get_status'
- Line 377: Missing docstring for functiondef 'get_user_info'
- Line 381: Missing docstring for asyncfunctiondef 'protected_endpoint'
- Line 436: Missing docstring for asyncfunctiondef 'health_check'
- Line 457: Missing docstring for asyncfunctiondef 'detailed_health'
- Line 484: Missing docstring for asyncfunctiondef 'check_service_health'
- Line 508: Missing docstring for asyncfunctiondef 'add_security_headers'
- Line 516: Missing docstring for asyncfunctiondef 'test_endpoint'
- Line 533: Missing docstring for classdef 'UserInput'
- Line 539: Missing docstring for asyncfunctiondef 'create_user'
- Line 559: Missing docstring for asyncfunctiondef 'value_error_handler'
- Line 567: Missing docstring for asyncfunctiondef 'sensitive_error'
- Line 602: Missing docstring for asyncfunctiondef 'add_security_headers'
- Line 609: Missing docstring for asyncfunctiondef 'general_exception_handler'
- Line 617: Missing docstring for asyncfunctiondef 'root'
- Line 621: Missing docstring for asyncfunctiondef 'health'
- Line 81: Missing docstring for functiondef 'get_cpu_temp'
- Line 110: Missing docstring for functiondef 'get_mem_usage'
- Line 123: Missing docstring for functiondef 'get_disk_usage'
- Line 137: Missing docstring for functiondef 'get_network_throughput'
- Line 161: Missing docstring for asyncfunctiondef 'service_status_async'
- Line 182: Missing docstring for functiondef 'run_service_cmd'
- Line 218: Missing docstring for functiondef '__init__'
- Line 221: Missing docstring for asyncfunctiondef '__call__'
- Line 239: Missing docstring for functiondef '__init__'
- Line 242: Missing docstring for asyncfunctiondef 'dispatch'
- Line 275: Missing docstring for asyncfunctiondef 'http_exception_handler'
- Line 279: Missing docstring for asyncfunctiondef 'general_exception_handler'

### src/piwardrive/core/config.py
- Line 345: Missing docstring for functiondef '_profile_path'
- Line 383: Missing docstring for functiondef '_load'

### src/piwardrive/widgets/heatmap.py
- Line 26: Missing docstring for functiondef '__init__'
- Line 42: Missing docstring for functiondef '_apply'

### tests/test_service_direct_import.py
- Line 82: Missing docstring for functiondef 'mock_create_app'

### src/piwardrive/integrations/sigint_suite/models.py
- Line 15: Missing docstring for functiondef '__getitem__'
- Line 18: Missing docstring for functiondef '__setitem__'

### src/piwardrive/direction_finding/hardware.py
- Line 310: Missing docstring for functiondef '__init__'
- Line 439: Missing docstring for functiondef '__init__'
- Line 655: Missing docstring for functiondef '__init__'

### tests/test_robust_request.py
- Line 6: Missing docstring for functiondef 'test_robust_request_retries'
- Line 37: Missing docstring for functiondef 'test_orientation_widget_update'
- Line 9: Missing docstring for functiondef 'fake_request'
- Line 17: Missing docstring for functiondef 'fake_sleep'

### tests/test_lazy_widget_loading.py
- Line 5: Missing docstring for functiondef 'test_lazy_loading'

### tests/test_battery_widget.py
- Line 5: Missing docstring for classdef 'DummyBattery'
- Line 11: Missing docstring for functiondef '_load_widget'
- Line 15: Missing docstring for functiondef 'test_widget_updates'
- Line 6: Missing docstring for functiondef '__init__'

### tests/test_exception_handler.py
- Line 10: Missing docstring for functiondef 'load_handler'
- Line 17: Missing docstring for classdef 'DummyLoop'
- Line 25: Missing docstring for functiondef 'test_install_sets_hooks'
- Line 45: Missing docstring for functiondef 'test_install_only_once'
- Line 18: Missing docstring for functiondef '__init__'
- Line 21: Missing docstring for functiondef 'set_exception_handler'
- Line 30: Missing docstring for functiondef 'sentinel'
- Line 50: Missing docstring for functiondef 'sentinel'

### tests/test_heatmap.py
- Line 6: Missing docstring for functiondef 'test_histogram_counts'
- Line 19: Missing docstring for functiondef 'test_histogram_points'
- Line 26: Missing docstring for functiondef 'test_density_map_expands_counts'
- Line 36: Missing docstring for functiondef 'test_coverage_map_binary'
- Line 44: Missing docstring for functiondef 'test_histogram_invalid_bins'
- Line 51: Missing docstring for functiondef 'test_density_map_invalid_radius'

### src/piwardrive/route_optimizer.py
- Line 36: Missing docstring for functiondef 'to_cell'

### tests/test_persistence.py
- Line 9: Missing docstring for functiondef 'setup_tmp'
- Line 13: Missing docstring for functiondef 'test_save_and_load_health_record'
- Line 27: Missing docstring for functiondef 'test_save_and_load_app_state'
- Line 36: Missing docstring for functiondef 'test_save_and_load_dashboard_settings'
- Line 48: Missing docstring for functiondef 'test_custom_db_path'
- Line 65: Missing docstring for functiondef 'test_purge_old_health'
- Line 80: Missing docstring for functiondef 'test_vacuum'
- Line 91: Missing docstring for functiondef 'test_conn_closed_on_loop_switch'
- Line 111: Missing docstring for functiondef 'test_schema_version'

### src/piwardrive/widgets/threat_map.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### tests/test_aggregation_service_main.py
- Line 6: Missing docstring for functiondef 'test_main_starts_uvicorn'

### tests/test_vehicle_sensors.py
- Line 6: Missing docstring for functiondef 'test_read_rpm_obd_missing'
- Line 11: Missing docstring for functiondef 'test_read_engine_load_obd_success'
- Line 12: Missing docstring for classdef 'DummyVal'
- Line 19: Missing docstring for classdef 'DummyConn'
- Line 13: Missing docstring for functiondef '__init__'
- Line 16: Missing docstring for functiondef 'to'
- Line 20: Missing docstring for functiondef 'query'

### tests/test_export.py
- Line 10: Missing docstring for functiondef 'test_filter_records'
- Line 38: Missing docstring for functiondef 'test_export_records_formats'
- Line 70: Missing docstring for functiondef 'test_estimate_location_from_rssi'
- Line 83: Missing docstring for functiondef 'test_export_map_kml'
- Line 101: Missing docstring for functiondef 'test_export_map_kml_compute_position'

### src/piwardrive/sigint_suite/cellular/tower_tracker/tracker.py
- Line 9: Missing docstring for classdef 'TowerTracker'
- Line 10: Missing docstring for functiondef '__init__'
- Line 13: Missing docstring for asyncfunctiondef 'update_tower'
- Line 16: Missing docstring for asyncfunctiondef 'get_tower'
- Line 19: Missing docstring for asyncfunctiondef 'all_towers'
- Line 22: Missing docstring for asyncfunctiondef 'log_wifi'
- Line 25: Missing docstring for asyncfunctiondef 'log_bluetooth'
- Line 28: Missing docstring for asyncfunctiondef 'wifi_history'
- Line 31: Missing docstring for asyncfunctiondef 'bluetooth_history'
- Line 34: Missing docstring for asyncfunctiondef 'log_tower'
- Line 37: Missing docstring for asyncfunctiondef 'tower_history'
- Line 40: Missing docstring for asyncfunctiondef 'close'

### src/piwardrive/routes/websocket.py
- Line 18: Missing docstring for asyncfunctiondef 'ws_detections'
- Line 36: Missing docstring for asyncfunctiondef 'sse_detections'
- Line 37: Missing docstring for asyncfunctiondef '_gen'

### scripts/performance_monitor.py
- Line 39: Missing docstring for functiondef '__post_init__'
- Line 59: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/service_status.py
- Line 24: Missing docstring for functiondef '__init__'

### tests/test_log_viewer.py
- Line 7: Missing docstring for functiondef 'test_log_viewer_filter_regex'
- Line 15: Missing docstring for functiondef 'test_log_viewer_no_filter'
- Line 23: Missing docstring for functiondef 'test_log_viewer_path_menu'

### src/piwardrive/db/sqlite.py
- Line 14: Missing docstring for functiondef '__init__'
- Line 29: Missing docstring for asyncfunctiondef '_create_conn'
- Line 47: Missing docstring for asyncfunctiondef 'connect'
- Line 59: Missing docstring for asyncfunctiondef '_close_pool'
- Line 64: Missing docstring for asyncfunctiondef 'close'
- Line 72: Missing docstring for asyncfunctiondef '_acquire'
- Line 90: Missing docstring for asyncfunctiondef '_release'
- Line 96: Missing docstring for asyncfunctiondef 'execute'
- Line 102: Missing docstring for asyncfunctiondef 'executemany'
- Line 108: Missing docstring for asyncfunctiondef 'fetchall'
- Line 115: Missing docstring for asyncfunctiondef 'transaction'
- Line 127: Missing docstring for functiondef 'get_metrics'

### src/piwardrive/heatmap.py
- Line 28: Missing docstring for functiondef '_derive_bounds'
- Line 34: Missing docstring for functiondef '_fill_histogram'

### src/piwardrive/services/coordinator.py
- Line 81: Missing docstring for asyncfunctiondef '_push_config'

### scripts/performance_cli.py
- Line 296: Missing docstring for asyncfunctiondef 'test_operation'

### src/piwardrive/widgets/cpu_temp_graph.py
- Line 18: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/detection_rate.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### tests/test_scheduler_tasks.py
- Line 174: Missing docstring for functiondef 'failing_task'
- Line 243: Missing docstring for asyncfunctiondef 'mock_async_task'
- Line 259: Missing docstring for asyncfunctiondef 'counting_task'
- Line 285: Missing docstring for asyncfunctiondef 'failing_task'
- Line 288: Missing docstring for asyncfunctiondef 'success_task'
- Line 316: Missing docstring for asyncfunctiondef 'task1'
- Line 320: Missing docstring for asyncfunctiondef 'task2'
- Line 364: Missing docstring for asyncfunctiondef 'test_task'
- Line 380: Missing docstring for asyncfunctiondef 'test_task'
- Line 410: Missing docstring for asyncfunctiondef 'priority_task'
- Line 438: Missing docstring for asyncfunctiondef 'failing_task'
- Line 441: Missing docstring for asyncfunctiondef 'success_task'
- Line 465: Missing docstring for asyncfunctiondef 'slow_task'
- Line 489: Missing docstring for asyncfunctiondef 'calculation_task'
- Line 649: Missing docstring for functiondef 'cpu_task'
- Line 680: Missing docstring for asyncfunctiondef 'concurrent_task'
- Line 714: Missing docstring for asyncfunctiondef 'throughput_task'
- Line 752: Missing docstring for functiondef 'failing_task'
- Line 757: Missing docstring for functiondef 'success_task'
- Line 783: Missing docstring for asyncfunctiondef 'failing_task'
- Line 788: Missing docstring for asyncfunctiondef 'success_task'
- Line 816: Missing docstring for asyncfunctiondef 'sometimes_failing_task'

### tests/test_parsers.py
- Line 7: Missing docstring for functiondef 'test_parse_imsi_output'
- Line 30: Missing docstring for functiondef 'test_parse_band_output'

### src/piwardrive/jobs/maintenance_jobs.py
- Line 20: Missing docstring for functiondef '__init__'
- Line 59: Missing docstring for functiondef 'enqueue'
- Line 60: Missing docstring for asyncfunctiondef '_run'

### src/piwardrive/widgets/base.py
- Line 13: Missing docstring for functiondef '__init__'

### src/piwardrive/migrations/007_create_suspicious_activities.py
- Line 11: Missing docstring for asyncfunctiondef 'apply'
- Line 45: Missing docstring for asyncfunctiondef 'rollback'

### tests/test_di.py
- Line 9: Missing docstring for functiondef 'test_register_instance_and_resolve'
- Line 17: Missing docstring for functiondef 'test_register_factory_and_single_instance'
- Line 28: Missing docstring for functiondef 'test_resolve_missing_key_raises'
- Line 34: Missing docstring for functiondef 'test_concurrent_resolve_creates_single_instance'
- Line 39: Missing docstring for functiondef 'factory'
- Line 48: Missing docstring for functiondef 'worker'

### tests/test_service_main.py
- Line 8: Missing docstring for functiondef 'test_main_starts_uvicorn'

### tests/test_prune_db_script.py
- Line 4: Missing docstring for functiondef 'test_prune_db_script'
- Line 7: Missing docstring for asyncfunctiondef 'fake_prune'

### src/piwardrive/lora_scanner.py
- Line 173: Missing docstring for functiondef '_to_float'
- Line 214: Missing docstring for functiondef '_to_float'
- Line 326: Missing docstring for functiondef '_repeat'

### src/piwardrive/unified_platform.py
- Line 544: Missing docstring for functiondef 'run_scan'
- Line 779: Missing docstring for functiondef 'run_api'
- Line 785: Missing docstring for functiondef 'run_dashboard'

### src/piwardrive/widgets/vehicle_speed.py
- Line 24: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/database_health.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### src/piwardrive/widgets/threat_level.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### tests/test_orientation_sensors_pkg.py
- Line 8: Missing docstring for functiondef 'test_orientation_to_angle_pkg'
- Line 14: Missing docstring for functiondef 'test_orientation_to_angle_custom_map_pkg'
- Line 19: Missing docstring for functiondef 'test_update_orientation_map_pkg'
- Line 27: Missing docstring for functiondef 'test_get_orientation_dbus_missing_pkg'
- Line 32: Missing docstring for functiondef 'test_get_orientation_dbus_success_pkg'
- Line 60: Missing docstring for functiondef 'test_read_mpu6050_missing_pkg'
- Line 65: Missing docstring for functiondef 'test_read_mpu6050_success_pkg'
- Line 81: Missing docstring for functiondef 'test_read_mpu6050_env_pkg'
- Line 99: Missing docstring for functiondef 'test_reset_orientation_map_unsafe_pkg'
- Line 33: Missing docstring for classdef 'DummyIface'
- Line 46: Missing docstring for classdef 'DummyBus'
- Line 50: Missing docstring for functiondef 'interface'
- Line 66: Missing docstring for classdef 'DummySensor'
- Line 82: Missing docstring for classdef 'DummySensor'
- Line 34: Missing docstring for functiondef 'HasAccelerometer'
- Line 37: Missing docstring for functiondef 'ClaimAccelerometer'
- Line 40: Missing docstring for functiondef 'ReleaseAccelerometer'
- Line 43: Missing docstring for functiondef 'GetAccelerometerOrientation'
- Line 47: Missing docstring for functiondef 'get_object'
- Line 67: Missing docstring for functiondef '__init__'
- Line 70: Missing docstring for functiondef 'get_accel_data'
- Line 73: Missing docstring for functiondef 'get_gyro_data'
- Line 83: Missing docstring for functiondef '__init__'
- Line 86: Missing docstring for functiondef 'get_accel_data'
- Line 89: Missing docstring for functiondef 'get_gyro_data'

### tests/test_analysis_queries_service.py
- Line 6: Missing docstring for functiondef '_get_service'
- Line 40: Missing docstring for asyncfunctiondef '_make_request'
- Line 49: Missing docstring for asyncfunctiondef '_dummy_result'
- Line 53: Missing docstring for functiondef 'test_analysis_endpoints'
- Line 17: Missing docstring for classdef 'MetricsResult'
- Line 24: Missing docstring for asyncfunctiondef '_dummy_async'
- Line 71: Missing docstring for asyncfunctiondef 'run_tests'

### src/piwardrive/widgets/db_stats.py
- Line 23: Missing docstring for functiondef '_db_path'
- Line 68: Missing docstring for functiondef '_apply'

### tests/test_orientation_sensors.py
- Line 17: Missing docstring for functiondef 'test_orientation_to_angle'
- Line 23: Missing docstring for functiondef 'test_orientation_to_angle_custom_map'
- Line 28: Missing docstring for functiondef 'test_update_orientation_map'
- Line 36: Missing docstring for functiondef 'test_update_orientation_map_clone'
- Line 44: Missing docstring for functiondef 'test_get_orientation_dbus_missing'
- Line 53: Missing docstring for functiondef 'test_get_orientation_dbus_success'
- Line 86: Missing docstring for functiondef 'test_get_heading'
- Line 92: Missing docstring for functiondef 'test_get_heading_none'
- Line 97: Missing docstring for functiondef 'test_read_mpu6050_missing'
- Line 106: Missing docstring for functiondef 'test_read_mpu6050_success'
- Line 128: Missing docstring for functiondef 'test_read_mpu6050_env'
- Line 152: Missing docstring for functiondef 'test_reset_orientation_map_env'
- Line 166: Missing docstring for functiondef 'test_reset_orientation_map_invalid'
- Line 178: Missing docstring for functiondef 'test_reset_orientation_map_unsafe'
- Line 54: Missing docstring for classdef 'DummyIface'
- Line 67: Missing docstring for classdef 'DummyBus'
- Line 71: Missing docstring for functiondef 'interface'
- Line 107: Missing docstring for classdef 'DummySensor'
- Line 129: Missing docstring for classdef 'DummySensor'
- Line 55: Missing docstring for functiondef 'HasAccelerometer'
- Line 58: Missing docstring for functiondef 'ClaimAccelerometer'
- Line 61: Missing docstring for functiondef 'ReleaseAccelerometer'
- Line 64: Missing docstring for functiondef 'GetAccelerometerOrientation'
- Line 68: Missing docstring for functiondef 'get_object'
- Line 108: Missing docstring for functiondef '__init__'
- Line 111: Missing docstring for functiondef 'get_accel_data'
- Line 114: Missing docstring for functiondef 'get_gyro_data'
- Line 130: Missing docstring for functiondef '__init__'
- Line 133: Missing docstring for functiondef 'get_accel_data'
- Line 136: Missing docstring for functiondef 'get_gyro_data'

### tests/test_network_analytics.py
- Line 26: Missing docstring for functiondef 'test_empty_records_returns_empty'
- Line 30: Missing docstring for functiondef 'test_open_network_flagged'
- Line 35: Missing docstring for functiondef 'test_duplicate_bssid_multiple_ssids_flagged_second_only'
- Line 42: Missing docstring for functiondef 'test_missing_fields_handled'
- Line 49: Missing docstring for functiondef 'test_open_and_duplicate_combined'
- Line 57: Missing docstring for functiondef 'test_duplicate_bssid_same_ssid_not_flagged'
- Line 64: Missing docstring for functiondef 'test_wep_network_flagged'
- Line 69: Missing docstring for functiondef 'test_unknown_vendor_flagged'
- Line 75: Missing docstring for functiondef 'test_duplicate_bssid_three_ssids_flagged_second_third_only'
- Line 83: Missing docstring for functiondef 'test_open_network_case_insensitive'
- Line 88: Missing docstring for functiondef 'test_duplicate_and_unknown_vendor_flagged'
- Line 96: Missing docstring for functiondef 'test_cluster_by_signal_returns_centroids'
- Line 139: Missing docstring for functiondef 'test_detect_rogue_devices_combines_checks'
- Line 20: Missing docstring for functiondef 'fake_lookup'

### src/piwardrive/testing/automated_framework.py
- Line 106: Missing docstring for functiondef '__init__'
- Line 362: Missing docstring for functiondef '__init__'
- Line 560: Missing docstring for functiondef '__init__'
- Line 725: Missing docstring for functiondef '__init__'
- Line 973: Missing docstring for functiondef '__init__'
- Line 1025: Missing docstring for functiondef 'continuous_test_loop'
- Line 377: Missing docstring for functiondef 'is_prime'
- Line 574: Missing docstring for functiondef 'cpu_stress_worker'

### src/piwardrive/memory_monitor.py
- Line 43: Missing docstring for functiondef '_check_leak'

### src/piwardrive/widgets/log_viewer.py
- Line 33: Missing docstring for functiondef '__init__'
- Line 46: Missing docstring for functiondef '_compile_filter'
- Line 49: Missing docstring for functiondef '_compile_error'
- Line 52: Missing docstring for functiondef '_update_text_size'
- Line 55: Missing docstring for functiondef '_update_height'
- Line 60: Missing docstring for functiondef '_refresh'

### src/piwardrive/widgets/alert_summary.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### src/piwardrive/mysql_export.py
- Line 470: Missing docstring for asyncfunctiondef '_bulk_insert'

### tests/test_config_env_webhooks.py
- Line 6: Missing docstring for functiondef 'setup_tmp'
- Line 17: Missing docstring for functiondef 'test_env_override_list'

### src/piwardrive/services/security_analyzer.py
- Line 18: Missing docstring for functiondef '_make_row'

### tests/test_imsi_catcher.py
- Line 11: Missing docstring for functiondef 'test_scan_imsis_parses_output_and_tags_location'
- Line 39: Missing docstring for functiondef 'test_scan_imsis_custom_hook'
- Line 50: Missing docstring for functiondef 'add_op'

### tests/test_core_config.py
- Line 560: Missing docstring for functiondef 'save_config_worker'

### tests/test_export_logs_script.py
- Line 5: Missing docstring for functiondef 'test_export_logs_script'
- Line 8: Missing docstring for asyncfunctiondef 'fake_export'
- Line 13: Missing docstring for classdef 'DummyApp'
- Line 14: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/__init__.py
- Line 234: Missing docstring for functiondef '__getattr__'
- Line 17: Missing docstring for functiondef 'format_error'
- Line 20: Missing docstring for functiondef 'report_error'
- Line 184: Missing docstring for functiondef '_loader'

### src/piwardrive/route_prefetch.py
- Line 78: Missing docstring for functiondef '_predict_points'
- Line 95: Missing docstring for functiondef '_run'

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 9: Missing docstring for functiondef 'test_plot_cpu_temp_plotly_backend'
- Line 10: Missing docstring for classdef 'FakeSeries'
- Line 31: Missing docstring for classdef 'FakeDataFrame'
- Line 11: Missing docstring for functiondef 'rolling'
- Line 32: Missing docstring for functiondef '__init__'
- Line 35: Missing docstring for functiondef '__getitem__'
- Line 41: Missing docstring for functiondef '__setitem__'
- Line 44: Missing docstring for functiondef 'sort_values'
- Line 12: Missing docstring for classdef 'Roll'
- Line 13: Missing docstring for functiondef '__init__'
- Line 16: Missing docstring for functiondef 'mean'

### tests/test_continuous_scan.py
- Line 8: Missing docstring for functiondef 'test_scan_once_returns_data'
- Line 16: Missing docstring for functiondef 'test_run_continuous_scan_iterations'
- Line 45: Missing docstring for functiondef 'test_run_once_writes_json'
- Line 58: Missing docstring for functiondef 'test_main_runs_iterations'
- Line 19: Missing docstring for asyncfunctiondef 'fake_wifi'
- Line 22: Missing docstring for asyncfunctiondef 'fake_bt'
- Line 30: Missing docstring for asyncfunctiondef 'fast_sleep'
- Line 61: Missing docstring for functiondef 'fake_save'
- Line 66: Missing docstring for asyncfunctiondef 'fake_wifi'
- Line 69: Missing docstring for asyncfunctiondef 'fake_bt'
- Line 77: Missing docstring for asyncfunctiondef 'fast_sleep'

### tests/test_logging_filters.py
- Line 7: Missing docstring for functiondef 'test_content_filter_include_exclude'
- Line 25: Missing docstring for functiondef 'test_rate_limiter'
- Line 35: Missing docstring for functiondef 'test_sensitive_data_redaction'

### src/piwardrive/api/analytics/endpoints.py
- Line 20: Missing docstring for asyncfunctiondef 'get_network_analytics'
- Line 33: Missing docstring for asyncfunctiondef 'get_daily_stats'
- Line 46: Missing docstring for asyncfunctiondef 'get_coverage_grid'
- Line 55: Missing docstring for asyncfunctiondef 'get_lifecycle_forecast'
- Line 66: Missing docstring for asyncfunctiondef 'get_capacity_forecast'
- Line 76: Missing docstring for asyncfunctiondef 'get_predictive_summary'

### tests/test_interfaces.py
- Line 42: Missing docstring for classdef 'TestMapService'
- Line 174: Missing docstring for functiondef 'mock_generator'
- Line 211: Missing docstring for classdef 'TestDataCollector'
- Line 354: Missing docstring for classdef 'MockMapService'
- Line 361: Missing docstring for classdef 'MockDataCollector'
- Line 43: Missing docstring for functiondef 'get_current_position'
- Line 46: Missing docstring for functiondef 'fetch_access_points'
- Line 212: Missing docstring for functiondef 'collect'
- Line 355: Missing docstring for functiondef 'get_current_position'
- Line 358: Missing docstring for functiondef 'fetch_access_points'
- Line 362: Missing docstring for functiondef 'collect'

### tests/test_sync_receiver.py
- Line 8: Missing docstring for functiondef '_load_receiver'
- Line 23: Missing docstring for functiondef 'test_rejects_traversal'
- Line 30: Missing docstring for functiondef 'test_rejects_nested_traversal'
- Line 37: Missing docstring for functiondef 'test_rejects_evil_db'
- Line 9: Missing docstring for functiondef 'fake_expand'

### tests/test_scheduler_system.py
- Line 75: Missing docstring for functiondef 'test_func'
- Line 96: Missing docstring for functiondef 'failing_task'
- Line 121: Missing docstring for functiondef 'high_priority_task'
- Line 124: Missing docstring for functiondef 'low_priority_task'
- Line 157: Missing docstring for functiondef 'task_a'
- Line 160: Missing docstring for functiondef 'task_b'
- Line 196: Missing docstring for functiondef 'test_task'
- Line 299: Missing docstring for functiondef 'test_func'
- Line 316: Missing docstring for functiondef 'failing_task'
- Line 340: Missing docstring for functiondef 'flaky_task'
- Line 372: Missing docstring for functiondef 'long_running_task'
- Line 422: Missing docstring for asyncfunctiondef 'async_task'
- Line 440: Missing docstring for asyncfunctiondef 'failing_async_task'
- Line 464: Missing docstring for asyncfunctiondef 'concurrent_task'
- Line 498: Missing docstring for functiondef 'db_task'
- Line 520: Missing docstring for functiondef 'widget_task'
- Line 542: Missing docstring for functiondef 'notification_task'
- Line 570: Missing docstring for functiondef 'high_freq_task'
- Line 592: Missing docstring for functiondef 'create_task_func'
- Line 593: Missing docstring for functiondef 'task_func'

### tests/test_webui_server.py
- Line 17: Missing docstring for functiondef 'test_webui_serves_static_and_api'

### scripts/health_stats.py
- Line 18: Missing docstring for asyncfunctiondef '_load_records'

### tests/test_web_server.py
- Line 20: Missing docstring for functiondef 'test_web_server_serves_static_and_api'
- Line 30: Missing docstring for functiondef 'fake_join'
- Line 40: Missing docstring for functiondef 'fake_isdir'

### tests/test_core_application.py
- Line 285: Missing docstring for functiondef 'failing_service_cmd'

### scripts/calibrate_orientation.py
- Line 15: Missing docstring for functiondef '_prompt'

### src/piwardrive/export.py
- Line 47: Missing docstring for functiondef '_matches'
- Line 174: Missing docstring for functiondef '_create_writer'
- Line 182: Missing docstring for functiondef '_add_fields'
- Line 188: Missing docstring for functiondef '_add_records'
- Line 272: Missing docstring for functiondef '_add_point'
- Line 279: Missing docstring for functiondef '_add_records'
- Line 308: Missing docstring for functiondef '_write_kmz'

### scripts/localize_aps.py
- Line 20: Missing docstring for functiondef '_save_map'
- Line 34: Missing docstring for functiondef 'main'

### src/piwardrive/integrations/sigint_suite/bluetooth/scanner.py
- Line 23: Missing docstring for functiondef '_allowed'

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 25: Missing docstring for functiondef '_allowed'
- Line 51: Missing docstring for functiondef 'finalize'
- Line 65: Missing docstring for functiondef 'parse_info'

### src/piwardrive/widgets/disk_trend.py
- Line 18: Missing docstring for functiondef '__init__'

### tests/test_security_analyzer_integration.py
- Line 4: Missing docstring for functiondef 'test_detect_hidden_ssids'
- Line 17: Missing docstring for functiondef 'test_detect_evil_twins'

### src/piwardrive/config_watcher.py
- Line 23: Missing docstring for functiondef '__init__'

### tests/staging/test_staging_environment.py
- Line 36: Missing docstring for functiondef '__init__'
- Line 198: Missing docstring for functiondef 'make_request'
- Line 243: Missing docstring for asyncfunctiondef 'make_async_request'
- Line 250: Missing docstring for asyncfunctiondef 'run_load_test'

### tests/test_sigint_plugins.py
- Line 5: Missing docstring for functiondef 'test_sigint_plugin_loaded'
- Line 20: Missing docstring for functiondef 'test_sigint_plugin_error'

### tests/test_config_watcher.py
- Line 6: Missing docstring for functiondef 'test_watch_config_triggers'

### src/piwardrive/api/widget_marketplace.py
- Line 18: Missing docstring for functiondef '_load_market'

### src/remote_sync/__init__.py
- Line 103: Missing docstring for functiondef '_load_sync_state'
- Line 111: Missing docstring for functiondef '_save_sync_state'

### src/piwardrive/performance/optimization.py
- Line 123: Missing docstring for functiondef '__init__'
- Line 239: Missing docstring for functiondef '__init__'
- Line 395: Missing docstring for functiondef '__init__'
- Line 450: Missing docstring for functiondef '__init__'
- Line 618: Missing docstring for functiondef '__init__'
- Line 706: Missing docstring for functiondef '__init__'
- Line 793: Missing docstring for functiondef '__init__'
- Line 852: Missing docstring for functiondef '__init__'

### src/piwardrive/api/system/endpoints.py
- Line 30: Missing docstring for asyncfunctiondef 'get_cpu'
- Line 40: Missing docstring for asyncfunctiondef 'get_ram'
- Line 45: Missing docstring for asyncfunctiondef 'get_storage'
- Line 52: Missing docstring for asyncfunctiondef 'get_orientation_endpoint'
- Line 76: Missing docstring for asyncfunctiondef 'get_vehicle_endpoint'
- Line 89: Missing docstring for asyncfunctiondef 'get_gps_endpoint'
- Line 123: Missing docstring for asyncfunctiondef 'get_logs'
- Line 140: Missing docstring for asyncfunctiondef 'get_db_stats_endpoint'
- Line 152: Missing docstring for asyncfunctiondef 'db_health_endpoint'
- Line 162: Missing docstring for asyncfunctiondef 'db_index_usage_endpoint'
- Line 169: Missing docstring for asyncfunctiondef 'lora_scan_endpoint'
- Line 177: Missing docstring for asyncfunctiondef 'control_service_endpoint'
- Line 191: Missing docstring for asyncfunctiondef 'get_service_status_endpoint'
- Line 199: Missing docstring for asyncfunctiondef 'get_config_endpoint'
- Line 204: Missing docstring for asyncfunctiondef 'update_config_endpoint'
- Line 224: Missing docstring for asyncfunctiondef 'get_webhooks_endpoint'
- Line 232: Missing docstring for asyncfunctiondef 'update_webhooks_endpoint'
- Line 242: Missing docstring for asyncfunctiondef 'list_fingerprints_endpoint'
- Line 250: Missing docstring for asyncfunctiondef 'add_fingerprint_endpoint'
- Line 263: Missing docstring for asyncfunctiondef 'list_geofences_endpoint'
- Line 270: Missing docstring for asyncfunctiondef 'add_geofence_endpoint'
- Line 287: Missing docstring for asyncfunctiondef 'update_geofence_endpoint'
- Line 307: Missing docstring for asyncfunctiondef 'remove_geofence_endpoint'
- Line 325: Missing docstring for asyncfunctiondef 'export_access_points'
- Line 341: Missing docstring for asyncfunctiondef 'export_bluetooth'

### src/piwardrive/direction_finding/integration.py
- Line 23: Missing docstring for functiondef '__init__'

### src/piwardrive/widgets/system_resource.py
- Line 18: Missing docstring for functiondef '__init__'
- Line 26: Missing docstring for functiondef 'update'

### src/piwardrive/cache.py
- Line 26: Missing docstring for functiondef '_key'

### tests/test_web_server_missing.py
- Line 8: Missing docstring for functiondef 'test_create_app_missing_dist'
- Line 17: Missing docstring for functiondef 'fake_join'

### tests/test_widget_system_comprehensive.py
- Line 46: Missing docstring for classdef 'TestWidget'
- Line 253: Missing docstring for classdef 'MockWidget'
- Line 279: Missing docstring for classdef 'AsyncWidget'
- Line 294: Missing docstring for asyncfunctiondef 'test_async_update'
- Line 303: Missing docstring for classdef 'ErrorWidget'
- Line 366: Missing docstring for classdef 'TestWidget'
- Line 392: Missing docstring for classdef 'MockWidgetRegistry'
- Line 407: Missing docstring for classdef 'MockWidgetRegistry'
- Line 420: Missing docstring for classdef 'TestWidget'
- Line 481: Missing docstring for classdef 'TestWidget'
- Line 47: Missing docstring for functiondef 'render'
- Line 50: Missing docstring for functiondef 'update'
- Line 254: Missing docstring for functiondef '__init__'
- Line 257: Missing docstring for functiondef 'render'
- Line 260: Missing docstring for functiondef 'update'
- Line 280: Missing docstring for functiondef '__init__'
- Line 283: Missing docstring for functiondef 'render'
- Line 286: Missing docstring for asyncfunctiondef 'update_async'
- Line 304: Missing docstring for functiondef 'render'
- Line 307: Missing docstring for functiondef 'update'
- Line 367: Missing docstring for functiondef 'render'
- Line 370: Missing docstring for functiondef 'update'
- Line 393: Missing docstring for functiondef '__init__'
- Line 396: Missing docstring for functiondef 'register'
- Line 399: Missing docstring for functiondef 'get'
- Line 408: Missing docstring for functiondef '__init__'
- Line 411: Missing docstring for functiondef 'register'
- Line 414: Missing docstring for functiondef 'get'
- Line 421: Missing docstring for functiondef 'render'
- Line 424: Missing docstring for functiondef 'update'
- Line 482: Missing docstring for functiondef '__init__'
- Line 485: Missing docstring for functiondef 'render'
- Line 488: Missing docstring for functiondef 'update'

### tests/test_scan_report.py
- Line 11: Missing docstring for asyncfunctiondef 'test_generate_scan_report'
- Line 12: Missing docstring for asyncfunctiondef 'fake_load'

### tests/test_analysis_extra.py
- Line 21: Missing docstring for functiondef 'test_compute_health_stats_empty'
- Line 25: Missing docstring for functiondef 'test_plot_cpu_temp_matplotlib_backend'
- Line 90: Missing docstring for functiondef 'test_plot_cpu_temp_no_pandas'
- Line 110: Missing docstring for functiondef 'test_plot_cpu_temp_plotly'
- Line 26: Missing docstring for classdef 'FakeSeries'
- Line 47: Missing docstring for classdef 'FakeDataFrame'
- Line 111: Missing docstring for classdef 'FakeSeries'
- Line 132: Missing docstring for classdef 'FakeDataFrame'
- Line 27: Missing docstring for functiondef 'rolling'
- Line 48: Missing docstring for functiondef '__init__'
- Line 51: Missing docstring for functiondef '__getitem__'
- Line 57: Missing docstring for functiondef '__setitem__'
- Line 60: Missing docstring for functiondef 'sort_values'
- Line 112: Missing docstring for functiondef 'rolling'
- Line 133: Missing docstring for functiondef '__init__'
- Line 136: Missing docstring for functiondef '__getitem__'
- Line 142: Missing docstring for functiondef '__setitem__'
- Line 145: Missing docstring for functiondef 'sort_values'
- Line 28: Missing docstring for classdef 'Roll'
- Line 113: Missing docstring for classdef 'Roll'
- Line 29: Missing docstring for functiondef '__init__'
- Line 32: Missing docstring for functiondef 'mean'
- Line 114: Missing docstring for functiondef '__init__'
- Line 117: Missing docstring for functiondef 'mean'

### tests/test_sigint_integration.py
- Line 7: Missing docstring for functiondef 'test_load_sigint_data'
- Line 20: Missing docstring for functiondef 'test_load_sigint_data_missing'

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 16: Missing docstring for functiondef 'normalise'

### src/piwardrive/api/websockets/events.py
- Line 16: Missing docstring for asyncfunctiondef '_gen'

### tests/test_vector_tile_customizer_cli.py
- Line 4: Missing docstring for functiondef 'test_vector_tile_customizer_cli_build'
- Line 18: Missing docstring for functiondef 'test_vector_tile_customizer_cli_style'
- Line 10: Missing docstring for functiondef 'fake_build'
- Line 24: Missing docstring for functiondef 'fake_style'

### tests/test_route_prefetch.py
- Line 8: Missing docstring for functiondef '_haversine'
- Line 26: Missing docstring for classdef 'DummyScheduler'
- Line 38: Missing docstring for classdef 'DummyMap'
- Line 51: Missing docstring for functiondef 'test_route_prefetcher_runs'
- Line 75: Missing docstring for functiondef 'test_route_prefetcher_no_points'
- Line 99: Missing docstring for functiondef 'test_predict_points'
- Line 124: Missing docstring for functiondef 'test_zero_lookahead'
- Line 27: Missing docstring for functiondef '__init__'
- Line 30: Missing docstring for functiondef 'schedule'
- Line 34: Missing docstring for functiondef 'cancel'
- Line 39: Missing docstring for functiondef '__init__'
- Line 44: Missing docstring for functiondef 'prefetch_tiles'

### src/piwardrive/widgets/handshake_counter.py
- Line 24: Missing docstring for functiondef '__init__'

### tests/test_config_runtime.py
- Line 6: Missing docstring for functiondef 'setup_tmp'
- Line 14: Missing docstring for functiondef 'test_config_mtime_updates'
- Line 26: Missing docstring for functiondef 'test_config_mtime_returns_timestamp'

### tests/test_tower_tracking.py
- Line 25: Missing docstring for asyncfunctiondef 'test_tracker_update_and_query'
- Line 37: Missing docstring for asyncfunctiondef 'test_wifi_and_bluetooth_logging'
- Line 54: Missing docstring for asyncfunctiondef 'test_async_logging_and_retrieval'
- Line 67: Missing docstring for asyncfunctiondef 'test_tower_history'

### src/piwardrive/widget_manager.py
- Line 93: Missing docstring for functiondef '_plugin_dir'
- Line 97: Missing docstring for functiondef '_discover_plugins'
- Line 130: Missing docstring for functiondef '_load_widget_class'
- Line 140: Missing docstring for functiondef '_maybe_unload'

### scripts/generate_openapi.py
- Line 18: Missing docstring for functiondef 'main'

### tests/test_service.py
- Line 23: Missing docstring for classdef 'MetricsResult'
- Line 32: Missing docstring for asyncfunctiondef '_dummy_async'
- Line 52: Missing docstring for functiondef 'test_status_endpoint_returns_recent_records'
- Line 84: Missing docstring for functiondef 'test_status_auth_missing_credentials'
- Line 97: Missing docstring for functiondef 'test_widget_metrics_endpoint'
- Line 149: Missing docstring for functiondef 'test_logs_endpoint_returns_lines_async'
- Line 163: Missing docstring for functiondef 'test_logs_endpoint_handles_sync_function'
- Line 177: Missing docstring for functiondef 'test_logs_endpoint_allows_whitelisted_path'
- Line 192: Missing docstring for functiondef 'test_logs_endpoint_rejects_unknown_path'
- Line 210: Missing docstring for functiondef 'test_websocket_status_stream'
- Line 263: Missing docstring for functiondef 'test_sse_status_stream'
- Line 319: Missing docstring for functiondef 'test_ws_aps_stream'
- Line 344: Missing docstring for functiondef 'test_sse_aps_stream'
- Line 372: Missing docstring for functiondef 'test_websocket_timeout_closes_connection'
- Line 411: Missing docstring for functiondef 'test_get_config_endpoint'
- Line 420: Missing docstring for functiondef 'test_update_config_endpoint_success'
- Line 434: Missing docstring for functiondef 'test_update_config_endpoint_invalid_key'
- Line 442: Missing docstring for functiondef 'test_dashboard_settings_endpoints'
- Line 473: Missing docstring for functiondef 'test_widget_metrics_auth_missing_credentials'
- Line 501: Missing docstring for functiondef 'test_widget_metrics_auth_bad_password'
- Line 535: Missing docstring for functiondef 'test_cpu_endpoint'
- Line 548: Missing docstring for functiondef 'test_baseline_analysis_endpoint'
- Line 574: Missing docstring for functiondef 'test_ram_endpoint'
- Line 585: Missing docstring for functiondef 'test_storage_endpoint'
- Line 596: Missing docstring for functiondef 'test_gps_endpoint'
- Line 617: Missing docstring for functiondef 'test_service_control_endpoint_success'
- Line 628: Missing docstring for functiondef 'test_service_control_endpoint_failure'
- Line 640: Missing docstring for functiondef 'test_service_control_endpoint_invalid_action'
- Line 646: Missing docstring for functiondef 'test_service_status_endpoint'
- Line 657: Missing docstring for functiondef 'test_service_status_endpoint_inactive'
- Line 668: Missing docstring for functiondef 'test_db_stats_endpoint'
- Line 686: Missing docstring for functiondef 'test_lora_scan_endpoint'
- Line 701: Missing docstring for functiondef 'test_auth_login_valid'
- Line 61: Missing docstring for asyncfunctiondef '_mock'
- Line 98: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 150: Missing docstring for asyncfunctiondef 'fake_tail'
- Line 164: Missing docstring for functiondef 'fake_tail'
- Line 178: Missing docstring for asyncfunctiondef 'fake_tail'
- Line 195: Missing docstring for asyncfunctiondef 'fake_tail'
- Line 219: Missing docstring for asyncfunctiondef 'fake_load'
- Line 222: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 272: Missing docstring for asyncfunctiondef 'fake_load'
- Line 275: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 320: Missing docstring for asyncfunctiondef 'fake_load'
- Line 345: Missing docstring for asyncfunctiondef 'fake_load'
- Line 373: Missing docstring for asyncfunctiondef 'fake_load'
- Line 376: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 379: Missing docstring for asyncfunctiondef 'send_timeout'
- Line 448: Missing docstring for asyncfunctiondef 'fake_load'
- Line 451: Missing docstring for asyncfunctiondef 'fake_save'
- Line 474: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 502: Missing docstring for asyncfunctiondef 'fake_fetch'
- Line 551: Missing docstring for asyncfunctiondef 'fake_recent'
- Line 554: Missing docstring for asyncfunctiondef 'fake_base'
- Line 557: Missing docstring for functiondef 'fake_analyze'
- Line 669: Missing docstring for asyncfunctiondef 'fake_counts'
- Line 687: Missing docstring for asyncfunctiondef 'fake_scan'
- Line 704: Missing docstring for asyncfunctiondef 'fake_get_user'

### src/piwardrive/integrations/sigint_suite/continuous_scan.py
- Line 39: Missing docstring for asyncfunctiondef '_scan_once'

### src/piwardrive/migrations/runner.py
- Line 12: Missing docstring for asyncfunctiondef '_ensure_table'
- Line 19: Missing docstring for asyncfunctiondef '_applied_versions'

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 20: Missing docstring for functiondef '_allowed'
- Line 121: Missing docstring for functiondef 'main'

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 18: Missing docstring for functiondef '_allowed'
- Line 82: Missing docstring for functiondef 'main'

### src/piwardrive/resource_manager.py
- Line 90: Missing docstring for functiondef '_cancel_task'

### service.py
- Line 27: Missing docstring for functiondef '_proxy'
- Line 28: Missing docstring for functiondef 'wrapper'

### tests/test_health_import.py
- Line 9: Missing docstring for functiondef 'setup_tmp'
- Line 13: Missing docstring for functiondef 'test_import_json'
- Line 31: Missing docstring for functiondef 'test_import_csv'

### tests/test_performance.py
- Line 4: Missing docstring for functiondef 'test_record_metrics'

### tests/test_health_export.py
- Line 8: Missing docstring for functiondef 'test_export_json'
- Line 20: Missing docstring for functiondef 'test_export_csv'
- Line 11: Missing docstring for asyncfunctiondef 'fake_load'
- Line 23: Missing docstring for asyncfunctiondef 'fake_load'

### tests/test_advanced_localization.py
- Line 15: Missing docstring for functiondef 'test_kalman_1d_empty'
- Line 21: Missing docstring for functiondef 'test_kalman_1d_sample_values'
- Line 28: Missing docstring for functiondef 'test_kalman_1d_constant_series'
- Line 34: Missing docstring for functiondef 'test_apply_kalman_filter_changes_values'
- Line 45: Missing docstring for functiondef 'test_apply_kalman_filter_noop_when_disabled'
- Line 52: Missing docstring for functiondef 'test_remove_outliers_drops_points'
- Line 68: Missing docstring for functiondef 'test_rssi_to_distance'
- Line 73: Missing docstring for functiondef 'test_estimate_ap_location_centroid_weighted'
- Line 87: Missing docstring for functiondef 'test_localize_aps_returns_dict'

### tests/test_widget_system.py
- Line 36: Missing docstring for classdef 'TestWidget'
- Line 51: Missing docstring for classdef 'TestWidget'
- Line 68: Missing docstring for classdef 'TestWidget'
- Line 88: Missing docstring for classdef 'TestWidget1'
- Line 95: Missing docstring for classdef 'TestWidget2'
- Line 115: Missing docstring for classdef 'TestWidget'
- Line 134: Missing docstring for classdef 'TestWidget'
- Line 149: Missing docstring for classdef 'TestWidget1'
- Line 156: Missing docstring for classdef 'TestWidget2'
- Line 177: Missing docstring for classdef 'FailingWidget'
- Line 193: Missing docstring for classdef 'CountingWidget'
- Line 216: Missing docstring for classdef 'ConfigurableWidget'
- Line 253: Missing docstring for classdef 'TestWidget'
- Line 267: Missing docstring for classdef 'TestWidget'
- Line 281: Missing docstring for classdef 'TestWidget1'
- Line 288: Missing docstring for classdef 'TestWidget2'
- Line 374: Missing docstring for classdef 'DatabaseWidget'
- Line 395: Missing docstring for classdef 'SchedulerWidget'
- Line 419: Missing docstring for classdef 'ConfigWidget'
- Line 446: Missing docstring for classdef 'SlowWidget'
- Line 479: Missing docstring for classdef 'MemoryWidget'
- Line 503: Missing docstring for classdef 'ConcurrentWidget'
- Line 518: Missing docstring for functiondef 'access_widget'
- Line 546: Missing docstring for classdef 'ValidatingWidget'
- Line 582: Missing docstring for classdef 'SanitizingWidget'
- Line 37: Missing docstring for functiondef '__init__'
- Line 40: Missing docstring for functiondef 'get_data'
- Line 52: Missing docstring for functiondef '__init__'
- Line 55: Missing docstring for functiondef 'get_data'
- Line 69: Missing docstring for functiondef '__init__'
- Line 72: Missing docstring for functiondef 'get_data'
- Line 89: Missing docstring for functiondef '__init__'
- Line 92: Missing docstring for functiondef 'get_data'
- Line 96: Missing docstring for functiondef '__init__'
- Line 99: Missing docstring for functiondef 'get_data'
- Line 116: Missing docstring for functiondef '__init__'
- Line 120: Missing docstring for functiondef 'get_data'
- Line 123: Missing docstring for functiondef 'refresh'
- Line 135: Missing docstring for functiondef '__init__'
- Line 138: Missing docstring for functiondef 'get_data'
- Line 150: Missing docstring for functiondef '__init__'
- Line 153: Missing docstring for functiondef 'get_data'
- Line 157: Missing docstring for functiondef '__init__'
- Line 160: Missing docstring for functiondef 'get_data'
- Line 178: Missing docstring for functiondef '__init__'
- Line 181: Missing docstring for functiondef 'get_data'
- Line 194: Missing docstring for functiondef '__init__'
- Line 198: Missing docstring for functiondef 'get_data'
- Line 217: Missing docstring for functiondef '__init__'
- Line 221: Missing docstring for functiondef 'get_data'
- Line 224: Missing docstring for functiondef 'set_config'
- Line 254: Missing docstring for functiondef '__init__'
- Line 257: Missing docstring for functiondef 'get_data'
- Line 268: Missing docstring for functiondef '__init__'
- Line 271: Missing docstring for functiondef 'get_data'
- Line 282: Missing docstring for functiondef '__init__'
- Line 285: Missing docstring for functiondef 'get_data'
- Line 289: Missing docstring for functiondef '__init__'
- Line 292: Missing docstring for functiondef 'get_data'
- Line 375: Missing docstring for functiondef '__init__'
- Line 379: Missing docstring for functiondef 'get_data'
- Line 396: Missing docstring for functiondef '__init__'
- Line 400: Missing docstring for functiondef 'get_data'
- Line 420: Missing docstring for functiondef '__init__'
- Line 424: Missing docstring for functiondef 'get_data'
- Line 447: Missing docstring for functiondef '__init__'
- Line 451: Missing docstring for functiondef 'get_data'
- Line 480: Missing docstring for functiondef '__init__'
- Line 484: Missing docstring for functiondef 'get_data'
- Line 504: Missing docstring for functiondef '__init__'
- Line 508: Missing docstring for functiondef 'get_data'
- Line 547: Missing docstring for functiondef '__init__'
- Line 550: Missing docstring for functiondef 'get_data'
- Line 553: Missing docstring for functiondef 'set_config'
- Line 583: Missing docstring for functiondef '__init__'
- Line 586: Missing docstring for functiondef 'get_data'

### tests/test_memory_monitor.py
- Line 6: Missing docstring for functiondef 'test_memory_monitor_detects_growth'

### src/piwardrive/integrations/sigint_suite/cellular/tower_scanner/scanner.py
- Line 47: Missing docstring for functiondef '_allowed'

### tests/test_r_integration.py
- Line 12: Missing docstring for classdef 'DummyResult'
- Line 18: Missing docstring for functiondef 'test_health_summary_missing_rpy2'
- Line 32: Missing docstring for functiondef 'test_health_summary_no_plot'
- Line 53: Missing docstring for functiondef 'test_health_summary_with_plot'
- Line 13: Missing docstring for functiondef '__init__'
- Line 21: Missing docstring for functiondef 'fake_import'

### code_analysis.py
- Line 15: Missing docstring for classdef 'CodeAnalyzer'
- Line 16: Missing docstring for functiondef '__init__'

## Formatting Issues

### src/piwardrive/hardware/enhanced_hardware.py
- Line 142: E501 line too long (82 > 79 characters)
- Line 263: E501 line too long (82 > 79 characters)
- Line 298: E501 line too long (84 > 79 characters)
- Line 299: E501 line too long (84 > 79 characters)
- Line 325: E501 line too long (83 > 79 characters)
- Line 345: W503 line break before binary operator
- Line 352: E501 line too long (80 > 79 characters)
- Line 365: E501 line too long (88 > 79 characters)
- Line 397: E501 line too long (87 > 79 characters)
- Line 524: E501 line too long (84 > 79 characters)
- Line 593: E501 line too long (83 > 79 characters)
- Line 656: E501 line too long (82 > 79 characters)
- Line 754: E501 line too long (81 > 79 characters)
- Line 833: E501 line too long (83 > 79 characters)
- Line 835: E501 line too long (84 > 79 characters)
- Line 940: E501 line too long (82 > 79 characters)
- Line 1064: E501 line too long (87 > 79 characters)

### tests/test_route_optimizer.py
- Line 20: E501 line too long (81 > 79 characters)

### tests/test_compute_health_stats_empty.py
- Line 12: E501 line too long (80 > 79 characters)
- Line 13: E501 line too long (91 > 79 characters)

### tests/test_direction_finding.py
- Line 3: E265 block comment should start with '# '
- Line 69: E501 line too long (81 > 79 characters)
- Line 72: E501 line too long (85 > 79 characters)
- Line 79: E501 line too long (80 > 79 characters)
- Line 162: E501 line too long (85 > 79 characters)
- Line 253: E501 line too long (80 > 79 characters)
- Line 258: E501 line too long (81 > 79 characters)
- Line 273: E501 line too long (82 > 79 characters)
- Line 274: E501 line too long (82 > 79 characters)
- Line 293: E501 line too long (82 > 79 characters)
- Line 294: E501 line too long (82 > 79 characters)
- Line 295: E501 line too long (82 > 79 characters)
- Line 324: E501 line too long (83 > 79 characters)

### tests/test_migrations_fixed.py
- Line 16: W293 blank line contains whitespace
- Line 22: W293 blank line contains whitespace
- Line 25: W293 blank line contains whitespace
- Line 28: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 36: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 64: W293 blank line contains whitespace
- Line 67: E501 line too long (93 > 79 characters)
- Line 71: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 77: E501 line too long (93 > 79 characters)
- Line 81: W293 blank line contains whitespace
- Line 87: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 114: E501 line too long (92 > 79 characters)
- Line 119: W293 blank line contains whitespace
- Line 134: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 141: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 166: E501 line too long (80 > 79 characters)
- Line 167: E501 line too long (80 > 79 characters)
- Line 169: W293 blank line contains whitespace
- Line 175: W293 blank line contains whitespace
- Line 184: W293 blank line contains whitespace
- Line 202: W293 blank line contains whitespace
- Line 205: E501 line too long (99 > 79 characters)
- Line 210: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 228: E501 line too long (97 > 79 characters)
- Line 229: E501 line too long (87 > 79 characters)
- Line 231: W293 blank line contains whitespace
- Line 234: E501 line too long (95 > 79 characters)
- Line 237: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 265: W293 blank line contains whitespace
- Line 268: E501 line too long (89 > 79 characters)
- Line 273: W293 blank line contains whitespace
- Line 288: W293 blank line contains whitespace
- Line 291: E501 line too long (81 > 79 characters)
- Line 294: W293 blank line contains whitespace
- Line 300: W293 blank line contains whitespace
- Line 309: W293 blank line contains whitespace
- Line 323: W293 blank line contains whitespace
- Line 331: W293 blank line contains whitespace
- Line 333: E501 line too long (87 > 79 characters)
- Line 334: E501 line too long (99 > 79 characters)
- Line 335: E501 line too long (101 > 79 characters)
- Line 336: E501 line too long (102 > 79 characters)
- Line 337: W293 blank line contains whitespace
- Line 340: E501 line too long (89 > 79 characters)
- Line 343: W293 blank line contains whitespace
- Line 351: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 371: E501 line too long (88 > 79 characters)
- Line 374: W293 blank line contains whitespace
- Line 376: E501 line too long (87 > 79 characters)
- Line 377: W293 blank line contains whitespace
- Line 380: E501 line too long (81 > 79 characters)
- Line 389: W293 blank line contains whitespace
- Line 396: W293 blank line contains whitespace
- Line 399: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 408: W293 blank line contains whitespace
- Line 412: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 429: W293 blank line contains whitespace
- Line 436: W293 blank line contains whitespace
- Line 438: W293 blank line contains whitespace
- Line 450: W293 blank line contains whitespace
- Line 452: E501 line too long (85 > 79 characters)
- Line 453: E501 line too long (85 > 79 characters)
- Line 454: E501 line too long (85 > 79 characters)
- Line 455: W293 blank line contains whitespace
- Line 457: E501 line too long (82 > 79 characters)
- Line 458: W293 blank line contains whitespace
- Line 460: E501 line too long (86 > 79 characters)
- Line 463: W293 blank line contains whitespace
- Line 469: W293 blank line contains whitespace
- Line 476: W293 blank line contains whitespace
- Line 486: W293 blank line contains whitespace
- Line 496: E501 line too long (89 > 79 characters)
- Line 497: W293 blank line contains whitespace
- Line 506: E501 line too long (89 > 79 characters)
- Line 507: W293 blank line contains whitespace
- Line 509: E501 line too long (90 > 79 characters)
- Line 512: W293 blank line contains whitespace
- Line 519: W293 blank line contains whitespace
- Line 523: W293 blank line contains whitespace
- Line 527: W293 blank line contains whitespace
- Line 535: W293 blank line contains whitespace
- Line 537: E501 line too long (82 > 79 characters)
- Line 538: W293 blank line contains whitespace
- Line 540: E501 line too long (89 > 79 characters)
- Line 16: Trailing whitespace
- Line 22: Trailing whitespace
- Line 25: Trailing whitespace
- Line 28: Trailing whitespace
- Line 31: Trailing whitespace
- Line 36: Trailing whitespace
- Line 38: Trailing whitespace
- Line 43: Trailing whitespace
- Line 52: Trailing whitespace
- Line 55: Trailing whitespace
- Line 58: Trailing whitespace
- Line 64: Trailing whitespace
- Line 71: Trailing whitespace
- Line 74: Trailing whitespace
- Line 81: Trailing whitespace
- Line 87: Trailing whitespace
- Line 111: Trailing whitespace
- Line 119: Trailing whitespace
- Line 134: Trailing whitespace
- Line 138: Trailing whitespace
- Line 141: Trailing whitespace
- Line 148: Trailing whitespace
- Line 163: Trailing whitespace
- Line 169: Trailing whitespace
- Line 175: Trailing whitespace
- Line 184: Trailing whitespace
- Line 202: Trailing whitespace
- Line 210: Trailing whitespace
- Line 225: Trailing whitespace
- Line 231: Trailing whitespace
- Line 237: Trailing whitespace
- Line 246: Trailing whitespace
- Line 265: Trailing whitespace
- Line 273: Trailing whitespace
- Line 288: Trailing whitespace
- Line 294: Trailing whitespace
- Line 300: Trailing whitespace
- Line 309: Trailing whitespace
- Line 323: Trailing whitespace
- Line 331: Trailing whitespace
- Line 337: Trailing whitespace
- Line 343: Trailing whitespace
- Line 351: Trailing whitespace
- Line 364: Trailing whitespace
- Line 374: Trailing whitespace
- Line 377: Trailing whitespace
- Line 389: Trailing whitespace
- Line 396: Trailing whitespace
- Line 399: Trailing whitespace
- Line 403: Trailing whitespace
- Line 408: Trailing whitespace
- Line 412: Trailing whitespace
- Line 424: Trailing whitespace
- Line 429: Trailing whitespace
- Line 436: Trailing whitespace
- Line 438: Trailing whitespace
- Line 450: Trailing whitespace
- Line 455: Trailing whitespace
- Line 458: Trailing whitespace
- Line 463: Trailing whitespace
- Line 469: Trailing whitespace
- Line 476: Trailing whitespace
- Line 486: Trailing whitespace
- Line 497: Trailing whitespace
- Line 507: Trailing whitespace
- Line 512: Trailing whitespace
- Line 519: Trailing whitespace
- Line 523: Trailing whitespace
- Line 527: Trailing whitespace
- Line 535: Trailing whitespace
- Line 538: Trailing whitespace

### test_imports.py
- Line 9: E302 expected 2 blank lines, found 1
- Line 14: E305 expected 2 blank lines after class or function definition, found 1
- Line 19: W293 blank line contains whitespace
- Line 23: W293 blank line contains whitespace
- Line 27: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 33: W293 blank line contains whitespace
- Line 19: Trailing whitespace
- Line 23: Trailing whitespace
- Line 27: Trailing whitespace
- Line 31: Trailing whitespace
- Line 33: Trailing whitespace

### src/piwardrive/logging/filters.py
- Line 36: E501 line too long (84 > 79 characters)
- Line 57: W503 line break before binary operator

### scripts/export_log_bundle.py
- Line 17: E501 line too long (84 > 79 characters)

### tests/test_status_service.py
- Line 29: E501 line too long (86 > 79 characters)

### quality_summary.py
- Line 39: E501 line too long (91 > 79 characters)
- Line 43: E501 line too long (93 > 79 characters)
- Line 63: E501 line too long (82 > 79 characters)
- Line 93: E501 line too long (82 > 79 characters)

### src/piwardrive/services/network_analytics.py
- Line 25: W503 line break before binary operator
- Line 33: E501 line too long (86 > 79 characters)
- Line 75: E501 line too long (88 > 79 characters)
- Line 77: E501 line too long (84 > 79 characters)
- Line 79: E501 line too long (81 > 79 characters)
- Line 96: E501 line too long (82 > 79 characters)
- Line 109: W293 blank line contains whitespace
- Line 116: E501 line too long (86 > 79 characters)
- Line 109: Trailing whitespace

### tests/test_exceptions_comprehensive.py
- Line 16: E402 module level import not at top of file
- Line 31: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 54: W293 blank line contains whitespace
- Line 68: E501 line too long (81 > 79 characters)
- Line 69: W293 blank line contains whitespace
- Line 80: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 102: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 136: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 182: W293 blank line contains whitespace
- Line 193: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 231: W293 blank line contains whitespace
- Line 245: W293 blank line contains whitespace
- Line 259: W293 blank line contains whitespace
- Line 266: W293 blank line contains whitespace
- Line 269: W291 trailing whitespace
- Line 273: W293 blank line contains whitespace
- Line 276: W293 blank line contains whitespace
- Line 289: E501 line too long (88 > 79 characters)
- Line 298: E501 line too long (108 > 79 characters)
- Line 307: E501 line too long (108 > 79 characters)
- Line 318: E501 line too long (118 > 79 characters)
- Line 31: Trailing whitespace
- Line 41: Trailing whitespace
- Line 54: Trailing whitespace
- Line 69: Trailing whitespace
- Line 80: Trailing whitespace
- Line 93: Trailing whitespace
- Line 102: Trailing whitespace
- Line 122: Trailing whitespace
- Line 136: Trailing whitespace
- Line 147: Trailing whitespace
- Line 154: Trailing whitespace
- Line 168: Trailing whitespace
- Line 182: Trailing whitespace
- Line 193: Trailing whitespace
- Line 200: Trailing whitespace
- Line 214: Trailing whitespace
- Line 231: Trailing whitespace
- Line 245: Trailing whitespace
- Line 259: Trailing whitespace
- Line 266: Trailing whitespace
- Line 269: Trailing whitespace
- Line 273: Trailing whitespace
- Line 276: Trailing whitespace

### tests/test_imports_src.py
- Line 10: E501 line too long (85 > 79 characters)
- Line 17: E501 line too long (86 > 79 characters)

### tests/test_sigint_scanners_basic.py
- Line 8: E501 line too long (80 > 79 characters)
- Line 52: E501 line too long (84 > 79 characters)
- Line 80: E501 line too long (88 > 79 characters)

### fix_issues.py
- Line 17: E501 line too long (89 > 79 characters)
- Line 20: E128 continuation line under-indented for visual indent
- Line 21: E128 continuation line under-indented for visual indent
- Line 22: E128 continuation line under-indented for visual indent
- Line 23: E128 continuation line under-indented for visual indent
- Line 68: E501 line too long (86 > 79 characters)
- Line 70: E501 line too long (81 > 79 characters)
- Line 115: W293 blank line contains whitespace
- Line 118: W504 line break after binary operator
- Line 118: W291 trailing whitespace
- Line 119: W504 line break after binary operator
- Line 119: W291 trailing whitespace
- Line 120: E129 visually indented line with same indent as next logical line
- Line 127: E226 missing whitespace around arithmetic operator
- Line 127: E226 missing whitespace around arithmetic operator
- Line 130: E226 missing whitespace around arithmetic operator
- Line 130: E226 missing whitespace around arithmetic operator
- Line 134: W293 blank line contains whitespace
- Line 136: W504 line break after binary operator
- Line 136: W291 trailing whitespace
- Line 137: W504 line break after binary operator
- Line 137: W291 trailing whitespace
- Line 138: E226 missing whitespace around arithmetic operator
- Line 138: W504 line break after binary operator
- Line 139: E129 visually indented line with same indent as next logical line
- Line 141: E226 missing whitespace around arithmetic operator
- Line 145: E226 missing whitespace around arithmetic operator
- Line 146: E226 missing whitespace around arithmetic operator
- Line 148: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 165: W504 line break after binary operator
- Line 165: W291 trailing whitespace
- Line 166: E129 visually indented line with same indent as next logical line
- Line 172: E501 line too long (85 > 79 characters)
- Line 175: W293 blank line contains whitespace
- Line 190: W293 blank line contains whitespace
- Line 193: W293 blank line contains whitespace
- Line 201: W293 blank line contains whitespace
- Line 204: W504 line break after binary operator
- Line 204: W291 trailing whitespace
- Line 205: W504 line break after binary operator
- Line 205: W291 trailing whitespace
- Line 206: E129 visually indented line with same indent as next logical line
- Line 214: W293 blank line contains whitespace
- Line 222: W293 blank line contains whitespace
- Line 225: W504 line break after binary operator
- Line 225: W291 trailing whitespace
- Line 226: W504 line break after binary operator
- Line 226: W291 trailing whitespace
- Line 227: E226 missing whitespace around arithmetic operator
- Line 227: W504 line break after binary operator
- Line 228: W504 line break after binary operator
- Line 229: E129 visually indented line with same indent as next logical line
- Line 234: W293 blank line contains whitespace
- Line 291: E305 expected 2 blank lines after class or function definition, found 1
- Line 115: Trailing whitespace
- Line 118: Trailing whitespace
- Line 119: Trailing whitespace
- Line 134: Trailing whitespace
- Line 136: Trailing whitespace
- Line 137: Trailing whitespace
- Line 148: Trailing whitespace
- Line 151: Trailing whitespace
- Line 159: Trailing whitespace
- Line 163: Trailing whitespace
- Line 165: Trailing whitespace
- Line 175: Trailing whitespace
- Line 190: Trailing whitespace
- Line 193: Trailing whitespace
- Line 201: Trailing whitespace
- Line 204: Trailing whitespace
- Line 205: Trailing whitespace
- Line 214: Trailing whitespace
- Line 222: Trailing whitespace
- Line 225: Trailing whitespace
- Line 226: Trailing whitespace
- Line 234: Trailing whitespace

### tests/performance/test_performance_infrastructure.py
- Line 40: E302 expected 2 blank lines, found 1
- Line 61: E501 line too long (81 > 79 characters)
- Line 95: E501 line too long (81 > 79 characters)
- Line 102: E501 line too long (82 > 79 characters)
- Line 138: E128 continuation line under-indented for visual indent
- Line 139: W293 blank line contains whitespace
- Line 141: E128 continuation line under-indented for visual indent
- Line 142: W293 blank line contains whitespace
- Line 143: E501 line too long (88 > 79 characters)
- Line 154: E128 continuation line under-indented for visual indent
- Line 154: E125 continuation line with same indent as next logical line
- Line 196: E501 line too long (82 > 79 characters)
- Line 228: E501 line too long (85 > 79 characters)
- Line 233: E128 continuation line under-indented for visual indent
- Line 234: W293 blank line contains whitespace
- Line 236: E128 continuation line under-indented for visual indent
- Line 237: W293 blank line contains whitespace
- Line 238: E501 line too long (88 > 79 characters)
- Line 257: E501 line too long (82 > 79 characters)
- Line 282: E501 line too long (83 > 79 characters)
- Line 297: E128 continuation line under-indented for visual indent
- Line 298: W293 blank line contains whitespace
- Line 300: E128 continuation line under-indented for visual indent
- Line 301: W293 blank line contains whitespace
- Line 347: E501 line too long (81 > 79 characters)
- Line 349: E128 continuation line under-indented for visual indent
- Line 349: E501 line too long (103 > 79 characters)
- Line 350: W293 blank line contains whitespace
- Line 352: E128 continuation line under-indented for visual indent
- Line 352: E501 line too long (104 > 79 characters)
- Line 353: W293 blank line contains whitespace
- Line 382: E501 line too long (84 > 79 characters)
- Line 383: E501 line too long (82 > 79 characters)
- Line 384: E501 line too long (92 > 79 characters)
- Line 385: W293 blank line contains whitespace
- Line 392: E128 continuation line under-indented for visual indent
- Line 393: E128 continuation line under-indented for visual indent
- Line 393: E125 continuation line with same indent as next logical line
- Line 406: E501 line too long (80 > 79 characters)
- Line 412: E501 line too long (97 > 79 characters)
- Line 417: E501 line too long (90 > 79 characters)
- Line 422: E302 expected 2 blank lines, found 1
- Line 436: E501 line too long (84 > 79 characters)
- Line 469: E501 line too long (87 > 79 characters)
- Line 535: E501 line too long (97 > 79 characters)
- Line 537: E305 expected 2 blank lines after class or function definition, found 1
- Line 139: Trailing whitespace
- Line 142: Trailing whitespace
- Line 234: Trailing whitespace
- Line 237: Trailing whitespace
- Line 298: Trailing whitespace
- Line 301: Trailing whitespace
- Line 350: Trailing whitespace
- Line 353: Trailing whitespace
- Line 385: Trailing whitespace

### src/piwardrive/exception_handler.py
- Line 27: E501 line too long (87 > 79 characters)
- Line 40: E501 line too long (80 > 79 characters)
- Line 66: E501 line too long (85 > 79 characters)

### tests/test_security_system.py
- Line 14: E402 module level import not at top of file
- Line 19: E402 module level import not at top of file
- Line 29: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 46: W293 blank line contains whitespace
- Line 68: W293 blank line contains whitespace
- Line 78: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 108: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 155: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 175: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 189: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 271: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 293: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 308: W293 blank line contains whitespace
- Line 317: W293 blank line contains whitespace
- Line 319: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 338: W293 blank line contains whitespace
- Line 349: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 367: W293 blank line contains whitespace
- Line 370: W293 blank line contains whitespace
- Line 374: W293 blank line contains whitespace
- Line 383: W293 blank line contains whitespace
- Line 390: W293 blank line contains whitespace
- Line 393: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 408: W293 blank line contains whitespace
- Line 420: W293 blank line contains whitespace
- Line 422: W293 blank line contains whitespace
- Line 436: W293 blank line contains whitespace
- Line 438: W293 blank line contains whitespace
- Line 447: W293 blank line contains whitespace
- Line 449: W293 blank line contains whitespace
- Line 463: W293 blank line contains whitespace
- Line 466: W293 blank line contains whitespace
- Line 476: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 488: W293 blank line contains whitespace
- Line 497: W293 blank line contains whitespace
- Line 499: W293 blank line contains whitespace
- Line 515: W293 blank line contains whitespace
- Line 526: W293 blank line contains whitespace
- Line 534: W293 blank line contains whitespace
- Line 536: W293 blank line contains whitespace
- Line 546: W293 blank line contains whitespace
- Line 549: W293 blank line contains whitespace
- Line 552: W293 blank line contains whitespace
- Line 29: Trailing whitespace
- Line 38: Trailing whitespace
- Line 46: Trailing whitespace
- Line 68: Trailing whitespace
- Line 78: Trailing whitespace
- Line 81: Trailing whitespace
- Line 93: Trailing whitespace
- Line 101: Trailing whitespace
- Line 108: Trailing whitespace
- Line 114: Trailing whitespace
- Line 117: Trailing whitespace
- Line 120: Trailing whitespace
- Line 123: Trailing whitespace
- Line 131: Trailing whitespace
- Line 138: Trailing whitespace
- Line 155: Trailing whitespace
- Line 167: Trailing whitespace
- Line 175: Trailing whitespace
- Line 181: Trailing whitespace
- Line 189: Trailing whitespace
- Line 200: Trailing whitespace
- Line 221: Trailing whitespace
- Line 234: Trailing whitespace
- Line 246: Trailing whitespace
- Line 258: Trailing whitespace
- Line 271: Trailing whitespace
- Line 280: Trailing whitespace
- Line 293: Trailing whitespace
- Line 297: Trailing whitespace
- Line 305: Trailing whitespace
- Line 308: Trailing whitespace
- Line 317: Trailing whitespace
- Line 319: Trailing whitespace
- Line 326: Trailing whitespace
- Line 329: Trailing whitespace
- Line 335: Trailing whitespace
- Line 338: Trailing whitespace
- Line 349: Trailing whitespace
- Line 357: Trailing whitespace
- Line 367: Trailing whitespace
- Line 370: Trailing whitespace
- Line 374: Trailing whitespace
- Line 383: Trailing whitespace
- Line 390: Trailing whitespace
- Line 393: Trailing whitespace
- Line 406: Trailing whitespace
- Line 408: Trailing whitespace
- Line 420: Trailing whitespace
- Line 422: Trailing whitespace
- Line 436: Trailing whitespace
- Line 438: Trailing whitespace
- Line 447: Trailing whitespace
- Line 449: Trailing whitespace
- Line 463: Trailing whitespace
- Line 466: Trailing whitespace
- Line 476: Trailing whitespace
- Line 479: Trailing whitespace
- Line 488: Trailing whitespace
- Line 497: Trailing whitespace
- Line 499: Trailing whitespace
- Line 515: Trailing whitespace
- Line 526: Trailing whitespace
- Line 534: Trailing whitespace
- Line 536: Trailing whitespace
- Line 546: Trailing whitespace
- Line 549: Trailing whitespace
- Line 552: Trailing whitespace

### src/piwardrive/integrations/sigint_suite/rf/utils.py
- Line 59: E501 line too long (82 > 79 characters)

### src/piwardrive/reporting/professional.py
- Line 97: E501 line too long (88 > 79 characters)
- Line 143: E501 line too long (82 > 79 characters)
- Line 172: E501 line too long (81 > 79 characters)
- Line 174: E501 line too long (92 > 79 characters)
- Line 206: E501 line too long (80 > 79 characters)
- Line 214: E501 line too long (85 > 79 characters)
- Line 220: E501 line too long (89 > 79 characters)
- Line 258: E501 line too long (89 > 79 characters)
- Line 280: E501 line too long (97 > 79 characters)
- Line 285: E501 line too long (86 > 79 characters)
- Line 645: E501 line too long (84 > 79 characters)
- Line 799: E501 line too long (83 > 79 characters)
- Line 824: E501 line too long (86 > 79 characters)
- Line 836: E501 line too long (82 > 79 characters)
- Line 865: E501 line too long (86 > 79 characters)
- Line 958: E501 line too long (84 > 79 characters)
- Line 959: E501 line too long (87 > 79 characters)
- Line 960: E501 line too long (82 > 79 characters)
- Line 975: E501 line too long (80 > 79 characters)
- Line 981: E501 line too long (81 > 79 characters)
- Line 1000: E501 line too long (96 > 79 characters)
- Line 1026: E501 line too long (83 > 79 characters)
- Line 1032: E501 line too long (82 > 79 characters)
- Line 1064: W503 line break before binary operator
- Line 1065: W503 line break before binary operator
- Line 1128: E501 line too long (86 > 79 characters)
- Line 1131: E501 line too long (88 > 79 characters)
- Line 1133: E501 line too long (86 > 79 characters)
- Line 1152: E501 line too long (81 > 79 characters)
- Line 1159: E501 line too long (90 > 79 characters)
- Line 1194: E501 line too long (86 > 79 characters)
- Line 1197: E501 line too long (82 > 79 characters)
- Line 1235: E501 line too long (93 > 79 characters)
- Line 1237: E501 line too long (81 > 79 characters)
- Line 1241: E501 line too long (80 > 79 characters)
- Line 1257: E501 line too long (80 > 79 characters)
- Line 1314: E501 line too long (86 > 79 characters)
- Line 1319: E501 line too long (85 > 79 characters)
- Line 1324: E501 line too long (82 > 79 characters)
- Line 1330: E501 line too long (87 > 79 characters)
- Line 1332: E501 line too long (82 > 79 characters)

### src/piwardrive/cli/config_cli.py
- Line 48: E501 line too long (83 > 79 characters)

### tests/test_service_api_fixed_v2.py
- Line 19: W293 blank line contains whitespace
- Line 23: W293 blank line contains whitespace
- Line 30: W293 blank line contains whitespace
- Line 34: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 50: E501 line too long (88 > 79 characters)
- Line 51: W293 blank line contains whitespace
- Line 56: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 69: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 80: E501 line too long (85 > 79 characters)
- Line 81: W293 blank line contains whitespace
- Line 85: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 94: E501 line too long (81 > 79 characters)
- Line 98: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 113: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 139: W293 blank line contains whitespace
- Line 143: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 154: E501 line too long (85 > 79 characters)
- Line 160: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 170: W293 blank line contains whitespace
- Line 173: E501 line too long (88 > 79 characters)
- Line 175: W293 blank line contains whitespace
- Line 176: E501 line too long (85 > 79 characters)
- Line 184: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 196: E501 line too long (94 > 79 characters)
- Line 197: W293 blank line contains whitespace
- Line 203: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 216: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 222: W293 blank line contains whitespace
- Line 230: W293 blank line contains whitespace
- Line 236: W293 blank line contains whitespace
- Line 240: W293 blank line contains whitespace
- Line 248: W293 blank line contains whitespace
- Line 252: W293 blank line contains whitespace
- Line 260: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 285: W293 blank line contains whitespace
- Line 288: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 308: W293 blank line contains whitespace
- Line 316: W293 blank line contains whitespace
- Line 320: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 328: W293 blank line contains whitespace
- Line 330: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 340: W293 blank line contains whitespace
- Line 344: W293 blank line contains whitespace
- Line 347: W293 blank line contains whitespace
- Line 351: W293 blank line contains whitespace
- Line 355: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 359: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 368: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 375: W293 blank line contains whitespace
- Line 378: E501 line too long (83 > 79 characters)
- Line 380: W293 blank line contains whitespace
- Line 389: W293 blank line contains whitespace
- Line 402: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 410: E501 line too long (81 > 79 characters)
- Line 412: W293 blank line contains whitespace
- Line 414: E501 line too long (81 > 79 characters)
- Line 420: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 431: W293 blank line contains whitespace
- Line 435: W293 blank line contains whitespace
- Line 439: W293 blank line contains whitespace
- Line 449: W293 blank line contains whitespace
- Line 452: W293 blank line contains whitespace
- Line 458: W293 blank line contains whitespace
- Line 464: W293 blank line contains whitespace
- Line 471: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 483: W293 blank line contains whitespace
- Line 491: W293 blank line contains whitespace
- Line 495: W293 blank line contains whitespace
- Line 498: W293 blank line contains whitespace
- Line 503: W293 blank line contains whitespace
- Line 507: W293 blank line contains whitespace
- Line 509: W293 blank line contains whitespace
- Line 514: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 520: W293 blank line contains whitespace
- Line 525: W293 blank line contains whitespace
- Line 527: E501 line too long (88 > 79 characters)
- Line 530: W293 blank line contains whitespace
- Line 534: W293 blank line contains whitespace
- Line 542: W293 blank line contains whitespace
- Line 547: W293 blank line contains whitespace
- Line 550: W293 blank line contains whitespace
- Line 559: W293 blank line contains whitespace
- Line 563: W293 blank line contains whitespace
- Line 572: W293 blank line contains whitespace
- Line 579: W293 blank line contains whitespace
- Line 587: W293 blank line contains whitespace
- Line 592: W293 blank line contains whitespace
- Line 596: W293 blank line contains whitespace
- Line 600: W293 blank line contains whitespace
- Line 602: W293 blank line contains whitespace
- Line 607: W293 blank line contains whitespace
- Line 612: W293 blank line contains whitespace
- Line 19: Trailing whitespace
- Line 23: Trailing whitespace
- Line 30: Trailing whitespace
- Line 34: Trailing whitespace
- Line 43: Trailing whitespace
- Line 47: Trailing whitespace
- Line 51: Trailing whitespace
- Line 56: Trailing whitespace
- Line 62: Trailing whitespace
- Line 69: Trailing whitespace
- Line 76: Trailing whitespace
- Line 81: Trailing whitespace
- Line 85: Trailing whitespace
- Line 88: Trailing whitespace
- Line 98: Trailing whitespace
- Line 101: Trailing whitespace
- Line 106: Trailing whitespace
- Line 110: Trailing whitespace
- Line 113: Trailing whitespace
- Line 118: Trailing whitespace
- Line 122: Trailing whitespace
- Line 125: Trailing whitespace
- Line 131: Trailing whitespace
- Line 139: Trailing whitespace
- Line 143: Trailing whitespace
- Line 151: Trailing whitespace
- Line 160: Trailing whitespace
- Line 163: Trailing whitespace
- Line 170: Trailing whitespace
- Line 175: Trailing whitespace
- Line 184: Trailing whitespace
- Line 188: Trailing whitespace
- Line 191: Trailing whitespace
- Line 197: Trailing whitespace
- Line 203: Trailing whitespace
- Line 207: Trailing whitespace
- Line 216: Trailing whitespace
- Line 219: Trailing whitespace
- Line 222: Trailing whitespace
- Line 230: Trailing whitespace
- Line 236: Trailing whitespace
- Line 240: Trailing whitespace
- Line 248: Trailing whitespace
- Line 252: Trailing whitespace
- Line 260: Trailing whitespace
- Line 267: Trailing whitespace
- Line 270: Trailing whitespace
- Line 274: Trailing whitespace
- Line 281: Trailing whitespace
- Line 285: Trailing whitespace
- Line 288: Trailing whitespace
- Line 290: Trailing whitespace
- Line 294: Trailing whitespace
- Line 301: Trailing whitespace
- Line 305: Trailing whitespace
- Line 308: Trailing whitespace
- Line 316: Trailing whitespace
- Line 320: Trailing whitespace
- Line 324: Trailing whitespace
- Line 328: Trailing whitespace
- Line 330: Trailing whitespace
- Line 335: Trailing whitespace
- Line 340: Trailing whitespace
- Line 344: Trailing whitespace
- Line 347: Trailing whitespace
- Line 351: Trailing whitespace
- Line 355: Trailing whitespace
- Line 357: Trailing whitespace
- Line 359: Trailing whitespace
- Line 364: Trailing whitespace
- Line 368: Trailing whitespace
- Line 372: Trailing whitespace
- Line 375: Trailing whitespace
- Line 380: Trailing whitespace
- Line 389: Trailing whitespace
- Line 402: Trailing whitespace
- Line 406: Trailing whitespace
- Line 412: Trailing whitespace
- Line 420: Trailing whitespace
- Line 424: Trailing whitespace
- Line 428: Trailing whitespace
- Line 431: Trailing whitespace
- Line 435: Trailing whitespace
- Line 439: Trailing whitespace
- Line 449: Trailing whitespace
- Line 452: Trailing whitespace
- Line 458: Trailing whitespace
- Line 464: Trailing whitespace
- Line 471: Trailing whitespace
- Line 479: Trailing whitespace
- Line 483: Trailing whitespace
- Line 491: Trailing whitespace
- Line 495: Trailing whitespace
- Line 498: Trailing whitespace
- Line 503: Trailing whitespace
- Line 507: Trailing whitespace
- Line 509: Trailing whitespace
- Line 514: Trailing whitespace
- Line 518: Trailing whitespace
- Line 520: Trailing whitespace
- Line 525: Trailing whitespace
- Line 530: Trailing whitespace
- Line 534: Trailing whitespace
- Line 542: Trailing whitespace
- Line 547: Trailing whitespace
- Line 550: Trailing whitespace
- Line 559: Trailing whitespace
- Line 563: Trailing whitespace
- Line 572: Trailing whitespace
- Line 579: Trailing whitespace
- Line 587: Trailing whitespace
- Line 592: Trailing whitespace
- Line 596: Trailing whitespace
- Line 600: Trailing whitespace
- Line 602: Trailing whitespace
- Line 607: Trailing whitespace
- Line 612: Trailing whitespace

### scripts/health_import.py
- Line 10: E501 line too long (82 > 79 characters)

### src/piwardrive/direction_finding/algorithms.py
- Line 27: E501 line too long (85 > 79 characters)
- Line 63: E501 line too long (82 > 79 characters)
- Line 65: E501 line too long (87 > 79 characters)
- Line 87: W503 line break before binary operator
- Line 88: W503 line break before binary operator
- Line 89: W503 line break before binary operator
- Line 90: W503 line break before binary operator
- Line 111: W503 line break before binary operator
- Line 112: W503 line break before binary operator
- Line 138: W503 line break before binary operator
- Line 139: W503 line break before binary operator
- Line 140: W503 line break before binary operator
- Line 141: W503 line break before binary operator
- Line 167: W503 line break before binary operator
- Line 168: W503 line break before binary operator
- Line 169: W503 line break before binary operator
- Line 170: W503 line break before binary operator
- Line 190: E501 line too long (87 > 79 characters)
- Line 195: E501 line too long (88 > 79 characters)
- Line 206: E501 line too long (83 > 79 characters)
- Line 211: E501 line too long (86 > 79 characters)
- Line 245: E501 line too long (83 > 79 characters)
- Line 266: E501 line too long (85 > 79 characters)
- Line 268: E501 line too long (97 > 79 characters)
- Line 274: E501 line too long (82 > 79 characters)
- Line 324: E501 line too long (84 > 79 characters)
- Line 370: E501 line too long (83 > 79 characters)
- Line 371: E501 line too long (85 > 79 characters)
- Line 396: E501 line too long (88 > 79 characters)
- Line 397: E501 line too long (81 > 79 characters)
- Line 406: E501 line too long (83 > 79 characters)
- Line 408: E501 line too long (85 > 79 characters)
- Line 427: E501 line too long (88 > 79 characters)
- Line 436: E501 line too long (88 > 79 characters)
- Line 451: E501 line too long (81 > 79 characters)
- Line 454: E501 line too long (82 > 79 characters)
- Line 458: E501 line too long (81 > 79 characters)
- Line 466: E501 line too long (86 > 79 characters)
- Line 471: W503 line break before binary operator
- Line 472: W503 line break before binary operator
- Line 495: E501 line too long (86 > 79 characters)
- Line 503: E501 line too long (85 > 79 characters)
- Line 570: E501 line too long (82 > 79 characters)
- Line 616: W503 line break before binary operator
- Line 616: E501 line too long (84 > 79 characters)
- Line 624: E501 line too long (91 > 79 characters)
- Line 727: E501 line too long (82 > 79 characters)
- Line 799: W503 line break before binary operator
- Line 834: E501 line too long (80 > 79 characters)
- Line 846: E501 line too long (86 > 79 characters)
- Line 865: E501 line too long (88 > 79 characters)
- Line 878: E501 line too long (85 > 79 characters)
- Line 897: E501 line too long (88 > 79 characters)
- Line 907: E501 line too long (85 > 79 characters)
- Line 923: W503 line break before binary operator
- Line 956: E501 line too long (84 > 79 characters)

### src/piwardrive/performance/async_optimizer.py
- Line 40: W293 blank line contains whitespace
- Line 57: E501 line too long (82 > 79 characters)
- Line 84: E501 line too long (83 > 79 characters)
- Line 109: E501 line too long (80 > 79 characters)
- Line 120: E501 line too long (86 > 79 characters)
- Line 144: E501 line too long (80 > 79 characters)
- Line 175: E501 line too long (81 > 79 characters)
- Line 196: E501 line too long (87 > 79 characters)
- Line 197: E501 line too long (91 > 79 characters)
- Line 209: E501 line too long (81 > 79 characters)
- Line 228: E501 line too long (85 > 79 characters)
- Line 398: W503 line break before binary operator
- Line 398: E501 line too long (84 > 79 characters)
- Line 401: E501 line too long (88 > 79 characters)
- Line 416: E501 line too long (80 > 79 characters)
- Line 430: E501 line too long (99 > 79 characters)
- Line 475: W503 line break before binary operator
- Line 526: E501 line too long (89 > 79 characters)
- Line 558: E501 line too long (89 > 79 characters)
- Line 578: E501 line too long (81 > 79 characters)
- Line 581: E501 line too long (103 > 79 characters)
- Line 40: Trailing whitespace

### scripts/health_export.py
- Line 52: E501 line too long (80 > 79 characters)

### src/piwardrive/services/bluetooth_scanner.py
- Line 14: E501 line too long (86 > 79 characters)
- Line 19: E501 line too long (82 > 79 characters)

### tests/test_export_db_script.py
- Line 26: E501 line too long (85 > 79 characters)

### tests/test_jwt_utils_fixed.py
- Line 24: E402 module level import not at top of file
- Line 29: W293 blank line contains whitespace
- Line 37: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 90: W293 blank line contains whitespace
- Line 95: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 102: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 111: E501 line too long (85 > 79 characters)
- Line 112: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 121: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 139: W293 blank line contains whitespace
- Line 145: W293 blank line contains whitespace
- Line 146: E501 line too long (82 > 79 characters)
- Line 148: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 161: W293 blank line contains whitespace
- Line 163: E501 line too long (97 > 79 characters)
- Line 165: E226 missing whitespace around arithmetic operator
- Line 170: W293 blank line contains whitespace
- Line 175: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 182: W293 blank line contains whitespace
- Line 187: W293 blank line contains whitespace
- Line 190: E501 line too long (86 > 79 characters)
- Line 191: W293 blank line contains whitespace
- Line 196: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 212: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 224: W293 blank line contains whitespace
- Line 225: E501 line too long (88 > 79 characters)
- Line 226: E501 line too long (90 > 79 characters)
- Line 227: W293 blank line contains whitespace
- Line 230: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 241: W293 blank line contains whitespace
- Line 245: W293 blank line contains whitespace
- Line 250: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 263: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 276: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 285: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 310: W293 blank line contains whitespace
- Line 313: W293 blank line contains whitespace
- Line 318: W293 blank line contains whitespace
- Line 327: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 337: E501 line too long (86 > 79 characters)
- Line 338: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 350: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 360: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 368: W293 blank line contains whitespace
- Line 371: W293 blank line contains whitespace
- Line 375: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 383: W293 blank line contains whitespace
- Line 388: W293 blank line contains whitespace
- Line 393: W293 blank line contains whitespace
- Line 402: W293 blank line contains whitespace
- Line 407: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 416: W293 blank line contains whitespace
- Line 419: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 433: W293 blank line contains whitespace
- Line 434: E501 line too long (82 > 79 characters)
- Line 436: W293 blank line contains whitespace
- Line 440: W293 blank line contains whitespace
- Line 444: W293 blank line contains whitespace
- Line 447: W293 blank line contains whitespace
- Line 451: W293 blank line contains whitespace
- Line 455: W293 blank line contains whitespace
- Line 458: W293 blank line contains whitespace
- Line 29: Trailing whitespace
- Line 37: Trailing whitespace
- Line 44: Trailing whitespace
- Line 51: Trailing whitespace
- Line 58: Trailing whitespace
- Line 65: Trailing whitespace
- Line 72: Trailing whitespace
- Line 79: Trailing whitespace
- Line 90: Trailing whitespace
- Line 95: Trailing whitespace
- Line 98: Trailing whitespace
- Line 102: Trailing whitespace
- Line 107: Trailing whitespace
- Line 112: Trailing whitespace
- Line 117: Trailing whitespace
- Line 121: Trailing whitespace
- Line 125: Trailing whitespace
- Line 128: Trailing whitespace
- Line 139: Trailing whitespace
- Line 145: Trailing whitespace
- Line 148: Trailing whitespace
- Line 152: Trailing whitespace
- Line 156: Trailing whitespace
- Line 161: Trailing whitespace
- Line 170: Trailing whitespace
- Line 175: Trailing whitespace
- Line 178: Trailing whitespace
- Line 182: Trailing whitespace
- Line 187: Trailing whitespace
- Line 191: Trailing whitespace
- Line 196: Trailing whitespace
- Line 200: Trailing whitespace
- Line 204: Trailing whitespace
- Line 207: Trailing whitespace
- Line 212: Trailing whitespace
- Line 215: Trailing whitespace
- Line 219: Trailing whitespace
- Line 224: Trailing whitespace
- Line 227: Trailing whitespace
- Line 230: Trailing whitespace
- Line 234: Trailing whitespace
- Line 241: Trailing whitespace
- Line 245: Trailing whitespace
- Line 250: Trailing whitespace
- Line 254: Trailing whitespace
- Line 258: Trailing whitespace
- Line 263: Trailing whitespace
- Line 267: Trailing whitespace
- Line 276: Trailing whitespace
- Line 281: Trailing whitespace
- Line 285: Trailing whitespace
- Line 290: Trailing whitespace
- Line 294: Trailing whitespace
- Line 298: Trailing whitespace
- Line 301: Trailing whitespace
- Line 306: Trailing whitespace
- Line 310: Trailing whitespace
- Line 313: Trailing whitespace
- Line 318: Trailing whitespace
- Line 327: Trailing whitespace
- Line 332: Trailing whitespace
- Line 338: Trailing whitespace
- Line 345: Trailing whitespace
- Line 350: Trailing whitespace
- Line 357: Trailing whitespace
- Line 360: Trailing whitespace
- Line 364: Trailing whitespace
- Line 368: Trailing whitespace
- Line 371: Trailing whitespace
- Line 375: Trailing whitespace
- Line 380: Trailing whitespace
- Line 383: Trailing whitespace
- Line 388: Trailing whitespace
- Line 393: Trailing whitespace
- Line 402: Trailing whitespace
- Line 407: Trailing whitespace
- Line 410: Trailing whitespace
- Line 416: Trailing whitespace
- Line 419: Trailing whitespace
- Line 428: Trailing whitespace
- Line 433: Trailing whitespace
- Line 436: Trailing whitespace
- Line 440: Trailing whitespace
- Line 444: Trailing whitespace
- Line 447: Trailing whitespace
- Line 451: Trailing whitespace
- Line 455: Trailing whitespace
- Line 458: Trailing whitespace

### src/piwardrive/api/demographics/endpoints.py
- Line 19: E501 line too long (87 > 79 characters)
- Line 20: E501 line too long (93 > 79 characters)
- Line 22: E501 line too long (82 > 79 characters)

### src/piwardrive/circuit_breaker.py
- Line 16: E501 line too long (83 > 79 characters)
- Line 18: W293 blank line contains whitespace
- Line 33: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 18: Trailing whitespace
- Line 33: Trailing whitespace
- Line 38: Trailing whitespace
- Line 41: Trailing whitespace

### src/piwardrive/data_sink.py
- Line 18: E501 line too long (82 > 79 characters)
- Line 61: E501 line too long (81 > 79 characters)

### src/piwardrive/sigint_suite/__init__.py
- Line 11: E501 line too long (82 > 79 characters)
- Line 13: E501 line too long (80 > 79 characters)
- Line 25: E501 line too long (81 > 79 characters)
- Line 31: E501 line too long (80 > 79 characters)

### src/piwardrive/map/tile_maintenance.py
- Line 10: E501 line too long (83 > 79 characters)
- Line 42: E501 line too long (85 > 79 characters)
- Line 92: E501 line too long (83 > 79 characters)
- Line 155: E501 line too long (86 > 79 characters)
- Line 199: E501 line too long (81 > 79 characters)
- Line 200: E501 line too long (83 > 79 characters)

### src/piwardrive/services/data_export.py
- Line 20: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 42: W293 blank line contains whitespace
- Line 53: W293 blank line contains whitespace
- Line 20: Trailing whitespace
- Line 31: Trailing whitespace
- Line 42: Trailing whitespace
- Line 53: Trailing whitespace

### tests/test_service_status_script.py
- Line 14: E741 ambiguous variable name 'l'
- Line 14: E501 line too long (80 > 79 characters)
- Line 16: E501 line too long (82 > 79 characters)

### tests/test_critical_paths.py
- Line 2: E501 line too long (81 > 79 characters)
- Line 25: W293 blank line contains whitespace
- Line 27: E501 line too long (86 > 79 characters)
- Line 30: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 45: E501 line too long (86 > 79 characters)
- Line 48: W293 blank line contains whitespace
- Line 61: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 90: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 108: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 129: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 170: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 196: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 217: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 227: W293 blank line contains whitespace
- Line 238: W293 blank line contains whitespace
- Line 240: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 249: W293 blank line contains whitespace
- Line 263: W293 blank line contains whitespace
- Line 266: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 289: W293 blank line contains whitespace
- Line 292: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 309: W293 blank line contains whitespace
- Line 320: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 349: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 425: W293 blank line contains whitespace
- Line 435: W293 blank line contains whitespace
- Line 438: W293 blank line contains whitespace
- Line 456: W293 blank line contains whitespace
- Line 464: W293 blank line contains whitespace
- Line 472: W293 blank line contains whitespace
- Line 476: W293 blank line contains whitespace
- Line 486: W293 blank line contains whitespace
- Line 500: E501 line too long (83 > 79 characters)
- Line 501: W293 blank line contains whitespace
- Line 507: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 533: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 555: W293 blank line contains whitespace
- Line 25: Trailing whitespace
- Line 30: Trailing whitespace
- Line 43: Trailing whitespace
- Line 48: Trailing whitespace
- Line 61: Trailing whitespace
- Line 73: Trailing whitespace
- Line 90: Trailing whitespace
- Line 101: Trailing whitespace
- Line 108: Trailing whitespace
- Line 118: Trailing whitespace
- Line 129: Trailing whitespace
- Line 144: Trailing whitespace
- Line 154: Trailing whitespace
- Line 156: Trailing whitespace
- Line 164: Trailing whitespace
- Line 170: Trailing whitespace
- Line 181: Trailing whitespace
- Line 196: Trailing whitespace
- Line 199: Trailing whitespace
- Line 205: Trailing whitespace
- Line 215: Trailing whitespace
- Line 217: Trailing whitespace
- Line 221: Trailing whitespace
- Line 227: Trailing whitespace
- Line 238: Trailing whitespace
- Line 240: Trailing whitespace
- Line 243: Trailing whitespace
- Line 249: Trailing whitespace
- Line 263: Trailing whitespace
- Line 266: Trailing whitespace
- Line 277: Trailing whitespace
- Line 289: Trailing whitespace
- Line 292: Trailing whitespace
- Line 306: Trailing whitespace
- Line 309: Trailing whitespace
- Line 320: Trailing whitespace
- Line 332: Trailing whitespace
- Line 335: Trailing whitespace
- Line 349: Trailing whitespace
- Line 356: Trailing whitespace
- Line 369: Trailing whitespace
- Line 376: Trailing whitespace
- Line 380: Trailing whitespace
- Line 403: Trailing whitespace
- Line 410: Trailing whitespace
- Line 425: Trailing whitespace
- Line 435: Trailing whitespace
- Line 438: Trailing whitespace
- Line 456: Trailing whitespace
- Line 464: Trailing whitespace
- Line 472: Trailing whitespace
- Line 476: Trailing whitespace
- Line 486: Trailing whitespace
- Line 501: Trailing whitespace
- Line 507: Trailing whitespace
- Line 518: Trailing whitespace
- Line 533: Trailing whitespace
- Line 544: Trailing whitespace
- Line 555: Trailing whitespace

### scripts/validate_config.py
- Line 15: E501 line too long (81 > 79 characters)

### src/piwardrive/migrations/010_performance_indexes.py
- Line 13: E501 line too long (124 > 79 characters)
- Line 16: E501 line too long (113 > 79 characters)
- Line 19: E501 line too long (116 > 79 characters)
- Line 22: E501 line too long (92 > 79 characters)
- Line 25: E501 line too long (83 > 79 characters)
- Line 28: E501 line too long (93 > 79 characters)
- Line 31: E501 line too long (106 > 79 characters)
- Line 34: E501 line too long (100 > 79 characters)
- Line 13: Line too long (124 > 120 characters)

### src/piwardrive/gpsd_client.py
- Line 41: E501 line too long (81 > 79 characters)
- Line 43: W293 blank line contains whitespace
- Line 43: Trailing whitespace

### tests/test_vector_tile_customizer.py
- Line 15: E501 line too long (88 > 79 characters)
- Line 18: E501 line too long (80 > 79 characters)

### tests/test_async_scheduler.py
- Line 37: E501 line too long (80 > 79 characters)
- Line 57: E501 line too long (82 > 79 characters)
- Line 151: E501 line too long (81 > 79 characters)

### tests/test_config.py
- Line 40: E501 line too long (82 > 79 characters)
- Line 41: E501 line too long (88 > 79 characters)
- Line 43: E501 line too long (87 > 79 characters)
- Line 104: E501 line too long (88 > 79 characters)

### tests/test_service_simple.py
- Line 5: E501 line too long (85 > 79 characters)
- Line 28: W293 blank line contains whitespace
- Line 30: W291 trailing whitespace
- Line 31: E128 continuation line under-indented for visual indent
- Line 32: E128 continuation line under-indented for visual indent
- Line 33: E128 continuation line under-indented for visual indent
- Line 34: E128 continuation line under-indented for visual indent
- Line 35: W293 blank line contains whitespace
- Line 37: E501 line too long (91 > 79 characters)
- Line 42: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 47: E501 line too long (99 > 79 characters)
- Line 58: W293 blank line contains whitespace
- Line 60: W293 blank line contains whitespace
- Line 67: E501 line too long (80 > 79 characters)
- Line 68: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 78: W291 trailing whitespace
- Line 82: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 99: W293 blank line contains whitespace
- Line 105: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 127: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 143: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 157: W293 blank line contains whitespace
- Line 163: W291 trailing whitespace
- Line 167: W293 blank line contains whitespace
- Line 175: W293 blank line contains whitespace
- Line 177: E501 line too long (104 > 79 characters)
- Line 179: E501 line too long (91 > 79 characters)
- Line 190: W293 blank line contains whitespace
- Line 28: Trailing whitespace
- Line 30: Trailing whitespace
- Line 35: Trailing whitespace
- Line 42: Trailing whitespace
- Line 45: Trailing whitespace
- Line 58: Trailing whitespace
- Line 60: Trailing whitespace
- Line 68: Trailing whitespace
- Line 73: Trailing whitespace
- Line 78: Trailing whitespace
- Line 82: Trailing whitespace
- Line 86: Trailing whitespace
- Line 93: Trailing whitespace
- Line 99: Trailing whitespace
- Line 105: Trailing whitespace
- Line 111: Trailing whitespace
- Line 127: Trailing whitespace
- Line 133: Trailing whitespace
- Line 140: Trailing whitespace
- Line 143: Trailing whitespace
- Line 151: Trailing whitespace
- Line 157: Trailing whitespace
- Line 163: Trailing whitespace
- Line 167: Trailing whitespace
- Line 175: Trailing whitespace
- Line 190: Trailing whitespace

### tests/test_analysis_hooks.py
- Line 13: E501 line too long (80 > 79 characters)
- Line 14: E501 line too long (91 > 79 characters)
- Line 17: E402 module level import not at top of file
- Line 18: E402 module level import not at top of file

### tests/test_gpsd_client_async.py
- Line 38: E501 line too long (86 > 79 characters)
- Line 39: E501 line too long (86 > 79 characters)
- Line 40: E501 line too long (86 > 79 characters)
- Line 41: E501 line too long (86 > 79 characters)

### src/piwardrive/services/cluster_manager.py
- Line 59: E501 line too long (80 > 79 characters)
- Line 65: E501 line too long (87 > 79 characters)
- Line 104: E501 line too long (86 > 79 characters)
- Line 112: E501 line too long (82 > 79 characters)

### src/piwardrive/migrations/001_create_scan_sessions.py
- Line 35: E501 line too long (110 > 79 characters)
- Line 38: E501 line too long (91 > 79 characters)
- Line 41: E501 line too long (124 > 79 characters)
- Line 45: E501 line too long (80 > 79 characters)
- Line 41: Line too long (124 > 120 characters)

### scripts/prefetch_cli.py
- Line 23: E501 line too long (88 > 79 characters)

### tests/test_iot_analytics.py
- Line 4: E501 line too long (85 > 79 characters)
- Line 26: E501 line too long (82 > 79 characters)

### src/piwardrive/migrations/002_enhance_wifi_detections.py
- Line 9: E501 line too long (81 > 79 characters)
- Line 155: E501 line too long (81 > 79 characters)
- Line 156: E501 line too long (81 > 79 characters)
- Line 159: E501 line too long (80 > 79 characters)
- Line 166: E501 line too long (85 > 79 characters)
- Line 167: E501 line too long (85 > 79 characters)
- Line 170: E501 line too long (84 > 79 characters)
- Line 183: E501 line too long (81 > 79 characters)

### src/piwardrive/db/mysql.py
- Line 68: E501 line too long (88 > 79 characters)

### src/piwardrive/protocols/multi_protocol.py
- Line 50: E302 expected 2 blank lines, found 1
- Line 66: E302 expected 2 blank lines, found 1
- Line 82: E302 expected 2 blank lines, found 1
- Line 99: E302 expected 2 blank lines, found 1
- Line 115: E302 expected 2 blank lines, found 1
- Line 132: E302 expected 2 blank lines, found 1
- Line 165: E501 line too long (85 > 79 characters)
- Line 186: E501 line too long (83 > 79 characters)
- Line 260: E203 whitespace before ':'
- Line 265: E501 line too long (82 > 79 characters)
- Line 267: E501 line too long (82 > 79 characters)
- Line 271: E501 line too long (85 > 79 characters)
- Line 284: E203 whitespace before ':'
- Line 294: E303 too many blank lines (3)
- Line 406: E303 too many blank lines (3)
- Line 506: E303 too many blank lines (3)
- Line 512: E501 line too long (81 > 79 characters)
- Line 521: E501 line too long (83 > 79 characters)
- Line 620: E303 too many blank lines (3)
- Line 711: E501 line too long (83 > 79 characters)
- Line 716: E501 line too long (81 > 79 characters)
- Line 748: E303 too many blank lines (3)
- Line 758: E501 line too long (82 > 79 characters)
- Line 764: E226 missing whitespace around arithmetic operator
- Line 764: E226 missing whitespace around arithmetic operator
- Line 764: E501 line too long (100 > 79 characters)
- Line 854: E501 line too long (80 > 79 characters)
- Line 1003: E501 line too long (80 > 79 characters)
- Line 1020: E226 missing whitespace around arithmetic operator
- Line 1052: E501 line too long (84 > 79 characters)
- Line 1081: E501 line too long (88 > 79 characters)
- Line 1086: E302 expected 2 blank lines, found 1
- Line 1095: E501 line too long (81 > 79 characters)
- Line 1096: E226 missing whitespace around arithmetic operator
- Line 1130: E501 line too long (83 > 79 characters)
- Line 1151: E501 line too long (80 > 79 characters)
- Line 1155: E305 expected 2 blank lines after class or function definition, found 1

### scripts/prefetch_batch.py
- Line 49: E501 line too long (88 > 79 characters)

### scripts/bench_geom.py
- Line 21: E501 line too long (85 > 79 characters)
- Line 26: E501 line too long (85 > 79 characters)
- Line 41: E501 line too long (85 > 79 characters)
- Line 46: E501 line too long (85 > 79 characters)

### src/piwardrive/integrations/sigint_suite/scan_all.py
- Line 13: E501 line too long (88 > 79 characters)

### src/piwardrive/widgets/suspicious_activity.py
- Line 30: E501 line too long (80 > 79 characters)

### src/piwardrive/services/integration_service.py
- Line 29: W293 blank line contains whitespace
- Line 38: E501 line too long (84 > 79 characters)
- Line 40: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 48: W293 blank line contains whitespace
- Line 75: E501 line too long (81 > 79 characters)
- Line 98: E501 line too long (86 > 79 characters)
- Line 117: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 29: Trailing whitespace
- Line 40: Trailing whitespace
- Line 45: Trailing whitespace
- Line 48: Trailing whitespace
- Line 117: Trailing whitespace
- Line 131: Trailing whitespace

### tests/test_unit_enhanced.py
- Line 121: E501 line too long (85 > 79 characters)
- Line 165: E501 line too long (86 > 79 characters)
- Line 228: E501 line too long (80 > 79 characters)
- Line 268: E501 line too long (81 > 79 characters)
- Line 323: E226 missing whitespace around arithmetic operator
- Line 323: E228 missing whitespace around modulo operator
- Line 342: E226 missing whitespace around arithmetic operator
- Line 342: E228 missing whitespace around modulo operator
- Line 399: E501 line too long (81 > 79 characters)
- Line 404: E501 line too long (80 > 79 characters)
- Line 453: E501 line too long (80 > 79 characters)
- Line 455: E501 line too long (82 > 79 characters)
- Line 456: E501 line too long (80 > 79 characters)
- Line 457: E501 line too long (80 > 79 characters)
- Line 464: E501 line too long (85 > 79 characters)
- Line 520: E226 missing whitespace around arithmetic operator
- Line 520: E228 missing whitespace around modulo operator
- Line 644: E501 line too long (82 > 79 characters)
- Line 721: E501 line too long (80 > 79 characters)
- Line 723: E501 line too long (83 > 79 characters)
- Line 1007: E501 line too long (87 > 79 characters)
- Line 1048: E501 line too long (84 > 79 characters)
- Line 1078: E501 line too long (88 > 79 characters)

### src/piwardrive/ui/user_experience.py
- Line 46: E302 expected 2 blank lines, found 1
- Line 64: E302 expected 2 blank lines, found 1
- Line 78: E302 expected 2 blank lines, found 1
- Line 93: E302 expected 2 blank lines, found 1
- Line 109: E303 too many blank lines (3)
- Line 130: E501 line too long (125 > 79 characters)
- Line 137: E501 line too long (85 > 79 characters)
- Line 143: E501 line too long (91 > 79 characters)
- Line 156: E501 line too long (82 > 79 characters)
- Line 162: E501 line too long (85 > 79 characters)
- Line 174: E501 line too long (94 > 79 characters)
- Line 180: E501 line too long (101 > 79 characters)
- Line 310: E501 line too long (86 > 79 characters)
- Line 313: E501 line too long (86 > 79 characters)
- Line 316: E501 line too long (84 > 79 characters)
- Line 318: E501 line too long (81 > 79 characters)
- Line 329: E501 line too long (85 > 79 characters)
- Line 381: E501 line too long (105 > 79 characters)
- Line 389: E501 line too long (99 > 79 characters)
- Line 422: E501 line too long (97 > 79 characters)
- Line 430: E501 line too long (87 > 79 characters)
- Line 437: E501 line too long (89 > 79 characters)
- Line 445: E501 line too long (85 > 79 characters)
- Line 456: E501 line too long (96 > 79 characters)
- Line 464: E501 line too long (103 > 79 characters)
- Line 505: E501 line too long (81 > 79 characters)
- Line 517: E501 line too long (81 > 79 characters)
- Line 539: E501 line too long (88 > 79 characters)
- Line 682: E501 line too long (85 > 79 characters)
- Line 696: E501 line too long (82 > 79 characters)
- Line 1073: E501 line too long (84 > 79 characters)
- Line 1169: E501 line too long (80 > 79 characters)
- Line 1209: E305 expected 2 blank lines after class or function definition, found 1
- Line 1263: E501 line too long (88 > 79 characters)
- Line 1270: E501 line too long (84 > 79 characters)
- Line 1271: E501 line too long (87 > 79 characters)
- Line 1273: E501 line too long (82 > 79 characters)
- Line 1312: E302 expected 2 blank lines, found 1
- Line 1399: E305 expected 2 blank lines after class or function definition, found 1
- Line 130: Line too long (125 > 120 characters)

### src/piwardrive/logconfig.py
- Line 18: E501 line too long (81 > 79 characters)

### scripts/uav_record.py
- Line 54: E501 line too long (86 > 79 characters)

### src/piwardrive/routes/analytics.py
- Line 10: E501 line too long (87 > 79 characters)
- Line 51: E501 line too long (85 > 79 characters)

### src/piwardrive/widgets/signal_strength.py
- Line 10: E501 line too long (85 > 79 characters)
- Line 27: E501 line too long (88 > 79 characters)

### src/piwardrive/analytics/anomaly.py
- Line 17: E501 line too long (82 > 79 characters)
- Line 22: E501 line too long (87 > 79 characters)
- Line 30: E501 line too long (81 > 79 characters)

### tests/test_cli_tools.py
- Line 30: E501 line too long (88 > 79 characters)

### src/piwardrive/utils.py
- Line 37: E501 line too long (81 > 79 characters)
- Line 38: W293 blank line contains whitespace
- Line 46: E501 line too long (84 > 79 characters)
- Line 52: E501 line too long (83 > 79 characters)
- Line 58: E501 line too long (88 > 79 characters)
- Line 71: E501 line too long (92 > 79 characters)
- Line 77: E501 line too long (88 > 79 characters)
- Line 83: E501 line too long (93 > 79 characters)
- Line 110: E501 line too long (82 > 79 characters)
- Line 38: Trailing whitespace

### src/piwardrive/data_processing/enhanced_processing.py
- Line 52: E501 line too long (80 > 79 characters)
- Line 64: E501 line too long (87 > 79 characters)
- Line 68: E501 line too long (80 > 79 characters)
- Line 102: E501 line too long (88 > 79 characters)
- Line 205: E501 line too long (86 > 79 characters)
- Line 263: E501 line too long (80 > 79 characters)
- Line 283: E501 line too long (81 > 79 characters)
- Line 294: E501 line too long (80 > 79 characters)
- Line 344: W503 line break before binary operator
- Line 368: E501 line too long (82 > 79 characters)
- Line 397: E501 line too long (86 > 79 characters)
- Line 406: E501 line too long (85 > 79 characters)
- Line 461: W503 line break before binary operator
- Line 489: E501 line too long (87 > 79 characters)
- Line 493: E501 line too long (84 > 79 characters)
- Line 513: E501 line too long (81 > 79 characters)
- Line 516: E501 line too long (81 > 79 characters)
- Line 519: E501 line too long (85 > 79 characters)
- Line 544: E501 line too long (85 > 79 characters)
- Line 613: E501 line too long (84 > 79 characters)
- Line 640: E501 line too long (82 > 79 characters)
- Line 647: E501 line too long (82 > 79 characters)
- Line 693: E501 line too long (84 > 79 characters)
- Line 695: E501 line too long (87 > 79 characters)
- Line 698: E128 continuation line under-indented for visual indent
- Line 714: E501 line too long (82 > 79 characters)
- Line 771: E501 line too long (80 > 79 characters)

### tests/test_lora_scanner.py
- Line 95: E741 ambiguous variable name 'l'
- Line 95: E501 line too long (80 > 79 characters)

### src/piwardrive/routes/bluetooth.py
- Line 47: E501 line too long (81 > 79 characters)

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 4: E501 line too long (81 > 79 characters)
- Line 125: E501 line too long (84 > 79 characters)
- Line 172: W293 blank line contains whitespace
- Line 275: E501 line too long (87 > 79 characters)
- Line 285: E501 line too long (86 > 79 characters)
- Line 387: E501 line too long (85 > 79 characters)
- Line 460: E501 line too long (83 > 79 characters)
- Line 469: E501 line too long (84 > 79 characters)
- Line 502: E501 line too long (83 > 79 characters)
- Line 513: E501 line too long (85 > 79 characters)
- Line 518: E501 line too long (84 > 79 characters)
- Line 520: E501 line too long (83 > 79 characters)
- Line 581: E501 line too long (87 > 79 characters)
- Line 603: E501 line too long (86 > 79 characters)
- Line 609: E501 line too long (80 > 79 characters)
- Line 619: E226 missing whitespace around arithmetic operator
- Line 619: E501 line too long (92 > 79 characters)
- Line 711: E501 line too long (81 > 79 characters)
- Line 781: E501 line too long (84 > 79 characters)
- Line 782: E501 line too long (87 > 79 characters)
- Line 860: E501 line too long (85 > 79 characters)
- Line 864: E501 line too long (85 > 79 characters)
- Line 897: E501 line too long (85 > 79 characters)
- Line 909: E501 line too long (83 > 79 characters)
- Line 926: E501 line too long (86 > 79 characters)
- Line 970: E501 line too long (86 > 79 characters)
- Line 973: E501 line too long (86 > 79 characters)
- Line 983: E501 line too long (80 > 79 characters)
- Line 996: E501 line too long (86 > 79 characters)
- Line 1057: E501 line too long (80 > 79 characters)
- Line 1066: E501 line too long (81 > 79 characters)
- Line 1095: E501 line too long (83 > 79 characters)
- Line 1098: E501 line too long (88 > 79 characters)
- Line 1114: E501 line too long (80 > 79 characters)
- Line 1236: E501 line too long (85 > 79 characters)
- Line 1239: E501 line too long (85 > 79 characters)
- Line 1314: E501 line too long (88 > 79 characters)
- Line 1453: E501 line too long (82 > 79 characters)
- Line 172: Trailing whitespace

### tests/test_vendor_lookup.py
- Line 13: E501 line too long (80 > 79 characters)

### src/piwardrive/integration/system_orchestration.py
- Line 4: E501 line too long (88 > 79 characters)
- Line 48: E501 line too long (84 > 79 characters)
- Line 142: E501 line too long (82 > 79 characters)
- Line 146: E501 line too long (88 > 79 characters)
- Line 258: E501 line too long (88 > 79 characters)
- Line 293: E501 line too long (83 > 79 characters)
- Line 298: E501 line too long (80 > 79 characters)
- Line 301: E501 line too long (80 > 79 characters)
- Line 309: E501 line too long (86 > 79 characters)
- Line 358: E501 line too long (85 > 79 characters)
- Line 400: E501 line too long (87 > 79 characters)
- Line 457: E501 line too long (83 > 79 characters)
- Line 462: E501 line too long (83 > 79 characters)
- Line 566: E501 line too long (80 > 79 characters)
- Line 579: E501 line too long (85 > 79 characters)
- Line 637: W293 blank line contains whitespace
- Line 640: W293 blank line contains whitespace
- Line 840: E501 line too long (86 > 79 characters)
- Line 858: E501 line too long (81 > 79 characters)
- Line 918: E501 line too long (86 > 79 characters)
- Line 637: Trailing whitespace
- Line 640: Trailing whitespace

### src/piwardrive/logging/storage.py
- Line 124: E501 line too long (86 > 79 characters)
- Line 184: E501 line too long (81 > 79 characters)
- Line 194: E501 line too long (84 > 79 characters)
- Line 207: E501 line too long (85 > 79 characters)

### src/piwardrive/database_service.py
- Line 27: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 48: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 78: W293 blank line contains whitespace
- Line 88: E501 line too long (86 > 79 characters)
- Line 90: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 99: E501 line too long (81 > 79 characters)
- Line 101: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 139: E501 line too long (86 > 79 characters)
- Line 141: W293 blank line contains whitespace
- Line 147: E501 line too long (81 > 79 characters)
- Line 149: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 158: E501 line too long (84 > 79 characters)
- Line 160: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 179: W293 blank line contains whitespace
- Line 187: W293 blank line contains whitespace
- Line 190: W293 blank line contains whitespace
- Line 198: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 27: Trailing whitespace
- Line 45: Trailing whitespace
- Line 48: Trailing whitespace
- Line 58: Trailing whitespace
- Line 62: Trailing whitespace
- Line 70: Trailing whitespace
- Line 78: Trailing whitespace
- Line 90: Trailing whitespace
- Line 93: Trailing whitespace
- Line 101: Trailing whitespace
- Line 109: Trailing whitespace
- Line 117: Trailing whitespace
- Line 125: Trailing whitespace
- Line 133: Trailing whitespace
- Line 141: Trailing whitespace
- Line 149: Trailing whitespace
- Line 152: Trailing whitespace
- Line 160: Trailing whitespace
- Line 163: Trailing whitespace
- Line 171: Trailing whitespace
- Line 179: Trailing whitespace
- Line 187: Trailing whitespace
- Line 190: Trailing whitespace
- Line 198: Trailing whitespace
- Line 206: Trailing whitespace
- Line 215: Trailing whitespace
- Line 218: Trailing whitespace

### src/piwardrive/ml/threat_detection.py
- Line 50: E501 line too long (80 > 79 characters)
- Line 114: E501 line too long (84 > 79 characters)
- Line 182: E501 line too long (86 > 79 characters)
- Line 185: E501 line too long (84 > 79 characters)
- Line 187: E501 line too long (86 > 79 characters)
- Line 190: E501 line too long (87 > 79 characters)
- Line 192: E501 line too long (88 > 79 characters)
- Line 196: E501 line too long (85 > 79 characters)
- Line 197: E501 line too long (87 > 79 characters)
- Line 236: E501 line too long (82 > 79 characters)
- Line 260: E501 line too long (83 > 79 characters)
- Line 295: E501 line too long (82 > 79 characters)
- Line 305: E501 line too long (86 > 79 characters)
- Line 312: E501 line too long (88 > 79 characters)
- Line 327: E501 line too long (80 > 79 characters)
- Line 334: E501 line too long (83 > 79 characters)
- Line 353: E501 line too long (82 > 79 characters)
- Line 374: E501 line too long (87 > 79 characters)
- Line 423: E501 line too long (81 > 79 characters)
- Line 492: E501 line too long (82 > 79 characters)
- Line 521: E501 line too long (81 > 79 characters)
- Line 534: E501 line too long (80 > 79 characters)
- Line 536: E501 line too long (80 > 79 characters)
- Line 541: E501 line too long (87 > 79 characters)
- Line 591: E501 line too long (85 > 79 characters)
- Line 596: E501 line too long (88 > 79 characters)
- Line 601: E501 line too long (82 > 79 characters)
- Line 606: E501 line too long (86 > 79 characters)
- Line 621: E501 line too long (81 > 79 characters)
- Line 624: E501 line too long (83 > 79 characters)
- Line 634: E501 line too long (86 > 79 characters)
- Line 636: E501 line too long (84 > 79 characters)
- Line 652: E501 line too long (88 > 79 characters)
- Line 689: W503 line break before binary operator
- Line 690: W503 line break before binary operator
- Line 706: E501 line too long (81 > 79 characters)
- Line 714: E501 line too long (85 > 79 characters)
- Line 768: E501 line too long (80 > 79 characters)
- Line 772: E501 line too long (86 > 79 characters)
- Line 776: E501 line too long (84 > 79 characters)
- Line 780: E501 line too long (81 > 79 characters)
- Line 787: E501 line too long (80 > 79 characters)
- Line 859: E501 line too long (80 > 79 characters)
- Line 862: E501 line too long (82 > 79 characters)
- Line 912: E501 line too long (83 > 79 characters)
- Line 916: E501 line too long (87 > 79 characters)
- Line 977: W503 line break before binary operator
- Line 978: W503 line break before binary operator
- Line 986: E501 line too long (82 > 79 characters)
- Line 990: E501 line too long (88 > 79 characters)
- Line 992: E501 line too long (83 > 79 characters)
- Line 1003: E501 line too long (85 > 79 characters)
- Line 1072: E501 line too long (84 > 79 characters)
- Line 1103: E501 line too long (86 > 79 characters)
- Line 1149: E501 line too long (84 > 79 characters)
- Line 1151: E501 line too long (85 > 79 characters)
- Line 1229: E501 line too long (122 > 79 characters)
- Line 1229: Line too long (122 > 120 characters)

### src/piwardrive/analytics/baseline.py
- Line 34: E501 line too long (81 > 79 characters)
- Line 50: E402 module level import not at top of file

### src/piwardrive/aggregation_service.py
- Line 24: E501 line too long (82 > 79 characters)
- Line 114: E501 line too long (85 > 79 characters)
- Line 121: E501 line too long (83 > 79 characters)
- Line 169: E501 line too long (80 > 79 characters)
- Line 183: W293 blank line contains whitespace
- Line 183: Trailing whitespace

### tests/test_health_monitor.py
- Line 95: E501 line too long (85 > 79 characters)
- Line 120: E501 line too long (85 > 79 characters)
- Line 156: E501 line too long (80 > 79 characters)
- Line 158: E501 line too long (82 > 79 characters)
- Line 159: E501 line too long (80 > 79 characters)
- Line 163: E501 line too long (85 > 79 characters)

### comprehensive_fix.py
- Line 60: E501 line too long (81 > 79 characters)
- Line 62: E501 line too long (88 > 79 characters)
- Line 178: E501 line too long (81 > 79 characters)
- Line 210: E501 line too long (81 > 79 characters)
- Line 218: E501 line too long (87 > 79 characters)

### tests/test_diagnostics.py
- Line 15: E402 module level import not at top of file
- Line 17: E402 module level import not at top of file
- Line 19: E402 module level import not at top of file
- Line 40: E501 line too long (83 > 79 characters)
- Line 44: E501 line too long (88 > 79 characters)
- Line 49: E501 line too long (87 > 79 characters)
- Line 58: E501 line too long (81 > 79 characters)
- Line 66: E501 line too long (80 > 79 characters)

### src/piwardrive/notifications.py
- Line 32: W293 blank line contains whitespace
- Line 66: E501 line too long (81 > 79 characters)
- Line 32: Trailing whitespace

### src/piwardrive/analytics/clustering.py
- Line 24: E501 line too long (87 > 79 characters)

### tests/test_cache.py
- Line 19: E402 module level import not at top of file
- Line 58: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 71: E501 line too long (81 > 79 characters)
- Line 81: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 85: E501 line too long (88 > 79 characters)
- Line 87: W293 blank line contains whitespace
- Line 95: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 99: E501 line too long (88 > 79 characters)
- Line 101: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 113: W293 blank line contains whitespace
- Line 114: E501 line too long (88 > 79 characters)
- Line 116: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 127: W293 blank line contains whitespace
- Line 128: E501 line too long (88 > 79 characters)
- Line 129: E501 line too long (90 > 79 characters)
- Line 137: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 152: E501 line too long (92 > 79 characters)
- Line 164: W293 blank line contains whitespace
- Line 165: E501 line too long (81 > 79 characters)
- Line 174: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 177: E501 line too long (88 > 79 characters)
- Line 179: W293 blank line contains whitespace
- Line 181: W291 trailing whitespace
- Line 192: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 195: E501 line too long (88 > 79 characters)
- Line 197: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 211: W293 blank line contains whitespace
- Line 212: E501 line too long (88 > 79 characters)
- Line 214: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 240: W293 blank line contains whitespace
- Line 241: E501 line too long (92 > 79 characters)
- Line 243: W293 blank line contains whitespace
- Line 259: W293 blank line contains whitespace
- Line 260: E501 line too long (81 > 79 characters)
- Line 268: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 271: E501 line too long (88 > 79 characters)
- Line 273: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 283: E501 line too long (88 > 79 characters)
- Line 285: W293 blank line contains whitespace
- Line 292: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 295: E501 line too long (88 > 79 characters)
- Line 297: W293 blank line contains whitespace
- Line 298: E501 line too long (82 > 79 characters)
- Line 309: W293 blank line contains whitespace
- Line 310: E501 line too long (81 > 79 characters)
- Line 318: W293 blank line contains whitespace
- Line 321: W293 blank line contains whitespace
- Line 322: E501 line too long (88 > 79 characters)
- Line 324: W293 blank line contains whitespace
- Line 326: E501 line too long (93 > 79 characters)
- Line 332: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 336: E501 line too long (88 > 79 characters)
- Line 338: W293 blank line contains whitespace
- Line 346: W293 blank line contains whitespace
- Line 349: W293 blank line contains whitespace
- Line 350: E501 line too long (88 > 79 characters)
- Line 352: W293 blank line contains whitespace
- Line 354: E501 line too long (84 > 79 characters)
- Line 369: W293 blank line contains whitespace
- Line 371: W293 blank line contains whitespace
- Line 373: E501 line too long (88 > 79 characters)
- Line 375: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 384: E501 line too long (88 > 79 characters)
- Line 388: W293 blank line contains whitespace
- Line 390: E501 line too long (88 > 79 characters)
- Line 399: W293 blank line contains whitespace
- Line 401: W293 blank line contains whitespace
- Line 402: E501 line too long (88 > 79 characters)
- Line 406: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 413: W293 blank line contains whitespace
- Line 427: W293 blank line contains whitespace
- Line 429: W293 blank line contains whitespace
- Line 431: E501 line too long (88 > 79 characters)
- Line 433: W293 blank line contains whitespace
- Line 440: W293 blank line contains whitespace
- Line 442: E501 line too long (83 > 79 characters)
- Line 443: E501 line too long (88 > 79 characters)
- Line 451: W293 blank line contains whitespace
- Line 457: W293 blank line contains whitespace
- Line 458: E501 line too long (88 > 79 characters)
- Line 459: E501 line too long (84 > 79 characters)
- Line 462: W293 blank line contains whitespace
- Line 465: W293 blank line contains whitespace
- Line 477: W293 blank line contains whitespace
- Line 480: W293 blank line contains whitespace
- Line 481: E501 line too long (88 > 79 characters)
- Line 484: E501 line too long (96 > 79 characters)
- Line 485: W293 blank line contains whitespace
- Line 489: W293 blank line contains whitespace
- Line 498: W293 blank line contains whitespace
- Line 500: W293 blank line contains whitespace
- Line 501: E501 line too long (88 > 79 characters)
- Line 504: E501 line too long (90 > 79 characters)
- Line 510: W293 blank line contains whitespace
- Line 512: W293 blank line contains whitespace
- Line 513: E501 line too long (88 > 79 characters)
- Line 515: E501 line too long (91 > 79 characters)
- Line 521: W293 blank line contains whitespace
- Line 523: W293 blank line contains whitespace
- Line 524: E501 line too long (88 > 79 characters)
- Line 526: E501 line too long (96 > 79 characters)
- Line 58: Trailing whitespace
- Line 70: Trailing whitespace
- Line 81: Trailing whitespace
- Line 84: Trailing whitespace
- Line 87: Trailing whitespace
- Line 95: Trailing whitespace
- Line 98: Trailing whitespace
- Line 101: Trailing whitespace
- Line 110: Trailing whitespace
- Line 113: Trailing whitespace
- Line 116: Trailing whitespace
- Line 124: Trailing whitespace
- Line 127: Trailing whitespace
- Line 137: Trailing whitespace
- Line 147: Trailing whitespace
- Line 151: Trailing whitespace
- Line 164: Trailing whitespace
- Line 174: Trailing whitespace
- Line 176: Trailing whitespace
- Line 179: Trailing whitespace
- Line 181: Trailing whitespace
- Line 192: Trailing whitespace
- Line 194: Trailing whitespace
- Line 197: Trailing whitespace
- Line 209: Trailing whitespace
- Line 211: Trailing whitespace
- Line 214: Trailing whitespace
- Line 225: Trailing whitespace
- Line 237: Trailing whitespace
- Line 240: Trailing whitespace
- Line 243: Trailing whitespace
- Line 259: Trailing whitespace
- Line 268: Trailing whitespace
- Line 270: Trailing whitespace
- Line 273: Trailing whitespace
- Line 280: Trailing whitespace
- Line 282: Trailing whitespace
- Line 285: Trailing whitespace
- Line 292: Trailing whitespace
- Line 294: Trailing whitespace
- Line 297: Trailing whitespace
- Line 309: Trailing whitespace
- Line 318: Trailing whitespace
- Line 321: Trailing whitespace
- Line 324: Trailing whitespace
- Line 332: Trailing whitespace
- Line 335: Trailing whitespace
- Line 338: Trailing whitespace
- Line 346: Trailing whitespace
- Line 349: Trailing whitespace
- Line 352: Trailing whitespace
- Line 369: Trailing whitespace
- Line 371: Trailing whitespace
- Line 375: Trailing whitespace
- Line 381: Trailing whitespace
- Line 388: Trailing whitespace
- Line 399: Trailing whitespace
- Line 401: Trailing whitespace
- Line 406: Trailing whitespace
- Line 410: Trailing whitespace
- Line 413: Trailing whitespace
- Line 427: Trailing whitespace
- Line 429: Trailing whitespace
- Line 433: Trailing whitespace
- Line 440: Trailing whitespace
- Line 451: Trailing whitespace
- Line 457: Trailing whitespace
- Line 462: Trailing whitespace
- Line 465: Trailing whitespace
- Line 477: Trailing whitespace
- Line 480: Trailing whitespace
- Line 485: Trailing whitespace
- Line 489: Trailing whitespace
- Line 498: Trailing whitespace
- Line 500: Trailing whitespace
- Line 510: Trailing whitespace
- Line 512: Trailing whitespace
- Line 521: Trailing whitespace
- Line 523: Trailing whitespace

### src/piwardrive/integrations/sigint_suite/scripts/continuous_scan.py
- Line 13: E501 line too long (81 > 79 characters)
- Line 22: E501 line too long (83 > 79 characters)

### src/piwardrive/db_browser.py
- Line 19: E501 line too long (87 > 79 characters)
- Line 22: E501 line too long (87 > 79 characters)
- Line 39: E501 line too long (84 > 79 characters)

### tests/test_tile_maintenance_cli.py
- Line 10: E501 line too long (82 > 79 characters)
- Line 19: E402 module level import not at top of file
- Line 49: E501 line too long (80 > 79 characters)

### scripts/mobile_diagnostics.py
- Line 66: E722 do not use bare 'except'
- Line 72: E501 line too long (88 > 79 characters)
- Line 74: E722 do not use bare 'except'
- Line 104: E501 line too long (83 > 79 characters)
- Line 121: E501 line too long (87 > 79 characters)
- Line 125: E501 line too long (87 > 79 characters)
- Line 128: E722 do not use bare 'except'
- Line 137: E722 do not use bare 'except'
- Line 142: E501 line too long (87 > 79 characters)
- Line 144: E722 do not use bare 'except'
- Line 162: E501 line too long (80 > 79 characters)
- Line 183: E501 line too long (87 > 79 characters)
- Line 231: E501 line too long (87 > 79 characters)
- Line 246: E501 line too long (85 > 79 characters)
- Line 248: E501 line too long (82 > 79 characters)
- Line 262: E501 line too long (82 > 79 characters)
- Line 300: E722 do not use bare 'except'
- Line 310: E722 do not use bare 'except'
- Line 321: E722 do not use bare 'except'
- Line 333: E722 do not use bare 'except'
- Line 406: E501 line too long (85 > 79 characters)
- Line 408: E501 line too long (85 > 79 characters)
- Line 409: E501 line too long (87 > 79 characters)
- Line 410: E501 line too long (82 > 79 characters)
- Line 415: E501 line too long (85 > 79 characters)
- Line 479: E501 line too long (80 > 79 characters)

### src/piwardrive/services/monitoring.py
- Line 100: E501 line too long (82 > 79 characters)

### tests/test_main_simple.py
- Line 14: W293 blank line contains whitespace
- Line 22: W293 blank line contains whitespace
- Line 26: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 35: W293 blank line contains whitespace
- Line 39: W293 blank line contains whitespace
- Line 46: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 61: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 80: E501 line too long (90 > 79 characters)
- Line 86: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 97: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 105: E501 line too long (121 > 79 characters)
- Line 106: E501 line too long (109 > 79 characters)
- Line 107: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 119: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 145: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 196: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 203: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 216: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 252: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 280: E501 line too long (82 > 79 characters)
- Line 283: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 14: Trailing whitespace
- Line 22: Trailing whitespace
- Line 26: Trailing whitespace
- Line 31: Trailing whitespace
- Line 35: Trailing whitespace
- Line 39: Trailing whitespace
- Line 46: Trailing whitespace
- Line 55: Trailing whitespace
- Line 61: Trailing whitespace
- Line 65: Trailing whitespace
- Line 70: Trailing whitespace
- Line 74: Trailing whitespace
- Line 77: Trailing whitespace
- Line 86: Trailing whitespace
- Line 91: Trailing whitespace
- Line 94: Trailing whitespace
- Line 97: Trailing whitespace
- Line 100: Trailing whitespace
- Line 105: Line too long (121 > 120 characters)
- Line 107: Trailing whitespace
- Line 111: Trailing whitespace
- Line 119: Trailing whitespace
- Line 124: Trailing whitespace
- Line 128: Trailing whitespace
- Line 133: Trailing whitespace
- Line 140: Trailing whitespace
- Line 145: Trailing whitespace
- Line 159: Trailing whitespace
- Line 163: Trailing whitespace
- Line 167: Trailing whitespace
- Line 173: Trailing whitespace
- Line 178: Trailing whitespace
- Line 183: Trailing whitespace
- Line 185: Trailing whitespace
- Line 191: Trailing whitespace
- Line 196: Trailing whitespace
- Line 200: Trailing whitespace
- Line 203: Trailing whitespace
- Line 209: Trailing whitespace
- Line 216: Trailing whitespace
- Line 225: Trailing whitespace
- Line 234: Trailing whitespace
- Line 243: Trailing whitespace
- Line 252: Trailing whitespace
- Line 267: Trailing whitespace
- Line 283: Trailing whitespace
- Line 291: Trailing whitespace
- Line 294: Trailing whitespace
- Line 298: Trailing whitespace
- Line 301: Trailing whitespace
- Line 305: Trailing whitespace

### tests/test_wifi_scanner.py
- Line 30: E501 line too long (81 > 79 characters)
- Line 95: E501 line too long (81 > 79 characters)

### src/piwardrive/mqtt/__init__.py
- Line 21: W293 blank line contains whitespace
- Line 42: W293 blank line contains whitespace
- Line 21: Trailing whitespace
- Line 42: Trailing whitespace

### tests/test_imports.py
- Line 67: E501 line too long (88 > 79 characters)
- Line 77: E501 line too long (82 > 79 characters)
- Line 172: E501 line too long (88 > 79 characters)

### tests/test_core_persistence.py
- Line 47: W293 blank line contains whitespace
- Line 51: E501 line too long (99 > 79 characters)
- Line 54: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 66: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 77: E501 line too long (99 > 79 characters)
- Line 80: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 96: E501 line too long (99 > 79 characters)
- Line 99: W293 blank line contains whitespace
- Line 102: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 107: E501 line too long (94 > 79 characters)
- Line 110: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 126: W293 blank line contains whitespace
- Line 130: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 143: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 155: E501 line too long (99 > 79 characters)
- Line 157: W293 blank line contains whitespace
- Line 166: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 172: W293 blank line contains whitespace
- Line 179: W293 blank line contains whitespace
- Line 183: E501 line too long (99 > 79 characters)
- Line 185: W293 blank line contains whitespace
- Line 188: E226 missing whitespace around arithmetic operator
- Line 188: E226 missing whitespace around arithmetic operator
- Line 188: E226 missing whitespace around arithmetic operator
- Line 188: E501 line too long (92 > 79 characters)
- Line 188: E226 missing whitespace around arithmetic operator
- Line 188: E226 missing whitespace around arithmetic operator
- Line 191: W293 blank line contains whitespace
- Line 195: W293 blank line contains whitespace
- Line 198: W293 blank line contains whitespace
- Line 201: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 210: E501 line too long (99 > 79 characters)
- Line 212: W293 blank line contains whitespace
- Line 215: E226 missing whitespace around arithmetic operator
- Line 215: E226 missing whitespace around arithmetic operator
- Line 215: E226 missing whitespace around arithmetic operator
- Line 215: E501 line too long (92 > 79 characters)
- Line 215: E226 missing whitespace around arithmetic operator
- Line 215: E226 missing whitespace around arithmetic operator
- Line 218: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 230: W293 blank line contains whitespace
- Line 234: E501 line too long (99 > 79 characters)
- Line 236: W293 blank line contains whitespace
- Line 240: W293 blank line contains whitespace
- Line 243: E501 line too long (81 > 79 characters)
- Line 245: W293 blank line contains whitespace
- Line 248: E501 line too long (80 > 79 characters)
- Line 250: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 266: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 274: E501 line too long (99 > 79 characters)
- Line 276: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 295: E501 line too long (85 > 79 characters)
- Line 298: W293 blank line contains whitespace
- Line 302: W293 blank line contains whitespace
- Line 309: W293 blank line contains whitespace
- Line 313: E501 line too long (99 > 79 characters)
- Line 315: W293 blank line contains whitespace
- Line 322: W293 blank line contains whitespace
- Line 325: W293 blank line contains whitespace
- Line 328: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 337: E501 line too long (99 > 79 characters)
- Line 339: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 347: W293 blank line contains whitespace
- Line 351: E501 line too long (99 > 79 characters)
- Line 353: W293 blank line contains whitespace
- Line 361: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 385: E501 line too long (99 > 79 characters)
- Line 387: W293 blank line contains whitespace
- Line 391: E501 line too long (82 > 79 characters)
- Line 396: W293 blank line contains whitespace
- Line 399: W293 blank line contains whitespace
- Line 402: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 410: E501 line too long (99 > 79 characters)
- Line 412: W293 blank line contains whitespace
- Line 415: W293 blank line contains whitespace
- Line 419: W293 blank line contains whitespace
- Line 423: E501 line too long (99 > 79 characters)
- Line 425: W293 blank line contains whitespace
- Line 463: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 470: E501 line too long (82 > 79 characters)
- Line 471: E501 line too long (84 > 79 characters)
- Line 477: W293 blank line contains whitespace
- Line 481: E501 line too long (99 > 79 characters)
- Line 483: W293 blank line contains whitespace
- Line 486: E226 missing whitespace around arithmetic operator
- Line 486: E226 missing whitespace around arithmetic operator
- Line 486: E501 line too long (86 > 79 characters)
- Line 491: W293 blank line contains whitespace
- Line 494: W293 blank line contains whitespace
- Line 498: W293 blank line contains whitespace
- Line 501: W293 blank line contains whitespace
- Line 502: E501 line too long (86 > 79 characters)
- Line 505: E501 line too long (87 > 79 characters)
- Line 507: W293 blank line contains whitespace
- Line 511: E501 line too long (99 > 79 characters)
- Line 513: W293 blank line contains whitespace
- Line 515: E501 line too long (80 > 79 characters)
- Line 517: W293 blank line contains whitespace
- Line 520: W293 blank line contains whitespace
- Line 524: W293 blank line contains whitespace
- Line 528: W293 blank line contains whitespace
- Line 532: W293 blank line contains whitespace
- Line 537: W293 blank line contains whitespace
- Line 542: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 548: E501 line too long (99 > 79 characters)
- Line 553: W293 blank line contains whitespace
- Line 564: W293 blank line contains whitespace
- Line 573: W293 blank line contains whitespace
- Line 578: W293 blank line contains whitespace
- Line 582: W293 blank line contains whitespace
- Line 585: W293 blank line contains whitespace
- Line 588: W293 blank line contains whitespace
- Line 591: W293 blank line contains whitespace
- Line 596: W293 blank line contains whitespace
- Line 599: W293 blank line contains whitespace
- Line 603: E501 line too long (99 > 79 characters)
- Line 605: W293 blank line contains whitespace
- Line 608: E226 missing whitespace around arithmetic operator
- Line 608: E501 line too long (84 > 79 characters)
- Line 613: W293 blank line contains whitespace
- Line 616: W293 blank line contains whitespace
- Line 622: W293 blank line contains whitespace
- Line 629: W293 blank line contains whitespace
- Line 633: E501 line too long (99 > 79 characters)
- Line 638: E501 line too long (85 > 79 characters)
- Line 639: W293 blank line contains whitespace
- Line 643: E501 line too long (99 > 79 characters)
- Line 645: W293 blank line contains whitespace
- Line 654: W293 blank line contains whitespace
- Line 660: E501 line too long (81 > 79 characters)
- Line 661: W293 blank line contains whitespace
- Line 665: E501 line too long (99 > 79 characters)
- Line 667: W293 blank line contains whitespace
- Line 672: W293 blank line contains whitespace
- Line 678: E501 line too long (84 > 79 characters)
- Line 679: W293 blank line contains whitespace
- Line 683: E501 line too long (99 > 79 characters)
- Line 685: W293 blank line contains whitespace
- Line 690: E226 missing whitespace around arithmetic operator
- Line 690: E226 missing whitespace around arithmetic operator
- Line 697: W293 blank line contains whitespace
- Line 701: W293 blank line contains whitespace
- Line 47: Trailing whitespace
- Line 54: Trailing whitespace
- Line 58: Trailing whitespace
- Line 62: Trailing whitespace
- Line 66: Trailing whitespace
- Line 71: Trailing whitespace
- Line 73: Trailing whitespace
- Line 80: Trailing whitespace
- Line 84: Trailing whitespace
- Line 89: Trailing whitespace
- Line 92: Trailing whitespace
- Line 99: Trailing whitespace
- Line 102: Trailing whitespace
- Line 106: Trailing whitespace
- Line 110: Trailing whitespace
- Line 112: Trailing whitespace
- Line 118: Trailing whitespace
- Line 122: Trailing whitespace
- Line 126: Trailing whitespace
- Line 130: Trailing whitespace
- Line 140: Trailing whitespace
- Line 143: Trailing whitespace
- Line 151: Trailing whitespace
- Line 157: Trailing whitespace
- Line 166: Trailing whitespace
- Line 169: Trailing whitespace
- Line 172: Trailing whitespace
- Line 179: Trailing whitespace
- Line 185: Trailing whitespace
- Line 191: Trailing whitespace
- Line 195: Trailing whitespace
- Line 198: Trailing whitespace
- Line 201: Trailing whitespace
- Line 206: Trailing whitespace
- Line 212: Trailing whitespace
- Line 218: Trailing whitespace
- Line 221: Trailing whitespace
- Line 225: Trailing whitespace
- Line 230: Trailing whitespace
- Line 236: Trailing whitespace
- Line 240: Trailing whitespace
- Line 245: Trailing whitespace
- Line 250: Trailing whitespace
- Line 254: Trailing whitespace
- Line 258: Trailing whitespace
- Line 262: Trailing whitespace
- Line 266: Trailing whitespace
- Line 270: Trailing whitespace
- Line 276: Trailing whitespace
- Line 294: Trailing whitespace
- Line 298: Trailing whitespace
- Line 302: Trailing whitespace
- Line 309: Trailing whitespace
- Line 315: Trailing whitespace
- Line 322: Trailing whitespace
- Line 325: Trailing whitespace
- Line 328: Trailing whitespace
- Line 333: Trailing whitespace
- Line 339: Trailing whitespace
- Line 342: Trailing whitespace
- Line 347: Trailing whitespace
- Line 353: Trailing whitespace
- Line 361: Trailing whitespace
- Line 369: Trailing whitespace
- Line 372: Trailing whitespace
- Line 381: Trailing whitespace
- Line 387: Trailing whitespace
- Line 396: Trailing whitespace
- Line 399: Trailing whitespace
- Line 402: Trailing whitespace
- Line 406: Trailing whitespace
- Line 412: Trailing whitespace
- Line 415: Trailing whitespace
- Line 419: Trailing whitespace
- Line 425: Trailing whitespace
- Line 463: Trailing whitespace
- Line 467: Trailing whitespace
- Line 477: Trailing whitespace
- Line 483: Trailing whitespace
- Line 491: Trailing whitespace
- Line 494: Trailing whitespace
- Line 498: Trailing whitespace
- Line 501: Trailing whitespace
- Line 507: Trailing whitespace
- Line 513: Trailing whitespace
- Line 517: Trailing whitespace
- Line 520: Trailing whitespace
- Line 524: Trailing whitespace
- Line 528: Trailing whitespace
- Line 532: Trailing whitespace
- Line 537: Trailing whitespace
- Line 542: Trailing whitespace
- Line 544: Trailing whitespace
- Line 553: Trailing whitespace
- Line 564: Trailing whitespace
- Line 573: Trailing whitespace
- Line 578: Trailing whitespace
- Line 582: Trailing whitespace
- Line 585: Trailing whitespace
- Line 588: Trailing whitespace
- Line 591: Trailing whitespace
- Line 596: Trailing whitespace
- Line 599: Trailing whitespace
- Line 605: Trailing whitespace
- Line 613: Trailing whitespace
- Line 616: Trailing whitespace
- Line 622: Trailing whitespace
- Line 629: Trailing whitespace
- Line 639: Trailing whitespace
- Line 645: Trailing whitespace
- Line 654: Trailing whitespace
- Line 661: Trailing whitespace
- Line 667: Trailing whitespace
- Line 672: Trailing whitespace
- Line 679: Trailing whitespace
- Line 685: Trailing whitespace
- Line 697: Trailing whitespace
- Line 701: Trailing whitespace

### src/gps_handler.py
- Line 38: W293 blank line contains whitespace
- Line 88: E501 line too long (87 > 79 characters)
- Line 90: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 132: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 38: Trailing whitespace
- Line 90: Trailing whitespace
- Line 93: Trailing whitespace
- Line 111: Trailing whitespace
- Line 114: Trailing whitespace
- Line 132: Trailing whitespace
- Line 135: Trailing whitespace

### src/piwardrive/db/adapter.py
- Line 18: E501 line too long (88 > 79 characters)

### src/piwardrive/analytics/explain.py
- Line 21: E501 line too long (84 > 79 characters)
- Line 22: E501 line too long (85 > 79 characters)
- Line 23: E501 line too long (88 > 79 characters)

### tests/test_localization.py
- Line 20: E402 module level import not at top of file
- Line 78: W293 blank line contains whitespace
- Line 82: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 89: E501 line too long (80 > 79 characters)
- Line 101: W293 blank line contains whitespace
- Line 108: E501 line too long (83 > 79 characters)
- Line 114: E501 line too long (101 > 79 characters)
- Line 130: W293 blank line contains whitespace
- Line 136: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 152: E501 line too long (93 > 79 characters)
- Line 154: E501 line too long (93 > 79 characters)
- Line 157: W293 blank line contains whitespace
- Line 160: E501 line too long (99 > 79 characters)
- Line 161: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 187: E501 line too long (104 > 79 characters)
- Line 189: W293 blank line contains whitespace
- Line 192: E501 line too long (83 > 79 characters)
- Line 193: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 217: W293 blank line contains whitespace
- Line 223: W293 blank line contains whitespace
- Line 226: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 238: W293 blank line contains whitespace
- Line 251: E501 line too long (82 > 79 characters)
- Line 253: E501 line too long (80 > 79 characters)
- Line 254: W293 blank line contains whitespace
- Line 256: W293 blank line contains whitespace
- Line 259: E501 line too long (96 > 79 characters)
- Line 262: E501 line too long (81 > 79 characters)
- Line 269: W293 blank line contains whitespace
- Line 270: E501 line too long (98 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 275: W293 blank line contains whitespace
- Line 278: E501 line too long (81 > 79 characters)
- Line 288: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 304: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 310: W293 blank line contains whitespace
- Line 313: E501 line too long (80 > 79 characters)
- Line 314: E501 line too long (89 > 79 characters)
- Line 322: W293 blank line contains whitespace
- Line 326: E501 line too long (93 > 79 characters)
- Line 328: E501 line too long (93 > 79 characters)
- Line 330: W293 blank line contains whitespace
- Line 333: E501 line too long (99 > 79 characters)
- Line 334: W293 blank line contains whitespace
- Line 339: W293 blank line contains whitespace
- Line 78: Trailing whitespace
- Line 82: Trailing whitespace
- Line 86: Trailing whitespace
- Line 101: Trailing whitespace
- Line 130: Trailing whitespace
- Line 136: Trailing whitespace
- Line 140: Trailing whitespace
- Line 148: Trailing whitespace
- Line 157: Trailing whitespace
- Line 161: Trailing whitespace
- Line 164: Trailing whitespace
- Line 176: Trailing whitespace
- Line 183: Trailing whitespace
- Line 189: Trailing whitespace
- Line 193: Trailing whitespace
- Line 199: Trailing whitespace
- Line 205: Trailing whitespace
- Line 215: Trailing whitespace
- Line 217: Trailing whitespace
- Line 223: Trailing whitespace
- Line 226: Trailing whitespace
- Line 234: Trailing whitespace
- Line 238: Trailing whitespace
- Line 254: Trailing whitespace
- Line 256: Trailing whitespace
- Line 269: Trailing whitespace
- Line 271: Trailing whitespace
- Line 275: Trailing whitespace
- Line 288: Trailing whitespace
- Line 291: Trailing whitespace
- Line 304: Trailing whitespace
- Line 306: Trailing whitespace
- Line 310: Trailing whitespace
- Line 322: Trailing whitespace
- Line 330: Trailing whitespace
- Line 334: Trailing whitespace
- Line 339: Trailing whitespace

### scripts/test_db_improvements.py
- Line 100: E501 line too long (96 > 79 characters)
- Line 101: E501 line too long (93 > 79 characters)
- Line 102: E501 line too long (97 > 79 characters)
- Line 103: E501 line too long (85 > 79 characters)
- Line 104: E501 line too long (92 > 79 characters)

### src/piwardrive/api/system/endpoints_simple.py
- Line 9: E302 expected 2 blank lines, found 1
- Line 17: E302 expected 2 blank lines, found 1
- Line 22: E302 expected 2 blank lines, found 1
- Line 23: E501 line too long (80 > 79 characters)
- Line 27: E302 expected 2 blank lines, found 1

### src/piwardrive/performance/realtime_optimizer.py
- Line 25: E302 expected 2 blank lines, found 1
- Line 56: E303 too many blank lines (3)
- Line 61: W293 blank line contains whitespace
- Line 71: E501 line too long (86 > 79 characters)
- Line 81: E501 line too long (83 > 79 characters)
- Line 108: E501 line too long (81 > 79 characters)
- Line 115: E501 line too long (80 > 79 characters)
- Line 133: E501 line too long (86 > 79 characters)
- Line 174: E501 line too long (83 > 79 characters)
- Line 250: W293 blank line contains whitespace
- Line 302: E501 line too long (85 > 79 characters)
- Line 377: W293 blank line contains whitespace
- Line 388: E501 line too long (87 > 79 characters)
- Line 418: E501 line too long (88 > 79 characters)
- Line 443: E303 too many blank lines (3)
- Line 447: E501 line too long (80 > 79 characters)
- Line 463: E501 line too long (81 > 79 characters)
- Line 471: E501 line too long (81 > 79 characters)
- Line 475: E501 line too long (82 > 79 characters)
- Line 480: E501 line too long (83 > 79 characters)
- Line 483: E501 line too long (85 > 79 characters)
- Line 509: E501 line too long (82 > 79 characters)
- Line 538: E501 line too long (85 > 79 characters)
- Line 551: E501 line too long (83 > 79 characters)
- Line 567: E501 line too long (84 > 79 characters)
- Line 574: E501 line too long (84 > 79 characters)
- Line 587: E501 line too long (110 > 79 characters)
- Line 590: E302 expected 2 blank lines, found 1
- Line 602: E501 line too long (80 > 79 characters)
- Line 614: E501 line too long (81 > 79 characters)
- Line 632: E302 expected 2 blank lines, found 1
- Line 687: E501 line too long (115 > 79 characters)
- Line 61: Trailing whitespace
- Line 250: Trailing whitespace
- Line 377: Trailing whitespace

### tests/test_cache_security_fixed.py
- Line 13: W291 trailing whitespace
- Line 14: W291 trailing whitespace
- Line 47: W293 blank line contains whitespace
- Line 50: E306 expected 1 blank line before a nested definition, found 0
- Line 54: W293 blank line contains whitespace
- Line 61: W293 blank line contains whitespace
- Line 63: E306 expected 1 blank line before a nested definition, found 0
- Line 66: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 76: E306 expected 1 blank line before a nested definition, found 0
- Line 78: E501 line too long (98 > 79 characters)
- Line 79: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 90: E306 expected 1 blank line before a nested definition, found 0
- Line 93: E501 line too long (80 > 79 characters)
- Line 94: W293 blank line contains whitespace
- Line 105: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 129: W293 blank line contains whitespace
- Line 132: E501 line too long (80 > 79 characters)
- Line 134: W293 blank line contains whitespace
- Line 142: W293 blank line contains whitespace
- Line 147: E501 line too long (81 > 79 characters)
- Line 150: W293 blank line contains whitespace
- Line 157: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 172: W293 blank line contains whitespace
- Line 179: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 202: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 213: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 224: W293 blank line contains whitespace
- Line 13: Trailing whitespace
- Line 14: Trailing whitespace
- Line 47: Trailing whitespace
- Line 54: Trailing whitespace
- Line 61: Trailing whitespace
- Line 66: Trailing whitespace
- Line 74: Trailing whitespace
- Line 79: Trailing whitespace
- Line 88: Trailing whitespace
- Line 94: Trailing whitespace
- Line 105: Trailing whitespace
- Line 114: Trailing whitespace
- Line 122: Trailing whitespace
- Line 129: Trailing whitespace
- Line 134: Trailing whitespace
- Line 142: Trailing whitespace
- Line 150: Trailing whitespace
- Line 157: Trailing whitespace
- Line 164: Trailing whitespace
- Line 172: Trailing whitespace
- Line 179: Trailing whitespace
- Line 188: Trailing whitespace
- Line 194: Trailing whitespace
- Line 202: Trailing whitespace
- Line 205: Trailing whitespace
- Line 213: Trailing whitespace
- Line 221: Trailing whitespace
- Line 224: Trailing whitespace

### src/piwardrive/models/api_models.py
- Line 34: E501 line too long (80 > 79 characters)
- Line 35: E501 line too long (86 > 79 characters)
- Line 113: E501 line too long (80 > 79 characters)
- Line 147: E501 line too long (80 > 79 characters)
- Line 201: E501 line too long (82 > 79 characters)
- Line 232: E501 line too long (80 > 79 characters)
- Line 274: E501 line too long (82 > 79 characters)
- Line 275: E501 line too long (80 > 79 characters)

### tests/test_utils_comprehensive.py
- Line 23: E402 module level import not at top of file
- Line 24: E402 module level import not at top of file
- Line 32: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 53: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 75: W293 blank line contains whitespace
- Line 82: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 146: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 158: W293 blank line contains whitespace
- Line 160: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 189: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 198: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 211: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 227: W293 blank line contains whitespace
- Line 231: E501 line too long (82 > 79 characters)
- Line 235: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 238: E501 line too long (85 > 79 characters)
- Line 243: W293 blank line contains whitespace
- Line 248: W293 blank line contains whitespace
- Line 254: E501 line too long (120 > 79 characters)
- Line 255: E501 line too long (81 > 79 characters)
- Line 256: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 273: W293 blank line contains whitespace
- Line 275: W293 blank line contains whitespace
- Line 277: E501 line too long (91 > 79 characters)
- Line 278: W293 blank line contains whitespace
- Line 284: W293 blank line contains whitespace
- Line 286: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 299: W293 blank line contains whitespace
- Line 304: W293 blank line contains whitespace
- Line 310: W293 blank line contains whitespace
- Line 312: W293 blank line contains whitespace
- Line 321: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 351: W293 blank line contains whitespace
- Line 355: W293 blank line contains whitespace
- Line 358: W293 blank line contains whitespace
- Line 361: W293 blank line contains whitespace
- Line 368: W293 blank line contains whitespace
- Line 32: Trailing whitespace
- Line 38: Trailing whitespace
- Line 44: Trailing whitespace
- Line 53: Trailing whitespace
- Line 62: Trailing whitespace
- Line 75: Trailing whitespace
- Line 82: Trailing whitespace
- Line 88: Trailing whitespace
- Line 94: Trailing whitespace
- Line 104: Trailing whitespace
- Line 111: Trailing whitespace
- Line 114: Trailing whitespace
- Line 125: Trailing whitespace
- Line 131: Trailing whitespace
- Line 133: Trailing whitespace
- Line 138: Trailing whitespace
- Line 144: Trailing whitespace
- Line 146: Trailing whitespace
- Line 151: Trailing whitespace
- Line 158: Trailing whitespace
- Line 160: Trailing whitespace
- Line 165: Trailing whitespace
- Line 171: Trailing whitespace
- Line 173: Trailing whitespace
- Line 178: Trailing whitespace
- Line 189: Trailing whitespace
- Line 191: Trailing whitespace
- Line 194: Trailing whitespace
- Line 198: Trailing whitespace
- Line 205: Trailing whitespace
- Line 208: Trailing whitespace
- Line 211: Trailing whitespace
- Line 221: Trailing whitespace
- Line 227: Trailing whitespace
- Line 235: Trailing whitespace
- Line 237: Trailing whitespace
- Line 243: Trailing whitespace
- Line 248: Trailing whitespace
- Line 256: Trailing whitespace
- Line 267: Trailing whitespace
- Line 273: Trailing whitespace
- Line 275: Trailing whitespace
- Line 278: Trailing whitespace
- Line 284: Trailing whitespace
- Line 286: Trailing whitespace
- Line 291: Trailing whitespace
- Line 297: Trailing whitespace
- Line 299: Trailing whitespace
- Line 304: Trailing whitespace
- Line 310: Trailing whitespace
- Line 312: Trailing whitespace
- Line 321: Trailing whitespace
- Line 326: Trailing whitespace
- Line 332: Trailing whitespace
- Line 342: Trailing whitespace
- Line 351: Trailing whitespace
- Line 355: Trailing whitespace
- Line 358: Trailing whitespace
- Line 361: Trailing whitespace
- Line 368: Trailing whitespace

### tests/test_core_config_extra.py
- Line 86: E501 line too long (87 > 79 characters)

### src/piwardrive/main.py
- Line 16: E501 line too long (88 > 79 characters)
- Line 28: E501 line too long (85 > 79 characters)
- Line 47: W293 blank line contains whitespace
- Line 77: E501 line too long (87 > 79 characters)
- Line 85: W503 line break before binary operator
- Line 100: E501 line too long (84 > 79 characters)
- Line 110: W503 line break before binary operator
- Line 129: E501 line too long (82 > 79 characters)
- Line 136: E501 line too long (82 > 79 characters)
- Line 143: E501 line too long (80 > 79 characters)
- Line 167: E501 line too long (82 > 79 characters)
- Line 168: E501 line too long (82 > 79 characters)
- Line 173: E501 line too long (85 > 79 characters)
- Line 190: E501 line too long (88 > 79 characters)
- Line 208: E501 line too long (84 > 79 characters)
- Line 248: E501 line too long (81 > 79 characters)
- Line 47: Trailing whitespace

### tests/test_remote_sync.py
- Line 58: E501 line too long (85 > 79 characters)
- Line 118: E501 line too long (81 > 79 characters)
- Line 152: E501 line too long (81 > 79 characters)
- Line 166: E501 line too long (81 > 79 characters)
- Line 218: E501 line too long (85 > 79 characters)
- Line 344: E501 line too long (86 > 79 characters)
- Line 347: E501 line too long (81 > 79 characters)

### tests/test_extra_widgets.py
- Line 19: E501 line too long (87 > 79 characters)
- Line 28: E501 line too long (85 > 79 characters)

### tests/test_aggregation_service.py
- Line 29: E501 line too long (86 > 79 characters)
- Line 30: E501 line too long (86 > 79 characters)
- Line 31: E501 line too long (80 > 79 characters)
- Line 32: E501 line too long (80 > 79 characters)

### tests/test_load_kismet_data.py
- Line 12: E501 line too long (80 > 79 characters)
- Line 16: E501 line too long (82 > 79 characters)
- Line 20: E501 line too long (82 > 79 characters)
- Line 22: E501 line too long (84 > 79 characters)
- Line 28: E501 line too long (80 > 79 characters)

### tests/test_service_direct.py
- Line 7: E302 expected 2 blank lines, found 1
- Line 11: W293 blank line contains whitespace
- Line 20: W293 blank line contains whitespace
- Line 24: W293 blank line contains whitespace
- Line 27: W293 blank line contains whitespace
- Line 32: E501 line too long (91 > 79 characters)
- Line 39: W293 blank line contains whitespace
- Line 46: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 96: W293 blank line contains whitespace
- Line 99: W293 blank line contains whitespace
- Line 100: E501 line too long (83 > 79 characters)
- Line 107: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 119: E501 line too long (80 > 79 characters)
- Line 124: E501 line too long (82 > 79 characters)
- Line 140: E501 line too long (80 > 79 characters)
- Line 141: W293 blank line contains whitespace
- Line 146: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 11: Trailing whitespace
- Line 20: Trailing whitespace
- Line 24: Trailing whitespace
- Line 27: Trailing whitespace
- Line 39: Trailing whitespace
- Line 46: Trailing whitespace
- Line 57: Trailing whitespace
- Line 65: Trailing whitespace
- Line 84: Trailing whitespace
- Line 92: Trailing whitespace
- Line 96: Trailing whitespace
- Line 99: Trailing whitespace
- Line 107: Trailing whitespace
- Line 111: Trailing whitespace
- Line 118: Trailing whitespace
- Line 141: Trailing whitespace
- Line 146: Trailing whitespace
- Line 154: Trailing whitespace

### fix_remaining_syntax.py
- Line 11: E302 expected 2 blank lines, found 1
- Line 16: W293 blank line contains whitespace
- Line 18: W293 blank line contains whitespace
- Line 23: W293 blank line contains whitespace
- Line 26: W293 blank line contains whitespace
- Line 29: W293 blank line contains whitespace
- Line 33: W293 blank line contains whitespace
- Line 36: W293 blank line contains whitespace
- Line 39: E501 line too long (82 > 79 characters)
- Line 44: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 56: E302 expected 2 blank lines, found 1
- Line 61: W293 blank line contains whitespace
- Line 64: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 77: E302 expected 2 blank lines, found 1
- Line 82: W293 blank line contains whitespace
- Line 86: E501 line too long (87 > 79 characters)
- Line 91: E226 missing whitespace around arithmetic operator
- Line 92: E501 line too long (94 > 79 characters)
- Line 94: E501 line too long (113 > 79 characters)
- Line 102: W293 blank line contains whitespace
- Line 105: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 112: E302 expected 2 blank lines, found 1
- Line 117: W293 blank line contains whitespace
- Line 121: E501 line too long (96 > 79 characters)
- Line 122: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 129: W293 blank line contains whitespace
- Line 132: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 137: W293 blank line contains whitespace
- Line 142: E302 expected 2 blank lines, found 1
- Line 144: W293 blank line contains whitespace
- Line 158: W293 blank line contains whitespace
- Line 162: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 179: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 196: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 217: W293 blank line contains whitespace
- Line 220: E305 expected 2 blank lines after class or function definition, found 1
- Line 16: Trailing whitespace
- Line 18: Trailing whitespace
- Line 23: Trailing whitespace
- Line 26: Trailing whitespace
- Line 29: Trailing whitespace
- Line 33: Trailing whitespace
- Line 36: Trailing whitespace
- Line 44: Trailing whitespace
- Line 49: Trailing whitespace
- Line 51: Trailing whitespace
- Line 61: Trailing whitespace
- Line 64: Trailing whitespace
- Line 67: Trailing whitespace
- Line 70: Trailing whitespace
- Line 72: Trailing whitespace
- Line 82: Trailing whitespace
- Line 102: Trailing whitespace
- Line 105: Trailing whitespace
- Line 107: Trailing whitespace
- Line 117: Trailing whitespace
- Line 122: Trailing whitespace
- Line 125: Trailing whitespace
- Line 129: Trailing whitespace
- Line 132: Trailing whitespace
- Line 135: Trailing whitespace
- Line 137: Trailing whitespace
- Line 144: Trailing whitespace
- Line 158: Trailing whitespace
- Line 162: Trailing whitespace
- Line 169: Trailing whitespace
- Line 173: Trailing whitespace
- Line 176: Trailing whitespace
- Line 179: Trailing whitespace
- Line 183: Trailing whitespace
- Line 185: Trailing whitespace
- Line 188: Trailing whitespace
- Line 192: Trailing whitespace
- Line 196: Trailing whitespace
- Line 200: Trailing whitespace
- Line 204: Trailing whitespace
- Line 207: Trailing whitespace
- Line 217: Trailing whitespace

### src/piwardrive/migrations/008_create_network_analytics.py
- Line 36: E501 line too long (88 > 79 characters)
- Line 39: E501 line too long (95 > 79 characters)
- Line 42: E501 line too long (104 > 79 characters)

### src/piwardrive/api/system/monitoring.py
- Line 24: E501 line too long (80 > 79 characters)
- Line 37: E501 line too long (88 > 79 characters)
- Line 59: E501 line too long (81 > 79 characters)
- Line 61: E501 line too long (85 > 79 characters)

### src/piwardrive/services/export_service.py
- Line 41: E501 line too long (88 > 79 characters)

### src/piwardrive/orientation_sensors.py
- Line 50: E501 line too long (80 > 79 characters)
- Line 61: E501 line too long (82 > 79 characters)
- Line 73: E501 line too long (83 > 79 characters)
- Line 94: E501 line too long (85 > 79 characters)
- Line 123: E501 line too long (83 > 79 characters)
- Line 164: E501 line too long (87 > 79 characters)
- Line 165: E501 line too long (80 > 79 characters)

### src/piwardrive/geospatial/intelligence.py
- Line 39: E302 expected 2 blank lines, found 1
- Line 51: E302 expected 2 blank lines, found 1
- Line 62: E302 expected 2 blank lines, found 1
- Line 72: E302 expected 2 blank lines, found 1
- Line 81: E302 expected 2 blank lines, found 1
- Line 91: E302 expected 2 blank lines, found 1
- Line 102: E302 expected 2 blank lines, found 1
- Line 146: E501 line too long (84 > 79 characters)
- Line 159: E501 line too long (83 > 79 characters)
- Line 308: E501 line too long (87 > 79 characters)
- Line 372: E501 line too long (80 > 79 characters)
- Line 403: E501 line too long (88 > 79 characters)
- Line 452: E203 whitespace before ':'
- Line 455: W503 line break before binary operator
- Line 488: E501 line too long (87 > 79 characters)
- Line 537: E501 line too long (88 > 79 characters)
- Line 567: W503 line break before binary operator
- Line 568: W503 line break before binary operator
- Line 579: E501 line too long (88 > 79 characters)
- Line 633: E501 line too long (88 > 79 characters)
- Line 687: E302 expected 2 blank lines, found 1
- Line 778: E501 line too long (81 > 79 characters)
- Line 791: E501 line too long (86 > 79 characters)
- Line 792: E501 line too long (87 > 79 characters)
- Line 793: E501 line too long (86 > 79 characters)
- Line 821: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/logging/levels.py
- Line 42: E501 line too long (84 > 79 characters)
- Line 83: E501 line too long (87 > 79 characters)

### src/piwardrive/services/view_refresher.py
- Line 15: W293 blank line contains whitespace
- Line 15: Trailing whitespace

### src/piwardrive/scripts/__init__.py
- Line 6: E501 line too long (80 > 79 characters)
- Line 16: E501 line too long (86 > 79 characters)

### tests/test_service_comprehensive.py
- Line 20: E402 module level import not at top of file
- Line 49: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 59: E501 line too long (86 > 79 characters)
- Line 63: E501 line too long (80 > 79 characters)
- Line 64: W293 blank line contains whitespace
- Line 66: W293 blank line contains whitespace
- Line 74: E501 line too long (87 > 79 characters)
- Line 79: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 95: W293 blank line contains whitespace
- Line 99: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 134: W293 blank line contains whitespace
- Line 139: W293 blank line contains whitespace
- Line 141: W293 blank line contains whitespace
- Line 148: E501 line too long (99 > 79 characters)
- Line 149: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 223: E501 line too long (85 > 79 characters)
- Line 239: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 257: W293 blank line contains whitespace
- Line 266: E501 line too long (81 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 273: W293 blank line contains whitespace
- Line 49: Trailing whitespace
- Line 51: Trailing whitespace
- Line 64: Trailing whitespace
- Line 66: Trailing whitespace
- Line 79: Trailing whitespace
- Line 81: Trailing whitespace
- Line 95: Trailing whitespace
- Line 99: Trailing whitespace
- Line 107: Trailing whitespace
- Line 109: Trailing whitespace
- Line 120: Trailing whitespace
- Line 122: Trailing whitespace
- Line 134: Trailing whitespace
- Line 139: Trailing whitespace
- Line 141: Trailing whitespace
- Line 149: Trailing whitespace
- Line 154: Trailing whitespace
- Line 156: Trailing whitespace
- Line 164: Trailing whitespace
- Line 169: Trailing whitespace
- Line 171: Trailing whitespace
- Line 183: Trailing whitespace
- Line 194: Trailing whitespace
- Line 239: Trailing whitespace
- Line 254: Trailing whitespace
- Line 257: Trailing whitespace
- Line 271: Trailing whitespace
- Line 273: Trailing whitespace

### scripts/vector_tile_customizer_cli.py
- Line 15: E501 line too long (83 > 79 characters)

### fix_quality_issues.py
- Line 10: E302 expected 2 blank lines, found 1
- Line 15: W293 blank line contains whitespace
- Line 18: W293 blank line contains whitespace
- Line 21: W293 blank line contains whitespace
- Line 25: E501 line too long (83 > 79 characters)
- Line 28: W293 blank line contains whitespace
- Line 30: E501 line too long (109 > 79 characters)
- Line 35: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 52: E302 expected 2 blank lines, found 1
- Line 52: E501 line too long (83 > 79 characters)
- Line 57: W293 blank line contains whitespace
- Line 60: W293 blank line contains whitespace
- Line 63: W293 blank line contains whitespace
- Line 64: E501 line too long (80 > 79 characters)
- Line 66: E501 line too long (122 > 79 characters)
- Line 71: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 79: E501 line too long (108 > 79 characters)
- Line 81: E501 line too long (105 > 79 characters)
- Line 82: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 98: E302 expected 2 blank lines, found 1
- Line 98: E501 line too long (91 > 79 characters)
- Line 103: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 137: W293 blank line contains whitespace
- Line 142: E302 expected 2 blank lines, found 1
- Line 144: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 158: E501 line too long (99 > 79 characters)
- Line 160: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 180: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 186: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 195: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 213: E501 line too long (86 > 79 characters)
- Line 216: W293 blank line contains whitespace
- Line 219: E501 line too long (94 > 79 characters)
- Line 222: W293 blank line contains whitespace
- Line 224: W293 blank line contains whitespace
- Line 236: E305 expected 2 blank lines after class or function definition, found 1
- Line 15: Trailing whitespace
- Line 18: Trailing whitespace
- Line 21: Trailing whitespace
- Line 28: Trailing whitespace
- Line 35: Trailing whitespace
- Line 38: Trailing whitespace
- Line 45: Trailing whitespace
- Line 47: Trailing whitespace
- Line 57: Trailing whitespace
- Line 60: Trailing whitespace
- Line 63: Trailing whitespace
- Line 66: Line too long (122 > 120 characters)
- Line 71: Trailing whitespace
- Line 77: Trailing whitespace
- Line 82: Trailing whitespace
- Line 84: Trailing whitespace
- Line 91: Trailing whitespace
- Line 93: Trailing whitespace
- Line 103: Trailing whitespace
- Line 106: Trailing whitespace
- Line 117: Trailing whitespace
- Line 128: Trailing whitespace
- Line 135: Trailing whitespace
- Line 137: Trailing whitespace
- Line 144: Trailing whitespace
- Line 154: Trailing whitespace
- Line 160: Trailing whitespace
- Line 163: Trailing whitespace
- Line 168: Trailing whitespace
- Line 180: Trailing whitespace
- Line 183: Trailing whitespace
- Line 186: Trailing whitespace
- Line 188: Trailing whitespace
- Line 195: Trailing whitespace
- Line 199: Trailing whitespace
- Line 204: Trailing whitespace
- Line 210: Trailing whitespace
- Line 216: Trailing whitespace
- Line 222: Trailing whitespace
- Line 224: Trailing whitespace

### src/piwardrive/api/widgets/__init__.py
- Line 29: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/analytics/forecasting.py
- Line 36: E501 line too long (82 > 79 characters)

### tests/test_plugins.py
- Line 8: E501 line too long (84 > 79 characters)
- Line 9: E501 line too long (84 > 79 characters)
- Line 18: E501 line too long (88 > 79 characters)

### tests/test_health_stats_script.py
- Line 18: E741 ambiguous variable name 'l'
- Line 18: E501 line too long (80 > 79 characters)
- Line 20: E501 line too long (85 > 79 characters)

### src/piwardrive/visualization/advanced_viz.py
- Line 67: E501 line too long (80 > 79 characters)
- Line 68: E501 line too long (80 > 79 characters)
- Line 115: E501 line too long (87 > 79 characters)
- Line 116: E501 line too long (87 > 79 characters)
- Line 124: E501 line too long (83 > 79 characters)
- Line 162: W503 line break before binary operator
- Line 174: W503 line break before binary operator
- Line 175: W503 line break before binary operator
- Line 176: W503 line break before binary operator
- Line 192: E501 line too long (87 > 79 characters)
- Line 230: E501 line too long (80 > 79 characters)
- Line 364: E501 line too long (80 > 79 characters)
- Line 368: E501 line too long (81 > 79 characters)
- Line 386: E501 line too long (81 > 79 characters)
- Line 390: E501 line too long (84 > 79 characters)
- Line 409: E501 line too long (84 > 79 characters)
- Line 550: E501 line too long (92 > 79 characters)
- Line 556: E501 line too long (87 > 79 characters)
- Line 569: E501 line too long (81 > 79 characters)
- Line 575: E501 line too long (82 > 79 characters)
- Line 671: E501 line too long (82 > 79 characters)
- Line 677: E501 line too long (81 > 79 characters)
- Line 683: E501 line too long (81 > 79 characters)
- Line 705: E501 line too long (84 > 79 characters)
- Line 708: E501 line too long (82 > 79 characters)
- Line 712: E501 line too long (84 > 79 characters)
- Line 716: E501 line too long (88 > 79 characters)
- Line 717: E501 line too long (88 > 79 characters)
- Line 720: E501 line too long (89 > 79 characters)
- Line 722: E501 line too long (93 > 79 characters)
- Line 724: E501 line too long (84 > 79 characters)
- Line 725: E501 line too long (89 > 79 characters)
- Line 733: E501 line too long (83 > 79 characters)
- Line 757: E501 line too long (81 > 79 characters)
- Line 780: E501 line too long (82 > 79 characters)
- Line 795: E501 line too long (84 > 79 characters)
- Line 803: E501 line too long (85 > 79 characters)
- Line 826: E501 line too long (80 > 79 characters)
- Line 829: E501 line too long (80 > 79 characters)
- Line 836: E501 line too long (80 > 79 characters)
- Line 861: E501 line too long (83 > 79 characters)
- Line 881: E501 line too long (81 > 79 characters)
- Line 919: E501 line too long (85 > 79 characters)
- Line 972: E501 line too long (83 > 79 characters)
- Line 973: E501 line too long (80 > 79 characters)
- Line 980: E501 line too long (87 > 79 characters)
- Line 990: E501 line too long (85 > 79 characters)
- Line 991: E501 line too long (82 > 79 characters)
- Line 997: E501 line too long (87 > 79 characters)
- Line 1048: E501 line too long (87 > 79 characters)
- Line 1054: E501 line too long (85 > 79 characters)
- Line 1063: E501 line too long (85 > 79 characters)
- Line 1119: E501 line too long (81 > 79 characters)
- Line 1134: E501 line too long (90 > 79 characters)
- Line 1149: E501 line too long (111 > 79 characters)

### src/piwardrive/api/common.py
- Line 63: E501 line too long (84 > 79 characters)

### tests/test_persistence_comprehensive.py
- Line 3: E501 line too long (84 > 79 characters)
- Line 29: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 56: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 82: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 116: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 129: W293 blank line contains whitespace
- Line 132: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 160: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 190: W293 blank line contains whitespace
- Line 193: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 214: E501 line too long (82 > 79 characters)
- Line 217: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 226: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 240: W293 blank line contains whitespace
- Line 245: E501 line too long (85 > 79 characters)
- Line 247: W293 blank line contains whitespace
- Line 251: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 261: W293 blank line contains whitespace
- Line 264: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 285: E501 line too long (83 > 79 characters)
- Line 287: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 293: W293 blank line contains whitespace
- Line 300: W293 blank line contains whitespace
- Line 303: W293 blank line contains whitespace
- Line 304: E501 line too long (93 > 79 characters)
- Line 310: W293 blank line contains whitespace
- Line 336: W293 blank line contains whitespace
- Line 337: E501 line too long (80 > 79 characters)
- Line 339: W293 blank line contains whitespace
- Line 344: W293 blank line contains whitespace
- Line 346: W293 blank line contains whitespace
- Line 349: E501 line too long (81 > 79 characters)
- Line 350: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 367: W293 blank line contains whitespace
- Line 370: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 384: W293 blank line contains whitespace
- Line 396: W293 blank line contains whitespace
- Line 404: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 417: W293 blank line contains whitespace
- Line 419: E501 line too long (100 > 79 characters)
- Line 426: E501 line too long (83 > 79 characters)
- Line 430: W293 blank line contains whitespace
- Line 436: W293 blank line contains whitespace
- Line 437: W291 trailing whitespace
- Line 443: W293 blank line contains whitespace
- Line 446: E501 line too long (99 > 79 characters)
- Line 450: E501 line too long (83 > 79 characters)
- Line 453: W293 blank line contains whitespace
- Line 454: E501 line too long (82 > 79 characters)
- Line 456: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 465: W293 blank line contains whitespace
- Line 467: E501 line too long (82 > 79 characters)
- Line 468: W293 blank line contains whitespace
- Line 469: E501 line too long (84 > 79 characters)
- Line 29: Trailing whitespace
- Line 38: Trailing whitespace
- Line 43: Trailing whitespace
- Line 51: Trailing whitespace
- Line 56: Trailing whitespace
- Line 65: Trailing whitespace
- Line 76: Trailing whitespace
- Line 82: Trailing whitespace
- Line 89: Trailing whitespace
- Line 92: Trailing whitespace
- Line 94: Trailing whitespace
- Line 101: Trailing whitespace
- Line 107: Trailing whitespace
- Line 116: Trailing whitespace
- Line 123: Trailing whitespace
- Line 129: Trailing whitespace
- Line 132: Trailing whitespace
- Line 138: Trailing whitespace
- Line 144: Trailing whitespace
- Line 147: Trailing whitespace
- Line 154: Trailing whitespace
- Line 160: Trailing whitespace
- Line 163: Trailing whitespace
- Line 167: Trailing whitespace
- Line 173: Trailing whitespace
- Line 190: Trailing whitespace
- Line 193: Trailing whitespace
- Line 200: Trailing whitespace
- Line 207: Trailing whitespace
- Line 217: Trailing whitespace
- Line 219: Trailing whitespace
- Line 226: Trailing whitespace
- Line 234: Trailing whitespace
- Line 240: Trailing whitespace
- Line 247: Trailing whitespace
- Line 251: Trailing whitespace
- Line 254: Trailing whitespace
- Line 261: Trailing whitespace
- Line 264: Trailing whitespace
- Line 267: Trailing whitespace
- Line 274: Trailing whitespace
- Line 277: Trailing whitespace
- Line 280: Trailing whitespace
- Line 287: Trailing whitespace
- Line 290: Trailing whitespace
- Line 293: Trailing whitespace
- Line 300: Trailing whitespace
- Line 303: Trailing whitespace
- Line 310: Trailing whitespace
- Line 336: Trailing whitespace
- Line 339: Trailing whitespace
- Line 344: Trailing whitespace
- Line 346: Trailing whitespace
- Line 350: Trailing whitespace
- Line 356: Trailing whitespace
- Line 367: Trailing whitespace
- Line 370: Trailing whitespace
- Line 376: Trailing whitespace
- Line 380: Trailing whitespace
- Line 384: Trailing whitespace
- Line 396: Trailing whitespace
- Line 404: Trailing whitespace
- Line 410: Trailing whitespace
- Line 417: Trailing whitespace
- Line 430: Trailing whitespace
- Line 436: Trailing whitespace
- Line 437: Trailing whitespace
- Line 443: Trailing whitespace
- Line 453: Trailing whitespace
- Line 456: Trailing whitespace
- Line 459: Trailing whitespace
- Line 465: Trailing whitespace
- Line 468: Trailing whitespace

### tests/test_gpsd_client.py
- Line 8: E501 line too long (86 > 79 characters)
- Line 32: E501 line too long (85 > 79 characters)
- Line 41: E501 line too long (81 > 79 characters)

### src/piwardrive/advanced_localization.py
- Line 72: E501 line too long (81 > 79 characters)
- Line 82: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 113: W293 blank line contains whitespace
- Line 121: E501 line too long (88 > 79 characters)
- Line 140: W293 blank line contains whitespace
- Line 142: W291 trailing whitespace
- Line 145: W293 blank line contains whitespace
- Line 157: E501 line too long (82 > 79 characters)
- Line 159: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 82: Trailing whitespace
- Line 86: Trailing whitespace
- Line 109: Trailing whitespace
- Line 113: Trailing whitespace
- Line 140: Trailing whitespace
- Line 142: Trailing whitespace
- Line 145: Trailing whitespace
- Line 159: Trailing whitespace
- Line 164: Trailing whitespace

### scripts/migrate_sqlite_to_postgres.py
- Line 26: E501 line too long (80 > 79 characters)
- Line 37: E501 line too long (87 > 79 characters)
- Line 44: E501 line too long (83 > 79 characters)

### src/piwardrive/services/maintenance.py
- Line 21: E501 line too long (86 > 79 characters)
- Line 53: E501 line too long (88 > 79 characters)
- Line 56: E501 line too long (82 > 79 characters)
- Line 67: E501 line too long (81 > 79 characters)
- Line 90: E501 line too long (88 > 79 characters)

### main.py
- Line 4: E501 line too long (88 > 79 characters)
- Line 68: E501 line too long (83 > 79 characters)
- Line 72: E501 line too long (80 > 79 characters)
- Line 82: E501 line too long (81 > 79 characters)
- Line 177: E501 line too long (88 > 79 characters)
- Line 183: E501 line too long (87 > 79 characters)
- Line 187: E501 line too long (87 > 79 characters)

### tests/test_service_async_endpoints.py
- Line 55: E501 line too long (82 > 79 characters)
- Line 64: E501 line too long (85 > 79 characters)

### src/piwardrive/sync.py
- Line 33: E501 line too long (84 > 79 characters)

### src/piwardrive/web/webui_server.py
- Line 25: E501 line too long (81 > 79 characters)
- Line 28: E501 line too long (83 > 79 characters)

### tests/logging/test_structured_logger.py
- Line 12: W291 trailing whitespace
- Line 19: W293 blank line contains whitespace
- Line 22: E501 line too long (89 > 79 characters)
- Line 24: W293 blank line contains whitespace
- Line 28: E501 line too long (101 > 79 characters)
- Line 34: W293 blank line contains whitespace
- Line 46: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 87: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 103: W291 trailing whitespace
- Line 104: W291 trailing whitespace
- Line 108: W293 blank line contains whitespace
- Line 116: W293 blank line contains whitespace
- Line 120: E501 line too long (80 > 79 characters)
- Line 121: W293 blank line contains whitespace
- Line 130: W293 blank line contains whitespace
- Line 134: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 145: W293 blank line contains whitespace
- Line 153: W293 blank line contains whitespace
- Line 157: E501 line too long (104 > 79 characters)
- Line 162: W293 blank line contains whitespace
- Line 165: E501 line too long (104 > 79 characters)
- Line 166: E501 line too long (81 > 79 characters)
- Line 169: W293 blank line contains whitespace
- Line 173: W291 trailing whitespace
- Line 174: W291 trailing whitespace
- Line 175: W291 trailing whitespace
- Line 176: W291 trailing whitespace
- Line 177: W291 trailing whitespace
- Line 178: W291 trailing whitespace
- Line 182: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 212: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 222: W293 blank line contains whitespace
- Line 229: E501 line too long (80 > 79 characters)
- Line 230: W293 blank line contains whitespace
- Line 233: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 249: W293 blank line contains whitespace
- Line 251: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 265: W293 blank line contains whitespace
- Line 271: E501 line too long (81 > 79 characters)
- Line 272: W293 blank line contains whitespace
- Line 277: E501 line too long (81 > 79 characters)
- Line 279: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 304: W293 blank line contains whitespace
- Line 310: W293 blank line contains whitespace
- Line 314: W293 blank line contains whitespace
- Line 320: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 331: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 338: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 350: W293 blank line contains whitespace
- Line 353: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 373: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 385: W293 blank line contains whitespace
- Line 392: W293 blank line contains whitespace
- Line 394: W293 blank line contains whitespace
- Line 397: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 408: W293 blank line contains whitespace
- Line 415: W293 blank line contains whitespace
- Line 420: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 432: W293 blank line contains whitespace
- Line 439: W293 blank line contains whitespace
- Line 443: W293 blank line contains whitespace
- Line 447: W293 blank line contains whitespace
- Line 453: W293 blank line contains whitespace
- Line 458: W293 blank line contains whitespace
- Line 463: W293 blank line contains whitespace
- Line 469: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 484: W293 blank line contains whitespace
- Line 487: W293 blank line contains whitespace
- Line 492: W293 blank line contains whitespace
- Line 496: W293 blank line contains whitespace
- Line 500: W293 blank line contains whitespace
- Line 504: W293 blank line contains whitespace
- Line 514: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 525: W293 blank line contains whitespace
- Line 531: W293 blank line contains whitespace
- Line 535: W293 blank line contains whitespace
- Line 541: E501 line too long (91 > 79 characters)
- Line 546: W293 blank line contains whitespace
- Line 551: W293 blank line contains whitespace
- Line 554: W293 blank line contains whitespace
- Line 558: W293 blank line contains whitespace
- Line 563: W293 blank line contains whitespace
- Line 568: W293 blank line contains whitespace
- Line 570: W293 blank line contains whitespace
- Line 574: W293 blank line contains whitespace
- Line 577: W293 blank line contains whitespace
- Line 582: W293 blank line contains whitespace
- Line 592: W293 blank line contains whitespace
- Line 599: W293 blank line contains whitespace
- Line 602: W293 blank line contains whitespace
- Line 607: W293 blank line contains whitespace
- Line 612: W293 blank line contains whitespace
- Line 615: W293 blank line contains whitespace
- Line 619: W293 blank line contains whitespace
- Line 623: W293 blank line contains whitespace
- Line 630: W293 blank line contains whitespace
- Line 636: W293 blank line contains whitespace
- Line 639: W293 blank line contains whitespace
- Line 643: W293 blank line contains whitespace
- Line 647: W293 blank line contains whitespace
- Line 652: W293 blank line contains whitespace
- Line 655: W293 blank line contains whitespace
- Line 662: W293 blank line contains whitespace
- Line 666: W293 blank line contains whitespace
- Line 669: W293 blank line contains whitespace
- Line 676: W293 blank line contains whitespace
- Line 680: W293 blank line contains whitespace
- Line 682: E501 line too long (107 > 79 characters)
- Line 686: W293 blank line contains whitespace
- Line 691: W293 blank line contains whitespace
- Line 699: W293 blank line contains whitespace
- Line 702: E501 line too long (87 > 79 characters)
- Line 703: W293 blank line contains whitespace
- Line 706: W293 blank line contains whitespace
- Line 710: W293 blank line contains whitespace
- Line 715: W293 blank line contains whitespace
- Line 721: W293 blank line contains whitespace
- Line 724: W293 blank line contains whitespace
- Line 727: W293 blank line contains whitespace
- Line 730: W293 blank line contains whitespace
- Line 734: W293 blank line contains whitespace
- Line 740: W293 blank line contains whitespace
- Line 743: W293 blank line contains whitespace
- Line 752: W293 blank line contains whitespace
- Line 762: W293 blank line contains whitespace
- Line 764: E501 line too long (91 > 79 characters)
- Line 766: W293 blank line contains whitespace
- Line 772: E501 line too long (81 > 79 characters)
- Line 775: W293 blank line contains whitespace
- Line 780: W293 blank line contains whitespace
- Line 785: W293 blank line contains whitespace
- Line 788: W293 blank line contains whitespace
- Line 792: W293 blank line contains whitespace
- Line 799: W293 blank line contains whitespace
- Line 801: W293 blank line contains whitespace
- Line 804: W293 blank line contains whitespace
- Line 814: W293 blank line contains whitespace
- Line 819: W293 blank line contains whitespace
- Line 824: W293 blank line contains whitespace
- Line 829: W293 blank line contains whitespace
- Line 834: W293 blank line contains whitespace
- Line 841: W293 blank line contains whitespace
- Line 845: W293 blank line contains whitespace
- Line 848: E501 line too long (81 > 79 characters)
- Line 850: W293 blank line contains whitespace
- Line 12: Trailing whitespace
- Line 19: Trailing whitespace
- Line 24: Trailing whitespace
- Line 34: Trailing whitespace
- Line 46: Trailing whitespace
- Line 62: Trailing whitespace
- Line 87: Trailing whitespace
- Line 92: Trailing whitespace
- Line 98: Trailing whitespace
- Line 103: Trailing whitespace
- Line 104: Trailing whitespace
- Line 108: Trailing whitespace
- Line 116: Trailing whitespace
- Line 121: Trailing whitespace
- Line 130: Trailing whitespace
- Line 134: Trailing whitespace
- Line 140: Trailing whitespace
- Line 145: Trailing whitespace
- Line 153: Trailing whitespace
- Line 162: Trailing whitespace
- Line 169: Trailing whitespace
- Line 173: Trailing whitespace
- Line 174: Trailing whitespace
- Line 175: Trailing whitespace
- Line 176: Trailing whitespace
- Line 177: Trailing whitespace
- Line 178: Trailing whitespace
- Line 182: Trailing whitespace
- Line 185: Trailing whitespace
- Line 192: Trailing whitespace
- Line 199: Trailing whitespace
- Line 206: Trailing whitespace
- Line 212: Trailing whitespace
- Line 215: Trailing whitespace
- Line 222: Trailing whitespace
- Line 230: Trailing whitespace
- Line 233: Trailing whitespace
- Line 237: Trailing whitespace
- Line 246: Trailing whitespace
- Line 249: Trailing whitespace
- Line 251: Trailing whitespace
- Line 262: Trailing whitespace
- Line 265: Trailing whitespace
- Line 272: Trailing whitespace
- Line 279: Trailing whitespace
- Line 282: Trailing whitespace
- Line 290: Trailing whitespace
- Line 297: Trailing whitespace
- Line 304: Trailing whitespace
- Line 310: Trailing whitespace
- Line 314: Trailing whitespace
- Line 320: Trailing whitespace
- Line 324: Trailing whitespace
- Line 331: Trailing whitespace
- Line 335: Trailing whitespace
- Line 338: Trailing whitespace
- Line 345: Trailing whitespace
- Line 350: Trailing whitespace
- Line 353: Trailing whitespace
- Line 357: Trailing whitespace
- Line 364: Trailing whitespace
- Line 369: Trailing whitespace
- Line 373: Trailing whitespace
- Line 380: Trailing whitespace
- Line 385: Trailing whitespace
- Line 392: Trailing whitespace
- Line 394: Trailing whitespace
- Line 397: Trailing whitespace
- Line 403: Trailing whitespace
- Line 408: Trailing whitespace
- Line 415: Trailing whitespace
- Line 420: Trailing whitespace
- Line 424: Trailing whitespace
- Line 432: Trailing whitespace
- Line 439: Trailing whitespace
- Line 443: Trailing whitespace
- Line 447: Trailing whitespace
- Line 453: Trailing whitespace
- Line 458: Trailing whitespace
- Line 463: Trailing whitespace
- Line 469: Trailing whitespace
- Line 479: Trailing whitespace
- Line 484: Trailing whitespace
- Line 487: Trailing whitespace
- Line 492: Trailing whitespace
- Line 496: Trailing whitespace
- Line 500: Trailing whitespace
- Line 504: Trailing whitespace
- Line 514: Trailing whitespace
- Line 518: Trailing whitespace
- Line 525: Trailing whitespace
- Line 531: Trailing whitespace
- Line 535: Trailing whitespace
- Line 546: Trailing whitespace
- Line 551: Trailing whitespace
- Line 554: Trailing whitespace
- Line 558: Trailing whitespace
- Line 563: Trailing whitespace
- Line 568: Trailing whitespace
- Line 570: Trailing whitespace
- Line 574: Trailing whitespace
- Line 577: Trailing whitespace
- Line 582: Trailing whitespace
- Line 592: Trailing whitespace
- Line 599: Trailing whitespace
- Line 602: Trailing whitespace
- Line 607: Trailing whitespace
- Line 612: Trailing whitespace
- Line 615: Trailing whitespace
- Line 619: Trailing whitespace
- Line 623: Trailing whitespace
- Line 630: Trailing whitespace
- Line 636: Trailing whitespace
- Line 639: Trailing whitespace
- Line 643: Trailing whitespace
- Line 647: Trailing whitespace
- Line 652: Trailing whitespace
- Line 655: Trailing whitespace
- Line 662: Trailing whitespace
- Line 666: Trailing whitespace
- Line 669: Trailing whitespace
- Line 676: Trailing whitespace
- Line 680: Trailing whitespace
- Line 686: Trailing whitespace
- Line 691: Trailing whitespace
- Line 699: Trailing whitespace
- Line 703: Trailing whitespace
- Line 706: Trailing whitespace
- Line 710: Trailing whitespace
- Line 715: Trailing whitespace
- Line 721: Trailing whitespace
- Line 724: Trailing whitespace
- Line 727: Trailing whitespace
- Line 730: Trailing whitespace
- Line 734: Trailing whitespace
- Line 740: Trailing whitespace
- Line 743: Trailing whitespace
- Line 752: Trailing whitespace
- Line 762: Trailing whitespace
- Line 766: Trailing whitespace
- Line 775: Trailing whitespace
- Line 780: Trailing whitespace
- Line 785: Trailing whitespace
- Line 788: Trailing whitespace
- Line 792: Trailing whitespace
- Line 799: Trailing whitespace
- Line 801: Trailing whitespace
- Line 804: Trailing whitespace
- Line 814: Trailing whitespace
- Line 819: Trailing whitespace
- Line 824: Trailing whitespace
- Line 829: Trailing whitespace
- Line 834: Trailing whitespace
- Line 841: Trailing whitespace
- Line 845: Trailing whitespace
- Line 850: Trailing whitespace

### fix_undefined.py
- Line 17: E501 line too long (103 > 79 characters)
- Line 20: E501 line too long (89 > 79 characters)
- Line 61: E501 line too long (96 > 79 characters)

### scripts/kiosk.py
- Line 8: E501 line too long (80 > 79 characters)

### tests/test_api_service.py
- Line 24: E501 line too long (99 > 79 characters)
- Line 25: E501 line too long (87 > 79 characters)
- Line 38: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 50: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 56: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 66: W293 blank line contains whitespace
- Line 75: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 97: W293 blank line contains whitespace
- Line 98: E501 line too long (85 > 79 characters)
- Line 102: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 116: W293 blank line contains whitespace
- Line 117: E501 line too long (85 > 79 characters)
- Line 120: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 153: E501 line too long (87 > 79 characters)
- Line 156: W293 blank line contains whitespace
- Line 158: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 208: E501 line too long (84 > 79 characters)
- Line 211: W293 blank line contains whitespace
- Line 213: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 227: W293 blank line contains whitespace
- Line 228: E501 line too long (83 > 79 characters)
- Line 231: W293 blank line contains whitespace
- Line 233: W293 blank line contains whitespace
- Line 238: W293 blank line contains whitespace
- Line 247: W293 blank line contains whitespace
- Line 248: E501 line too long (82 > 79 characters)
- Line 251: W293 blank line contains whitespace
- Line 253: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 271: E501 line too long (88 > 79 characters)
- Line 274: W293 blank line contains whitespace
- Line 276: W293 blank line contains whitespace
- Line 285: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 307: E501 line too long (86 > 79 characters)
- Line 310: W293 blank line contains whitespace
- Line 312: W293 blank line contains whitespace
- Line 318: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 346: E501 line too long (90 > 79 characters)
- Line 349: W293 blank line contains whitespace
- Line 351: W293 blank line contains whitespace
- Line 360: W293 blank line contains whitespace
- Line 366: W293 blank line contains whitespace
- Line 378: W293 blank line contains whitespace
- Line 379: E501 line too long (85 > 79 characters)
- Line 382: W293 blank line contains whitespace
- Line 384: W293 blank line contains whitespace
- Line 389: W293 blank line contains whitespace
- Line 397: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 407: E501 line too long (96 > 79 characters)
- Line 409: E501 line too long (80 > 79 characters)
- Line 410: W293 blank line contains whitespace
- Line 412: W293 blank line contains whitespace
- Line 417: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 429: E501 line too long (95 > 79 characters)
- Line 431: E501 line too long (81 > 79 characters)
- Line 432: W293 blank line contains whitespace
- Line 434: W293 blank line contains whitespace
- Line 443: W293 blank line contains whitespace
- Line 449: W293 blank line contains whitespace
- Line 454: W293 blank line contains whitespace
- Line 457: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 462: W293 blank line contains whitespace
- Line 486: W293 blank line contains whitespace
- Line 487: E501 line too long (89 > 79 characters)
- Line 490: W293 blank line contains whitespace
- Line 492: W293 blank line contains whitespace
- Line 497: W293 blank line contains whitespace
- Line 502: W293 blank line contains whitespace
- Line 504: E501 line too long (90 > 79 characters)
- Line 505: W293 blank line contains whitespace
- Line 507: W293 blank line contains whitespace
- Line 514: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 519: E501 line too long (80 > 79 characters)
- Line 520: E501 line too long (80 > 79 characters)
- Line 526: W293 blank line contains whitespace
- Line 531: W293 blank line contains whitespace
- Line 537: W293 blank line contains whitespace
- Line 540: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 548: W293 blank line contains whitespace
- Line 549: E501 line too long (80 > 79 characters)
- Line 559: W293 blank line contains whitespace
- Line 563: W293 blank line contains whitespace
- Line 569: W293 blank line contains whitespace
- Line 572: W293 blank line contains whitespace
- Line 580: W293 blank line contains whitespace
- Line 586: W293 blank line contains whitespace
- Line 593: W293 blank line contains whitespace
- Line 599: W293 blank line contains whitespace
- Line 602: W293 blank line contains whitespace
- Line 604: E501 line too long (81 > 79 characters)
- Line 605: W293 blank line contains whitespace
- Line 607: W293 blank line contains whitespace
- Line 612: W293 blank line contains whitespace
- Line 616: W293 blank line contains whitespace
- Line 619: W293 blank line contains whitespace
- Line 621: E501 line too long (90 > 79 characters)
- Line 622: W293 blank line contains whitespace
- Line 624: W293 blank line contains whitespace
- Line 626: W293 blank line contains whitespace
- Line 630: E501 line too long (88 > 79 characters)
- Line 631: W293 blank line contains whitespace
- Line 633: W293 blank line contains whitespace
- Line 636: W293 blank line contains whitespace
- Line 640: W293 blank line contains whitespace
- Line 643: W293 blank line contains whitespace
- Line 645: E501 line too long (88 > 79 characters)
- Line 646: W293 blank line contains whitespace
- Line 648: W293 blank line contains whitespace
- Line 654: W293 blank line contains whitespace
- Line 660: W293 blank line contains whitespace
- Line 665: W293 blank line contains whitespace
- Line 670: W293 blank line contains whitespace
- Line 672: W293 blank line contains whitespace
- Line 674: W293 blank line contains whitespace
- Line 681: W293 blank line contains whitespace
- Line 683: W293 blank line contains whitespace
- Line 685: W293 blank line contains whitespace
- Line 692: W293 blank line contains whitespace
- Line 703: W293 blank line contains whitespace
- Line 705: W293 blank line contains whitespace
- Line 707: W293 blank line contains whitespace
- Line 712: W293 blank line contains whitespace
- Line 717: W293 blank line contains whitespace
- Line 719: W293 blank line contains whitespace
- Line 725: W293 blank line contains whitespace
- Line 731: W293 blank line contains whitespace
- Line 736: W293 blank line contains whitespace
- Line 739: E501 line too long (82 > 79 characters)
- Line 741: W293 blank line contains whitespace
- Line 743: W293 blank line contains whitespace
- Line 747: W293 blank line contains whitespace
- Line 751: W293 blank line contains whitespace
- Line 755: E501 line too long (87 > 79 characters)
- Line 761: W293 blank line contains whitespace
- Line 762: E501 line too long (89 > 79 characters)
- Line 765: W293 blank line contains whitespace
- Line 767: W293 blank line contains whitespace
- Line 773: W293 blank line contains whitespace
- Line 782: W293 blank line contains whitespace
- Line 783: E501 line too long (80 > 79 characters)
- Line 787: W293 blank line contains whitespace
- Line 789: W293 blank line contains whitespace
- Line 796: W293 blank line contains whitespace
- Line 802: W293 blank line contains whitespace
- Line 809: W293 blank line contains whitespace
- Line 812: W293 blank line contains whitespace
- Line 814: E501 line too long (91 > 79 characters)
- Line 817: W293 blank line contains whitespace
- Line 821: W293 blank line contains whitespace
- Line 823: E501 line too long (80 > 79 characters)
- Line 825: W293 blank line contains whitespace
- Line 829: W293 blank line contains whitespace
- Line 833: W293 blank line contains whitespace
- Line 837: W293 blank line contains whitespace
- Line 842: W293 blank line contains whitespace
- Line 843: E501 line too long (80 > 79 characters)
- Line 847: W293 blank line contains whitespace
- Line 854: W293 blank line contains whitespace
- Line 859: W293 blank line contains whitespace
- Line 862: W293 blank line contains whitespace
- Line 38: Trailing whitespace
- Line 43: Trailing whitespace
- Line 50: Trailing whitespace
- Line 52: Trailing whitespace
- Line 56: Trailing whitespace
- Line 62: Trailing whitespace
- Line 66: Trailing whitespace
- Line 75: Trailing whitespace
- Line 81: Trailing whitespace
- Line 97: Trailing whitespace
- Line 102: Trailing whitespace
- Line 104: Trailing whitespace
- Line 107: Trailing whitespace
- Line 116: Trailing whitespace
- Line 120: Trailing whitespace
- Line 122: Trailing whitespace
- Line 125: Trailing whitespace
- Line 152: Trailing whitespace
- Line 156: Trailing whitespace
- Line 158: Trailing whitespace
- Line 167: Trailing whitespace
- Line 173: Trailing whitespace
- Line 207: Trailing whitespace
- Line 211: Trailing whitespace
- Line 213: Trailing whitespace
- Line 219: Trailing whitespace
- Line 227: Trailing whitespace
- Line 231: Trailing whitespace
- Line 233: Trailing whitespace
- Line 238: Trailing whitespace
- Line 247: Trailing whitespace
- Line 251: Trailing whitespace
- Line 253: Trailing whitespace
- Line 258: Trailing whitespace
- Line 270: Trailing whitespace
- Line 274: Trailing whitespace
- Line 276: Trailing whitespace
- Line 285: Trailing whitespace
- Line 291: Trailing whitespace
- Line 306: Trailing whitespace
- Line 310: Trailing whitespace
- Line 312: Trailing whitespace
- Line 318: Trailing whitespace
- Line 345: Trailing whitespace
- Line 349: Trailing whitespace
- Line 351: Trailing whitespace
- Line 360: Trailing whitespace
- Line 366: Trailing whitespace
- Line 378: Trailing whitespace
- Line 382: Trailing whitespace
- Line 384: Trailing whitespace
- Line 389: Trailing whitespace
- Line 397: Trailing whitespace
- Line 406: Trailing whitespace
- Line 410: Trailing whitespace
- Line 412: Trailing whitespace
- Line 417: Trailing whitespace
- Line 428: Trailing whitespace
- Line 432: Trailing whitespace
- Line 434: Trailing whitespace
- Line 443: Trailing whitespace
- Line 449: Trailing whitespace
- Line 454: Trailing whitespace
- Line 457: Trailing whitespace
- Line 459: Trailing whitespace
- Line 462: Trailing whitespace
- Line 486: Trailing whitespace
- Line 490: Trailing whitespace
- Line 492: Trailing whitespace
- Line 497: Trailing whitespace
- Line 502: Trailing whitespace
- Line 505: Trailing whitespace
- Line 507: Trailing whitespace
- Line 514: Trailing whitespace
- Line 518: Trailing whitespace
- Line 526: Trailing whitespace
- Line 531: Trailing whitespace
- Line 537: Trailing whitespace
- Line 540: Trailing whitespace
- Line 544: Trailing whitespace
- Line 548: Trailing whitespace
- Line 559: Trailing whitespace
- Line 563: Trailing whitespace
- Line 569: Trailing whitespace
- Line 572: Trailing whitespace
- Line 580: Trailing whitespace
- Line 586: Trailing whitespace
- Line 593: Trailing whitespace
- Line 599: Trailing whitespace
- Line 602: Trailing whitespace
- Line 605: Trailing whitespace
- Line 607: Trailing whitespace
- Line 612: Trailing whitespace
- Line 616: Trailing whitespace
- Line 619: Trailing whitespace
- Line 622: Trailing whitespace
- Line 624: Trailing whitespace
- Line 626: Trailing whitespace
- Line 631: Trailing whitespace
- Line 633: Trailing whitespace
- Line 636: Trailing whitespace
- Line 640: Trailing whitespace
- Line 643: Trailing whitespace
- Line 646: Trailing whitespace
- Line 648: Trailing whitespace
- Line 654: Trailing whitespace
- Line 660: Trailing whitespace
- Line 665: Trailing whitespace
- Line 670: Trailing whitespace
- Line 672: Trailing whitespace
- Line 674: Trailing whitespace
- Line 681: Trailing whitespace
- Line 683: Trailing whitespace
- Line 685: Trailing whitespace
- Line 692: Trailing whitespace
- Line 703: Trailing whitespace
- Line 705: Trailing whitespace
- Line 707: Trailing whitespace
- Line 712: Trailing whitespace
- Line 717: Trailing whitespace
- Line 719: Trailing whitespace
- Line 725: Trailing whitespace
- Line 731: Trailing whitespace
- Line 736: Trailing whitespace
- Line 741: Trailing whitespace
- Line 743: Trailing whitespace
- Line 747: Trailing whitespace
- Line 751: Trailing whitespace
- Line 761: Trailing whitespace
- Line 765: Trailing whitespace
- Line 767: Trailing whitespace
- Line 773: Trailing whitespace
- Line 782: Trailing whitespace
- Line 787: Trailing whitespace
- Line 789: Trailing whitespace
- Line 796: Trailing whitespace
- Line 802: Trailing whitespace
- Line 809: Trailing whitespace
- Line 812: Trailing whitespace
- Line 817: Trailing whitespace
- Line 821: Trailing whitespace
- Line 825: Trailing whitespace
- Line 829: Trailing whitespace
- Line 833: Trailing whitespace
- Line 837: Trailing whitespace
- Line 842: Trailing whitespace
- Line 847: Trailing whitespace
- Line 854: Trailing whitespace
- Line 859: Trailing whitespace
- Line 862: Trailing whitespace

### tests/test_service_layer.py
- Line 16: E402 module level import not at top of file
- Line 16: E501 line too long (91 > 79 characters)
- Line 17: E402 module level import not at top of file
- Line 59: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 141: W293 blank line contains whitespace
- Line 170: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 193: W293 blank line contains whitespace
- Line 203: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 235: W293 blank line contains whitespace
- Line 266: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 309: E501 line too long (80 > 79 characters)
- Line 317: W293 blank line contains whitespace
- Line 319: E501 line too long (80 > 79 characters)
- Line 336: W293 blank line contains whitespace
- Line 346: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 366: W293 blank line contains whitespace
- Line 385: W293 blank line contains whitespace
- Line 392: E501 line too long (82 > 79 characters)
- Line 405: W293 blank line contains whitespace
- Line 59: Trailing whitespace
- Line 84: Trailing whitespace
- Line 100: Trailing whitespace
- Line 114: Trailing whitespace
- Line 141: Trailing whitespace
- Line 170: Trailing whitespace
- Line 183: Trailing whitespace
- Line 193: Trailing whitespace
- Line 203: Trailing whitespace
- Line 214: Trailing whitespace
- Line 225: Trailing whitespace
- Line 235: Trailing whitespace
- Line 266: Trailing whitespace
- Line 281: Trailing whitespace
- Line 297: Trailing whitespace
- Line 307: Trailing whitespace
- Line 317: Trailing whitespace
- Line 336: Trailing whitespace
- Line 346: Trailing whitespace
- Line 356: Trailing whitespace
- Line 366: Trailing whitespace
- Line 385: Trailing whitespace
- Line 405: Trailing whitespace

### src/piwardrive/sigint_suite/cellular/imsi_catcher/__init__.py
- Line 1: E501 line too long (84 > 79 characters)

### src/piwardrive/error_reporting.py
- Line 56: E501 line too long (88 > 79 characters)

### src/piwardrive/logging/rotation.py
- Line 26: E501 line too long (84 > 79 characters)
- Line 71: E501 line too long (82 > 79 characters)
- Line 84: E501 line too long (88 > 79 characters)
- Line 108: E501 line too long (80 > 79 characters)
- Line 229: W503 line break before binary operator
- Line 230: W503 line break before binary operator
- Line 236: E501 line too long (81 > 79 characters)
- Line 242: E501 line too long (82 > 79 characters)
- Line 244: E203 whitespace before ':'

### src/piwardrive/direction_finding/core.py
- Line 105: E501 line too long (83 > 79 characters)
- Line 151: E501 line too long (84 > 79 characters)
- Line 184: E501 line too long (86 > 79 characters)
- Line 260: E501 line too long (80 > 79 characters)
- Line 282: E501 line too long (88 > 79 characters)
- Line 288: E501 line too long (87 > 79 characters)
- Line 292: E501 line too long (88 > 79 characters)
- Line 300: E501 line too long (82 > 79 characters)
- Line 323: E501 line too long (85 > 79 characters)
- Line 327: E501 line too long (81 > 79 characters)
- Line 367: W503 line break before binary operator
- Line 368: E501 line too long (85 > 79 characters)
- Line 380: W503 line break before binary operator
- Line 381: E501 line too long (81 > 79 characters)
- Line 424: E501 line too long (81 > 79 characters)

### tests/test_tile_maintenance.py
- Line 13: E501 line too long (82 > 79 characters)
- Line 74: E501 line too long (84 > 79 characters)

### src/piwardrive/db/postgres.py
- Line 80: E501 line too long (83 > 79 characters)
- Line 89: E501 line too long (88 > 79 characters)

### tests/test_utils.py
- Line 29: E402 module level import not at top of file
- Line 35: E402 module level import not at top of file
- Line 37: E402 module level import not at top of file
- Line 116: E501 line too long (83 > 79 characters)
- Line 132: E501 line too long (80 > 79 characters)
- Line 186: E501 line too long (81 > 79 characters)
- Line 207: E501 line too long (85 > 79 characters)
- Line 227: E501 line too long (80 > 79 characters)
- Line 270: E501 line too long (109 > 79 characters)
- Line 271: E501 line too long (93 > 79 characters)
- Line 285: E501 line too long (93 > 79 characters)
- Line 306: E501 line too long (86 > 79 characters)
- Line 337: E501 line too long (86 > 79 characters)
- Line 395: E501 line too long (86 > 79 characters)
- Line 424: E501 line too long (86 > 79 characters)
- Line 464: E501 line too long (86 > 79 characters)
- Line 497: E501 line too long (86 > 79 characters)
- Line 520: E128 continuation line under-indented for visual indent
- Line 521: E128 continuation line under-indented for visual indent
- Line 521: E125 continuation line with same indent as next logical line
- Line 571: E501 line too long (80 > 79 characters)
- Line 578: E501 line too long (86 > 79 characters)
- Line 717: E501 line too long (83 > 79 characters)
- Line 786: E501 line too long (84 > 79 characters)
- Line 826: E501 line too long (81 > 79 characters)
- Line 832: E501 line too long (81 > 79 characters)
- Line 860: E501 line too long (80 > 79 characters)
- Line 862: E501 line too long (82 > 79 characters)
- Line 896: E501 line too long (81 > 79 characters)
- Line 926: E501 line too long (82 > 79 characters)
- Line 929: E501 line too long (80 > 79 characters)
- Line 954: E501 line too long (89 > 79 characters)
- Line 982: E501 line too long (87 > 79 characters)
- Line 1000: E501 line too long (97 > 79 characters)

### src/piwardrive/localization.py
- Line 39: E305 expected 2 blank lines after class or function definition, found 0

### src/piwardrive/integrations/sigint_suite/rf/spectrum.py
- Line 18: E501 line too long (84 > 79 characters)
- Line 33: E501 line too long (86 > 79 characters)

### src/piwardrive/task_queue.py
- Line 19: W293 blank line contains whitespace
- Line 23: E501 line too long (82 > 79 characters)
- Line 66: W293 blank line contains whitespace
- Line 70: E501 line too long (88 > 79 characters)
- Line 105: E501 line too long (85 > 79 characters)
- Line 107: W293 blank line contains whitespace
- Line 19: Trailing whitespace
- Line 66: Trailing whitespace
- Line 107: Trailing whitespace

### src/piwardrive/migrations/005_create_cellular_detections.py
- Line 63: E501 line too long (83 > 79 characters)
- Line 66: E501 line too long (82 > 79 characters)

### scripts/test_database_functions.py
- Line 41: E302 expected 2 blank lines, found 1
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E501 line too long (449 > 79 characters)
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 48: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E501 line too long (618 > 79 characters)
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E231 missing whitespace after ','
- Line 61: E226 missing whitespace around arithmetic operator
- Line 61: E231 missing whitespace after ','
- Line 66: E231 missing whitespace after ','
- Line 66: E501 line too long (186 > 79 characters)
- Line 66: E231 missing whitespace after ','
- Line 66: E231 missing whitespace after ','
- Line 67: E231 missing whitespace after ','
- Line 67: E231 missing whitespace after ','
- Line 67: E231 missing whitespace after ','
- Line 67: E501 line too long (121 > 79 characters)
- Line 68: E231 missing whitespace after ','
- Line 68: E231 missing whitespace after ','
- Line 68: E501 line too long (193 > 79 characters)
- Line 68: E231 missing whitespace after ','
- Line 68: E231 missing whitespace after ','
- Line 73: E231 missing whitespace after ','
- Line 73: E501 line too long (164 > 79 characters)
- Line 73: E231 missing whitespace after ','
- Line 73: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E501 line too long (285 > 79 characters)
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E501 line too long (443 > 79 characters)
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 83: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 94: E501 line too long (264 > 79 characters)
- Line 94: E226 missing whitespace around arithmetic operator
- Line 94: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 94: E231 missing whitespace after ','
- Line 103: E231 missing whitespace after ','
- Line 103: E231 missing whitespace after ','
- Line 103: E501 line too long (203 > 79 characters)
- Line 103: E231 missing whitespace after ','
- Line 103: E231 missing whitespace after ','
- Line 103: E231 missing whitespace after ','
- Line 103: E231 missing whitespace after ','
- Line 112: E302 expected 2 blank lines, found 1
- Line 133: E501 line too long (132 > 79 characters)
- Line 137: E302 expected 2 blank lines, found 1
- Line 154: E302 expected 2 blank lines, found 1
- Line 179: E501 line too long (84 > 79 characters)
- Line 48: Line too long (449 > 120 characters)
- Line 61: Line too long (618 > 120 characters)
- Line 66: Line too long (186 > 120 characters)
- Line 67: Line too long (121 > 120 characters)
- Line 68: Line too long (193 > 120 characters)
- Line 73: Line too long (164 > 120 characters)
- Line 74: Line too long (285 > 120 characters)
- Line 83: Line too long (443 > 120 characters)
- Line 94: Line too long (264 > 120 characters)
- Line 103: Line too long (203 > 120 characters)
- Line 133: Line too long (132 > 120 characters)

### src/piwardrive/web_server.py
- Line 28: E501 line too long (81 > 79 characters)
- Line 31: E501 line too long (83 > 79 characters)

### tests/test_sync.py
- Line 11: E402 module level import not at top of file
- Line 49: E501 line too long (81 > 79 characters)
- Line 87: E501 line too long (81 > 79 characters)

### src/piwardrive/navigation/offline_navigation.py
- Line 50: E302 expected 2 blank lines, found 1
- Line 65: E501 line too long (87 > 79 characters)
- Line 80: E302 expected 2 blank lines, found 1
- Line 104: E302 expected 2 blank lines, found 1
- Line 137: E302 expected 2 blank lines, found 1
- Line 156: E501 line too long (85 > 79 characters)
- Line 164: E501 line too long (86 > 79 characters)
- Line 296: E501 line too long (85 > 79 characters)
- Line 330: E501 line too long (82 > 79 characters)
- Line 429: E501 line too long (85 > 79 characters)
- Line 434: E501 line too long (80 > 79 characters)
- Line 437: E501 line too long (80 > 79 characters)
- Line 478: E501 line too long (84 > 79 characters)
- Line 554: E501 line too long (86 > 79 characters)
- Line 564: E303 too many blank lines (3)
- Line 604: E501 line too long (84 > 79 characters)
- Line 606: E501 line too long (81 > 79 characters)
- Line 612: E501 line too long (86 > 79 characters)
- Line 618: W503 line break before binary operator
- Line 625: E501 line too long (85 > 79 characters)
- Line 638: E501 line too long (82 > 79 characters)
- Line 673: E501 line too long (81 > 79 characters)
- Line 695: E501 line too long (86 > 79 characters)
- Line 730: E501 line too long (84 > 79 characters)
- Line 759: E501 line too long (80 > 79 characters)
- Line 846: E501 line too long (85 > 79 characters)
- Line 887: E501 line too long (80 > 79 characters)
- Line 888: E501 line too long (80 > 79 characters)
- Line 889: E501 line too long (80 > 79 characters)
- Line 903: E501 line too long (85 > 79 characters)
- Line 953: E501 line too long (87 > 79 characters)
- Line 961: E501 line too long (91 > 79 characters)
- Line 970: E226 missing whitespace around arithmetic operator
- Line 985: E501 line too long (87 > 79 characters)
- Line 999: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/services/demographic_analytics.py
- Line 11: E501 line too long (87 > 79 characters)
- Line 23: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 94: E501 line too long (88 > 79 characters)
- Line 102: E501 line too long (87 > 79 characters)
- Line 107: E501 line too long (85 > 79 characters)
- Line 108: W293 blank line contains whitespace
- Line 23: Trailing whitespace
- Line 43: Trailing whitespace
- Line 58: Trailing whitespace
- Line 71: Trailing whitespace
- Line 88: Trailing whitespace
- Line 108: Trailing whitespace

### src/piwardrive/widgets/battery_status.py
- Line 42: E501 line too long (82 > 79 characters)
- Line 43: E501 line too long (81 > 79 characters)

### scripts/df_integration_demo.py
- Line 4: E501 line too long (82 > 79 characters)
- Line 15: E402 module level import not at top of file
- Line 34: E501 line too long (85 > 79 characters)
- Line 217: E501 line too long (82 > 79 characters)

### tests/test_gps_handler.py
- Line 9: E501 line too long (84 > 79 characters)

### src/piwardrive/analysis/packet_engine.py
- Line 157: E501 line too long (83 > 79 characters)
- Line 410: E501 line too long (87 > 79 characters)
- Line 478: E203 whitespace before ':'
- Line 752: E501 line too long (88 > 79 characters)
- Line 941: E501 line too long (87 > 79 characters)
- Line 1010: E501 line too long (84 > 79 characters)
- Line 1050: E501 line too long (86 > 79 characters)
- Line 1061: E501 line too long (84 > 79 characters)
- Line 1070: E501 line too long (85 > 79 characters)
- Line 1164: E501 line too long (84 > 79 characters)
- Line 1165: E501 line too long (80 > 79 characters)
- Line 1167: E501 line too long (83 > 79 characters)
- Line 1186: E501 line too long (122 > 79 characters)
- Line 1190: E501 line too long (98 > 79 characters)
- Line 1194: E501 line too long (82 > 79 characters)
- Line 1201: E226 missing whitespace around arithmetic operator
- Line 1211: E501 line too long (81 > 79 characters)
- Line 1220: E501 line too long (81 > 79 characters)
- Line 1222: E501 line too long (90 > 79 characters)
- Line 1186: Line too long (122 > 120 characters)

### src/piwardrive/routes/wifi.py
- Line 69: E501 line too long (87 > 79 characters)
- Line 155: E501 line too long (87 > 79 characters)

### scripts/export_mysql.py
- Line 29: E501 line too long (80 > 79 characters)
- Line 30: E501 line too long (85 > 79 characters)
- Line 31: E501 line too long (88 > 79 characters)
- Line 32: E501 line too long (86 > 79 characters)
- Line 33: E501 line too long (84 > 79 characters)
- Line 34: E501 line too long (88 > 79 characters)

### tests/test_geometry_utils.py
- Line 19: E501 line too long (82 > 79 characters)

### src/piwardrive/logging/dynamic_config.py
- Line 50: E501 line too long (81 > 79 characters)
- Line 70: E501 line too long (82 > 79 characters)
- Line 72: E501 line too long (82 > 79 characters)

### tests/test_service_sync.py
- Line 16: E501 line too long (82 > 79 characters)
- Line 42: E501 line too long (80 > 79 characters)

### tests/test_kiosk_cli.py
- Line 31: E501 line too long (86 > 79 characters)

### src/piwardrive/mining/advanced_data_mining.py
- Line 48: E302 expected 2 blank lines, found 1
- Line 62: E302 expected 2 blank lines, found 1
- Line 78: E302 expected 2 blank lines, found 1
- Line 98: E501 line too long (86 > 79 characters)
- Line 107: E501 line too long (84 > 79 characters)
- Line 141: E501 line too long (83 > 79 characters)
- Line 149: E501 line too long (94 > 79 characters)
- Line 159: E203 whitespace before ':'
- Line 159: E501 line too long (84 > 79 characters)
- Line 189: E203 whitespace before ':'
- Line 206: E203 whitespace before ':'
- Line 281: E501 line too long (80 > 79 characters)
- Line 296: E501 line too long (83 > 79 characters)
- Line 304: E203 whitespace before ':'
- Line 304: E501 line too long (87 > 79 characters)
- Line 350: E501 line too long (81 > 79 characters)
- Line 390: E501 line too long (85 > 79 characters)
- Line 418: E501 line too long (81 > 79 characters)
- Line 424: E501 line too long (85 > 79 characters)
- Line 431: E501 line too long (84 > 79 characters)
- Line 475: E501 line too long (82 > 79 characters)
- Line 529: E501 line too long (84 > 79 characters)
- Line 598: E501 line too long (81 > 79 characters)
- Line 624: E501 line too long (87 > 79 characters)
- Line 676: E501 line too long (88 > 79 characters)
- Line 721: E501 line too long (88 > 79 characters)
- Line 746: E501 line too long (91 > 79 characters)
- Line 784: E501 line too long (88 > 79 characters)
- Line 790: E501 line too long (83 > 79 characters)
- Line 807: E501 line too long (145 > 79 characters)
- Line 816: E501 line too long (108 > 79 characters)
- Line 816: E226 missing whitespace around arithmetic operator
- Line 824: E226 missing whitespace around arithmetic operator
- Line 824: E501 line too long (101 > 79 characters)
- Line 846: E501 line too long (82 > 79 characters)
- Line 850: E501 line too long (85 > 79 characters)
- Line 857: E501 line too long (123 > 79 characters)
- Line 883: E501 line too long (81 > 79 characters)
- Line 896: E501 line too long (86 > 79 characters)
- Line 901: E501 line too long (80 > 79 characters)
- Line 905: E501 line too long (80 > 79 characters)
- Line 967: E501 line too long (104 > 79 characters)
- Line 994: E501 line too long (87 > 79 characters)
- Line 995: E501 line too long (87 > 79 characters)
- Line 1005: E303 too many blank lines (3)
- Line 1043: E501 line too long (87 > 79 characters)
- Line 1072: E501 line too long (84 > 79 characters)
- Line 1078: E501 line too long (86 > 79 characters)
- Line 1090: W503 line break before binary operator
- Line 1097: E501 line too long (110 > 79 characters)
- Line 1133: E501 line too long (82 > 79 characters)
- Line 1161: E501 line too long (84 > 79 characters)
- Line 1167: E501 line too long (85 > 79 characters)
- Line 1168: E501 line too long (82 > 79 characters)
- Line 1188: E501 line too long (85 > 79 characters)
- Line 1194: E302 expected 2 blank lines, found 1
- Line 1251: E501 line too long (87 > 79 characters)
- Line 1252: E501 line too long (88 > 79 characters)
- Line 1253: E501 line too long (87 > 79 characters)
- Line 1254: E501 line too long (87 > 79 characters)
- Line 1255: E501 line too long (88 > 79 characters)
- Line 1274: E501 line too long (84 > 79 characters)
- Line 1282: E501 line too long (80 > 79 characters)
- Line 1289: E501 line too long (118 > 79 characters)
- Line 1301: E305 expected 2 blank lines after class or function definition, found 1
- Line 807: Line too long (145 > 120 characters)
- Line 857: Line too long (123 > 120 characters)

### src/piwardrive/logging/config.py
- Line 27: E501 line too long (85 > 79 characters)
- Line 60: E501 line too long (83 > 79 characters)
- Line 78: W503 line break before binary operator
- Line 79: W503 line break before binary operator
- Line 90: E501 line too long (84 > 79 characters)

### src/piwardrive/services/analytics_processor.py
- Line 54: E501 line too long (84 > 79 characters)
- Line 56: E501 line too long (81 > 79 characters)
- Line 73: E501 line too long (82 > 79 characters)

### src/piwardrive/widgets/health_analysis.py
- Line 33: E501 line too long (81 > 79 characters)
- Line 49: E501 line too long (85 > 79 characters)
- Line 62: E501 line too long (80 > 79 characters)

### src/piwardrive/analytics/iot.py
- Line 71: E203 whitespace before ':'

### src/piwardrive/migrations/__init__.py
- Line 8: E501 line too long (81 > 79 characters)
- Line 9: E501 line too long (85 > 79 characters)
- Line 11: E501 line too long (84 > 79 characters)
- Line 12: E501 line too long (85 > 79 characters)
- Line 13: E501 line too long (86 > 79 characters)
- Line 14: E501 line too long (82 > 79 characters)
- Line 15: E501 line too long (83 > 79 characters)

### src/piwardrive/services/model_trainer.py
- Line 15: W293 blank line contains whitespace
- Line 15: Trailing whitespace

### src/piwardrive/core/__init__.py
- Line 4: E501 line too long (80 > 79 characters)
- Line 6: W292 no newline at end of file

### src/piwardrive/logging/structured_logger.py
- Line 50: E501 line too long (85 > 79 characters)
- Line 73: E501 line too long (81 > 79 characters)
- Line 84: E501 line too long (80 > 79 characters)
- Line 95: W503 line break before binary operator
- Line 96: W503 line break before binary operator
- Line 97: W503 line break before binary operator
- Line 98: W503 line break before binary operator
- Line 103: E501 line too long (80 > 79 characters)
- Line 106: E501 line too long (81 > 79 characters)
- Line 167: W293 blank line contains whitespace
- Line 175: E501 line too long (90 > 79 characters)
- Line 176: E501 line too long (101 > 79 characters)
- Line 178: E501 line too long (96 > 79 characters)
- Line 195: E501 line too long (81 > 79 characters)
- Line 211: E501 line too long (81 > 79 characters)
- Line 217: E501 line too long (81 > 79 characters)
- Line 167: Trailing whitespace

### src/piwardrive/visualization/advanced_visualization.py
- Line 126: E501 line too long (82 > 79 characters)
- Line 168: E501 line too long (85 > 79 characters)
- Line 175: E501 line too long (80 > 79 characters)
- Line 178: E501 line too long (85 > 79 characters)
- Line 179: E501 line too long (85 > 79 characters)
- Line 210: E501 line too long (86 > 79 characters)
- Line 250: W503 line break before binary operator
- Line 324: E741 ambiguous variable name 'l'
- Line 326: E501 line too long (83 > 79 characters)
- Line 345: E501 line too long (83 > 79 characters)
- Line 472: E501 line too long (84 > 79 characters)
- Line 520: E501 line too long (87 > 79 characters)
- Line 521: E501 line too long (84 > 79 characters)
- Line 530: E501 line too long (83 > 79 characters)
- Line 536: W503 line break before binary operator
- Line 538: W503 line break before binary operator
- Line 593: E501 line too long (87 > 79 characters)
- Line 594: E501 line too long (95 > 79 characters)
- Line 644: E501 line too long (84 > 79 characters)
- Line 646: E501 line too long (88 > 79 characters)
- Line 747: E501 line too long (84 > 79 characters)
- Line 788: E501 line too long (81 > 79 characters)
- Line 814: E501 line too long (83 > 79 characters)
- Line 825: E501 line too long (81 > 79 characters)
- Line 868: E501 line too long (85 > 79 characters)
- Line 894: E501 line too long (87 > 79 characters)
- Line 919: E501 line too long (87 > 79 characters)
- Line 1046: E501 line too long (82 > 79 characters)
- Line 1054: E501 line too long (85 > 79 characters)
- Line 1089: E501 line too long (83 > 79 characters)
- Line 1090: E501 line too long (88 > 79 characters)
- Line 1157: E501 line too long (81 > 79 characters)

### src/piwardrive/logging/scheduler.py
- Line 68: E501 line too long (85 > 79 characters)
- Line 70: E501 line too long (86 > 79 characters)
- Line 71: E501 line too long (83 > 79 characters)
- Line 72: E501 line too long (86 > 79 characters)

### src/piwardrive/migrations/003_create_bluetooth_detections.py
- Line 46: E501 line too long (107 > 79 characters)
- Line 49: E501 line too long (99 > 79 characters)
- Line 52: E501 line too long (108 > 79 characters)
- Line 55: E501 line too long (112 > 79 characters)
- Line 58: E501 line too long (97 > 79 characters)

### tests/test_integration_comprehensive.py
- Line 51: E501 line too long (85 > 79 characters)
- Line 63: E501 line too long (84 > 79 characters)
- Line 177: E501 line too long (82 > 79 characters)
- Line 198: E501 line too long (84 > 79 characters)
- Line 241: E501 line too long (83 > 79 characters)
- Line 256: E501 line too long (80 > 79 characters)
- Line 369: E501 line too long (88 > 79 characters)
- Line 373: E501 line too long (80 > 79 characters)
- Line 403: E501 line too long (81 > 79 characters)
- Line 427: E501 line too long (80 > 79 characters)
- Line 483: E226 missing whitespace around arithmetic operator
- Line 483: E228 missing whitespace around modulo operator
- Line 528: E501 line too long (80 > 79 characters)
- Line 536: E501 line too long (86 > 79 characters)
- Line 545: E501 line too long (80 > 79 characters)
- Line 564: E226 missing whitespace around arithmetic operator
- Line 564: E228 missing whitespace around modulo operator
- Line 585: E501 line too long (85 > 79 characters)

### scripts/validate_migration.py
- Line 23: E501 line too long (81 > 79 characters)
- Line 24: E501 line too long (85 > 79 characters)
- Line 45: E501 line too long (87 > 79 characters)

### src/piwardrive/direction_finding/config.py
- Line 87: E501 line too long (82 > 79 characters)
- Line 105: E501 line too long (88 > 79 characters)
- Line 182: E501 line too long (80 > 79 characters)
- Line 190: E501 line too long (81 > 79 characters)
- Line 253: E501 line too long (83 > 79 characters)
- Line 255: E501 line too long (84 > 79 characters)
- Line 257: E501 line too long (81 > 79 characters)
- Line 265: E501 line too long (83 > 79 characters)
- Line 282: E501 line too long (82 > 79 characters)
- Line 286: E501 line too long (84 > 79 characters)
- Line 373: E501 line too long (87 > 79 characters)
- Line 375: E501 line too long (96 > 79 characters)
- Line 472: E501 line too long (82 > 79 characters)
- Line 482: E501 line too long (81 > 79 characters)
- Line 506: E501 line too long (86 > 79 characters)
- Line 513: E501 line too long (81 > 79 characters)
- Line 514: E501 line too long (85 > 79 characters)
- Line 515: E501 line too long (85 > 79 characters)
- Line 519: E501 line too long (93 > 79 characters)
- Line 529: E501 line too long (81 > 79 characters)
- Line 531: E501 line too long (80 > 79 characters)
- Line 538: E501 line too long (80 > 79 characters)
- Line 540: E501 line too long (82 > 79 characters)

### tests/test_mysql_export.py
- Line 51: E501 line too long (82 > 79 characters)
- Line 63: E501 line too long (83 > 79 characters)
- Line 65: E501 line too long (83 > 79 characters)

### src/pwutils/__init__.py
- Line 1: W292 no newline at end of file

### src/piwardrive/plugins/plugin_architecture.py
- Line 220: E501 line too long (85 > 79 characters)
- Line 229: E501 line too long (81 > 79 characters)
- Line 261: E501 line too long (81 > 79 characters)
- Line 333: E501 line too long (82 > 79 characters)
- Line 420: E501 line too long (84 > 79 characters)
- Line 523: E501 line too long (84 > 79 characters)
- Line 611: E128 continuation line under-indented for visual indent
- Line 700: E501 line too long (84 > 79 characters)
- Line 709: E501 line too long (85 > 79 characters)

### src/piwardrive/core/utils.py
- Line 3: E501 line too long (82 > 79 characters)
- Line 188: E501 line too long (88 > 79 characters)
- Line 213: E501 line too long (84 > 79 characters)
- Line 234: E501 line too long (88 > 79 characters)
- Line 316: E501 line too long (85 > 79 characters)
- Line 368: E501 line too long (85 > 79 characters)
- Line 396: E501 line too long (80 > 79 characters)
- Line 451: E501 line too long (85 > 79 characters)
- Line 482: E501 line too long (87 > 79 characters)
- Line 553: E501 line too long (84 > 79 characters)
- Line 596: E501 line too long (82 > 79 characters)
- Line 660: E501 line too long (85 > 79 characters)
- Line 748: E501 line too long (81 > 79 characters)
- Line 772: E501 line too long (80 > 79 characters)
- Line 773: E501 line too long (86 > 79 characters)
- Line 775: E501 line too long (88 > 79 characters)
- Line 794: E501 line too long (85 > 79 characters)
- Line 841: E501 line too long (87 > 79 characters)
- Line 916: E501 line too long (81 > 79 characters)
- Line 1097: E501 line too long (85 > 79 characters)
- Line 1104: E501 line too long (86 > 79 characters)
- Line 1105: E501 line too long (83 > 79 characters)
- Line 1117: W503 line break before binary operator
- Line 1125: E501 line too long (85 > 79 characters)
- Line 1164: E501 line too long (83 > 79 characters)
- Line 1213: E501 line too long (81 > 79 characters)
- Line 1218: E501 line too long (87 > 79 characters)
- Line 1228: E501 line too long (86 > 79 characters)

### scripts/export_grafana.py
- Line 33: E501 line too long (83 > 79 characters)
- Line 39: E501 line too long (82 > 79 characters)
- Line 61: E501 line too long (86 > 79 characters)

### scripts/monitoring_service.py
- Line 3: E501 line too long (82 > 79 characters)
- Line 19: E402 module level import not at top of file
- Line 61: E501 line too long (80 > 79 characters)
- Line 140: E501 line too long (132 > 79 characters)
- Line 152: E501 line too long (115 > 79 characters)
- Line 161: E501 line too long (83 > 79 characters)
- Line 164: E501 line too long (80 > 79 characters)
- Line 171: E501 line too long (151 > 79 characters)
- Line 182: E501 line too long (83 > 79 characters)
- Line 202: E501 line too long (105 > 79 characters)
- Line 213: E501 line too long (100 > 79 characters)
- Line 226: E501 line too long (138 > 79 characters)
- Line 250: E501 line too long (80 > 79 characters)
- Line 261: E501 line too long (81 > 79 characters)
- Line 264: E501 line too long (80 > 79 characters)
- Line 266: E501 line too long (83 > 79 characters)
- Line 271: E501 line too long (100 > 79 characters)
- Line 271: E226 missing whitespace around arithmetic operator
- Line 286: E501 line too long (85 > 79 characters)
- Line 291: E501 line too long (105 > 79 characters)
- Line 302: E501 line too long (80 > 79 characters)
- Line 328: E501 line too long (137 > 79 characters)
- Line 371: E501 line too long (86 > 79 characters)
- Line 378: W503 line break before binary operator
- Line 384: E501 line too long (111 > 79 characters)
- Line 384: E226 missing whitespace around arithmetic operator
- Line 386: E501 line too long (82 > 79 characters)
- Line 387: W503 line break before binary operator
- Line 418: E501 line too long (84 > 79 characters)
- Line 432: W503 line break before binary operator
- Line 433: W503 line break before binary operator
- Line 434: W503 line break before binary operator
- Line 435: W503 line break before binary operator
- Line 455: E501 line too long (82 > 79 characters)
- Line 503: E501 line too long (84 > 79 characters)
- Line 505: E501 line too long (80 > 79 characters)
- Line 521: W503 line break before binary operator
- Line 140: Line too long (132 > 120 characters)
- Line 171: Line too long (151 > 120 characters)
- Line 226: Line too long (138 > 120 characters)
- Line 328: Line too long (137 > 120 characters)

### src/piwardrive/widgets/health_status.py
- Line 53: E501 line too long (83 > 79 characters)

### tests/test_export_log_bundle_script.py
- Line 16: E501 line too long (85 > 79 characters)

### src/piwardrive/simpleui.py
- Line 12: E501 line too long (81 > 79 characters)
- Line 13: E501 line too long (80 > 79 characters)

### src/piwardrive/enhanced/critical_additions.py
- Line 4: E501 line too long (84 > 79 characters)
- Line 78: E302 expected 2 blank lines, found 1
- Line 91: E302 expected 2 blank lines, found 1
- Line 107: E302 expected 2 blank lines, found 1
- Line 125: W293 blank line contains whitespace
- Line 138: E501 line too long (88 > 79 characters)
- Line 153: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 202: E501 line too long (83 > 79 characters)
- Line 229: E501 line too long (86 > 79 characters)
- Line 256: E501 line too long (81 > 79 characters)
- Line 298: E501 line too long (80 > 79 characters)
- Line 389: W503 line break before binary operator
- Line 396: E501 line too long (81 > 79 characters)
- Line 405: E501 line too long (87 > 79 characters)
- Line 579: E501 line too long (82 > 79 characters)
- Line 592: E501 line too long (81 > 79 characters)
- Line 638: E501 line too long (83 > 79 characters)
- Line 678: E501 line too long (80 > 79 characters)
- Line 685: E501 line too long (80 > 79 characters)
- Line 706: E501 line too long (117 > 79 characters)
- Line 710: E501 line too long (84 > 79 characters)
- Line 727: E501 line too long (90 > 79 characters)
- Line 754: E501 line too long (85 > 79 characters)
- Line 766: E501 line too long (88 > 79 characters)
- Line 774: E501 line too long (114 > 79 characters)
- Line 787: E501 line too long (83 > 79 characters)
- Line 818: E501 line too long (82 > 79 characters)
- Line 893: E303 too many blank lines (3)
- Line 914: E501 line too long (82 > 79 characters)
- Line 940: E501 line too long (87 > 79 characters)
- Line 947: E501 line too long (114 > 79 characters)
- Line 1008: E501 line too long (84 > 79 characters)
- Line 1020: E501 line too long (86 > 79 characters)
- Line 1023: E501 line too long (97 > 79 characters)
- Line 1026: E501 line too long (88 > 79 characters)
- Line 1045: E305 expected 2 blank lines after class or function definition, found 1
- Line 125: Trailing whitespace
- Line 153: Trailing whitespace
- Line 171: Trailing whitespace

### tests/test_jwt_utils_comprehensive.py
- Line 19: E402 module level import not at top of file
- Line 22: E402 module level import not at top of file
- Line 39: E501 line too long (82 > 79 characters)
- Line 69: E501 line too long (82 > 79 characters)
- Line 84: E501 line too long (84 > 79 characters)
- Line 97: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 102: E501 line too long (89 > 79 characters)
- Line 110: W293 blank line contains whitespace
- Line 112: E501 line too long (85 > 79 characters)
- Line 113: W293 blank line contains whitespace
- Line 114: E501 line too long (89 > 79 characters)
- Line 121: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 125: E501 line too long (89 > 79 characters)
- Line 137: W293 blank line contains whitespace
- Line 140: E501 line too long (93 > 79 characters)
- Line 147: W293 blank line contains whitespace
- Line 149: E501 line too long (89 > 79 characters)
- Line 150: W293 blank line contains whitespace
- Line 152: E501 line too long (82 > 79 characters)
- Line 162: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 167: E501 line too long (89 > 79 characters)
- Line 176: W293 blank line contains whitespace
- Line 178: E501 line too long (86 > 79 characters)
- Line 179: W293 blank line contains whitespace
- Line 180: E501 line too long (89 > 79 characters)
- Line 188: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 192: E501 line too long (89 > 79 characters)
- Line 199: W293 blank line contains whitespace
- Line 200: E501 line too long (89 > 79 characters)
- Line 206: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 210: E501 line too long (103 > 79 characters)
- Line 211: E501 line too long (105 > 79 characters)
- Line 212: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 231: W293 blank line contains whitespace
- Line 239: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 253: W293 blank line contains whitespace
- Line 257: W293 blank line contains whitespace
- Line 260: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 278: W293 blank line contains whitespace
- Line 288: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 314: E501 line too long (86 > 79 characters)
- Line 315: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 339: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 346: W293 blank line contains whitespace
- Line 348: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 361: W293 blank line contains whitespace
- Line 365: W293 blank line contains whitespace
- Line 375: W293 blank line contains whitespace
- Line 379: W293 blank line contains whitespace
- Line 383: W293 blank line contains whitespace
- Line 387: W293 blank line contains whitespace
- Line 399: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 420: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 97: Trailing whitespace
- Line 100: Trailing whitespace
- Line 110: Trailing whitespace
- Line 113: Trailing whitespace
- Line 121: Trailing whitespace
- Line 124: Trailing whitespace
- Line 137: Trailing whitespace
- Line 147: Trailing whitespace
- Line 150: Trailing whitespace
- Line 162: Trailing whitespace
- Line 165: Trailing whitespace
- Line 176: Trailing whitespace
- Line 179: Trailing whitespace
- Line 188: Trailing whitespace
- Line 191: Trailing whitespace
- Line 199: Trailing whitespace
- Line 206: Trailing whitespace
- Line 209: Trailing whitespace
- Line 212: Trailing whitespace
- Line 215: Trailing whitespace
- Line 219: Trailing whitespace
- Line 231: Trailing whitespace
- Line 239: Trailing whitespace
- Line 246: Trailing whitespace
- Line 253: Trailing whitespace
- Line 257: Trailing whitespace
- Line 260: Trailing whitespace
- Line 267: Trailing whitespace
- Line 270: Trailing whitespace
- Line 278: Trailing whitespace
- Line 288: Trailing whitespace
- Line 305: Trailing whitespace
- Line 315: Trailing whitespace
- Line 326: Trailing whitespace
- Line 332: Trailing whitespace
- Line 339: Trailing whitespace
- Line 342: Trailing whitespace
- Line 346: Trailing whitespace
- Line 348: Trailing whitespace
- Line 357: Trailing whitespace
- Line 361: Trailing whitespace
- Line 365: Trailing whitespace
- Line 375: Trailing whitespace
- Line 379: Trailing whitespace
- Line 383: Trailing whitespace
- Line 387: Trailing whitespace
- Line 399: Trailing whitespace
- Line 403: Trailing whitespace
- Line 406: Trailing whitespace
- Line 410: Trailing whitespace
- Line 420: Trailing whitespace
- Line 424: Trailing whitespace
- Line 428: Trailing whitespace

### src/piwardrive/services/stream_processor.py
- Line 24: W293 blank line contains whitespace
- Line 30: E501 line too long (85 > 79 characters)
- Line 61: W293 blank line contains whitespace
- Line 65: E501 line too long (85 > 79 characters)
- Line 73: W293 blank line contains whitespace
- Line 79: E501 line too long (82 > 79 characters)
- Line 83: E501 line too long (80 > 79 characters)
- Line 89: E501 line too long (84 > 79 characters)
- Line 95: W293 blank line contains whitespace
- Line 103: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 24: Trailing whitespace
- Line 61: Trailing whitespace
- Line 73: Trailing whitespace
- Line 95: Trailing whitespace
- Line 103: Trailing whitespace
- Line 111: Trailing whitespace

### tests/test_main_application_comprehensive.py
- Line 24: W293 blank line contains whitespace
- Line 29: E501 line too long (82 > 79 characters)
- Line 30: E501 line too long (85 > 79 characters)
- Line 31: E501 line too long (84 > 79 characters)
- Line 32: W293 blank line contains whitespace
- Line 34: W293 blank line contains whitespace
- Line 40: E501 line too long (86 > 79 characters)
- Line 41: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 59: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 74: E501 line too long (84 > 79 characters)
- Line 75: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 85: E501 line too long (96 > 79 characters)
- Line 86: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 90: E501 line too long (86 > 79 characters)
- Line 91: E501 line too long (93 > 79 characters)
- Line 92: E501 line too long (94 > 79 characters)
- Line 93: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 106: E501 line too long (100 > 79 characters)
- Line 107: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 111: E501 line too long (97 > 79 characters)
- Line 116: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 129: E501 line too long (86 > 79 characters)
- Line 132: W293 blank line contains whitespace
- Line 134: W293 blank line contains whitespace
- Line 138: E501 line too long (83 > 79 characters)
- Line 139: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 161: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 175: E501 line too long (86 > 79 characters)
- Line 176: W293 blank line contains whitespace
- Line 184: E501 line too long (94 > 79 characters)
- Line 187: W293 blank line contains whitespace
- Line 189: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 201: E501 line too long (84 > 79 characters)
- Line 203: E501 line too long (83 > 79 characters)
- Line 204: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 226: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 236: W293 blank line contains whitespace
- Line 239: W293 blank line contains whitespace
- Line 247: W293 blank line contains whitespace
- Line 249: W293 blank line contains whitespace
- Line 256: W293 blank line contains whitespace
- Line 265: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 272: W293 blank line contains whitespace
- Line 274: E501 line too long (100 > 79 characters)
- Line 275: E501 line too long (81 > 79 characters)
- Line 276: W293 blank line contains whitespace
- Line 284: E501 line too long (90 > 79 characters)
- Line 285: W293 blank line contains whitespace
- Line 287: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 298: E501 line too long (86 > 79 characters)
- Line 299: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 304: W293 blank line contains whitespace
- Line 310: E501 line too long (85 > 79 characters)
- Line 312: E501 line too long (91 > 79 characters)
- Line 313: E501 line too long (99 > 79 characters)
- Line 314: W293 blank line contains whitespace
- Line 316: W293 blank line contains whitespace
- Line 325: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 340: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 345: E501 line too long (111 > 79 characters)
- Line 347: E501 line too long (82 > 79 characters)
- Line 352: W293 blank line contains whitespace
- Line 358: W293 blank line contains whitespace
- Line 363: W293 blank line contains whitespace
- Line 365: E501 line too long (93 > 79 characters)
- Line 367: W293 blank line contains whitespace
- Line 373: W293 blank line contains whitespace
- Line 378: W293 blank line contains whitespace
- Line 380: E501 line too long (96 > 79 characters)
- Line 382: W293 blank line contains whitespace
- Line 390: W293 blank line contains whitespace
- Line 395: E501 line too long (86 > 79 characters)
- Line 397: E501 line too long (112 > 79 characters)
- Line 399: W293 blank line contains whitespace
- Line 401: E501 line too long (98 > 79 characters)
- Line 403: W293 blank line contains whitespace
- Line 411: E501 line too long (90 > 79 characters)
- Line 412: E501 line too long (94 > 79 characters)
- Line 413: W293 blank line contains whitespace
- Line 416: W293 blank line contains whitespace
- Line 417: E501 line too long (87 > 79 characters)
- Line 423: W293 blank line contains whitespace
- Line 428: E501 line too long (82 > 79 characters)
- Line 429: E501 line too long (85 > 79 characters)
- Line 430: E501 line too long (84 > 79 characters)
- Line 431: E501 line too long (91 > 79 characters)
- Line 432: E501 line too long (99 > 79 characters)
- Line 433: W293 blank line contains whitespace
- Line 435: W293 blank line contains whitespace
- Line 448: W293 blank line contains whitespace
- Line 450: E501 line too long (82 > 79 characters)
- Line 453: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 472: E501 line too long (86 > 79 characters)
- Line 475: W293 blank line contains whitespace
- Line 476: E501 line too long (94 > 79 characters)
- Line 478: W293 blank line contains whitespace
- Line 480: E501 line too long (82 > 79 characters)
- Line 481: E501 line too long (81 > 79 characters)
- Line 482: E501 line too long (108 > 79 characters)
- Line 483: E501 line too long (89 > 79 characters)
- Line 485: E501 line too long (94 > 79 characters)
- Line 486: W293 blank line contains whitespace
- Line 497: W293 blank line contains whitespace
- Line 502: W293 blank line contains whitespace
- Line 504: W293 blank line contains whitespace
- Line 507: E501 line too long (88 > 79 characters)
- Line 510: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 520: W293 blank line contains whitespace
- Line 524: W293 blank line contains whitespace
- Line 527: E501 line too long (84 > 79 characters)
- Line 528: W293 blank line contains whitespace
- Line 24: Trailing whitespace
- Line 32: Trailing whitespace
- Line 34: Trailing whitespace
- Line 41: Trailing whitespace
- Line 45: Trailing whitespace
- Line 51: Trailing whitespace
- Line 57: Trailing whitespace
- Line 59: Trailing whitespace
- Line 62: Trailing whitespace
- Line 67: Trailing whitespace
- Line 73: Trailing whitespace
- Line 75: Trailing whitespace
- Line 77: Trailing whitespace
- Line 86: Trailing whitespace
- Line 88: Trailing whitespace
- Line 93: Trailing whitespace
- Line 101: Trailing whitespace
- Line 107: Trailing whitespace
- Line 109: Trailing whitespace
- Line 116: Trailing whitespace
- Line 124: Trailing whitespace
- Line 132: Trailing whitespace
- Line 134: Trailing whitespace
- Line 139: Trailing whitespace
- Line 147: Trailing whitespace
- Line 152: Trailing whitespace
- Line 154: Trailing whitespace
- Line 161: Trailing whitespace
- Line 169: Trailing whitespace
- Line 171: Trailing whitespace
- Line 176: Trailing whitespace
- Line 187: Trailing whitespace
- Line 189: Trailing whitespace
- Line 194: Trailing whitespace
- Line 204: Trailing whitespace
- Line 206: Trailing whitespace
- Line 210: Trailing whitespace
- Line 218: Trailing whitespace
- Line 220: Trailing whitespace
- Line 226: Trailing whitespace
- Line 234: Trailing whitespace
- Line 236: Trailing whitespace
- Line 239: Trailing whitespace
- Line 247: Trailing whitespace
- Line 249: Trailing whitespace
- Line 256: Trailing whitespace
- Line 265: Trailing whitespace
- Line 270: Trailing whitespace
- Line 272: Trailing whitespace
- Line 276: Trailing whitespace
- Line 285: Trailing whitespace
- Line 287: Trailing whitespace
- Line 290: Trailing whitespace
- Line 299: Trailing whitespace
- Line 301: Trailing whitespace
- Line 304: Trailing whitespace
- Line 314: Trailing whitespace
- Line 316: Trailing whitespace
- Line 325: Trailing whitespace
- Line 335: Trailing whitespace
- Line 340: Trailing whitespace
- Line 342: Trailing whitespace
- Line 352: Trailing whitespace
- Line 358: Trailing whitespace
- Line 363: Trailing whitespace
- Line 367: Trailing whitespace
- Line 373: Trailing whitespace
- Line 378: Trailing whitespace
- Line 382: Trailing whitespace
- Line 390: Trailing whitespace
- Line 399: Trailing whitespace
- Line 403: Trailing whitespace
- Line 413: Trailing whitespace
- Line 416: Trailing whitespace
- Line 423: Trailing whitespace
- Line 433: Trailing whitespace
- Line 435: Trailing whitespace
- Line 448: Trailing whitespace
- Line 453: Trailing whitespace
- Line 467: Trailing whitespace
- Line 475: Trailing whitespace
- Line 478: Trailing whitespace
- Line 486: Trailing whitespace
- Line 497: Trailing whitespace
- Line 502: Trailing whitespace
- Line 504: Trailing whitespace
- Line 510: Trailing whitespace
- Line 518: Trailing whitespace
- Line 520: Trailing whitespace
- Line 524: Trailing whitespace
- Line 528: Trailing whitespace

### src/service.py
- Line 5: E501 line too long (80 > 79 characters)
- Line 35: E501 line too long (81 > 79 characters)
- Line 38: E501 line too long (82 > 79 characters)

### src/piwardrive/signal/rf_spectrum.py
- Line 30: E302 expected 2 blank lines, found 1
- Line 40: E302 expected 2 blank lines, found 1
- Line 49: E302 expected 2 blank lines, found 1
- Line 61: E302 expected 2 blank lines, found 1
- Line 72: E302 expected 2 blank lines, found 1
- Line 91: E501 line too long (85 > 79 characters)
- Line 105: E501 line too long (86 > 79 characters)
- Line 114: E303 too many blank lines (3)
- Line 145: E501 line too long (81 > 79 characters)
- Line 168: W503 line break before binary operator
- Line 175: E501 line too long (87 > 79 characters)
- Line 298: E501 line too long (82 > 79 characters)
- Line 305: E501 line too long (84 > 79 characters)
- Line 318: E501 line too long (83 > 79 characters)
- Line 329: E501 line too long (85 > 79 characters)
- Line 343: E501 line too long (81 > 79 characters)
- Line 353: W503 line break before binary operator
- Line 417: E501 line too long (86 > 79 characters)
- Line 440: E501 line too long (84 > 79 characters)
- Line 485: E501 line too long (85 > 79 characters)
- Line 499: E501 line too long (88 > 79 characters)
- Line 502: E501 line too long (85 > 79 characters)
- Line 514: E501 line too long (80 > 79 characters)
- Line 519: E501 line too long (80 > 79 characters)
- Line 531: E501 line too long (82 > 79 characters)
- Line 583: E302 expected 2 blank lines, found 1
- Line 607: E226 missing whitespace around arithmetic operator
- Line 607: E501 line too long (115 > 79 characters)
- Line 607: E226 missing whitespace around arithmetic operator
- Line 611: E501 line too long (84 > 79 characters)
- Line 619: E226 missing whitespace around arithmetic operator
- Line 619: E501 line too long (89 > 79 characters)
- Line 637: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/widgets/orientation_widget.py
- Line 40: E501 line too long (86 > 79 characters)

### scripts/watch_service.py
- Line 18: E501 line too long (80 > 79 characters)

### src/piwardrive/scan_report.py
- Line 48: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 48: Trailing whitespace
- Line 51: Trailing whitespace

### src/piwardrive/widgets/storage_usage.py
- Line 27: E501 line too long (87 > 79 characters)

### src/piwardrive/jwt_utils.py
- Line 22: W293 blank line contains whitespace
- Line 26: W293 blank line contains whitespace
- Line 34: E501 line too long (81 > 79 characters)
- Line 36: W293 blank line contains whitespace
- Line 40: W293 blank line contains whitespace
- Line 54: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 22: Trailing whitespace
- Line 26: Trailing whitespace
- Line 36: Trailing whitespace
- Line 40: Trailing whitespace
- Line 54: Trailing whitespace
- Line 57: Trailing whitespace

### tests/test_performance_comprehensive.py
- Line 66: E501 line too long (85 > 79 characters)
- Line 72: E231 missing whitespace after ','
- Line 72: E501 line too long (125 > 79 characters)
- Line 72: E231 missing whitespace after ','
- Line 72: E231 missing whitespace after ','
- Line 73: E231 missing whitespace after ','
- Line 76: E231 missing whitespace after ','
- Line 77: E231 missing whitespace after ','
- Line 77: E231 missing whitespace after ','
- Line 78: E231 missing whitespace after ','
- Line 79: E231 missing whitespace after ','
- Line 79: E231 missing whitespace after ','
- Line 80: E231 missing whitespace after ','
- Line 81: E231 missing whitespace after ','
- Line 81: E231 missing whitespace after ','
- Line 81: E501 line too long (89 > 79 characters)
- Line 103: E128 continuation line under-indented for visual indent
- Line 103: E125 continuation line with same indent as next logical line
- Line 103: E231 missing whitespace after ','
- Line 120: E231 missing whitespace after ','
- Line 127: E501 line too long (82 > 79 characters)
- Line 135: E302 expected 2 blank lines, found 1
- Line 158: E125 continuation line with same indent as next logical line
- Line 158: E128 continuation line under-indented for visual indent
- Line 164: E226 missing whitespace around arithmetic operator
- Line 164: E228 missing whitespace around modulo operator
- Line 177: E231 missing whitespace after ','
- Line 177: E501 line too long (92 > 79 characters)
- Line 180: E231 missing whitespace after ','
- Line 180: E501 line too long (112 > 79 characters)
- Line 193: E226 missing whitespace around arithmetic operator
- Line 193: E228 missing whitespace around modulo operator
- Line 195: E231 missing whitespace after ','
- Line 202: E231 missing whitespace after ','
- Line 202: E501 line too long (256 > 79 characters)
- Line 202: E231 missing whitespace after ','
- Line 202: E231 missing whitespace after ','
- Line 202: E231 missing whitespace after ','
- Line 203: E128 continuation line under-indented for visual indent
- Line 203: E231 missing whitespace after ','
- Line 214: E501 line too long (83 > 79 characters)
- Line 230: E228 missing whitespace around modulo operator
- Line 232: E231 missing whitespace after ','
- Line 244: E501 line too long (85 > 79 characters)
- Line 245: E128 continuation line under-indented for visual indent
- Line 245: E501 line too long (85 > 79 characters)
- Line 251: E128 continuation line under-indented for visual indent
- Line 252: E128 continuation line under-indented for visual indent
- Line 263: E231 missing whitespace after ','
- Line 263: E501 line too long (102 > 79 characters)
- Line 285: E226 missing whitespace around arithmetic operator
- Line 285: E228 missing whitespace around modulo operator
- Line 287: E231 missing whitespace after ','
- Line 287: E501 line too long (82 > 79 characters)
- Line 298: E231 missing whitespace after ','
- Line 298: E501 line too long (89 > 79 characters)
- Line 318: E231 missing whitespace after ','
- Line 318: E501 line too long (82 > 79 characters)
- Line 333: E231 missing whitespace after ','
- Line 333: E501 line too long (90 > 79 characters)
- Line 351: E231 missing whitespace after ','
- Line 351: E231 missing whitespace after ','
- Line 351: E231 missing whitespace after ','
- Line 351: E501 line too long (92 > 79 characters)
- Line 355: E501 line too long (98 > 79 characters)
- Line 355: E231 missing whitespace after ','
- Line 356: E125 continuation line with same indent as next logical line
- Line 356: E128 continuation line under-indented for visual indent
- Line 357: E501 line too long (81 > 79 characters)
- Line 364: E231 missing whitespace after ','
- Line 364: E501 line too long (93 > 79 characters)
- Line 386: E231 missing whitespace after ','
- Line 386: E231 missing whitespace after ','
- Line 386: E231 missing whitespace after ','
- Line 386: E501 line too long (95 > 79 characters)
- Line 389: E501 line too long (84 > 79 characters)
- Line 407: E501 line too long (112 > 79 characters)
- Line 408: W293 blank line contains whitespace
- Line 409: E128 continuation line under-indented for visual indent
- Line 411: E501 line too long (86 > 79 characters)
- Line 415: E128 continuation line under-indented for visual indent
- Line 416: E128 continuation line under-indented for visual indent
- Line 420: E501 line too long (85 > 79 characters)
- Line 431: E231 missing whitespace after ','
- Line 431: E501 line too long (103 > 79 characters)
- Line 434: E231 missing whitespace after ','
- Line 434: E501 line too long (106 > 79 characters)
- Line 456: E226 missing whitespace around arithmetic operator
- Line 456: E228 missing whitespace around modulo operator
- Line 458: E231 missing whitespace after ','
- Line 467: E231 missing whitespace after ','
- Line 467: E501 line too long (170 > 79 characters)
- Line 467: E231 missing whitespace after ','
- Line 468: E128 continuation line under-indented for visual indent
- Line 468: E231 missing whitespace after ','
- Line 468: E501 line too long (148 > 79 characters)
- Line 479: E501 line too long (87 > 79 characters)
- Line 492: E228 missing whitespace around modulo operator
- Line 494: E231 missing whitespace after ','
- Line 504: E231 missing whitespace after ','
- Line 504: E501 line too long (103 > 79 characters)
- Line 516: E231 missing whitespace after ','
- Line 516: E501 line too long (232 > 79 characters)
- Line 516: E231 missing whitespace after ','
- Line 516: E231 missing whitespace after ','
- Line 527: E231 missing whitespace after ','
- Line 527: E501 line too long (112 > 79 characters)
- Line 530: E231 missing whitespace after ','
- Line 530: E501 line too long (112 > 79 characters)
- Line 543: E231 missing whitespace after ','
- Line 557: E226 missing whitespace around arithmetic operator
- Line 557: E228 missing whitespace around modulo operator
- Line 559: E231 missing whitespace after ','
- Line 579: E228 missing whitespace around modulo operator
- Line 581: E231 missing whitespace after ','
- Line 581: E501 line too long (82 > 79 characters)
- Line 616: E231 missing whitespace after ','
- Line 616: E501 line too long (80 > 79 characters)
- Line 632: E231 missing whitespace after ','
- Line 632: E501 line too long (101 > 79 characters)
- Line 649: E501 line too long (97 > 79 characters)
- Line 649: E231 missing whitespace after ','
- Line 662: E231 missing whitespace after ','
- Line 662: E501 line too long (96 > 79 characters)
- Line 684: E501 line too long (110 > 79 characters)
- Line 684: E231 missing whitespace after ','
- Line 687: E501 line too long (90 > 79 characters)
- Line 688: E128 continuation line under-indented for visual indent
- Line 694: E501 line too long (86 > 79 characters)
- Line 701: E501 line too long (96 > 79 characters)
- Line 705: E501 line too long (80 > 79 characters)
- Line 713: E231 missing whitespace after ','
- Line 713: E501 line too long (118 > 79 characters)
- Line 743: E228 missing whitespace around modulo operator
- Line 759: E501 line too long (90 > 79 characters)
- Line 762: E231 missing whitespace after ','
- Line 762: E501 line too long (109 > 79 characters)
- Line 765: E501 line too long (89 > 79 characters)
- Line 765: E231 missing whitespace after ','
- Line 771: E501 line too long (104 > 79 characters)
- Line 772: W293 blank line contains whitespace
- Line 773: E501 line too long (95 > 79 characters)
- Line 774: W293 blank line contains whitespace
- Line 775: E501 line too long (91 > 79 characters)
- Line 794: E305 expected 2 blank lines after class or function definition, found 1
- Line 72: Line too long (125 > 120 characters)
- Line 202: Line too long (256 > 120 characters)
- Line 408: Trailing whitespace
- Line 467: Line too long (170 > 120 characters)
- Line 468: Line too long (148 > 120 characters)
- Line 516: Line too long (232 > 120 characters)
- Line 772: Trailing whitespace
- Line 774: Trailing whitespace

### src/piwardrive/sigint_suite/cellular/tower_tracker/__init__.py
- Line 1: E501 line too long (85 > 79 characters)

### tests/test_sigint_exports.py
- Line 4: E501 line too long (80 > 79 characters)

### src/piwardrive/core/persistence.py
- Line 33: E402 module level import not at top of file
- Line 41: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 108: E501 line too long (88 > 79 characters)
- Line 148: E501 line too long (81 > 79 characters)
- Line 230: E501 line too long (81 > 79 characters)
- Line 234: E501 line too long (81 > 79 characters)
- Line 405: E501 line too long (85 > 79 characters)
- Line 416: E501 line too long (83 > 79 characters)
- Line 436: E501 line too long (88 > 79 characters)
- Line 453: E501 line too long (84 > 79 characters)
- Line 470: E501 line too long (85 > 79 characters)
- Line 471: E501 line too long (85 > 79 characters)
- Line 475: E501 line too long (84 > 79 characters)
- Line 491: W293 blank line contains whitespace
- Line 492: E501 line too long (81 > 79 characters)
- Line 498: E501 line too long (84 > 79 characters)
- Line 527: E501 line too long (84 > 79 characters)
- Line 529: E501 line too long (88 > 79 characters)
- Line 551: E501 line too long (82 > 79 characters)
- Line 563: E501 line too long (83 > 79 characters)
- Line 587: E501 line too long (85 > 79 characters)
- Line 596: E501 line too long (87 > 79 characters)
- Line 607: E501 line too long (82 > 79 characters)
- Line 618: E501 line too long (85 > 79 characters)
- Line 706: E501 line too long (83 > 79 characters)
- Line 720: E501 line too long (87 > 79 characters)
- Line 723: E501 line too long (83 > 79 characters)
- Line 742: E501 line too long (88 > 79 characters)
- Line 743: E501 line too long (82 > 79 characters)
- Line 770: E501 line too long (81 > 79 characters)
- Line 771: E501 line too long (81 > 79 characters)
- Line 774: E501 line too long (80 > 79 characters)
- Line 801: E501 line too long (80 > 79 characters)
- Line 805: E501 line too long (83 > 79 characters)
- Line 806: E501 line too long (82 > 79 characters)
- Line 807: E501 line too long (82 > 79 characters)
- Line 808: E501 line too long (85 > 79 characters)
- Line 866: E501 line too long (81 > 79 characters)
- Line 915: E501 line too long (80 > 79 characters)
- Line 942: E501 line too long (84 > 79 characters)
- Line 946: E501 line too long (85 > 79 characters)
- Line 977: E501 line too long (92 > 79 characters)
- Line 1171: E501 line too long (86 > 79 characters)
- Line 1172: E501 line too long (89 > 79 characters)
- Line 1174: E501 line too long (88 > 79 characters)
- Line 1220: E501 line too long (81 > 79 characters)
- Line 1246: E501 line too long (81 > 79 characters)
- Line 1263: W503 line break before binary operator
- Line 1290: E501 line too long (85 > 79 characters)
- Line 1327: E501 line too long (82 > 79 characters)
- Line 1335: E501 line too long (84 > 79 characters)
- Line 1460: E501 line too long (86 > 79 characters)
- Line 1487: E501 line too long (87 > 79 characters)
- Line 1492: E501 line too long (84 > 79 characters)
- Line 1502: E501 line too long (110 > 79 characters)
- Line 1507: E501 line too long (82 > 79 characters)
- Line 1515: E501 line too long (88 > 79 characters)
- Line 1545: E501 line too long (88 > 79 characters)
- Line 1622: E501 line too long (88 > 79 characters)
- Line 1706: E501 line too long (105 > 79 characters)
- Line 1723: E501 line too long (92 > 79 characters)
- Line 1750: E501 line too long (84 > 79 characters)
- Line 1775: E501 line too long (87 > 79 characters)
- Line 1788: E501 line too long (85 > 79 characters)
- Line 1817: E501 line too long (88 > 79 characters)
- Line 1825: W293 blank line contains whitespace
- Line 1834: W293 blank line contains whitespace
- Line 1836: E501 line too long (86 > 79 characters)
- Line 1839: W293 blank line contains whitespace
- Line 1849: E501 line too long (84 > 79 characters)
- Line 1851: W293 blank line contains whitespace
- Line 1853: W293 blank line contains whitespace
- Line 1857: W293 blank line contains whitespace
- Line 1860: E302 expected 2 blank lines, found 1
- Line 1864: E302 expected 2 blank lines, found 1
- Line 41: Trailing whitespace
- Line 49: Trailing whitespace
- Line 52: Trailing whitespace
- Line 491: Trailing whitespace
- Line 1825: Trailing whitespace
- Line 1834: Trailing whitespace
- Line 1839: Trailing whitespace
- Line 1851: Trailing whitespace
- Line 1853: Trailing whitespace
- Line 1857: Trailing whitespace

### src/piwardrive/diagnostics.py
- Line 97: E226 missing whitespace around arithmetic operator
- Line 114: E501 line too long (85 > 79 characters)
- Line 134: E226 missing whitespace around arithmetic operator
- Line 166: E501 line too long (84 > 79 characters)
- Line 210: E501 line too long (82 > 79 characters)
- Line 225: E501 line too long (84 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 334: E501 line too long (82 > 79 characters)
- Line 347: E501 line too long (84 > 79 characters)
- Line 349: E501 line too long (88 > 79 characters)
- Line 353: E501 line too long (83 > 79 characters)
- Line 439: E501 line too long (84 > 79 characters)
- Line 445: E501 line too long (81 > 79 characters)
- Line 456: E501 line too long (85 > 79 characters)
- Line 463: E501 line too long (81 > 79 characters)
- Line 470: E501 line too long (87 > 79 characters)
- Line 271: Trailing whitespace

### scripts/dependency_audit.py
- Line 30: E501 line too long (85 > 79 characters)
- Line 114: E501 line too long (88 > 79 characters)
- Line 173: E501 line too long (87 > 79 characters)
- Line 211: E501 line too long (86 > 79 characters)
- Line 228: E501 line too long (83 > 79 characters)
- Line 276: E501 line too long (86 > 79 characters)
- Line 285: E501 line too long (88 > 79 characters)
- Line 311: E501 line too long (102 > 79 characters)
- Line 312: E501 line too long (122 > 79 characters)
- Line 321: E501 line too long (80 > 79 characters)
- Line 364: E501 line too long (81 > 79 characters)
- Line 420: E501 line too long (87 > 79 characters)
- Line 440: E501 line too long (84 > 79 characters)
- Line 445: E501 line too long (82 > 79 characters)
- Line 452: E501 line too long (87 > 79 characters)
- Line 453: E501 line too long (87 > 79 characters)
- Line 312: Line too long (122 > 120 characters)

### comprehensive_code_analyzer.py
- Line 4: E501 line too long (99 > 79 characters)
- Line 16: E302 expected 2 blank lines, found 1
- Line 20: W293 blank line contains whitespace
- Line 30: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 53: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 59: E501 line too long (80 > 79 characters)
- Line 61: E501 line too long (87 > 79 characters)
- Line 63: E501 line too long (83 > 79 characters)
- Line 64: E501 line too long (91 > 79 characters)
- Line 65: W293 blank line contains whitespace
- Line 68: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 75: W293 blank line contains whitespace
- Line 85: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 95: W293 blank line contains whitespace
- Line 100: E501 line too long (82 > 79 characters)
- Line 102: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 116: W293 blank line contains whitespace
- Line 122: E501 line too long (106 > 79 characters)
- Line 125: E501 line too long (99 > 79 characters)
- Line 126: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 132: W293 blank line contains whitespace
- Line 138: E501 line too long (90 > 79 characters)
- Line 142: W293 blank line contains whitespace
- Line 144: E501 line too long (127 > 79 characters)
- Line 145: W293 blank line contains whitespace
- Line 148: E501 line too long (115 > 79 characters)
- Line 149: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 160: E501 line too long (84 > 79 characters)
- Line 161: E501 line too long (94 > 79 characters)
- Line 163: E501 line too long (87 > 79 characters)
- Line 164: E501 line too long (80 > 79 characters)
- Line 165: E501 line too long (88 > 79 characters)
- Line 167: W293 blank line contains whitespace
- Line 172: W293 blank line contains whitespace
- Line 174: W293 blank line contains whitespace
- Line 179: W293 blank line contains whitespace
- Line 181: E501 line too long (100 > 79 characters)
- Line 182: E501 line too long (106 > 79 characters)
- Line 183: E501 line too long (107 > 79 characters)
- Line 184: E501 line too long (96 > 79 characters)
- Line 187: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 203: E501 line too long (88 > 79 characters)
- Line 204: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 210: E501 line too long (80 > 79 characters)
- Line 213: E501 line too long (93 > 79 characters)
- Line 214: W293 blank line contains whitespace
- Line 216: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 223: W293 blank line contains whitespace
- Line 228: E501 line too long (109 > 79 characters)
- Line 230: W293 blank line contains whitespace
- Line 233: W293 blank line contains whitespace
- Line 235: W293 blank line contains whitespace
- Line 239: W293 blank line contains whitespace
- Line 241: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 248: W293 blank line contains whitespace
- Line 252: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 265: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 297: E302 expected 2 blank lines, found 1
- Line 299: W293 blank line contains whitespace
- Line 308: W293 blank line contains whitespace
- Line 316: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 336: W293 blank line contains whitespace
- Line 344: E302 expected 2 blank lines, found 1
- Line 349: W293 blank line contains whitespace
- Line 354: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 359: E501 line too long (111 > 79 characters)
- Line 362: E305 expected 2 blank lines after class or function definition, found 1
- Line 20: Trailing whitespace
- Line 30: Trailing whitespace
- Line 43: Trailing whitespace
- Line 47: Trailing whitespace
- Line 49: Trailing whitespace
- Line 53: Trailing whitespace
- Line 57: Trailing whitespace
- Line 65: Trailing whitespace
- Line 68: Trailing whitespace
- Line 70: Trailing whitespace
- Line 75: Trailing whitespace
- Line 85: Trailing whitespace
- Line 91: Trailing whitespace
- Line 95: Trailing whitespace
- Line 102: Trailing whitespace
- Line 104: Trailing whitespace
- Line 112: Trailing whitespace
- Line 116: Trailing whitespace
- Line 126: Trailing whitespace
- Line 128: Trailing whitespace
- Line 132: Trailing whitespace
- Line 142: Trailing whitespace
- Line 144: Line too long (127 > 120 characters)
- Line 145: Trailing whitespace
- Line 149: Trailing whitespace
- Line 151: Trailing whitespace
- Line 156: Trailing whitespace
- Line 167: Trailing whitespace
- Line 172: Trailing whitespace
- Line 174: Trailing whitespace
- Line 179: Trailing whitespace
- Line 187: Trailing whitespace
- Line 192: Trailing whitespace
- Line 194: Trailing whitespace
- Line 199: Trailing whitespace
- Line 204: Trailing whitespace
- Line 208: Trailing whitespace
- Line 214: Trailing whitespace
- Line 216: Trailing whitespace
- Line 220: Trailing whitespace
- Line 223: Trailing whitespace
- Line 230: Trailing whitespace
- Line 233: Trailing whitespace
- Line 235: Trailing whitespace
- Line 239: Trailing whitespace
- Line 241: Trailing whitespace
- Line 246: Trailing whitespace
- Line 248: Trailing whitespace
- Line 252: Trailing whitespace
- Line 258: Trailing whitespace
- Line 265: Trailing whitespace
- Line 277: Trailing whitespace
- Line 281: Trailing whitespace
- Line 290: Trailing whitespace
- Line 294: Trailing whitespace
- Line 299: Trailing whitespace
- Line 308: Trailing whitespace
- Line 316: Trailing whitespace
- Line 324: Trailing whitespace
- Line 329: Trailing whitespace
- Line 336: Trailing whitespace
- Line 349: Trailing whitespace
- Line 354: Trailing whitespace
- Line 356: Trailing whitespace

### tests/test_analysis_queries_cache.py
- Line 7: E402 module level import not at top of file

### src/piwardrive/db/manager.py
- Line 42: E501 line too long (84 > 79 characters)
- Line 63: E501 line too long (87 > 79 characters)
- Line 70: E501 line too long (86 > 79 characters)
- Line 78: E501 line too long (87 > 79 characters)

### src/piwardrive/errors.py
- Line 5: E501 line too long (88 > 79 characters)

### tests/test_migrations_comprehensive.py
- Line 19: W293 blank line contains whitespace
- Line 26: W293 blank line contains whitespace
- Line 32: W293 blank line contains whitespace
- Line 37: W293 blank line contains whitespace
- Line 40: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 66: W293 blank line contains whitespace
- Line 69: E501 line too long (92 > 79 characters)
- Line 74: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 82: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 113: E501 line too long (92 > 79 characters)
- Line 117: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 123: E501 line too long (92 > 79 characters)
- Line 131: W293 blank line contains whitespace
- Line 136: W293 blank line contains whitespace
- Line 141: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 147: E501 line too long (99 > 79 characters)
- Line 152: W293 blank line contains whitespace
- Line 157: W293 blank line contains whitespace
- Line 160: W293 blank line contains whitespace
- Line 162: E501 line too long (82 > 79 characters)
- Line 164: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 186: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 197: E501 line too long (89 > 79 characters)
- Line 202: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 217: W293 blank line contains whitespace
- Line 232: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 242: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 265: W293 blank line contains whitespace
- Line 268: E501 line too long (89 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 279: W293 blank line contains whitespace
- Line 289: W293 blank line contains whitespace
- Line 292: W293 blank line contains whitespace
- Line 295: E501 line too long (89 > 79 characters)
- Line 299: W293 blank line contains whitespace
- Line 302: W293 blank line contains whitespace
- Line 305: E501 line too long (89 > 79 characters)
- Line 313: W293 blank line contains whitespace
- Line 319: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 330: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 336: W293 blank line contains whitespace
- Line 341: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 348: W293 blank line contains whitespace
- Line 351: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 359: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 367: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 377: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 385: W293 blank line contains whitespace
- Line 388: W293 blank line contains whitespace
- Line 390: W293 blank line contains whitespace
- Line 393: W293 blank line contains whitespace
- Line 398: W293 blank line contains whitespace
- Line 405: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 413: E501 line too long (91 > 79 characters)
- Line 414: W293 blank line contains whitespace
- Line 416: W293 blank line contains whitespace
- Line 423: W293 blank line contains whitespace
- Line 430: W293 blank line contains whitespace
- Line 433: W293 blank line contains whitespace
- Line 437: W293 blank line contains whitespace
- Line 441: W293 blank line contains whitespace
- Line 445: E501 line too long (96 > 79 characters)
- Line 449: W293 blank line contains whitespace
- Line 453: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 462: W293 blank line contains whitespace
- Line 466: W293 blank line contains whitespace
- Line 470: W293 blank line contains whitespace
- Line 473: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 482: W293 blank line contains whitespace
- Line 486: W293 blank line contains whitespace
- Line 490: E501 line too long (96 > 79 characters)
- Line 494: W293 blank line contains whitespace
- Line 497: W293 blank line contains whitespace
- Line 501: E501 line too long (96 > 79 characters)
- Line 505: W293 blank line contains whitespace
- Line 512: W293 blank line contains whitespace
- Line 517: W293 blank line contains whitespace
- Line 521: W293 blank line contains whitespace
- Line 524: W293 blank line contains whitespace
- Line 529: W293 blank line contains whitespace
- Line 533: W293 blank line contains whitespace
- Line 536: W293 blank line contains whitespace
- Line 541: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 549: W293 blank line contains whitespace
- Line 554: W293 blank line contains whitespace
- Line 561: W293 blank line contains whitespace
- Line 566: W293 blank line contains whitespace
- Line 576: W293 blank line contains whitespace
- Line 579: W291 trailing whitespace
- Line 582: W293 blank line contains whitespace
- Line 585: W293 blank line contains whitespace
- Line 588: E501 line too long (81 > 79 characters)
- Line 592: W293 blank line contains whitespace
- Line 597: W293 blank line contains whitespace
- Line 601: W293 blank line contains whitespace
- Line 607: W293 blank line contains whitespace
- Line 609: E501 line too long (103 > 79 characters)
- Line 612: W293 blank line contains whitespace
- Line 19: Trailing whitespace
- Line 26: Trailing whitespace
- Line 32: Trailing whitespace
- Line 37: Trailing whitespace
- Line 40: Trailing whitespace
- Line 45: Trailing whitespace
- Line 52: Trailing whitespace
- Line 57: Trailing whitespace
- Line 62: Trailing whitespace
- Line 66: Trailing whitespace
- Line 74: Trailing whitespace
- Line 79: Trailing whitespace
- Line 82: Trailing whitespace
- Line 86: Trailing whitespace
- Line 89: Trailing whitespace
- Line 101: Trailing whitespace
- Line 106: Trailing whitespace
- Line 110: Trailing whitespace
- Line 117: Trailing whitespace
- Line 120: Trailing whitespace
- Line 131: Trailing whitespace
- Line 136: Trailing whitespace
- Line 141: Trailing whitespace
- Line 144: Trailing whitespace
- Line 152: Trailing whitespace
- Line 157: Trailing whitespace
- Line 160: Trailing whitespace
- Line 164: Trailing whitespace
- Line 167: Trailing whitespace
- Line 181: Trailing whitespace
- Line 186: Trailing whitespace
- Line 191: Trailing whitespace
- Line 194: Trailing whitespace
- Line 202: Trailing whitespace
- Line 207: Trailing whitespace
- Line 210: Trailing whitespace
- Line 214: Trailing whitespace
- Line 217: Trailing whitespace
- Line 232: Trailing whitespace
- Line 237: Trailing whitespace
- Line 242: Trailing whitespace
- Line 262: Trailing whitespace
- Line 265: Trailing whitespace
- Line 271: Trailing whitespace
- Line 274: Trailing whitespace
- Line 279: Trailing whitespace
- Line 289: Trailing whitespace
- Line 292: Trailing whitespace
- Line 299: Trailing whitespace
- Line 302: Trailing whitespace
- Line 313: Trailing whitespace
- Line 319: Trailing whitespace
- Line 324: Trailing whitespace
- Line 330: Trailing whitespace
- Line 333: Trailing whitespace
- Line 336: Trailing whitespace
- Line 341: Trailing whitespace
- Line 345: Trailing whitespace
- Line 348: Trailing whitespace
- Line 351: Trailing whitespace
- Line 356: Trailing whitespace
- Line 359: Trailing whitespace
- Line 364: Trailing whitespace
- Line 367: Trailing whitespace
- Line 369: Trailing whitespace
- Line 372: Trailing whitespace
- Line 377: Trailing whitespace
- Line 380: Trailing whitespace
- Line 385: Trailing whitespace
- Line 388: Trailing whitespace
- Line 390: Trailing whitespace
- Line 393: Trailing whitespace
- Line 398: Trailing whitespace
- Line 405: Trailing whitespace
- Line 410: Trailing whitespace
- Line 414: Trailing whitespace
- Line 416: Trailing whitespace
- Line 423: Trailing whitespace
- Line 430: Trailing whitespace
- Line 433: Trailing whitespace
- Line 437: Trailing whitespace
- Line 441: Trailing whitespace
- Line 449: Trailing whitespace
- Line 453: Trailing whitespace
- Line 459: Trailing whitespace
- Line 462: Trailing whitespace
- Line 466: Trailing whitespace
- Line 470: Trailing whitespace
- Line 473: Trailing whitespace
- Line 479: Trailing whitespace
- Line 482: Trailing whitespace
- Line 486: Trailing whitespace
- Line 494: Trailing whitespace
- Line 497: Trailing whitespace
- Line 505: Trailing whitespace
- Line 512: Trailing whitespace
- Line 517: Trailing whitespace
- Line 521: Trailing whitespace
- Line 524: Trailing whitespace
- Line 529: Trailing whitespace
- Line 533: Trailing whitespace
- Line 536: Trailing whitespace
- Line 541: Trailing whitespace
- Line 544: Trailing whitespace
- Line 549: Trailing whitespace
- Line 554: Trailing whitespace
- Line 561: Trailing whitespace
- Line 566: Trailing whitespace
- Line 576: Trailing whitespace
- Line 579: Trailing whitespace
- Line 582: Trailing whitespace
- Line 585: Trailing whitespace
- Line 592: Trailing whitespace
- Line 597: Trailing whitespace
- Line 601: Trailing whitespace
- Line 607: Trailing whitespace
- Line 612: Trailing whitespace

### scripts/compare_performance.py
- Line 21: E501 line too long (86 > 79 characters)
- Line 58: E501 line too long (85 > 79 characters)
- Line 76: E501 line too long (85 > 79 characters)
- Line 85: E501 line too long (81 > 79 characters)
- Line 94: W503 line break before binary operator
- Line 95: W503 line break before binary operator
- Line 97: E501 line too long (82 > 79 characters)
- Line 98: E501 line too long (84 > 79 characters)
- Line 102: E501 line too long (80 > 79 characters)
- Line 107: E501 line too long (84 > 79 characters)
- Line 112: W503 line break before binary operator
- Line 113: W503 line break before binary operator
- Line 114: W503 line break before binary operator
- Line 115: W503 line break before binary operator
- Line 116: W503 line break before binary operator
- Line 130: E501 line too long (81 > 79 characters)
- Line 146: E501 line too long (84 > 79 characters)
- Line 148: E501 line too long (84 > 79 characters)
- Line 151: E501 line too long (80 > 79 characters)
- Line 153: E501 line too long (87 > 79 characters)
- Line 155: E501 line too long (85 > 79 characters)
- Line 158: E501 line too long (80 > 79 characters)
- Line 160: E501 line too long (87 > 79 characters)
- Line 162: E501 line too long (85 > 79 characters)
- Line 175: E501 line too long (87 > 79 characters)
- Line 177: E501 line too long (83 > 79 characters)
- Line 184: E501 line too long (84 > 79 characters)
- Line 195: E501 line too long (82 > 79 characters)
- Line 201: E501 line too long (86 > 79 characters)
- Line 204: E501 line too long (88 > 79 characters)
- Line 235: E501 line too long (137 > 79 characters)
- Line 239: E501 line too long (143 > 79 characters)
- Line 243: E501 line too long (106 > 79 characters)
- Line 259: E501 line too long (131 > 79 characters)
- Line 263: E501 line too long (137 > 79 characters)
- Line 267: E501 line too long (100 > 79 characters)
- Line 273: E501 line too long (81 > 79 characters)
- Line 291: E501 line too long (136 > 79 characters)
- Line 295: E501 line too long (142 > 79 characters)
- Line 299: E501 line too long (105 > 79 characters)
- Line 308: E501 line too long (87 > 79 characters)
- Line 313: E501 line too long (133 > 79 characters)
- Line 317: E501 line too long (139 > 79 characters)
- Line 321: E501 line too long (102 > 79 characters)
- Line 330: E501 line too long (87 > 79 characters)
- Line 335: E501 line too long (133 > 79 characters)
- Line 339: E501 line too long (139 > 79 characters)
- Line 343: E501 line too long (102 > 79 characters)
- Line 376: E501 line too long (154 > 79 characters)
- Line 380: E501 line too long (160 > 79 characters)
- Line 384: E501 line too long (123 > 79 characters)
- Line 398: E501 line too long (87 > 79 characters)
- Line 413: E501 line too long (83 > 79 characters)
- Line 414: E501 line too long (84 > 79 characters)
- Line 415: E501 line too long (86 > 79 characters)
- Line 416: E501 line too long (81 > 79 characters)
- Line 470: E501 line too long (82 > 79 characters)
- Line 500: E501 line too long (109 > 79 characters)
- Line 505: E501 line too long (113 > 79 characters)
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

### src/piwardrive/api/websockets/handlers.py
- Line 33: E501 line too long (88 > 79 characters)
- Line 45: E501 line too long (85 > 79 characters)
- Line 110: E501 line too long (85 > 79 characters)

### tests/models/test_api_models.py
- Line 20: E402 module level import not at top of file
- Line 60: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 102: E501 line too long (86 > 79 characters)
- Line 117: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 268: W293 blank line contains whitespace
- Line 382: W293 blank line contains whitespace
- Line 388: W293 blank line contains whitespace
- Line 398: W293 blank line contains whitespace
- Line 411: W293 blank line contains whitespace
- Line 419: W293 blank line contains whitespace
- Line 435: W293 blank line contains whitespace
- Line 447: W293 blank line contains whitespace
- Line 451: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 468: E501 line too long (104 > 79 characters)
- Line 469: E501 line too long (118 > 79 characters)
- Line 470: E501 line too long (130 > 79 characters)
- Line 60: Trailing whitespace
- Line 77: Trailing whitespace
- Line 117: Trailing whitespace
- Line 163: Trailing whitespace
- Line 218: Trailing whitespace
- Line 254: Trailing whitespace
- Line 268: Trailing whitespace
- Line 382: Trailing whitespace
- Line 388: Trailing whitespace
- Line 398: Trailing whitespace
- Line 411: Trailing whitespace
- Line 419: Trailing whitespace
- Line 435: Trailing whitespace
- Line 447: Trailing whitespace
- Line 451: Trailing whitespace
- Line 467: Trailing whitespace
- Line 470: Line too long (130 > 120 characters)

### src/piwardrive/di.py
- Line 24: E501 line too long (82 > 79 characters)

### src/piwardrive/services/analysis_queries.py
- Line 25: E501 line too long (84 > 79 characters)
- Line 49: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 95: W293 blank line contains whitespace
- Line 115: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 137: E501 line too long (83 > 79 characters)
- Line 49: Trailing whitespace
- Line 71: Trailing whitespace
- Line 95: Trailing whitespace
- Line 115: Trailing whitespace
- Line 135: Trailing whitespace

### fix_syntax_errors.py
- Line 11: E302 expected 2 blank lines, found 1
- Line 16: W293 blank line contains whitespace
- Line 18: W293 blank line contains whitespace
- Line 23: E501 line too long (90 > 79 characters)
- Line 23: W291 trailing whitespace
- Line 25: W293 blank line contains whitespace
- Line 29: W293 blank line contains whitespace
- Line 32: W293 blank line contains whitespace
- Line 39: W293 blank line contains whitespace
- Line 45: E302 expected 2 blank lines, found 1
- Line 50: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 54: E501 line too long (85 > 79 characters)
- Line 56: E226 missing whitespace around arithmetic operator
- Line 60: W293 blank line contains whitespace
- Line 62: E501 line too long (94 > 79 characters)
- Line 65: E226 missing whitespace around arithmetic operator
- Line 66: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 77: E302 expected 2 blank lines, found 1
- Line 80: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 87: E302 expected 2 blank lines, found 1
- Line 92: W293 blank line contains whitespace
- Line 94: E501 line too long (129 > 79 characters)
- Line 95: E501 line too long (125 > 79 characters)
- Line 96: W293 blank line contains whitespace
- Line 97: E501 line too long (100 > 79 characters)
- Line 98: W293 blank line contains whitespace
- Line 99: E501 line too long (111 > 79 characters)
- Line 100: E501 line too long (110 > 79 characters)
- Line 101: W293 blank line contains whitespace
- Line 102: E501 line too long (102 > 79 characters)
- Line 103: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 114: E302 expected 2 blank lines, found 1
- Line 117: W293 blank line contains whitespace
- Line 145: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 150: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 163: W293 blank line contains whitespace
- Line 167: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 174: W293 blank line contains whitespace
- Line 184: W293 blank line contains whitespace
- Line 187: E305 expected 2 blank lines after class or function definition, found 1
- Line 16: Trailing whitespace
- Line 18: Trailing whitespace
- Line 23: Trailing whitespace
- Line 25: Trailing whitespace
- Line 29: Trailing whitespace
- Line 32: Trailing whitespace
- Line 39: Trailing whitespace
- Line 50: Trailing whitespace
- Line 52: Trailing whitespace
- Line 60: Trailing whitespace
- Line 66: Trailing whitespace
- Line 71: Trailing whitespace
- Line 80: Trailing whitespace
- Line 84: Trailing whitespace
- Line 92: Trailing whitespace
- Line 94: Line too long (129 > 120 characters)
- Line 95: Line too long (125 > 120 characters)
- Line 96: Trailing whitespace
- Line 98: Trailing whitespace
- Line 101: Trailing whitespace
- Line 103: Trailing whitespace
- Line 106: Trailing whitespace
- Line 109: Trailing whitespace
- Line 117: Trailing whitespace
- Line 145: Trailing whitespace
- Line 147: Trailing whitespace
- Line 150: Trailing whitespace
- Line 154: Trailing whitespace
- Line 156: Trailing whitespace
- Line 159: Trailing whitespace
- Line 163: Trailing whitespace
- Line 167: Trailing whitespace
- Line 171: Trailing whitespace
- Line 174: Trailing whitespace
- Line 184: Trailing whitespace

### src/piwardrive/integrations/sigint_suite/cellular/tower_tracker/tracker.py
- Line 89: E501 line too long (84 > 79 characters)
- Line 112: E501 line too long (80 > 79 characters)
- Line 128: E501 line too long (84 > 79 characters)
- Line 155: E501 line too long (80 > 79 characters)
- Line 233: E501 line too long (83 > 79 characters)
- Line 241: E501 line too long (82 > 79 characters)

### tests/test_remote_sync_pkg.py
- Line 19: E402 module level import not at top of file
- Line 56: E501 line too long (85 > 79 characters)
- Line 95: E501 line too long (84 > 79 characters)
- Line 103: E501 line too long (81 > 79 characters)
- Line 137: E501 line too long (81 > 79 characters)
- Line 151: E501 line too long (81 > 79 characters)

### tests/test_main_application_fixed.py
- Line 3: E501 line too long (80 > 79 characters)
- Line 17: W293 blank line contains whitespace
- Line 23: W293 blank line contains whitespace
- Line 32: E501 line too long (98 > 79 characters)
- Line 33: E128 continuation line under-indented for visual indent
- Line 33: W291 trailing whitespace
- Line 34: E128 continuation line under-indented for visual indent
- Line 34: W291 trailing whitespace
- Line 35: E128 continuation line under-indented for visual indent
- Line 40: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 54: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 61: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 75: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 101: E501 line too long (87 > 79 characters)
- Line 101: W291 trailing whitespace
- Line 102: E128 continuation line under-indented for visual indent
- Line 102: E501 line too long (81 > 79 characters)
- Line 103: E128 continuation line under-indented for visual indent
- Line 103: E501 line too long (80 > 79 characters)
- Line 103: W291 trailing whitespace
- Line 104: E128 continuation line under-indented for visual indent
- Line 104: E501 line too long (90 > 79 characters)
- Line 109: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 126: W293 blank line contains whitespace
- Line 130: W293 blank line contains whitespace
- Line 134: W293 blank line contains whitespace
- Line 137: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 142: E501 line too long (89 > 79 characters)
- Line 144: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 157: E501 line too long (81 > 79 characters)
- Line 158: E128 continuation line under-indented for visual indent
- Line 159: E128 continuation line under-indented for visual indent
- Line 159: W291 trailing whitespace
- Line 160: E128 continuation line under-indented for visual indent
- Line 166: W293 blank line contains whitespace
- Line 177: W293 blank line contains whitespace
- Line 180: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 187: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 197: W293 blank line contains whitespace
- Line 201: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 212: W293 blank line contains whitespace
- Line 216: E501 line too long (80 > 79 characters)
- Line 220: E501 line too long (88 > 79 characters)
- Line 222: E501 line too long (92 > 79 characters)
- Line 232: E501 line too long (91 > 79 characters)
- Line 233: W293 blank line contains whitespace
- Line 236: W293 blank line contains whitespace
- Line 237: E501 line too long (83 > 79 characters)
- Line 238: E501 line too long (89 > 79 characters)
- Line 239: W293 blank line contains whitespace
- Line 240: E501 line too long (108 > 79 characters)
- Line 241: E501 line too long (107 > 79 characters)
- Line 242: W293 blank line contains whitespace
- Line 243: E501 line too long (86 > 79 characters)
- Line 244: E501 line too long (94 > 79 characters)
- Line 249: W293 blank line contains whitespace
- Line 257: W293 blank line contains whitespace
- Line 261: W293 blank line contains whitespace
- Line 268: W293 blank line contains whitespace
- Line 272: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 286: E501 line too long (85 > 79 characters)
- Line 287: E128 continuation line under-indented for visual indent
- Line 291: W293 blank line contains whitespace
- Line 302: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 309: W293 blank line contains whitespace
- Line 313: W293 blank line contains whitespace
- Line 317: W293 blank line contains whitespace
- Line 322: E501 line too long (80 > 79 characters)
- Line 323: E501 line too long (92 > 79 characters)
- Line 326: W293 blank line contains whitespace
- Line 331: W293 blank line contains whitespace
- Line 335: W293 blank line contains whitespace
- Line 338: E501 line too long (85 > 79 characters)
- Line 342: W293 blank line contains whitespace
- Line 353: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 359: W293 blank line contains whitespace
- Line 363: W293 blank line contains whitespace
- Line 367: E501 line too long (80 > 79 characters)
- Line 368: E501 line too long (96 > 79 characters)
- Line 369: E501 line too long (96 > 79 characters)
- Line 372: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 385: W293 blank line contains whitespace
- Line 387: E501 line too long (85 > 79 characters)
- Line 390: W293 blank line contains whitespace
- Line 401: W293 blank line contains whitespace
- Line 404: E501 line too long (85 > 79 characters)
- Line 408: W293 blank line contains whitespace
- Line 418: W293 blank line contains whitespace
- Line 421: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 429: E501 line too long (80 > 79 characters)
- Line 430: E501 line too long (106 > 79 characters)
- Line 431: E501 line too long (82 > 79 characters)
- Line 432: E501 line too long (100 > 79 characters)
- Line 435: W293 blank line contains whitespace
- Line 436: E501 line too long (81 > 79 characters)
- Line 437: E501 line too long (112 > 79 characters)
- Line 438: W293 blank line contains whitespace
- Line 439: E501 line too long (80 > 79 characters)
- Line 442: W293 blank line contains whitespace
- Line 448: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 462: W293 blank line contains whitespace
- Line 464: E501 line too long (86 > 79 characters)
- Line 468: E501 line too long (88 > 79 characters)
- Line 469: E501 line too long (98 > 79 characters)
- Line 470: E501 line too long (90 > 79 characters)
- Line 471: E501 line too long (116 > 79 characters)
- Line 473: W293 blank line contains whitespace
- Line 475: E501 line too long (97 > 79 characters)
- Line 17: Trailing whitespace
- Line 23: Trailing whitespace
- Line 33: Trailing whitespace
- Line 34: Trailing whitespace
- Line 40: Trailing whitespace
- Line 51: Trailing whitespace
- Line 54: Trailing whitespace
- Line 57: Trailing whitespace
- Line 61: Trailing whitespace
- Line 65: Trailing whitespace
- Line 73: Trailing whitespace
- Line 75: Trailing whitespace
- Line 79: Trailing whitespace
- Line 86: Trailing whitespace
- Line 91: Trailing whitespace
- Line 101: Trailing whitespace
- Line 103: Trailing whitespace
- Line 109: Trailing whitespace
- Line 120: Trailing whitespace
- Line 123: Trailing whitespace
- Line 126: Trailing whitespace
- Line 130: Trailing whitespace
- Line 134: Trailing whitespace
- Line 137: Trailing whitespace
- Line 140: Trailing whitespace
- Line 144: Trailing whitespace
- Line 148: Trailing whitespace
- Line 159: Trailing whitespace
- Line 166: Trailing whitespace
- Line 177: Trailing whitespace
- Line 180: Trailing whitespace
- Line 183: Trailing whitespace
- Line 187: Trailing whitespace
- Line 191: Trailing whitespace
- Line 194: Trailing whitespace
- Line 197: Trailing whitespace
- Line 201: Trailing whitespace
- Line 204: Trailing whitespace
- Line 208: Trailing whitespace
- Line 212: Trailing whitespace
- Line 233: Trailing whitespace
- Line 236: Trailing whitespace
- Line 239: Trailing whitespace
- Line 242: Trailing whitespace
- Line 249: Trailing whitespace
- Line 257: Trailing whitespace
- Line 261: Trailing whitespace
- Line 268: Trailing whitespace
- Line 272: Trailing whitespace
- Line 277: Trailing whitespace
- Line 281: Trailing whitespace
- Line 291: Trailing whitespace
- Line 302: Trailing whitespace
- Line 306: Trailing whitespace
- Line 309: Trailing whitespace
- Line 313: Trailing whitespace
- Line 317: Trailing whitespace
- Line 326: Trailing whitespace
- Line 331: Trailing whitespace
- Line 335: Trailing whitespace
- Line 342: Trailing whitespace
- Line 353: Trailing whitespace
- Line 356: Trailing whitespace
- Line 359: Trailing whitespace
- Line 363: Trailing whitespace
- Line 372: Trailing whitespace
- Line 376: Trailing whitespace
- Line 380: Trailing whitespace
- Line 385: Trailing whitespace
- Line 390: Trailing whitespace
- Line 401: Trailing whitespace
- Line 408: Trailing whitespace
- Line 418: Trailing whitespace
- Line 421: Trailing whitespace
- Line 424: Trailing whitespace
- Line 435: Trailing whitespace
- Line 438: Trailing whitespace
- Line 442: Trailing whitespace
- Line 448: Trailing whitespace
- Line 459: Trailing whitespace
- Line 462: Trailing whitespace
- Line 473: Trailing whitespace

### tests/test_model_trainer.py
- Line 33: E501 line too long (88 > 79 characters)

### tests/test_service_api.py
- Line 29: W293 blank line contains whitespace
- Line 36: E501 line too long (80 > 79 characters)
- Line 37: E501 line too long (85 > 79 characters)
- Line 40: W293 blank line contains whitespace
- Line 42: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 50: E501 line too long (104 > 79 characters)
- Line 53: W293 blank line contains whitespace
- Line 57: E501 line too long (81 > 79 characters)
- Line 62: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 69: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 103: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 115: E501 line too long (85 > 79 characters)
- Line 116: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 126: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 150: W293 blank line contains whitespace
- Line 155: W293 blank line contains whitespace
- Line 164: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 189: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 195: W293 blank line contains whitespace
- Line 200: W293 blank line contains whitespace
- Line 203: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 213: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 221: W293 blank line contains whitespace
- Line 225: W293 blank line contains whitespace
- Line 228: W293 blank line contains whitespace
- Line 235: W293 blank line contains whitespace
- Line 241: E501 line too long (83 > 79 characters)
- Line 242: E501 line too long (85 > 79 characters)
- Line 243: E501 line too long (91 > 79 characters)
- Line 246: W293 blank line contains whitespace
- Line 248: W293 blank line contains whitespace
- Line 253: W293 blank line contains whitespace
- Line 261: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 277: E501 line too long (88 > 79 characters)
- Line 278: W293 blank line contains whitespace
- Line 281: E501 line too long (91 > 79 characters)
- Line 283: W293 blank line contains whitespace
- Line 288: W293 blank line contains whitespace
- Line 293: E501 line too long (91 > 79 characters)
- Line 295: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 315: W293 blank line contains whitespace
- Line 320: E501 line too long (80 > 79 characters)
- Line 327: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 334: W293 blank line contains whitespace
- Line 339: E501 line too long (85 > 79 characters)
- Line 342: W293 blank line contains whitespace
- Line 348: W293 blank line contains whitespace
- Line 358: W293 blank line contains whitespace
- Line 363: W293 blank line contains whitespace
- Line 368: W293 blank line contains whitespace
- Line 373: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 384: W293 blank line contains whitespace
- Line 393: W293 blank line contains whitespace
- Line 404: W293 blank line contains whitespace
- Line 406: W293 blank line contains whitespace
- Line 409: E501 line too long (88 > 79 characters)
- Line 410: W293 blank line contains whitespace
- Line 413: W293 blank line contains whitespace
- Line 416: E501 line too long (86 > 79 characters)
- Line 417: W293 blank line contains whitespace
- Line 421: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 430: W293 blank line contains whitespace
- Line 433: W293 blank line contains whitespace
- Line 440: W293 blank line contains whitespace
- Line 442: W293 blank line contains whitespace
- Line 453: W293 blank line contains whitespace
- Line 29: Trailing whitespace
- Line 40: Trailing whitespace
- Line 42: Trailing whitespace
- Line 47: Trailing whitespace
- Line 53: Trailing whitespace
- Line 62: Trailing whitespace
- Line 65: Trailing whitespace
- Line 69: Trailing whitespace
- Line 72: Trailing whitespace
- Line 79: Trailing whitespace
- Line 84: Trailing whitespace
- Line 89: Trailing whitespace
- Line 98: Trailing whitespace
- Line 101: Trailing whitespace
- Line 103: Trailing whitespace
- Line 111: Trailing whitespace
- Line 116: Trailing whitespace
- Line 120: Trailing whitespace
- Line 126: Trailing whitespace
- Line 131: Trailing whitespace
- Line 135: Trailing whitespace
- Line 140: Trailing whitespace
- Line 144: Trailing whitespace
- Line 150: Trailing whitespace
- Line 155: Trailing whitespace
- Line 164: Trailing whitespace
- Line 169: Trailing whitespace
- Line 176: Trailing whitespace
- Line 185: Trailing whitespace
- Line 189: Trailing whitespace
- Line 192: Trailing whitespace
- Line 195: Trailing whitespace
- Line 200: Trailing whitespace
- Line 203: Trailing whitespace
- Line 207: Trailing whitespace
- Line 210: Trailing whitespace
- Line 213: Trailing whitespace
- Line 218: Trailing whitespace
- Line 221: Trailing whitespace
- Line 225: Trailing whitespace
- Line 228: Trailing whitespace
- Line 235: Trailing whitespace
- Line 246: Trailing whitespace
- Line 248: Trailing whitespace
- Line 253: Trailing whitespace
- Line 261: Trailing whitespace
- Line 267: Trailing whitespace
- Line 274: Trailing whitespace
- Line 278: Trailing whitespace
- Line 283: Trailing whitespace
- Line 288: Trailing whitespace
- Line 295: Trailing whitespace
- Line 297: Trailing whitespace
- Line 305: Trailing whitespace
- Line 315: Trailing whitespace
- Line 327: Trailing whitespace
- Line 329: Trailing whitespace
- Line 334: Trailing whitespace
- Line 342: Trailing whitespace
- Line 348: Trailing whitespace
- Line 358: Trailing whitespace
- Line 363: Trailing whitespace
- Line 368: Trailing whitespace
- Line 373: Trailing whitespace
- Line 376: Trailing whitespace
- Line 381: Trailing whitespace
- Line 384: Trailing whitespace
- Line 393: Trailing whitespace
- Line 404: Trailing whitespace
- Line 406: Trailing whitespace
- Line 410: Trailing whitespace
- Line 413: Trailing whitespace
- Line 417: Trailing whitespace
- Line 421: Trailing whitespace
- Line 424: Trailing whitespace
- Line 428: Trailing whitespace
- Line 430: Trailing whitespace
- Line 433: Trailing whitespace
- Line 440: Trailing whitespace
- Line 442: Trailing whitespace
- Line 453: Trailing whitespace

### tests/test_wigle_integration.py
- Line 52: E501 line too long (87 > 79 characters)
- Line 78: E501 line too long (83 > 79 characters)

### src/piwardrive/gpsd_client_async.py
- Line 16: E501 line too long (81 > 79 characters)
- Line 18: W293 blank line contains whitespace
- Line 83: E501 line too long (83 > 79 characters)
- Line 103: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 135: W291 trailing whitespace
- Line 18: Trailing whitespace
- Line 103: Trailing whitespace
- Line 118: Trailing whitespace
- Line 133: Trailing whitespace
- Line 135: Trailing whitespace

### src/piwardrive/api/health/endpoints.py
- Line 14: E501 line too long (87 > 79 characters)
- Line 51: E501 line too long (80 > 79 characters)
- Line 78: E501 line too long (85 > 79 characters)

### src/piwardrive/scheduler.py
- Line 82: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 135: E501 line too long (80 > 79 characters)
- Line 148: E501 line too long (82 > 79 characters)
- Line 149: E501 line too long (81 > 79 characters)
- Line 199: E501 line too long (88 > 79 characters)
- Line 217: E501 line too long (80 > 79 characters)
- Line 218: E501 line too long (85 > 79 characters)
- Line 229: E501 line too long (82 > 79 characters)
- Line 230: E501 line too long (84 > 79 characters)
- Line 82: Trailing whitespace
- Line 86: Trailing whitespace

### src/piwardrive/performance/db_optimizer.py
- Line 19: E302 expected 2 blank lines, found 1
- Line 33: E302 expected 2 blank lines, found 1
- Line 47: E501 line too long (88 > 79 characters)
- Line 51: E303 too many blank lines (3)
- Line 62: E501 line too long (85 > 79 characters)
- Line 72: E501 line too long (85 > 79 characters)
- Line 73: E501 line too long (83 > 79 characters)
- Line 74: W503 line break before binary operator
- Line 106: E501 line too long (84 > 79 characters)
- Line 329: E501 line too long (86 > 79 characters)
- Line 342: E203 whitespace before ':'
- Line 355: E501 line too long (84 > 79 characters)
- Line 392: E501 line too long (83 > 79 characters)
- Line 396: E501 line too long (83 > 79 characters)
- Line 411: E302 expected 2 blank lines, found 1
- Line 427: E302 expected 2 blank lines, found 1
- Line 442: E501 line too long (83 > 79 characters)
- Line 460: E501 line too long (85 > 79 characters)
- Line 474: E501 line too long (82 > 79 characters)
- Line 484: E501 line too long (84 > 79 characters)
- Line 486: E501 line too long (86 > 79 characters)

### src/piwardrive/jobs/analytics_jobs.py
- Line 24: E501 line too long (86 > 79 characters)

### src/piwardrive/widgets/device_classification.py
- Line 30: E501 line too long (82 > 79 characters)

### src/piwardrive/exceptions.py
- Line 12: E501 line too long (82 > 79 characters)
- Line 15: W293 blank line contains whitespace
- Line 29: W293 blank line contains whitespace
- Line 40: E501 line too long (82 > 79 characters)
- Line 43: W293 blank line contains whitespace
- Line 55: E501 line too long (82 > 79 characters)
- Line 58: W293 blank line contains whitespace
- Line 15: Trailing whitespace
- Line 29: Trailing whitespace
- Line 43: Trailing whitespace
- Line 58: Trailing whitespace

### src/piwardrive/integrations/sigint_suite/enrichment/oui.py
- Line 76: E402 module level import not at top of file
- Line 152: E501 line too long (86 > 79 characters)
- Line 170: E501 line too long (86 > 79 characters)

### scripts/simple_db_check.py
- Line 15: E302 expected 2 blank lines, found 1
- Line 18: E231 missing whitespace after ','
- Line 18: E231 missing whitespace after ','
- Line 18: E501 line too long (217 > 79 characters)
- Line 18: E231 missing whitespace after ','
- Line 18: E231 missing whitespace after ','
- Line 18: E231 missing whitespace after ','
- Line 18: E231 missing whitespace after ','
- Line 18: E231 missing whitespace after ','
- Line 23: E231 missing whitespace after ','
- Line 23: E501 line too long (94 > 79 characters)
- Line 42: E501 line too long (84 > 79 characters)
- Line 43: E501 line too long (80 > 79 characters)
- Line 47: E501 line too long (94 > 79 characters)
- Line 71: E231 missing whitespace after ','
- Line 71: E501 line too long (175 > 79 characters)
- Line 71: E231 missing whitespace after ','
- Line 74: E501 line too long (90 > 79 characters)
- Line 77: E231 missing whitespace after ','
- Line 77: E501 line too long (96 > 79 characters)
- Line 82: E231 missing whitespace after ','
- Line 82: E501 line too long (181 > 79 characters)
- Line 82: E231 missing whitespace after ','
- Line 85: E501 line too long (93 > 79 characters)
- Line 88: E231 missing whitespace after ','
- Line 88: E501 line too long (101 > 79 characters)
- Line 99: E302 expected 2 blank lines, found 1
- Line 105: E231 missing whitespace after ','
- Line 105: E501 line too long (137 > 79 characters)
- Line 105: E231 missing whitespace after ','
- Line 127: E501 line too long (102 > 79 characters)
- Line 128: E501 line too long (103 > 79 characters)
- Line 18: Line too long (217 > 120 characters)
- Line 71: Line too long (175 > 120 characters)
- Line 82: Line too long (181 > 120 characters)
- Line 105: Line too long (137 > 120 characters)

### tests/test_fastjson.py
- Line 27: W293 blank line contains whitespace
- Line 39: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 51: E501 line too long (89 > 79 characters)
- Line 53: E501 line too long (84 > 79 characters)
- Line 59: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 99: W293 blank line contains whitespace
- Line 101: E501 line too long (80 > 79 characters)
- Line 108: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 181: E501 line too long (87 > 79 characters)
- Line 187: W293 blank line contains whitespace
- Line 189: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 224: E501 line too long (81 > 79 characters)
- Line 228: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 238: E501 line too long (87 > 79 characters)
- Line 244: W293 blank line contains whitespace
- Line 27: Trailing whitespace
- Line 39: Trailing whitespace
- Line 44: Trailing whitespace
- Line 49: Trailing whitespace
- Line 59: Trailing whitespace
- Line 67: Trailing whitespace
- Line 70: Trailing whitespace
- Line 77: Trailing whitespace
- Line 88: Trailing whitespace
- Line 94: Trailing whitespace
- Line 99: Trailing whitespace
- Line 108: Trailing whitespace
- Line 118: Trailing whitespace
- Line 120: Trailing whitespace
- Line 133: Trailing whitespace
- Line 147: Trailing whitespace
- Line 156: Trailing whitespace
- Line 165: Trailing whitespace
- Line 169: Trailing whitespace
- Line 187: Trailing whitespace
- Line 189: Trailing whitespace
- Line 199: Trailing whitespace
- Line 205: Trailing whitespace
- Line 218: Trailing whitespace
- Line 228: Trailing whitespace
- Line 237: Trailing whitespace
- Line 244: Trailing whitespace

### src/piwardrive/api/auth/endpoints.py
- Line 25: E501 line too long (84 > 79 characters)
- Line 37: E501 line too long (82 > 79 characters)

### src/piwardrive/integrations/sigint_suite/paths.py
- Line 18: E501 line too long (81 > 79 characters)
- Line 20: E501 line too long (88 > 79 characters)

### src/piwardrive/analytics/predictive.py
- Line 38: W503 line break before binary operator
- Line 39: W503 line break before binary operator
- Line 39: E501 line too long (80 > 79 characters)

### src/piwardrive/graphql_api.py
- Line 24: W293 blank line contains whitespace
- Line 34: W293 blank line contains whitespace
- Line 35: E501 line too long (81 > 79 characters)
- Line 40: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 24: Trailing whitespace
- Line 34: Trailing whitespace
- Line 40: Trailing whitespace
- Line 44: Trailing whitespace
- Line 55: Trailing whitespace
- Line 58: Trailing whitespace
- Line 71: Trailing whitespace

### src/piwardrive/migrations/004_create_gps_tracks.py
- Line 36: E501 line too long (94 > 79 characters)
- Line 39: E501 line too long (85 > 79 characters)
- Line 42: E501 line too long (99 > 79 characters)

### scripts/tile_maintenance_cli.py
- Line 28: E501 line too long (80 > 79 characters)
- Line 29: E501 line too long (81 > 79 characters)
- Line 62: E501 line too long (80 > 79 characters)

### src/piwardrive/migrations/006_create_network_fingerprints.py
- Line 34: E501 line too long (101 > 79 characters)
- Line 37: E501 line too long (104 > 79 characters)
- Line 40: E501 line too long (112 > 79 characters)
- Line 44: E501 line too long (82 > 79 characters)

### src/piwardrive/services/report_generator.py
- Line 35: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 72: E501 line too long (86 > 79 characters)
- Line 81: E501 line too long (84 > 79 characters)
- Line 35: Trailing whitespace
- Line 38: Trailing whitespace
- Line 65: Trailing whitespace

### src/piwardrive/widgets/gps_status.py
- Line 27: E501 line too long (87 > 79 characters)

### tests/test_service_api_fixed.py
- Line 19: W293 blank line contains whitespace
- Line 23: W293 blank line contains whitespace
- Line 30: W293 blank line contains whitespace
- Line 34: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 50: E501 line too long (88 > 79 characters)
- Line 51: W293 blank line contains whitespace
- Line 54: E501 line too long (91 > 79 characters)
- Line 56: W293 blank line contains whitespace
- Line 61: W293 blank line contains whitespace
- Line 66: E501 line too long (91 > 79 characters)
- Line 68: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 78: E501 line too long (85 > 79 characters)
- Line 79: W293 blank line contains whitespace
- Line 83: E501 line too long (81 > 79 characters)
- Line 87: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 113: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 126: W293 blank line contains whitespace
- Line 130: W293 blank line contains whitespace
- Line 136: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 151: W293 blank line contains whitespace
- Line 160: W293 blank line contains whitespace
- Line 163: E501 line too long (85 > 79 characters)
- Line 169: W293 blank line contains whitespace
- Line 174: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 190: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 227: W293 blank line contains whitespace
- Line 229: W293 blank line contains whitespace
- Line 234: W293 blank line contains whitespace
- Line 241: W293 blank line contains whitespace
- Line 246: W293 blank line contains whitespace
- Line 249: W293 blank line contains whitespace
- Line 255: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 260: W293 blank line contains whitespace
- Line 269: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 281: W293 blank line contains whitespace
- Line 284: W293 blank line contains whitespace
- Line 287: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 302: W293 blank line contains whitespace
- Line 305: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 311: W293 blank line contains whitespace
- Line 318: W293 blank line contains whitespace
- Line 322: W293 blank line contains whitespace
- Line 325: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 337: W293 blank line contains whitespace
- Line 341: W293 blank line contains whitespace
- Line 344: W293 blank line contains whitespace
- Line 349: W293 blank line contains whitespace
- Line 353: W293 blank line contains whitespace
- Line 356: W293 blank line contains whitespace
- Line 360: W293 blank line contains whitespace
- Line 362: W293 blank line contains whitespace
- Line 365: W293 blank line contains whitespace
- Line 370: W293 blank line contains whitespace
- Line 374: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 379: W293 blank line contains whitespace
- Line 382: E501 line too long (80 > 79 characters)
- Line 383: W293 blank line contains whitespace
- Line 386: W293 blank line contains whitespace
- Line 395: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 409: W293 blank line contains whitespace
- Line 416: W293 blank line contains whitespace
- Line 421: W293 blank line contains whitespace
- Line 430: W293 blank line contains whitespace
- Line 434: W293 blank line contains whitespace
- Line 442: W293 blank line contains whitespace
- Line 445: W293 blank line contains whitespace
- Line 451: W293 blank line contains whitespace
- Line 455: W293 blank line contains whitespace
- Line 469: W293 blank line contains whitespace
- Line 472: W293 blank line contains whitespace
- Line 480: W293 blank line contains whitespace
- Line 491: W293 blank line contains whitespace
- Line 493: W293 blank line contains whitespace
- Line 502: W293 blank line contains whitespace
- Line 506: W293 blank line contains whitespace
- Line 514: W293 blank line contains whitespace
- Line 518: W293 blank line contains whitespace
- Line 521: W293 blank line contains whitespace
- Line 526: W293 blank line contains whitespace
- Line 530: W293 blank line contains whitespace
- Line 532: W293 blank line contains whitespace
- Line 537: W293 blank line contains whitespace
- Line 540: E501 line too long (84 > 79 characters)
- Line 541: W293 blank line contains whitespace
- Line 543: W293 blank line contains whitespace
- Line 545: E501 line too long (85 > 79 characters)
- Line 548: W293 blank line contains whitespace
- Line 553: W293 blank line contains whitespace
- Line 557: W293 blank line contains whitespace
- Line 565: W293 blank line contains whitespace
- Line 570: W293 blank line contains whitespace
- Line 573: W293 blank line contains whitespace
- Line 579: E501 line too long (92 > 79 characters)
- Line 586: W293 blank line contains whitespace
- Line 590: W293 blank line contains whitespace
- Line 599: W293 blank line contains whitespace
- Line 606: W293 blank line contains whitespace
- Line 614: W293 blank line contains whitespace
- Line 619: W293 blank line contains whitespace
- Line 623: W293 blank line contains whitespace
- Line 627: W293 blank line contains whitespace
- Line 629: W293 blank line contains whitespace
- Line 634: W293 blank line contains whitespace
- Line 19: Trailing whitespace
- Line 23: Trailing whitespace
- Line 30: Trailing whitespace
- Line 34: Trailing whitespace
- Line 43: Trailing whitespace
- Line 47: Trailing whitespace
- Line 51: Trailing whitespace
- Line 56: Trailing whitespace
- Line 61: Trailing whitespace
- Line 68: Trailing whitespace
- Line 74: Trailing whitespace
- Line 79: Trailing whitespace
- Line 87: Trailing whitespace
- Line 91: Trailing whitespace
- Line 100: Trailing whitespace
- Line 104: Trailing whitespace
- Line 109: Trailing whitespace
- Line 113: Trailing whitespace
- Line 117: Trailing whitespace
- Line 122: Trailing whitespace
- Line 126: Trailing whitespace
- Line 130: Trailing whitespace
- Line 136: Trailing whitespace
- Line 144: Trailing whitespace
- Line 151: Trailing whitespace
- Line 160: Trailing whitespace
- Line 169: Trailing whitespace
- Line 174: Trailing whitespace
- Line 181: Trailing whitespace
- Line 190: Trailing whitespace
- Line 199: Trailing whitespace
- Line 206: Trailing whitespace
- Line 209: Trailing whitespace
- Line 214: Trailing whitespace
- Line 220: Trailing whitespace
- Line 227: Trailing whitespace
- Line 229: Trailing whitespace
- Line 234: Trailing whitespace
- Line 241: Trailing whitespace
- Line 246: Trailing whitespace
- Line 249: Trailing whitespace
- Line 255: Trailing whitespace
- Line 258: Trailing whitespace
- Line 260: Trailing whitespace
- Line 269: Trailing whitespace
- Line 277: Trailing whitespace
- Line 281: Trailing whitespace
- Line 284: Trailing whitespace
- Line 287: Trailing whitespace
- Line 291: Trailing whitespace
- Line 298: Trailing whitespace
- Line 302: Trailing whitespace
- Line 305: Trailing whitespace
- Line 307: Trailing whitespace
- Line 311: Trailing whitespace
- Line 318: Trailing whitespace
- Line 322: Trailing whitespace
- Line 325: Trailing whitespace
- Line 333: Trailing whitespace
- Line 337: Trailing whitespace
- Line 341: Trailing whitespace
- Line 344: Trailing whitespace
- Line 349: Trailing whitespace
- Line 353: Trailing whitespace
- Line 356: Trailing whitespace
- Line 360: Trailing whitespace
- Line 362: Trailing whitespace
- Line 365: Trailing whitespace
- Line 370: Trailing whitespace
- Line 374: Trailing whitespace
- Line 376: Trailing whitespace
- Line 379: Trailing whitespace
- Line 383: Trailing whitespace
- Line 386: Trailing whitespace
- Line 395: Trailing whitespace
- Line 403: Trailing whitespace
- Line 409: Trailing whitespace
- Line 416: Trailing whitespace
- Line 421: Trailing whitespace
- Line 430: Trailing whitespace
- Line 434: Trailing whitespace
- Line 442: Trailing whitespace
- Line 445: Trailing whitespace
- Line 451: Trailing whitespace
- Line 455: Trailing whitespace
- Line 469: Trailing whitespace
- Line 472: Trailing whitespace
- Line 480: Trailing whitespace
- Line 491: Trailing whitespace
- Line 493: Trailing whitespace
- Line 502: Trailing whitespace
- Line 506: Trailing whitespace
- Line 514: Trailing whitespace
- Line 518: Trailing whitespace
- Line 521: Trailing whitespace
- Line 526: Trailing whitespace
- Line 530: Trailing whitespace
- Line 532: Trailing whitespace
- Line 537: Trailing whitespace
- Line 541: Trailing whitespace
- Line 543: Trailing whitespace
- Line 548: Trailing whitespace
- Line 553: Trailing whitespace
- Line 557: Trailing whitespace
- Line 565: Trailing whitespace
- Line 570: Trailing whitespace
- Line 573: Trailing whitespace
- Line 586: Trailing whitespace
- Line 590: Trailing whitespace
- Line 599: Trailing whitespace
- Line 606: Trailing whitespace
- Line 614: Trailing whitespace
- Line 619: Trailing whitespace
- Line 623: Trailing whitespace
- Line 627: Trailing whitespace
- Line 629: Trailing whitespace
- Line 634: Trailing whitespace

### src/piwardrive/services/db_monitor.py
- Line 36: E302 expected 2 blank lines, found 1
- Line 46: E302 expected 2 blank lines, found 1
- Line 47: E501 line too long (81 > 79 characters)
- Line 51: E501 line too long (161 > 79 characters)
- Line 59: E501 line too long (86 > 79 characters)
- Line 51: Line too long (161 > 120 characters)

### src/piwardrive/core/config.py
- Line 49: E501 line too long (81 > 79 characters)
- Line 123: E501 line too long (82 > 79 characters)
- Line 124: E501 line too long (80 > 79 characters)
- Line 125: E501 line too long (80 > 79 characters)
- Line 274: E501 line too long (85 > 79 characters)
- Line 275: E501 line too long (87 > 79 characters)
- Line 276: E501 line too long (83 > 79 characters)
- Line 280: E501 line too long (81 > 79 characters)
- Line 508: E501 line too long (81 > 79 characters)

### src/piwardrive/widgets/heatmap.py
- Line 54: E501 line too long (88 > 79 characters)

### tests/test_service_direct_import.py
- Line 29: E501 line too long (89 > 79 characters)
- Line 29: W291 trailing whitespace
- Line 30: E128 continuation line under-indented for visual indent
- Line 30: W291 trailing whitespace
- Line 31: E128 continuation line under-indented for visual indent
- Line 31: E501 line too long (84 > 79 characters)
- Line 33: W293 blank line contains whitespace
- Line 35: W291 trailing whitespace
- Line 36: E128 continuation line under-indented for visual indent
- Line 39: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 59: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 85: E501 line too long (95 > 79 characters)
- Line 96: W293 blank line contains whitespace
- Line 102: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 29: Trailing whitespace
- Line 30: Trailing whitespace
- Line 33: Trailing whitespace
- Line 35: Trailing whitespace
- Line 39: Trailing whitespace
- Line 43: Trailing whitespace
- Line 47: Trailing whitespace
- Line 51: Trailing whitespace
- Line 55: Trailing whitespace
- Line 59: Trailing whitespace
- Line 67: Trailing whitespace
- Line 72: Trailing whitespace
- Line 76: Trailing whitespace
- Line 81: Trailing whitespace
- Line 96: Trailing whitespace
- Line 102: Trailing whitespace
- Line 107: Trailing whitespace

### src/piwardrive/vehicle_sensors.py
- Line 25: E501 line too long (83 > 79 characters)
- Line 83: E501 line too long (80 > 79 characters)

### src/piwardrive/direction_finding/hardware.py
- Line 38: E501 line too long (81 > 79 characters)
- Line 94: E501 line too long (81 > 79 characters)
- Line 115: E501 line too long (81 > 79 characters)
- Line 187: E501 line too long (88 > 79 characters)
- Line 194: E501 line too long (88 > 79 characters)
- Line 218: E501 line too long (85 > 79 characters)
- Line 351: E501 line too long (87 > 79 characters)
- Line 419: E501 line too long (87 > 79 characters)
- Line 439: E501 line too long (80 > 79 characters)
- Line 511: E501 line too long (80 > 79 characters)
- Line 530: E501 line too long (80 > 79 characters)
- Line 539: E501 line too long (80 > 79 characters)
- Line 544: E501 line too long (86 > 79 characters)
- Line 549: E501 line too long (81 > 79 characters)
- Line 578: E501 line too long (83 > 79 characters)
- Line 581: E501 line too long (84 > 79 characters)
- Line 623: E501 line too long (82 > 79 characters)
- Line 635: E501 line too long (88 > 79 characters)
- Line 642: E501 line too long (84 > 79 characters)
- Line 721: E501 line too long (81 > 79 characters)
- Line 744: E501 line too long (89 > 79 characters)
- Line 801: E501 line too long (88 > 79 characters)
- Line 830: E501 line too long (84 > 79 characters)
- Line 841: E501 line too long (92 > 79 characters)

### tests/test_robust_request.py
- Line 10: E501 line too long (81 > 79 characters)
- Line 46: E501 line too long (87 > 79 characters)

### tests/test_battery_widget.py
- Line 19: E501 line too long (86 > 79 characters)

### src/piwardrive/routes/security.py
- Line 29: E501 line too long (84 > 79 characters)
- Line 57: E501 line too long (86 > 79 characters)

### tests/test_heatmap.py
- Line 12: E501 line too long (87 > 79 characters)
- Line 28: E501 line too long (88 > 79 characters)
- Line 38: E501 line too long (80 > 79 characters)

### src/piwardrive/api/logging_control.py
- Line 31: E501 line too long (81 > 79 characters)

### tests/test_persistence.py
- Line 29: E501 line too long (88 > 79 characters)

### src/piwardrive/sigint_suite/cellular/tower_tracker/tracker.py
- Line 4: E501 line too long (80 > 79 characters)
- Line 6: Line too long (127 > 120 characters)

### src/piwardrive/routes/websocket.py
- Line 25: E501 line too long (84 > 79 characters)
- Line 49: E501 line too long (85 > 79 characters)

### scripts/performance_monitor.py
- Line 5: E501 line too long (82 > 79 characters)
- Line 61: E501 line too long (87 > 79 characters)
- Line 73: E501 line too long (80 > 79 characters)
- Line 74: E501 line too long (82 > 79 characters)
- Line 161: E501 line too long (88 > 79 characters)
- Line 167: E501 line too long (98 > 79 characters)
- Line 183: E501 line too long (85 > 79 characters)
- Line 197: E501 line too long (88 > 79 characters)
- Line 223: E501 line too long (86 > 79 characters)
- Line 276: E501 line too long (80 > 79 characters)
- Line 280: E501 line too long (88 > 79 characters)
- Line 296: E501 line too long (80 > 79 characters)
- Line 393: E501 line too long (86 > 79 characters)
- Line 469: E501 line too long (85 > 79 characters)
- Line 472: E501 line too long (83 > 79 characters)
- Line 508: E501 line too long (86 > 79 characters)
- Line 514: E501 line too long (82 > 79 characters)
- Line 531: E501 line too long (87 > 79 characters)
- Line 538: E501 line too long (81 > 79 characters)
- Line 553: E501 line too long (80 > 79 characters)
- Line 556: E501 line too long (86 > 79 characters)
- Line 564: E501 line too long (82 > 79 characters)
- Line 593: E501 line too long (82 > 79 characters)
- Line 613: E501 line too long (80 > 79 characters)

### src/piwardrive/widgets/service_status.py
- Line 40: E201 whitespace after '{'
- Line 40: E202 whitespace before '}'
- Line 41: E201 whitespace after '{'
- Line 41: E202 whitespace before '}'

### src/piwardrive/db/sqlite.py
- Line 59: E501 line too long (83 > 79 characters)
- Line 85: E501 line too long (84 > 79 characters)
- Line 91: E501 line too long (83 > 79 characters)
- Line 102: E501 line too long (88 > 79 characters)

### src/piwardrive/heatmap.py
- Line 14: E501 line too long (80 > 79 characters)
- Line 85: E501 line too long (87 > 79 characters)
- Line 134: E501 line too long (83 > 79 characters)
- Line 135: E501 line too long (82 > 79 characters)

### src/piwardrive/interfaces.py
- Line 12: E501 line too long (80 > 79 characters)

### src/piwardrive/services/coordinator.py
- Line 38: E501 line too long (83 > 79 characters)
- Line 81: E501 line too long (80 > 79 characters)

### scripts/performance_cli.py
- Line 20: E402 module level import not at top of file
- Line 24: E402 module level import not at top of file
- Line 29: E402 module level import not at top of file
- Line 56: E501 line too long (87 > 79 characters)
- Line 59: E128 continuation line under-indented for visual indent
- Line 59: E226 missing whitespace around arithmetic operator
- Line 125: E501 line too long (83 > 79 characters)
- Line 127: E226 missing whitespace around arithmetic operator
- Line 127: E226 missing whitespace around arithmetic operator
- Line 127: E501 line too long (87 > 79 characters)
- Line 157: E501 line too long (84 > 79 characters)
- Line 184: E226 missing whitespace around arithmetic operator
- Line 185: E226 missing whitespace around arithmetic operator
- Line 216: E501 line too long (86 > 79 characters)
- Line 276: E501 line too long (84 > 79 characters)
- Line 277: E501 line too long (85 > 79 characters)
- Line 283: E501 line too long (88 > 79 characters)
- Line 283: E501 line too long (88 > 79 characters)
- Line 283: E202 whitespace before '}'
- Line 284: E124 closing bracket does not match visual indentation
- Line 287: E501 line too long (93 > 79 characters)
- Line 289: E226 missing whitespace around arithmetic operator
- Line 322: E226 missing whitespace around arithmetic operator
- Line 364: E501 line too long (81 > 79 characters)
- Line 371: E501 line too long (88 > 79 characters)
- Line 393: E501 line too long (87 > 79 characters)
- Line 395: E501 line too long (86 > 79 characters)
- Line 402: E501 line too long (87 > 79 characters)

### tests/test_performance_dashboard_integration.py
- Line 13: E402 module level import not at top of file
- Line 24: E501 line too long (89 > 79 characters)
- Line 24: E231 missing whitespace after ','
- Line 25: E501 line too long (89 > 79 characters)
- Line 25: E231 missing whitespace after ','
- Line 26: E501 line too long (88 > 79 characters)
- Line 30: E231 missing whitespace after ','
- Line 30: E231 missing whitespace after ','
- Line 30: E231 missing whitespace after ','
- Line 30: E501 line too long (99 > 79 characters)
- Line 34: E231 missing whitespace after ','
- Line 34: E231 missing whitespace after ','
- Line 34: E501 line too long (101 > 79 characters)
- Line 34: E231 missing whitespace after ','
- Line 38: E231 missing whitespace after ','
- Line 38: E231 missing whitespace after ','
- Line 38: E501 line too long (109 > 79 characters)
- Line 38: E231 missing whitespace after ','
- Line 68: E501 line too long (89 > 79 characters)
- Line 68: E231 missing whitespace after ','
- Line 69: E501 line too long (89 > 79 characters)
- Line 69: E231 missing whitespace after ','
- Line 70: E501 line too long (88 > 79 characters)
- Line 74: E231 missing whitespace after ','
- Line 74: E231 missing whitespace after ','
- Line 74: E501 line too long (107 > 79 characters)
- Line 78: E231 missing whitespace after ','
- Line 78: E231 missing whitespace after ','
- Line 78: E501 line too long (100 > 79 characters)
- Line 82: E231 missing whitespace after ','
- Line 82: E231 missing whitespace after ','
- Line 82: E501 line too long (103 > 79 characters)
- Line 105: E501 line too long (89 > 79 characters)
- Line 105: E231 missing whitespace after ','
- Line 106: E501 line too long (89 > 79 characters)
- Line 106: E231 missing whitespace after ','
- Line 107: E501 line too long (88 > 79 characters)
- Line 111: E501 line too long (84 > 79 characters)
- Line 115: E501 line too long (87 > 79 characters)
- Line 119: E231 missing whitespace after ','
- Line 119: E231 missing whitespace after ','
- Line 119: E231 missing whitespace after ','
- Line 119: E501 line too long (90 > 79 characters)
- Line 142: E501 line too long (89 > 79 characters)
- Line 142: E231 missing whitespace after ','
- Line 143: E501 line too long (89 > 79 characters)
- Line 143: E231 missing whitespace after ','
- Line 144: E501 line too long (88 > 79 characters)
- Line 147: E231 missing whitespace after ','
- Line 147: E501 line too long (110 > 79 characters)
- Line 148: E501 line too long (110 > 79 characters)
- Line 148: E231 missing whitespace after ','
- Line 149: E231 missing whitespace after ','
- Line 149: E501 line too long (110 > 79 characters)
- Line 152: E501 line too long (87 > 79 characters)
- Line 159: E501 line too long (84 > 79 characters)
- Line 166: E501 line too long (87 > 79 characters)
- Line 172: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/integrations/r_integration.py
- Line 11: E501 line too long (83 > 79 characters)
- Line 21: E501 line too long (81 > 79 characters)

### scripts/db_summary.py
- Line 25: E501 line too long (83 > 79 characters)

### tests/test_scheduler_tasks.py
- Line 22: W293 blank line contains whitespace
- Line 26: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 35: W293 blank line contains whitespace
- Line 38: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 53: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 66: W293 blank line contains whitespace
- Line 73: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 80: W293 blank line contains whitespace
- Line 83: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 93: W293 blank line contains whitespace
- Line 96: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 108: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 115: W293 blank line contains whitespace
- Line 121: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 135: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 142: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 149: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 158: W293 blank line contains whitespace
- Line 160: E501 line too long (81 > 79 characters)
- Line 161: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 172: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 195: W293 blank line contains whitespace
- Line 197: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 211: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 216: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 227: W293 blank line contains whitespace
- Line 232: W293 blank line contains whitespace
- Line 236: W293 blank line contains whitespace
- Line 241: W293 blank line contains whitespace
- Line 245: W293 blank line contains whitespace
- Line 247: E501 line too long (80 > 79 characters)
- Line 248: W293 blank line contains whitespace
- Line 251: W293 blank line contains whitespace
- Line 256: W293 blank line contains whitespace
- Line 258: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 264: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 284: W293 blank line contains whitespace
- Line 287: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 300: W293 blank line contains whitespace
- Line 304: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 312: W293 blank line contains whitespace
- Line 315: W293 blank line contains whitespace
- Line 319: W293 blank line contains whitespace
- Line 323: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 336: W293 blank line contains whitespace
- Line 340: W293 blank line contains whitespace
- Line 349: W293 blank line contains whitespace
- Line 354: W293 blank line contains whitespace
- Line 358: W293 blank line contains whitespace
- Line 363: W293 blank line contains whitespace
- Line 366: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 377: W293 blank line contains whitespace
- Line 379: W293 blank line contains whitespace
- Line 383: W293 blank line contains whitespace
- Line 386: W293 blank line contains whitespace
- Line 392: W293 blank line contains whitespace
- Line 395: W293 blank line contains whitespace
- Line 398: W293 blank line contains whitespace
- Line 402: W293 blank line contains whitespace
- Line 406: E501 line too long (85 > 79 characters)
- Line 407: W293 blank line contains whitespace
- Line 409: W293 blank line contains whitespace
- Line 413: W293 blank line contains whitespace
- Line 415: W293 blank line contains whitespace
- Line 417: E501 line too long (96 > 79 characters)
- Line 418: E501 line too long (99 > 79 characters)
- Line 419: E501 line too long (105 > 79 characters)
- Line 420: E501 line too long (99 > 79 characters)
- Line 421: W293 blank line contains whitespace
- Line 425: W293 blank line contains whitespace
- Line 428: E501 line too long (119 > 79 characters)
- Line 430: W293 blank line contains whitespace
- Line 435: W293 blank line contains whitespace
- Line 437: W293 blank line contains whitespace
- Line 440: W293 blank line contains whitespace
- Line 444: W293 blank line contains whitespace
- Line 446: W293 blank line contains whitespace
- Line 452: W293 blank line contains whitespace
- Line 456: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 464: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 469: W293 blank line contains whitespace
- Line 473: W293 blank line contains whitespace
- Line 476: W293 blank line contains whitespace
- Line 481: W293 blank line contains whitespace
- Line 483: W293 blank line contains whitespace
- Line 488: W293 blank line contains whitespace
- Line 491: W293 blank line contains whitespace
- Line 493: W293 blank line contains whitespace
- Line 496: W293 blank line contains whitespace
- Line 500: W293 blank line contains whitespace
- Line 502: W293 blank line contains whitespace
- Line 508: W293 blank line contains whitespace
- Line 512: W293 blank line contains whitespace
- Line 516: W293 blank line contains whitespace
- Line 523: W293 blank line contains whitespace
- Line 527: W293 blank line contains whitespace
- Line 530: W293 blank line contains whitespace
- Line 534: W293 blank line contains whitespace
- Line 538: W293 blank line contains whitespace
- Line 541: W293 blank line contains whitespace
- Line 543: E501 line too long (83 > 79 characters)
- Line 545: W293 blank line contains whitespace
- Line 549: W293 blank line contains whitespace
- Line 553: W293 blank line contains whitespace
- Line 559: W293 blank line contains whitespace
- Line 561: E501 line too long (94 > 79 characters)
- Line 562: E501 line too long (89 > 79 characters)
- Line 565: W293 blank line contains whitespace
- Line 568: W293 blank line contains whitespace
- Line 572: W293 blank line contains whitespace
- Line 575: W293 blank line contains whitespace
- Line 580: W293 blank line contains whitespace
- Line 584: W293 blank line contains whitespace
- Line 590: W293 blank line contains whitespace
- Line 592: E501 line too long (88 > 79 characters)
- Line 593: E501 line too long (94 > 79 characters)
- Line 596: W293 blank line contains whitespace
- Line 599: W293 blank line contains whitespace
- Line 603: W293 blank line contains whitespace
- Line 606: W293 blank line contains whitespace
- Line 611: W293 blank line contains whitespace
- Line 619: W293 blank line contains whitespace
- Line 623: W293 blank line contains whitespace
- Line 627: E501 line too long (84 > 79 characters)
- Line 628: W293 blank line contains whitespace
- Line 633: W293 blank line contains whitespace
- Line 636: W293 blank line contains whitespace
- Line 640: W293 blank line contains whitespace
- Line 642: W293 blank line contains whitespace
- Line 646: W293 blank line contains whitespace
- Line 648: W293 blank line contains whitespace
- Line 654: W293 blank line contains whitespace
- Line 656: E501 line too long (85 > 79 characters)
- Line 657: W293 blank line contains whitespace
- Line 663: W293 blank line contains whitespace
- Line 665: W293 blank line contains whitespace
- Line 669: W293 blank line contains whitespace
- Line 672: W293 blank line contains whitespace
- Line 677: W293 blank line contains whitespace
- Line 679: W293 blank line contains whitespace
- Line 685: W293 blank line contains whitespace
- Line 688: E501 line too long (87 > 79 characters)
- Line 689: W293 blank line contains whitespace
- Line 692: W293 blank line contains whitespace
- Line 695: W293 blank line contains whitespace
- Line 699: W293 blank line contains whitespace
- Line 702: W293 blank line contains whitespace
- Line 706: W293 blank line contains whitespace
- Line 711: W293 blank line contains whitespace
- Line 713: W293 blank line contains whitespace
- Line 718: W293 blank line contains whitespace
- Line 720: W293 blank line contains whitespace
- Line 725: W293 blank line contains whitespace
- Line 729: W293 blank line contains whitespace
- Line 732: W293 blank line contains whitespace
- Line 734: W293 blank line contains whitespace
- Line 737: W293 blank line contains whitespace
- Line 744: W293 blank line contains whitespace
- Line 748: W293 blank line contains whitespace
- Line 751: W293 blank line contains whitespace
- Line 756: W293 blank line contains whitespace
- Line 760: W293 blank line contains whitespace
- Line 763: W293 blank line contains whitespace
- Line 767: W293 blank line contains whitespace
- Line 771: W293 blank line contains whitespace
- Line 774: W293 blank line contains whitespace
- Line 779: W293 blank line contains whitespace
- Line 782: W293 blank line contains whitespace
- Line 787: W293 blank line contains whitespace
- Line 791: W293 blank line contains whitespace
- Line 794: W293 blank line contains whitespace
- Line 797: W293 blank line contains whitespace
- Line 800: W293 blank line contains whitespace
- Line 804: W293 blank line contains whitespace
- Line 808: W293 blank line contains whitespace
- Line 813: W293 blank line contains whitespace
- Line 815: W293 blank line contains whitespace
- Line 821: W293 blank line contains whitespace
- Line 823: W293 blank line contains whitespace
- Line 827: W293 blank line contains whitespace
- Line 831: W293 blank line contains whitespace
- Line 22: Trailing whitespace
- Line 26: Trailing whitespace
- Line 31: Trailing whitespace
- Line 35: Trailing whitespace
- Line 38: Trailing whitespace
- Line 41: Trailing whitespace
- Line 44: Trailing whitespace
- Line 49: Trailing whitespace
- Line 53: Trailing whitespace
- Line 55: Trailing whitespace
- Line 66: Trailing whitespace
- Line 73: Trailing whitespace
- Line 77: Trailing whitespace
- Line 80: Trailing whitespace
- Line 83: Trailing whitespace
- Line 86: Trailing whitespace
- Line 89: Trailing whitespace
- Line 93: Trailing whitespace
- Line 96: Trailing whitespace
- Line 100: Trailing whitespace
- Line 104: Trailing whitespace
- Line 108: Trailing whitespace
- Line 112: Trailing whitespace
- Line 115: Trailing whitespace
- Line 121: Trailing whitespace
- Line 124: Trailing whitespace
- Line 128: Trailing whitespace
- Line 131: Trailing whitespace
- Line 135: Trailing whitespace
- Line 138: Trailing whitespace
- Line 142: Trailing whitespace
- Line 144: Trailing whitespace
- Line 147: Trailing whitespace
- Line 149: Trailing whitespace
- Line 154: Trailing whitespace
- Line 158: Trailing whitespace
- Line 161: Trailing whitespace
- Line 165: Trailing whitespace
- Line 168: Trailing whitespace
- Line 172: Trailing whitespace
- Line 176: Trailing whitespace
- Line 178: Trailing whitespace
- Line 181: Trailing whitespace
- Line 185: Trailing whitespace
- Line 188: Trailing whitespace
- Line 192: Trailing whitespace
- Line 195: Trailing whitespace
- Line 197: Trailing whitespace
- Line 204: Trailing whitespace
- Line 208: Trailing whitespace
- Line 211: Trailing whitespace
- Line 214: Trailing whitespace
- Line 216: Trailing whitespace
- Line 220: Trailing whitespace
- Line 227: Trailing whitespace
- Line 232: Trailing whitespace
- Line 236: Trailing whitespace
- Line 241: Trailing whitespace
- Line 245: Trailing whitespace
- Line 248: Trailing whitespace
- Line 251: Trailing whitespace
- Line 256: Trailing whitespace
- Line 258: Trailing whitespace
- Line 262: Trailing whitespace
- Line 264: Trailing whitespace
- Line 267: Trailing whitespace
- Line 270: Trailing whitespace
- Line 274: Trailing whitespace
- Line 277: Trailing whitespace
- Line 282: Trailing whitespace
- Line 284: Trailing whitespace
- Line 287: Trailing whitespace
- Line 291: Trailing whitespace
- Line 294: Trailing whitespace
- Line 297: Trailing whitespace
- Line 300: Trailing whitespace
- Line 304: Trailing whitespace
- Line 307: Trailing whitespace
- Line 312: Trailing whitespace
- Line 315: Trailing whitespace
- Line 319: Trailing whitespace
- Line 323: Trailing whitespace
- Line 326: Trailing whitespace
- Line 329: Trailing whitespace
- Line 332: Trailing whitespace
- Line 336: Trailing whitespace
- Line 340: Trailing whitespace
- Line 349: Trailing whitespace
- Line 354: Trailing whitespace
- Line 358: Trailing whitespace
- Line 363: Trailing whitespace
- Line 366: Trailing whitespace
- Line 369: Trailing whitespace
- Line 372: Trailing whitespace
- Line 377: Trailing whitespace
- Line 379: Trailing whitespace
- Line 383: Trailing whitespace
- Line 386: Trailing whitespace
- Line 392: Trailing whitespace
- Line 395: Trailing whitespace
- Line 398: Trailing whitespace
- Line 402: Trailing whitespace
- Line 407: Trailing whitespace
- Line 409: Trailing whitespace
- Line 413: Trailing whitespace
- Line 415: Trailing whitespace
- Line 421: Trailing whitespace
- Line 425: Trailing whitespace
- Line 430: Trailing whitespace
- Line 435: Trailing whitespace
- Line 437: Trailing whitespace
- Line 440: Trailing whitespace
- Line 444: Trailing whitespace
- Line 446: Trailing whitespace
- Line 452: Trailing whitespace
- Line 456: Trailing whitespace
- Line 459: Trailing whitespace
- Line 464: Trailing whitespace
- Line 467: Trailing whitespace
- Line 469: Trailing whitespace
- Line 473: Trailing whitespace
- Line 476: Trailing whitespace
- Line 481: Trailing whitespace
- Line 483: Trailing whitespace
- Line 488: Trailing whitespace
- Line 491: Trailing whitespace
- Line 493: Trailing whitespace
- Line 496: Trailing whitespace
- Line 500: Trailing whitespace
- Line 502: Trailing whitespace
- Line 508: Trailing whitespace
- Line 512: Trailing whitespace
- Line 516: Trailing whitespace
- Line 523: Trailing whitespace
- Line 527: Trailing whitespace
- Line 530: Trailing whitespace
- Line 534: Trailing whitespace
- Line 538: Trailing whitespace
- Line 541: Trailing whitespace
- Line 545: Trailing whitespace
- Line 549: Trailing whitespace
- Line 553: Trailing whitespace
- Line 559: Trailing whitespace
- Line 565: Trailing whitespace
- Line 568: Trailing whitespace
- Line 572: Trailing whitespace
- Line 575: Trailing whitespace
- Line 580: Trailing whitespace
- Line 584: Trailing whitespace
- Line 590: Trailing whitespace
- Line 596: Trailing whitespace
- Line 599: Trailing whitespace
- Line 603: Trailing whitespace
- Line 606: Trailing whitespace
- Line 611: Trailing whitespace
- Line 619: Trailing whitespace
- Line 623: Trailing whitespace
- Line 628: Trailing whitespace
- Line 633: Trailing whitespace
- Line 636: Trailing whitespace
- Line 640: Trailing whitespace
- Line 642: Trailing whitespace
- Line 646: Trailing whitespace
- Line 648: Trailing whitespace
- Line 654: Trailing whitespace
- Line 657: Trailing whitespace
- Line 663: Trailing whitespace
- Line 665: Trailing whitespace
- Line 669: Trailing whitespace
- Line 672: Trailing whitespace
- Line 677: Trailing whitespace
- Line 679: Trailing whitespace
- Line 685: Trailing whitespace
- Line 689: Trailing whitespace
- Line 692: Trailing whitespace
- Line 695: Trailing whitespace
- Line 699: Trailing whitespace
- Line 702: Trailing whitespace
- Line 706: Trailing whitespace
- Line 711: Trailing whitespace
- Line 713: Trailing whitespace
- Line 718: Trailing whitespace
- Line 720: Trailing whitespace
- Line 725: Trailing whitespace
- Line 729: Trailing whitespace
- Line 732: Trailing whitespace
- Line 734: Trailing whitespace
- Line 737: Trailing whitespace
- Line 744: Trailing whitespace
- Line 748: Trailing whitespace
- Line 751: Trailing whitespace
- Line 756: Trailing whitespace
- Line 760: Trailing whitespace
- Line 763: Trailing whitespace
- Line 767: Trailing whitespace
- Line 771: Trailing whitespace
- Line 774: Trailing whitespace
- Line 779: Trailing whitespace
- Line 782: Trailing whitespace
- Line 787: Trailing whitespace
- Line 791: Trailing whitespace
- Line 794: Trailing whitespace
- Line 797: Trailing whitespace
- Line 800: Trailing whitespace
- Line 804: Trailing whitespace
- Line 808: Trailing whitespace
- Line 813: Trailing whitespace
- Line 815: Trailing whitespace
- Line 821: Trailing whitespace
- Line 823: Trailing whitespace
- Line 827: Trailing whitespace
- Line 831: Trailing whitespace

### src/piwardrive/jobs/maintenance_jobs.py
- Line 20: E501 line too long (86 > 79 characters)
- Line 27: E501 line too long (81 > 79 characters)
- Line 39: E501 line too long (83 > 79 characters)
- Line 44: E501 line too long (88 > 79 characters)
- Line 49: E501 line too long (82 > 79 characters)
- Line 54: E501 line too long (87 > 79 characters)

### src/piwardrive/widgets/base.py
- Line 26: W503 line break before binary operator
- Line 27: W503 line break before binary operator

### src/piwardrive/migrations/007_create_suspicious_activities.py
- Line 33: E501 line too long (105 > 79 characters)
- Line 36: E501 line too long (100 > 79 characters)
- Line 39: E501 line too long (99 > 79 characters)
- Line 42: E501 line too long (98 > 79 characters)

### src/piwardrive/r_integration.py
- Line 11: E501 line too long (83 > 79 characters)
- Line 21: E501 line too long (81 > 79 characters)

### src/piwardrive/lora_scanner.py
- Line 4: E501 line too long (80 > 79 characters)
- Line 44: E501 line too long (85 > 79 characters)
- Line 50: E501 line too long (80 > 79 characters)
- Line 64: E501 line too long (80 > 79 characters)
- Line 99: E501 line too long (80 > 79 characters)
- Line 106: E501 line too long (80 > 79 characters)
- Line 304: E501 line too long (80 > 79 characters)
- Line 325: E501 line too long (80 > 79 characters)

### src/piwardrive/unified_platform.py
- Line 4: E501 line too long (91 > 79 characters)
- Line 57: E501 line too long (85 > 79 characters)
- Line 119: W293 blank line contains whitespace
- Line 149: W293 blank line contains whitespace
- Line 155: E501 line too long (81 > 79 characters)
- Line 243: E501 line too long (88 > 79 characters)
- Line 385: E501 line too long (86 > 79 characters)
- Line 502: E501 line too long (83 > 79 characters)
- Line 514: E501 line too long (87 > 79 characters)
- Line 553: W503 line break before binary operator
- Line 568: E501 line too long (86 > 79 characters)
- Line 571: E501 line too long (83 > 79 characters)
- Line 605: E501 line too long (80 > 79 characters)
- Line 609: E501 line too long (83 > 79 characters)
- Line 618: E501 line too long (85 > 79 characters)
- Line 635: E501 line too long (81 > 79 characters)
- Line 681: E501 line too long (104 > 79 characters)
- Line 682: E501 line too long (134 > 79 characters)
- Line 689: E501 line too long (85 > 79 characters)
- Line 692: E501 line too long (124 > 79 characters)
- Line 694: E501 line too long (149 > 79 characters)
- Line 695: E501 line too long (144 > 79 characters)
- Line 708: E501 line too long (86 > 79 characters)
- Line 734: E501 line too long (86 > 79 characters)
- Line 735: E501 line too long (100 > 79 characters)
- Line 738: E501 line too long (120 > 79 characters)
- Line 741: E501 line too long (110 > 79 characters)
- Line 746: E501 line too long (80 > 79 characters)
- Line 749: E501 line too long (87 > 79 characters)
- Line 750: E501 line too long (89 > 79 characters)
- Line 751: E501 line too long (99 > 79 characters)
- Line 755: E501 line too long (80 > 79 characters)
- Line 756: E501 line too long (109 > 79 characters)
- Line 781: E501 line too long (87 > 79 characters)
- Line 802: E501 line too long (80 > 79 characters)
- Line 848: E501 line too long (82 > 79 characters)
- Line 899: E501 line too long (88 > 79 characters)
- Line 902: E501 line too long (93 > 79 characters)
- Line 119: Trailing whitespace
- Line 149: Trailing whitespace
- Line 682: Line too long (134 > 120 characters)
- Line 692: Line too long (124 > 120 characters)
- Line 694: Line too long (149 > 120 characters)
- Line 695: Line too long (144 > 120 characters)

### src/piwardrive/analysis.py
- Line 61: E501 line too long (81 > 79 characters)
- Line 66: E203 whitespace before ':'
- Line 113: W503 line break before binary operator
- Line 113: E501 line too long (81 > 79 characters)
- Line 114: W503 line break before binary operator

### tests/test_analysis_queries_service.py
- Line 44: E501 line too long (82 > 79 characters)
- Line 57: E501 line too long (87 > 79 characters)

### src/piwardrive/widgets/db_stats.py
- Line 36: E501 line too long (81 > 79 characters)
- Line 60: E501 line too long (86 > 79 characters)

### tests/test_orientation_sensors.py
- Line 167: E501 line too long (81 > 79 characters)

### tests/test_network_analytics.py
- Line 31: E501 line too long (81 > 79 characters)
- Line 71: E501 line too long (82 > 79 characters)
- Line 84: E501 line too long (81 > 79 characters)
- Line 89: E501 line too long (81 > 79 characters)
- Line 90: E501 line too long (81 > 79 characters)
- Line 91: E501 line too long (82 > 79 characters)
- Line 130: E501 line too long (84 > 79 characters)

### src/piwardrive/testing/automated_framework.py
- Line 150: E501 line too long (80 > 79 characters)
- Line 167: E501 line too long (87 > 79 characters)
- Line 201: E501 line too long (80 > 79 characters)
- Line 228: E501 line too long (83 > 79 characters)
- Line 230: E501 line too long (82 > 79 characters)
- Line 311: E501 line too long (81 > 79 characters)
- Line 316: E501 line too long (85 > 79 characters)
- Line 334: E501 line too long (82 > 79 characters)
- Line 401: E501 line too long (81 > 79 characters)
- Line 405: E501 line too long (84 > 79 characters)
- Line 408: E501 line too long (86 > 79 characters)
- Line 412: E501 line too long (86 > 79 characters)
- Line 603: E501 line too long (85 > 79 characters)
- Line 625: E501 line too long (88 > 79 characters)
- Line 677: E501 line too long (84 > 79 characters)
- Line 696: W503 line break before binary operator
- Line 697: W503 line break before binary operator
- Line 774: E501 line too long (82 > 79 characters)
- Line 797: E501 line too long (80 > 79 characters)
- Line 905: E501 line too long (83 > 79 characters)
- Line 906: E501 line too long (83 > 79 characters)
- Line 907: E501 line too long (81 > 79 characters)
- Line 915: E501 line too long (88 > 79 characters)
- Line 930: E501 line too long (85 > 79 characters)
- Line 939: E501 line too long (86 > 79 characters)
- Line 940: E501 line too long (86 > 79 characters)
- Line 941: E501 line too long (87 > 79 characters)
- Line 942: E501 line too long (87 > 79 characters)
- Line 1075: E501 line too long (81 > 79 characters)
- Line 1076: E501 line too long (81 > 79 characters)
- Line 1083: E226 missing whitespace around arithmetic operator
- Line 1083: E226 missing whitespace around arithmetic operator

### src/piwardrive/memory_monitor.py
- Line 4: E501 line too long (81 > 79 characters)
- Line 21: W293 blank line contains whitespace
- Line 28: E501 line too long (82 > 79 characters)
- Line 21: Trailing whitespace

### src/piwardrive/widgets/log_viewer.py
- Line 16: E402 module level import not at top of file
- Line 40: E501 line too long (85 > 79 characters)
- Line 47: E501 line too long (86 > 79 characters)

### tests/test_cache_security_comprehensive.py
- Line 14: W291 trailing whitespace
- Line 15: W291 trailing whitespace
- Line 32: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 48: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 88: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 121: W293 blank line contains whitespace
- Line 146: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 215: W293 blank line contains whitespace
- Line 224: W293 blank line contains whitespace
- Line 231: W293 blank line contains whitespace
- Line 238: W293 blank line contains whitespace
- Line 245: W293 blank line contains whitespace
- Line 252: W293 blank line contains whitespace
- Line 260: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 275: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 308: W293 blank line contains whitespace
- Line 312: W293 blank line contains whitespace
- Line 314: E501 line too long (85 > 79 characters)
- Line 319: W293 blank line contains whitespace
- Line 322: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 347: W293 blank line contains whitespace
- Line 355: W293 blank line contains whitespace
- Line 359: W293 blank line contains whitespace
- Line 376: W293 blank line contains whitespace
- Line 380: W293 blank line contains whitespace
- Line 388: W293 blank line contains whitespace
- Line 392: W293 blank line contains whitespace
- Line 404: W293 blank line contains whitespace
- Line 407: W293 blank line contains whitespace
- Line 14: Trailing whitespace
- Line 15: Trailing whitespace
- Line 32: Trailing whitespace
- Line 41: Trailing whitespace
- Line 48: Trailing whitespace
- Line 55: Trailing whitespace
- Line 81: Trailing whitespace
- Line 88: Trailing whitespace
- Line 98: Trailing whitespace
- Line 110: Trailing whitespace
- Line 112: Trailing whitespace
- Line 121: Trailing whitespace
- Line 146: Trailing whitespace
- Line 148: Trailing whitespace
- Line 156: Trailing whitespace
- Line 159: Trailing whitespace
- Line 169: Trailing whitespace
- Line 173: Trailing whitespace
- Line 176: Trailing whitespace
- Line 183: Trailing whitespace
- Line 192: Trailing whitespace
- Line 194: Trailing whitespace
- Line 206: Trailing whitespace
- Line 215: Trailing whitespace
- Line 224: Trailing whitespace
- Line 231: Trailing whitespace
- Line 238: Trailing whitespace
- Line 245: Trailing whitespace
- Line 252: Trailing whitespace
- Line 260: Trailing whitespace
- Line 267: Trailing whitespace
- Line 275: Trailing whitespace
- Line 282: Trailing whitespace
- Line 291: Trailing whitespace
- Line 308: Trailing whitespace
- Line 312: Trailing whitespace
- Line 319: Trailing whitespace
- Line 322: Trailing whitespace
- Line 329: Trailing whitespace
- Line 332: Trailing whitespace
- Line 342: Trailing whitespace
- Line 347: Trailing whitespace
- Line 355: Trailing whitespace
- Line 359: Trailing whitespace
- Line 376: Trailing whitespace
- Line 380: Trailing whitespace
- Line 388: Trailing whitespace
- Line 392: Trailing whitespace
- Line 404: Trailing whitespace
- Line 407: Trailing whitespace

### src/piwardrive/mysql_export.py
- Line 26: E302 expected 2 blank lines, found 1
- Line 37: E302 expected 2 blank lines, found 1
- Line 52: E501 line too long (85 > 79 characters)
- Line 67: E501 line too long (83 > 79 characters)
- Line 70: E501 line too long (86 > 79 characters)
- Line 73: E501 line too long (84 > 79 characters)
- Line 88: E501 line too long (87 > 79 characters)
- Line 91: E501 line too long (89 > 79 characters)
- Line 94: E501 line too long (87 > 79 characters)
- Line 109: E501 line too long (85 > 79 characters)
- Line 112: E501 line too long (88 > 79 characters)
- Line 115: E501 line too long (86 > 79 characters)
- Line 138: E501 line too long (100 > 79 characters)
- Line 142: E501 line too long (91 > 79 characters)
- Line 145: E501 line too long (106 > 79 characters)
- Line 192: E501 line too long (104 > 79 characters)
- Line 195: E501 line too long (92 > 79 characters)
- Line 198: E501 line too long (90 > 79 characters)
- Line 201: E501 line too long (105 > 79 characters)
- Line 204: E501 line too long (100 > 79 characters)
- Line 238: E501 line too long (107 > 79 characters)
- Line 241: E501 line too long (99 > 79 characters)
- Line 244: E501 line too long (108 > 79 characters)
- Line 247: E501 line too long (103 > 79 characters)
- Line 281: E501 line too long (112 > 79 characters)
- Line 284: E501 line too long (103 > 79 characters)
- Line 288: E501 line too long (113 > 79 characters)
- Line 291: E501 line too long (108 > 79 characters)
- Line 315: E501 line too long (94 > 79 characters)
- Line 318: E501 line too long (85 > 79 characters)
- Line 321: E501 line too long (90 > 79 characters)
- Line 344: E501 line too long (101 > 79 characters)
- Line 347: E501 line too long (104 > 79 characters)
- Line 350: E501 line too long (112 > 79 characters)
- Line 372: E501 line too long (105 > 79 characters)
- Line 375: E501 line too long (100 > 79 characters)
- Line 378: E501 line too long (99 > 79 characters)
- Line 381: E501 line too long (98 > 79 characters)
- Line 407: E501 line too long (88 > 79 characters)
- Line 410: E501 line too long (95 > 79 characters)
- Line 413: E501 line too long (104 > 79 characters)
- Line 417: E302 expected 2 blank lines, found 1
- Line 444: E302 expected 2 blank lines, found 1
- Line 470: E302 expected 2 blank lines, found 1
- Line 488: E302 expected 2 blank lines, found 1
- Line 510: E302 expected 2 blank lines, found 1
- Line 554: E302 expected 2 blank lines, found 1
- Line 585: E302 expected 2 blank lines, found 1
- Line 616: E302 expected 2 blank lines, found 1
- Line 637: E302 expected 2 blank lines, found 1
- Line 657: E302 expected 2 blank lines, found 1
- Line 677: E302 expected 2 blank lines, found 1
- Line 700: E302 expected 2 blank lines, found 1

### src/piwardrive/integrations/sigint_suite/cellular/utils.py
- Line 20: E501 line too long (87 > 79 characters)

### src/piwardrive/services/security_analyzer.py
- Line 40: E501 line too long (86 > 79 characters)
- Line 42: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 53: E501 line too long (81 > 79 characters)
- Line 58: E501 line too long (84 > 79 characters)
- Line 60: W293 blank line contains whitespace
- Line 63: W293 blank line contains whitespace
- Line 93: E501 line too long (98 > 79 characters)
- Line 99: E501 line too long (88 > 79 characters)
- Line 101: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 112: W503 line break before binary operator
- Line 113: W503 line break before binary operator
- Line 119: E501 line too long (93 > 79 characters)
- Line 42: Trailing whitespace
- Line 45: Trailing whitespace
- Line 60: Trailing whitespace
- Line 63: Trailing whitespace
- Line 101: Trailing whitespace
- Line 104: Trailing whitespace

### src/piwardrive/service.py
- Line 23: E302 expected 2 blank lines, found 1
- Line 26: E305 expected 2 blank lines after class or function definition, found 0
- Line 26: E402 module level import not at top of file
- Line 40: E402 module level import not at top of file
- Line 41: E402 module level import not at top of file
- Line 42: E402 module level import not at top of file
- Line 43: E402 module level import not at top of file
- Line 44: E402 module level import not at top of file
- Line 45: E402 module level import not at top of file
- Line 45: E501 line too long (83 > 79 characters)
- Line 46: E402 module level import not at top of file
- Line 47: E402 module level import not at top of file
- Line 48: E402 module level import not at top of file
- Line 49: E402 module level import not at top of file
- Line 50: E402 module level import not at top of file
- Line 51: E402 module level import not at top of file
- Line 52: E402 module level import not at top of file
- Line 53: E402 module level import not at top of file
- Line 54: E402 module level import not at top of file
- Line 55: E402 module level import not at top of file
- Line 56: E402 module level import not at top of file

### tests/test_imsi_catcher.py
- Line 5: E501 line too long (81 > 79 characters)

### tests/test_core_config.py
- Line 16: W291 trailing whitespace
- Line 17: W291 trailing whitespace
- Line 39: W293 blank line contains whitespace
- Line 44: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 65: W293 blank line contains whitespace
- Line 68: W293 blank line contains whitespace
- Line 70: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 87: W293 blank line contains whitespace
- Line 90: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 116: W293 blank line contains whitespace
- Line 121: W293 blank line contains whitespace
- Line 130: W293 blank line contains whitespace
- Line 138: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 160: E501 line too long (84 > 79 characters)
- Line 161: E501 line too long (82 > 79 characters)
- Line 163: W293 blank line contains whitespace
- Line 166: W293 blank line contains whitespace
- Line 169: W293 blank line contains whitespace
- Line 173: E501 line too long (90 > 79 characters)
- Line 174: E501 line too long (88 > 79 characters)
- Line 175: E501 line too long (82 > 79 characters)
- Line 176: W293 blank line contains whitespace
- Line 180: W293 blank line contains whitespace
- Line 184: W293 blank line contains whitespace
- Line 186: W293 blank line contains whitespace
- Line 190: W293 blank line contains whitespace
- Line 198: W293 blank line contains whitespace
- Line 206: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 213: W293 blank line contains whitespace
- Line 218: W293 blank line contains whitespace
- Line 223: W293 blank line contains whitespace
- Line 226: E501 line too long (87 > 79 characters)
- Line 228: W293 blank line contains whitespace
- Line 232: W293 blank line contains whitespace
- Line 235: E501 line too long (83 > 79 characters)
- Line 237: W293 blank line contains whitespace
- Line 241: E501 line too long (86 > 79 characters)
- Line 243: W293 blank line contains whitespace
- Line 247: W293 blank line contains whitespace
- Line 250: E501 line too long (90 > 79 characters)
- Line 252: W293 blank line contains whitespace
- Line 256: E501 line too long (87 > 79 characters)
- Line 262: W293 blank line contains whitespace
- Line 266: E501 line too long (90 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 273: W293 blank line contains whitespace
- Line 277: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 284: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 296: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 305: E501 line too long (90 > 79 characters)
- Line 306: E501 line too long (107 > 79 characters)
- Line 311: W293 blank line contains whitespace
- Line 315: W293 blank line contains whitespace
- Line 319: W293 blank line contains whitespace
- Line 323: W293 blank line contains whitespace
- Line 331: W293 blank line contains whitespace
- Line 334: W293 blank line contains whitespace
- Line 337: W293 blank line contains whitespace
- Line 340: W293 blank line contains whitespace
- Line 345: E501 line too long (85 > 79 characters)
- Line 347: W293 blank line contains whitespace
- Line 349: E501 line too long (85 > 79 characters)
- Line 355: W293 blank line contains whitespace
- Line 365: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 386: W293 blank line contains whitespace
- Line 391: W293 blank line contains whitespace
- Line 401: W293 blank line contains whitespace
- Line 405: W293 blank line contains whitespace
- Line 414: W293 blank line contains whitespace
- Line 418: W293 blank line contains whitespace
- Line 426: W293 blank line contains whitespace
- Line 433: W293 blank line contains whitespace
- Line 441: W293 blank line contains whitespace
- Line 449: W293 blank line contains whitespace
- Line 452: W293 blank line contains whitespace
- Line 455: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 463: W293 blank line contains whitespace
- Line 476: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 484: W293 blank line contains whitespace
- Line 492: W293 blank line contains whitespace
- Line 494: E501 line too long (84 > 79 characters)
- Line 496: W293 blank line contains whitespace
- Line 504: E501 line too long (82 > 79 characters)
- Line 505: E501 line too long (87 > 79 characters)
- Line 506: W293 blank line contains whitespace
- Line 510: W293 blank line contains whitespace
- Line 513: W293 blank line contains whitespace
- Line 517: E501 line too long (90 > 79 characters)
- Line 518: E501 line too long (95 > 79 characters)
- Line 523: W293 blank line contains whitespace
- Line 530: W293 blank line contains whitespace
- Line 534: W293 blank line contains whitespace
- Line 535: E501 line too long (81 > 79 characters)
- Line 537: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 548: W293 blank line contains whitespace
- Line 551: W293 blank line contains whitespace
- Line 557: W293 blank line contains whitespace
- Line 559: W293 blank line contains whitespace
- Line 567: W293 blank line contains whitespace
- Line 571: E501 line too long (84 > 79 characters)
- Line 574: W293 blank line contains whitespace
- Line 578: W293 blank line contains whitespace
- Line 581: W293 blank line contains whitespace
- Line 587: W293 blank line contains whitespace
- Line 592: W293 blank line contains whitespace
- Line 16: Trailing whitespace
- Line 17: Trailing whitespace
- Line 39: Trailing whitespace
- Line 44: Trailing whitespace
- Line 52: Trailing whitespace
- Line 65: Trailing whitespace
- Line 68: Trailing whitespace
- Line 70: Trailing whitespace
- Line 77: Trailing whitespace
- Line 87: Trailing whitespace
- Line 90: Trailing whitespace
- Line 92: Trailing whitespace
- Line 98: Trailing whitespace
- Line 106: Trailing whitespace
- Line 110: Trailing whitespace
- Line 116: Trailing whitespace
- Line 121: Trailing whitespace
- Line 130: Trailing whitespace
- Line 138: Trailing whitespace
- Line 140: Trailing whitespace
- Line 144: Trailing whitespace
- Line 148: Trailing whitespace
- Line 152: Trailing whitespace
- Line 163: Trailing whitespace
- Line 166: Trailing whitespace
- Line 169: Trailing whitespace
- Line 176: Trailing whitespace
- Line 180: Trailing whitespace
- Line 184: Trailing whitespace
- Line 186: Trailing whitespace
- Line 190: Trailing whitespace
- Line 198: Trailing whitespace
- Line 206: Trailing whitespace
- Line 209: Trailing whitespace
- Line 213: Trailing whitespace
- Line 218: Trailing whitespace
- Line 223: Trailing whitespace
- Line 228: Trailing whitespace
- Line 232: Trailing whitespace
- Line 237: Trailing whitespace
- Line 243: Trailing whitespace
- Line 247: Trailing whitespace
- Line 252: Trailing whitespace
- Line 262: Trailing whitespace
- Line 271: Trailing whitespace
- Line 273: Trailing whitespace
- Line 277: Trailing whitespace
- Line 280: Trailing whitespace
- Line 284: Trailing whitespace
- Line 291: Trailing whitespace
- Line 296: Trailing whitespace
- Line 298: Trailing whitespace
- Line 301: Trailing whitespace
- Line 311: Trailing whitespace
- Line 315: Trailing whitespace
- Line 319: Trailing whitespace
- Line 323: Trailing whitespace
- Line 331: Trailing whitespace
- Line 334: Trailing whitespace
- Line 337: Trailing whitespace
- Line 340: Trailing whitespace
- Line 347: Trailing whitespace
- Line 355: Trailing whitespace
- Line 365: Trailing whitespace
- Line 369: Trailing whitespace
- Line 386: Trailing whitespace
- Line 391: Trailing whitespace
- Line 401: Trailing whitespace
- Line 405: Trailing whitespace
- Line 414: Trailing whitespace
- Line 418: Trailing whitespace
- Line 426: Trailing whitespace
- Line 433: Trailing whitespace
- Line 441: Trailing whitespace
- Line 449: Trailing whitespace
- Line 452: Trailing whitespace
- Line 455: Trailing whitespace
- Line 459: Trailing whitespace
- Line 463: Trailing whitespace
- Line 476: Trailing whitespace
- Line 479: Trailing whitespace
- Line 484: Trailing whitespace
- Line 492: Trailing whitespace
- Line 496: Trailing whitespace
- Line 506: Trailing whitespace
- Line 510: Trailing whitespace
- Line 513: Trailing whitespace
- Line 523: Trailing whitespace
- Line 530: Trailing whitespace
- Line 534: Trailing whitespace
- Line 537: Trailing whitespace
- Line 544: Trailing whitespace
- Line 548: Trailing whitespace
- Line 551: Trailing whitespace
- Line 557: Trailing whitespace
- Line 559: Trailing whitespace
- Line 567: Trailing whitespace
- Line 574: Trailing whitespace
- Line 578: Trailing whitespace
- Line 581: Trailing whitespace
- Line 587: Trailing whitespace
- Line 592: Trailing whitespace

### tests/test_export_logs_script.py
- Line 19: E501 line too long (85 > 79 characters)

### src/piwardrive/widgets/__init__.py
- Line 58: E501 line too long (87 > 79 characters)
- Line 123: E501 line too long (87 > 79 characters)
- Line 138: E501 line too long (88 > 79 characters)
- Line 153: E501 line too long (84 > 79 characters)
- Line 201: W503 line break before binary operator
- Line 202: W503 line break before binary operator
- Line 208: E501 line too long (86 > 79 characters)

### src/piwardrive/route_prefetch.py
- Line 20: E402 module level import not at top of file
- Line 21: E402 module level import not at top of file
- Line 32: E501 line too long (85 > 79 characters)
- Line 48: E501 line too long (86 > 79 characters)
- Line 99: E203 whitespace before ':'
- Line 119: W503 line break before binary operator

### src/piwardrive/cli/kiosk.py
- Line 19: E501 line too long (83 > 79 characters)
- Line 21: E501 line too long (81 > 79 characters)

### tests/test_plot_cpu_temp_plotly_backend.py
- Line 20: E203 whitespace before ':'
- Line 20: E501 line too long (88 > 79 characters)

### tests/test_continuous_scan.py
- Line 82: E501 line too long (85 > 79 characters)

### tests/test_logging_filters.py
- Line 4: E501 line too long (86 > 79 characters)

### src/piwardrive/api/analytics/endpoints.py
- Line 51: E501 line too long (83 > 79 characters)

### tests/test_interfaces.py
- Line 18: E402 module level import not at top of file
- Line 34: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 48: W293 blank line contains whitespace
- Line 53: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 74: E501 line too long (85 > 79 characters)
- Line 76: W293 blank line contains whitespace
- Line 78: W293 blank line contains whitespace
- Line 85: W293 blank line contains whitespace
- Line 86: E501 line too long (85 > 79 characters)
- Line 88: W293 blank line contains whitespace
- Line 90: W293 blank line contains whitespace
- Line 97: W293 blank line contains whitespace
- Line 98: E501 line too long (85 > 79 characters)
- Line 100: W293 blank line contains whitespace
- Line 102: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 110: E501 line too long (85 > 79 characters)
- Line 112: E501 line too long (89 > 79 characters)
- Line 113: W293 blank line contains whitespace
- Line 115: W293 blank line contains whitespace
- Line 124: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 133: E501 line too long (89 > 79 characters)
- Line 135: W293 blank line contains whitespace
- Line 138: E501 line too long (101 > 79 characters)
- Line 144: W293 blank line contains whitespace
- Line 149: W293 blank line contains whitespace
- Line 150: E501 line too long (90 > 79 characters)
- Line 152: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 161: W293 blank line contains whitespace
- Line 162: E501 line too long (90 > 79 characters)
- Line 164: W293 blank line contains whitespace
- Line 166: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 177: W293 blank line contains whitespace
- Line 178: E501 line too long (90 > 79 characters)
- Line 180: W293 blank line contains whitespace
- Line 182: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 192: E501 line too long (90 > 79 characters)
- Line 194: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 214: W293 blank line contains whitespace
- Line 232: W293 blank line contains whitespace
- Line 238: W293 blank line contains whitespace
- Line 239: E501 line too long (89 > 79 characters)
- Line 241: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 250: W293 blank line contains whitespace
- Line 251: E501 line too long (89 > 79 characters)
- Line 253: W293 blank line contains whitespace
- Line 255: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 268: W293 blank line contains whitespace
- Line 269: E501 line too long (89 > 79 characters)
- Line 271: W293 blank line contains whitespace
- Line 273: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 283: E501 line too long (89 > 79 characters)
- Line 285: W293 blank line contains whitespace
- Line 293: W293 blank line contains whitespace
- Line 299: W293 blank line contains whitespace
- Line 300: E501 line too long (89 > 79 characters)
- Line 302: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 318: E501 line too long (82 > 79 characters)
- Line 320: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 328: W293 blank line contains whitespace
- Line 330: E501 line too long (92 > 79 characters)
- Line 333: W293 blank line contains whitespace
- Line 334: E501 line too long (99 > 79 characters)
- Line 339: E501 line too long (85 > 79 characters)
- Line 341: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 347: E501 line too long (88 > 79 characters)
- Line 353: W293 blank line contains whitespace
- Line 357: W293 blank line contains whitespace
- Line 360: W293 blank line contains whitespace
- Line 364: W293 blank line contains whitespace
- Line 368: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 383: E501 line too long (87 > 79 characters)
- Line 384: E501 line too long (93 > 79 characters)
- Line 385: E501 line too long (91 > 79 characters)
- Line 386: W293 blank line contains whitespace
- Line 391: W293 blank line contains whitespace
- Line 396: W293 blank line contains whitespace
- Line 401: W293 blank line contains whitespace
- Line 414: W293 blank line contains whitespace
- Line 422: W293 blank line contains whitespace
- Line 424: E501 line too long (89 > 79 characters)
- Line 426: W293 blank line contains whitespace
- Line 427: E501 line too long (92 > 79 characters)
- Line 431: E501 line too long (93 > 79 characters)
- Line 439: W293 blank line contains whitespace
- Line 440: E501 line too long (89 > 79 characters)
- Line 442: W293 blank line contains whitespace
- Line 444: W293 blank line contains whitespace
- Line 34: Trailing whitespace
- Line 41: Trailing whitespace
- Line 45: Trailing whitespace
- Line 48: Trailing whitespace
- Line 53: Trailing whitespace
- Line 72: Trailing whitespace
- Line 76: Trailing whitespace
- Line 78: Trailing whitespace
- Line 85: Trailing whitespace
- Line 88: Trailing whitespace
- Line 90: Trailing whitespace
- Line 97: Trailing whitespace
- Line 100: Trailing whitespace
- Line 102: Trailing whitespace
- Line 109: Trailing whitespace
- Line 113: Trailing whitespace
- Line 115: Trailing whitespace
- Line 124: Trailing whitespace
- Line 131: Trailing whitespace
- Line 135: Trailing whitespace
- Line 144: Trailing whitespace
- Line 149: Trailing whitespace
- Line 152: Trailing whitespace
- Line 154: Trailing whitespace
- Line 161: Trailing whitespace
- Line 164: Trailing whitespace
- Line 166: Trailing whitespace
- Line 173: Trailing whitespace
- Line 177: Trailing whitespace
- Line 180: Trailing whitespace
- Line 182: Trailing whitespace
- Line 191: Trailing whitespace
- Line 194: Trailing whitespace
- Line 210: Trailing whitespace
- Line 214: Trailing whitespace
- Line 232: Trailing whitespace
- Line 238: Trailing whitespace
- Line 241: Trailing whitespace
- Line 243: Trailing whitespace
- Line 250: Trailing whitespace
- Line 253: Trailing whitespace
- Line 255: Trailing whitespace
- Line 262: Trailing whitespace
- Line 268: Trailing whitespace
- Line 271: Trailing whitespace
- Line 273: Trailing whitespace
- Line 282: Trailing whitespace
- Line 285: Trailing whitespace
- Line 293: Trailing whitespace
- Line 299: Trailing whitespace
- Line 302: Trailing whitespace
- Line 307: Trailing whitespace
- Line 320: Trailing whitespace
- Line 324: Trailing whitespace
- Line 328: Trailing whitespace
- Line 333: Trailing whitespace
- Line 341: Trailing whitespace
- Line 345: Trailing whitespace
- Line 353: Trailing whitespace
- Line 357: Trailing whitespace
- Line 360: Trailing whitespace
- Line 364: Trailing whitespace
- Line 368: Trailing whitespace
- Line 372: Trailing whitespace
- Line 381: Trailing whitespace
- Line 386: Trailing whitespace
- Line 391: Trailing whitespace
- Line 396: Trailing whitespace
- Line 401: Trailing whitespace
- Line 414: Trailing whitespace
- Line 422: Trailing whitespace
- Line 426: Trailing whitespace
- Line 439: Trailing whitespace
- Line 442: Trailing whitespace
- Line 444: Trailing whitespace

### tests/test_scheduler_system.py
- Line 16: E402 module level import not at top of file
- Line 17: E402 module level import not at top of file
- Line 18: E402 module level import not at top of file
- Line 38: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 64: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 83: W293 blank line contains whitespace
- Line 86: W293 blank line contains whitespace
- Line 89: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 126: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 148: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 162: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 175: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 182: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 198: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 209: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 257: W293 blank line contains whitespace
- Line 268: W293 blank line contains whitespace
- Line 274: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 285: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 301: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 311: W293 blank line contains whitespace
- Line 318: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 327: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 339: W293 blank line contains whitespace
- Line 345: W293 blank line contains whitespace
- Line 352: W293 blank line contains whitespace
- Line 355: W293 blank line contains whitespace
- Line 366: W293 blank line contains whitespace
- Line 375: W293 blank line contains whitespace
- Line 382: W293 blank line contains whitespace
- Line 385: W293 blank line contains whitespace
- Line 389: W293 blank line contains whitespace
- Line 403: W293 blank line contains whitespace
- Line 421: W293 blank line contains whitespace
- Line 424: W293 blank line contains whitespace
- Line 430: W293 blank line contains whitespace
- Line 434: W293 blank line contains whitespace
- Line 442: W293 blank line contains whitespace
- Line 448: W293 blank line contains whitespace
- Line 451: W293 blank line contains whitespace
- Line 456: W293 blank line contains whitespace
- Line 463: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 477: W293 blank line contains whitespace
- Line 481: W293 blank line contains whitespace
- Line 497: W293 blank line contains whitespace
- Line 500: W293 blank line contains whitespace
- Line 506: W293 blank line contains whitespace
- Line 511: W293 blank line contains whitespace
- Line 519: W293 blank line contains whitespace
- Line 522: W293 blank line contains whitespace
- Line 528: W293 blank line contains whitespace
- Line 533: W293 blank line contains whitespace
- Line 541: W293 blank line contains whitespace
- Line 544: W293 blank line contains whitespace
- Line 550: W293 blank line contains whitespace
- Line 555: W293 blank line contains whitespace
- Line 569: W293 blank line contains whitespace
- Line 573: W293 blank line contains whitespace
- Line 579: W293 blank line contains whitespace
- Line 584: W293 blank line contains whitespace
- Line 591: W293 blank line contains whitespace
- Line 594: E501 line too long (80 > 79 characters)
- Line 596: W293 blank line contains whitespace
- Line 605: W293 blank line contains whitespace
- Line 609: W293 blank line contains whitespace
- Line 617: W293 blank line contains whitespace
- Line 620: W293 blank line contains whitespace
- Line 629: W293 blank line contains whitespace
- Line 633: W293 blank line contains whitespace
- Line 636: W293 blank line contains whitespace
- Line 38: Trailing whitespace
- Line 41: Trailing whitespace
- Line 52: Trailing whitespace
- Line 64: Trailing whitespace
- Line 67: Trailing whitespace
- Line 74: Trailing whitespace
- Line 77: Trailing whitespace
- Line 83: Trailing whitespace
- Line 86: Trailing whitespace
- Line 89: Trailing whitespace
- Line 91: Trailing whitespace
- Line 98: Trailing whitespace
- Line 104: Trailing whitespace
- Line 107: Trailing whitespace
- Line 110: Trailing whitespace
- Line 112: Trailing whitespace
- Line 120: Trailing whitespace
- Line 123: Trailing whitespace
- Line 126: Trailing whitespace
- Line 133: Trailing whitespace
- Line 140: Trailing whitespace
- Line 144: Trailing whitespace
- Line 148: Trailing whitespace
- Line 156: Trailing whitespace
- Line 159: Trailing whitespace
- Line 162: Trailing whitespace
- Line 168: Trailing whitespace
- Line 175: Trailing whitespace
- Line 178: Trailing whitespace
- Line 182: Trailing whitespace
- Line 191: Trailing whitespace
- Line 198: Trailing whitespace
- Line 204: Trailing whitespace
- Line 209: Trailing whitespace
- Line 243: Trailing whitespace
- Line 254: Trailing whitespace
- Line 257: Trailing whitespace
- Line 268: Trailing whitespace
- Line 274: Trailing whitespace
- Line 280: Trailing whitespace
- Line 285: Trailing whitespace
- Line 290: Trailing whitespace
- Line 298: Trailing whitespace
- Line 301: Trailing whitespace
- Line 307: Trailing whitespace
- Line 311: Trailing whitespace
- Line 318: Trailing whitespace
- Line 324: Trailing whitespace
- Line 327: Trailing whitespace
- Line 333: Trailing whitespace
- Line 339: Trailing whitespace
- Line 345: Trailing whitespace
- Line 352: Trailing whitespace
- Line 355: Trailing whitespace
- Line 366: Trailing whitespace
- Line 375: Trailing whitespace
- Line 382: Trailing whitespace
- Line 385: Trailing whitespace
- Line 389: Trailing whitespace
- Line 403: Trailing whitespace
- Line 421: Trailing whitespace
- Line 424: Trailing whitespace
- Line 430: Trailing whitespace
- Line 434: Trailing whitespace
- Line 442: Trailing whitespace
- Line 448: Trailing whitespace
- Line 451: Trailing whitespace
- Line 456: Trailing whitespace
- Line 463: Trailing whitespace
- Line 467: Trailing whitespace
- Line 477: Trailing whitespace
- Line 481: Trailing whitespace
- Line 497: Trailing whitespace
- Line 500: Trailing whitespace
- Line 506: Trailing whitespace
- Line 511: Trailing whitespace
- Line 519: Trailing whitespace
- Line 522: Trailing whitespace
- Line 528: Trailing whitespace
- Line 533: Trailing whitespace
- Line 541: Trailing whitespace
- Line 544: Trailing whitespace
- Line 550: Trailing whitespace
- Line 555: Trailing whitespace
- Line 569: Trailing whitespace
- Line 573: Trailing whitespace
- Line 579: Trailing whitespace
- Line 584: Trailing whitespace
- Line 591: Trailing whitespace
- Line 596: Trailing whitespace
- Line 605: Trailing whitespace
- Line 609: Trailing whitespace
- Line 617: Trailing whitespace
- Line 620: Trailing whitespace
- Line 629: Trailing whitespace
- Line 633: Trailing whitespace
- Line 636: Trailing whitespace

### tests/test_webui_server.py
- Line 14: E402 module level import not at top of file
- Line 50: E501 line too long (83 > 79 characters)

### src/piwardrive/api/auth/dependencies.py
- Line 23: E501 line too long (82 > 79 characters)

### tests/test_core_application.py
- Line 16: E501 line too long (89 > 79 characters)
- Line 23: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 36: W293 blank line contains whitespace
- Line 40: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 47: W293 blank line contains whitespace
- Line 53: E501 line too long (88 > 79 characters)
- Line 55: W293 blank line contains whitespace
- Line 57: E501 line too long (105 > 79 characters)
- Line 58: W293 blank line contains whitespace
- Line 64: E501 line too long (82 > 79 characters)
- Line 68: W293 blank line contains whitespace
- Line 72: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 81: W293 blank line contains whitespace
- Line 86: E501 line too long (82 > 79 characters)
- Line 87: E501 line too long (83 > 79 characters)
- Line 88: E501 line too long (91 > 79 characters)
- Line 89: E501 line too long (93 > 79 characters)
- Line 90: W293 blank line contains whitespace
- Line 92: W293 blank line contains whitespace
- Line 96: W293 blank line contains whitespace
- Line 105: W293 blank line contains whitespace
- Line 112: W293 blank line contains whitespace
- Line 117: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 131: W293 blank line contains whitespace
- Line 143: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 150: W293 blank line contains whitespace
- Line 156: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 171: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 181: W293 blank line contains whitespace
- Line 185: W293 blank line contains whitespace
- Line 192: W293 blank line contains whitespace
- Line 202: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 213: W293 blank line contains whitespace
- Line 219: W293 blank line contains whitespace
- Line 223: W293 blank line contains whitespace
- Line 235: W293 blank line contains whitespace
- Line 239: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 254: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 272: E501 line too long (83 > 79 characters)
- Line 273: E501 line too long (82 > 79 characters)
- Line 274: W293 blank line contains whitespace
- Line 280: W293 blank line contains whitespace
- Line 287: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 292: E501 line too long (81 > 79 characters)
- Line 299: W293 blank line contains whitespace
- Line 303: W293 blank line contains whitespace
- Line 307: W293 blank line contains whitespace
- Line 310: W293 blank line contains whitespace
- Line 314: W293 blank line contains whitespace
- Line 318: W293 blank line contains whitespace
- Line 322: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 329: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 337: W293 blank line contains whitespace
- Line 344: W293 blank line contains whitespace
- Line 353: W293 blank line contains whitespace
- Line 359: W293 blank line contains whitespace
- Line 363: W293 blank line contains whitespace
- Line 367: W293 blank line contains whitespace
- Line 374: E501 line too long (86 > 79 characters)
- Line 382: W293 blank line contains whitespace
- Line 383: E501 line too long (82 > 79 characters)
- Line 386: W293 blank line contains whitespace
- Line 389: W293 blank line contains whitespace
- Line 393: E501 line too long (80 > 79 characters)
- Line 394: E501 line too long (86 > 79 characters)
- Line 396: W293 blank line contains whitespace
- Line 404: W293 blank line contains whitespace
- Line 407: W293 blank line contains whitespace
- Line 411: W293 blank line contains whitespace
- Line 415: W293 blank line contains whitespace
- Line 418: W293 blank line contains whitespace
- Line 23: Trailing whitespace
- Line 31: Trailing whitespace
- Line 36: Trailing whitespace
- Line 40: Trailing whitespace
- Line 45: Trailing whitespace
- Line 47: Trailing whitespace
- Line 55: Trailing whitespace
- Line 58: Trailing whitespace
- Line 68: Trailing whitespace
- Line 72: Trailing whitespace
- Line 74: Trailing whitespace
- Line 81: Trailing whitespace
- Line 90: Trailing whitespace
- Line 92: Trailing whitespace
- Line 96: Trailing whitespace
- Line 105: Trailing whitespace
- Line 112: Trailing whitespace
- Line 117: Trailing whitespace
- Line 122: Trailing whitespace
- Line 131: Trailing whitespace
- Line 143: Trailing whitespace
- Line 147: Trailing whitespace
- Line 150: Trailing whitespace
- Line 156: Trailing whitespace
- Line 165: Trailing whitespace
- Line 168: Trailing whitespace
- Line 171: Trailing whitespace
- Line 176: Trailing whitespace
- Line 181: Trailing whitespace
- Line 185: Trailing whitespace
- Line 192: Trailing whitespace
- Line 202: Trailing whitespace
- Line 205: Trailing whitespace
- Line 208: Trailing whitespace
- Line 213: Trailing whitespace
- Line 219: Trailing whitespace
- Line 223: Trailing whitespace
- Line 235: Trailing whitespace
- Line 239: Trailing whitespace
- Line 243: Trailing whitespace
- Line 254: Trailing whitespace
- Line 262: Trailing whitespace
- Line 267: Trailing whitespace
- Line 274: Trailing whitespace
- Line 280: Trailing whitespace
- Line 287: Trailing whitespace
- Line 291: Trailing whitespace
- Line 299: Trailing whitespace
- Line 303: Trailing whitespace
- Line 307: Trailing whitespace
- Line 310: Trailing whitespace
- Line 314: Trailing whitespace
- Line 318: Trailing whitespace
- Line 322: Trailing whitespace
- Line 326: Trailing whitespace
- Line 329: Trailing whitespace
- Line 333: Trailing whitespace
- Line 337: Trailing whitespace
- Line 344: Trailing whitespace
- Line 353: Trailing whitespace
- Line 359: Trailing whitespace
- Line 363: Trailing whitespace
- Line 367: Trailing whitespace
- Line 382: Trailing whitespace
- Line 386: Trailing whitespace
- Line 389: Trailing whitespace
- Line 396: Trailing whitespace
- Line 404: Trailing whitespace
- Line 407: Trailing whitespace
- Line 411: Trailing whitespace
- Line 415: Trailing whitespace
- Line 418: Trailing whitespace

### src/piwardrive/integrations/sigint_suite/plugins.py
- Line 58: E501 line too long (85 > 79 characters)

### src/piwardrive/cloud_export.py
- Line 25: E501 line too long (81 > 79 characters)

### src/piwardrive/routes/cellular.py
- Line 68: E501 line too long (80 > 79 characters)

### src/piwardrive/export.py
- Line 25: E501 line too long (81 > 79 characters)
- Line 44: E501 line too long (83 > 79 characters)
- Line 152: E501 line too long (80 > 79 characters)
- Line 209: E501 line too long (81 > 79 characters)
- Line 311: E501 line too long (88 > 79 characters)
- Line 312: E501 line too long (84 > 79 characters)
- Line 318: E501 line too long (80 > 79 characters)

### scripts/localize_aps.py
- Line 11: E501 line too long (88 > 79 characters)
- Line 20: E501 line too long (87 > 79 characters)
- Line 42: E501 line too long (88 > 79 characters)

### src/piwardrive/integrations/sigint_suite/bluetooth/scanner.py
- Line 25: E501 line too long (85 > 79 characters)
- Line 45: E203 whitespace before ':'
- Line 45: E501 line too long (83 > 79 characters)
- Line 90: E501 line too long (80 > 79 characters)
- Line 118: E501 line too long (86 > 79 characters)
- Line 147: E203 whitespace before ':'
- Line 162: E501 line too long (83 > 79 characters)
- Line 177: E203 whitespace before ':'
- Line 177: E501 line too long (83 > 79 characters)
- Line 189: E501 line too long (84 > 79 characters)

### src/piwardrive/integrations/sigint_suite/wifi/scanner.py
- Line 16: E501 line too long (88 > 79 characters)
- Line 27: E501 line too long (80 > 79 characters)
- Line 81: E501 line too long (81 > 79 characters)
- Line 95: E501 line too long (86 > 79 characters)
- Line 119: E501 line too long (85 > 79 characters)
- Line 126: E501 line too long (85 > 79 characters)
- Line 156: E501 line too long (85 > 79 characters)
- Line 163: E501 line too long (85 > 79 characters)
- Line 189: E501 line too long (82 > 79 characters)
- Line 190: E501 line too long (84 > 79 characters)

### src/piwardrive/widgets/disk_trend.py
- Line 14: E501 line too long (80 > 79 characters)

### src/piwardrive/map/vector_tile_customizer.py
- Line 31: E501 line too long (83 > 79 characters)
- Line 34: E501 line too long (81 > 79 characters)
- Line 42: E501 line too long (82 > 79 characters)
- Line 70: E501 line too long (82 > 79 characters)

### tests/staging/test_staging_environment.py
- Line 66: E501 line too long (83 > 79 characters)
- Line 102: E501 line too long (98 > 79 characters)
- Line 106: E501 line too long (101 > 79 characters)
- Line 109: E501 line too long (81 > 79 characters)
- Line 110: E501 line too long (84 > 79 characters)
- Line 123: E501 line too long (81 > 79 characters)
- Line 139: E302 expected 2 blank lines, found 1
- Line 169: E302 expected 2 blank lines, found 1
- Line 193: E501 line too long (84 > 79 characters)
- Line 194: E501 line too long (107 > 79 characters)
- Line 200: E501 line too long (80 > 79 characters)
- Line 202: E722 do not use bare 'except'
- Line 212: E501 line too long (80 > 79 characters)
- Line 217: E501 line too long (81 > 79 characters)
- Line 225: E501 line too long (87 > 79 characters)
- Line 230: E501 line too long (80 > 79 characters)
- Line 247: E722 do not use bare 'except'
- Line 254: E501 line too long (83 > 79 characters)
- Line 265: E501 line too long (90 > 79 characters)
- Line 267: E302 expected 2 blank lines, found 1
- Line 280: E501 line too long (82 > 79 characters)
- Line 312: E501 line too long (87 > 79 characters)
- Line 384: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/integrations/sigint_suite/cellular/parsers/__init__.py
- Line 43: E501 line too long (87 > 79 characters)

### src/piwardrive/setup_wizard.py
- Line 28: E501 line too long (86 > 79 characters)

### src/piwardrive/api/widget_marketplace.py
- Line 15: E501 line too long (82 > 79 characters)

### tests/test_main_application.py
- Line 14: E402 module level import not at top of file
- Line 15: E402 module level import not at top of file
- Line 37: W293 blank line contains whitespace
- Line 51: W293 blank line contains whitespace
- Line 58: W293 blank line contains whitespace
- Line 63: W293 blank line contains whitespace
- Line 67: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 82: E501 line too long (82 > 79 characters)
- Line 90: W293 blank line contains whitespace
- Line 111: W293 blank line contains whitespace
- Line 114: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 139: W293 blank line contains whitespace
- Line 147: W293 blank line contains whitespace
- Line 158: W293 blank line contains whitespace
- Line 166: W293 blank line contains whitespace
- Line 176: W293 blank line contains whitespace
- Line 184: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 202: W293 blank line contains whitespace
- Line 212: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 229: W293 blank line contains whitespace
- Line 237: W293 blank line contains whitespace
- Line 247: W293 blank line contains whitespace
- Line 255: W293 blank line contains whitespace
- Line 267: W293 blank line contains whitespace
- Line 272: W293 blank line contains whitespace
- Line 275: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 286: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 302: W293 blank line contains whitespace
- Line 315: W293 blank line contains whitespace
- Line 324: W293 blank line contains whitespace
- Line 333: W293 blank line contains whitespace
- Line 342: W293 blank line contains whitespace
- Line 37: Trailing whitespace
- Line 51: Trailing whitespace
- Line 58: Trailing whitespace
- Line 63: Trailing whitespace
- Line 67: Trailing whitespace
- Line 76: Trailing whitespace
- Line 90: Trailing whitespace
- Line 111: Trailing whitespace
- Line 114: Trailing whitespace
- Line 120: Trailing whitespace
- Line 123: Trailing whitespace
- Line 139: Trailing whitespace
- Line 147: Trailing whitespace
- Line 158: Trailing whitespace
- Line 166: Trailing whitespace
- Line 176: Trailing whitespace
- Line 184: Trailing whitespace
- Line 194: Trailing whitespace
- Line 202: Trailing whitespace
- Line 212: Trailing whitespace
- Line 220: Trailing whitespace
- Line 229: Trailing whitespace
- Line 237: Trailing whitespace
- Line 247: Trailing whitespace
- Line 255: Trailing whitespace
- Line 267: Trailing whitespace
- Line 272: Trailing whitespace
- Line 275: Trailing whitespace
- Line 282: Trailing whitespace
- Line 286: Trailing whitespace
- Line 294: Trailing whitespace
- Line 302: Trailing whitespace
- Line 315: Trailing whitespace
- Line 324: Trailing whitespace
- Line 333: Trailing whitespace
- Line 342: Trailing whitespace

### src/remote_sync/__init__.py
- Line 55: E501 line too long (82 > 79 characters)
- Line 59: E501 line too long (83 > 79 characters)
- Line 81: E501 line too long (84 > 79 characters)
- Line 92: E501 line too long (81 > 79 characters)
- Line 97: E501 line too long (88 > 79 characters)
- Line 189: E501 line too long (81 > 79 characters)
- Line 191: E501 line too long (82 > 79 characters)

### src/piwardrive/performance/optimization.py
- Line 72: E302 expected 2 blank lines, found 1
- Line 98: E302 expected 2 blank lines, found 1
- Line 120: E303 too many blank lines (3)
- Line 192: E501 line too long (88 > 79 characters)
- Line 207: W503 line break before binary operator
- Line 210: W503 line break before binary operator
- Line 211: E501 line too long (80 > 79 characters)
- Line 213: W503 line break before binary operator
- Line 214: E501 line too long (85 > 79 characters)
- Line 392: E303 too many blank lines (3)
- Line 395: E501 line too long (80 > 79 characters)
- Line 425: W503 line break before binary operator
- Line 447: E303 too many blank lines (3)
- Line 536: E501 line too long (110 > 79 characters)
- Line 619: E501 line too long (82 > 79 characters)
- Line 790: E303 too many blank lines (3)
- Line 803: E501 line too long (80 > 79 characters)
- Line 825: E501 line too long (80 > 79 characters)
- Line 827: E251 unexpected spaces around keyword / parameter equals
- Line 829: E501 line too long (88 > 79 characters)
- Line 844: E501 line too long (86 > 79 characters)
- Line 849: E303 too many blank lines (3)
- Line 853: E501 line too long (80 > 79 characters)
- Line 973: E226 missing whitespace around arithmetic operator
- Line 973: E501 line too long (88 > 79 characters)
- Line 1006: E501 line too long (80 > 79 characters)
- Line 1007: E501 line too long (87 > 79 characters)
- Line 1024: E501 line too long (82 > 79 characters)
- Line 1032: E501 line too long (92 > 79 characters)
- Line 1097: W293 blank line contains whitespace
- Line 1129: E501 line too long (88 > 79 characters)
- Line 1134: E501 line too long (110 > 79 characters)
- Line 1139: E501 line too long (94 > 79 characters)
- Line 1147: E501 line too long (92 > 79 characters)
- Line 1150: E501 line too long (90 > 79 characters)
- Line 1156: E501 line too long (88 > 79 characters)
- Line 1159: E501 line too long (84 > 79 characters)
- Line 1159: E501 line too long (84 > 79 characters)
- Line 1160: E128 continuation line under-indented for visual indent
- Line 1172: E501 line too long (84 > 79 characters)
- Line 1177: E305 expected 2 blank lines after class or function definition, found 1
- Line 1097: Trailing whitespace

### src/piwardrive/api/system/endpoints.py
- Line 63: E501 line too long (89 > 79 characters)
- Line 81: E501 line too long (85 > 79 characters)

### scripts/export_db.py
- Line 24: E501 line too long (82 > 79 characters)
- Line 28: E501 line too long (80 > 79 characters)

### comprehensive_qa_fix.py
- Line 49: E501 line too long (94 > 79 characters)
- Line 50: E128 continuation line under-indented for visual indent
- Line 51: E128 continuation line under-indented for visual indent
- Line 75: E501 line too long (81 > 79 characters)
- Line 95: E501 line too long (88 > 79 characters)
- Line 122: E501 line too long (81 > 79 characters)
- Line 127: E501 line too long (90 > 79 characters)
- Line 128: E128 continuation line under-indented for visual indent
- Line 167: E128 continuation line under-indented for visual indent
- Line 206: E501 line too long (80 > 79 characters)
- Line 207: E501 line too long (80 > 79 characters)
- Line 220: E501 line too long (87 > 79 characters)
- Line 253: E128 continuation line under-indented for visual indent
- Line 254: E128 continuation line under-indented for visual indent
- Line 255: E128 continuation line under-indented for visual indent
- Line 256: E128 continuation line under-indented for visual indent
- Line 257: E128 continuation line under-indented for visual indent
- Line 314: E226 missing whitespace around arithmetic operator
- Line 316: E226 missing whitespace around arithmetic operator
- Line 328: E501 line too long (106 > 79 characters)
- Line 329: E128 continuation line under-indented for visual indent
- Line 334: E501 line too long (91 > 79 characters)
- Line 335: E128 continuation line under-indented for visual indent
- Line 341: E305 expected 2 blank lines after class or function definition, found 1

### src/piwardrive/security.py
- Line 52: E501 line too long (92 > 79 characters)

### src/piwardrive/direction_finding/integration.py
- Line 120: E501 line too long (86 > 79 characters)
- Line 125: E501 line too long (86 > 79 characters)
- Line 171: E501 line too long (82 > 79 characters)
- Line 185: E501 line too long (83 > 79 characters)
- Line 187: E501 line too long (84 > 79 characters)
- Line 227: E501 line too long (83 > 79 characters)
- Line 300: E501 line too long (81 > 79 characters)
- Line 373: E501 line too long (82 > 79 characters)

### src/piwardrive/cache.py
- Line 20: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 34: W293 blank line contains whitespace
- Line 46: W293 blank line contains whitespace
- Line 60: W293 blank line contains whitespace
- Line 20: Trailing whitespace
- Line 31: Trailing whitespace
- Line 34: Trailing whitespace
- Line 46: Trailing whitespace
- Line 60: Trailing whitespace

### tests/test_widget_system_comprehensive.py
- Line 22: W293 blank line contains whitespace
- Line 29: W293 blank line contains whitespace
- Line 33: W293 blank line contains whitespace
- Line 36: W293 blank line contains whitespace
- Line 40: W293 blank line contains whitespace
- Line 43: W293 blank line contains whitespace
- Line 49: W293 blank line contains whitespace
- Line 52: W293 blank line contains whitespace
- Line 60: W293 blank line contains whitespace
- Line 68: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 82: E501 line too long (81 > 79 characters)
- Line 85: W293 blank line contains whitespace
- Line 87: W293 blank line contains whitespace
- Line 90: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 100: W293 blank line contains whitespace
- Line 103: W293 blank line contains whitespace
- Line 106: W293 blank line contains whitespace
- Line 109: W293 blank line contains whitespace
- Line 113: W293 blank line contains whitespace
- Line 118: W293 blank line contains whitespace
- Line 123: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 132: W293 blank line contains whitespace
- Line 137: W293 blank line contains whitespace
- Line 141: W293 blank line contains whitespace
- Line 144: W293 blank line contains whitespace
- Line 150: W293 blank line contains whitespace
- Line 154: W293 blank line contains whitespace
- Line 158: E501 line too long (91 > 79 characters)
- Line 160: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 170: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 180: W293 blank line contains whitespace
- Line 184: E501 line too long (91 > 79 characters)
- Line 186: E501 line too long (80 > 79 characters)
- Line 188: W293 blank line contains whitespace
- Line 191: W293 blank line contains whitespace
- Line 194: W293 blank line contains whitespace
- Line 197: E501 line too long (91 > 79 characters)
- Line 199: E501 line too long (90 > 79 characters)
- Line 201: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 207: W293 blank line contains whitespace
- Line 210: E501 line too long (87 > 79 characters)
- Line 212: E501 line too long (88 > 79 characters)
- Line 214: W293 blank line contains whitespace
- Line 217: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 223: E501 line too long (93 > 79 characters)
- Line 225: E501 line too long (80 > 79 characters)
- Line 227: W293 blank line contains whitespace
- Line 230: W293 blank line contains whitespace
- Line 233: W293 blank line contains whitespace
- Line 236: E501 line too long (93 > 79 characters)
- Line 238: E501 line too long (83 > 79 characters)
- Line 240: W293 blank line contains whitespace
- Line 243: W293 blank line contains whitespace
- Line 250: W293 blank line contains whitespace
- Line 256: W293 blank line contains whitespace
- Line 259: W293 blank line contains whitespace
- Line 262: W293 blank line contains whitespace
- Line 264: W293 blank line contains whitespace
- Line 268: W293 blank line contains whitespace
- Line 271: W293 blank line contains whitespace
- Line 276: W293 blank line contains whitespace
- Line 282: W293 blank line contains whitespace
- Line 285: W293 blank line contains whitespace
- Line 290: W293 blank line contains whitespace
- Line 292: W293 blank line contains whitespace
- Line 298: W293 blank line contains whitespace
- Line 300: W293 blank line contains whitespace
- Line 306: W293 blank line contains whitespace
- Line 309: W293 blank line contains whitespace
- Line 311: W293 blank line contains whitespace
- Line 315: W293 blank line contains whitespace
- Line 323: W293 blank line contains whitespace
- Line 330: W293 blank line contains whitespace
- Line 332: W293 blank line contains whitespace
- Line 336: W293 blank line contains whitespace
- Line 340: W293 blank line contains whitespace
- Line 347: W293 blank line contains whitespace
- Line 352: W293 blank line contains whitespace
- Line 355: W293 blank line contains whitespace
- Line 358: W293 blank line contains whitespace
- Line 362: W293 blank line contains whitespace
- Line 365: W293 blank line contains whitespace
- Line 369: W293 blank line contains whitespace
- Line 372: W293 blank line contains whitespace
- Line 375: W293 blank line contains whitespace
- Line 378: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 388: W293 blank line contains whitespace
- Line 395: W293 blank line contains whitespace
- Line 398: W293 blank line contains whitespace
- Line 401: W293 blank line contains whitespace
- Line 404: W293 blank line contains whitespace
- Line 410: W293 blank line contains whitespace
- Line 413: W293 blank line contains whitespace
- Line 416: W293 blank line contains whitespace
- Line 418: W293 blank line contains whitespace
- Line 423: W293 blank line contains whitespace
- Line 426: W293 blank line contains whitespace
- Line 428: W293 blank line contains whitespace
- Line 432: W293 blank line contains whitespace
- Line 437: E501 line too long (101 > 79 characters)
- Line 438: W293 blank line contains whitespace
- Line 439: E501 line too long (91 > 79 characters)
- Line 444: W293 blank line contains whitespace
- Line 451: W293 blank line contains whitespace
- Line 459: W293 blank line contains whitespace
- Line 463: E501 line too long (85 > 79 characters)
- Line 468: W293 blank line contains whitespace
- Line 470: W293 blank line contains whitespace
- Line 475: W293 blank line contains whitespace
- Line 479: W293 blank line contains whitespace
- Line 484: W293 blank line contains whitespace
- Line 487: W293 blank line contains whitespace
- Line 490: W293 blank line contains whitespace
- Line 496: W293 blank line contains whitespace
- Line 500: W293 blank line contains whitespace
- Line 504: W293 blank line contains whitespace
- Line 507: W293 blank line contains whitespace
- Line 510: W293 blank line contains whitespace
- Line 514: W293 blank line contains whitespace
- Line 516: E501 line too long (87 > 79 characters)
- Line 520: W293 blank line contains whitespace
- Line 525: W293 blank line contains whitespace
- Line 529: W293 blank line contains whitespace
- Line 531: E501 line too long (81 > 79 characters)
- Line 535: W293 blank line contains whitespace
- Line 537: E501 line too long (81 > 79 characters)
- Line 539: W293 blank line contains whitespace
- Line 545: W293 blank line contains whitespace
- Line 22: Trailing whitespace
- Line 29: Trailing whitespace
- Line 33: Trailing whitespace
- Line 36: Trailing whitespace
- Line 40: Trailing whitespace
- Line 43: Trailing whitespace
- Line 49: Trailing whitespace
- Line 52: Trailing whitespace
- Line 60: Trailing whitespace
- Line 68: Trailing whitespace
- Line 74: Trailing whitespace
- Line 76: Trailing whitespace
- Line 79: Trailing whitespace
- Line 85: Trailing whitespace
- Line 87: Trailing whitespace
- Line 90: Trailing whitespace
- Line 94: Trailing whitespace
- Line 100: Trailing whitespace
- Line 103: Trailing whitespace
- Line 106: Trailing whitespace
- Line 109: Trailing whitespace
- Line 113: Trailing whitespace
- Line 118: Trailing whitespace
- Line 123: Trailing whitespace
- Line 128: Trailing whitespace
- Line 132: Trailing whitespace
- Line 137: Trailing whitespace
- Line 141: Trailing whitespace
- Line 144: Trailing whitespace
- Line 150: Trailing whitespace
- Line 154: Trailing whitespace
- Line 160: Trailing whitespace
- Line 165: Trailing whitespace
- Line 170: Trailing whitespace
- Line 173: Trailing whitespace
- Line 180: Trailing whitespace
- Line 188: Trailing whitespace
- Line 191: Trailing whitespace
- Line 194: Trailing whitespace
- Line 201: Trailing whitespace
- Line 204: Trailing whitespace
- Line 207: Trailing whitespace
- Line 214: Trailing whitespace
- Line 217: Trailing whitespace
- Line 220: Trailing whitespace
- Line 227: Trailing whitespace
- Line 230: Trailing whitespace
- Line 233: Trailing whitespace
- Line 240: Trailing whitespace
- Line 243: Trailing whitespace
- Line 250: Trailing whitespace
- Line 256: Trailing whitespace
- Line 259: Trailing whitespace
- Line 262: Trailing whitespace
- Line 264: Trailing whitespace
- Line 268: Trailing whitespace
- Line 271: Trailing whitespace
- Line 276: Trailing whitespace
- Line 282: Trailing whitespace
- Line 285: Trailing whitespace
- Line 290: Trailing whitespace
- Line 292: Trailing whitespace
- Line 298: Trailing whitespace
- Line 300: Trailing whitespace
- Line 306: Trailing whitespace
- Line 309: Trailing whitespace
- Line 311: Trailing whitespace
- Line 315: Trailing whitespace
- Line 323: Trailing whitespace
- Line 330: Trailing whitespace
- Line 332: Trailing whitespace
- Line 336: Trailing whitespace
- Line 340: Trailing whitespace
- Line 347: Trailing whitespace
- Line 352: Trailing whitespace
- Line 355: Trailing whitespace
- Line 358: Trailing whitespace
- Line 362: Trailing whitespace
- Line 365: Trailing whitespace
- Line 369: Trailing whitespace
- Line 372: Trailing whitespace
- Line 375: Trailing whitespace
- Line 378: Trailing whitespace
- Line 381: Trailing whitespace
- Line 388: Trailing whitespace
- Line 395: Trailing whitespace
- Line 398: Trailing whitespace
- Line 401: Trailing whitespace
- Line 404: Trailing whitespace
- Line 410: Trailing whitespace
- Line 413: Trailing whitespace
- Line 416: Trailing whitespace
- Line 418: Trailing whitespace
- Line 423: Trailing whitespace
- Line 426: Trailing whitespace
- Line 428: Trailing whitespace
- Line 432: Trailing whitespace
- Line 438: Trailing whitespace
- Line 444: Trailing whitespace
- Line 451: Trailing whitespace
- Line 459: Trailing whitespace
- Line 468: Trailing whitespace
- Line 470: Trailing whitespace
- Line 475: Trailing whitespace
- Line 479: Trailing whitespace
- Line 484: Trailing whitespace
- Line 487: Trailing whitespace
- Line 490: Trailing whitespace
- Line 496: Trailing whitespace
- Line 500: Trailing whitespace
- Line 504: Trailing whitespace
- Line 507: Trailing whitespace
- Line 510: Trailing whitespace
- Line 514: Trailing whitespace
- Line 520: Trailing whitespace
- Line 525: Trailing whitespace
- Line 529: Trailing whitespace
- Line 535: Trailing whitespace
- Line 539: Trailing whitespace
- Line 545: Trailing whitespace

### src/piwardrive/integrations/sigint.py
- Line 11: E501 line too long (80 > 79 characters)

### tests/test_analysis_extra.py
- Line 13: E501 line too long (80 > 79 characters)
- Line 36: E203 whitespace before ':'
- Line 36: E501 line too long (88 > 79 characters)
- Line 121: E203 whitespace before ':'
- Line 121: E501 line too long (88 > 79 characters)
- Line 162: E501 line too long (84 > 79 characters)

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 81: E501 line too long (92 > 79 characters)

### src/piwardrive/api/websockets/events.py
- Line 33: E501 line too long (85 > 79 characters)

### src/piwardrive/error_middleware.py
- Line 24: W293 blank line contains whitespace
- Line 27: E501 line too long (88 > 79 characters)
- Line 33: E501 line too long (87 > 79 characters)
- Line 36: W293 blank line contains whitespace
- Line 40: W293 blank line contains whitespace
- Line 24: Trailing whitespace
- Line 36: Trailing whitespace
- Line 40: Trailing whitespace

### tests/test_route_prefetch.py
- Line 17: W503 line break before binary operator

### src/piwardrive/widgets/handshake_counter.py
- Line 35: E501 line too long (82 > 79 characters)

### tests/test_tower_tracking.py
- Line 42: E501 line too long (80 > 79 characters)

### src/piwardrive/widget_manager.py
- Line 38: W293 blank line contains whitespace
- Line 49: E501 line too long (80 > 79 characters)
- Line 95: E501 line too long (87 > 79 characters)
- Line 121: W503 line break before binary operator
- Line 122: W503 line break before binary operator
- Line 38: Trailing whitespace

### scripts/generate_openapi.py
- Line 15: E402 module level import not at top of file
- Line 19: E501 line too long (80 > 79 characters)

### tests/test_service.py
- Line 69: E501 line too long (84 > 79 characters)
- Line 79: E501 line too long (82 > 79 characters)
- Line 90: E501 line too long (82 > 79 characters)
- Line 111: E501 line too long (80 > 79 characters)
- Line 114: E501 line too long (80 > 79 characters)
- Line 120: E501 line too long (80 > 79 characters)
- Line 121: E501 line too long (80 > 79 characters)
- Line 122: E501 line too long (86 > 79 characters)
- Line 234: E501 line too long (80 > 79 characters)
- Line 237: E501 line too long (80 > 79 characters)
- Line 243: E501 line too long (80 > 79 characters)
- Line 244: E501 line too long (80 > 79 characters)
- Line 245: E501 line too long (86 > 79 characters)
- Line 287: E501 line too long (80 > 79 characters)
- Line 290: E501 line too long (80 > 79 characters)
- Line 296: E501 line too long (80 > 79 characters)
- Line 297: E501 line too long (80 > 79 characters)
- Line 298: E501 line too long (86 > 79 characters)
- Line 392: E501 line too long (80 > 79 characters)
- Line 395: E501 line too long (80 > 79 characters)
- Line 401: E501 line too long (80 > 79 characters)
- Line 402: E501 line too long (80 > 79 characters)
- Line 403: E501 line too long (86 > 79 characters)
- Line 464: E501 line too long (86 > 79 characters)
- Line 470: E501 line too long (86 > 79 characters)
- Line 487: E501 line too long (80 > 79 characters)
- Line 490: E501 line too long (80 > 79 characters)
- Line 493: E501 line too long (80 > 79 characters)
- Line 515: E501 line too long (80 > 79 characters)
- Line 518: E501 line too long (80 > 79 characters)
- Line 521: E501 line too long (80 > 79 characters)
- Line 531: E501 line too long (85 > 79 characters)
- Line 600: E501 line too long (81 > 79 characters)
- Line 605: E501 line too long (80 > 79 characters)
- Line 620: E501 line too long (86 > 79 characters)
- Line 630: E501 line too long (80 > 79 characters)
- Line 632: E501 line too long (82 > 79 characters)
- Line 649: E501 line too long (81 > 79 characters)
- Line 660: E501 line too long (82 > 79 characters)
- Line 676: E501 line too long (81 > 79 characters)

### src/piwardrive/config.py
- Line 4: E501 line too long (80 > 79 characters)

### src/piwardrive/migrations/runner.py
- Line 14: E501 line too long (85 > 79 characters)
- Line 20: E501 line too long (87 > 79 characters)

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 22: E501 line too long (80 > 79 characters)
- Line 29: E501 line too long (81 > 79 characters)
- Line 74: E501 line too long (81 > 79 characters)
- Line 127: E501 line too long (84 > 79 characters)

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 20: E501 line too long (81 > 79 characters)
- Line 40: E501 line too long (85 > 79 characters)
- Line 64: E501 line too long (85 > 79 characters)
- Line 88: E501 line too long (84 > 79 characters)

### src/piwardrive/resource_manager.py
- Line 21: W293 blank line contains whitespace
- Line 31: E501 line too long (80 > 79 characters)
- Line 34: E501 line too long (84 > 79 characters)
- Line 36: W293 blank line contains whitespace
- Line 41: W293 blank line contains whitespace
- Line 53: E501 line too long (80 > 79 characters)
- Line 55: W293 blank line contains whitespace
- Line 59: W293 blank line contains whitespace
- Line 21: Trailing whitespace
- Line 36: Trailing whitespace
- Line 41: Trailing whitespace
- Line 55: Trailing whitespace
- Line 59: Trailing whitespace

### service.py
- Line 5: E501 line too long (80 > 79 characters)
- Line 35: E501 line too long (81 > 79 characters)
- Line 38: E501 line too long (86 > 79 characters)

### tests/test_advanced_localization.py
- Line 47: E501 line too long (80 > 79 characters)

### tests/test_widget_system.py
- Line 15: E402 module level import not at top of file
- Line 16: E402 module level import not at top of file
- Line 17: E402 module level import not at top of file
- Line 39: W293 blank line contains whitespace
- Line 42: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 54: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 60: W293 blank line contains whitespace
- Line 62: W293 blank line contains whitespace
- Line 71: W293 blank line contains whitespace
- Line 74: W293 blank line contains whitespace
- Line 77: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 94: W293 blank line contains whitespace
- Line 98: W293 blank line contains whitespace
- Line 101: W293 blank line contains whitespace
- Line 104: W293 blank line contains whitespace
- Line 107: W293 blank line contains whitespace
- Line 119: W293 blank line contains whitespace
- Line 122: W293 blank line contains whitespace
- Line 125: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 137: W293 blank line contains whitespace
- Line 140: W293 blank line contains whitespace
- Line 143: W293 blank line contains whitespace
- Line 152: W293 blank line contains whitespace
- Line 155: W293 blank line contains whitespace
- Line 159: W293 blank line contains whitespace
- Line 162: W293 blank line contains whitespace
- Line 165: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 180: W293 blank line contains whitespace
- Line 183: W293 blank line contains whitespace
- Line 186: W293 blank line contains whitespace
- Line 197: W293 blank line contains whitespace
- Line 201: W293 blank line contains whitespace
- Line 204: W293 blank line contains whitespace
- Line 208: W293 blank line contains whitespace
- Line 220: W293 blank line contains whitespace
- Line 223: W293 blank line contains whitespace
- Line 226: W293 blank line contains whitespace
- Line 229: W293 blank line contains whitespace
- Line 233: W293 blank line contains whitespace
- Line 256: W293 blank line contains whitespace
- Line 259: W293 blank line contains whitespace
- Line 261: W293 blank line contains whitespace
- Line 270: W293 blank line contains whitespace
- Line 273: W293 blank line contains whitespace
- Line 275: W293 blank line contains whitespace
- Line 284: W293 blank line contains whitespace
- Line 287: W293 blank line contains whitespace
- Line 291: W293 blank line contains whitespace
- Line 294: W293 blank line contains whitespace
- Line 297: W293 blank line contains whitespace
- Line 304: E501 line too long (82 > 79 characters)
- Line 308: W293 blank line contains whitespace
- Line 326: W293 blank line contains whitespace
- Line 334: W293 blank line contains whitespace
- Line 341: W293 blank line contains whitespace
- Line 344: W293 blank line contains whitespace
- Line 350: W293 blank line contains whitespace
- Line 373: W293 blank line contains whitespace
- Line 378: W293 blank line contains whitespace
- Line 381: W293 blank line contains whitespace
- Line 384: W293 blank line contains whitespace
- Line 394: W293 blank line contains whitespace
- Line 399: W293 blank line contains whitespace
- Line 402: W293 blank line contains whitespace
- Line 405: W293 blank line contains whitespace
- Line 418: W293 blank line contains whitespace
- Line 423: W293 blank line contains whitespace
- Line 426: W293 blank line contains whitespace
- Line 429: W293 blank line contains whitespace
- Line 445: W293 blank line contains whitespace
- Line 450: W293 blank line contains whitespace
- Line 455: W293 blank line contains whitespace
- Line 460: W293 blank line contains whitespace
- Line 465: W293 blank line contains whitespace
- Line 467: W293 blank line contains whitespace
- Line 475: W293 blank line contains whitespace
- Line 478: W293 blank line contains whitespace
- Line 483: W293 blank line contains whitespace
- Line 486: W293 blank line contains whitespace
- Line 491: W293 blank line contains whitespace
- Line 494: W293 blank line contains whitespace
- Line 502: W293 blank line contains whitespace
- Line 507: W293 blank line contains whitespace
- Line 512: W293 blank line contains whitespace
- Line 515: W293 blank line contains whitespace
- Line 517: W293 blank line contains whitespace
- Line 521: W293 blank line contains whitespace
- Line 528: W293 blank line contains whitespace
- Line 532: W293 blank line contains whitespace
- Line 549: W293 blank line contains whitespace
- Line 552: W293 blank line contains whitespace
- Line 557: W293 blank line contains whitespace
- Line 561: E501 line too long (82 > 79 characters)
- Line 563: W293 blank line contains whitespace
- Line 565: W293 blank line contains whitespace
- Line 568: W293 blank line contains whitespace
- Line 572: W293 blank line contains whitespace
- Line 576: W293 blank line contains whitespace
- Line 585: W293 blank line contains whitespace
- Line 592: W293 blank line contains whitespace
- Line 600: E501 line too long (99 > 79 characters)
- Line 605: W293 blank line contains whitespace
- Line 608: W293 blank line contains whitespace
- Line 612: W293 blank line contains whitespace
- Line 39: Trailing whitespace
- Line 42: Trailing whitespace
- Line 45: Trailing whitespace
- Line 54: Trailing whitespace
- Line 57: Trailing whitespace
- Line 60: Trailing whitespace
- Line 62: Trailing whitespace
- Line 71: Trailing whitespace
- Line 74: Trailing whitespace
- Line 77: Trailing whitespace
- Line 91: Trailing whitespace
- Line 94: Trailing whitespace
- Line 98: Trailing whitespace
- Line 101: Trailing whitespace
- Line 104: Trailing whitespace
- Line 107: Trailing whitespace
- Line 119: Trailing whitespace
- Line 122: Trailing whitespace
- Line 125: Trailing whitespace
- Line 128: Trailing whitespace
- Line 137: Trailing whitespace
- Line 140: Trailing whitespace
- Line 143: Trailing whitespace
- Line 152: Trailing whitespace
- Line 155: Trailing whitespace
- Line 159: Trailing whitespace
- Line 162: Trailing whitespace
- Line 165: Trailing whitespace
- Line 168: Trailing whitespace
- Line 180: Trailing whitespace
- Line 183: Trailing whitespace
- Line 186: Trailing whitespace
- Line 197: Trailing whitespace
- Line 201: Trailing whitespace
- Line 204: Trailing whitespace
- Line 208: Trailing whitespace
- Line 220: Trailing whitespace
- Line 223: Trailing whitespace
- Line 226: Trailing whitespace
- Line 229: Trailing whitespace
- Line 233: Trailing whitespace
- Line 256: Trailing whitespace
- Line 259: Trailing whitespace
- Line 261: Trailing whitespace
- Line 270: Trailing whitespace
- Line 273: Trailing whitespace
- Line 275: Trailing whitespace
- Line 284: Trailing whitespace
- Line 287: Trailing whitespace
- Line 291: Trailing whitespace
- Line 294: Trailing whitespace
- Line 297: Trailing whitespace
- Line 308: Trailing whitespace
- Line 326: Trailing whitespace
- Line 334: Trailing whitespace
- Line 341: Trailing whitespace
- Line 344: Trailing whitespace
- Line 350: Trailing whitespace
- Line 373: Trailing whitespace
- Line 378: Trailing whitespace
- Line 381: Trailing whitespace
- Line 384: Trailing whitespace
- Line 394: Trailing whitespace
- Line 399: Trailing whitespace
- Line 402: Trailing whitespace
- Line 405: Trailing whitespace
- Line 418: Trailing whitespace
- Line 423: Trailing whitespace
- Line 426: Trailing whitespace
- Line 429: Trailing whitespace
- Line 445: Trailing whitespace
- Line 450: Trailing whitespace
- Line 455: Trailing whitespace
- Line 460: Trailing whitespace
- Line 465: Trailing whitespace
- Line 467: Trailing whitespace
- Line 475: Trailing whitespace
- Line 478: Trailing whitespace
- Line 483: Trailing whitespace
- Line 486: Trailing whitespace
- Line 491: Trailing whitespace
- Line 494: Trailing whitespace
- Line 502: Trailing whitespace
- Line 507: Trailing whitespace
- Line 512: Trailing whitespace
- Line 515: Trailing whitespace
- Line 517: Trailing whitespace
- Line 521: Trailing whitespace
- Line 528: Trailing whitespace
- Line 532: Trailing whitespace
- Line 549: Trailing whitespace
- Line 552: Trailing whitespace
- Line 557: Trailing whitespace
- Line 563: Trailing whitespace
- Line 565: Trailing whitespace
- Line 568: Trailing whitespace
- Line 572: Trailing whitespace
- Line 576: Trailing whitespace
- Line 585: Trailing whitespace
- Line 592: Trailing whitespace
- Line 605: Trailing whitespace
- Line 608: Trailing whitespace
- Line 612: Trailing whitespace

### src/piwardrive/api/performance_dashboard.py
- Line 30: E302 expected 2 blank lines, found 1
- Line 31: E501 line too long (82 > 79 characters)
- Line 38: E302 expected 2 blank lines, found 1
- Line 78: E501 line too long (88 > 79 characters)
- Line 89: E302 expected 2 blank lines, found 1
- Line 101: E302 expected 2 blank lines, found 1
- Line 113: E302 expected 2 blank lines, found 1
- Line 126: E501 line too long (86 > 79 characters)
- Line 136: E501 line too long (88 > 79 characters)
- Line 163: E302 expected 2 blank lines, found 1
- Line 181: E501 line too long (87 > 79 characters)
- Line 183: E501 line too long (80 > 79 characters)
- Line 194: E302 expected 2 blank lines, found 1
- Line 195: E501 line too long (83 > 79 characters)
- Line 223: E501 line too long (83 > 79 characters)
- Line 236: E501 line too long (82 > 79 characters)
- Line 243: E302 expected 2 blank lines, found 1
- Line 253: E501 line too long (88 > 79 characters)
- Line 258: E501 line too long (101 > 79 characters)
- Line 260: E501 line too long (101 > 79 characters)
- Line 275: E501 line too long (83 > 79 characters)
- Line 276: E501 line too long (96 > 79 characters)
- Line 295: E501 line too long (96 > 79 characters)
- Line 297: E501 line too long (111 > 79 characters)
- Line 311: E501 line too long (86 > 79 characters)
- Line 315: E501 line too long (83 > 79 characters)
- Line 317: E302 expected 2 blank lines, found 1
- Line 345: E501 line too long (124 > 79 characters)
- Line 347: E501 line too long (92 > 79 characters)
- Line 349: E501 line too long (83 > 79 characters)
- Line 355: E501 line too long (85 > 79 characters)
- Line 363: E501 line too long (110 > 79 characters)
- Line 365: E501 line too long (104 > 79 characters)
- Line 367: E501 line too long (97 > 79 characters)
- Line 393: E501 line too long (115 > 79 characters)
- Line 396: W503 line break before binary operator
- Line 397: E501 line too long (82 > 79 characters)
- Line 416: E501 line too long (112 > 79 characters)
- Line 418: E501 line too long (91 > 79 characters)
- Line 420: E501 line too long (91 > 79 characters)
- Line 434: E501 line too long (83 > 79 characters)
- Line 435: E501 line too long (94 > 79 characters)
- Line 437: E501 line too long (87 > 79 characters)
- Line 448: E302 expected 2 blank lines, found 1
- Line 460: E501 line too long (87 > 79 characters)
- Line 345: Line too long (124 > 120 characters)

### src/piwardrive/integrations/sigint_suite/cellular/tower_scanner/scanner.py
- Line 49: E501 line too long (82 > 79 characters)

### tests/test_r_integration.py
- Line 28: E501 line too long (88 > 79 characters)
- Line 43: E501 line too long (80 > 79 characters)
- Line 47: E501 line too long (81 > 79 characters)
- Line 64: E501 line too long (80 > 79 characters)
- Line 68: E501 line too long (81 > 79 characters)

### src/piwardrive/services/alerting.py
- Line 36: E501 line too long (82 > 79 characters)
- Line 70: W293 blank line contains whitespace
- Line 81: E501 line too long (81 > 79 characters)
- Line 92: E501 line too long (86 > 79 characters)
- Line 70: Trailing whitespace

### code_analysis.py
- Line 4: E501 line too long (80 > 79 characters)
- Line 15: E302 expected 2 blank lines, found 1
- Line 19: W293 blank line contains whitespace
- Line 31: W293 blank line contains whitespace
- Line 35: W293 blank line contains whitespace
- Line 42: W293 blank line contains whitespace
- Line 45: W293 blank line contains whitespace
- Line 47: E501 line too long (92 > 79 characters)
- Line 48: E501 line too long (83 > 79 characters)
- Line 52: W293 blank line contains whitespace
- Line 55: W293 blank line contains whitespace
- Line 57: W293 blank line contains whitespace
- Line 68: W293 blank line contains whitespace
- Line 76: W293 blank line contains whitespace
- Line 79: W293 blank line contains whitespace
- Line 84: W293 blank line contains whitespace
- Line 91: W293 blank line contains whitespace
- Line 94: E501 line too long (91 > 79 characters)
- Line 96: E501 line too long (92 > 79 characters)
- Line 98: E501 line too long (89 > 79 characters)
- Line 100: E501 line too long (88 > 79 characters)
- Line 102: E501 line too long (89 > 79 characters)
- Line 103: W293 blank line contains whitespace
- Line 105: E501 line too long (96 > 79 characters)
- Line 108: W293 blank line contains whitespace
- Line 110: W293 blank line contains whitespace
- Line 111: E501 line too long (80 > 79 characters)
- Line 115: W293 blank line contains whitespace
- Line 120: W293 blank line contains whitespace
- Line 122: E501 line too long (87 > 79 characters)
- Line 124: E501 line too long (97 > 79 characters)
- Line 126: W293 blank line contains whitespace
- Line 128: W293 blank line contains whitespace
- Line 133: W293 blank line contains whitespace
- Line 139: E501 line too long (96 > 79 characters)
- Line 140: W293 blank line contains whitespace
- Line 142: W293 blank line contains whitespace
- Line 146: W293 blank line contains whitespace
- Line 151: E501 line too long (83 > 79 characters)
- Line 154: E501 line too long (88 > 79 characters)
- Line 155: W293 blank line contains whitespace
- Line 157: W293 blank line contains whitespace
- Line 161: W293 blank line contains whitespace
- Line 163: E501 line too long (87 > 79 characters)
- Line 165: E501 line too long (127 > 79 characters)
- Line 166: W293 blank line contains whitespace
- Line 168: W293 blank line contains whitespace
- Line 173: W293 blank line contains whitespace
- Line 178: W293 blank line contains whitespace
- Line 181: E501 line too long (88 > 79 characters)
- Line 182: W293 blank line contains whitespace
- Line 184: W293 blank line contains whitespace
- Line 188: W293 blank line contains whitespace
- Line 191: E501 line too long (83 > 79 characters)
- Line 193: W293 blank line contains whitespace
- Line 196: E501 line too long (98 > 79 characters)
- Line 197: W293 blank line contains whitespace
- Line 199: W293 blank line contains whitespace
- Line 203: W293 blank line contains whitespace
- Line 205: W293 blank line contains whitespace
- Line 210: W293 blank line contains whitespace
- Line 212: W293 blank line contains whitespace
- Line 216: W293 blank line contains whitespace
- Line 222: W293 blank line contains whitespace
- Line 229: W293 blank line contains whitespace
- Line 234: W291 trailing whitespace
- Line 240: W293 blank line contains whitespace
- Line 244: W293 blank line contains whitespace
- Line 253: W293 blank line contains whitespace
- Line 257: W293 blank line contains whitespace
- Line 260: E302 expected 2 blank lines, found 1
- Line 265: W293 blank line contains whitespace
- Line 269: W293 blank line contains whitespace
- Line 271: W293 blank line contains whitespace
- Line 274: E501 line too long (111 > 79 characters)
- Line 277: E305 expected 2 blank lines after class or function definition, found 1
- Line 19: Trailing whitespace
- Line 31: Trailing whitespace
- Line 35: Trailing whitespace
- Line 42: Trailing whitespace
- Line 45: Trailing whitespace
- Line 52: Trailing whitespace
- Line 55: Trailing whitespace
- Line 57: Trailing whitespace
- Line 68: Trailing whitespace
- Line 76: Trailing whitespace
- Line 79: Trailing whitespace
- Line 84: Trailing whitespace
- Line 91: Trailing whitespace
- Line 103: Trailing whitespace
- Line 108: Trailing whitespace
- Line 110: Trailing whitespace
- Line 115: Trailing whitespace
- Line 120: Trailing whitespace
- Line 126: Trailing whitespace
- Line 128: Trailing whitespace
- Line 133: Trailing whitespace
- Line 140: Trailing whitespace
- Line 142: Trailing whitespace
- Line 146: Trailing whitespace
- Line 155: Trailing whitespace
- Line 157: Trailing whitespace
- Line 161: Trailing whitespace
- Line 165: Line too long (127 > 120 characters)
- Line 166: Trailing whitespace
- Line 168: Trailing whitespace
- Line 173: Trailing whitespace
- Line 178: Trailing whitespace
- Line 182: Trailing whitespace
- Line 184: Trailing whitespace
- Line 188: Trailing whitespace
- Line 193: Trailing whitespace
- Line 197: Trailing whitespace
- Line 199: Trailing whitespace
- Line 203: Trailing whitespace
- Line 205: Trailing whitespace
- Line 210: Trailing whitespace
- Line 212: Trailing whitespace
- Line 216: Trailing whitespace
- Line 222: Trailing whitespace
- Line 229: Trailing whitespace
- Line 234: Trailing whitespace
- Line 240: Trailing whitespace
- Line 244: Trailing whitespace
- Line 253: Trailing whitespace
- Line 257: Trailing whitespace
- Line 265: Trailing whitespace
- Line 269: Trailing whitespace
- Line 271: Trailing whitespace

## Other Issues

### src/piwardrive/hardware/enhanced_hardware.py
- Line 276: F841 local variable '_frequencies' is assigned to but never used
- Line 330: F841 local variable '_available_adapters' is assigned to but never used

### tests/test_direction_finding.py
- Line 230: F841 local variable '_original_exponent' is assigned to but never used

### test_imports.py
- Line 10: F541 f-string is missing placeholders

### src/piwardrive/reporting/professional.py
- Line 338: F841 local variable '_reportdata' is assigned to but never used
- Line 645: F841 local variable '_encryption_data' is assigned to but never used
- Line 646: F841 local variable '_vendor_data' is assigned to but never used
- Line 762: F841 local variable '_result' is assigned to but never used

### src/piwardrive/cli/config_cli.py
- Line 74: F841 local variable '_data' is assigned to but never used

### src/piwardrive/direction_finding/algorithms.py
- Line 277: F841 local variable '_result' is assigned to but never used
- Line 344: F841 local variable '__result' is assigned to but never used
- Line 725: F841 local variable '_iqdata' is assigned to but never used
- Line 736: F841 local variable '_result' is assigned to but never used
- Line 959: F841 local variable '_result' is assigned to but never used

### src/piwardrive/performance/async_optimizer.py
- Line 106: F841 local variable '_failed' is assigned to but never used
- Line 140: F841 local variable '_result' is assigned to but never used
- Line 248: F841 local variable '_stats' is assigned to but never used
- Line 333: F841 local variable '_stats' is assigned to but never used
- Line 409: F841 local variable '__result' is assigned to but never used
- Line 422: F841 local variable 'e' is assigned to but never used
- Line 511: F841 local variable '_stats' is assigned to but never used
- Line 645: F841 local variable '_results' is assigned to but never used

### src/piwardrive/data_sink.py
- Line 37: F841 local variable '_data' is assigned to but never used

### src/piwardrive/map/tile_maintenance.py
- Line 24: F841 local variable '_result' is assigned to but never used

### tests/test_service_simple.py
- Line 37: F841 local variable 'mock_error_middleware' is assigned to but never used

### src/piwardrive/protocols/multi_protocol.py
- Line 793: F841 local variable '_iqdata' is assigned to but never used
- Line 1062: F841 local variable '_stats' is assigned to but never used
- Line 1136: F841 local variable '_stats' is assigned to but never used

### src/piwardrive/ui/user_experience.py
- Line 191: F841 local variable '_data' is assigned to but never used
- Line 208: F841 local variable '__data' is assigned to but never used
- Line 693: F841 local variable '_config' is assigned to but never used
- Line 746: F841 local variable '__config' is assigned to but never used
- Line 778: F841 local variable '_widgetconfig' is assigned to but never used
- Line 784: F841 local variable '_config' is assigned to but never used
- Line 1254: F841 local variable '_data' is assigned to but never used
- Line 1294: F841 local variable '_data' is assigned to but never used

### src/piwardrive/data_processing/enhanced_processing.py
- Line 197: F841 local variable '_lat' is assigned to but never used
- Line 198: F841 local variable '_lon' is assigned to but never used
- Line 218: F841 local variable '_filtereddata' is assigned to but never used
- Line 364: F841 local variable '__stats' is assigned to but never used
- Line 532: F841 local variable '_enhanceddata' is assigned to but never used
- Line 559: F841 local variable '__data' is assigned to but never used
- Line 608: F841 local variable '_lat' is assigned to but never used
- Line 609: F841 local variable '_lon' is assigned to but never used
- Line 613: F841 local variable '_style' is assigned to but never used
- Line 616: F841 local variable '_name' is assigned to but never used
- Line 617: F841 local variable '_description' is assigned to but never used
- Line 678: F841 local variable '_description' is assigned to but never used

### src/piwardrive/routes/bluetooth.py
- Line 32: F841 local variable '_result' is assigned to but never used
- Line 48: F841 local variable '_result' is assigned to but never used

### src/piwardrive/enhanced/strategic_enhancements.py
- Line 359: F841 local variable '_siem_config' is assigned to but never used
- Line 379: F841 local variable '_playbook_data' is assigned to but never used
- Line 874: F841 local variable '_stats' is assigned to but never used
- Line 944: F841 local variable '_result' is assigned to but never used
- Line 1363: F841 local variable '__data' is assigned to but never used
- Line 1393: F841 local variable '_result' is assigned to but never used
- Line 1408: F841 local variable '_data' is assigned to but never used

### src/piwardrive/integration/system_orchestration.py
- Line 264: F841 local variable '_service_def' is assigned to but never used

### src/piwardrive/logging/storage.py
- Line 198: F841 local variable '_data' is assigned to but never used

### src/piwardrive/analytics/baseline.py
- Line 50: F811 redefinition of unused 'run_cpu_bound' from line 10

### comprehensive_fix.py
- Line 73: F841 local variable '_patterns' is assigned to but never used
- Line 214: F841 local variable '_in_complex_function' is assigned to but never used

### src/piwardrive/db_browser.py
- Line 21: F841 local variable '__data' is assigned to but never used

### tests/test_main_simple.py
- Line 297: F811 redefinition of unused 'Path' from line 9

### tests/test_core_persistence.py
- Line 497: F841 local variable 'size_before' is assigned to but never used

### src/piwardrive/performance/realtime_optimizer.py
- Line 214: F841 local variable '_stats' is assigned to but never used
- Line 356: F841 local variable '_stats' is assigned to but never used
- Line 469: F841 local variable '_optimizeddata' is assigned to but never used
- Line 538: F841 local variable '_optimizeddata' is assigned to but never used
- Line 679: F841 local variable '_stats' is assigned to but never used

### tests/test_utils_comprehensive.py
- Line 112: F841 local variable 'result' is assigned to but never used
- Line 190: F841 local variable 'result' is assigned to but never used
- Line 352: F841 local variable 'start_time' is assigned to but never used
- Line 354: F841 local variable 'end_time' is assigned to but never used

### src/piwardrive/main.py
- Line 176: F841 local variable '_data' is assigned to but never used
- Line 226: F841 local variable '_data' is assigned to but never used

### tests/test_service_direct.py
- Line 161: F841 local variable 'e' is assigned to but never used

### src/piwardrive/orientation_sensors.py
- Line 84: F841 local variable '_data' is assigned to but never used

### src/piwardrive/geospatial/intelligence.py
- Line 172: F841 local variable '_result' is assigned to but never used
- Line 229: F841 local variable '_stats' is assigned to but never used
- Line 406: F841 local variable '_contours' is assigned to but never used
- Line 795: F841 local variable '_pos' is assigned to but never used
- Line 813: F841 local variable '_stats' is assigned to but never used

### src/piwardrive/visualization/advanced_viz.py
- Line 95: F841 local variable '_data' is assigned to but never used
- Line 296: F841 local variable '_ssiddata' is assigned to but never used
- Line 457: F841 local variable '_analysis' is assigned to but never used
- Line 472: F841 local variable '__stats' is assigned to but never used
- Line 558: F841 local variable '_total_aps' is assigned to but never used
- Line 562: F841 local variable '_analysis' is assigned to but never used
- Line 711: F841 local variable '_total_aps' is assigned to but never used
- Line 712: F841 local variable '_open_networks' is assigned to but never used
- Line 713: F841 local variable '_avg_signal' is assigned to but never used
- Line 806: F841 local variable '_analysis' is assigned to but never used
- Line 807: F841 local variable '__stats' is assigned to but never used
- Line 940: F841 local variable '_data' is assigned to but never used

### src/piwardrive/services/maintenance.py
- Line 90: F841 local variable '_result' is assigned to but never used

### tests/logging/test_structured_logger.py
- Line 758: F841 local variable 'tmp' is assigned to but never used
- Line 770: F841 local variable 'handlers' is assigned to but never used

### fix_undefined.py
- Line 32: F841 local variable '_undefined_patterns' is assigned to but never used

### tests/test_api_service.py
- Line 57: F841 local variable 'mock_cors' is assigned to but never used
- Line 278: F811 redefinition of unused 'status' from line 13
- Line 314: F811 redefinition of unused 'status' from line 13

### src/piwardrive/direction_finding/core.py
- Line 260: F841 local variable '_result' is assigned to but never used
- Line 294: F841 local variable '_result' is assigned to but never used

### scripts/test_database_functions.py
- Line 169: F541 f-string is missing placeholders
- Line 171: F541 f-string is missing placeholders
- Line 177: F541 f-string is missing placeholders

### src/piwardrive/navigation/offline_navigation.py
- Line 788: F841 local variable '__data' is assigned to but never used
- Line 818: F841 local variable '_data' is assigned to but never used

### src/piwardrive/analysis/packet_engine.py
- Line 431: F841 local variable '_aa' is assigned to but never used
- Line 432: F841 local variable '_tc' is assigned to but never used
- Line 433: F841 local variable '_rd' is assigned to but never used
- Line 434: F841 local variable '_ra' is assigned to but never used
- Line 467: F841 local variable '_hops' is assigned to but never used
- Line 470: F841 local variable '_secs' is assigned to but never used
- Line 471: F841 local variable '_flags' is assigned to but never used
- Line 512: F841 local variable '_hardware_type' is assigned to but never used
- Line 513: F841 local variable '_protocol_type' is assigned to but never used
- Line 514: F841 local variable '_hardware_length' is assigned to but never used
- Line 515: F841 local variable '_protocol_length' is assigned to but never used
- Line 797: F841 local variable '_well_known_ports' is assigned to but never used

### src/piwardrive/mining/advanced_data_mining.py
- Line 118: F841 local variable '_data' is assigned to but never used
- Line 125: F841 local variable '_timestamps' is assigned to but never used
- Line 177: F841 local variable '_data' is assigned to but never used
- Line 219: F841 local variable '_data' is assigned to but never used
- Line 424: F841 local variable '_features' is assigned to but never used
- Line 879: F841 local variable '_devices' is assigned to but never used
- Line 1293: F841 local variable '_stats' is assigned to but never used

### src/piwardrive/logging/config.py
- Line 59: F841 local variable '_fileconfig' is assigned to but never used

### src/piwardrive/widgets/health_analysis.py
- Line 51: F841 local variable '_stats' is assigned to but never used

### src/piwardrive/visualization/advanced_visualization.py
- Line 623: F841 local variable '_timestamps' is assigned to but never used
- Line 624: F841 local variable '_event_types' is assigned to but never used
- Line 1043: F841 local variable '_fig_temporal' is assigned to but never used
- Line 1057: F841 local variable '_fig_heatmap' is assigned to but never used
- Line 1089: F841 local variable '_fig_network' is assigned to but never used
- Line 1140: F841 local variable '_custom_fig' is assigned to but never used

### tests/test_integration_comprehensive.py
- Line 123: F841 local variable '_config' is assigned to but never used
- Line 139: F841 local variable '_config' is assigned to but never used
- Line 159: F841 local variable '_config' is assigned to but never used
- Line 174: F841 local variable '_config' is assigned to but never used
- Line 194: F841 local variable '_config' is assigned to but never used
- Line 215: F841 local variable '_config' is assigned to but never used
- Line 254: F841 local variable '_config' is assigned to but never used
- Line 275: F841 local variable '_config' is assigned to but never used
- Line 316: F841 local variable '_config' is assigned to but never used
- Line 319: F841 local variable '_tasks' is assigned to but never used
- Line 363: F841 local variable '_config' is assigned to but never used
- Line 400: F841 local variable '_config' is assigned to but never used
- Line 421: F841 local variable '_config' is assigned to but never used
- Line 436: F841 local variable '_config' is assigned to but never used
- Line 473: F841 local variable '_config' is assigned to but never used
- Line 502: F841 local variable '_config' is assigned to but never used
- Line 526: F841 local variable '_config' is assigned to but never used

### src/piwardrive/plugins/plugin_architecture.py
- Line 709: F841 local variable '_vizresult' is assigned to but never used
- Line 713: F841 local variable '_analysisresult' is assigned to but never used

### src/piwardrive/core/utils.py
- Line 236: F841 local variable '_data' is assigned to but never used
- Line 243: F841 local variable '_result' is assigned to but never used
- Line 385: F841 local variable '_result' is assigned to but never used
- Line 460: F841 local variable '_result' is assigned to but never used
- Line 642: F841 local variable '_result' is assigned to but never used
- Line 1052: F841 local variable '_data' is assigned to but never used
- Line 1060: F841 local variable '_data' is assigned to but never used
- Line 1235: F841 local variable '_data' is assigned to but never used

### src/piwardrive/widgets/health_status.py
- Line 43: F841 local variable '_data' is assigned to but never used

### src/piwardrive/enhanced/critical_additions.py
- Line 900: F841 local variable '_streamer' is assigned to but never used

### tests/test_jwt_utils_comprehensive.py
- Line 419: F841 local variable 'username' is assigned to but never used

### tests/test_main_application_comprehensive.py
- Line 30: F841 local variable 'mock_async' is assigned to but never used
- Line 31: F841 local variable 'mock_tile' is assigned to but never used
- Line 286: F841 local variable 'app' is assigned to but never used
- Line 300: F841 local variable 'app' is assigned to but never used
- Line 315: F841 local variable 'app' is assigned to but never used
- Line 430: F841 local variable 'mock_tile' is assigned to but never used
- Line 431: F841 local variable 'mock_analytics' is assigned to but never used
- Line 432: F841 local variable 'mock_maintenance' is assigned to but never used

### src/piwardrive/integrations/sigint_suite/dashboard/__init__.py
- Line 33: F841 local variable '_data' is assigned to but never used
- Line 96: F841 local variable '_data' is assigned to but never used

### src/piwardrive/widgets/orientation_widget.py
- Line 43: F841 local variable '_data' is assigned to but never used

### src/piwardrive/scan_report.py
- Line 32: F841 local variable '_data' is assigned to but never used

### tests/test_performance_comprehensive.py
- Line 149: F841 local variable '_config' is assigned to but never used
- Line 184: F841 local variable '_config' is assigned to but never used
- Line 208: F841 local variable '_result' is assigned to but never used
- Line 218: F841 local variable '_config' is assigned to but never used
- Line 271: F841 local variable '_config' is assigned to but never used
- Line 303: F841 local variable '_config' is assigned to but never used
- Line 341: F841 local variable '_config' is assigned to but never used
- Line 371: F841 local variable '_config' is assigned to but never used
- Line 445: F841 local variable '_config' is assigned to but never used
- Line 473: F841 local variable '_result' is assigned to but never used
- Line 483: F841 local variable '_config' is assigned to but never used
- Line 512: F841 local variable '_config' is assigned to but never used
- Line 594: F841 local variable '_config' is assigned to but never used
- Line 638: F841 local variable '_config' is assigned to but never used
- Line 670: F841 local variable '_config' is assigned to but never used
- Line 720: F841 local variable '_config' is assigned to but never used
- Line 730: F841 local variable '_initial_memory' is assigned to but never used

### src/piwardrive/core/persistence.py
- Line 987: F841 local variable 'e' is assigned to but never used
- Line 1636: F811 redefinition of unused 'backup_database' from line 338

### src/piwardrive/diagnostics.py
- Line 145: F841 local variable '_data' is assigned to but never used
- Line 166: F841 local variable '_stats' is assigned to but never used
- Line 192: F841 local variable '_stats' is assigned to but never used
- Line 403: F841 local variable '__result' is assigned to but never used

### comprehensive_code_analyzer.py
- Line 74: F841 local variable 'lines' is assigned to but never used
- Line 260: F541 f-string is missing placeholders

### src/piwardrive/api/websockets/handlers.py
- Line 36: F841 local variable '_data' is assigned to but never used
- Line 77: F841 local variable '_data' is assigned to but never used
- Line 101: F841 local variable '_data' is assigned to but never used
- Line 130: F841 local variable '_data' is assigned to but never used

### tests/test_main_application_fixed.py
- Line 143: F841 local variable 'app' is assigned to but never used
- Line 472: F841 local variable 'app' is assigned to but never used

### tests/test_widget_manager.py
- Line 32: F841 local variable '_widget' is assigned to but never used
- Line 42: F841 local variable '_widget' is assigned to but never used
- Line 70: F841 local variable '_widget' is assigned to but never used

### tests/test_service_api.py
- Line 33: F841 local variable 'mock_router' is assigned to but never used
- Line 34: F841 local variable 'mock_analytics' is assigned to but never used
- Line 35: F841 local variable 'mock_wifi' is assigned to but never used
- Line 36: F841 local variable 'mock_bt' is assigned to but never used
- Line 37: F841 local variable 'mock_cell' is assigned to but never used
- Line 198: F811 redefinition of unused 'HTTPException' from line 11
- Line 199: F811 redefinition of unused 'TestClient' from line 10
- Line 217: F811 redefinition of unused 'TestClient' from line 10
- Line 239: F841 local variable 'mock_analysis' is assigned to but never used
- Line 240: F841 local variable 'mock_wifi' is assigned to but never used
- Line 241: F841 local variable 'mock_bluetooth' is assigned to but never used
- Line 242: F841 local variable 'mock_cellular' is assigned to but never used
- Line 243: F841 local variable 'mock_analytics' is assigned to but never used
- Line 371: F811 redefinition of unused 'HTTPException' from line 11
- Line 372: F811 redefinition of unused 'TestClient' from line 10

### src/piwardrive/scheduler.py
- Line 49: F841 local variable '_data' is assigned to but never used
- Line 129: F841 local variable '_result' is assigned to but never used
- Line 158: F841 local variable '_result' is assigned to but never used
- Line 212: F841 local variable '_result' is assigned to but never used

### src/piwardrive/performance/db_optimizer.py
- Line 84: F841 local variable '__stats' is assigned to but never used
- Line 253: F841 local variable '_result' is assigned to but never used
- Line 386: F841 local variable '_result' is assigned to but never used

### scripts/simple_db_check.py
- Line 131: F541 f-string is missing placeholders

### src/piwardrive/analytics/predictive.py
- Line 86: F841 local variable '_result' is assigned to but never used

### tests/test_service_direct_import.py
- Line 70: F841 local variable 'mock_cors' is assigned to but never used

### src/piwardrive/direction_finding/hardware.py
- Line 32: F841 local variable '_result' is assigned to but never used
- Line 114: F841 local variable '_result' is assigned to but never used
- Line 148: F841 local variable '_result' is assigned to but never used
- Line 186: F841 local variable '_result' is assigned to but never used
- Line 242: F841 local variable '_result' is assigned to but never used
- Line 614: F841 local variable '_data' is assigned to but never used

### src/piwardrive/api/logging_control.py
- Line 43: F841 local variable '__data' is assigned to but never used

### src/piwardrive/routes/websocket.py
- Line 23: F841 local variable '_data' is assigned to but never used
- Line 43: F841 local variable '_data' is assigned to but never used

### scripts/performance_monitor.py
- Line 319: F841 local variable '_result' is assigned to but never used

### scripts/performance_cli.py
- Line 43: F541 f-string is missing placeholders
- Line 53: F541 f-string is missing placeholders
- Line 78: F541 f-string is missing placeholders
- Line 102: F541 f-string is missing placeholders
- Line 123: F541 f-string is missing placeholders
- Line 234: F541 f-string is missing placeholders
- Line 241: F541 f-string is missing placeholders
- Line 320: F541 f-string is missing placeholders

### tests/test_scheduler_tasks.py
- Line 57: F841 local variable 'task_id' is assigned to but never used

### src/piwardrive/jobs/maintenance_jobs.py
- Line 66: F841 local variable '_result' is assigned to but never used

### src/piwardrive/widgets/db_stats.py
- Line 31: F811 redefinition of unused 'Any' from line 6
- Line 42: F841 local variable '_result' is assigned to but never used
- Line 72: F841 local variable '_stats' is assigned to but never used

### src/piwardrive/testing/automated_framework.py
- Line 229: F841 local variable '_result' is assigned to but never used
- Line 411: F841 local variable '__result' is assigned to but never used
- Line 416: F841 local variable '_result' is assigned to but never used
- Line 450: F841 local variable '_testdata' is assigned to but never used
- Line 572: F841 local variable '_processes' is assigned to but never used
- Line 620: F841 local variable '__result' is assigned to but never used
- Line 623: F841 local variable '_result' is assigned to but never used
- Line 656: F841 local variable '_available_mb' is assigned to but never used
- Line 792: F841 local variable '_result' is assigned to but never used
- Line 827: F841 local variable '_result' is assigned to but never used
- Line 852: F841 local variable '_result' is assigned to but never used

### src/piwardrive/widgets/log_viewer.py
- Line 16: F811 redefinition of unused 'tail_file' from line 8

### tests/test_core_application.py
- Line 87: F841 local variable 'mock_analytics' is assigned to but never used
- Line 88: F841 local variable 'mock_maintenance' is assigned to but never used
- Line 89: F841 local variable 'mock_async' is assigned to but never used

### src/piwardrive/routes/cellular.py
- Line 32: F841 local variable '_result' is assigned to but never used
- Line 48: F841 local variable '_result' is assigned to but never used

### src/piwardrive/map/vector_tile_customizer.py
- Line 84: F841 local variable '__data' is assigned to but never used

### src/piwardrive/integrations/wigle.py
- Line 49: F841 local variable '_data' is assigned to but never used

### tests/test_main_application.py
- Line 52: F841 local variable 'app' is assigned to but never used
- Line 91: F841 local variable 'app' is assigned to but never used
- Line 104: F841 local variable 'app' is assigned to but never used

### src/piwardrive/performance/optimization.py
- Line 816: F841 local variable '_total_calls' is assigned to but never used
- Line 817: F841 local variable '_total_time' is assigned to but never used
- Line 1039: F841 local variable '_test_objects' is assigned to but never used
- Line 1061: F841 local variable '__result' is assigned to but never used

### src/piwardrive/api/system/endpoints.py
- Line 63: F841 local variable '_data' is assigned to but never used
- Line 131: F841 local variable '_data' is assigned to but never used
- Line 182: F841 local variable '_result' is assigned to but never used
- Line 208: F841 local variable '_data' is assigned to but never used

### src/piwardrive/direction_finding/integration.py
- Line 51: F841 local variable '_config' is assigned to but never used

### tests/test_widget_system_comprehensive.py
- Line 361: F841 local variable 'manager' is assigned to but never used

### src/piwardrive/remote_sync.py
- Line 17: F811 redefinition of unused 'logging' from line 8

### src/piwardrive/integrations/sigint.py
- Line 16: F841 local variable '_data' is assigned to but never used

### src/piwardrive/integrations/sigint_suite/exports/exporter.py
- Line 63: F841 local variable '_data' is assigned to but never used

### src/piwardrive/api/websockets/events.py
- Line 27: F841 local variable '_data' is assigned to but never used

### tests/test_route_prefetch.py
- Line 61: F811 redefinition of unused 'route_prefetch' from line 23
- Line 86: F811 redefinition of unused 'route_prefetch' from line 23
- Line 109: F811 redefinition of unused 'route_prefetch' from line 23
- Line 134: F811 redefinition of unused 'route_prefetch' from line 23

### src/piwardrive/integrations/sigint_suite/cellular/imsi_catcher/scanner.py
- Line 133: F841 local variable '_data' is assigned to but never used

### src/piwardrive/integrations/sigint_suite/cellular/band_scanner/scanner.py
- Line 91: F841 local variable '_data' is assigned to but never used

### tests/test_memory_monitor.py
- Line 9: F841 local variable '_data' is assigned to but never used

### src/piwardrive/api/performance_dashboard.py
- Line 106: F841 local variable '_stats' is assigned to but never used
- Line 126: F841 local variable '_stats' is assigned to but never used
- Line 132: F841 local variable '_tablestats' is assigned to but never used
- Line 156: F841 local variable '_realtimestats' is assigned to but never used
- Line 456: F841 local variable '_stats' is assigned to but never used

### code_analysis.py
- Line 224: F541 f-string is missing placeholders
