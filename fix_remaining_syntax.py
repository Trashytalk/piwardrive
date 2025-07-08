#!/usr/bin/env python3
"""
Enhanced syntax error fix script with specific patterns for each error type.
"""

import os
import re
import ast
from pathlib import Path

def fix_unterminated_string_literals(file_path):
    """Fix unterminated string literals."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common patterns for broken string literals
        patterns = [
            # Pattern 1: Simple broken strings across lines
            (r'("[^"]*),\s*\n\s*([^"]*")', r'\1,\2'),
            
            # Pattern 2: SQL/multiline strings with broken quotes
            (r'"""([^"]*)\n([^"]*)\n([^"]*?)"""', r'"""\1\2\3"""'),
            
            # Pattern 3: f-strings that are broken
            (r'f"([^"]*)\n\s*([^"]*)"', r'f"\1\2"'),
            
            # Pattern 4: Complex multi-line strings
            (r'"([^"]*)\n\s*([^"]*)\n\s*([^"]*)"', r'"\1\2\3"'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # Specific pattern for coordinates in XML/KML
        content = re.sub(
            r'<coordinates>([^<]*),\s*\n\s*([^<]*),\s*\n\s*([^<]*)</coordinates>',
            r'<coordinates>\1,\2,\3</coordinates>',
            content,
            flags=re.MULTILINE
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing string literals in {file_path}: {e}")
        return False

def fix_line_continuation_errors(file_path):
    """Fix unexpected character after line continuation character."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove trailing whitespace after backslash
        content = re.sub(r'\\\s+', r'\\', content)
        
        # Fix common line continuation patterns
        content = re.sub(r'\\\n\s*\n', r'\\\n', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error fixing line continuation in {file_path}: {e}")
        return False

def fix_unexpected_indentation(file_path):
    """Fix unexpected indentation errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        for i, line in enumerate(lines):
            # Check for lines that start with unexpected indentation
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                # This is likely a line that should be at module level
                fixed_lines.append(line)
            elif line.strip() and line.startswith('    ') and i > 0:
                # Check if this is unexpected indentation
                prev_line = lines[i-1].strip()
                if prev_line and not prev_line.endswith(':') and not prev_line.endswith('\\'):
                    # This might be wrongly indented
                    if any(keyword in line for keyword in ['import ', 'from ', 'def ', 'class ', 'if __name__']):
                        fixed_lines.append(line.lstrip())
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        return True
        
    except Exception as e:
        print(f"Error fixing indentation in {file_path}: {e}")
        return False

def fix_invalid_syntax_patterns(file_path):
    """Fix common invalid syntax patterns."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix common invalid syntax patterns
        patterns = [
            # Missing colon after if/for/while/def/class
            (r'(\s*(?:if|for|while|def|class|try|except|finally|with)\s+[^:]+)\s*\n', r'\1:\n'),
            
            # Missing quotes around strings
            (r'(\s*=\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*$', r'\1"\2"'),
            
            # Fix broken f-strings
            (r'f"([^"]*)\{([^}]*)\}([^"]*)"', r'f"\1{\2}\3"'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error fixing invalid syntax in {file_path}: {e}")
        return False

def main():
    """Fix syntax errors in specific files."""
    
    # Files with remaining syntax errors
    error_files = [
        # Unterminated string literals
        'tests/test_vector_tiles_module.py',
        'tests/test_widget_plugins.py',
        'scripts/migrate_enhanced_schema.py',
        'scripts/enhance_schema.py',
        'scripts/database_optimizer.py',
        'scripts/check_api_compatibility.py',
        'scripts/critical_db_improvements.py',
        'scripts/init_database.py',
        'scripts/optimize_database.py',
        'scripts/advanced_analytics_service.py',
        
        # Unexpected indentation
        'scripts/run_migrations.py',
        'scripts/check_migration_status.py',
        
        # Line continuation errors
        'scripts/problem_reporter.py',
        'scripts/field_status_indicators.py',
        'scripts/field_diagnostics.py',
        'scripts/create_performance_baseline.py',
        'tests/utils/metrics.py',
        
        # Invalid syntax
        'tests/test_plot_cpu_temp_no_pandas.py',
    ]
    
    base_dir = Path(__file__).parent
    fixed_count = 0
    
    for file_rel_path in error_files:
        file_path = base_dir / file_rel_path
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
            
        print(f"Fixing {file_rel_path}...")
        
        # Try different fixing strategies
        fixed = False
        
        # 1. Fix unterminated string literals
        if fix_unterminated_string_literals(file_path):
            fixed = True
        
        # 2. Fix line continuation errors
        if fix_line_continuation_errors(file_path):
            fixed = True
        
        # 3. Fix unexpected indentation
        if fix_unexpected_indentation(file_path):
            fixed = True
        
        # 4. Fix invalid syntax patterns
        if fix_invalid_syntax_patterns(file_path):
            fixed = True
        
        if fixed:
            fixed_count += 1
            
            # Test if the file compiles now
            try:
                with open(file_path, 'r') as f:
                    compile(f.read(), str(file_path), 'exec')
                print(f"✓ {file_rel_path} now compiles successfully")
            except SyntaxError as e:
                print(f"✗ {file_rel_path} still has syntax errors: {e}")
        else:
            print(f"- No fixes applied to {file_rel_path}")
    
    print(f"\nProcessed {len(error_files)} files, {fixed_count} were modified")

if __name__ == '__main__':
    main()
