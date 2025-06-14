from setuptools import setup, Extension

setup(
    name='ckml',
    version='0.1',
    ext_modules=[Extension('ckml', ['ckml.c'])],
)
