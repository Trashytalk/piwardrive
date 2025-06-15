from setuptools import setup, Extension, find_packages

setup(
    name="piwardrive",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=[
        Extension("ckml", ["ckml.c"]),
        Extension("cgeom", ["cgeom.c"]),
    ],
    entry_points={
        "console_scripts": [
            "piwardrive=piwardrive.main:main",
            "piwardrive-service=piwardrive.service:main",
        ]
    },
)
