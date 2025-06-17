"""Entry point for setup module."""
from pathlib import Path
from setuptools import setup, Extension, find_packages
try:  # Python >=3.11
    import tomllib  # type: ignore
except ModuleNotFoundError:  # Python <=3.10
    import tomli as tomllib  # type: ignore


def load_project_config():
    """Parse project metadata from ``pyproject.toml``."""
    with open(Path(__file__).parent / "pyproject.toml", "rb") as f:
        return tomllib.load(f)


config = load_project_config()
project = config.get("project", {})
package_cfg = (
    config.get("tool", {})
    .get("setuptools", {})
    .get("packages", {})
    .get("find", {})
)


setup(
    name=project.get("name", "piwardrive"),
    version=project.get("version", "0.0.0"),
    description=project.get("description", ""),
    long_description=Path(project.get("readme", "README.md")).read_text(
        encoding="utf-8"
    ),
    long_description_content_type="text/markdown",
    python_requires=project.get("requires-python", ">=3.10"),
    packages=find_packages(where="src", exclude=("tests*", "docs*", "benchmarks*", "examples*")),
    package_dir={"": "src"},
    data_files=[("", ["src/piwardrive/py.typed"])],
    ext_modules=[
        Extension("piwardrive.ckml", ["src/piwardrive/ckml.c"]),
        Extension("piwardrive.cgeom", ["src/piwardrive/cgeom.c"]),
    ],
)
