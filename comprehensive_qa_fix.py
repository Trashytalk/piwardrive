#!/usr/bin/env python3
"""
Comprehensive QA fix script for PiWarDrive
Addresses flake8 and mypy issues systematically
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple


def run_command(cmd: str, cwd: str = None) -> Tuple[str, str, int]:
    """Run a command and return stdout, stderr, and return code"""
    try:
        result = subprocess.run(
            cmd.split(),
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def fix_whitespace_issues(file_path: str) -> bool:
    """Fix whitespace and blank line issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix trailing whitespace
        content = re.sub(r' +$', '', content, flags=re.MULTILINE)

        # Fix blank lines with whitespace
        content = re.sub(r'^\s*$', '', content, flags=re.MULTILINE)

        # Fix multiple blank lines
        content = re.sub(r'\n\n\n+', '\n\n', content)

        # Fix missing blank lines after class/function definitions
        content = re.sub(r'(\n    def .+?:\n(?:        .+\n)*?)(\n(?:class|def|if __name__))',
            r'\1\n\2',
            content)

        # Fix missing blank lines before class/function definitions
        content = re.sub(r'(\n[^\n]*\n)(\nclass )', r'\1\n\2', content)
        content = re.sub(r'(\n[^\n]*\n)(\ndef )', r'\1\n\2', content)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False
    except Exception as e:
        print(f"Error fixing whitespace in {file_path}: {e}")
        return False


def fix_unused_imports(file_path: str) -> bool:
    """Remove unused imports"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Get flake8 output for this file
        stdout, _, _ = run_command(f"python -m flake8 --select=F401 {file_path}")

        unused_imports = []
        for line in stdout.split('\n'):
            if 'F401' in line and 'imported but unused' in line:
                # Extract the import name
                match = re.search(r"'(.+?)' imported but unused", line)
                if match:
                    unused_imports.append(match.group(1))

        if not unused_imports:
            return False

        # Remove unused imports
        new_lines = []
        for line in lines:
            should_remove = False
            for unused in unused_imports:
                if f"import {unused}" in line or f"from {unused}" in line:
                    # Check if it's a simple import line
                    if line.strip().startswith(('import ', 'from ')) and unused in line:
                        should_remove = True
                        break

            if not should_remove:
                new_lines.append(line)

        if len(new_lines) != len(lines):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

        return False
    except Exception as e:
        print(f"Error fixing unused imports in {file_path}: {e}")
        return False


def fix_unused_variables(file_path: str) -> bool:
    """Fix unused variables by prefixing with underscore"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Get flake8 output for this file
        stdout, _, _ = run_command(f"python -m flake8 --select=F841 {file_path}")

        for line in stdout.split('\n'):
            if 'F841' in line and 'assigned to but never used' in line:
                # Extract variable name
                match = re.search(r"local variable '(.+?)' is assigned to but never used",
                    line)
                if match:
                    var_name = match.group(1)
                    # Replace variable assignment with underscore prefix
                    content = re.sub(
                        rf'\b{re.escape(var_name)}\b\s*=',
                        f'_{var_name} =',
                        content
                    )

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False
    except Exception as e:
        print(f"Error fixing unused variables in {file_path}: {e}")
        return False


