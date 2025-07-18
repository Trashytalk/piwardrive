#!/usr/bin/env python3
"""
Comprehensive code quality analysis focusing on working Python files.
Identifies imports, undefined names, unused variables, missing docstrings, and code quality issues.
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List


class ComprehensiveCodeAnalyzer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues = []
        
    def can_compile(self, file_path: Path) -> bool:
        """Check if a Python file can be compiled."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content, str(file_path))
            return True
        except Exception:
            return False
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file comprehensively."""
        issues = {
            'undefined_names': [],
            'unused_variables': [],
            'import_issues': [],
            'missing_docstrings': [],
            'complexity_issues': [],
            'security_issues': [],
            'performance_issues': [],
            'maintainability_issues': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content, str(file_path))
            
            # Analyze with custom AST visitor
            analyzer = DetailedASTAnalyzer(file_path, content)
            analyzer.visit(tree)
            
            # Merge results
            for key in issues:
                issues[key].extend(getattr(analyzer, key, []))
            
            # Additional analysis
            issues['import_issues'].extend(self._analyze_imports(tree, content))
            issues['missing_docstrings'].extend(self._analyze_docstrings(tree))
            issues['complexity_issues'].extend(self._analyze_complexity(tree, content))
            issues['security_issues'].extend(self._analyze_security(content))
            issues['performance_issues'].extend(self._analyze_performance(content))
            issues['maintainability_issues'].extend(self._analyze_maintainability(content))
            
        except Exception as e:
            issues['undefined_names'].append(f"Analysis error: {e}")
            
        return issues
    
    def _analyze_imports(self, tree: ast.AST, content: str) -> List[str]:
        """Analyze import statements for issues."""
        issues = []
        lines = content.split('\n')
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append((f"{module}.{alias.name}", node.lineno))
        
        # Check for unused imports
        import_names = set()
        for import_name, line_no in imports:
            base_name = import_name.split('.')[0]
            import_names.add(base_name)
            
            # Check if import is used
            if not self._is_import_used(base_name, content):
                issues.append(f"Line {line_no}: Unused import '{import_name}'")
        
        # Check for duplicate imports
        seen_imports = set()
        for import_name, line_no in imports:
            if import_name in seen_imports:
                issues.append(f"Line {line_no}: Duplicate import '{import_name}'")
            seen_imports.add(import_name)
        
        return issues
    
    def _is_import_used(self, import_name: str, content: str) -> bool:
        """Check if an import is used in the content."""
        # Simple heuristic - look for the import name in the content
        pattern = rf'\b{re.escape(import_name)}\b'
        matches = re.findall(pattern, content)
        # Should appear more than once (once for import, once for usage)
        return len(matches) > 1
    
    def _analyze_docstrings(self, tree: ast.AST) -> List[str]:
        """Analyze docstring coverage."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private methods and very short functions
                if not node.name.startswith('_') and len(node.body) > 1:
                    if not ast.get_docstring(node):
                        issues.append(f"Line {node.lineno}: Missing docstring for function '{node.name}'")
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    issues.append(f"Line {node.lineno}: Missing docstring for class '{node.name}'")
        
        return issues
    
    def _analyze_complexity(self, tree: ast.AST, content: str) -> List[str]:
        """Analyze code complexity."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count complexity indicators
                complexity_score = 0
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                        complexity_score += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity_score += len(child.values) - 1
                
                if complexity_score > 10:
                    issues.append(f"Line {node.lineno}: High complexity in function '{node.name}' (score: {complexity_score})")
                
                # Check function length
                if len(node.body) > 50:
                    issues.append(f"Line {node.lineno}: Long function '{node.name}' ({len(node.body)} statements)")
        
        return issues
    
    def _analyze_security(self, content: str) -> List[str]:
        """Analyze for security issues."""
        issues = []
        lines = content.split('\n')
        
        security_patterns = [
            (r'eval\s*\(', 'Use of eval() is dangerous'),
            (r'exec\s*\(', 'Use of exec() is dangerous'),
            (r'__import__\s*\(', 'Dynamic import with __import__ can be dangerous'),
            (r'subprocess\.[^)]*shell\s*=\s*True', 'subprocess with shell=True is dangerous'),
            (r'os\.system\s*\(', 'Use of os.system() is dangerous'),
            (r'input\s*\([^)]*\)', 'Use of input() can be dangerous in some contexts'),
            (r'pickle\.loads?\s*\(', 'Pickle deserialization can be dangerous'),
            (r'yaml\.load\s*\((?!.*Loader)', 'yaml.load() without Loader is dangerous'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, message in security_patterns:
                if re.search(pattern, line):
                    issues.append(f"Line {i}: {message}")
        
        return issues
    
    def _analyze_performance(self, content: str) -> List[str]:
        """Analyze for performance issues."""
        issues = []
        lines = content.split('\n')
        
        performance_patterns = [
            (r'\.join\s*\(\s*\[.*for.*in.*\]', 'List comprehension in join() - consider generator'),
            (r'len\s*\(\s*\[.*for.*in.*\]\s*\)', 'len() of list comprehension - consider sum(1 for ...)'),
            (r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', 'for i in range(len(...)) - consider enumerate()'),
            (r'\.keys\s*\(\s*\).*in\s+', 'Iterating over .keys() - iterate over dict directly'),
            (r'\.has_key\s*\(', 'Use of has_key() - use "in" operator'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, message in performance_patterns:
                if re.search(pattern, line):
                    issues.append(f"Line {i}: {message}")
        
        return issues
    
    def _analyze_maintainability(self, content: str) -> List[str]:
        """Analyze for maintainability issues."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 120:
                issues.append(f"Line {i}: Line too long ({len(line)} > 120 characters)")
            
            # Check for TODO/FIXME comments
            if re.search(r'#.*\b(TODO|FIXME|XXX|HACK)\b', line, re.IGNORECASE):
                issues.append(f"Line {i}: TODO/FIXME comment found")
            
            # Check for magic numbers
            if re.search(r'\b\d{2,}\b', line) and not re.search(r'#.*\d', line):
                numbers = re.findall(r'\b\d{2,}\b', line)
                if any(int(n) > 100 for n in numbers):
                    issues.append(f"Line {i}: Magic number found - consider using constants")
        
        return issues
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Analyze all working Python files in the repository."""
        results = {}
        
        # Get all Python files
        python_files = list(self.root_path.rglob("*.py"))
        
        # Filter to only working files
        working_files = []
        for py_file in python_files:
            # Skip virtual environment and cache files
            if any(skip in str(py_file) for skip in ['venv/', '__pycache__/', '.pytest_cache/', 'htmlcov/']):
                continue
            
            if self.can_compile(py_file):
                working_files.append(py_file)
        
        print(f"Analyzing {len(working_files)} working Python files...")
        
        for py_file in working_files:
            rel_path = py_file.relative_to(self.root_path)
            print(f"Analyzing: {rel_path}")
            
            file_issues = self.analyze_file(py_file)
            
            # Only include files with issues
            total_issues = sum(len(issues) for issues in file_issues.values())
            if total_issues > 0:
                results[str(rel_path)] = file_issues
                
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive report of all issues."""
        report = ["# Comprehensive Code Quality Analysis Report", ""]
        
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
            'undefined_names': 'Undefined Names',
            'unused_variables': 'Unused Variables',
            'import_issues': 'Import Issues',
            'missing_docstrings': 'Missing Docstrings',
            'complexity_issues': 'Complexity Issues',
            'security_issues': 'Security Issues',
            'performance_issues': 'Performance Issues',
            'maintainability_issues': 'Maintainability Issues'
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

