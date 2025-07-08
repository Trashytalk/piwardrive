#!/usr/bin/env python3
"""
Focused code quality improvements for main target modules.
"""

import re
from pathlib import Path
from typing import Dict, List

def fix_unused_imports(file_path: Path, unused_imports: List[str]) -> bool:
    """Remove unused imports from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            should_remove = False
            
            # Check if this line contains any unused imports
            for unused_import in unused_imports:
                # Extract the import name from the issue description
                import_match = re.search(r"Unused import '([^']+)'", unused_import)
                if import_match:
                    import_name = import_match.group(1)
                    
                    # Check if this line imports the unused module
                    if f"import {import_name}" in line or f"from {import_name.split('.')[0]} import" in line:
                        # Check if it's the exact import we want to remove
                        if import_name in line:
                            should_remove = True
                            break
            
            if not should_remove:
                fixed_lines.append(line)
        
        # Only write if we made changes
        new_content = '\n'.join(fixed_lines)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error fixing unused imports in {file_path}: {e}")
        return False

def add_missing_docstrings(file_path: Path, missing_docstrings: List[str]) -> bool:
    """Add missing docstrings to functions and classes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            fixed_lines.append(line)
            
            # Check if this line defines a function or class missing a docstring
            for missing_docstring in missing_docstrings:
                line_match = re.search(r"Line (\d+): Missing docstring for (function|class) '([^']+)'", missing_docstring)
                if line_match:
                    line_num = int(line_match.group(1))
                    item_type = line_match.group(2)
                    item_name = line_match.group(3)
                    
                    # Check if this is the line we need to fix
                    if i + 1 == line_num:
                        # Add a basic docstring
                        indent = len(line) - len(line.lstrip())
                        indent_str = ' ' * (indent + 4)
                        
                        if item_type == 'function':
                            docstring = f'{indent_str}"""{item_name.replace("_", " ").title()} function."""'
                        else:  # class
                            docstring = f'{indent_str}"""{item_name.replace("_", " ").title()} class."""'
                        
                        fixed_lines.append(docstring)
        
        # Only write if we made changes
        new_content = '\n'.join(fixed_lines)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error adding docstrings to {file_path}: {e}")
        return False

def fix_maintainability_issues(file_path: Path, maintainability_issues: List[str]) -> bool:
    """Fix maintainability issues like long lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Check for long lines
            if len(line) > 120:
                # Try to break the line intelligently
                if ',' in line and len(line) > 120:
                    # For function calls or lists, break at commas
                    parts = line.split(',')
                    if len(parts) > 1:
                        indent = len(line) - len(line.lstrip())
                        indent_str = ' ' * (indent + 4)
                        
                        fixed_lines.append(parts[0] + ',')
                        for part in parts[1:-1]:
                            fixed_lines.append(indent_str + part.strip() + ',')
                        fixed_lines.append(indent_str + parts[-1].strip())
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        # Only write if we made changes
        new_content = '\n'.join(fixed_lines)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error fixing maintainability issues in {file_path}: {e}")
        return False

def main():
    """Main function to fix code quality issues."""
    
    # Focus on our main target modules
    target_modules = [
        'src/piwardrive/fastjson.py',
        'src/piwardrive/models/api_models.py',
        'src/piwardrive/logging/structured_logger.py',
        'src/piwardrive/localization.py',
        'src/piwardrive/cache.py',
        'src/piwardrive/interfaces.py'
    ]
    
    # Parse the comprehensive analysis report
    report_file = Path("comprehensive_code_quality_report.md")
    if not report_file.exists():
        print("Comprehensive analysis report not found. Run comprehensive_code_analyzer.py first.")
        return
    
    with open(report_file, 'r') as f:
        report_content = f.read()
    
    # Extract issues for each target module
    file_issues = {}
    current_file = None
    current_section = None
    
    for line in report_content.split('\n'):
        if line.startswith('## '):
            current_section = line[3:].strip()
        elif line.startswith('### '):
            current_file = line[4:].strip()
            if current_file not in file_issues:
                file_issues[current_file] = {}
            if current_section not in file_issues[current_file]:
                file_issues[current_file][current_section] = []
        elif line.startswith('- ') and current_file and current_section:
            file_issues[current_file][current_section].append(line[2:].strip())
    
    # Fix issues in target modules
    fixes_applied = 0
    
    for module_path in target_modules:
        module_name = module_path.split('/')[-1]
        
        print(f"\nProcessing {module_path}...")
        
        # Find issues for this module
        module_issues = {}
        for file_path, issues in file_issues.items():
            if module_name in file_path or module_path in file_path:
                module_issues = issues
                break
        
        if not module_issues:
            print(f"No issues found for {module_path}")
            continue
        
        file_path = Path(module_path)
        if not file_path.exists():
            print(f"Module not found: {module_path}")
            continue
        
        # Fix unused imports
        if 'Import Issues' in module_issues:
            if fix_unused_imports(file_path, module_issues['Import Issues']):
                print(f"✓ Fixed unused imports in {module_path}")
                fixes_applied += 1
        
        # Add missing docstrings
        if 'Missing Docstrings' in module_issues:
            if add_missing_docstrings(file_path, module_issues['Missing Docstrings']):
                print(f"✓ Added missing docstrings to {module_path}")
                fixes_applied += 1
        
        # Fix maintainability issues
        if 'Maintainability Issues' in module_issues:
            if fix_maintainability_issues(file_path, module_issues['Maintainability Issues']):
                print(f"✓ Fixed maintainability issues in {module_path}")
                fixes_applied += 1
    
    print(f"\nApplied {fixes_applied} fixes to target modules")
    
    # Test that modules still compile
    print("\nTesting module compilation...")
    for module_path in target_modules:
        try:
            with open(module_path, 'r') as f:
                content = f.read()
            compile(content, module_path, 'exec')
            print(f"✓ {module_path} compiles successfully")
        except Exception as e:
            print(f"✗ {module_path} compilation error: {e}")

if __name__ == '__main__':
    main()
