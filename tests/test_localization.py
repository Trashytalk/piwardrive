#!/usr/bin/env python3

"""
Comprehensive test suite for localization.py module.
Tests simple localization functionality with JSON locale files.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from piwardrive import localization


class TestLocalizationBasics:
    """Test basic localization functionality."""

    def test_default_locale_is_en(self):
        """Test that default locale is English."""
        # Reset to default state
        with mock.patch.dict(os.environ, {}, clear=True):
            # Reload the module to get fresh default
            import importlib
            importlib.reload(localization)
            # The default should be 'en' when PW_LANG is not set
            assert localization._current in ['en', 'en']  # Default fallback

    def test_environment_variable_sets_locale(self):
        """Test that PW_LANG environment variable sets the locale."""
        with mock.patch.dict(os.environ, {'PW_LANG': 'fr'}):
            import importlib
            importlib.reload(localization)
            assert localization._current == 'fr'

    def test_set_locale_changes_current(self):
        """Test that set_locale changes the current locale."""
        original = localization._current
        try:
            localization.set_locale('es')
            assert localization._current == 'es'
        finally:
            localization.set_locale(original)

    def test_translate_alias(self):
        """Test that _ is an alias for translate."""
        assert localization._ is localization.translate


class TestTranslationFunctionality:
    """Test translation and locale loading functionality."""

    def setup_method(self):
        """Clear the LRU cache before each test."""
        localization._load_locale.cache_clear()

    def test_translate_returns_key_when_no_translation(self):
        """Test that translate returns the key when no translation exists."""
        # Set to a locale that doesn't exist
        localization.set_locale('nonexistent')
        result = localization.translate('test.key')
        assert result == 'test.key'

    def test_translate_with_mock_locale_file(self):
        """Test translation with a mocked locale file."""
        test_translations = {
            'hello': 'Hola',
            'goodbye': 'Adiós',
            'welcome.message': 'Bienvenido'
        }
        
        # Mock the file reading
        mock_path = '/fake/path/locales/es.json'
        mock_open = mock.mock_open(read_data=json.dumps(test_translations))
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value=mock_path):
                localization.set_locale('es')
                
                assert localization.translate('hello') == 'Hola'
                assert localization.translate('goodbye') == 'Adiós'
                assert localization.translate('welcome.message') == 'Bienvenido'
                assert localization.translate('nonexistent') == 'nonexistent'

    def test_load_locale_file_not_found(self):
        """Test _load_locale handles missing files gracefully."""
        with mock.patch('builtins.open', side_effect=FileNotFoundError()):
            result = localization._load_locale('missing')
            assert result == {}

    def test_load_locale_invalid_json(self):
        """Test _load_locale handles invalid JSON gracefully."""
        mock_open = mock.mock_open(read_data='invalid json content')
        
        with mock.patch('builtins.open', mock_open):
            result = localization._load_locale('invalid')
            assert result == {}

    def test_load_locale_io_error(self):
        """Test _load_locale handles IO errors gracefully."""
        with mock.patch('builtins.open', side_effect=OSError("Permission denied")):
            result = localization._load_locale('permission_error')
            assert result == {}

    def test_load_locale_encoding_error(self):
        """Test _load_locale handles encoding errors gracefully."""
        with mock.patch('builtins.open', side_effect=UnicodeDecodeError('utf-8', b'', 0, 1, 'test')):
            result = localization._load_locale('encoding_error')
            assert result == {}


class TestCaching:
    """Test LRU caching behavior."""

    def setup_method(self):
        """Clear the LRU cache before each test."""
        localization._load_locale.cache_clear()

    def test_lru_cache_is_used(self):
        """Test that LRU cache prevents repeated file reads."""
        test_translations = {'test': 'prueba'}
        mock_open = mock.mock_open(read_data=json.dumps(test_translations))
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value='/fake/path'):
                # First call should read the file
                result1 = localization._load_locale('es')
                assert result1 == test_translations
                
                # Second call should use cache (file shouldn't be read again)
                result2 = localization._load_locale('es')
                assert result2 == test_translations
                
                # Verify file was only opened once
                assert mock_open.call_count == 1

    def test_cache_different_locales(self):
        """Test that different locales are cached separately."""
        es_translations = {'hello': 'Hola'}
        fr_translations = {'hello': 'Bonjour'}
        
        def mock_open_side_effect(*args, **kwargs):
            filename = args[0]
            if 'es.json' in filename:
                return mock.mock_open(read_data=json.dumps(es_translations))(*args, **kwargs)
            elif 'fr.json' in filename:
                return mock.mock_open(read_data=json.dumps(fr_translations))(*args, **kwargs)
            else:
                raise FileNotFoundError()
        
        with mock.patch('builtins.open', side_effect=mock_open_side_effect):
            with mock.patch('os.path.join') as mock_join:
                mock_join.side_effect = lambda base, locale, filename: f'/fake/{locale}/{filename}'
                
                result_es = localization._load_locale('es')
                result_fr = localization._load_locale('fr')
                
                assert result_es == es_translations
                assert result_fr == fr_translations


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_multiple_locale_switches(self):
        """Test switching between multiple locales."""
        # Clear any cached values first
        localization._load_locale.cache_clear()
        
        # Mock different locale files
        locales = {
            'en': {'greeting': 'Hello', 'farewell': 'Goodbye'},
            'es': {'greeting': 'Hola', 'farewell': 'Adiós'},
            'fr': {'greeting': 'Bonjour', 'farewell': 'Au revoir'}
        }
        
        def mock_open_side_effect(filename, *args, **kwargs):
            for locale, translations in locales.items():
                if f'{locale}.json' in filename:
                    return mock.mock_open(read_data=json.dumps(translations))(filename, *args, **kwargs)
            raise FileNotFoundError()
        
        with mock.patch('builtins.open', side_effect=mock_open_side_effect):
            with mock.patch('os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: f'/fake/{"/".join(args[1:])}'
                
                # Test English
                localization._load_locale.cache_clear()
                localization.set_locale('en')
                assert localization.translate('greeting') == 'Hello'
                assert localization.translate('farewell') == 'Goodbye'
                
                # Test Spanish
                localization._load_locale.cache_clear()
                localization.set_locale('es')
                assert localization.translate('greeting') == 'Hola'
                assert localization.translate('farewell') == 'Adiós'
                
                # Test French
                localization._load_locale.cache_clear()
                localization.set_locale('fr')
                assert localization.translate('greeting') == 'Bonjour'
                assert localization.translate('farewell') == 'Au revoir'

    def test_partial_translations(self):
        """Test behavior when some keys are missing in translation file."""
        partial_translations = {'greeting': 'Hola'}  # Missing 'farewell'
        
        mock_open = mock.mock_open(read_data=json.dumps(partial_translations))
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value='/fake/path'):
                # Clear cache to ensure fresh load
                localization._load_locale.cache_clear()
                localization.set_locale('es')
                
                # Should translate existing key
                assert localization.translate('greeting') == 'Hola'
                
                # Should return key itself for missing translation
                assert localization.translate('farewell') == 'farewell'
                assert localization.translate('unknown.key') == 'unknown.key'

    def test_empty_locale_file(self):
        """Test behavior with empty locale file."""
        mock_open = mock.mock_open(read_data='{}')
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value='/fake/path'):
                localization.set_locale('empty')
                
                # All translations should return the key itself
                assert localization.translate('any.key') == 'any.key'
                assert localization.translate('test') == 'test'


class TestFilePathConstruction:
    """Test that file paths are constructed correctly."""

    def test_locale_file_path_construction(self):
        """Test that locale file paths are constructed correctly."""
        with mock.patch('os.path.join') as mock_join:
            with mock.patch('os.path.dirname') as mock_dirname:
                with mock.patch('builtins.open', side_effect=FileNotFoundError()):
                    mock_dirname.return_value = '/app/piwardrive'
                    mock_join.return_value = '/app/piwardrive/locales/test.json'
                    
                    localization._load_locale('test')
                    
                    # Verify correct path construction
                    mock_dirname.assert_called_once()
                    mock_join.assert_called_once_with('/app/piwardrive', 'locales', 'test.json')

    def test_unicode_handling_in_translations(self):
        """Test that Unicode characters in translations are handled correctly."""
        unicode_translations = {
            'emoji': '🚀 Rocket',
            'chinese': '你好世界',
            'accents': 'Café, naïve, résumé',
            'symbols': '© 2023 • ™ ® ℠'
        }
        
        mock_open = mock.mock_open(read_data=json.dumps(unicode_translations, ensure_ascii=False))
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value='/fake/path'):
                localization.set_locale('unicode')
                
                assert localization.translate('emoji') == '🚀 Rocket'
                assert localization.translate('chinese') == '你好世界'
                assert localization.translate('accents') == 'Café, naïve, résumé'
                assert localization.translate('symbols') == '© 2023 • ™ ® ℠'


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_none_and_empty_keys(self):
        """Test behavior with None and empty string keys."""
        localization.set_locale('en')
        
        # Empty string key
        assert localization.translate('') == ''
        
        # None should work but return None converted to string
        assert localization.translate(str(None)) == 'None'

    def test_numeric_and_special_keys(self):
        """Test behavior with numeric and special character keys."""
        special_translations = {
            '123': 'number key',
            'key.with.dots': 'dotted key',
            'key-with-dashes': 'dashed key',
            'key_with_underscores': 'underscore key',
            'UPPERCASE': 'upper key'
        }
        
        mock_open = mock.mock_open(read_data=json.dumps(special_translations))
        
        with mock.patch('builtins.open', mock_open):
            with mock.patch('os.path.join', return_value='/fake/path'):
                localization.set_locale('special')
                
                assert localization.translate('123') == 'number key'
                assert localization.translate('key.with.dots') == 'dotted key'
                assert localization.translate('key-with-dashes') == 'dashed key'
                assert localization.translate('key_with_underscores') == 'underscore key'
                assert localization.translate('UPPERCASE') == 'upper key'

    def test_locale_switching_clears_previous_context(self):
        """Test that switching locales doesn't leak previous translations."""
        # Setup two different locales with different translations for same keys
        en_translations = {'color': 'color', 'center': 'center'}
        uk_translations = {'color': 'colour', 'center': 'centre'}
        
        def mock_open_side_effect(*args, **kwargs):
            filename = args[0]
            if 'en.json' in filename:
                return mock.mock_open(read_data=json.dumps(en_translations))(*args, **kwargs)
            elif 'uk.json' in filename:
                return mock.mock_open(read_data=json.dumps(uk_translations))(*args, **kwargs)
            raise FileNotFoundError()
        
        with mock.patch('builtins.open', side_effect=mock_open_side_effect):
            with mock.patch('os.path.join') as mock_join:
                mock_join.side_effect = lambda base, locale, filename: f'/fake/{locale}/{filename}'
                
                # Start with US English
                localization.set_locale('en')
                assert localization.translate('color') == 'color'
                assert localization.translate('center') == 'center'
                
                # Switch to UK English
                localization.set_locale('uk')
                assert localization.translate('color') == 'colour'
                assert localization.translate('center') == 'centre'


if __name__ == "__main__":
    pytest.main([__file__])
