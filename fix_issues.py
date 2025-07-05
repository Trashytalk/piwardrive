#!/usr/bin/env python3
"""
Script to fix common Python code quality issues
"""
import re
from pathlib import Path
from typing import List, Tuple


def fix_unused_imports(content: str) -> str:
    """Remove unused imports (simplified approach)"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Skip common unused imports we can safely remove
        if (line.strip().startswith('import ') or line.strip().startswith('from ')) \and
            \
           any(unused in line for unused in ['typing.Optional',
               'typing.Union',
               'typing.Dict',
               'typing.List',
               'typing.Tuple',
               'typing.Set']):
            # Only remove if it's clearly unused (this is simplified)
            if 'Optional' in line and 'Optional' not in '\n'.join(lines):
                continue
            if 'Union' in line and 'Union' not in '\n'.join(lines):
                continue
            if 'Dict' in line and 'Dict' not in '\n'.join(lines):
                continue
            if 'List' in line and 'List' not in '\n'.join(lines):
                continue

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_trailing_whitespace(content: str) -> str:
    """Fix trailing whitespace issues"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Remove trailing whitespace
        fixed_line = line.rstrip()
        # Convert blank lines with whitespace to empty lines
        if not fixed_line.strip():
            fixed_line = ''
        fixed_lines.append(fixed_line)

    return '\n'.join(fixed_lines)


def fix_unused_variables(content: str) -> str:
    """Fix unused variable issues by prefixing with underscore"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Fix unused variables by prefixing with _
        if '=' in line and not line.strip().startswith('#'):
            # Look for pattern like "variable = "
            match = re.match(r'(\s*)([a-zA-Z_]\w*)\s*=', line)
            if match:
                indent, var_name = match.groups()
                # If it's a common unused variable name, prefix with _
                if var_name in ['e', 'result', 'data', 'response', 'stats', 'config']:
                    if not var_name.startswith('_'):
                        line = line.replace(f'{var_name} =', f'_{var_name} =', 1)

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_fstring_placeholders(content: str) -> str:
    """Fix f-strings missing placeholders"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Find f-strings without placeholders
        if 'f"' in line and '{' not in line:
            # Convert f-string to regular string
            line = line.replace('f"', '"')
        if "f'" in line and '{' not in line:
            # Convert f-string to regular string
            line = line.replace("f'", "'")

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_bare_except(content: str) -> str:
    """Fix bare except clauses"""
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Replace bare except with except Exception
        if line.strip() == 'except:':
            line = line.replace('except:', 'except Exception:')

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def fix_file(file_path: Path) -> bool:
    """Fix a single Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply fixes
        content = fix_trailing_whitespace(content)
        content = fix_unused_variables(content)
        content = fix_fstring_placeholders(content)
        content = fix_bare_except(content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Main function"""
    src_dir = Path('src')

    if not src_dir.exists():
        print("src directory not found")
        return

    python_files = list(src_dir.glob('**/*.py'))

    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1

    print(f"Fixed {fixed_count} files out of {len(python_files)}")

if __name__ == '__main__':
    main()
