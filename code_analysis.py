#!/usr/bin/env python3
"""
Comprehensive code analysis for PiWardrive repository.
Identifies imports, errors, docstrings, formatting, variables, and other issues.
"""

import ast
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class CodeAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues = []
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file for issues."""
        issues = {
            'syntax_errors': [],
            'undefined_names': [],
            'unused_variables': [],
            'import_issues': [],
            'missing_docstrings': [],
            'formatting_issues': [],
            'other_issues': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check syntax first
            try:
                tree = ast.parse(content, str(file_path))
            except SyntaxError as e:
                issues['syntax_errors'].append(f"Line {e.lineno}: {e.msg}")
                return issues
                
            # Run flake8 for comprehensive analysis
            issues.update(self._run_flake8(file_path))
            
            # Check for undefined names and unused variables
            issues['undefined_names'].extend(self._find_undefined_names(content, file_path))
            issues['unused_variables'].extend(self._find_unused_variables(content))
            issues['import_issues'].extend(self._check_imports(tree))
            issues['missing_docstrings'].extend(self._check_docstrings(tree))
            issues['formatting_issues'].extend(self._check_formatting(content))
            
        except Exception as e:
            issues['other_issues'].append(f"Analysis error: {e}")
            
        return issues
    
    def _run_flake8(self, file_path: Path) -> Dict[str, List[str]]:
        """Run flake8 on a file and parse the output."""
        issues = {
            'syntax_errors': [],
            'undefined_names': [],
            'unused_variables': [],
            'import_issues': [],
            'formatting_issues': [],
            'other_issues': []
        }
        
        try:
            result = subprocess.run(
                ['flake8', '--select=E,W,F', str(file_path)],
                capture_output=True,
                text=True,
                cwd=self.root_path
            )
            
            if result.returncode == 0:
                return issues
                
            # Parse flake8 output
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                # Format: filename:line:col: error_code message
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    line_num = parts[1]
                    error_code = parts[3].strip().split()[0]
                    message = parts[3].strip()
                    
                    if error_code.startswith('F'):
                        if 'undefined name' in message:
                            issues['undefined_names'].append(f"Line {line_num}: {message}")
                        elif 'imported but unused' in message:
                            issues['unused_variables'].append(f"Line {line_num}: {message}")
                        elif 'import' in message:
                            issues['import_issues'].append(f"Line {line_num}: {message}")
                        else:
                            issues['other_issues'].append(f"Line {line_num}: {message}")
                    elif error_code.startswith(('E', 'W')):
                        issues['formatting_issues'].append(f"Line {line_num}: {message}")
                        
        except FileNotFoundError:
            issues['other_issues'].append("flake8 not found - install with: pip install flake8")
        except Exception as e:
            issues['other_issues'].append(f"flake8 error: {e}")
            
        return issues
    
    def _find_undefined_names(self, content: str, file_path: Path) -> List[str]:
        """Find potential undefined names using regex patterns."""
        issues = []
        lines = content.split('\n')
        
        # Look for common undefined name patterns
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#') or not line.strip():
                continue
                
            # Look for variables that might be undefined
            if 'Config(**data)' in line and 'data' not in content[:content.find(line)]:
                issues.append(f"Line {i}: 'data' might be undefined")
            if 'uvicorn.Server(config)' in line and 'config' not in content[:content.find(line)]:
                issues.append(f"Line {i}: 'config' might be undefined")
                
        return issues
    
    def _find_unused_variables(self, content: str) -> List[str]:
        """Find unused variables."""
        issues = []
        lines = content.split('\n')
        
        # Simple heuristic for unused variables
        for i, line in enumerate(lines, 1):
            if re.match(r'\s*(\w+)\s*=.*# unused', line):
                var_match = re.search(r'(\w+)\s*=', line)
                if var_match:
                    issues.append(f"Line {i}: Variable '{var_match.group(1)}' marked as unused")
                    
        return issues
    
    def _check_imports(self, tree: ast.AST) -> List[str]:
        """Check for import issues."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('.'):
                        issues.append(f"Line {node.lineno}: Invalid import syntax")
            elif isinstance(node, ast.ImportFrom):
                if node.level > 0 and not node.module:
                    issues.append(f"Line {node.lineno}: Relative import without module")
                    
        return issues
    
    def _check_docstrings(self, tree: ast.AST) -> List[str]:
        """Check for missing docstrings."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    issues.append(f"Line {node.lineno}: Missing docstring for {node.__class__.__name__.lower()} '{node.name}'")
                    
        return issues
    
    def _check_formatting(self, content: str) -> List[str]:
        """Check for formatting issues."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Trailing whitespace
            if line.rstrip() != line:
                issues.append(f"Line {i}: Trailing whitespace")
            
            # Line too long (over 120 chars)
            if len(line) > 120:
                issues.append(f"Line {i}: Line too long ({len(line)} > 120 characters)")
                
        return issues
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Analyze all Python files in the repository."""
        results = {}
        
        # Focus on source files, not virtual environment
        python_files = []
        for pattern in ['src/**/*.py', 'tests/**/*.py', 'scripts/**/*.py', '*.py']:
            python_files.extend(self.root_path.glob(pattern))
        
        # Remove duplicates and filter out venv/virtual environment files
        python_files = list(set(python_files))
        python_files = [f for f in python_files if 'venv' not in str(f) and '.venv' not in str(f)]
        
        print(f"Analyzing {len(python_files)} Python files...")
        
        for py_file in python_files:
            rel_path = py_file.relative_to(self.root_path)
            print(f"Analyzing: {rel_path}")
            
            file_issues = self.analyze_file(py_file)
            
            # Only include files with issues
            total_issues = sum(len(issues) for issues in file_issues.values())
            if total_issues > 0:
                results[str(rel_path)] = file_issues
                
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a formatted report of all issues."""
        report = ["# Code Analysis Report for PiWardrive", ""]
        
        total_files_with_issues = len(results)
        total_issues = sum(
            sum(len(issues) for issues in file_issues.values())
            for file_issues in results.values()
        )
        
        report.extend([
            f"## Summary",
            f"- Files with issues: {total_files_with_issues}",
            f"- Total issues found: {total_issues}",
            ""
        ])
        
        # Group by issue type
        issue_types = {
            'syntax_errors': 'Syntax Errors',
            'undefined_names': 'Undefined Names',
            'unused_variables': 'Unused Variables/Imports', 
            'import_issues': 'Import Issues',
            'missing_docstrings': 'Missing Docstrings',
            'formatting_issues': 'Formatting Issues',
            'other_issues': 'Other Issues'
        }
        
        for issue_type, title in issue_types.items():
            report.append(f"## {title}")
            report.append("")
            
            found_issues = False
            for file_path, file_issues in results.items():
                if file_issues[issue_type]:
                    found_issues = True
                    report.append(f"### {file_path}")
                    for issue in file_issues[issue_type]:
                        report.append(f"- {issue}")
                    report.append("")
                    
            if not found_issues:
                report.append("No issues found.")
                report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run the code analysis."""
    analyzer = CodeAnalyzer(".")
    results = analyzer.analyze_repository()
    report = analyzer.generate_report(results)
    
    # Save report
    with open("code_analysis_report.md", "w") as f:
        f.write(report)
    
    print("\nAnalysis complete! Report saved to code_analysis_report.md")
    
    # Print summary
    total_files = len(results)
    total_issues = sum(sum(len(issues) for issues in file_issues.values()) for file_issues in results.values())
    print(f"Found {total_issues} issues across {total_files} files")

if __name__ == "__main__":
    main()