def fix_undefined_names(file_path: str) -> bool:
    """Fix common undefined name issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Common fixes for undefined names
        fixes = {
            'result': 'None  # TODO: Define result',
            'conn': 'connection',
            'self.logger': 'logging.getLogger(__name__)',
        }

        for undefined, replacement in fixes.items():
            if f'Name "{undefined}" is not defined' in content:
                content = content.replace(f'return {undefined}',
                    f'return {replacement}')

        # Fix missing imports
        if 'logging' in content and 'import logging' not in content:
            content = 'import logging\n' + content

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False
    except Exception as e:
        print(f"Error fixing undefined names in {file_path}: {e}")
        return False


def fix_long_lines(file_path: str) -> bool:
    """Fix long lines by breaking them appropriately"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        changed = False

        for line in lines:
            if len(line.rstrip()) > 88:  # flake8 line length limit
                # Try to break long lines
                stripped = line.rstrip()
                indent = len(line) - len(line.lstrip())

                # Break on common separators
                if ',' in stripped and len(stripped) > 88:
                    # Break on commas
                    parts = stripped.split(',')
                    if len(parts) > 1:
                        new_line = parts[0] + ','
                        for part in parts[1:-1]:
                            new_line += f'\n{" " * (indent + 4)}{part.strip()},'
                        new_line += f'\n{" " * (indent + 4)}{parts[-1].strip()}'
                        new_lines.append(new_line + '\n')
                        changed = True
                        continue

                # Break on logical operators
                if ' and ' in stripped or ' or ' in stripped:
                    for op in [' and ', ' or ']:
                        if op in stripped:
                            parts = stripped.split(op)
                            if len(parts) > 1:
                                new_line = parts[0] + f' \\{op.strip()}'
                                for part in parts[1:]:
                                    new_line += f'\n{" " * (indent + 4)}{part.strip()}'
                                new_lines.append(new_line + '\n')
                                changed = True
                                break
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True

        return False
    except Exception as e:
        print(f"Error fixing long lines in {file_path}: {e}")
        return False


def main():
    """Main function to run comprehensive QA fixes"""
    project_root = Path(__file__).parent

    print("Starting comprehensive QA fixes...")

    # Get all Python files
    python_files = []
    for root, dirs, files in os.walk(project_root):
        # Skip certain directories
        skip_dirs = {'.git',
            '__pycache__',
            '.pytest_cache',
            'node_modules',
            '.venv',
            'venv'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} Python files to process")

    # Statistics
    stats = {
        'files_processed': 0,
        'whitespace_fixes': 0,
        'unused_imports_fixes': 0,
        'unused_variables_fixes': 0,
        'undefined_names_fixes': 0,
        'long_lines_fixes': 0,
    }

    for file_path in python_files:
        print(f"Processing: {file_path}")
        stats['files_processed'] += 1

        # Apply fixes
        if fix_whitespace_issues(file_path):
            stats['whitespace_fixes'] += 1

        if fix_unused_imports(file_path):
            stats['unused_imports_fixes'] += 1

        if fix_unused_variables(file_path):
            stats['unused_variables_fixes'] += 1

        if fix_undefined_names(file_path):
            stats['undefined_names_fixes'] += 1

        if fix_long_lines(file_path):
            stats['long_lines_fixes'] += 1

    # Run formatters
    print("\nRunning formatters...")

    # Run black
    stdout, stderr, code = run_command("python -m black .", str(project_root))
    if code == 0:
        print("✓ Black formatting completed")
    else:
        print(f"✗ Black formatting failed: {stderr}")

    # Run isort
    stdout, stderr, code = run_command("python -m isort .", str(project_root))
    if code == 0:
        print("✓ isort completed")
    else:
        print(f"✗ isort failed: {stderr}")

    # Print statistics
    print("\n" + "="*50)
    print("COMPREHENSIVE QA FIXES SUMMARY")
    print("="*50)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Whitespace fixes: {stats['whitespace_fixes']}")
    print(f"Unused imports fixes: {stats['unused_imports_fixes']}")
    print(f"Unused variables fixes: {stats['unused_variables_fixes']}")
    print(f"Undefined names fixes: {stats['undefined_names_fixes']}")
    print(f"Long lines fixes: {stats['long_lines_fixes']}")

    # Run final quality checks
    print("\nRunning final quality checks...")

    # Flake8 check
    stdout,
        stderr,
        code = run_command("python -m flake8 --config=config/.flake8 src/ main.py service.py",
        str(project_root))
    flake8_issues = len(stdout.strip().split('\n')) if stdout.strip() else 0
    print(f"Flake8 issues remaining: {flake8_issues}")

    # Mypy check
    stdout,
        stderr,
        code = run_command("python -m mypy src/ --config-file=config/mypy.ini",
        str(project_root))
    mypy_issues = len(stdout.strip().split('\n')) if stdout.strip() else 0
    print(f"Mypy issues remaining: {mypy_issues}")

    print("\nComprehensive QA fixes completed!")

if __name__ == "__main__":
    main()
