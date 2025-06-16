from setuptools import setup, Extension, find_packages

setup(
    name="piwardrive",
    version="0.1.0",
    packages=find_packages(exclude=("tests*", "docs*", "benchmarks*", "examples*")),
    py_modules=[
        "analysis",
        "ckml",
        "config",
        "di",
        "diagnostics",
        "exception_handler",
        "export",
        "gpsd_client",
        "interfaces",
        "localization",
        "logconfig",
        "main",
        "persistence",
        "r_integration",
        "scheduler",
        "security",
        "service",
        "utils",
    ],
    data_files=[("", ["py.typed"])],
    ext_modules=[
        Extension("ckml", ["ckml.c"]),
        Extension("cgeom", ["cgeom.c"]),
    ],
    python_requires=">=3.10",
)
