#!/usr/bin/env python3

"""
Comprehensive test suite for fastjson.py module.
Tests JSON serialization/deserialization with various backends.
"""

import json
import sys
from pathlib import Path
from unittest import mock
from typing import Any, Dict, List

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestFastJSON:
    """Test suite for fastjson module functionality."""

    def test_loads_basic_data_types(self):
        """Test loading basic JSON data types."""
        # Import here to ensure we get the actual module being tested
        from piwardrive import fastjson
        
        # Test basic types
        assert fastjson.loads('null') is None
        assert fastjson.loads('true') is True
        assert fastjson.loads('false') is False
        assert fastjson.loads('42') == 42
        assert fastjson.loads('3.14') == 3.14
        assert fastjson.loads('"hello"') == "hello"

    def test_loads_complex_data_structures(self):
        """Test loading complex JSON structures."""
        from piwardrive import fastjson
        
        # Test array
        array_data = '[1, 2, 3, "test"]'
        result = fastjson.loads(array_data)
        assert result == [1, 2, 3, "test"]
        
        # Test object
        object_data = '{"name": "test", "value": 42, "active": true}'
        result = fastjson.loads(object_data)
        assert result == {"name": "test", "value": 42, "active": True}
        
        # Test nested structure
        nested_data = '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'
        result = fastjson.loads(nested_data)
        expected = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        assert result == expected

    def test_loads_with_bytes_input(self):
        """Test loading JSON from bytes input."""
        from piwardrive import fastjson
        
        data = b'{"test": "value"}'
        result = fastjson.loads(data)
        assert result == {"test": "value"}

    def test_loads_invalid_json_raises_exception(self):
        """Test that invalid JSON raises appropriate exception."""
        from piwardrive import fastjson
        
        with pytest.raises((ValueError, TypeError)):
            fastjson.loads('{"invalid": json}')
        
        with pytest.raises((ValueError, TypeError)):
            fastjson.loads('{"unclosed": "object"')

    def test_dumps_basic_data_types(self):
        """Test dumping basic Python data types to JSON."""
        from piwardrive import fastjson
        
        assert fastjson.dumps(None) == "null"
        assert fastjson.dumps(True) == "true"
        assert fastjson.dumps(False) == "false"
        assert fastjson.dumps(42) == "42"
        assert fastjson.dumps(3.14) == "3.14"
        assert fastjson.dumps("hello") == '"hello"'

    def test_dumps_complex_data_structures(self):
        """Test dumping complex Python structures to JSON."""
        from piwardrive import fastjson
        
        # Test list
        data = [1, 2, 3, "test"]
        result = fastjson.dumps(data)
        # Parse back to verify correctness
        assert json.loads(result) == data
        
        # Test dictionary
        data = {"name": "test", "value": 42, "active": True}
        result = fastjson.dumps(data)
        assert json.loads(result) == data
        
        # Test nested structure
        data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        result = fastjson.dumps(data)
        assert json.loads(result) == data

    def test_dumps_returns_string(self):
        """Test that dumps always returns a string, not bytes."""
        from piwardrive import fastjson
        
        data = {"test": "value"}
        result = fastjson.dumps(data)
        assert isinstance(result, str)
        assert '"test"' in result
        assert '"value"' in result

    def test_dumps_with_kwargs(self):
        """Test dumps with additional keyword arguments."""
        from piwardrive import fastjson
        
        data = {"b": 2, "a": 1}
        
        # Test that kwargs are passed through (if supported by backend)
        try:
            result = fastjson.dumps(data, sort_keys=True)
            # If sort_keys is supported, the result should have keys in order
            assert isinstance(result, str)
        except TypeError:
            # Some backends might not support sort_keys, which is fine
            pass

    def test_round_trip_consistency(self):
        """Test that loads(dumps(data)) == data for various data types."""
        from piwardrive import fastjson
        
        test_cases = [
            None,
            True,
            False,
            42,
            3.14,
            "hello world",
            [1, 2, 3],
            {"name": "test", "value": 42},
            {"nested": {"data": [1, 2, {"inner": True}]}},
            [],
            {},
        ]
        
        for original_data in test_cases:
            json_str = fastjson.dumps(original_data)
            restored_data = fastjson.loads(json_str)
            assert restored_data == original_data

    def test_unicode_handling(self):
        """Test proper handling of Unicode characters."""
        from piwardrive import fastjson
        
        unicode_data = {"emoji": "🚀", "chinese": "你好", "special": "àáâãäå"}
        json_str = fastjson.dumps(unicode_data)
        restored = fastjson.loads(json_str)
        assert restored == unicode_data

    def test_empty_inputs(self):
        """Test handling of empty inputs."""
        from piwardrive import fastjson
        
        # Empty string should raise an exception
        with pytest.raises((ValueError, TypeError)):
            fastjson.loads("")
        
        # Empty dict and list should work fine
        assert fastjson.dumps({}) == "{}"
        assert fastjson.dumps([]) == "[]"
        assert fastjson.loads("{}") == {}
        assert fastjson.loads("[]") == []


class TestBackendSelection:
    """Test that different JSON backends are properly selected."""

    def test_fallback_to_builtin_json(self):
        """Test fallback to builtin json when accelerated libraries are unavailable."""
        # Mock both orjson and ujson as unavailable
        with mock.patch.dict('sys.modules', {'orjson': None, 'ujson': None}):
            # Force reimport of fastjson module
            if 'piwardrive.fastjson' in sys.modules:
                del sys.modules['piwardrive.fastjson']
            
            from piwardrive import fastjson
            
            # Should still work with builtin json
            data = {"test": "value"}
            json_str = fastjson.dumps(data)
            result = fastjson.loads(json_str)
            assert result == data

    def test_module_exports(self):
        """Test that the module exports the expected interface."""
        from piwardrive import fastjson
        
        # Check that required functions are available
        assert hasattr(fastjson, 'loads')
        assert hasattr(fastjson, 'dumps')
        assert callable(fastjson.loads)
        assert callable(fastjson.dumps)
        
        # Check __all__ export
        assert hasattr(fastjson, '__all__')
        assert 'loads' in fastjson.__all__
        assert 'dumps' in fastjson.__all__


class TestPerformanceCompatibility:
    """Test compatibility with different JSON performance libraries."""

    def test_large_data_structures(self):
        """Test handling of reasonably large data structures."""
        from piwardrive import fastjson
        
        # Create a moderately large data structure
        large_data = {
            f"key_{i}": {
                "id": i,
                "values": list(range(10)),
                "metadata": {"created": f"2023-{i:02d}-01", "active": i % 2 == 0}
            }
            for i in range(100)
        }
        
        # Should handle this without issues
        json_str = fastjson.dumps(large_data)
        restored = fastjson.loads(json_str)
        assert restored == large_data

    def test_deeply_nested_structures(self):
        """Test handling of deeply nested data structures."""
        from piwardrive import fastjson
        
        # Create a deeply nested structure (but not too deep to avoid recursion limits)
        nested_data = {"level": 0}
        current = nested_data
        for i in range(1, 20):
            current["next"] = {"level": i}
            current = current["next"]
        
        json_str = fastjson.dumps(nested_data)
        restored = fastjson.loads(json_str)
        assert restored == nested_data


if __name__ == "__main__":
    pytest.main([__file__])
