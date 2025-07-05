#!/usr/bin/env python3
"""
Better script to fix the variable name issues we created
"""
import re
from pathlib import Path


def fix_undefined_variables(content: str) -> str:
    """Fix undefined variables by removing underscore prefix"""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Find lines that reference undefined variables
        if "= _" in line and "=" in line:
            # Look for patterns where we reference the original variable name but assigned to _variable
            for var_name in ["data", "result", "config", "stats", "response"]:
                if f"_{var_name} =" in line:
                    # Find all subsequent lines that reference the original variable name
                    original_var_pattern = rf"\b{var_name}\b"
                    if re.search(original_var_pattern, line):
                        # Replace the assignment back to original name
                        line = line.replace(f"_{var_name} =", f"{var_name} =")

        fixed_lines.append(line)

    # Second pass: fix references to undefined variables
    content = "\n".join(fixed_lines)

    # Look for undefined variable references and fix them
    _undefined_patterns = [
        (r"\bdata\b(?!\s*=)", "_data"),
        (r"\bresult\b(?!\s*=)", "_result"),
        (r"\bconfig\b(?!\s*=)", "_config"),
        (r"\bstats\b(?!\s*=)", "_stats"),
        (r"\bresponse\b(?!\s*=)", "_response"),
    ]

    lines = content.split("\n")
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this line has an assignment to _variable
        assigned_vars = []
        for var_name in ["data", "result", "config", "stats", "response"]:
            if f"_{var_name} =" in line:
                assigned_vars.append(var_name)

        # If we found assignments, look ahead for undefined references
        if assigned_vars:
            # Check subsequent lines for undefined references
            j = i + 1
            while j < len(lines) and j < i + 10:  # Look ahead 10 lines
                next_line = lines[j]

                for var_name in assigned_vars:
                    # If the next line references the original variable name (not as assignment)
                    if re.search(rf"\b{var_name}\b(?!\s*=)", next_line):
                        # Replace the assignment line to use original name
                        line = line.replace(f"_{var_name} =", f"{var_name} =")
                        break

                j += 1

        fixed_lines.append(line)
        i += 1

    return "\n".join(fixed_lines)


def fix_file(file_path: Path) -> bool:
    """Fix a single Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        content = fix_undefined_variables(content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Main function"""
    src_dir = Path("src")

    if not src_dir.exists():
        print("src directory not found")
        return

    python_files = list(src_dir.glob("**/*.py"))

    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1

    print(f"Fixed {fixed_count} files out of {len(python_files)}")


if __name__ == "__main__":
    main()
