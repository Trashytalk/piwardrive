#!/usr/bin/env python3
"""
API Compatibility Checker

This script checks for breaking changes in the API by comparing
the current API with the baseline from the main branch.
"""

import ast
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set


@dataclass
class APIEndpoint:
    """Represents an API endpoint."""
    path: str
    method: str
    parameters: List[str]
    return_type: str
    description: str = ""

@dataclass
class APIFunction:
    """Represents an API function."""
    name: str
    parameters: List[str]
    return_type: str
    module: str
    description: str = ""


class APICompatibilityChecker:
    """Checks API compatibility between versions."""

    def __init__(self, src_path: str = "src"):
        self.src_path = Path(src_path)
        self.current_api = {}
        self.baseline_api = {}

    def extract_fastapi_endpoints(self) -> List[APIEndpoint]:
        """Extract FastAPI endpoints from the codebase."""
        endpoints = []

        # Look for FastAPI routers and apps
        for py_file in self.src_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check for FastAPI decorators
                        for decorator in node.decorator_list:
                            if self._is_fastapi_decorator(decorator):
                                endpoint = self._extract_endpoint_info(node, decorator)
                                if endpoint:
                                    endpoints.append(endpoint)

            except Exception as e:
                print(f"Warning: Could not parse {py_file}: {e}")

        return endpoints

    def _is_fastapi_decorator(self, decorator) -> bool:
        """Check if a decorator is a FastAPI route decorator."""
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr in ['get', 'post', 'put', 'delete', 'patch']
            elif isinstance(decorator.func, ast.Name):
                return decorator.func.id in ['get', 'post', 'put', 'delete', 'patch']
        return False

    def _extract_endpoint_info(self, node, decorator) -> APIEndpoint:
        """Extract endpoint information from AST node."""
        # Get HTTP method
        if isinstance(decorator.func, ast.Attribute):
            method = decorator.func.attr.upper()
        elif isinstance(decorator.func, ast.Name):
            method = decorator.func.id.upper()
        else:
            return None

        # Get path
        path = "unknown"
        if decorator.args:
            if isinstance(decorator.args[0], ast.Constant):
                path = decorator.args[0].value

        # Get parameters
        parameters = []
        for arg in node.args.args:
            if arg.arg != 'self':
                parameters.append(arg.arg)

        # Get return type
        return_type = "Any"
        if node.returns:
            return_type = ast.unparse(node.returns)

        return APIEndpoint(
            path=path,
            method=method,
            parameters=parameters,
            return_type=return_type,
            description=ast.get_docstring(node) or ""
        )

    def extract_public_functions(self) -> List[APIFunction]:
        """Extract public functions from the codebase."""
        functions = []

        for py_file in self.src_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Only include public functions (not starting with _)
                        if not node.name.startswith('_'):
                            # Get parameters
                            parameters = []
                            for arg in node.args.args:
                                if arg.arg != 'self':
                                    parameters.append(arg.arg)

                            # Get return type
                            return_type = "Any"
                            if node.returns:
                                return_type = ast.unparse(node.returns)

                            function = APIFunction(
                                name=node.name,
                                parameters=parameters,
                                return_type=return_type,
                                module=str(py_file.relative_to(self.src_path)),
                                description=ast.get_docstring(node) or ""
                            )
                            functions.append(function)

            except Exception as e:
                print(f"Warning: Could not parse {py_file}: {e}")

        return functions

    def get_current_api(self) -> Dict[str, Any]:
        """Get the current API definition."""
        return {
            'endpoints': [
                {
                    'path': ep.path,
                    'method': ep.method,
                    'parameters': ep.parameters,
                    'return_type': ep.return_type
                }
                for ep in self.extract_fastapi_endpoints()
            ],
            'functions': [
                {
                    'name': func.name,
                    'parameters': func.parameters,
                    'return_type': func.return_type,
                    'module': func.module
                }
                for func in self.extract_public_functions()
            ]
        }

    def get_baseline_api(self, baseline_ref: str = "main") -> Dict[str, Any]:
        """Get the baseline API definition from git."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the baseline version
            subprocess.run([
                'git', 'clone', '--depth', '1', '--branch', baseline_ref,
                '.', temp_dir
            ], check=True, capture_output=True)

            # Create checker for baseline
            baseline_checker = APICompatibilityChecker(
                src_path=str(Path(temp_dir) / "src")
            )

            return baseline_checker.get_current_api()

    def compare_apis(self,
        current_api: Dict[str,
        Any],
        baseline_api: Dict[str,
        Any]) -> Dict[str,
        List[str]]:
        """Compare current API with baseline API."""
        breaking_changes = []
        additions = []
        modifications = []

        # Compare endpoints
        current_endpoints = {
            f"{ep['method']} {ep['path']}" for ep in current_api['endpoints']
        }
        baseline_endpoints = {
            f"{ep['method']} {ep['path']}" for ep in baseline_api['endpoints']
        }

        # Check for removed endpoints
        removed_endpoints = baseline_endpoints - current_endpoints
        for endpoint in removed_endpoints:
            breaking_changes.append(f"Removed endpoint: {endpoint}")

        # Check for added endpoints
        added_endpoints = current_endpoints - baseline_endpoints
        for endpoint in added_endpoints:
            additions.append(f"Added endpoint: {endpoint}")

        # Check for modified endpoints
        for current_ep in current_api['endpoints']:
            current_key = f"{current_ep['method']} {current_ep['path']}"
            baseline_ep = next(
                (ep for ep in baseline_api['endpoints']
                 if f"{ep['method']} {ep['path']}" == current_key),
                None
            )

            if baseline_ep:
                # Check parameter changes
                current_params = set(current_ep['parameters'])
                baseline_params = set(baseline_ep['parameters'])

                if current_params != baseline_params:
                    removed_params = baseline_params - current_params
                    added_params = current_params - baseline_params

                    if removed_params:
                        breaking_changes.append(
                            f"Removed parameters from {current_key}: {',
                                '.join(removed_params)}"
                        )
                    if added_params:
                        modifications.append(
                            f"Added parameters to {current_key}: {',
                                '.join(added_params)}"
                        )

                # Check return type changes
                if current_ep['return_type'] != baseline_ep['return_type']:
                    breaking_changes.append(
                        f"Changed return type for {current_key}: "
                        f"{baseline_ep['return_type']} -> {current_ep['return_type']}"
                    )

        # Compare functions
        current_functions = {func['name'] for func in current_api['functions']}
        baseline_functions = {func['name'] for func in baseline_api['functions']}

        # Check for removed functions
        removed_functions = baseline_functions - current_functions
        for function in removed_functions:
            breaking_changes.append(f"Removed function: {function}")

        # Check for added functions
        added_functions = current_functions - baseline_functions
        for function in added_functions:
            additions.append(f"Added function: {function}")

        return {
            'breaking_changes': breaking_changes,
            'additions': additions,
            'modifications': modifications
        }

    def check_compatibility(self, baseline_ref: str = "main") -> Dict[str, Any]:
        """Check API compatibility with baseline."""
        try:
            current_api = self.get_current_api()
            baseline_api = self.get_baseline_api(baseline_ref)

            comparison = self.compare_apis(current_api, baseline_api)

            return {
                'status': 'breaking' if comparison['breaking_changes'] else 'compatible',
                    
                'summary': {
                    'breaking_changes': len(comparison['breaking_changes']),
                    'additions': len(comparison['additions']),
                    'modifications': len(comparison['modifications'])
                },
                'details': comparison
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'summary': {'breaking_changes': 0, 'additions': 0, 'modifications': 0},
                'details': {'breaking_changes': [],
                    'additions': [],
                    'modifications': []}
            }


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description='Check API compatibility')
    parser.add_argument('--baseline',
        default='main',
        help='Baseline reference (default: main)')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--src-path',
        default='src',
        help='Source code path (default: src)')

    args = parser.parse_args()

    checker = APICompatibilityChecker(src_path=args.src_path)
    result = checker.check_compatibility(args.baseline)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"API Compatibility Check Results")
        print(f"Status: {result['status']}")
        print(f"Summary: {result['summary']}")

        if result['details']['breaking_changes']:
            print("\n⚠️  Breaking Changes:")
            for change in result['details']['breaking_changes']:
                print(f"  - {change}")

        if result['details']['additions']:
            print("\n✅ Additions:")
            for addition in result['details']['additions']:
                print(f"  - {addition}")

        if result['details']['modifications']:
            print("\n🔄 Modifications:")
            for modification in result['details']['modifications']:
                print(f"  - {modification}")

    # Exit with error code if breaking changes found
    if result['status'] == 'breaking':
        sys.exit(1)

if __name__ == "__main__":
    main()
