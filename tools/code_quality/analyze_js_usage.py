#!/usr/bin/env python3
"""
Analyze JavaScript/JSX files for unused imports and modules.
"""

import re
import os
from pathlib import Path
from typing import Set, Dict, List


def extract_imports(file_content: str) -> Set[str]:
    """Extract import statements from JavaScript/JSX content."""
    imports = set()
    
    # Match ES6 imports
    import_patterns = [
        r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",  # import ... from 'module'
        r"import\s+['\"]([^'\"]+)['\"]",  # import 'module'
        r"require\(['\"]([^'\"]+)['\"]\)",  # require('module')
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, file_content)
        imports.update(matches)
    
    return imports


def extract_exports(file_content: str) -> Set[str]:
    """Extract export statements from JavaScript/JSX content."""
    exports = set()
    
    # Match exports
    export_patterns = [
        r"export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)",
        r"export\s+\{\s*([^}]+)\s*\}",
        r"export\s+default\s+(\w+)",
    ]
    
    for pattern in export_patterns:
        matches = re.findall(pattern, file_content)
        for match in matches:
            if isinstance(match, str):
                if '{' in match:  # Handle export { name1, name2 }
                    names = [name.strip() for name in match.split(',')]
                    exports.update(names)
                else:
                    exports.add(match)
    
    return exports


def analyze_js_files(webui_path: Path) -> Dict[str, Dict]:
    """Analyze JavaScript files for usage patterns."""
    js_files = {}
    
    # Find all JS/JSX files
    for ext in ['*.js', '*.jsx']:
        for js_file in webui_path.rglob(ext):
            if 'node_modules' in str(js_file) or 'dist' in str(js_file):
                continue
                
            try:
                content = js_file.read_text(encoding='utf-8')
                
                js_files[str(js_file)] = {
                    'path': js_file,
                    'imports': extract_imports(content),
                    'exports': extract_exports(content),
                    'size': len(content),
                    'lines': len(content.splitlines())
                }
            except Exception as e:
                print(f"Error reading {js_file}: {e}")
    
    return js_files


def find_unused_modules(js_files: Dict[str, Dict]) -> List[str]:
    """Find JavaScript modules that are never imported."""
    all_files = set(js_files.keys())
    imported_modules = set()
    
    # Collect all imported modules
    for file_info in js_files.values():
        for imp in file_info['imports']:
            # Resolve relative imports
            if imp.startswith('./') or imp.startswith('../'):
                # This is a relative import to another project file
                base_path = file_info['path'].parent
                resolved = (base_path / imp).resolve()
                
                # Check for .js/.jsx extensions
                for ext in ['.js', '.jsx']:
                    if resolved.with_suffix(ext).exists():
                        imported_modules.add(str(resolved.with_suffix(ext)))
                        break
                else:
                    # Try without extension
                    if resolved.exists():
                        imported_modules.add(str(resolved))
    
    # Find unused modules
    unused = []
    for file_path in all_files:
        if file_path not in imported_modules:
            file_info = js_files[file_path]
            # Skip main entry points and test files
            if not any(x in str(file_info['path']) for x in ['main.', 'index.', 'App.', 'test', 'spec']):
                unused.append(file_path)
    
    return unused


def main():
    """Main analysis function."""
    webui_path = Path(__file__).parent.parent.parent / 'webui'
    
    if not webui_path.exists():
        print("WebUI directory not found")
        return
    
    print("🔍 Analyzing JavaScript/JSX files...")
    js_files = analyze_js_files(webui_path)
    
    print(f"📁 Found {len(js_files)} JavaScript/JSX files")
    
    # Find unused modules
    unused = find_unused_modules(js_files)
    
    if unused:
        print(f"\n❓ Potentially unused modules ({len(unused)}):")
        for file_path in unused:
            file_info = js_files[file_path]
            relative_path = file_info['path'].relative_to(webui_path)
            print(f"  📄 {relative_path} ({file_info['lines']} lines)")
    else:
        print("\n✅ No obviously unused modules found")
    
    # Find small/empty files
    small_files = [f for f in js_files.values() if f['lines'] < 10]
    if small_files:
        print(f"\n📏 Small files (<10 lines) that might be stubs:")
        for file_info in small_files:
            relative_path = file_info['path'].relative_to(webui_path)
            print(f"  📄 {relative_path} ({file_info['lines']} lines)")


if __name__ == '__main__':
    main()
