#!/usr/bin/env python3
"""
Script to fix syntax errors identified in the code analysis.
"""

import os
import re
import sys
from pathlib import Path

def fix_unterminated_strings(file_path):
    """Fix unterminated string literals by properly joining broken lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to find broken string literals with coordinates
        # This pattern matches strings that are broken across lines
        patterns = [
            # Fix broken coordinates in KML strings
            (r'("<[^"]*<coordinates>[^"]*),\n\s+([^"]*),\n\s+([^"]*</coordinates>[^"]*")', 
             r'\1,\2,\3'),
            
            # Fix other broken string literals
            (r'("[^"]*),\n\s+([^"]*")', r'\1,\2'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # If content changed, write it back
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed string literals in {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def fix_unexpected_indents(file_path):
    """Fix unexpected indentation errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        
        for i, line in enumerate(lines):
            # Check for unexpected indentation after empty lines or specific patterns
            if line.strip() and line.startswith('    ') and i > 0:
                prev_line = lines[i-1].strip()
                if not prev_line or prev_line.endswith(':'):
                    # This might be a continuation line that should be dedented
                    continue
                
                # Check if this line should be at module level
                if any(keyword in line for keyword in ['import ', 'from ', 'def ', 'class ']):
                    lines[i] = line.lstrip()
                    modified = True
                    print(f"Fixed indentation on line {i+1} in {file_path}")
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing indentation in {file_path}: {e}")
        return False

def fix_file_specific_issues(file_path):
    """Fix specific known issues in certain files."""
    file_name = os.path.basename(file_path)
    
    # Specific fixes for known problematic files
    if file_name == 'test_utils.py':
        return fix_test_utils_kml_strings(file_path)
    
    return False

def fix_test_utils_kml_strings(file_path):
    """Specifically fix the KML string issue in test_utils.py."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the specific broken KML string
        broken_pattern = r'"<Placemark><n>Line</n><LineString><coordinates>0,\s+0 1,\s+1</coordinates></LineString></Placemark>"'
        fixed_replacement = '"<Placemark><n>Line</n><LineString><coordinates>0,0 1,1</coordinates></LineString></Placemark>"'
        
        content = re.sub(broken_pattern, fixed_replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        broken_pattern2 = r'"<Placemark><n>Pt</n><Point><coordinates>2,\s+2</coordinates></Point></Placemark>"'
        fixed_replacement2 = '"<Placemark><n>Pt</n><Point><coordinates>2,2</coordinates></Point></Placemark>"'
        
        content = re.sub(broken_pattern2, fixed_replacement2, content, flags=re.MULTILINE | re.DOTALL)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed KML strings in {file_path}")
        return True
        
    except Exception as e:
        print(f"Error fixing KML strings in {file_path}: {e}")
        return False

def main():
    """Main function to fix syntax errors."""
    base_dir = Path(__file__).parent
    
    # List of files with syntax errors from the analysis
    syntax_error_files = [
        'tests/test_utils.py',
        'tests/test_performance_comprehensive.py',
        'tests/test_plot_cpu_temp_no_pandas.py',
        'tests/test_performance_dashboard_integration.py',
        'tests/test_vector_tiles_module.py',
        'tests/test_widget_plugins.py',
        'examples/direction_finding_example.py',
        'scripts/migrate_enhanced_schema.py',
        'scripts/enhance_schema.py',
        'scripts/database_optimizer.py',
        'scripts/run_migrations.py',
        'scripts/simple_db_check.py',
        'scripts/check_migration_status.py',
        'scripts/problem_reporter.py',
        'scripts/test_database_functions.py',
        'scripts/field_status_indicators.py',
        'scripts/field_diagnostics.py',
        'scripts/check_api_compatibility.py',
        'scripts/critical_db_improvements.py',
        'scripts/init_database.py',
        'scripts/optimize_database.py',
        'scripts/create_performance_baseline.py',
        'scripts/advanced_analytics_service.py',
        'tests/utils/metrics.py',
    ]
    
    fixed_count = 0
    
    for file_rel_path in syntax_error_files:
        file_path = base_dir / file_rel_path
        
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue
            
        print(f"Checking {file_rel_path}...")
        
        # Try different fixing strategies
        fixed = False
        
        # 1. Try file-specific fixes first
        if fix_file_specific_issues(file_path):
            fixed = True
        
        # 2. Try general string literal fixes
        elif fix_unterminated_strings(file_path):
            fixed = True
        
        # 3. Try indentation fixes
        elif fix_unexpected_indents(file_path):
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
            print(f"- No automatic fixes applied to {file_rel_path}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
