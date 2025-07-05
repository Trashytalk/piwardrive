#!/usr/bin/env python3
"""
Final summary and cleanup script
"""
import subprocess
from pathlib import Path


def run_command(cmd: str, description: str) -> tuple[int, str]:
    """Run a command and return exit code and output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=Path.cwd()
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)


def main():
    print("🔧 PiWarDrive Code Quality Summary")
    print("=" * 50)

    # Activate virtual environment
    venv_activate = "source venv/bin/activate"

    # Run each tool and summarize results
    tools = [
        (
            "Black (Python formatting)",
            f"{venv_activate} && black --check --diff src/ --quiet",
        ),
        (
            "isort (Import sorting)",
            f"{venv_activate} && isort --check-only --diff src/",
        ),
        (
            "flake8 (Code style)",
            f"{venv_activate} && flake8 --config=config/.flake8 src/ --count --statistics",
        ),
        (
            "Prettier (JS/TS formatting)",
            "npx prettier --check '**/*.js' '**/*.jsx' '**/*.ts' --config webui/.prettierrc",
        ),
    ]

    results = {}

    for tool_name, command in tools:
        print(f"\n📋 Running {tool_name}...")
        exit_code, output = run_command(command, tool_name)

        if exit_code == 0:
            print(f"✅ {tool_name}: PASSED")
            results[tool_name] = "PASSED"
        else:
            print(f"⚠️  {tool_name}: Issues found")
            results[tool_name] = "ISSUES"
            if output.strip():
                # Show summary of issues
                lines = output.strip().split("\n")
                if len(lines) > 10:
                    print("   " + "\n   ".join(lines[-10:]))  # Show last 10 lines
                else:
                    print("   " + "\n   ".join(lines))

    # Summary
    print("\n" + "=" * 50)
    print("🎯 SUMMARY:")
    print("=" * 50)

    for tool, status in results.items():
        status_icon = "✅" if status == "PASSED" else "⚠️"
        print(f"{status_icon} {tool}: {status}")

    # Recommendations
    print("\n🚀 What's been fixed:")
    print("• Python code formatting with Black")
    print("• Import organization with isort")
    print("• JavaScript/TypeScript formatting with Prettier")
    print("• Trailing whitespace and blank lines")
    print("• Some unused variables and f-string issues")

    print("\n📝 Remaining issues to address manually:")
    print("• Some unused imports (F401 errors)")
    print("• Module-level imports not at top (E402 errors)")
    print("• A few undefined names that need context to fix")
    print("• Some remaining unused variables in complex functions")

    # Create configuration summary
    print("\n⚙️  Tool Configurations:")
    configs = [
        ("pyproject.toml", "pytest, mypy, black, isort, coverage configurations"),
        ("config/.flake8", "flake8 configuration"),
        ("config/mypy.ini", "mypy type checking configuration"),
        ("webui/.prettierrc", "Prettier JavaScript formatting configuration"),
    ]

    for config_file, description in configs:
        if Path(config_file).exists():
            print(f"✅ {config_file}: {description}")
        else:
            print(f"❌ {config_file}: Missing")


if __name__ == "__main__":
    main()
