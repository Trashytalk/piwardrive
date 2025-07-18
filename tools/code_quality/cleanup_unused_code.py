#!/usr/bin/env python3
"""
Comprehensive unused code cleanup script for PiWarDrive.
Identifies and removes unused imports, variables, and files that are not tagged for future development.
"""

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


class UnusedCodeAnalyzer:
    """Analyzes and removes unused code from the repository."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.stats = {
            'files_analyzed': 0,
            'unused_imports_removed': 0,
            'unused_variables_removed': 0,
            'empty_files_removed': 0,
            'stub_files_identified': 0
        }
        
        # Files tagged for future development (should be preserved)
        self.protected_patterns = {
            'TODO', 'FIXME', 'STUB', 'Stub', 'stub',
            'Implement', 'implement', 'placeholder', 'PLACEHOLDER'
        }
        
        # Common unused import patterns that can be safely removed
        self.safe_unused_imports = {
            'typing.Optional', 'typing.Union', 'typing.Dict', 'typing.List',
            'typing.Tuple', 'typing.Set', 'typing.Any', 'typing.Callable',
            'typing.Iterator', 'typing.Iterable', 'typing.Sequence',
            '__future__.annotations', 'abc.ABC', 'abc.abstractmethod',
            'dataclasses.dataclass', 'dataclasses.field', 'dataclasses.asdict',
            'enum.Enum', 'pathlib.Path'
        }

    def is_protected_file(self, file_path: Path) -> bool:
        """Check if a file is protected (contains future development markers)."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return any(pattern in content for pattern in self.protected_patterns)
        except Exception:
            return True  # Err on the side of caution
    
    def get_flake8_issues(self, file_path: Path) -> List[Tuple[int, str, str]]:
        """Get flake8 F401 and F841 issues for a file."""
        try:
            result = subprocess.run(
                ['python', '-m', 'flake8', '--select=F401,F841', str(file_path)],
                capture_output=True, text=True, timeout=30
            )
            
            issues = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    # Parse: filename:line:col: code message
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        line_num = int(parts[1])
                        code = parts[3].strip().split()[0]
                        message = parts[3].strip()
                        issues.append((line_num, code, message))
            
            return issues
        except Exception:
            return []
    
    def remove_unused_imports(self, file_path: Path) -> bool:
        """Remove unused imports from a file."""
        if self.is_protected_file(file_path):
            return False
            
        try:
            issues = self.get_flake8_issues(file_path)
            f401_issues = [issue for issue in issues if issue[1] == 'F401']
            
            if not f401_issues:
                return False
            
            lines = file_path.read_text(encoding='utf-8').splitlines()
            lines_to_remove = set()
            
            for line_num, _, message in f401_issues:
                # Extract import name from message
                if 'imported but unused' in message:
                    match = re.search(r"'(.+?)' imported but unused", message)
                    if match:
                        import_name = match.group(1)
                        # Only remove if it's in our safe list or clearly unused
                        if (import_name in self.safe_unused_imports or
                            self._is_safe_to_remove_import(lines[line_num - 1], import_name)):
                            lines_to_remove.add(line_num - 1)  # Convert to 0-based
            
            if lines_to_remove:
                new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
                file_path.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
                self.stats['unused_imports_removed'] += len(lines_to_remove)
                return True
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return False
    
    def _is_safe_to_remove_import(self, import_line: str, import_name: str) -> bool:
        """Check if an import is safe to remove."""
        # Don't remove if it's part of a complex import
        if ',' in import_line and import_name not in import_line:
            return False
        
        # Don't remove if it's an __all__ export
        if '__all__' in import_line:
            return False
            
        # Safe patterns
        safe_patterns = [
            r'^from typing import',
            r'^from __future__ import',
            r'^from abc import',
            r'^from dataclasses import',
            r'^from enum import',
            r'^from pathlib import',
            r'^import os$',
            r'^import sys$',
            r'^import json$',
            r'^import logging$'
        ]
        
        return any(re.match(pattern, import_line.strip()) for pattern in safe_patterns)
    
    def remove_unused_variables(self, file_path: Path) -> bool:
        """Remove unused variables from a file."""
        if self.is_protected_file(file_path):
            return False
            
        try:
            issues = self.get_flake8_issues(file_path)
            f841_issues = [issue for issue in issues if issue[1] == 'F841']
            
            if not f841_issues:
                return False
            
            lines = file_path.read_text(encoding='utf-8').splitlines()
            modified = False
            
            for line_num, _, message in f841_issues:
                line_idx = line_num - 1
                line = lines[line_idx]
                
                # Only remove simple unused variables, not complex ones
                if self._is_safe_unused_variable(line, message):
                    # Comment out the line instead of removing it
                    lines[line_idx] = f"    # Unused: {line.strip()}"
                    modified = True
                    self.stats['unused_variables_removed'] += 1
            
            if modified:
                file_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
                return True
                
        except Exception as e:
            print(f"Error processing variables in {file_path}: {e}")
        
        return False
    
    def _is_safe_unused_variable(self, line: str, message: str) -> bool:
        """Check if an unused variable is safe to remove."""
        # Extract variable name
        match = re.search(r"'(.+?)' is assigned to but never used", message)
        if not match:
            return False
        
        var_name = match.group(1)
        
        # Don't remove important variables
        if var_name in ('result', 'data', 'response', 'config', 'settings'):
            return False
        
        # Don't remove exception variables
        if var_name in ('e', 'ex', 'err', 'error', 'exception'):
            return False
        
        # Only remove variables with obvious unused patterns
        safe_patterns = [
            r'^\s*_\w+\s*=',  # Variables starting with underscore
            r'^\s*\w+\s*=\s*\[\]',  # Empty list assignments
            r'^\s*\w+\s*=\s*\{\}',  # Empty dict assignments
            r'^\s*\w+\s*=\s*None',  # None assignments
        ]
        
        return any(re.match(pattern, line) for pattern in safe_patterns)
    
    def identify_empty_or_stub_files(self) -> List[Path]:
        """Identify files that are mostly empty or just stubs."""
        empty_files = []
        
        for py_file in self.repo_path.rglob('*.py'):
            if not py_file.is_file():
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                lines = [line.strip() for line in content.splitlines() if line.strip()]
                
                # Remove comments and docstrings
                non_comment_lines = []
                for line in lines:
                    if not line.startswith('#') and not line.startswith('"""') and not line.startswith("'''"):
                        non_comment_lines.append(line)
                
                # File is effectively empty
                if len(non_comment_lines) <= 3:
                    # Check if it's just imports and pass statements
                    code_lines = [line for line in non_comment_lines 
                                if not line.startswith('import ') and not line.startswith('from ') 
                                and line != 'pass']
                    
                    if len(code_lines) == 0:
                        empty_files.append(py_file)
                        self.stats['empty_files_removed'] += 1
                        
            except Exception:
                continue
        
        return empty_files
    
    def analyze_file(self, file_path: Path) -> Dict[str, int]:
        """Analyze a single Python file for unused code."""
        file_stats = {'imports_removed': 0, 'variables_removed': 0}
        
        if not file_path.suffix == '.py':
            return file_stats
        
        self.stats['files_analyzed'] += 1
        
        # Remove unused imports
        if self.remove_unused_imports(file_path):
            file_stats['imports_removed'] = 1
        
        # Remove unused variables
        if self.remove_unused_variables(file_path):
            file_stats['variables_removed'] = 1
        
        return file_stats
    
    def clean_repository(self) -> None:
        """Clean unused code from the entire repository."""
        print("🧹 Starting comprehensive unused code cleanup...")
        
        # Analyze Python files
        python_files = list(self.repo_path.rglob('*.py'))
        print(f"📁 Found {len(python_files)} Python files to analyze")
        
        for py_file in python_files:
            if py_file.is_file():
                try:
                    self.analyze_file(py_file)
                except Exception as e:
                    print(f"❌ Error analyzing {py_file}: {e}")
        
        # Identify stub files
        empty_files = self.identify_empty_or_stub_files()
        if empty_files:
            print(f"\n📋 Found {len(empty_files)} empty/stub files:")
            for empty_file in empty_files:
                if self.is_protected_file(empty_file):
                    print(f"  🔒 PROTECTED: {empty_file.relative_to(self.repo_path)}")
                    self.stats['stub_files_identified'] += 1
                else:
                    print(f"  📄 EMPTY: {empty_file.relative_to(self.repo_path)}")
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print cleanup summary."""
        print("\n" + "="*60)
        print("🎯 UNUSED CODE CLEANUP SUMMARY")
        print("="*60)
        print(f"📊 Files analyzed: {self.stats['files_analyzed']}")
        print(f"🗑️  Unused imports removed: {self.stats['unused_imports_removed']}")
        print(f"📝 Unused variables commented: {self.stats['unused_variables_removed']}")
        print(f"📁 Empty files identified: {self.stats['empty_files_removed']}")
        print(f"🔒 Stub files protected: {self.stats['stub_files_identified']}")
        print("="*60)
        
        if self.stats['unused_imports_removed'] + self.stats['unused_variables_removed'] > 0:
            print("✅ Repository cleaned successfully!")
            print("💡 Run tests to ensure functionality is preserved.")
        else:
            print("ℹ️  No unused code found to remove.")


def main():
    """Main entry point."""
    repo_path = Path(__file__).parent
    
    analyzer = UnusedCodeAnalyzer(repo_path)
    analyzer.clean_repository()


if __name__ == '__main__':
    main()
