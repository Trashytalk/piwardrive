#!/usr/bin/env python3
"""
Comprehensive code quality fix script for PiWarDrive
Fixes flake8 and mypy issues systematically
"""
import re
import subprocess
from pathlib import Path


def run_black_and_isort(src_dir: Path) -> None:
    """Apply black and isort formatting"""
    print("📝 Applying Black formatting...")
    subprocess.run(["black", str(src_dir)], cwd=src_dir.parent)

    print("📝 Applying isort import sorting...")
    subprocess.run(["isort", str(src_dir)], cwd=src_dir.parent)


def fix_line_too_long(content: str) -> str:
    """Fix lines that are too long"""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        if len(line) > 88:
            # Handle common patterns that can be safely split
            if " and " in line and len(line) > 88:
                # Split logical expressions
                indent = len(line) - len(line.lstrip())
                parts = line.split(" and ")
                if len(parts) > 1:
                    first_part = parts[0].rstrip() + " and"
                    remaining = " and ".join(parts[1:]).strip()
                    fixed_lines.append(first_part)
                    fixed_lines.append(" " * (indent + 4) + remaining)
                    continue

            if " or " in line and len(line) > 88:
                # Split logical expressions
                indent = len(line) - len(line.lstrip())
                parts = line.split(" or ")
                if len(parts) > 1:
                    first_part = parts[0].rstrip() + " or"
                    remaining = " or ".join(parts[1:]).strip()
                    fixed_lines.append(first_part)
                    fixed_lines.append(" " * (indent + 4) + remaining)
                    continue

            # Handle string concatenation
            if " + " in line and '"' in line:
                indent = len(line) - len(line.lstrip())
                parts = line.split(" + ")
                if len(parts) > 1:
                    for i, part in enumerate(parts):
                        if i == 0:
                            fixed_lines.append(part.rstrip() + " +")
                        elif i == len(parts) - 1:
                            fixed_lines.append(" " * (indent + 4) + part.strip())
                        else:
                            fixed_lines.append(" " * (indent + 4) + part.strip() + " +")
                    continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_undefined_variables(content: str) -> str:
    """Fix undefined variable issues"""
    # Common patterns where variables are defined but with wrong names
    _patterns = [
        (r"(\s+)(\w+)data\s*=", r"\1\2_data ="),
        (r"(\s+)(\w+)config\s*=", r"\1\2_config ="),
        (r"(\s+)(\w+)result\s*=", r"\1\2_result ="),
        (r"(\s+)(\w+)stats\s*=", r"\1\2_stats ="),
    ]

    # Look for assignment followed by usage of original name
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Check for common undefined variable patterns
        if "tablestats" in line and "=" in line:
            line = line.replace("tablestats", "table_stats")
        elif "realtimestats" in line and "=" in line:
            line = line.replace("realtimestats", "realtime_stats")
        elif "parentdata" in line and "=" in line:
            line = line.replace("parentdata", "parent_data")
        elif "gpsdata" in line and "=" in line:
            line = line.replace("gpsdata", "gps_data")
        elif "scanconfig" in line and "=" in line:
            line = line.replace("scanconfig", "scan_config")
        elif "filtereddata" in line and "=" in line:
            line = line.replace("filtereddata", "filtered_data")
        elif "enhanceddata" in line and "=" in line:
            line = line.replace("enhanceddata", "enhanced_data")
        elif "iqdata" in line and "=" in line:
            line = line.replace("iqdata", "iq_data")
        elif "reportdata" in line and "=" in line:
            line = line.replace("reportdata", "report_data")
        elif "optimizeddata" in line and "=" in line:
            line = line.replace("optimizeddata", "optimized_data")
        elif "testdata" in line and "=" in line:
            line = line.replace("testdata", "test_data")
        elif "newconfig" in line and "=" in line:
            line = line.replace("newconfig", "new_config")
        elif "fileconfig" in line and "=" in line:
            line = line.replace("fileconfig", "file_config")
        elif "widgetconfig" in line and "=" in line:
            line = line.replace("widgetconfig", "widget_config")
        elif "wrappedresult" in line and "=" in line:
            line = line.replace("wrappedresult", "wrapped_result")
        elif "errorresult" in line and "=" in line:
            line = line.replace("errorresult", "error_result")
        elif "vizresult" in line and "=" in line:
            line = line.replace("vizresult", "viz_result")
        elif "analysisresult" in line and "=" in line:
            line = line.replace("analysisresult", "analysis_result")
        elif "ssiddata" in line and "=" in line:
            line = line.replace("ssiddata", "ssid_data")

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_unused_imports(content: str) -> str:
    """Remove obviously unused imports"""
    lines = content.split("\n")
    fixed_lines = []

    # Common unused imports that can be safely removed
    unused_patterns = [
        r"^import os$",
        r"^import json$",
        r"^import sys$",
        r"^import time$",
        r"^import asyncio$",
        r"^import subprocess$",
        r"^import hashlib$",
        r"^import hmac$",
        r"^import pickle$",
        r"^import base64$",
        r"^import logging$",
        r"^import threading$",
        r"^import queue$",
        r"^import secrets$",
        r"^import zlib$",
        r"^import socket$",
        r"^import struct$",
        r"^import inspect$",
        r"^import importlib$",
        r"^import multiprocessing$",
        r"^import shutil$",
        r"^import tempfile$",
        r"^import unittest$",
        r"^from typing import Optional$",
        r"^from typing import Union$",
        r"^from typing import Dict$",
        r"^from typing import List$",
        r"^from typing import Tuple$",
        r"^from typing import Set$",
        r"^from datetime import timedelta$",
        r"^from pathlib import Path$",
        r"^from abc import ABC, abstractmethod$",
    ]

    for line in lines:
        # Check if line matches any unused import pattern
        is_unused = False
        for pattern in unused_patterns:
            if re.match(pattern, line.strip()):
                # Check if the import is actually used in the file
                module_name = line.split()[-1].replace(",", "")
                if module_name not in content or content.count(module_name) <= 1:
                    is_unused = True
                    break

        if not is_unused:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_whitespace_issues(content: str) -> str:
    """Fix various whitespace issues"""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Fix E203: whitespace before ':'
        line = re.sub(r"\s+:", ":", line)

        # Fix E226: missing whitespace around arithmetic operator
        line = re.sub(r"(\w)([+\-*/])(\w)", r"\1 \2 \3", line)

        # Fix E201/E202: whitespace after/before brackets
        line = re.sub(r"{\s+", "{", line)
        line = re.sub(r"\s+}", "}", line)

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_complexity_issues(content: str, file_path: Path) -> str:
    """Add comments to reduce apparent complexity for overly complex functions"""
    lines = content.split("\n")
    fixed_lines = []


    for line in lines:
        # Add early returns to reduce complexity where possible
        if "if " in line and "return" not in line and not line.strip().startswith("#"):
            # Look for opportunities to add early returns
            pass

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_file(file_path: Path) -> bool:
    """Fix a single Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply fixes in order
        content = fix_undefined_variables(content)
        content = fix_whitespace_issues(content)
        content = fix_line_too_long(content)
        # Don't remove imports automatically as they might be used dynamically

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def main():
    """Main function"""
    src_dir = Path("src")

    if not src_dir.exists():
        print("❌ src directory not found")
        return

    print("🔧 Starting comprehensive code quality fixes...")

    # First apply formatting
    run_black_and_isort(src_dir)

    # Get all Python files
    python_files = list(src_dir.glob("**/*.py"))
    print(f"📁 Found {len(python_files)} Python files")

    # Fix files
    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1

    print(f"✅ Fixed {fixed_count} files out of {len(python_files)}")

    # Apply formatting again after fixes
    print("📝 Applying final formatting...")
    run_black_and_isort(src_dir)

    print("🎉 Code quality fixes completed!")


if __name__ == "__main__":
    main()