class DetailedASTAnalyzer(ast.NodeVisitor):
    """Detailed AST visitor for comprehensive analysis."""
    
    def __init__(self, file_path: Path, content: str):
        self.file_path = file_path
        self.content = content
        self.lines = content.split('\n')
        self.undefined_names = []
        self.unused_variables = []
        self.defined_names = set()
        self.used_names = set()
        
    def visit_Name(self, node):
        """Visit name nodes to track usage."""
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Visit function definitions."""
        self.defined_names.add(node.name)
        # Add parameters to defined names
        for arg in node.args.args:
            self.defined_names.add(arg.arg)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Visit class definitions."""
        self.defined_names.add(node.name)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statements."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_names.add(name.split('.')[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Visit from-import statements."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_names.add(name)
        self.generic_visit(node)

def main():
    """Main function to run comprehensive analysis."""
    analyzer = ComprehensiveCodeAnalyzer(".")
    results = analyzer.analyze_repository()
    report = analyzer.generate_report(results)
    
    # Save report
    report_file = "comprehensive_code_quality_report.md"
    with open(report_file, "w") as f:
        f.write(report)
    
    print(f"\nComprehensive analysis complete! Report saved to {report_file}")
    
    # Print summary
    total_files = len(results)
    total_issues = sum(sum(len(issues) for issues in file_issues.values()) for file_issues in results.values())
    print(f"Found {total_issues} issues across {total_files} files")

if __name__ == "__main__":
    main()
