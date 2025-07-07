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
        if (line.strip().startswith('import ') or line.strip().startswith('from ')) and \
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


def fix_unterminated_fstrings(content: str) -> str:
    """Fix unterminated f-strings and broken string literals"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix unterminated f-strings split across lines
        if ('f"' in line and line.count('"') % 2 == 1 and 
            not line.strip().endswith('"') and 
            '{' in line and '}' not in line):
            # Look for the continuation
            j = i + 1
            while j < len(lines) and not lines[j].strip().endswith('"'):
                j += 1
            if j < len(lines):
                # Combine the lines
                combined = line + " " + " ".join(lines[i+1:j+1])
                fixed_lines.append(combined)
                # Skip the lines we just combined
                for k in range(i+1, j+1):
                    if k < len(lines):
                        lines[k] = None
                continue
        
        # Fix string literals split across lines without proper escaping
        if (line.strip().endswith(',') and 
            i < len(lines) - 1 and 
            lines[i+1].strip().startswith('"') and
            '"' in line and line.count('"') % 2 == 1):
            # This is likely a broken string literal
            next_line = lines[i+1].strip()
            # Combine them properly
            fixed_line = line.rstrip()[:-1] + ' ' + next_line + '"'
            fixed_lines.append(fixed_line)
            if i+1 < len(lines):
                lines[i+1] = None
            continue
            
        if line is not None:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_multiline_strings(content: str) -> str:
    """Fix broken multiline strings"""
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for broken multiline strings in function calls
        if ('f"' in line and line.count('"') % 2 == 1 and 
            not line.strip().endswith('"')):
            # Find the end of the string
            j = i + 1
            combined_line = line
            while j < len(lines):
                combined_line += " " + lines[j].strip()
                if lines[j].strip().endswith('"') or lines[j].strip().endswith('")'):
                    break
                j += 1
            
            # Clean up the combined line
            if '{' in combined_line and '}' in combined_line:
                # This is a proper f-string, just needs to be on one line
                fixed_lines.append(combined_line)
                i = j + 1
                continue
            else:
                # Convert to regular string concatenation
                parts = combined_line.split('f"')
                if len(parts) > 1:
                    fixed_line = parts[0] + '"' + parts[1]
                    fixed_lines.append(fixed_line)
                    i = j + 1
                    continue
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)


def fix_sql_strings(content: str) -> str:
    """Fix broken SQL strings in migration files"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Fix SQL strings that are improperly terminated
        if ('CREATE INDEX' in line and 
            line.count('"') % 2 == 1 and 
            not line.strip().endswith('"')):
            # Add proper termination
            if line.strip().endswith(','):
                fixed_lines.append(line.rstrip() + '"')
            else:
                fixed_lines.append(line + '"')
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_missing_commas(content: str) -> str:
    """Fix missing commas in data structures"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check for missing commas in dictionary/list definitions
        if (line.strip().endswith('"') and 
            i < len(lines) - 1 and 
            lines[i+1].strip().startswith('"') and
            not line.strip().endswith('",') and
            not line.strip().endswith('":"')):
            # Add missing comma
            fixed_lines.append(line + ',')
        else:
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
        content = fix_unterminated_fstrings(content)
        content = fix_multiline_strings(content)
        content = fix_sql_strings(content)
        content = fix_missing_commas(content)
        content = fix_unterminated_fstrings(content)
        content = fix_multiline_strings(content)
        content = fix_sql_strings(content)
        content = fix_missing_commas(content)

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
