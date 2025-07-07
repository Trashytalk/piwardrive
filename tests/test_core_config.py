"""
Comprehensive tests for configuration management system.
Tests configuration loading, validation, profiles, and environment overrides.
"""

import os
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from dataclasses import asdict
from typing import Dict, Any

from piwardrive.core.config import (
    Config, 
    get_config_path, 
    config_mtime,
    load_config,
    save_config,
    validate_config_data,
    get_active_profile,
    list_profiles,
    create_profile,
    delete_profile,
    switch_profile,
    export_config,
    import_config,
    CONFIG_DIR,
    CONFIG_PATH,
    PROFILES_DIR,
    ACTIVE_PROFILE_FILE
)
from piwardrive.errors import ConfigError


class TestConfigurationLoading:
    """Test configuration loading and defaults."""
    
    def test_load_config_with_defaults(self, tmp_path):
        """Test loading config with default values when no file exists."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = load_config()
            
            # Verify default values
            assert config.map_poll_aps == 60
            assert config.map_poll_bt == 60
            assert config.map_show_gps is True
            assert config.map_follow_gps is True
            assert config.debug_mode is False
            assert config.health_poll_interval == 10
            
    def test_load_config_from_file(self, tmp_path):
        """Test loading config from existing file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create config file
            config_path = tmp_path / "config.json"
            test_config = {
                "map_poll_aps": 30,
                "map_poll_bt": 45,
                "debug_mode": True,
                "health_poll_interval": 15,
                "map_show_gps": False
            }
            
            with open(config_path, 'w') as f:
                json.dump(test_config, f)
            
            config = load_config()
            
            # Verify loaded values
            assert config.map_poll_aps == 30
            assert config.map_poll_bt == 45
            assert config.debug_mode is True
            assert config.health_poll_interval == 15
            assert config.map_show_gps is False
            
    def test_load_config_with_partial_file(self, tmp_path):
        """Test loading config with partial configuration file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create partial config file
            config_path = tmp_path / "config.json"
            partial_config = {
                "map_poll_aps": 90,
                "debug_mode": True
            }
            
            with open(config_path, 'w') as f:
                json.dump(partial_config, f)
            
            config = load_config()
            
            # Verify loaded values and defaults
            assert config.map_poll_aps == 90  # From file
            assert config.debug_mode is True  # From file
            assert config.map_poll_bt == 60  # Default
            assert config.health_poll_interval == 10  # Default
            
    def test_load_config_with_invalid_json(self, tmp_path):
        """Test loading config with invalid JSON file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create invalid JSON file
            config_path = tmp_path / "config.json"
            with open(config_path, 'w') as f:
                f.write("invalid json content")
            
            # Should fall back to defaults
            config = load_config()
            assert config.map_poll_aps == 60  # Default value
            
    def test_config_modification_time(self, tmp_path):
        """Test config modification time tracking."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # No file exists - should return None
            assert config_mtime() is None
            
            # Create config file
            config_path = tmp_path / "config.json"
            with open(config_path, 'w') as f:
                json.dump({"map_poll_aps": 30}, f)
            
            # Should return modification time
            mtime = config_mtime()
            assert mtime is not None
            assert isinstance(mtime, float)


class TestConfigurationSaving:
    """Test configuration saving and persistence."""
    
    def test_save_config_basic(self, tmp_path):
        """Test basic configuration saving."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            config.map_poll_aps = 120
            config.debug_mode = True
            config.health_poll_interval = 5
            
            save_config(config)
            
            # Verify file was created
            config_path = tmp_path / "config.json"
            assert config_path.exists()
            
            # Verify content
            with open(config_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["map_poll_aps"] == 120
            assert saved_data["debug_mode"] is True
            assert saved_data["health_poll_interval"] == 5
            
    def test_save_and_load_roundtrip(self, tmp_path):
        """Test save/load roundtrip maintains data integrity."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create config with various data types
            original_config = Config()
            original_config.map_poll_aps = 75
            original_config.debug_mode = True
            original_config.log_paths = ["/var/log/test1.log", "/var/log/test2.log"]
            original_config.dashboard_layout = [{"widget": "test", "pos": [1, 2]}]
            original_config.offline_tile_path = "/custom/path/tiles.mbtiles"
            
            # Save config
            save_config(original_config)
            
            # Load config
            loaded_config = load_config()
            
            # Verify all values
            assert loaded_config.map_poll_aps == 75
            assert loaded_config.debug_mode is True
            assert loaded_config.log_paths == ["/var/log/test1.log", "/var/log/test2.log"]
            assert loaded_config.dashboard_layout == [{"widget": "test", "pos": [1, 2]}]
            assert loaded_config.offline_tile_path == "/custom/path/tiles.mbtiles"
            
    def test_save_config_creates_directory(self, tmp_path):
        """Test config saving creates directory if it doesn't exist."""
        config_dir = tmp_path / "new_config_dir"
        
        with patch('piwardrive.core.config.CONFIG_DIR', str(config_dir)):
            config = Config()
            config.map_poll_aps = 100
            
            save_config(config)
            
            # Verify directory was created
            assert config_dir.exists()
            assert config_dir.is_dir()
            
            # Verify file was created
            config_path = config_dir / "config.json"
            assert config_path.exists()


class TestConfigurationValidation:
    """Test configuration validation."""
    
    def test_validate_config_valid_values(self):
        """Test validation passes for valid config values."""
        config = Config()
        config.map_poll_aps = 60
        config.map_poll_bt = 30
        config.health_poll_interval = 10
        config.tile_cache_limit_mb = 512
        
        # Should not raise exception
        validate_config_data(config)
        
    def test_validate_config_invalid_poll_intervals(self):
        """Test validation catches invalid poll intervals."""
        config = Config()
        
        # Test negative values
        config.map_poll_aps = -1
        with pytest.raises(ConfigError, match="map_poll_aps must be positive"):
            validate_config_data(config)
            
        config.map_poll_aps = 60
        config.map_poll_bt = -1
        with pytest.raises(ConfigError, match="map_poll_bt must be positive"):
            validate_config_data(config)
            
        config.map_poll_bt = 60
        config.health_poll_interval = 0
        with pytest.raises(ConfigError, match="health_poll_interval must be positive"):
            validate_config_data(config)
            
    def test_validate_config_invalid_paths(self):
        """Test validation catches invalid file paths."""
        config = Config()
        
        # Test invalid offline tile path
        config.offline_tile_path = ""
        with pytest.raises(ConfigError, match="offline_tile_path cannot be empty"):
            validate_config_data(config)
            
        # Test invalid log paths
        config.offline_tile_path = "/valid/path.mbtiles"
        config.log_paths = [""]
        with pytest.raises(ConfigError, match="log_paths cannot contain empty paths"):
            validate_config_data(config)
            
    def test_validate_config_invalid_limits(self):
        """Test validation catches invalid limit values."""
        config = Config()
        
        # Test negative cache limit
        config.tile_cache_limit_mb = -1
        with pytest.raises(ConfigError, match="tile_cache_limit_mb must be non-negative"):
            validate_config_data(config)
            
        # Test invalid cluster capacity
        config.tile_cache_limit_mb = 512
        config.map_cluster_capacity = 0
        with pytest.raises(ConfigError, match="map_cluster_capacity must be positive"):
            validate_config_data(config)


class TestConfigurationProfiles:
    """Test configuration profile management."""
    
    def test_create_and_load_profile(self, tmp_path):
        """Test creating and loading configuration profiles."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.core.config.PROFILES_DIR', str(tmp_path / "profiles")):
                # Create a profile
                config = Config()
                config.map_poll_aps = 90
                config.debug_mode = True
                
                create_profile("test_profile", config)
                
                # Verify profile file was created
                profile_path = tmp_path / "profiles" / "test_profile.json"
                assert profile_path.exists()
                
                # Load profile
                loaded_config = load_config(profile="test_profile")
                
                # Verify loaded values
                assert loaded_config.map_poll_aps == 90
                assert loaded_config.debug_mode is True
                
    def test_list_profiles(self, tmp_path):
        """Test listing available profiles."""
        with patch('piwardrive.core.config.PROFILES_DIR', str(tmp_path)):
            # Create some profile files
            profile1_path = tmp_path / "profile1.json"
            profile2_path = tmp_path / "profile2.json"
            
            with open(profile1_path, 'w') as f:
                json.dump({"map_poll_aps": 30}, f)
            with open(profile2_path, 'w') as f:
                json.dump({"map_poll_aps": 60}, f)
            
            profiles = list_profiles()
            
            assert "profile1" in profiles
            assert "profile2" in profiles
            
    def test_switch_profile(self, tmp_path):
        """Test switching between profiles."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.core.config.PROFILES_DIR', str(tmp_path / "profiles")):
                with patch('piwardrive.core.config.ACTIVE_PROFILE_FILE', str(tmp_path / "active_profile")):
                    # Create profiles
                    config1 = Config()
                    config1.map_poll_aps = 30
                    create_profile("profile1", config1)
                    
                    config2 = Config()
                    config2.map_poll_aps = 60
                    create_profile("profile2", config2)
                    
                    # Switch to profile1
                    switch_profile("profile1")
                    assert get_active_profile() == "profile1"
                    
                    # Switch to profile2
                    switch_profile("profile2")
                    assert get_active_profile() == "profile2"
                    
    def test_delete_profile(self, tmp_path):
        """Test deleting configuration profiles."""
        with patch('piwardrive.core.config.PROFILES_DIR', str(tmp_path)):
            # Create a profile
            profile_path = tmp_path / "test_profile.json"
            with open(profile_path, 'w') as f:
                json.dump({"map_poll_aps": 30}, f)
            
            # Verify it exists
            assert profile_path.exists()
            
            # Delete profile
            delete_profile("test_profile")
            
            # Verify it's deleted
            assert not profile_path.exists()
            
    def test_profile_not_found_error(self, tmp_path):
        """Test error handling when profile doesn't exist."""
        with patch('piwardrive.core.config.PROFILES_DIR', str(tmp_path)):
            # Try to load non-existent profile
            with pytest.raises(ConfigError, match="Profile 'nonexistent' not found"):
                load_config(profile="nonexistent")
                
            # Try to delete non-existent profile
            with pytest.raises(ConfigError, match="Profile 'nonexistent' not found"):
                delete_profile("nonexistent")


class TestEnvironmentOverrides:
    """Test environment variable configuration overrides."""
    
    def test_environment_override_basic(self, tmp_path):
        """Test basic environment variable overrides."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            with patch.dict(os.environ, {
                'PW_MAP_POLL_APS': '45',
                'PW_DEBUG_MODE': 'true',
                'PW_HEALTH_POLL_INTERVAL': '20'
            }):
                config = load_config()
                
                assert config.map_poll_aps == 45
                assert config.debug_mode is True
                assert config.health_poll_interval == 20
                
    def test_environment_override_boolean_values(self, tmp_path):
        """Test environment variable boolean value parsing."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Test various boolean representations
            test_cases = [
                ('true', True),
                ('True', True),
                ('1', True),
                ('yes', True),
                ('on', True),
                ('false', False),
                ('False', False),
                ('0', False),
                ('no', False),
                ('off', False),
            ]
            
            for env_val, expected in test_cases:
                with patch.dict(os.environ, {'PW_DEBUG_MODE': env_val}):
                    config = load_config()
                    assert config.debug_mode is expected
                    
    def test_environment_override_numeric_values(self, tmp_path):
        """Test environment variable numeric value parsing."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            with patch.dict(os.environ, {
                'PW_MAP_POLL_APS': '75',
                'PW_HEALTH_POLL_INTERVAL': '25',
                'PW_TILE_CACHE_LIMIT_MB': '1024'
            }):
                config = load_config()
                
                assert config.map_poll_aps == 75
                assert config.health_poll_interval == 25
                assert config.tile_cache_limit_mb == 1024
                
    def test_environment_override_invalid_values(self, tmp_path):
        """Test environment variable invalid value handling."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            with patch.dict(os.environ, {
                'PW_MAP_POLL_APS': 'invalid_number',
                'PW_HEALTH_POLL_INTERVAL': 'not_a_number'
            }):
                config = load_config()
                
                # Should fall back to defaults for invalid values
                assert config.map_poll_aps == 60  # Default
                assert config.health_poll_interval == 10  # Default
                
    def test_environment_override_precedence(self, tmp_path):
        """Test environment variables override file configuration."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create config file
            config_path = tmp_path / "config.json"
            with open(config_path, 'w') as f:
                json.dump({"map_poll_aps": 30, "debug_mode": False}, f)
            
            # Set environment variables
            with patch.dict(os.environ, {
                'PW_MAP_POLL_APS': '90',
                'PW_DEBUG_MODE': 'true'
            }):
                config = load_config()
                
                # Environment should override file
                assert config.map_poll_aps == 90
                assert config.debug_mode is True


class TestConfigurationExportImport:
    """Test configuration export and import functionality."""
    
    def test_export_config(self, tmp_path):
        """Test exporting configuration to file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            config.map_poll_aps = 45
            config.debug_mode = True
            config.log_paths = ["/var/log/test.log"]
            
            export_path = tmp_path / "exported_config.json"
            export_config(config, str(export_path))
            
            # Verify export file was created
            assert export_path.exists()
            
            # Verify content
            with open(export_path, 'r') as f:
                exported_data = json.load(f)
            
            assert exported_data["map_poll_aps"] == 45
            assert exported_data["debug_mode"] is True
            assert exported_data["log_paths"] == ["/var/log/test.log"]
            
    def test_import_config(self, tmp_path):
        """Test importing configuration from file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create import file
            import_path = tmp_path / "import_config.json"
            import_data = {
                "map_poll_aps": 80,
                "debug_mode": True,
                "health_poll_interval": 15
            }
            with open(import_path, 'w') as f:
                json.dump(import_data, f)
            
            # Import config
            config = import_config(str(import_path))
            
            # Verify imported values
            assert config.map_poll_aps == 80
            assert config.debug_mode is True
            assert config.health_poll_interval == 15
            
    def test_import_config_invalid_file(self, tmp_path):
        """Test importing configuration from invalid file."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create invalid import file
            import_path = tmp_path / "invalid_config.json"
            with open(import_path, 'w') as f:
                f.write("invalid json")
            
            # Should raise error
            with pytest.raises(ConfigError, match="Failed to import configuration"):
                import_config(str(import_path))
                
    def test_export_import_roundtrip(self, tmp_path):
        """Test export/import roundtrip maintains data integrity."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            # Create original config
            original_config = Config()
            original_config.map_poll_aps = 35
            original_config.debug_mode = True
            original_config.log_paths = ["/var/log/app.log", "/var/log/error.log"]
            original_config.dashboard_layout = [{"widget": "test", "size": [100, 200]}]
            
            # Export config
            export_path = tmp_path / "roundtrip_config.json"
            export_config(original_config, str(export_path))
            
            # Import config
            imported_config = import_config(str(export_path))
            
            # Verify all values match
            assert imported_config.map_poll_aps == 35
            assert imported_config.debug_mode is True
            assert imported_config.log_paths == ["/var/log/app.log", "/var/log/error.log"]
            assert imported_config.dashboard_layout == [{"widget": "test", "size": [100, 200]}]


class TestConfigurationEdgeCases:
    """Test configuration edge cases and error conditions."""
    
    def test_config_with_unicode_characters(self, tmp_path):
        """Test configuration with unicode characters."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            config.offline_tile_path = "/mnt/ssd/tiles/测试.mbtiles"
            config.log_paths = ["/var/log/应用.log"]
            
            # Save and load
            save_config(config)
            loaded_config = load_config()
            
            assert loaded_config.offline_tile_path == "/mnt/ssd/tiles/测试.mbtiles"
            assert loaded_config.log_paths == ["/var/log/应用.log"]
            
    def test_config_with_very_large_values(self, tmp_path):
        """Test configuration with very large numeric values."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            config.map_poll_aps = 999999
            config.tile_cache_limit_mb = 99999
            
            # Save and load
            save_config(config)
            loaded_config = load_config()
            
            assert loaded_config.map_poll_aps == 999999
            assert loaded_config.tile_cache_limit_mb == 99999
            
    def test_config_concurrent_access(self, tmp_path):
        """Test configuration concurrent access scenarios."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            import threading
            import time
            
            results = []
            
            def save_config_worker(poll_value):
                config = Config()
                config.map_poll_aps = poll_value
                save_config(config)
                time.sleep(0.01)  # Small delay
                loaded_config = load_config()
                results.append(loaded_config.map_poll_aps)
            
            # Start multiple threads
            threads = []
            for i in range(5):
                thread = threading.Thread(target=save_config_worker, args=(i * 10,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads
            for thread in threads:
                thread.join()
            
            # Verify all operations completed
            assert len(results) == 5
            
    def test_config_permission_errors(self, tmp_path):
        """Test configuration permission error handling."""
        with patch('piwardrive.core.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            config.map_poll_aps = 50
            
            # Create read-only directory
            readonly_dir = tmp_path / "readonly"
            readonly_dir.mkdir()
            readonly_dir.chmod(0o444)  # Read-only
            
            with patch('piwardrive.core.config.CONFIG_DIR', str(readonly_dir)):
                try:
                    # Should handle permission error gracefully
                    save_config(config)
                except PermissionError:
                    # This is expected
                    pass
                finally:
                    # Clean up - restore write permissions
                    readonly_dir.chmod(0o755)
